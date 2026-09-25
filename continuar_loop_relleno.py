"""Séptima ronda; cobertura espacial en más mundos y cuatro rivales fijados."""
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
        if s.get('phase')=='six_rounds_complete':break
        time.sleep(5)
    loop.BASE='submission/main_publico_arshs3_vq_top3.py'
    variants={n:r['path'] for n,r in json.loads((loop.OUT/'infill_variants.json').read_text()).items()}
    pool={n:p for n,p in {**loop.POOL,**loop.EXTRA}.items() if n in ('arshs3','tds','hybu','ars40')}
    prefix=loop.run('pilot7',variants,1010000,16,pool)
    report=loop.analyze(prefix,variants,2,lambda n:'infill',2)
    result=loop.confirmation('confirm7',report['selected_for_confirmation'],variants,1011000)
    if result:
        selected=report['selected_for_confirmation']
        for name,r in result['results'].items():
            r['shared_eight_rival_panel']=r.pop('original_pool_only')
            extra_rivals=[n for n in {**loop.POOL,**loop.EXTRA} if n not in pool]
            with contextlib.redirect_stdout(io.StringIO()):
                r['pilot_pool_only']=loop.paired(str(loop.OUT/'confirm7.jsonl'),'base',name,','.join(['noop',*[n for n in selected if n!=name],*extra_rivals]))
        (loop.OUT/'confirm7.results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    loop.save('seven_rounds_complete',state='complete',pilot7=report,confirm7=result,
              next_action='Inspect spatial coverage and actual returns, review ladder, continue research. Goal remains active.')


if __name__=='__main__':
    try:main()
    except BaseException as exc:
        loop.save('loop7_failed',state='failed',error=repr(exc));raise
