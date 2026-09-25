"""Eighth registered round; serialize after the spatial investment block."""
import json
import time

import continuar_loop_publicos as loop


def main():
    while True:
        try:
            state = json.loads(loop.STATE.read_text())
        except (FileNotFoundError, json.JSONDecodeError):
            state = {}
        if state.get('state') == 'failed':
            raise RuntimeError(state)
        if state.get('phase') == 'seven_rounds_complete':
            break
        time.sleep(5)
    loop.BASE = 'submission/main_publico_arshs3_vq_top3.py'
    variants = {n: r['path'] for n, r in json.loads((loop.OUT / 'patterns_variants.json').read_text()).items()}
    prefix = loop.run('pilot8', variants, 1013000, 8)
    report = loop.analyze(prefix, variants, 2, lambda n: 'patterns', 2)
    confirmation = loop.confirmation('confirm8', report['selected_for_confirmation'], variants, 1014000)
    loop.save('eight_rounds_complete', state='complete', pilot8=report, confirm8=confirmation,
              next_action='Inspect mechanisms, behavior, runtime and real ladder; continue research. Goal remains active.')


if __name__ == '__main__':
    try:
        main()
    except BaseException as exc:
        loop.save('loop8_failed', state='failed', error=repr(exc))
        raise
