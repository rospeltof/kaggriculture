"""Reproduce a preregistered recency sample and expose zero-grain pickup stalls."""
import argparse
from copy import deepcopy
import gzip
import hashlib
import json
from pathlib import Path
import time

from auditar_forecast_pareado_real import inspect_env
from investigar_lider import compact_state
from sonda_fallo_forecast import run

OUT = Path('docs/evidencia/loop_publicos_20260925')
SOURCES = {'top3':'submission/main_publico_arshs3_vq_top3.py',
           'vq':'submission/main_publico_arshs3_vq.py'}


def main(suffix):
    plan = json.loads((OUT/f'feedback_{suffix}.plan.json').read_text())
    fetched = json.loads((OUT/f'feedback_{suffix}.fetch.json').read_text())
    target = OUT/f'feedback_{suffix}.audit.json'; assert not target.exists()
    assert {r['id'] for r in plan['selected']}=={r['id'] for r in fetched}
    results=[]
    for selection in plan['selected']:
        episode=selection['id']; policy=selection['policy']
        receipt=next(r for r in fetched if r['id']==episode and r['policy']==policy)
        path=Path(receipt['path']);raw=path.read_bytes();assert hashlib.sha256(raw).hexdigest()==receipt['sha256']
        replay=json.loads(raw);assert replay['info']['TeamNames'].count('Rospel')==1
        seat=replay['info']['TeamNames'].index('Rospel');seed=replay['info']['seed']
        source=Path(SOURCES[policy]);ns={};exec(compile(source.read_bytes(),str(source),'exec'),ns)
        entry=[v for v in ns.values() if callable(v)][-1];elapsed=[];empty_pickups=[]
        def opponent(obs): return deepcopy(replay['steps'][int(obs['step'])+1][1-seat]['action'])
        def agent(obs,config=None):
            start=time.perf_counter();action=entry(obs,config);elapsed.append((time.perf_counter()-start)*1000)
            state=ns.get('_V233_STATES',{}).get(seat,{})
            for actor,c in enumerate([action.get('farmer') or ['PASS'],*(action.get('hands') or [])]):
                if len(c)>=3 and c[:2]==['PICKUP','WHEAT'] and int(c[2])==0:
                    targets=state.get('workers',{}).get(actor)
                    inv=obs['private']['inventories'][actor] if actor<len(obs['private']['inventories']) else {}
                    empty_pickups.append(dict(step=int(obs['step']),actor=actor,targets=deepcopy(targets),
                        shed_wheat=obs['private']['shed'].get('WHEAT',0),bag_wheat=inv.get('WHEAT',0)))
            return action
        env,ledger=run(agent,opponent,seed,seat)
        assert len(env.steps)==len(replay['steps'])==720
        assert all(compact_state(a)==compact_state(b) for a,b in zip(env.steps,replay['steps']))
        assert all(env.steps[t+1][seat].action==replay['steps'][t+1][seat]['action'] for t in range(719))
        assert [s.reward for s in env.steps[-1]]==replay['rewards']
        reports={k:deepcopy(ns.get(k,{})) for k in ('_VQ_REPORT','_V92_P_REPORT','_V233_REPORT','_R85_REPORT')}
        assert not any(v for d in reports.values() for k,v in d.items() if 'error' in k and isinstance(v,(int,float)))
        result=dict(episode=episode,policy=policy,opponent=replay['info']['TeamNames'][1-seat],
                    seed=seed,seat=seat,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                    replay_sha256=receipt['sha256'],own_actions_exact=719,states_exact=720,
                    max_turn_ms=max(elapsed),empty_wheat_pickups=empty_pickups,reports=reports,
                    **inspect_env(env,ledger,seat))
        results.append(result)
        (OUT/f'feedback_{suffix}.{episode}.ledger.jsonl.gz').write_bytes(gzip.compress(('\n'.join(json.dumps(e) for e in ledger)+'\n').encode(),mtime=0))
        print(json.dumps({k:result[k] for k in ('episode','policy','opponent','seed','seat','margin','max_turn_ms','empty_wheat_pickups','escapes')}),flush=True)
    target.write_text(json.dumps(dict(plan=plan,results=results,note='Source controls only. Recency sample is not population WR. Zero requests require state/mechanism interpretation.'),indent=2)+'\n')


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('suffix');main(ap.parse_args().suffix)
