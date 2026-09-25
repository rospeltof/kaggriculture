"""Desarrollo con seed fijo; versiones forzadas verifican mecánica, no rendimiento."""
import gzip
import hashlib
import json
from pathlib import Path

from construir_tomate_relleno import BASE, OUT as AGENTS
from sonda_fallo_forecast import run

OUT=Path('docs/evidencia/loop_publicos_20260925')
TAG='infill_smoke_v4'


def main():
    variants=json.loads((AGENTS/'manifest.json').read_text())
    arms={'base':BASE,**{n:Path(r['path']) for n,r in variants.items()}}
    for name,parent,extra in (
        ('infill_noop','infill4_d16','_IF_SIZE=0'),
        ('forced4','infill4_d16','_IF_MARGIN=-1e12'),
        ('forced8','infill8_d18','_IF_MARGIN=-1e12'),
    ):
        p=AGENTS/(name+'.py')
        if p.exists():raise FileExistsError(p)
        p.write_bytes(arms[parent].read_bytes()+('\n# Development only, never submit.\n'+extra+'\n').encode());arms[name]=p
    plan=dict(seed=1004000,seats=[0,1],opponent='submission/main_publico_arshs3_arsgorynich.py',
              purpose='Known SE sheep world from earlier development. Execution/parent ownership only; no performance inference. Forced4/8 bypass economic gate only.',
              agents={n:dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for n,p in arms.items()})
    pp=OUT/(TAG+'.plan.json')
    if pp.exists():raise FileExistsError(pp)
    pp.write_text(json.dumps(plan,indent=2)+'\n');all_results=[];baseline={}
    for name,path in arms.items():
        for seat in plan['seats']:
            ns={};exec(compile(path.read_bytes(),str(path),'exec'),ns)
            entry=[v for v in ns.values() if callable(v)][-1]
            env,ledger=run(entry,plan['opponent'],plan['seed'],seat)
            actions=[e[seat].action for e in env.steps[1:]]
            if name=='base':baseline[seat]=actions
            changed=sum(a!=b for a,b in zip(baseline[seat],actions))
            if name=='infill_noop':assert changed==0
            crops=[]
            for day in range(14,30):
                farm=env.steps[day*24][0].observation.farms[seat]
                tiles=[t for y,row in enumerate(farm.tiles) for x,t in enumerate(row) if y>=7 and x>=5 and isinstance(t,dict)]
                crops.append(dict(day=day,tomatoes=sum(t.get('crop')=='TOMATO' for t in tiles),money=farm.money,
                                  sheep=sum(isinstance(t,dict) and t.get('animal')=='SHEEP' for row in farm.tiles for t in row)))
            stats=ns.get('_IF_REPORT',{})
            assert stats.get('hire_shortfalls',0)==0,stats
            parent_errors={k:v for key in ('_V219_REPORT','_R46_REPORT','_CA_REPORT','_R51_INPUT_REPORT') for k,v in ns.get(key,{}).items() if 'error' in k and isinstance(v,(int,float)) and v}
            assert not parent_errors,parent_errors
            r=dict(arm=name,seat=seat,rewards=[s.reward for s in env.steps[-1]],changed_action_turns=changed,
                   report=stats,project_report=ns.get('_V233_REPORT',{}),input_report=ns.get('_R51_INPUT_REPORT',{}),crops=crops,
                   first_changed_step=next((t for t,(a,b) in enumerate(zip(baseline[seat],actions)) if a!=b),None),
                   tomato_sold=sum(r['player']==seat and r['op']=='SELL' and r['item']=='TOMATO' for r in ledger),
                   tomato_revenue=sum(r['value'] for r in ledger if r['player']==seat and r['op']=='SELL' and r['item']=='TOMATO'))
            all_results.append(r)
            p=OUT/f'{TAG}.{name}.{seat}.ledger.jsonl.gz'
            p.write_bytes(gzip.compress(('\n'.join(json.dumps(x) for x in ledger)+'\n').encode(),mtime=0))
            print(json.dumps(r),flush=True)
    (OUT/(TAG+'.json')).write_text(json.dumps(all_results,indent=2)+'\n')


if __name__=='__main__':main()
