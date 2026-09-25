"""Tenth registered round, after the early-substitution execution audit."""
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
        if state.get('phase') == 'nine_rounds_complete':
            break
        time.sleep(5)
    validation = json.loads((loop.OUT/'early_cow_validation.json').read_text())
    assert validation['passed']
    manifest = json.loads((loop.OUT/'early_cow_variants.json').read_text())
    assert validation['candidate_hashes'] == {n: r['sha256'] for n, r in manifest.items()}
    loop.BASE = 'submission/main_publico_arshs3_vq_top3.py'
    variants = {n: r['path'] for n, r in manifest.items()}
    pool = {n: p for n, p in {**loop.POOL, **loop.EXTRA}.items() if n in ('arshs3', 'tds', 'hybu', 'ars40')}
    prefix = loop.run('pilot10', variants, 1018000, 16, pool)
    report = loop.analyze(prefix, variants, 2, lambda n: 'early_cow', 2)
    result = loop.confirmation('confirm10', report['selected_for_confirmation'], variants, 1019000)
    if result:
        selected = report['selected_for_confirmation']
        excluded = [n for n in {**loop.POOL, **loop.EXTRA} if n not in pool]
        for name, row in result['results'].items():
            row['shared_eight_rival_panel'] = row.pop('original_pool_only')
            with contextlib.redirect_stdout(io.StringIO()):
                row['pilot_pool_only'] = loop.paired(str(loop.OUT/'confirm10.jsonl'), 'base', name,
                    ','.join(['noop', *[n for n in selected if n != name], *excluded]))
        (loop.OUT/'confirm10.results.json').write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    loop.save('ten_rounds_complete', state='complete', pilot10=report, confirm10=result,
              next_action='Audit substitutions, accepted production and foregone milk; review ladder and continue. Goal remains active.')


if __name__ == '__main__':
    try:
        main()
    except BaseException as exc:
        loop.save('loop10_failed', state='failed', error=repr(exc))
        raise
