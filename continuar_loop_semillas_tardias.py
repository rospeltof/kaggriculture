"""Loop26: independently registered wheat seed policies against the close reactive panel."""
import hashlib
import json
from pathlib import Path
import time

import continuar_loop_publicos as loop
from continuar_loop_adelanto_trigo import changed_seeds
from continuar_loop_panel_cercano import analyze, verify_sources


def main():
    validation = json.loads((loop.OUT / 'late_seed_validation.json').read_text())
    candidates = json.loads((loop.OUT / 'late_seed_variants.json').read_text())
    panel = json.loads((loop.OUT / 'close_panel_manifest.json').read_text())
    assert validation['passed'] and validation['competitive_ready']
    assert validation['candidate_hashes'] == {name: spec['sha256'] for name, spec in candidates.items()}
    verify_sources(panel)
    for name, spec in candidates.items():
        assert hashlib.sha256(Path(spec['path']).read_bytes()).hexdigest() == spec['sha256'], name
    print('Loop26 seed mechanics and frozen sources verified; waiting for loop25.', flush=True)
    while True:
        try:
            state = json.loads(loop.STATE.read_text())
        except (FileNotFoundError, json.JSONDecodeError):
            state = {}
        if state.get('state') == 'failed':
            raise RuntimeError(state)
        if state.get('phase') == 'twenty_five_rounds_complete':
            break
        time.sleep(5)
    verify_sources(panel)
    for spec in candidates.values():
        assert hashlib.sha256(Path(spec['path']).read_bytes()).hexdigest() == spec['sha256']
    loop.BASE = panel['controls']['base']['path']
    control = panel['controls']['top3']['path']
    assert panel['controls']['base']['sha256'] == validation['base_hash']
    assert panel['controls']['top3']['sha256'] == validation['control_hash']
    variants = {name: spec['path'] for name, spec in candidates.items()}
    pool = {name: spec['path'] for name, spec in panel['pilot_pool'].items()}
    prefix = loop.run('pilot26', dict(variants, top3=control), 1066000, 16, pool)
    report = analyze(prefix, variants, control, 2)
    (loop.OUT / 'pilot26.results.json').write_text(json.dumps(report, indent=2, allow_nan=False) + '\n')
    selected = report['selected_for_confirmation']; result = None
    if selected:
        chosen = {name: variants[name] for name in selected}
        expanded = dict(pool, **{name: spec['path'] for name, spec in panel['confirm_extra'].items()})
        prefix = loop.run('confirm26', dict(chosen, top3=control), 1067000, 32, expanded)
        result = analyze(prefix, chosen, control, 0)
        for name in chosen:
            row = result['results'][name]
            row['changed_seeds_vs_vq'] = changed_seeds(prefix, name, 'base', chosen)
            eligible = (row['delta_points'] >= 3 and row['versus_top3']['delta_points'] >= 0
                        and min(row['opponent_breakdown'].values()) >= -20
                        and min(row['versus_top3']['opponent_breakdown'].values()) >= -20
                        and len(row['changed_seeds_vs_vq']) >= 2)
            row['registered_submission_gate'] = eligible
            if eligible:
                row['status'] = 'REAL_WORLD_CANDIDATE_REVIEW_REQUIRED'
        (loop.OUT / 'confirm26.results.json').write_text(json.dumps(result, indent=2, allow_nan=False) + '\n')
    loop.save('twenty_six_rounds_complete', state='complete', pilot26=report, confirm26=result,
              next_action='Review accepted planting/refills, physical preservation, both submitted references and alternate hash sensitivity. No automatic upload; continue research.')


if __name__ == '__main__':
    try:
        main()
    except BaseException as exc:
        loop.save('loop26_failed', state='failed', error=repr(exc))
        raise
