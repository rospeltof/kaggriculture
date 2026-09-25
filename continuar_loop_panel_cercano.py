"""Loop25: fixed contemporary mirror panel, independent of prior panel selection."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import time

import continuar_loop_publicos as loop
from continuar_loop_adelanto_trigo import changed_seeds


def verify_sources(manifest):
    groups = ('candidates', 'controls', 'pilot_pool', 'confirm_extra', 'prior_validation')
    items = [item for group in groups for item in manifest[group].values()]
    items += [manifest['prereg'], manifest['source_archive']]
    for item in items:
        assert hashlib.sha256(Path(item['path']).read_bytes()).hexdigest() == item['sha256'], item['path']


def analyze(prefix, candidates, control, limit):
    report = loop.analyze(prefix, dict(candidates, top3=control), 0, lambda n: n, 0)
    report['results']['top3']['status'] = 'DIAGNOSTIC_CONTROL_ONLY'
    for name in candidates:
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            comparison = loop.paired(str(prefix) + '.jsonl', 'top3', name,
                                     ','.join(['base', 'noop', *(n for n in candidates if n != name)]))
        report['results'][name]['versus_top3'] = comparison
        Path(str(prefix) + f'.{name}.versus_top3.txt').write_text(captured.getvalue())
    eligible = [name for name in candidates if min(report['results'][name]['delta_points'],
                report['results'][name]['versus_top3']['delta_points']) > 0]
    report['selected_for_confirmation'] = sorted(eligible, key=lambda name: (
        -min(report['results'][name]['delta_points'],
             report['results'][name]['versus_top3']['delta_points']), name))[:limit]
    return report


def main():
    manifest = json.loads((loop.OUT / 'close_panel_manifest.json').read_text())
    validation = json.loads((loop.OUT / 'close_panel_validation.json').read_text())
    assert validation['passed']
    assert hashlib.sha256((loop.OUT / 'close_panel_manifest.json').read_bytes()).hexdigest() == validation['manifest_sha256']
    verify_sources(manifest)
    print('Loop25 sources frozen and verified; waiting for loop24.', flush=True)
    while True:
        try:
            state = json.loads(loop.STATE.read_text())
        except (FileNotFoundError, json.JSONDecodeError):
            state = {}
        if state.get('state') == 'failed':
            raise RuntimeError(state)
        if state.get('phase') == 'twenty_four_rounds_complete':
            break
        time.sleep(5)
    verify_sources(manifest)
    loop.BASE = manifest['controls']['base']['path']
    control = manifest['controls']['top3']['path']
    candidates = {name: item['path'] for name, item in manifest['candidates'].items()}
    pool = {name: item['path'] for name, item in manifest['pilot_pool'].items()}
    prefix = loop.run('pilot25', dict(candidates, top3=control), 1063000, 16, pool)
    report = analyze(prefix, candidates, control, 2)
    (loop.OUT / 'pilot25.results.json').write_text(json.dumps(report, indent=2, allow_nan=False) + '\n')
    selected = report['selected_for_confirmation']
    result = None
    if selected:
        chosen = {name: candidates[name] for name in selected}
        expanded = dict(pool, **{name: item['path'] for name, item in manifest['confirm_extra'].items()})
        prefix = loop.run('confirm25', dict(chosen, top3=control), 1064000, 32, expanded)
        result = analyze(prefix, chosen, control, 0)
        for name in chosen:
            row = result['results'][name]
            parent = manifest['candidates'][name]['behavior_reference']
            row['behavior_reference'] = parent
            row['changed_seeds_vs_behavior_reference'] = changed_seeds(prefix, name, parent, chosen)
            comparisons = (row, row['versus_top3'])
            eligible = (all(item['delta_points'] >= 3 and min(item['opponent_breakdown'].values()) >= -20
                            for item in comparisons)
                        and len(row['changed_seeds_vs_behavior_reference']) >= 2)
            row['registered_submission_gate'] = eligible
            if eligible:
                row['status'] = 'REAL_WORLD_CANDIDATE_REVIEW_REQUIRED'
            for reference in ('base', 'top3'):
                for label, exclude_pool in (
                    ('original_four', list(manifest['confirm_extra'])),
                    ('added_two', list(manifest['pilot_pool'])),
                ):
                    excluded = ['noop', *(n for n in ('base', 'top3', *chosen) if n not in (reference, name)), *exclude_pool]
                    captured = io.StringIO()
                    with contextlib.redirect_stdout(captured):
                        comparison = loop.paired(str(prefix) + '.jsonl', reference, name, ','.join(excluded))
                    row[f'{label}_versus_{reference}'] = comparison
                    Path(str(prefix) + f'.{name}.{label}.versus_{reference}.txt').write_text(captured.getvalue())
        (loop.OUT / 'confirm25.results.json').write_text(json.dumps(result, indent=2, allow_nan=False) + '\n')
    loop.save('twenty_five_rounds_complete', state='complete', pilot25=report, confirm25=result,
              next_action='Review mechanisms, both submitted references and panel sensitivity. No automatic submission; continue research.')


if __name__ == '__main__':
    try:
        main()
    except BaseException as exc:
        loop.save('loop25_failed', state='failed', error=repr(exc))
        raise
