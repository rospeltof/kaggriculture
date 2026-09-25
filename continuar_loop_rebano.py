"""Ninth registered round; launch only after development validation is frozen."""
import contextlib
import io
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
        if state.get('phase') == 'eight_rounds_complete':
            break
        time.sleep(5)
    loop.BASE = 'submission/main_publico_arshs3_vq_top3.py'
    variants = {n: r['path'] for n, r in json.loads((loop.OUT / 'sheep_space_variants.json').read_text()).items()}
    pool = {n: p for n, p in {**loop.POOL, **loop.EXTRA}.items() if n in ('arshs3', 'tds', 'hybu', 'ars40')}
    prefix = loop.run('pilot9', variants, 1015000, 16, pool)
    report = loop.analyze(prefix, variants, 2, lambda n: 'sheep', 2)
    result = loop.confirmation('confirm9', report['selected_for_confirmation'], variants, 1016000)
    if result:
        selected = report['selected_for_confirmation']
        excluded = [n for n in {**loop.POOL, **loop.EXTRA} if n not in pool]
        for name, row in result['results'].items():
            row['shared_eight_rival_panel'] = row.pop('original_pool_only')
            with contextlib.redirect_stdout(io.StringIO()):
                row['pilot_pool_only'] = loop.paired(str(loop.OUT/'confirm9.jsonl'), 'base', name,
                    ','.join(['noop', *[n for n in selected if n != name], *excluded]))
        (loop.OUT/'confirm9.results.json').write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    loop.save('nine_rounds_complete', state='complete', pilot9=report, confirm9=result,
              next_action='Audit sheep productivity, marginal costs and effects on the parent; review ladder and continue. Goal remains active.')


if __name__ == '__main__':
    try:
        main()
    except BaseException as exc:
        loop.save('loop9_failed', state='failed', error=repr(exc))
        raise
