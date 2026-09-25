"""Quinta ronda, tras el bloque registrado de cobertura de reparación."""
import json
import time

from continuar_loop_publicos import OUT, STATE, run, analyze, confirmation, save


def main():
    while True:
        try:s=json.loads(STATE.read_text())
        except (FileNotFoundError,json.JSONDecodeError):s={}
        if s.get('state')=='failed':raise RuntimeError(s)
        if s.get('phase')=='four_rounds_complete':break
        time.sleep(5)
    variants={n:r['path'] for n,r in json.loads((OUT/'early_tomato_variants.json').read_text()).items()}
    p=run('pilot5',variants,1005000,4)
    report=analyze(p,variants,2,lambda n:'tomato',2)
    result=confirmation('confirm5',report['selected_for_confirmation'],variants,1006000)
    save('five_rounds_complete',state='complete',pilot5=report,confirm5=result,
         next_action='Review tomato activation and costs, then continue research. No automatic upload; goal remains active.')


if __name__=='__main__':
    try:main()
    except BaseException as exc:
        save('loop5_failed',state='failed',error=repr(exc));raise
