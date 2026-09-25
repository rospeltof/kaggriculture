"""Rerun quarantined confirm19 under fixed runtime, keeping its registered design."""
import contextlib
import hashlib
import io
import json
from pathlib import Path

import continuar_loop_publicos as loop


def main():
    smoke = json.loads((loop.OUT / 'runtime_fixed_smoke.validation.json').read_text())
    smoke_meta = json.loads((loop.OUT / 'runtime_fixed_smoke.meta.json').read_text())
    assert smoke['complete_coverage'] and smoke['episodes'] == 6 and smoke['noop_exact'] == 2
    assert smoke_meta['runtime']['python_hash_seed'] == '0'
    proof = json.loads((loop.OUT / 'confirm19.noop_probe.results.json').read_text())
    assert proof['games'] == 48 and proof['original_mismatches_reproduced'] == 4
    assert proof['all_six_cells_identical_states']
    old = json.loads((loop.OUT / 'confirm19.meta.json').read_text())
    assert old['state'] == 'complete' and old['completed_episodes'] == 3200
    for name, info in old['agentes'].items():
        assert hashlib.sha256(Path(info['ruta']).read_bytes()).hexdigest() == info['sha256'], name
    pilot = json.loads((loop.OUT / 'pilot19.results.json').read_text())
    assert pilot['selected_for_confirmation'] == ['wheat_both', 'wheat_front']
    chosen = {name: old['agentes'][name]['ruta'] for name in pilot['selected_for_confirmation']}
    pool = {name: info['ruta'] for name, info in old['agentes'].items() if name not in ('base', 'noop', *chosen)}
    assert len(pool) == 11 and old['seeds'] == list(range(1047000, 1047032))
    loop.BASE = old['agentes']['base']['ruta']
    prefix = loop.run('confirm19_fixedhash0', chosen, 1047000, 32, pool)
    result = loop.analyze(prefix, chosen, 0, lambda name: name, 0)
    excluded = [name for name in pool if name not in ('arshs3', 'tds', 'hybu', 'ars40')]
    for name, row in result['results'].items():
        eligible = row['delta_points'] >= 3 and min(row['opponent_breakdown'].values()) >= -20
        row['registered_submission_gate'] = eligible
        if eligible:
            row['status'] = 'REAL_WORLD_CANDIDATE'
        with contextlib.redirect_stdout(io.StringIO()):
            row['pilot_pool_only'] = loop.paired(str(prefix) + '.jsonl', 'base', name,
                ','.join(['noop', *(n for n in chosen if n != name), *excluded]))
    result['measurement_replaces'] = 'confirm19: strict noop rejected; original retained unchanged'
    result['new_independent_confirmation'] = False
    Path(str(prefix) + '.results.json').write_text(json.dumps(result, indent=2, allow_nan=False) + '\n')
    loop.save('nineteen_rounds_complete', state='complete', pilot19=pilot, confirm19=result,
              confirm19_prefix=prefix.name, quarantined_original='confirm19',
              next_action='Review mechanisms and alternate hash runtimes before upload. Continue registered20–25 with fixed runtime.')


if __name__ == '__main__':
    try:
        main()
    except BaseException as exc:
        loop.save('loop19_recovery_failed', state='failed', error=repr(exc))
        raise
