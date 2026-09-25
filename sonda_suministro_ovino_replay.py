"""General rule against the previously reproduced recorded opponent."""
from copy import deepcopy
import gzip
import hashlib
import json
from pathlib import Path

from investigar_lider import compact_state
from sonda_fallo_forecast import run

OUT = Path('docs/evidencia/loop_publicos_20260925')


def main():
    target = OUT/'davion_general_supply_probe.json'; assert not target.exists()
    source = Path('submission/main_publico_arshs3_vq_top3.py'); raw = source.read_bytes()
    path = Path('replays/top3_feedback_0653/episode-113174624-replay.json'); replay=json.loads(path.read_bytes())
    seat=replay['info']['TeamNames'].index('Rospel'); assert seat==0
    plan=dict(seed=replay['info']['seed'], seat=seat, source_sha256=hashlib.sha256(raw).hexdigest(),
              rule='General state-based rule versus recorded rival. Development mechanism only, not a competitive estimate.', candidate_sha256=hashlib.sha256(Path('results/suministro_ovino_20260925/sheep_supply_buy.py').read_bytes()).hexdigest(), games=2)
    (OUT/'davion_general_supply_probe.plan.json').write_text(json.dumps(plan,indent=2)+'\n')
    def rival(obs): return deepcopy(replay['steps'][int(obs['step'])+1][1-seat]['action'])
    results=[]
    for name in ('base','sheep_supply_buy'):
        used=source if name=='base' else Path('results/suministro_ovino_20260925/sheep_supply_buy.py')
        ns={};exec(compile(used.read_bytes(),str(used),'exec'),ns)
        agent=[v for v in ns.values() if callable(v)][-1];edits=[]
        env,ledger=run(agent,rival,plan['seed'],seat)
        if name=='base':
            assert all(compact_state(a)==compact_state(b) for a,b in zip(env.steps,replay['steps']))
            assert all(env.steps[t+1][seat].action==replay['steps'][t+1][seat]['action'] for t in range(719))
        else:
            edits=deepcopy(ns['_SS_EVENTS'])
            assert any(e['step']==601 and e['predicted_after']>=11 for e in edits)
            assert not ns['_SS_REPORT']['errors'] and not ns['_SS_REPORT']['prediction_errors']
        flows=[]
        for p in (seat,1-seat):
            wool=[e for e in ledger if e['player']==p and e['op']=='SELL' and e['item']=='WOOL']
            flows.append(dict(wool_sold=len(wool),wool_cash=sum(e['value'] for e in wool)))
        worker=[]
        for step in range(601,624):
            obs=env.steps[step][seat].observation;action=env.steps[step+1][seat].action
            worker.append(dict(step=step,shed_wheat=obs['private']['shed'].get('WHEAT',0),
                               wheat=obs['private']['inventories'][12].get('WHEAT',0) if len(obs['private']['inventories'])>12 else None,
                               action=action['hands'][11] if len(action['hands'])>=12 else None))
        cells=[(x,y) for y in (5,6) for x in (5,6,7)]
        tiles=[dict(xy=[x,y],tile=deepcopy(env.steps[624][0].observation['farms'][seat]['tiles'][y][x])) for x,y in cells]
        rewards=[s.reward for s in env.steps[-1]]
        row=dict(arm=name,rewards=rewards,margin=rewards[seat]-rewards[1-seat],wool=flows,edits=edits,worker=worker,tiles_after_night=tiles,
                 accepted_wheat601=sum(e['player']==seat and e['step']==601 and e['op']=='BUY_PRODUCT' and e['item']=='WHEAT' for e in ledger),
                 shops_preserved=all(a[0].observation['town']==b[0]['observation']['town'] for a,b in zip(env.steps,replay['steps'])))
        results.append(row)
        (OUT/f'davion_general_supply_probe.{name}.ledger.jsonl.gz').write_bytes(gzip.compress(('\n'.join(json.dumps(e) for e in ledger)+'\n').encode(),mtime=0))
        print(json.dumps({k:row[k] for k in ('arm','rewards','margin','wool','accepted_wheat601','shops_preserved')}),flush=True)
    target.write_text(json.dumps(dict(plan=plan,results=results),indent=2)+'\n')


if __name__=='__main__':main()
