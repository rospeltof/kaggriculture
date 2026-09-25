"""Loop31: close queue with both live references and ineligible town50 controls."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import time

import continuar_loop_publicos as loop
from continuar_loop_adelanto_trigo import changed_seeds
from continuar_loop_panel_cercano import analyze as two_reference_analysis, verify_sources


def choose(results, candidates, limit):
    eligible = [name for name in candidates
                if min(results[name]['delta_points'], results[name]['versus_top3']['delta_points']) > 0
                and results[name]['versus_town50']['delta_points'] >= 0]
    return sorted(eligible, key=lambda name: (
        -min(results[name]['delta_points'], results[name]['versus_top3']['delta_points']), name))[:limit]


def analyze(prefix, candidates, old_controls, parents, top3, pool, limit):
    nonpool = dict(candidates, **old_controls)
    report = two_reference_analysis(prefix, nonpool, top3, 0)
    for name in old_controls:
        report['results'][name]['status'] = 'DIAGNOSTIC_CONTROL_ONLY'
    for name in candidates:
        parent = parents[name]
        excluded = ['base', 'noop', 'top3', *(n for n in nonpool if n not in (parent, name))]
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            comparison = loop.paired(str(prefix) + '.jsonl', parent, name, ','.join(excluded))
        row = report['results'][name]
        row['versus_town50'] = comparison
        row['behavior_reference'] = parent
        row['changed_seeds_vs_town50'] = changed_seeds(prefix, name, parent, nonpool)
        for result in (row, row['versus_top3'], comparison):
            assert result['rivals'] == sorted(pool), (name, result['rivals'])
        Path(str(prefix) + f'.{name}.versus_town50.txt').write_text(captured.getvalue())
    report['selected_for_confirmation'] = choose(report['results'], candidates, limit)
    return report


def submission_gate(row):
    return (row['delta_points'] >= 3 and row['versus_top3']['delta_points'] >= 0
            and row['versus_town50']['delta_points'] >= 0
            and all(min(result['opponent_breakdown'].values()) >= -20
                    for result in (row, row['versus_top3'], row['versus_town50']))
            and len(row['changed_seeds_vs_town50']) >= 2)


def main():
    validation = json.loads((loop.OUT / 'close_queue_validation.json').read_text())
    fixture = json.loads((loop.OUT / 'close_queue_analysis_validation.json').read_text())
    candidates = json.loads((loop.OUT / 'close_queue_variants.json').read_text())
    panel = json.loads((loop.OUT / 'close_panel_manifest.json').read_text())
    old = {spec['behavior_reference']: spec['source_parent'] for spec in candidates.values()}
    assert validation['passed'] and validation['competitive_ready'] and fixture['passed']
    assert validation['candidate_hashes'] == {n: s['sha256'] for n, s in candidates.items()}
    assert validation['parent_hashes'] == {n: s['sha256'] for n, s in old.items()}

    def verify():
        verify_sources(panel)
        for spec in {**candidates, **old}.values():
            assert hashlib.sha256(Path(spec['path']).read_bytes()).hexdigest() == spec['sha256']
        assert hashlib.sha256(Path(__file__).read_bytes()).hexdigest() == fixture['analysis_source_sha256']

    verify()
    print('Loop31 mechanics, three-reference analysis and frozen sources verified; waiting for loop30.', flush=True)
    while True:
        try:
            state = json.loads(loop.STATE.read_text())
        except (FileNotFoundError, json.JSONDecodeError):
            state = {}
        if state.get('state') == 'failed':
            raise RuntimeError(state)
        if state.get('phase') == 'thirty_rounds_complete':
            break
        time.sleep(5)
    verify()
    loop.BASE = panel['controls']['base']['path']
    top3 = panel['controls']['top3']['path']
    assert panel['controls']['base']['sha256'] == validation['base_hash']
    assert panel['controls']['top3']['sha256'] == validation['control_hash']
    variants = {n: s['path'] for n, s in candidates.items()}
    parents = {n: s['behavior_reference'] for n, s in candidates.items()}
    old_paths = {n: s['path'] for n, s in old.items()}
    pool = {n: s['path'] for n, s in panel['pilot_pool'].items()}
    prefix = loop.run('pilot31', dict(variants, **old_paths, top3=top3), 1081000, 16, pool)
    report = analyze(prefix, variants, old_paths, parents, top3, pool, 2)
    (loop.OUT / 'pilot31.results.json').write_text(json.dumps(report, indent=2, allow_nan=False) + '\n')
    selected = report['selected_for_confirmation']
    result = None
    if selected:
        chosen = {n: variants[n] for n in selected}
        chosen_old = {parents[n]: old_paths[parents[n]] for n in selected}
        expanded = dict(pool, **{n: s['path'] for n, s in panel['confirm_extra'].items()})
        prefix = loop.run('confirm31', dict(chosen, **chosen_old, top3=top3), 1082000, 32, expanded)
        result = analyze(prefix, chosen, chosen_old, parents, top3, expanded, 0)
        for name in chosen:
            row = result['results'][name]
            row['registered_submission_gate'] = submission_gate(row)
            if row['registered_submission_gate']:
                row['status'] = 'REAL_WORLD_CANDIDATE_REVIEW_REQUIRED'
        (loop.OUT / 'confirm31.results.json').write_text(json.dumps(result, indent=2, allow_nan=False) + '\n')
    loop.save('thirty_one_rounds_complete', state='complete', pilot31=report, confirm31=result,
              next_action='Review queue and executed fills, physical effects, all three references and alternate hash sensitivity before a real upload. No automatic upload; continue research.')


if __name__ == '__main__':
    try:
        main()
    except BaseException as exc:
        loop.save('loop31_failed', state='failed', error=repr(exc))
        raise
