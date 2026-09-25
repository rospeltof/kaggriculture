"""Diagnóstico registrado del calendario; no selecciona ganadores por W/L/T."""
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path

from construir_tomate_temprano import BASE, OUT as AGENTS, transformed
from sonda_fallo_forecast import run

OUT=Path('docs/evidencia/loop_publicos_20260925')


def main():
    noop=AGENTS/'calendar_noop.py'
    raw=(transformed(BASE.read_text())+'\n_ET_START=18\n_ET_LIQUIDITY=12000\n').encode()
    if noop.exists():raise FileExistsError(noop)
    noop.write_bytes(raw)
    arms={'base':BASE,'calendar_noop':noop,
          'early12_6k':AGENTS/'early12_6k.py','late18_6k':AGENTS/'late18_6k.py'}
    plan=dict(seed=1004000,seats=[0,1],opponent='submission/main_publico_arshs3_arsgorynich.py',
              rule='Fixed first development seed; execution and calendar validation, not population performance or pilot selection.',
              agents={n:dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for n,p in arms.items()})
    plan_path=OUT/'early_tomato_smoke.plan.json'
    if plan_path.exists():raise FileExistsError(plan_path)
    plan_path.write_text(json.dumps(plan,indent=2)+'\n')
    result=[];base_actions={}
    for name,path in arms.items():
        for seat in plan['seats']:
            ns={};exec(compile(path.read_bytes(),str(path),'exec'),ns)
            entry=[v for v in ns.values() if callable(v)][-1]
            env,ledger=run(entry,plan['opponent'],plan['seed'],seat)
            actions=[e[seat].action for e in env.steps[1:]]
            if name=='base':base_actions[seat]=actions
            changed=sum(a!=b for a,b in zip(base_actions[seat],actions))
            if name=='calendar_noop':assert changed==0
            report={k:ns[k] for k in ('_V219_REPORT','_CXTB_REPORT','_R53_LABOR_REPORT','_V13V_REPORT')}
            assert report['_V219_REPORT']['errors']==0,report
            assert report['_CXTB_REPORT']['cxtb_errors']==0,report
            daily=[]
            for day in range(10,30):
                f=env.steps[day*24][0].observation.farms[seat]
                tiles=[t for row in f.tiles for t in row if isinstance(t,dict) and t.get('crop')=='TOMATO']
                daily.append(dict(day=day,tomatoes=len(tiles),births=dict(Counter(t['planted_day'] for t in tiles)),money=f.money))
            sales=[r for r in ledger if r['player']==seat and r['op']=='SELL' and r['item']=='TOMATO']
            r=dict(arm=name,seat=seat,changed_action_turns=changed,rewards=[s.reward for s in env.steps[-1]],
                   report=report,daily=daily,tomato_sold=len(sales),tomato_revenue=sum(r['value'] for r in sales))
            result.append(r)
            dest=OUT/f'early_tomato_smoke.{name}.{seat}.ledger.jsonl.gz'
            dest.write_bytes(gzip.compress(('\n'.join(json.dumps(x) for x in ledger)+'\n').encode(),mtime=0))
            print(json.dumps(r),flush=True)
    (OUT/'early_tomato_smoke.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
