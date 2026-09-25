"""Round13: final-night input rebalancing after the registered opening block."""
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
        if state.get('phase') == 'twelve_rounds_complete':
            break
        time.sleep(5)
    validation = json.loads((loop.OUT/'night_validation.json').read_text())
    manifest = json.loads((loop.OUT/'night_variants.json').read_text())
    assert validation['passed']
    assert validation['candidate_hashes'] == {n: r['sha256'] for n, r in manifest.items()}
    loop.BASE = 'submission/main_publico_arshs3_vq_top3.py'
    variants = {n: r['path'] for n, r in manifest.items()}
    pool = {k: loop.POOL[k] for k in ('tds', 'hybu', 'ars40')}
    pool['arshs3'] = loop.EXTRA['arshs3']
    prefix = loop.run('pilot13', variants, 1028000, 16, pool)
    report = loop.analyze(prefix, variants, 2, lambda n: 'candidate', 2)
    result = loop.confirmation('confirm13', report['selected_for_confirmation'], variants, 1029000)
    loop.save('thirteen_rounds_complete', state='complete', pilot13=report, confirm13=result,
              next_action='Review night-loss reduction, reserves, production and W/L/T, then continue research. Goal remains active.')


if __name__ == '__main__':
    try:
        main()
    except BaseException as exc:
        loop.save('loop13_failed', state='failed', error=repr(exc))
        raise
