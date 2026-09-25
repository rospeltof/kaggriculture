"""Encadena bloques registrados usando el harness existente, sin envíos automáticos.

Es un planificador de corridas: no define otra simulación ni otra estadística.
Puede retomarse leyendo su estado; jamás sobrescribe un bloque ya comenzado.
"""
import contextlib
from datetime import datetime, timezone
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from pareado_torneo import main as paired
from validar_torneo import validate

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'docs/evidencia/loop_publicos_20260925'
STATE=OUT/'pipeline_state.json'
PYTHON=ROOT/'.venv/bin/python'
BASE='submission/main_publico_arshs3_vq.py'
POOL={
    'tds':'submission/main_publico_tds_tetsutani.py',
    'hybu':'results/publicos/wzhengbiao_kaggriculture-hybu-submit/main.py',
    'ars40':'results/publicos/arsgorynich_kaggriculture-v40-challenger/main.py',
    'hsov':'results/publicos/haideptry_the-shepherds-ledger-herd-safe-sovereign/main.py',
    'v13':'submission/main_publico_v13_thomastschinkel.py',
    'obr':'results/publicos/arsgorynich_order-book-v3-response-improvement/main.py',
    'h2965':'results/publicos/haideptry_the-2965-master-hybrid-engine/main.py',
    'guru6':'results/publicos/guruprasaathas111_kaggriculture-master-engine-v3/main.py',
}
EXTRA={'tds25':'results/publicos_20260925/tds/main.py',
       'hl25':'results/publicos_20260925/hl/main.py',
       'arshs3':'submission/main_publico_arshs3_arsgorynich.py'}


def save(phase,**kw):
    state=dict(phase=phase,updated_at=datetime.now(timezone.utc).isoformat(),**kw)
    temp=STATE.with_suffix('.tmp');temp.write_text(json.dumps(state,indent=2)+'\n');temp.replace(STATE)
    print(json.dumps(state),flush=True)


def read_meta(prefix):
    try:return json.loads(prefix.with_suffix('.meta.json').read_text())
    except (FileNotFoundError,json.JSONDecodeError):return None


def wait_complete(prefix):
    while True:
        m=read_meta(prefix)
        if m and m['state']=='complete':return
        if m and m['state']=='failed':raise RuntimeError(m)
        time.sleep(5)


def run(name,variants,seed0,seeds,pool=None):
    prefix=OUT/name;m=read_meta(prefix)
    if m:
        if m['state']=='complete':return prefix
        raise RuntimeError(f'Bloque ya iniciado, inspeccionar antes de retomar: {prefix}')
    pool=POOL if pool is None else pool
    agents={'base':BASE,'noop':BASE,**variants,**pool}
    arms=['base','noop',*variants]
    cmd=[str(PYTHON),'-u','torneo.py','--out',str(prefix.relative_to(ROOT)),
         '--seeds',str(seeds),'--seed0',str(seed0),'--workers','8','--vs',','.join(arms)]
    cmd.extend(n+'='+p for n,p in agents.items())
    save(name,state='running',command=cmd)
    with (ROOT/'results'/f'{name}_20260925.log').open('x') as log:
        subprocess.run(cmd,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True,
                       env=dict(os.environ, PYTHONHASHSEED='0'))
    return prefix


def analyze(prefix,variants,limit,family,per_family):
    validate(str(prefix))
    results={};arms=['base','noop',*variants]
    for arm in variants:
        text=io.StringIO()
        with contextlib.redirect_stdout(text):
            r=paired(str(prefix)+'.jsonl','base',arm,','.join(a for a in arms if a not in ('base',arm)))
        Path(str(prefix)+f'.{arm}.txt').write_text(text.getvalue())
        r['status']='PROMISING' if r['delta_points']>0 else 'INCONCLUSIVE_NOT_SELECTED'
        if r['ci95_2way'] is not None and r['ci95_2way'][1]<0:r['status']='REJECTED'
        results[arm]=r
    selected=[];families={}
    for name in sorted(results,key=lambda n:(-results[n]['delta_points'],n)):
        group=family(name)
        if results[name]['delta_points']<=0 or families.get(group,0)>=per_family:continue
        if len(selected)>=limit:break
        selected.append(name);families[group]=families.get(group,0)+1
    report=dict(results=results,selected_for_confirmation=selected)
    Path(str(prefix)+'.results.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'block':prefix.name,'deltas':{n:r['delta_points'] for n,r in results.items()},'selected':selected}),flush=True)
    return report


def confirmation(name,selected,variants,seed0):
    if not selected:return None
    vv={n:variants[n] for n in selected}
    prefix=run(name,vv,seed0,16,{**POOL,**EXTRA})
    result=analyze(prefix,vv,0,lambda n:n,0)
    for n,r in result['results'].items():
        eligible=r['delta_points']>=3 and min(r['opponent_breakdown'].values())>=-20
        r['status']='REAL_WORLD_CANDIDATE' if eligible else r['status']
        r['registered_submission_gate']=eligible
        txt=io.StringIO()
        with contextlib.redirect_stdout(txt):
            r['original_pool_only']=paired(str(prefix)+'.jsonl','base',n,','.join(['noop',*[a for a in vv if a!=n],*EXTRA]))
    Path(str(prefix)+'.results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    return result


def main():
    v1={n:r['path'] for n,r in json.loads((OUT/'variants.json').read_text()).items()}
    v2={n:r['path'] for f in ('recovery_variants.json','tomato_variants.json') for n,r in json.loads((OUT/f).read_text()).items()}
    save('waiting_loop1',state='running')
    wait_complete(OUT/'pilot')
    r1=analyze(OUT/'pilot',v1,3,lambda n:n.split('_')[0] if n.startswith('pred') else 'crop',2)
    p2=run('pilot2',v2,998000,4)
    r2=analyze(p2,v2,2,lambda n:'recover' if n.startswith('recover') else 'tomato',1)
    c1=confirmation('confirm1',r1['selected_for_confirmation'],v1,996000)
    c2=confirmation('confirm2',r2['selected_for_confirmation'],v2,999000)
    save('registered_blocks_complete',state='complete',pilot1=r1,pilot2=r2,confirm1=c1,confirm2=c2,
         next_action='Review mechanisms, runtime and ladder before any upload; continue with next hypothesis. Optional neutral-repair mirror block is not automatically launched.')


if __name__=='__main__':
    try:main()
    except BaseException as exc:
        save('failed',state='failed',error=repr(exc));raise
