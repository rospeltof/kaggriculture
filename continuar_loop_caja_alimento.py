"""Round15: future-input funding, with the old policy as a diagnostic control."""
import contextlib
import io
import hashlib
import json
from pathlib import Path
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
        if state.get('phase') == 'fourteen_rounds_complete':
            break
        time.sleep(5)
    validation = json.loads((loop.OUT/'cash_validation.json').read_text())
    manifest = json.loads((loop.OUT/'cash_variants.json').read_text())
    assert validation['passed']
    assert validation['candidate_hashes'] == {n: r['sha256'] for n, r in manifest.items()}
    loop.BASE = 'submission/main_publico_arshs3_vq_top3.py'
    variants = {n: r['path'] for n, r in manifest.items()}
    legacy = 'results/vacas_tempranas_20260925/cow_d3_y1_m100.py'
    for name, spec in manifest.items():
        assert hashlib.sha256(Path(spec['path']).read_bytes()).hexdigest() == spec['sha256'], name
    assert hashlib.sha256(Path(legacy).read_bytes()).hexdigest() == validation['legacy_hash']
    all_arms = dict(variants, legacy=legacy)
    pool = {k: loop.POOL[k] for k in ('tds', 'hybu', 'ars40')}
    pool['arshs3'] = loop.EXTRA['arshs3']
    prefix = loop.run('pilot15', all_arms, 1034000, 16, pool)
    report = loop.analyze(prefix, all_arms, 0, lambda n: n, 0)
    # The registered control cannot displace a candidate in selection.
    report['results']['legacy']['status'] = 'DIAGNOSTIC_CONTROL_ONLY'
    selected = sorted((n for n in variants if report['results'][n]['delta_points'] > 0),
                      key=lambda n: (-report['results'][n]['delta_points'], n))[:2]
    report['selected_for_confirmation'] = selected
    secondary = {}
    for name in variants:
        excluded = ','.join(['base', 'noop', *(n for n in variants if n != name)])
        text = io.StringIO()
        with contextlib.redirect_stdout(text):
            secondary[name] = loop.paired(str(prefix)+'.jsonl', 'legacy', name, excluded)
        (loop.OUT/f'pilot15.{name}.versus_legacy.txt').write_text(text.getvalue())
    report['secondary_vs_legacy'] = secondary
    (loop.OUT/'pilot15.results.json').write_text(json.dumps(report, indent=2, allow_nan=False)+'\n')
    result = loop.confirmation('confirm15', selected, variants, 1035000)
    loop.save('fifteen_rounds_complete', state='complete', pilot15=report, confirm15=result,
              next_action='Review funding, accepted food/animals, W/L/T and real feedback; continue autonomous research. Goal remains active.')


if __name__ == '__main__':
    try:
        main()
    except BaseException as exc:
        loop.save('loop15_failed', state='failed', error=repr(exc))
        raise
