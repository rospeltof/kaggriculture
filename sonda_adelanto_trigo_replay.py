"""Recorded-opponent mechanism probe for moving a native wheat buy earlier."""
from copy import deepcopy
import gzip
import hashlib
import json
from pathlib import Path

from auditar_forecast_pareado_real import inspect_env
from investigar_lider import compact_state
from sonda_fallo_forecast import run

OUT=Path('docs/evidencia/loop_publicos_20260925')


def main():
    target=OUT/'grim_advance_probe.json';assert not target.exists()
    path=Path('replays/vq_feedback_0742/episode-113198597-replay.json');replay=json.loads(path.read_bytes())
    seat=replay['info']['TeamNames'].index('Rospel');seed=replay['info']['seed']
    arms={'base':'submission/main_publico_arshs3_vq.py','advance_vq':'results/adelanto_trigo_20260925/advance_vq.py'}
    plan=dict(seed=seed,seat=seat,episode=113198597,
        agents={n:dict(path=p,sha256=hashlib.sha256(Path(p).read_bytes()).hexdigest()) for n,p in arms.items()},
        scope='General timing rule on VQ versus recorded rival; mechanism and accounting, not competitive selection.')
    (OUT/'grim_advance_probe.plan.json').write_text(json.dumps(plan,indent=2)+'\n')
    def rival(obs):return deepcopy(replay['steps'][int(obs['step'])+1][1-seat]['action'])
    rows=[]
    for name,source in arms.items():
        ns={};exec(compile(Path(source).read_bytes(),source,'exec'),ns);entry=[v for v in ns.values() if callable(v)][-1]
        env,ledger=run(entry,rival,seed,seat)
        if name=='base':
            assert all(compact_state(a)==compact_state(b) for a,b in zip(env.steps,replay['steps']))
            assert all(env.steps[t+1][seat].action==replay['steps'][t+1][seat]['action'] for t in range(719))
        stats=deepcopy(ns.get('_BW_REPORT',{}));assert not any(v for k,v in stats.items() if 'error' in k)
        events=deepcopy(ns.get('_BW_EVENTS',[]))
        for e in events:
            accepted=[r for r in ledger if r['step']==e['step'] and r['player']==seat and r['op']=='BUY_PRODUCT' and r['item']=='WHEAT']
            e['engine_bought']=len(accepted);e['engine_cost']=-sum(r['value'] for r in accepted)
            assert e['engine_bought']==e['bought'] and e['hook_calls']>0
        row=dict(arm=name,stats=stats,events=events,**inspect_env(env,ledger,seat));rows.append(row)
        (OUT/f'grim_advance_probe.{name}.ledger.jsonl.gz').write_bytes(gzip.compress(('\n'.join(json.dumps(e) for e in ledger)+'\n').encode(),mtime=0))
        print(json.dumps(dict(arm=name,margin=row['margin'],stats=stats,escapes=row['escapes'])),flush=True)
    target.write_text(json.dumps(dict(plan=plan,results=rows),indent=2)+'\n')


if __name__=='__main__':main()
