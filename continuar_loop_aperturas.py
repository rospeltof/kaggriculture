"""Round12: controlled native openings and a freshly audited public reference."""
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
        if state.get('phase') == 'eleven_rounds_complete':
            break
        time.sleep(5)
    validation = json.loads((loop.OUT/'opening_validation.json').read_text())
    manifest = json.loads((loop.OUT/'opening_variants.json').read_text())
    assert validation['passed']
    assert validation['candidate_hashes'] == {n: r['sha256'] for n, r in manifest.items()}
    loop.BASE = 'submission/main_publico_arshs3_vq_top3.py'
    variants = {n: r['path'] for n, r in manifest.items()}
    prefix = loop.run('pilot12', variants, 1025000, 8)
    report = loop.analyze(prefix, variants, 2, lambda n: 'candidate', 2)
    result = loop.confirmation('confirm12', report['selected_for_confirmation'], variants, 1026000)
    loop.save('twelve_rounds_complete', state='complete', pilot12=report, confirm12=result,
              next_action='Review opening capital, production and source diversity; decide next experiment from evidence. Goal remains active.')


if __name__ == '__main__':
    try:
        main()
    except BaseException as exc:
        loop.save('loop12_failed', state='failed', error=repr(exc))
        raise
