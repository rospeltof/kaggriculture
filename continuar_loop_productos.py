"""Sexta ronda, con top3 como referencia explícita y controles factoriales."""
import contextlib
import io
import json
from pathlib import Path
import time

import continuar_loop_publicos as loop


def main():
    while True:
        try:s=json.loads(loop.STATE.read_text())
        except (FileNotFoundError,json.JSONDecodeError):s={}
        if s.get('state')=='failed':raise RuntimeError(s)
        if s.get('phase')=='five_rounds_complete':break
        time.sleep(5)
    loop.BASE='submission/main_publico_arshs3_vq_top3.py'
    variants={n:r['path'] for n,r in json.loads((loop.OUT/'forecast_products_variants.json').read_text()).items()}
    controls={'vq_control':'submission/main_publico_arshs3_vq.py',
              'fast2_control':'results/loop_publicos_20260925/pred_fast2.py'}
    all_arms={**variants,**controls};prefix=loop.run('pilot6',all_arms,1007000,4)
    loop.validate(str(prefix));results={}
    for name in all_arms:
        txt=io.StringIO()
        with contextlib.redirect_stdout(txt):
            r=loop.paired(str(prefix)+'.jsonl','base',name,','.join(['noop',*[n for n in all_arms if n!=name]]))
        r['status']='CONTROL' if name in controls else 'PROMISING' if r['delta_points']>0 else 'INCONCLUSIVE_NOT_SELECTED'
        if name not in controls and r['ci95_2way'] is not None and r['ci95_2way'][1]<0:r['status']='REJECTED'
        results[name]=r;Path(str(prefix)+'.'+name+'.txt').write_text(txt.getvalue())
    selected=sorted((n for n in variants if results[n]['delta_points']>0),key=lambda n:(-results[n]['delta_points'],n))[:2]
    report=dict(reference='top3',results=results,selected_for_confirmation=selected)
    Path(str(prefix)+'.results.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    result=loop.confirmation('confirm6',selected,variants,1008000)
    loop.save('six_rounds_complete',state='complete',pilot6=report,confirm6=result,
              next_action='Review coverage and interactions, inspect current ladder, continue with a new hypothesis. Goal remains active.')


if __name__=='__main__':
    try:main()
    except BaseException as exc:
        loop.save('loop6_failed',state='failed',error=repr(exc));raise
