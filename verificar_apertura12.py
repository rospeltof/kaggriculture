"""Verify opening execution, complete development grid, exact parent controls."""
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import tarfile

from construir_apertura12 import OUT as AGENTS, EVIDENCE as OUT


def main():
    data=json.loads((OUT/'opening12_smoke.json').read_text());rows=data['results'];plan=data['plan']
    manifest=json.loads((AGENTS/'manifest.json').read_text())
    keyed={(r['arm'],r['opponent'],r['seed'],r['seat']):r for r in rows}
    expected={(name,op,seed,seat) for name in plan['agents'] for op in plan['opponents'] for seed in plan['seeds'] for seat in (0,1)}
    assert len(rows)==len(keyed)==48 and set(keyed)==expected
    with tarfile.open(OUT/'opening12_smoke.sources.tgz') as tar:
        for name,spec in plan['agents'].items():
            assert hashlib.sha256(Path(spec['path']).read_bytes()).hexdigest()==spec['sha256']
            assert hashlib.sha256(tar.extractfile(f'agents/{name}.py').read()).hexdigest()==spec['sha256']
        for name,spec in plan['opponents'].items():
            assert hashlib.sha256(Path(spec['path']).read_bytes()).hexdigest()==spec['sha256']
            assert hashlib.sha256(tar.extractfile(f'opponents/{name}.py').read()).hexdigest()==spec['sha256']
    noops=0;activation=Counter();opening_checks=0;summaries=[]
    for row in rows:
        name,op,seed,seat=row['arm'],row['opponent'],row['seed'],row['seat']
        assert row['max_turn_ms']<1000
        assert not any(v for d in row['reports'].values() for k,v in d.items() if 'error' in k and isinstance(v,(int,float)))
        if name in ('base','top3'):continue
        spec=manifest[name];base=keyed[spec['behavior_reference'],op,seed,seat]
        assert row['reports']['_OPN_REPORT']['opening_calls']==1 and row['reports']['_OPN_REPORT']['initial_wheat']==5
        assert [e['step'] for e in row['edits']]==[0,1] and len(row['daily_min_cash'])==30
        if not spec['config']['enabled']:
            assert row['action_hashes']==base['action_hashes'] and row['rewards']==base['rewards']
            assert row['changed_own_turns']==row['changed_rival_turns']==0;noops+=719
        ledger=[json.loads(l) for l in gzip.decompress((OUT/f'opening12_smoke.{op}.{seed}.{name}.{seat}.ledger.jsonl.gz').read_bytes()).splitlines()]
        own=[e for e in ledger if e['player']==seat]
        assert 3000+sum(e['value'] for e in own)==row['rewards'][seat]
        buys=[e for e in own if e['step']==0 and e['op']=='BUY_PRODUCT' and e['item']=='WHEAT']
        sales=[e for e in own if e['step']==0 and e['op']=='SELL' and e['item']=='WHEAT']
        q=spec['config']['quantity'];assert len(buys)==q and len(sales)==q-5
        wheat=[o for o in row['edits'][0]['market'] if len(o)>=3 and o[1]=='WHEAT' and o[0] in ('BUY_PRODUCT','SELL')]
        assert wheat==[['BUY_PRODUCT','WHEAT',q],['SELL','WHEAT',q-5]]
        assert not any(e['step']==1 and e['op'] in ('BUY_PRODUCT','SELL') and e['item']=='WHEAT' for e in own)
        opening_checks+=1
        if not spec['config']['enabled']:continue
        activation[name]+=row['changed_own_turns']>0
        summaries.append(dict(arm=name,opponent=op,seed=seed,seat=seat,changed_own_turns=row['changed_own_turns'],
                              same_shops=row['same_shops'],same_work=row['accepted']==base['accepted'],
                              same_harvest=row['harvested']==base['harvested'],same_losses=row['nights']==base['nights'],
                              escapes=row['escapes'],base_margin=base['margin'],candidate_margin=row['margin'],
                              min_cash=min(row['daily_min_cash'].values()),daily_min_cash=row['daily_min_cash'],
                              step1_cash=row['edits'][1]['money'],opening_wheat_cash=sum(e['value'] for e in buys+sales)))
    candidates={n:r for n,r in manifest.items() if r['config']['enabled']}
    assert noops==11504 and opening_checks==32 and all(activation[n]>0 for n in candidates)
    result=dict(passed=True,competitive_ready=True,games=48,noop_exact_turns=noops,
                max_turn_ms=max(r['max_turn_ms'] for r in rows),activated_cells=dict(activation),opening_checks=opening_checks,
                candidate_hashes={n:r['sha256'] for n,r in candidates.items()},base_hash=plan['agents']['base']['sha256'],
                control_hash=plan['agents']['top3']['sha256'],summary=summaries,
                note='Only opening size differs; exact fills/stock5 and noops. Later physical behavior and margins reported, no development reward selection.')
    (OUT/'opening12_validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='summary'}))


if __name__=='__main__':main()
