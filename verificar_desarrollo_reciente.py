"""Recheck frozen development evidence for the library and opening experiments."""
import hashlib
import json
from pathlib import Path
import tarfile

OUT = Path('docs/evidencia/loop_publicos_20260925')


def check_sources(tag, manifest):
    plan = json.loads((OUT/(tag+'.plan.json')).read_text())
    with tarfile.open(OUT/(tag+'.sources.tgz'), 'r:gz') as tar:
        for name, spec in plan['agents'].items():
            assert hashlib.sha256(tar.extractfile(name+'.py').read()).hexdigest() == spec['sha256']
            if name in manifest:
                assert manifest[name]['sha256'] == spec['sha256']
    for spec in manifest.values():
        assert hashlib.sha256(Path(spec['path']).read_bytes()).hexdigest() == spec['sha256']
    return plan


def main():
    for family, count, noop in (('library', 20, 'library_noop'), ('opening', 12, 'open_noop')):
        manifest = json.loads((OUT/(family+'_variants.json')).read_text())
        validation = json.loads((OUT/(family+'_validation.json')).read_text())
        plan = check_sources(family+'_smoke', manifest)
        rows = json.loads((OUT/(family+'_smoke.json')).read_text())
        seeds = plan.get('seeds', [plan.get('seed')])
        keyed = {(r['arm'], r.get('seed', plan.get('seed')), r['seat']): r for r in rows}
        expected = {(arm, seed, seat) for arm in plan['agents'] for seed in seeds for seat in plan['seats']}
        assert set(keyed) == expected and len(rows) == len(keyed) == count
        for seed in seeds:
            for seat in plan['seats']:
                base, control = keyed['base', seed, seat], keyed[noop, seed, seat]
                assert (base['action_hash'], base['rewards']) == (control['action_hash'], control['rewards'])
                if family == 'library' and seed == 1004000:
                    for arm in manifest:
                        other = keyed[arm, seed, seat]
                        assert (other['action_hash'], other['rewards']) == (base['action_hash'], base['rewards'])
                if family == 'opening':
                    tomato = keyed['open_tomato', seed, seat]
                    assert sum(e['item'] == 'COW' for e in tomato['initial_animal_buys']) == 1
                    assert sum(e['inventory_delta'].get('TOMATO', 0) for e in tomato['watched_harvests']) == tomato['sales']['TOMATO'][0] == 4
        assert validation['candidate_hashes'] == {n: r['sha256'] for n, r in manifest.items()}
        assert validation['max_turn_ms'] == max(r['max_turn_ms'] for r in rows) < 1000
        print(family, count, 'games, complete coverage, exact controls and frozen sources verified')


if __name__ == '__main__':
    main()
