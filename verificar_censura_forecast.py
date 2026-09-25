"""Validate observation masks, exact parent noops and emitted-action coverage."""
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import tarfile

from construir_censura_forecast import OUT as AGENTS, EVIDENCE as OUT


def read_lines(path):
    return [json.loads(line) for line in gzip.decompress(path.read_bytes()).decode().splitlines()]


def main():
    data=json.loads((OUT/'forecast_censor_smoke.json').read_text())
    rows=data['results'];plan=data['plan'];manifest=json.loads((AGENTS/'manifest.json').read_text())
    keyed={(r['arm'],r['seed'],r['seat']):r for r in rows}
    expected={(name,seed,seat) for name in plan['agents'] for seed in plan['seeds'] for seat in (0,1)}
    assert len(rows)==len(keyed)==48 and set(keyed)==expected
    with tarfile.open(OUT/'forecast_censor_smoke.sources.tgz') as tar:
        for name,spec in plan['agents'].items():
            assert hashlib.sha256(Path(spec['path']).read_bytes()).hexdigest()==spec['sha256']
            assert hashlib.sha256(tar.extractfile(f'agents/{name}.py').read()).hexdigest()==spec['sha256']
        assert hashlib.sha256(tar.extractfile('opponent.py').read()).hexdigest()==plan['opponent']['sha256']
    noops=0;activation=Counter();rankings=Counter();checks=0;observables=0;summaries=[]
    for row in rows:
        name=row['arm'];seed=row['seed'];seat=row['seat']
        assert row['max_turn_ms']<1000
        assert not any(v for d in row['reports'].values() for k,v in d.items() if 'error' in k and isinstance(v,(int,float)))
        if name in ('base','top3'):continue
        spec=manifest[name];base=keyed[spec['behavior_reference'],seed,seat]
        if not spec['config']['enabled']:
            assert row['action_hashes']==base['action_hashes'] and row['rewards']==base['rewards']
            assert row['changed_own_turns']==row['changed_rival_turns']==0
            noops+=719;continue
        stem=f'forecast_censor_smoke.{seed}.{name}.{seat}'
        masks=read_lines(OUT/f'{stem}.masks.jsonl.gz');snapshots=read_lines(OUT/f'{stem}.snapshots.jsonl.gz')
        ledger=read_lines(OUT/f'{stem}.ledger.jsonl.gz')
        assert len(masks)==718 and [r['step'] for r in masks]==list(range(718))
        accepted=Counter((e['step'],e['player'],e['item']) for e in ledger if e['op']=='SELL')
        added=Counter((e['step'],e['player'],e['item']) for e in ledger if e['op']=='SELL' and e['value']>1)
        for mask in masks:
            t=mask['step'];assert len(mask['visible'])==5
            for item,visible in mask['visible'].items():
                checks+=1
                native=snapshots[t]['prices'].get(item,0)>3
                if spec['config']['mode']=='native':assert visible==native
                else:
                    assert not visible or native
                    if visible:
                        observables+=1
                        assert sum(accepted[t,p,item] for p in (0,1))==sum(added[t,p,item] for p in (0,1)),(name,seed,seat,t,item)
        report=row['reports']['_CF_REPORT']
        assert report['item_turns']==3590 and report['forecasts']==275
        assert report['ignored_penalties']>0
        activation[name]+=row['changed_own_turns']>0;rankings[name]+=report['changed_rankings']
        private=row['terminal_private'][0]
        summaries.append(dict(arm=name,seed=seed,seat=seat,changed_own_turns=row['changed_own_turns'],
                              changed_rankings=report['changed_rankings'],unobservable=report['unobservable'],
                              same_shops=row['same_shops'],same_work=row['accepted']==base['accepted'],
                              same_harvest=row['harvested']==base['harvested'],same_losses=row['nights']==base['nights'],
                              escapes=row['escapes'],terminal_products=sum(private['shed'].values())+sum(sum(b.values()) for b in private['inventories']),
                              base_margin=base['margin'],candidate_margin=row['margin']))
    candidates={n:r for n,r in manifest.items() if r['config']['enabled']}
    assert noops==8628 and checks==86160
    assert all(activation[n]>0 and rankings[n]>0 for n in candidates)
    result=dict(passed=True,competitive_ready=True,games=48,noop_exact_turns=noops,
                max_turn_ms=max(r['max_turn_ms'] for r in rows),activated_cells=dict(activation),changed_rankings=dict(rankings),
                mask_item_checks=checks,observable_market_checks=observables,
                candidate_hashes={n:r['sha256'] for n,r in candidates.items()},
                base_hash=plan['agents']['base']['sha256'],control_hash=plan['agents']['top3']['sha256'],summary=summaries,
                note='Floor-observable item-turns never contain invisible accepted sales in development. No claim of improved prediction accuracy, WLT or unchanged future physical production.')
    (OUT/'forecast_censor_validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='summary'}))


if __name__=='__main__':main()
