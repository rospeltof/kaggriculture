"""Check accepted initial composition, care and output in four fixed worlds."""
from collections import Counter
from copy import deepcopy
import gzip
import hashlib
import importlib
import json
from pathlib import Path
import sys
import tarfile
import time

from construir_rebano_inicial import BASE, OUT as AGENTS, EVIDENCE as OUT
from sonda_fallo_forecast import run

TAG = 'initial_herd_smoke'


def main():
    manifest = json.loads((AGENTS/'manifest.json').read_text())
    arms = {'base': str(BASE), **{n:r['path'] for n,r in manifest.items()}}
    opponent = 'submission/main_publico_arshs3_arsgorynich.py'
    plan = dict(seeds=[1036000,1004000,1272457736,1018001],seats=[0,1],opponent=opponent,
                purpose='Physical initial composition, noop and diagnostics; no selection by rewards.',
                agents={n:dict(path=p,sha256=hashlib.sha256(Path(p).read_bytes()).hexdigest()) for n,p in arms.items()},
                opponent_sha256=hashlib.sha256(Path(opponent).read_bytes()).hexdigest())
    dest = OUT/(TAG+'.plan.json')
    if dest.exists():
        raise FileExistsError(dest)
    dest.write_text(json.dumps(plan,indent=2)+'\n')
    with tarfile.open(OUT/(TAG+'.sources.tgz'),'x:gz') as tar:
        for name,path in arms.items():
            tar.add(path,arcname=name+'.py')
        tar.add(opponent,arcname='opponent.py')
    engine = importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    original = engine._apply_unit_action
    baseline,results = {},[]
    for seed in plan['seeds']:
        for name,path in arms.items():
            for seat in plan['seats']:
                ns = {}; exec(compile(Path(path).read_bytes(),path,'exec'),ns)
                entry = [v for v in ns.values() if callable(v)][-1]
                elapsed,events,checkpoints = [],[],{}
                counts,harvested = Counter(),Counter()
                def timed(obs,config=None):
                    start=time.perf_counter(); action=entry(obs,config)
                    elapsed.append((time.perf_counter()-start)*1000)
                    if int(obs['step']) in (12,24,72,192):
                        s=deepcopy(ns.get('_Y_STATES',{}).get(seat,{}))
                        checkpoints[str(obs['step'])]=dict(credit={str(k):v for k,v in s.get('credit',{}).items()},
                                                         pending=s.get('pending',[]),sites={str(k):v for k,v in s.get('sites',{}).items()})
                    return action
                def unit(farm,private,actor,action,*args,**kwargs):
                    frame=sys._getframe(1)
                    watch=frame.f_code is engine.interpreter.__code__ and frame.f_locals.get('i')==seat and action and action[0] in ('PLACE','FEED','CARE','HARVEST')
                    if watch:
                        pos=farm['farmer'] if actor==0 else farm['hands'][actor-1]
                        x,y=pos; tile=deepcopy(farm['tiles'][y][x]); inv=dict(private['inventories'][actor])
                    result=original(farm,private,actor,action,*args,**kwargs)
                    if watch:
                        after=private['inventories'][actor]; new=farm['tiles'][y][x]
                        delta={k:after.get(k,0)-inv.get(k,0) for k in set(inv)|set(after)}
                        subject=(tile.get('animal') or tile.get('crop') or tile.get('kind')) if isinstance(tile,dict) else str(tile)
                        accepted=False
                        if action[0]=='HARVEST':
                            gained={k:v for k,v in delta.items() if v>0};harvested.update(gained);accepted=bool(gained)
                        elif action[0] in ('FEED','CARE') and isinstance(tile,dict) and isinstance(new,dict):
                            key='fed_today' if action[0]=='FEED' else 'cared_today';accepted=not tile.get(key) and bool(new.get(key))
                        elif action[0]=='PLACE' and isinstance(tile,dict) and isinstance(new,dict):
                            accepted=not tile.get('animal') and bool(new.get('animal'));subject=new.get('animal')
                        if accepted:counts[action[0]+':'+str(subject)]+=1
                        events.append(dict(step=frame.f_locals['step'],actor=actor,xy=list(pos),action=deepcopy(action),
                                           subject=subject,accepted=accepted,inventory_delta={k:v for k,v in delta.items() if v}))
                    return result
                engine._apply_unit_action=unit
                try:
                    env,ledger=run(timed,opponent,seed,seat)
                finally:
                    engine._apply_unit_action=original
                actions=[[s.action for s in row] for row in env.steps[1:]]
                rewards=[s.reward for s in env.steps[-1]];key=seed,seat
                if name=='base':baseline[key]=actions,rewards
                if name=='initial_noop':assert (actions,rewards)==baseline[key]
                reports={k:deepcopy(ns.get(k,{})) for k in ('_IH_REPORT','_Y_REPORT','_R85_REPORT','_V92_P_REPORT','_VQ_REPORT')}
                assert not any(v for report in reports.values() for k,v in report.items() if 'error' in k and isinstance(v,(int,float)))
                initial=[dict(x=x,y=y,animal=t['animal'],placed_day=t['placed_day'])
                         for y,row in enumerate(env.steps[24][0].observation.farms[seat].tiles)
                         for x,t in enumerate(row) if isinstance(t,dict) and t.get('animal')]
                expected=Counter(COW=2,SHEEP=2)
                if name in manifest:
                    cfg=manifest[name]['config'];expected[cfg['source']]-=cfg['qty'];expected[cfg['target']]+=cfg['qty']
                assert Counter(t['animal'] for t in initial)==expected,(name,initial,expected)
                assert not any(checkpoints['24']['credit'].values()) and not checkpoints['24']['pending']
                escapes=[]
                for t in range(719):
                    a=env.steps[t][0].observation.farms[seat].tiles;b=env.steps[t+1][0].observation.farms[seat].tiles
                    for y,row in enumerate(a):
                        for x,tile in enumerate(row):
                            if isinstance(tile,dict) and tile.get('animal'):
                                new=b[y][x].get('animal') if isinstance(b[y][x],dict) else None
                                if new!=tile['animal']:escapes.append(dict(step=t,xy=[x,y],animal=tile['animal']))
                flows={}
                for e in ledger:
                    if e['player']==seat:
                        key=e['op']+':'+str(e['item']);q,cash=flows.get(key,[0,0]);flows[key]=[q+1,cash+e['value']]
                row=dict(seed=seed,arm=name,seat=seat,rewards=rewards,reports=reports,initial_animals=initial,
                         checkpoints=checkpoints,accepted=dict(counts),harvested=dict(harvested),flows=flows,escapes=escapes,
                         terminal_private=env.steps[-1][seat].observation.private,
                         shops=env.steps[-1][0].observation.town.unlocked_shops,max_turn_ms=max(elapsed),
                         action_hash=hashlib.sha256(json.dumps(actions,sort_keys=True).encode()).hexdigest(),
                         changed_action_turns=sum(a[seat]!=b[seat] for a,b in zip(actions,baseline[seed,seat][0])))
                results.append(row)
                for kind,data in (('ledger',ledger),('units',events)):
                    (OUT/f'{TAG}.{seed}.{name}.{seat}.{kind}.jsonl.gz').write_bytes(gzip.compress(('\n'.join(json.dumps(e) for e in data)+'\n').encode(),mtime=0))
                print(json.dumps({k:row[k] for k in ('seed','arm','seat','rewards','initial_animals','escapes','changed_action_turns','harvested','max_turn_ms')}),flush=True)
    (OUT/(TAG+'.json')).write_text(json.dumps(results,indent=2)+'\n')


if __name__=='__main__':
    main()
