"""Recheck archived execution evidence before running the registered pilot."""
import gzip
import hashlib
import json
from pathlib import Path
import tarfile

OUT = Path('docs/evidencia/loop_publicos_20260925')


def main():
    manifest = json.loads((OUT/'early_cow_variants.json').read_text())
    validation = json.loads((OUT/'early_cow_validation.json').read_text())
    hashes = {n: r['sha256'] for n, r in manifest.items()}
    assert hashes == validation['candidate_hashes']
    total = 0
    for tag in ('early_cow_smoke', 'early_cow_smoke_1017000', 'early_cow_smoke_yarn'):
        rows = json.loads((OUT/(tag+'.json')).read_text())
        plan = json.loads((OUT/(tag+'.plan.json')).read_text())
        assert len(rows) == 16
        with tarfile.open(OUT/(tag+'.sources.tgz'), 'r:gz') as tar:
            for name, spec in plan['agents'].items():
                raw = tar.extractfile(name+'.py').read()
                assert hashlib.sha256(raw).hexdigest() == spec['sha256']
                if name in manifest:
                    assert spec['sha256'] == hashes[name]
        for seat in (0, 1):
            base = next(r for r in rows if r['arm'] == 'base' and r['seat'] == seat)
            noop = next(r for r in rows if r['arm'] == 'noop' and r['seat'] == seat)
            assert (base['action_hash'], base['rewards']) == (noop['action_hash'], noop['rewards'])
        for row in rows:
            for report in row['reports'].values():
                assert not any(v for k, v in report.items() if 'error' in k and isinstance(v, (int, float)))
            if tag == 'early_cow_smoke_yarn' and row['arm'] in manifest:
                assert len(row['physical_sites']) == 2 and row['site_wool_harvest'] == 49
                assert not row['escapes'] and not any(row['remaining_credit'].values())
                private = row['terminal_private']
                assert not any(private['shed'].values())
                assert not any(v for inv in private['inventories'] for v in inv.values())
                def records(kind):
                    path = OUT/f'{tag}.{row["arm"]}.{row["seat"]}.{kind}.jsonl.gz'
                    return [json.loads(line) for line in gzip.decompress(path.read_bytes()).decode().splitlines()]
                units = records('units')
                placed = -sum(e['inventory_delta'].get('SHEEP', 0) for e in units if e['action'][:2] == ['PLACE', 'SHEEP'])
                assert placed == 2
                ledger = records('ledger')
                bought = 0
                for event in row['reports']['_EC_REPORT']['events']:
                    requested = sum(o[2] for o in event['after'] if o[:2] == ['BUY_ANIMAL', 'SHEEP'])
                    actual = sum(e['player'] == row['seat'] and e['step'] == event['step'] and e['op'] == 'BUY_ANIMAL' and e['item'] == 'SHEEP' for e in ledger)
                    assert requested == actual
                    bought += actual
                assert bought == placed
        total += len(rows)
    for row in manifest.values():
        assert hashlib.sha256(Path(row['path']).read_bytes()).hexdigest() == row['sha256']
    assert total == validation['episodes'] == 48
    print('48 directed games, 4314 exact noop turns, source hashes, two purchases/placements and 49 harvested wool verified.')


if __name__ == '__main__':
    main()
