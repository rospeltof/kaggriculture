"""Exact one-step opening economics on all latest0914/1003 replay openings."""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from kaggle_environments import make
from investigar_lider import compact_state

OUT=Path('docs/evidencia/loop_publicos_20260925')


def main():
    dest=OUT/'opening_market_audit.json';plan_path=OUT/'opening_market_audit.plan.json'
    assert not dest.exists() and not plan_path.exists()
    receipts=[]
    for suffix in ('0914','1003'):
        receipts+=json.loads((OUT/f'feedback_{suffix}.fetch.json').read_text())
    plan=dict(created_at=datetime.now(timezone.utc).isoformat(),episodes=[x['id'] for x in receipts],
              quantities=[5,8,12,20,43],seats=[0,1],expected_one_step_scenarios=130,
              rule='Every source-control opening from the two latest completed recency audits. Replace only our step0 BUY_WHEAT8/SELL_WHEAT3 with q/q-5, retain all other orders and field commands. Same terminal wheat5, no outcome selection. Both seats, frozen rival step0 commands; one-step receipts, not complete-game WLT or proof of reactive behavior.',
              script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    plan_path.write_text(json.dumps(plan,indent=2)+'\n');rows=[];exact=0
    for receipt in receipts:
        raw=Path(receipt['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==receipt['sha256'];replay=json.loads(raw)
        original_seat=replay['info']['TeamNames'].index('Rospel');seed=replay['info']['seed']
        own=deepcopy(replay['steps'][1][original_seat]['action']);rival=deepcopy(replay['steps'][1][1-original_seat]['action'])
        wheat=[o for o in own['market'] if len(o)>=3 and o[0] in ('BUY_PRODUCT','SELL') and o[1]=='WHEAT']
        assert wheat==[['BUY_PRODUCT','WHEAT',8],['SELL','WHEAT',3]],(receipt['id'],wheat)
        for seat in plan['seats']:
            for q in plan['quantities']:
                action=deepcopy(own)
                for order in action['market']:
                    if len(order)>=3 and order[1]=='WHEAT':
                        if order[0]=='BUY_PRODUCT':order[2]=q
                        elif order[0]=='SELL':order[2]=q-5
                env=make('kaggriculture',configuration={'seed':seed,'episodeSteps':720},debug=False);env.reset()
                actions=[None,None];actions[seat]=action;actions[1-seat]=rival;env.step(actions)
                assert len(env.steps)==2 and all(s.status=='ACTIVE' for s in env.steps[-1])
                if q==8 and seat==original_seat:
                    assert compact_state(env.steps[1])==compact_state(replay['steps'][1]),receipt['id'];exact+=1
                ob=env.steps[-1][seat].observation;other=env.steps[-1][1-seat].observation
                assert ob['private']['shed']['WHEAT']==5
                rows.append(dict(episode=receipt['id'],policy=receipt['policy'],seed=seed,seat=seat,quantity=q,
                                 opponent=replay['info']['TeamNames'][1-original_seat],rival_market=rival.get('market'),
                                 money=ob['farms'][seat]['money'],rival_money=ob['farms'][1-seat]['money'],
                                 own_shed=dict(ob['private']['shed']),rival_shed=dict(other['private']['shed']),
                                 own_seeds=dict(ob['private']['seeds']),rival_seeds=dict(other['private']['seeds']),
                                 margin=ob['farms'][seat]['money']-ob['farms'][1-seat]['money']))
    keyed={(r['episode'],r['seat'],r['quantity']):r for r in rows}
    for row in rows:
        b=keyed[row['episode'],row['seat'],8]
        row['own_cash_delta']=row['money']-b['money'];row['rival_cash_delta']=row['rival_money']-b['rival_money'];row['margin_delta']=row['margin']-b['margin']
        assert row['own_shed']==b['own_shed'] and row['rival_shed']==b['rival_shed']
        assert row['own_seeds']==b['own_seeds'] and row['rival_seeds']==b['rival_seeds']
    assert len(rows)==130 and exact==13
    summary={}
    for q in plan['quantities']:
        cells=[x for x in rows if x['quantity']==q]
        summary[q]=dict(mean_margin_delta=sum(x['margin_delta'] for x in cells)/len(cells),worst_margin_delta=min(x['margin_delta'] for x in cells),
                        mean_own_cash_delta=sum(x['own_cash_delta'] for x in cells)/len(cells),worst_own_cash_delta=min(x['own_cash_delta'] for x in cells),
                        better_cells=sum(x['margin_delta']>0 for x in cells),worse_cells=sum(x['margin_delta']<0 for x in cells),min_own_money=min(x['money'] for x in cells))
    dest.write_text(json.dumps(dict(plan=plan,exact_recorded_controls=exact,summary=summary,results=rows),indent=2)+'\n')
    print(json.dumps(dict(exact_recorded_controls=exact,scenarios=len(rows),summary=summary)),flush=True)


if __name__=='__main__':main()
