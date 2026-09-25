"""Corre la tercera ronda registrada cuando terminen las dos primeras."""
import json
import time

from continuar_loop_publicos import OUT, STATE, run, analyze, confirmation, save


def main():
    while True:
        try:s=json.loads(STATE.read_text())
        except (FileNotFoundError,json.JSONDecodeError):s={}
        if s.get('state')=='failed':raise RuntimeError(s)
        if s.get('phase')=='registered_blocks_complete':break
        time.sleep(5)
    variants={n:r['path'] for n,r in json.loads((OUT/'herd_variants.json').read_text()).items()}
    p=run('pilot3',variants,1001000,4)
    report=analyze(p,variants,2,lambda n:n,1)
    result=confirmation('confirm3',report['selected_for_confirmation'],variants,1002000)
    save('three_rounds_complete',state='complete',pilot3=report,confirm3=result,
         next_action='Review all saved scorecards, mechanism and ladder evidence; choose the next experiment or justified submission. Research goal remains active.')


if __name__=='__main__':
    try:main()
    except BaseException as exc:
        save('loop3_failed',state='failed',error=repr(exc));raise
