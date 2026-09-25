"""Verify loop25's two-reference analysis with archived games, without new games."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import tarfile
import tempfile

from continuar_loop_panel_cercano import analyze, verify_sources

OUT = Path('docs/evidencia/loop_publicos_20260925')


def main():
    manifest = json.loads((OUT / 'close_panel_manifest.json').read_text())
    verify_sources(manifest)
    source = OUT / 'pilot19'
    previous = json.loads(source.with_suffix('.results.json').read_text())
    # The archived half arm becomes a *labelled fixture control*, not real top3.
    # All three improved equally vs base: a one-reference selector would admit
    # front/both, but the second comparison must prevent selection here.
    rename = lambda name: 'top3' if name == 'wheat_half' else name
    with tempfile.TemporaryDirectory(prefix='kaggriculture-panel25-') as directory:
        prefix = Path(directory) / 'fixture'
        meta = json.loads(source.with_suffix('.meta.json').read_text())
        assert meta['state'] == 'complete'
        meta['agentes'] = {rename(name): item for name, item in meta['agentes'].items()}
        meta['vs'] = ','.join(rename(name) for name in meta['vs'].split(','))
        prefix.with_suffix('.meta.json').write_text(json.dumps(meta))
        rows = [json.loads(line) for line in source.with_suffix('.jsonl').read_text().splitlines()]
        for row in rows:
            row['a'], row['b'] = rename(row['a']), rename(row['b'])
        prefix.with_suffix('.jsonl').write_text(''.join(json.dumps(row) + '\n' for row in rows))
        with tarfile.open(source.with_suffix('.sources.tgz')) as old, tarfile.open(prefix.with_suffix('.sources.tgz'), 'w:gz') as new:
            for member in old.getmembers():
                if member.name == 'agents/wheat_half.py':
                    member.name = 'agents/top3.py'
                # TarInfo offset still points at the original payload.
                new.addfile(member, old.extractfile(member) if member.isfile() else None)
        with contextlib.redirect_stdout(io.StringIO()):
            report = analyze(prefix, dict(wheat_front='', wheat_both=''), '', 2)
        assert report['selected_for_confirmation'] == []
        for name in ('wheat_front', 'wheat_both'):
            row = report['results'][name]
            assert row['delta_points'] == previous['results'][name]['delta_points'] > 0
            assert row['versus_top3']['delta_points'] == 0
            assert row['rivals'] == row['versus_top3']['rivals'] == sorted(['arshs3', 'ars40', 'hybu', 'tds'])
        validation = json.loads(prefix.with_suffix('.validation.json').read_text())
    result = dict(
        passed=True, new_simulations=0, source_hashes_verified=True,
        archived_fixture='pilot19: wheat_half renamed only inside temporary fixture',
        fixture_episodes=validation['episodes'], fixture_noop_exact=validation['noop_exact'],
        positive_first_reference_but_tied_second_selects_nothing=True,
        same_four_rivals_in_both_comparisons=True,
        manifest_sha256=hashlib.sha256((OUT / 'close_panel_manifest.json').read_bytes()).hexdigest(),
    )
    (OUT / 'close_panel_validation.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
