"""Loop31: exact disabled controls, emitted priority and official buy/close receipts."""
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import tarfile

from construir_prioridad_cierre import OUT as AGENTS, EVIDENCE as OUT


def main():
    data=json.loads((OUT/'close_queue_smoke.json').read_text());rows=data['results'];plan=data['plan']
    manifest=json.loads((AGENTS/'manifest.json').read_text())
    keyed={(r['arm'],r['seed'],r['seat']):r for r in rows}
    expected={(name,seed,seat) for name in plan['agents'] for seed in plan['seeds'] for seat in (0,1)}
    assert len(rows)==len(keyed)==48 and set(keyed)==expected
    with tarfile.open(OUT/'close_queue_smoke.sources.tgz') as tar:
        for name,spec in plan['agents'].items():
            assert hashlib.sha256(Path(spec['path']).read_bytes()).hexdigest()==spec['sha256']
            assert hashlib.sha256(tar.extractfile(f'agents/{name}.py').read()).hexdigest()==spec['sha256']
        assert hashlib.sha256(tar.extractfile('opponent.py').read()).hexdigest()==plan['opponent']['sha256']
    noops=0;activation=Counter();operations=Counter();bought=Counter();sold=Counter();summaries=[]
    for row in rows:
        name,seed,seat=row['arm'],row['seed'],row['seat']
        assert row['max_turn_ms']<1000
        assert not any(v for d in row['reports'].values() for k,v in d.items() if 'error' in k and isinstance(v,(int,float)))
        if name in ('base','top3','town50_vq','town50_top3'):continue
        spec=manifest[name];base=keyed[spec['behavior_reference'],seed,seat]
        if not spec['config']['enabled']:
            assert row['action_hashes']==base['action_hashes'] and row['rewards']==base['rewards']
            assert row['changed_own_turns']==row['changed_rival_turns']==0
            assert row['edits']==base['edits'] and not row['queue_edits']
            noops+=719;continue
        ledger=[json.loads(l) for l in gzip.decompress((OUT/f'close_queue_smoke.{seed}.{name}.{seat}.ledger.jsonl.gz').read_bytes()).splitlines()]
        own=[e for e in ledger if e['player']==seat]
        assert 3000+sum(e['value'] for e in own)==row['rewards'][seat]
        buys={e['step']:e for e in row['edits'] if e['kind']=='buy'}
        closes={e['buy_step']:e for e in row['edits'] if e['kind']=='close'}
        stats=row['reports']['_TR_REPORT'];assert set(buys)==set(closes)
        assert stats['buys']==stats['closes']==len(buys)
        assert stats['requested']==sum(e['quantity'] for e in buys.values())
        assert stats['observed_bought']==sum(e['bought'] for e in closes.values())
        queue_events={e['step']:e for e in row['queue_edits']}
        assert set(queue_events)=={e['step'] for e in closes.values()}
        qstats=row['reports']['_CQ_REPORT']
        assert qstats['closes']==len(queue_events)
        assert qstats['reordered']==sum(e['town_computed']!=e['emitted'] for e in queue_events.values())
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
            q=queue_events[step+1]; action=row['emitted_closes'][str(step+1)]
            assert q['native']==close['original'] and q['town_computed']==close['modified']
            assert q['quantity']==close['quantity'] and q['bought']==close['bought']
            original=close['original']; quantity=close['quantity']
            wheat_indices=[i for i,o in enumerate(original) if len(o)>=3 and o[:2]==['SELL','WHEAT']]
            others=[o for o in original if not(len(o)>=3 and o[:2]==['SELL','WHEAT'])]
            if quantity:
                slot=sum(not(len(o)>=3 and o[:2]==['SELL','WHEAT']) for o in original[:wheat_indices[0]]) if wheat_indices else len(others)
                expected=others[:slot]+[['SELL','WHEAT',quantity]]+others[slot:]
            else:expected=original
            assert q['emitted']==expected==action.get('market') and len(expected)<=10
            assert [action.get('farmer')]+list(action.get('hands') or [])==close['units']
            bought[name]+=len(paid);sold[name]+=len(received)
            legs.append(dict(step=step,bought=len(paid),sold=len(received),inherited=close['inherited_sale'],
                             cash=sum(e['value'] for e in paid+received),naive_profit=buy['naive_profit'],
                             reordered=q['emitted']!=q['town_computed'], native_wheat_slot=bool(wheat_indices),
                             town_computed=q['town_computed'],emitted=q['emitted']))
        activation[name]+=row['changed_own_turns']>0;operations[name]+=len(legs)
        summaries.append(dict(arm=name,seed=seed,seat=seat,changed_own_turns=row['changed_own_turns'],
                              same_shops=row['same_shops'],same_work=row['accepted']==base['accepted'],
                              same_harvest=row['harvested']==base['harvested'],same_losses=row['nights']==base['nights'],same_escapes=row['escapes']==base['escapes'],
                              same_terminal_private=row['terminal_private']==base['terminal_private'],
                              escapes=row['escapes'],base_margin=base['margin'],candidate_margin=row['margin'],roundtrips=legs))
    candidates={n:r for n,r in manifest.items() if r['config']['enabled']}
    assert noops==8628 and all(activation[n]>0 and operations[n]>0 for n in candidates)
    result=dict(passed=True,competitive_ready=True,games=48,noop_exact_turns=noops,
                max_turn_ms=max(r['max_turn_ms'] for r in rows),activated_cells=dict(activation),operations=dict(operations),
                bought=dict(bought),sold=dict(sold),candidate_hashes={n:r['sha256'] for n,r in candidates.items()},
                base_hash=plan['agents']['base']['sha256'],control_hash=plan['agents']['top3']['sha256'],
                parent_hashes={n:plan['agents'][n]['sha256'] for n in ('town50_vq','town50_top3')},summary=summaries,
                note='Exact town50 noops, emitted queues, cash and wheat fills. Original town-computed and final-emitted queues kept separate. Changes to production and cash are diagnostic, not selection.')
    (OUT/'close_queue_validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='summary'}))


if __name__=='__main__':main()
