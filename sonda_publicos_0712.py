"""Official-vs-nominal entry equality for Harvest V68 and its selector-off ablation."""
from collections import Counter
from copy import deepcopy
import gzip
import hashlib
import json
from pathlib import Path
import tarfile
import time

from kaggle_environments.agent import get_last_callable
from sonda_fallo_forecast import run

OUT=Path('docs/evidencia/loop_publicos_20260925')
TAG='public_0712_smoke'
BASE='submission/main_publico_arshs3_vq_top3.py'
PUBLIC={n:r['path'] for n,r in json.loads((OUT/'public_0712_variants.json').read_text()).items()}


def main():
    manifest={n:dict(path=p,sha256=hashlib.sha256(Path(p).read_bytes()).hexdigest()) for n,p in PUBLIC.items()}
    target=OUT/'public_0712_variants.json'
    if target.exists():
        assert json.loads(target.read_text())==manifest
    else:
        target.write_text(json.dumps(manifest,indent=2)+'\n')
    arms={'base':BASE,'noop':BASE,'vq':'submission/main_publico_arshs3_vq.py',**PUBLIC}
    plan=dict(seeds=[1054000,1054001,1578791335],seats=[0,1],opponent=BASE,
              purpose='Official/nominal loader equivalence and diagnostics only, no selection by rewards.',
              agents={n:dict(path=p,sha256=hashlib.sha256(Path(p).read_bytes()).hexdigest()) for n,p in arms.items()})
    (OUT/(TAG+'.plan.json')).write_text(json.dumps(plan,indent=2)+'\n')
    with tarfile.open(OUT/(TAG+'.sources.tgz'),'x:gz') as tar:
        for name,path in arms.items():tar.add(path,arcname=name+'.py')
    baseline,official,rows={},{},[]
    for seed in plan['seeds']:
        for name,path in arms.items():
            raw=Path(path).read_text()
            for mode in (['official','nominal'] if name in PUBLIC else ['official']):
                for seat in plan['seats']:
                    # Both loaders compile a fresh namespace. The nominal entry
                    # records upstream report dictionaries; official is unmodified.
                    ns={};exec(compile(raw,path,'exec'),ns)
                    last=[v for v in ns.values() if callable(v)][-1]
                    if name in PUBLIC:
                        assert ns['agent'] is ns['kaggle_submission_agent']
                        assert last is ns['agent'] and last.__name__ == '_final_sell_block_reorder_entrypoint'
                    entry=get_last_callable(raw) if mode=='official' else ns['agent']
                    elapsed=[]
                    def timed(obs,config=None):
                        start=time.perf_counter();a=entry(obs,config);elapsed.append((time.perf_counter()-start)*1000)
                        return a
                    env,ledger=run(timed,BASE,seed,seat)
                    actions=[[s.action for s in turn] for turn in env.steps[1:]]
                    rewards=[s.reward for s in env.steps[-1]]
                    if name=='base':baseline[seed,seat]=actions,rewards
                    if name=='noop':assert (actions,rewards)==baseline[seed,seat]
                    if mode=='official':official[name,seed,seat]=actions,rewards
                    else:assert (actions,rewards)==official[name,seed,seat]
                    telemetry={}
                    if mode=='nominal':
                        for key,value in ns.items():
                            if (isinstance(value,dict) and ('REPORT' in key or 'STATS' in key)):
                                telemetry[key]=deepcopy(value)
                        assert not any(v for r in telemetry.values() for k,v in r.items() if 'error' in k and isinstance(v,(int,float)))
                    escapes=[]
                    for t in range(719):
                        a=env.steps[t][0].observation.farms[seat].tiles;b=env.steps[t+1][0].observation.farms[seat].tiles
                        for y,row in enumerate(a):
                            for x,tile in enumerate(row):
                                if isinstance(tile,dict) and tile.get('animal'):
                                    new=b[y][x].get('animal') if isinstance(b[y][x],dict) else None
                                    if new!=tile['animal']:escapes.append(dict(step=t,xy=[x,y],animal=tile['animal']))
                    additions=[]
                    for t in range(719):
                        a=env.steps[t][0].observation['farms'][seat]['tiles'];b=env.steps[t+1][0].observation['farms'][seat]['tiles']
                        for y,line in enumerate(b):
                            for x,tile in enumerate(line):
                                old=a[y][x].get('animal') if isinstance(a[y][x],dict) else None
                                new=tile.get('animal') if isinstance(tile,dict) else None
                                if new and new!=old:additions.append(dict(step=t,xy=[x,y],animal=new))
                    flows={}
                    for e in ledger:
                        if e['player']==seat:
                            key=e['op']+':'+str(e['item']);q,cash=flows.get(key,[0,0]);flows[key]=[q+1,cash+e['value']]
                    live=entry.__globals__.get('_Y_STATES',{}).get(seat,{})
                    credit=dict(pending=deepcopy(live.get('pending',[])),
                                credit={repr(k):v for k,v in live.get('credit',{}).items()},
                                coop_swap=live.get('coop_swap'),sites=[dict(xy=list(k),animal=v) for k,v in live.get('sites',{}).items()])
                    row=dict(seed=seed,arm=name,mode=mode,seat=seat,rewards=rewards,
                             entry_name=entry.__name__,telemetry=telemetry,flows=flows,escapes=escapes,additions=additions,credit=credit,
                             terminal_private=env.steps[-1][seat].observation.private,
                             shops=env.steps[-1][0].observation.town.unlocked_shops,max_turn_ms=max(elapsed),
                             action_hash=hashlib.sha256(json.dumps(actions,sort_keys=True).encode()).hexdigest(),
                             changed_action_turns=sum(a[seat]!=b[seat] for a,b in zip(actions,baseline[seed,seat][0])))
                    rows.append(row)
                    (OUT/f'{TAG}.{seed}.{name}.{mode}.{seat}.ledger.jsonl.gz').write_bytes(gzip.compress(('\n'.join(json.dumps(e) for e in ledger)+'\n').encode(),mtime=0))
                    print(json.dumps({k:row[k] for k in ('seed','arm','mode','seat','rewards','entry_name','max_turn_ms','changed_action_turns','escapes')}),flush=True)
    (OUT/(TAG+'.json')).write_text(json.dumps(rows,indent=2)+'\n')


if __name__=='__main__':main()
