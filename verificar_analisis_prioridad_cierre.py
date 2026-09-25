"""Archived fixture and gate edge cases for loop31; never launches games."""
import contextlib
from copy import deepcopy
import hashlib
import io
import json
from pathlib import Path
import tarfile
import tempfile

from continuar_loop_prioridad_cierre import analyze, choose, submission_gate

OUT = Path('docs/evidencia/loop_publicos_20260925')


def main():
    source = OUT / 'pilot20'
    rename = lambda name: {'town20': 'top3', 'town50': 'old_town50', 'town80': 'candidate'}.get(name, name)
    # Relabel only an archived fixture. These labels do not make its policies
    # the real VQ/top3/queue policies of loop31.
    with tempfile.TemporaryDirectory(prefix='kaggriculture-close-queue-') as directory:
        prefix = Path(directory) / 'fixture'
        meta = json.loads(source.with_suffix('.meta.json').read_text())
        assert meta['state'] == 'complete'
        meta['agentes'] = {rename(n): s for n, s in meta['agentes'].items()}
        meta['vs'] = ','.join(rename(n) for n in meta['vs'].split(','))
        prefix.with_suffix('.meta.json').write_text(json.dumps(meta))
        rows = [json.loads(line) for line in source.with_suffix('.jsonl').read_text().splitlines()]
        for row in rows:
            row['a'], row['b'] = rename(row['a']), rename(row['b'])
        prefix.with_suffix('.jsonl').write_text(''.join(json.dumps(row) + '\n' for row in rows))
        with tarfile.open(source.with_suffix('.sources.tgz')) as old, tarfile.open(prefix.with_suffix('.sources.tgz'), 'w:gz') as new:
            for member in old.getmembers():
                if member.name.startswith('agents/'):
                    member.name = 'agents/' + rename(Path(member.name).stem) + '.py'
                new.addfile(member, old.extractfile(member) if member.isfile() else None)
        pool = sorted(set(meta['agentes']) - set(meta['vs'].split(',')))
        with contextlib.redirect_stdout(io.StringIO()):
            report = analyze(prefix, {'candidate': ''}, {'old_town50': ''},
                             {'candidate': 'old_town50'}, '', pool, 2)
        result = report['results']['candidate']
        assert report['selected_for_confirmation'] == []
        assert report['results']['old_town50']['status'] == 'DIAGNOSTIC_CONTROL_ONLY'
        assert result['delta_points'] == 3.125
        assert result['versus_top3']['delta_points'] == result['versus_town50']['delta_points'] == 0
        assert result['rivals'] == result['versus_top3']['rivals'] == result['versus_town50']['rivals'] == pool
        keyed = {(r['a'], r['b'], r['seed'], r['seat']): r for r in rows}
        deltas = [100 * (r['score'] - keyed['old_town50', r['b'], r['seed'], r['seat']]['score'])
                  for r in rows if r['a'] == 'candidate' and r['b'] in pool]
        assert sum(deltas)/len(deltas) == result['versus_town50']['delta_points']
        expected_changed = sorted({r['seed'] for r in rows if r['a'] == 'candidate' and r['b'] in pool
                                   and r['action_hashes'][r['seat']] != keyed['old_town50', r['b'], r['seed'], r['seat']]['action_hashes'][r['seat']]})
        assert result['changed_seeds_vs_town50'] == expected_changed
        validation = json.loads(prefix.with_suffix('.validation.json').read_text())

    def sample(a, b, c):
        return dict(delta_points=a, opponent_breakdown={'a': 0}, changed_seeds_vs_town50=[1, 2],
                    versus_top3=dict(delta_points=b, opponent_breakdown={'a': 0}),
                    versus_town50=dict(delta_points=c, opponent_breakdown={'a': 0}))
    edge = dict(good=sample(5, 4, 0), weaker_old=sample(10, 9, -1), tied_top3=sample(12, 0, 3),
                lesser=sample(4, 3, 0), old_control=sample(100, 100, 100))
    names = ['good', 'weaker_old', 'tied_top3', 'lesser']
    assert choose(edge, names, 2) == ['good', 'lesser']
    assert choose(edge, names, 0) == []
    assert submission_gate(edge['good']) and not submission_gate(edge['weaker_old'])
    low = sample(2.99, 10, 10)
    assert not submission_gate(low)
    for ref in ('base', 'top3', 'town50'):
        row = sample(4, 0, 0)
        part = row if ref == 'base' else row['versus_' + ref]
        part['opponent_breakdown']['a'] = -20.01
        assert not submission_gate(row)
    row = sample(4, 0, 0)
    row['changed_seeds_vs_town50'] = [1]
    assert not submission_gate(row)
    summary = dict(passed=True, new_simulations=0, fixture='pilot20 relabelled only in a temporary copy',
                   fixture_episodes=validation['episodes'], fixture_noop_exact=validation['noop_exact'],
                   all_three_comparisons_exclude_controls=True, old_control_never_eligible=True,
                   manual_third_reference_and_changed_seeds_verified=True, gate_edges_passed=True,
                   analysis_source_sha256=hashlib.sha256(Path('continuar_loop_prioridad_cierre.py').read_bytes()).hexdigest())
    (OUT / 'close_queue_analysis_validation.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
