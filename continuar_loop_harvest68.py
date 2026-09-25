"""Loop22: public Harvest V68 and selector-off ablation, VQ control."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import time

import continuar_loop_publicos as loop


def analyze(prefix, candidates, limit):
    arms = {**candidates, 'vq': 'submission/main_publico_arshs3_vq.py'}
    report = loop.analyze(prefix, arms, 0, lambda n: n, 0)
    report['results']['vq']['status'] = 'DIAGNOSTIC_CONTROL_ONLY'
    report['selected_for_confirmation'] = sorted((n for n in candidates if report['results'][n]['delta_points'] > 0),
                                               key=lambda n: (-report['results'][n]['delta_points'], n))[:limit]
    for name in candidates:
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            versus_vq = loop.paired(str(prefix)+'.jsonl', 'vq', name, ','.join(['base', 'noop', *(n for n in candidates if n != name)]))
        report['results'][name]['versus_vq'] = versus_vq
        Path(str(prefix)+f'.{name}.versus_vq.txt').write_text(captured.getvalue())
    if 'harvest68' in candidates and 'harvest68_no_ev' in candidates:
        captured=io.StringIO()
        with contextlib.redirect_stdout(captured):
            report['selector_effect']=loop.paired(str(prefix)+'.jsonl','harvest68_no_ev','harvest68','base,noop,vq')
        Path(str(prefix)+'.selector_effect.txt').write_text(captured.getvalue())
    return report


def main():
    while True:
        try: state = json.loads(loop.STATE.read_text())
        except (FileNotFoundError, json.JSONDecodeError): state = {}
        if state.get('state') == 'failed': raise RuntimeError(state)
        if state.get('phase') == 'twenty_one_rounds_complete': break
        time.sleep(5)
    validation = json.loads((loop.OUT/'public_0712_validation.json').read_text())
    manifest = json.loads((loop.OUT/'public_0712_variants.json').read_text())
    fresh = json.loads((loop.OUT/'public_0548_variants.json').read_text())
    assert validation['passed'] and validation['competitive_ready']
    assert validation['candidate_hashes'] == {n: r['sha256'] for n, r in manifest.items()}
    for name, spec in {**manifest, **fresh}.items():
        assert hashlib.sha256(Path(spec['path']).read_bytes()).hexdigest() == spec['sha256'], name
    vq = 'submission/main_publico_arshs3_vq.py'
    assert hashlib.sha256(Path(vq).read_bytes()).hexdigest() == validation['control_hash']
    loop.BASE = 'submission/main_publico_arshs3_vq_top3.py'
    assert hashlib.sha256(Path(loop.BASE).read_bytes()).hexdigest() == '9668e30ad08f79d485bd230a3c660d4cc420b9382e87f9387b6908e3c94a5145'
    variants = {n: r['path'] for n, r in manifest.items()}
    pool = {n: p for n, p in {**loop.POOL, **loop.EXTRA}.items() if n in ('arshs3', 'tds', 'hybu', 'ars40')}
    pool.update({n: r['path'] for n, r in fresh.items()})
    prefix = loop.run('pilot22', dict(variants, vq=vq), 1055000, 16, pool)
    report = analyze(prefix, variants, 2)
    (loop.OUT/'pilot22.results.json').write_text(json.dumps(report, indent=2, allow_nan=False)+'\n')
    selected = report['selected_for_confirmation']; result = None
    if selected:
        chosen = {n: variants[n] for n in selected}; expanded = {**loop.POOL, **loop.EXTRA, **{n: r['path'] for n, r in fresh.items()}}
        prefix = loop.run('confirm22', dict(chosen, vq=vq), 1056000, 16, expanded)
        result = analyze(prefix, chosen, 0)
        for name in chosen:
            row = result['results'][name]
            eligible = row['delta_points'] >= 3 and min(row['opponent_breakdown'].values()) >= -20 and row['versus_vq']['delta_points'] >= 0
            row['registered_submission_gate'] = eligible
            if eligible: row['status'] = 'REAL_WORLD_CANDIDATE'
        (loop.OUT/'confirm22.results.json').write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    loop.save('twenty_two_rounds_complete', state='complete', pilot22=report, confirm22=result,
              next_action='Review remaining-season herd changes and the selector-off comparison, both baselines, runtime and current ladder. Continue autonomous research; goal remains active.')


if __name__ == '__main__':
    try: main()
    except BaseException as exc:
        loop.save('loop22_failed', state='failed', error=repr(exc)); raise
