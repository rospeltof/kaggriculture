"""Isolate prebuy versus earlier liquidation with the official market engine."""
from copy import deepcopy
import hashlib
import importlib
import json
from pathlib import Path

from kaggle_environments import make

OUT=Path('docs/evidencia/loop_publicos_20260925')


def main():
    dest=OUT/'wheat_timing_factorial.json';assert not dest.exists()
    source=Path('submission/main_publico_arshs3_vq.py');ns={};exec(compile(source.read_bytes(),str(source),'exec'),ns)
    engine=importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    env=make('kaggriculture',configuration={'seed':1060000,'episodeSteps':720},debug=False)
    template=deepcopy(env.reset())
    own_times={'native':(296,297),'buy_early':(295,297),'both_early':(295,296)}
    opponent_times={'passive':None,'buy_early':(295,297),'native':(296,297),'both_early':(295,296)}
    plan=dict(inventories=[10100,10000,9700,9300],town_drains=[0,1,3,6],quantities=[48,90],
              own_times=own_times,opponent_times=opponent_times,money_each=30000,steps=[295,296,297],
              scope='384 synthetic three-market scenarios, no field actions, no funding constraint, no candidate selection. Isolate buy time and induced sale time against four fixed rival schedules.',
              source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
              engine_sha256=hashlib.sha256(Path(engine.__file__).read_bytes()).hexdigest())
    (OUT/'wheat_timing_factorial.plan.json').write_text(json.dumps(plan,indent=2)+'\n')
    rows=[]
    for inventory in plan['inventories']:
        for drain in plan['town_drains']:
            for q in plan['quantities']:
                for rival,other_times in opponent_times.items():
                    for name,times in own_times.items():
                        state=deepcopy(template);obs=state[0].observation
                        for farm in obs.farms:farm.money=30000
                        obs.market.inventory.WHEAT=inventory;engine._refresh_prices(obs.market)
                        obs.town.unlocked_shops=['BAKERY']*drain
                        for p in (0,1):state[p].observation.private.shed.WHEAT=0
                        params=ns['_v44y_params'](obs);receipts=[]
                        for step in plan['steps']:
                            orders=[]
                            for schedule in (times,other_times):
                                order=[]
                                if schedule is not None:
                                    if step==schedule[0]:order=[['BUY_PRODUCT','WHEAT',q]]
                                    elif step==schedule[1]:order=[['SELL','WHEAT',q]]
                                orders.append(order)
                            model=ns['_v44y_lockstep'](orders[0],orders[1],{'WHEAT':obs.market.inventory['WHEAT']},
                                {'WHEAT':state[0].observation.private.shed['WHEAT']},
                                {'WHEAT':state[1].observation.private.shed['WHEAT']},{'WHEAT':params['WHEAT']})
                            before=[f['money'] for f in obs.farms]
                            for p in (0,1):state[p].action=dict(farmer=['PASS'],hands=[],market=orders[p])
                            engine._process_market(state,env)
                            actual=[f['money']-cash for f,cash in zip(obs.farms,before)]
                            assert actual==list(model),(inventory,drain,q,rival,name,step,actual,model)
                            receipts.append(dict(step=step,orders=orders,cash=actual))
                            if step<297:engine._town_consume(env,state,step)
                        assert all(state[p].observation.private.shed['WHEAT']==0 for p in (0,1))
                        money=[f['money']-30000 for f in obs.farms]
                        rows.append(dict(inventory=inventory,drain=drain,quantity=q,rival=rival,policy=name,
                                         own_net=money[0],rival_net=money[1],margin=money[0]-money[1],receipts=receipts))
    keyed={(r['inventory'],r['drain'],r['quantity'],r['rival'],r['policy']):r for r in rows}
    for row in rows:
        base=keyed[row['inventory'],row['drain'],row['quantity'],row['rival'],'native']
        row['margin_delta_vs_native']=row['margin']-base['margin']
    dest.write_text(json.dumps(rows,indent=2)+'\n')
    summary={}
    for name in ('buy_early','both_early'):
        part=[r for r in rows if r['policy']==name]
        summary[name]=dict(better=sum(r['margin_delta_vs_native']>0 for r in part),
                          worse=sum(r['margin_delta_vs_native']<0 for r in part),
                          equal=sum(r['margin_delta_vs_native']==0 for r in part),
                          own_losses=sum(r['own_net']<0 for r in part))
    print(json.dumps(dict(cases=len(rows),exact_market_legs=3*len(rows),summary=summary),indent=2))


if __name__=='__main__':main()
