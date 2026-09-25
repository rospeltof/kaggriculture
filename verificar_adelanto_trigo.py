"""Verify earlier fills, native repayment, both parent controls and field effects."""
import contextlib
import gzip
import io
import json
from pathlib import Path

from verificar_alimentacion_economica import main as verify_execution

OUT=Path('docs/evidencia/loop_publicos_20260925')
TAG='advance_wheat_smoke'


def main():
    with contextlib.redirect_stdout(io.StringIO()):
        common=verify_execution(tag=TAG,manifest_file='advance_wheat_variants.json',
            output_file='advance_wheat_execution.json',expected_games=36,noop_name='advance_noop_vq')
    rows=json.loads((OUT/(TAG+'.json')).read_text());keyed={(r['arm'],r['seed'],r['seat']):r for r in rows}
    manifest=json.loads((OUT/'advance_wheat_variants.json').read_text());summary=[];checks=[]
    for seed in sorted({r['seed'] for r in rows}):
        for seat in (0,1):
            ref=keyed['ref_top3',seed,seat];noop=keyed['advance_noop_top3',seed,seat]
            assert (ref['action_hash'],ref['rewards'])==(noop['action_hash'],noop['rewards'])
    activation={n:0 for n in manifest}
    for row in rows:
        if row['arm'] not in manifest:continue
        refname='base' if manifest[row['arm']]['config']['parent']=='vq' else 'ref_top3'
        ref=keyed[refname,row['seed'],row['seat']]
        stats=row['reports']['_BW_REPORT'];events=row['layer_events']['_BW_EVENTS']
        assert stats['advances']==len(events)
        assert stats['bought']==stats['cancelled']==sum(e['bought'] for e in events)
        ledger=[json.loads(l) for l in gzip.decompress((OUT/f"{TAG}.{row['seed']}.{row['arm']}.{row['seat']}.ledger.jsonl.gz").read_bytes()).decode().splitlines()]
        owned=[e for e in ledger if e['player']==row['seat'] and e['op']=='BUY_PRODUCT' and e['item']=='WHEAT']
        for event in events:
            step=event['step'];assert event['observed_step']==event['due']==step+1
            assert 288<=step<=693 and step%24<=21 and event['native_quantity']>=20
            assert event['next_sale']>=(event['native_quantity']+1)//2
            assert event['modified'][:-1]==event['original']
            assert event['modified'][-1]==['BUY_PRODUCT','WHEAT',event['quantity']]
            assert not any(o[:2] in (['BUY_PRODUCT','WHEAT'],['SELL','WHEAT']) for o in event['original'])
            assert event['hook_calls']>0 and event['native_next']['market'][event['native_index']]==['BUY_PRODUCT','WHEAT',event['native_quantity']]
            buys=[e for e in owned if e['step']==step];after=[e for e in owned if e['step']==step+1]
            assert len(buys)==event['bought']==event['quantity']
            # A reactive food guard could add an independent purchase. These
            # development worlds must be inspected if that ever occurs.
            remaining=max(0,event['native_quantity']-event['bought'])
            emitted=sum(o[2] for o in event['final_market'] if len(o)>=3 and o[:2]==['BUY_PRODUCT','WHEAT'])
            assert emitted<=remaining,(row['arm'],step,event)
            assert len(after)<=emitted
            checks.append(dict(arm=row['arm'],seed=row['seed'],seat=row['seat'],step=step,
                requested=event['quantity'],bought=len(buys),cancelled=event['bought'],native_remaining=remaining,
                following_request=emitted,following_accepted=len(after),buy_cash=sum(e['value'] for e in buys)))
        activation[row['arm']]+=len(events)
        summary.append(dict(arm=row['arm'],seed=row['seed'],seat=row['seat'],reference=refname,
            advances=len(events),both_actions_and_rewards_equal=(row['action_hash'],row['rewards'])==(ref['action_hash'],ref['rewards']),
            same_shops=row['shops']==ref['shops'],feed_base={k:v for k,v in ref['successful'].items() if k.startswith('FEED:')},
            feed_candidate={k:v for k,v in row['successful'].items() if k.startswith('FEED:')},
            harvest_base=ref['harvested'],harvest_candidate=row['harvested'],losses_base=ref['losses'],losses_candidate=row['losses'],
            wheat_buy_base=ref['flows'].get('BUY_PRODUCT:WHEAT'),wheat_buy_candidate=row['flows'].get('BUY_PRODUCT:WHEAT'),
            wheat_sale_base=ref['flows'].get('SELL:WHEAT'),wheat_sale_candidate=row['flows'].get('SELL:WHEAT'),escapes=row['escapes']))
    assert all(activation.values()),activation
    common.update(competitive_ready=True,noop_exact_turns=common['noop_exact_turns']*2,
                  activation=activation,summary=summary,transaction_checks=checks,
                  control_hash='9668e30ad08f79d485bd230a3c660d4cc420b9382e87f9387b6908e3c94a5145',
                  note='Both parent noops, sources, actual earlier fills and no duplicated native purchase verified. Earlier stock can also advance sales and change production; development outcomes do not select arms.')
    (OUT/'advance_wheat_validation.json').write_text(json.dumps(common,indent=2)+'\n')
    print(json.dumps({k:v for k,v in common.items() if k not in ('summary','transaction_checks')},indent=2))
    for row in summary:print(json.dumps(row))
    return common


if __name__=='__main__':main()
