"""Round11 uses 32 worlds per block because source coverage is only 10/64 pairs."""
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
        if state.get('phase') == 'ten_rounds_complete':
            break
        time.sleep(5)
    validation = json.loads((loop.OUT/'library_validation.json').read_text())
    manifest = json.loads((loop.OUT/'library_variants.json').read_text())
    assert validation['passed']
    assert validation['candidate_hashes'] == {n: r['sha256'] for n, r in manifest.items()}
    loop.BASE = 'submission/main_publico_arshs3_vq_top3.py'
    variants = {n: r['path'] for n, r in manifest.items()}
    pool = {n: p for n, p in {**loop.POOL, **loop.EXTRA}.items() if n in ('arshs3', 'tds', 'hybu', 'ars40')}
    prefix = loop.run('pilot11', variants, 1021000, 32, pool)
    report = loop.analyze(prefix, variants, 2, lambda n: 'library', 2)
    selected = report['selected_for_confirmation']
    result = None
    if selected:
        chosen = {n: variants[n] for n in selected}
        expanded = {**loop.POOL, **loop.EXTRA}
        prefix = loop.run('confirm11', chosen, 1022000, 32, expanded)
        result = loop.analyze(prefix, chosen, 0, lambda n: n, 0)
        excluded = [n for n in expanded if n not in pool]
        for name, row in result['results'].items():
            eligible = row['delta_points'] >= 3 and min(row['opponent_breakdown'].values()) >= -20
            row['registered_submission_gate'] = eligible
            if eligible:
                row['status'] = 'REAL_WORLD_CANDIDATE'
            with contextlib.redirect_stdout(io.StringIO()):
                row['pilot_pool_only'] = loop.paired(str(prefix)+'.jsonl', 'base', name,
                    ','.join(['noop', *[n for n in selected if n != name], *excluded]))
        (loop.OUT/'confirm11.results.json').write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    loop.save('eleven_rounds_complete', state='complete', pilot11=report, confirm11=result,
              next_action='Review new-stream selection, forecasting effects and ladder; continue research. Goal remains active.')


if __name__ == '__main__':
    try:
        main()
    except BaseException as exc:
        loop.save('loop11_failed', state='failed', error=repr(exc))
        raise
