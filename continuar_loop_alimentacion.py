"""Round14: native feed-value rule after the registered night-stock block."""
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
        if state.get('phase') == 'thirteen_rounds_complete':
            break
        time.sleep(5)
    validation = json.loads((loop.OUT/'feed_validation.json').read_text())
    manifest = json.loads((loop.OUT/'feed_variants.json').read_text())
    assert validation['passed']
    assert validation['candidate_hashes'] == {n: r['sha256'] for n, r in manifest.items()}
    loop.BASE = 'submission/main_publico_arshs3_vq_top3.py'
    variants = {n: r['path'] for n, r in manifest.items()}
    pool = {k: loop.POOL[k] for k in ('tds', 'hybu', 'ars40')}
    pool['arshs3'] = loop.EXTRA['arshs3']
    prefix = loop.run('pilot14', variants, 1031000, 16, pool)
    report = loop.analyze(prefix, variants, 2, lambda n: 'candidate', 2)
    result = loop.confirmation('confirm14', report['selected_for_confirmation'], variants, 1032000)
    loop.save('fourteen_rounds_complete', state='complete', pilot14=report, confirm14=result,
              next_action='Review food cost, accepted production, W/L/T and mechanisms; continue autonomous research. Goal remains active.')


if __name__ == '__main__':
    try:
        main()
    except BaseException as exc:
        loop.save('loop14_failed', state='failed', error=repr(exc))
        raise
