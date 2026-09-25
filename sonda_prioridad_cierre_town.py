"""Capture an exact failed confirmation trajectory, then isolate closing order in its market phase."""
from copy import deepcopy
from datetime import datetime, timezone
import gzip
import hashlib
import importlib
import json
from pathlib import Path
import sys

from sonda_fallo_forecast import run

OUT=Path('docs/evidencia/loop_publicos_20260925')


def main():
    target=OUT/'town_close_priority_probe_v2.json';plan_path=OUT/'town_close_priority_probe_v2.plan.json'
    assert not target.exists() and not plan_path.exists()
    meta=json.loads((OUT/'confirm20.meta.json').read_text());assert meta['state']=='complete'
    case=dict(arm='town50',opponent='v13',seed=1050019,seat=0,step=661)
    source=meta['agentes']['town50'];rival=meta['agentes']['v13']
    plan=dict(created_at=datetime.now(timezone.utc).isoformat(),case=case,source=source,rival=rival,
              rule='One complete exact-source control, capture official state after units before market661. Two isolated market phases on identical state: original wheat-first close and original parent milk queue followed by wheat. No changed agent or WLT claim; private states are phase-test fixtures only.',
              script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    plan_path.write_text(json.dumps(plan,indent=2)+'\n')
    code=Path(source['ruta']).read_bytes();assert hashlib.sha256(code).hexdigest()==source['sha256']
    assert hashlib.sha256(Path(rival['ruta']).read_bytes()).hexdigest()==rival['sha256']
    ns={};exec(compile(code,source['ruta'],'exec'),ns);entry=[v for v in ns.values() if callable(v)][-1];digest=hashlib.sha256()
    def own(obs,conf=None):
        action=entry(obs,conf);digest.update(json.dumps(action,sort_keys=True,separators=(',',':'),allow_nan=False).encode()+b'\n');return action
    engine=importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    process=engine._process_market;captured=[]
    def capture(state,env):
        frame=sys._getframe(1)
        if frame.f_back is not None and frame.f_back.f_code is engine.interpreter.__code__ and state[0].observation.day*24+state[0].observation.hour==case['step']:
            captured.append(deepcopy(state))
        return process(state,env)
    engine._process_market=capture
    try:env,ledger=run(own,rival['ruta'],case['seed'],case['seat'])
    finally:engine._process_market=process
    assert len(captured)==1
    row=next(json.loads(l) for l in (OUT/'confirm20.jsonl').read_text().splitlines() if (lambda r:r['a']=='town50' and r['b']=='v13' and r['seed']==1050019 and r['seat']==0)(json.loads(l)))
    assert digest.hexdigest()==row['action_hashes'][0] and [s.reward for s in env.steps[-1]]==row['rewards']
    expected=[json.loads(l) for l in gzip.decompress((OUT/'confirm20.physical.v13_1050019.town50.ledger.jsonl.gz').read_bytes()).splitlines()]
    assert ledger==expected
    fixture=captured[0];event=next(e for e in ns['_TR_EVENTS'] if e['kind']=='close' and e['step']==661)
    original=list(fixture[0].action['market']);assert original==[['SELL','WHEAT',50],['SELL','MILK',13]]
    reordered=deepcopy(event['original'])+[['SELL','WHEAT',event['quantity']]]
    assert reordered==[['SELL','MILK',13],['SELL','WHEAT',50]]
    commit=engine._commit_unit;results={};after={}
    for name,market in [('wheat_first',original),('parent_first',reordered)]:
        state=deepcopy(fixture);state[0].action['market']=deepcopy(market);flows=[]
        farms=state[0].observation.farms;before=[f['money'] for f in farms]
        def traced(op,item,price,farm,private,book,*args,**kwargs):
            player=0 if farm is farms[0] else 1;money=farm['money'];ok=commit(op,item,price,farm,private,book,*args,**kwargs)
            if ok:flows.append(dict(player=player,op=op,item=item,value=farm['money']-money))
            return ok
        engine._commit_unit=traced
        try:process(state,env)
        finally:engine._commit_unit=commit
        cash=[f['money']-b for f,b in zip(farms,before)]
        assert cash==[sum(e['value'] for e in flows if e['player']==p) for p in (0,1)]
        after[name]=state
        results[name]=dict(own_market=market,cash=cash,margin_cash=cash[0]-cash[1],ledger=flows)
    control=[dict(player=e['player'],op=e['op'],item=e['item'],value=e['value']) for e in ledger if e['step']==661]
    assert results['wheat_first']['ledger']==control
    assert after['wheat_first'][0].observation.market==after['parent_first'][0].observation.market
    for p in (0,1):assert after['wheat_first'][p].observation.private==after['parent_first'][p].observation.private
    output=dict(plan=plan,full_game_actions_exact=719,full_game_rewards=row['rewards'],results=results,
                margin_change=results['parent_first']['margin_cash']-results['wheat_first']['margin_cash'],
                note='Identical pre-market state and final inventories. Only this phase is causally isolated; a full candidate can alter later behavior and requires its own development/pilot.')
    target.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k not in ('plan','results')}),flush=True)
    print(json.dumps({n:{k:v for k,v in r.items() if k!='ledger'} for n,r in results.items()}),flush=True)


if __name__=='__main__':main()
