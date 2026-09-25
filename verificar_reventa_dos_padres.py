"""Loop29: exact parent controls and physical buy/close receipts, no new games."""
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import tarfile

from construir_reventa_dos_padres import OUT as AGENTS, EVIDENCE as OUT


def main():
    data=json.loads((OUT/'town_factorial_smoke.json').read_text());rows=data['results'];plan=data['plan']
    manifest=json.loads((AGENTS/'manifest.json').read_text())
    keyed={(r['arm'],r['seed'],r['seat']):r for r in rows}
    expected={(name,seed,seat) for name in plan['agents'] for seed in plan['seeds'] for seat in (0,1)}
    assert len(rows)==len(keyed)==48 and set(keyed)==expected
    with tarfile.open(OUT/'town_factorial_smoke.sources.tgz') as tar:
        for name,spec in plan['agents'].items():
            assert hashlib.sha256(Path(spec['path']).read_bytes()).hexdigest()==spec['sha256']
            assert hashlib.sha256(tar.extractfile(f'agents/{name}.py').read()).hexdigest()==spec['sha256']
        assert hashlib.sha256(tar.extractfile('opponent.py').read()).hexdigest()==plan['opponent']['sha256']
    noops=0;activation=Counter();operations=Counter();bought=Counter();sold=Counter();summaries=[]
    for row in rows:
        name,seed,seat=row['arm'],row['seed'],row['seat']
        assert row['max_turn_ms']<1000
        assert not any(v for d in row['reports'].values() for k,v in d.items() if 'error' in k and isinstance(v,(int,float)))
        if name in ('base','top3'):continue
        spec=manifest[name];base=keyed[spec['behavior_reference'],seed,seat]
        if not spec['config']['enabled']:
            assert row['action_hashes']==base['action_hashes'] and row['rewards']==base['rewards']
            assert row['changed_own_turns']==row['changed_rival_turns']==0
            assert not row['edits'];noops+=719;continue
        ledger=[json.loads(l) for l in gzip.decompress((OUT/f'town_factorial_smoke.{seed}.{name}.{seat}.ledger.jsonl.gz').read_bytes()).splitlines()]
        own=[e for e in ledger if e['player']==seat]
        assert 3000+sum(e['value'] for e in own)==row['rewards'][seat]
        buys={e['step']:e for e in row['edits'] if e['kind']=='buy'}
        closes={e['buy_step']:e for e in row['edits'] if e['kind']=='close'}
        stats=row['reports']['_TR_REPORT'];assert set(buys)==set(closes)
        assert stats['buys']==stats['closes']==len(buys)
        assert stats['requested']==sum(e['quantity'] for e in buys.values())
        assert stats['observed_bought']==sum(e['bought'] for e in closes.values())
        legs=[]
        for step,buy in buys.items():
            close=closes[step]
            assert close['step']==step+1 and 288<=step<=695 and step%24 in (4,8,12,16,20)
            assert 0<buy['quantity']<=min(buy['capacity'],spec['config']['max_quantity'])
            assert buy['money']-buy['estimated_cost']>=5000 and buy['drain']>0 and buy['naive_profit']>0
            for action in (buy['original'],buy['native_next']):
                assert not action.get('market')
                assert not any(c and c[0] in ('PICKUP','DROP','PLACE') for c in [action.get('farmer')]+list(action.get('hands') or []))
            paid=[e for e in own if e['step']==step and e['op']=='BUY_PRODUCT' and e['item']=='WHEAT']
            received=[e for e in own if e['step']==step+1 and e['op']=='SELL' and e['item']=='WHEAT']
            assert len(paid)==close['bought']<=buy['quantity']
            assert len(received)==close['quantity']>=close['bought']
            assert close['quantity']==max(close['bought'],close['inherited_sale'])
            if close['bought']:
                assert close['modified'][0]==['SELL','WHEAT',close['quantity']] and len(close['modified'])<=10
            bought[name]+=len(paid);sold[name]+=len(received)
            legs.append(dict(step=step,bought=len(paid),sold=len(received),inherited=close['inherited_sale'],
                             cash=sum(e['value'] for e in paid+received),naive_profit=buy['naive_profit']))
        activation[name]+=row['changed_own_turns']>0;operations[name]+=len(legs)
        summaries.append(dict(arm=name,seed=seed,seat=seat,changed_own_turns=row['changed_own_turns'],
                              same_shops=row['same_shops'],same_work=row['accepted']==base['accepted'],
                              same_harvest=row['harvested']==base['harvested'],same_losses=row['nights']==base['nights'],
                              escapes=row['escapes'],base_margin=base['margin'],candidate_margin=row['margin'],roundtrips=legs))
    candidates={n:r for n,r in manifest.items() if r['config']['enabled']}
    assert noops==8628 and all(activation[n]>0 and operations[n]>0 for n in candidates)
    result=dict(passed=True,competitive_ready=True,games=48,noop_exact_turns=noops,
                max_turn_ms=max(r['max_turn_ms'] for r in rows),activated_cells=dict(activation),operations=dict(operations),
                bought=dict(bought),sold=dict(sold),candidate_hashes={n:r['sha256'] for n,r in candidates.items()},
                base_hash=plan['agents']['base']['sha256'],control_hash=plan['agents']['top3']['sha256'],summary=summaries,
                note='Exact noops, cash and wheat fills. Production changes and roundtrip losses are reported; development cash does not select policies.')
    (OUT/'town_factorial_validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='summary'}))


if __name__=='__main__':main()
