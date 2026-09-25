"""Check predicted stock against observations and actual new-worker pickups."""
import contextlib
import gzip
import hashlib
import io
import json
from pathlib import Path

from verificar_alimentacion_economica import main as verify_execution

OUT = Path('docs/evidencia/loop_publicos_20260925')


def main():
    tags = [('sheep_supply_smoke',24), *[(f'sheep_supply_coverage_{r}',8)
                                      for r in ('vq','public_v7','public_hs4')]]
    manifest = json.loads((OUT/'sheep_supply_variants.json').read_text())
    activation = {n:0 for n in manifest}; checks = []; validations = []; equivalence = []
    for tag, games in tags:
        with contextlib.redirect_stdout(io.StringIO()):
            validations.append(verify_execution(tag=tag,manifest_file='sheep_supply_variants.json',
                output_file=tag+'.execution.json',expected_games=games,noop_name='sheep_supply_noop'))
        rows = json.loads((OUT/(tag+'.json')).read_text())
        keyed = {(r['arm'],r['seed'],r['seat']):r for r in rows}
        for row in rows:
            if row['arm'] != 'sheep_supply_buy': continue
            other = keyed['sheep_supply_hold',row['seed'],row['seat']]
            equivalence.append(dict(tag=tag,seed=row['seed'],seat=row['seat'],
                both_actions_and_rewards_equal=(row['action_hash'],row['rewards'])==(other['action_hash'],other['rewards'])))
        for row in rows:
            if row['arm'] not in manifest: continue
            events = row['layer_events']['_SS_EVENTS']; stats = row['reports']['_SS_REPORT']
            units = [json.loads(l) for l in gzip.decompress((OUT/f"{tag}.{row['seed']}.{row['arm']}.{row['seat']}.units.jsonl.gz").read_bytes()).decode().splitlines()]
            ledger = [json.loads(l) for l in gzip.decompress((OUT/f"{tag}.{row['seed']}.{row['arm']}.{row['seat']}.ledger.jsonl.gz").read_bytes()).decode().splitlines()]
            assert stats['changes']==len(events) and stats['errors']==stats['prediction_errors']==0
            for event in events:
                step = event['step']; before = event['original']; after = event['modified']
                assert step//24 < 28 and step%24 != 23
                assert event['observed_step']==step+1
                assert event['observed_next']==event['predicted_after']>=event['need']
                assert event['need']==event['native_need']+event['hungry']
                assert 0<event['hungry']<=6 and event['predicted_before']<event['need']
                assert len(after)<=10 and len(after) in (len(before),len(before)+1)
                for i,old in enumerate(before):
                    if old!=after[i]:
                        assert old[:2]==after[i][:2] and old[:2] in (['SELL','WHEAT'],['BUY_PRODUCT','WHEAT'])
                        assert (after[i][2]<=old[2] if old[0]=='SELL' else after[i][2]>=old[2])
                if len(after)>len(before): assert after[-1][:2]==['BUY_PRODUCT','WHEAT']
                pickups = [u for u in units if u['step']==step+1 and u['actor']==event['actor'] and u['action'][:2]==['PICKUP','WHEAT']]
                assert len(pickups)==1 and pickups[0]['inventory_delta'].get('WHEAT',0)>=event['hungry'], (row['arm'],step,pickups)
                accepted = [e for e in ledger if e['step']==step and e['player']==row['seat'] and e['op']=='BUY_PRODUCT' and e['item']=='WHEAT']
                requested = sum(o[2] for o in after if o[:2]==['BUY_PRODUCT','WHEAT'])
                assert len(accepted)==requested, (step,len(accepted),requested)
                checks.append(dict(tag=tag,arm=row['arm'],seed=row['seed'],seat=row['seat'],step=step,
                                   need=event['need'],predicted=event['predicted_after'],actual=event['observed_next'],
                                   accepted_buy=len(accepted),worker_pickup=pickups[0]['inventory_delta']['WHEAT']))
            activation[row['arm']]+=len(events)
    directed=json.loads((OUT/'davion_general_supply_probe.json').read_text())
    assert directed['plan']['candidate_sha256']==manifest['sheep_supply_buy']['sha256']
    assert directed['results'][1]['accepted_wheat601']==11
    assert directed['results'][1]['worker'][1]['wheat']==0
    assert directed['results'][1]['worker'][2]['wheat']==6
    assert all(activation.values()), activation
    report=dict(passed=True,competitive_ready=True,development_games=sum(n for _,n in tags),
                noop_exact_turns=sum(v['noop_exact_turns'] for v in validations),
                max_turn_ms=max(v['max_turn_ms'] for v in validations),activation=activation,pickup_checks=checks,
                buy_hold_equivalence=equivalence,
                candidate_hashes={n:r['sha256'] for n,r in manifest.items()},
                control_hash=hashlib.sha256(Path('submission/main_publico_arshs3_vq.py').read_bytes()).hexdigest(),
                note='Actual field pickups, accepted market buys, next stock, noop, cash and source hashes verified. Directed coverage is not population effectiveness; no reward-based development selection.')
    (OUT/'sheep_supply_validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    return report


if __name__=='__main__': main()
