"""Primer cambio causal en una celda del piloto; dos episodios, sin selección nueva."""
from collections import defaultdict
import gzip
import hashlib
import importlib
import json
from pathlib import Path

OUT=Path('docs/evidencia/research_20260925')


def run(path,opponent,seed,seat):
    from kaggle_environments import make
    engine=importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    names=('_process_market','_commit_unit','_do_hire','_do_buy_land')
    original={n:getattr(engine,n) for n in names};ctx={};ledger=[]
    def record(op,item,value,farm):
        p=next(i for i,f in enumerate(ctx['farms']) if f is farm)
        ledger.append(dict(step=ctx['step'],player=p,op=op,item=item,value=value))
    def market(state,env):
        obs=state[0].observation;ctx.update(step=obs.day*24+obs.hour,farms=obs.farms)
        return original['_process_market'](state,env)
    def commit(op,item,price,farm,private,market,shed_capacity=100):
        ok=original['_commit_unit'](op,item,price,farm,private,market,shed_capacity)
        if ok:record(op,item,price if op=='SELL' else -price,farm)
        return ok
    def atomic(name,op):
        def call(farm,*args,**kwargs):
            before=farm['money'];r=original[name](farm,*args,**kwargs)
            if farm['money']!=before:record(op,None,farm['money']-before,farm)
            return r
        return call
    engine._process_market=market;engine._commit_unit=commit
    engine._do_hire=atomic('_do_hire','HIRE');engine._do_buy_land=atomic('_do_buy_land','BUY_LAND')
    try:
        env=make('kaggriculture',configuration={'seed':seed,'episodeSteps':720},debug=False)
        agents=[None,None];agents[seat]=path;agents[1-seat]=opponent;env.run(agents)
        assert len(env.steps)==720 and [s.status for s in env.steps[-1]]==['DONE','DONE']
        assert not any(s.status in ('ERROR','TIMEOUT','INVALID') for row in env.steps for s in row)
        for p in (0,1):assert 3000+sum(r['value'] for r in ledger if r['player']==p)==env.steps[-1][p].reward
        return env,ledger
    finally:
        for n,fn in original.items():setattr(engine,n,fn)


if __name__=='__main__':
    meta=json.loads((OUT/'forecast_pilot.meta.json').read_text())
    rows=[json.loads(l) for l in (OUT/'forecast_pilot.jsonl').read_text().splitlines()]
    keyed={(r['a'],r['b'],r['seed'],r['seat']):r for r in rows}
    choices=sorted((r['b'],r['seed'],r['seat']) for r in rows if r['a']=='base' and r['b'] not in ('noop','gate','off') and r['score']==1 and keyed['gate',r['b'],r['seed'],r['seat']]['score']==0)
    opp,seed,seat=choices[0];envs=[];ledgers=[]
    for a in ('base','gate'):
        env,ledger=run(meta['agentes'][a]['ruta'],meta['agentes'][opp]['ruta'],seed,seat)
        assert [s.reward for s in env.steps[-1]]==keyed[a,opp,seed,seat]['rewards']
        envs.append(env);ledgers.append(ledger)
        (OUT/f'forecast_failure_{a}.ledger.jsonl.gz').write_bytes(gzip.compress(('\n'.join(json.dumps(r) for r in ledger)+'\n').encode(),mtime=0))
    b,c=envs
    diffs=[t for t in range(719) if b.steps[t+1][seat].action!=c.steps[t+1][seat].action]
    first=diffs[0]
    summary=dict(rule='Primera celda ordenada por rival/semilla/asiento donde base gana y gate pierde; sólo diagnóstico',
        opponent=opp,seed=seed,seat=seat,first_action_difference=first,
        before_market=b.steps[first][0].observation.market,
        first_actions=[e.steps[first+1][seat].action for e in envs],
        final_rewards=[[s.reward for s in e.steps[-1]] for e in envs],changed_action_turns=len(diffs),
        daily=[dict(day=d,money=[[s['money'] for s in e.steps[d*24][0].observation.farms] for e in envs]) for d in (6,10,15,20,25,29)],
        sale_summary=[],first_commits=[[r for r in ledger if first<=r['step']<=first+3] for ledger in ledgers])
    for ledger in ledgers:
        sums=defaultdict(lambda:[0,0])
        for r in ledger:
            if r['player']==seat and r['op']=='SELL':sums[r['item']][0]+=1;sums[r['item']][1]+=r['value']
        summary['sale_summary'].append(dict(sums))
    (OUT/'forecast_failure.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:summary[k] for k in ('opponent','seed','seat','first_action_difference','first_actions','final_rewards','sale_summary')},indent=2))
