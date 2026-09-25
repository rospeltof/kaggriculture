"""Recheck public refresh hashes, loader equivalence and cash before loop18."""
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import tarfile

OUT = Path('docs/evidencia/loop_publicos_20260925')
TAG = 'public_0548_smoke_v2'


def main():
    plan = json.loads((OUT/(TAG+'.plan.json')).read_text())
    rows = json.loads((OUT/(TAG+'.json')).read_text())
    manifest = json.loads((OUT/'public_0548_variants.json').read_text())
    assert plan['seeds'] == [1042000, 1042001] and plan['seats'] == [0, 1]
    assert set(manifest) == {'public_v7', 'public_hs4'}
    with tarfile.open(OUT/(TAG+'.sources.tgz'), 'r:gz') as tar:
        for name, spec in plan['agents'].items():
            assert hashlib.sha256(tar.extractfile(name+'.py').read()).hexdigest() == spec['sha256']
            assert hashlib.sha256(Path(spec['path']).read_bytes()).hexdigest() == spec['sha256']
            if name in manifest:
                assert manifest[name] == spec
    keyed = {(r['arm'], r['mode'], r['seed'], r['seat']): r for r in rows}
    expected = {(a, mode, s, p) for a in plan['agents']
                for mode in (['official', 'nominal'] if a in manifest else ['official'])
                for s in plan['seeds'] for p in plan['seats']}
    assert len(rows) == len(keyed) == 24 and set(keyed) == expected
    for row in rows:
        stem = f"{TAG}.{row['seed']}.{row['arm']}.{row['mode']}.{row['seat']}"
        ledger = [json.loads(l) for l in gzip.decompress((OUT/(stem+'.ledger.jsonl.gz')).read_bytes()).decode().splitlines()]
        for p in (0, 1):
            assert 3000 + sum(e['value'] for e in ledger if e['player'] == p) == row['rewards'][p]
        for report in row['telemetry'].values():
            assert not any(v for k, v in report.items() if 'error' in k and isinstance(v, (int, float)))
    summary = []
    for seed in plan['seeds']:
        for seat in plan['seats']:
            base = keyed['base', 'official', seed, seat]
            noop = keyed['noop', 'official', seed, seat]
            for key in ('action_hash', 'rewards', 'flows', 'shops', 'escapes', 'terminal_private'):
                assert base[key] == noop[key], ('noop', seed, seat, key)
            for arm in manifest:
                official = keyed[arm, 'official', seed, seat]
                nominal = keyed[arm, 'nominal', seed, seat]
                for key in ('action_hash', 'rewards', 'flows', 'shops', 'escapes', 'terminal_private'):
                    assert official[key] == nominal[key], (arm, seed, seat, key)
                private = official['terminal_private']
                summary.append(dict(arm=arm, seed=seed, seat=seat,
                                    entry_official=official['entry_name'], entry_nominal=nominal['entry_name'],
                                    changed_action_turns=official['changed_action_turns'],
                                    same_shops=base['shops'] == official['shops'], escapes=official['escapes'],
                                    terminal_product_units=sum(private['shed'].values()) + sum(sum(x.values()) for x in private['inventories']),
                                    terminal_seed_units=sum(private['seeds'].values()),
                                    telemetry=nominal['telemetry']))
    report = dict(passed=True, development_games=24, noop_exact_turns=4*719,
                  official_nominal_exact_turns=8*719,
                  candidate_hashes={n: s['sha256'] for n, s in manifest.items()},
                  max_turn_ms=max(r['max_turn_ms'] for r in rows), summary=summary,
                  error_scope='720 DONE and no fatal statuses asserted by run; new V7/HS4 report error counters zero. Inherited internal report counters not exhaustively collected.',
                  note='Execution/entry compatibility only; development rewards are not a selection criterion.')
    assert report['max_turn_ms'] < 1000
    (OUT/'public_0548_validation.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'summary'}, indent=2))
    return report


if __name__ == '__main__':
    main()
