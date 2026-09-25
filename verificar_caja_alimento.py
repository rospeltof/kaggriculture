"""Validate control/source identity and the observed funding mechanism."""
import gzip
import hashlib
import json
from pathlib import Path
import tarfile

OUT = Path('docs/evidencia/loop_publicos_20260925')


def main():
    plan = json.loads((OUT/'cash_smoke.plan.json').read_text())
    rows = json.loads((OUT/'cash_smoke.json').read_text())
    manifest = json.loads((OUT/'cash_variants.json').read_text())
    with tarfile.open(OUT/'cash_smoke.sources.tgz', 'r:gz') as tar:
        for name, spec in plan['agents'].items():
            assert hashlib.sha256(tar.extractfile(name+'.py').read()).hexdigest() == spec['sha256']
            assert hashlib.sha256(Path(spec['path']).read_bytes()).hexdigest() == spec['sha256']
            if name in manifest:
                assert manifest[name]['sha256'] == spec['sha256']
        for case in plan['cases']:
            assert tar.extractfile(f'opponent_{case["seed"]}.py').read() == Path(case['opponent']).read_bytes()
    keyed = {(r['arm'], r['seed'], r['seat']): r for r in rows}
    expected = {(a, c['seed'], p) for a in plan['agents'] for c in plan['cases'] for p in plan['seats']}
    assert len(rows) == len(keyed) == 42 and set(keyed) == expected
    summary = []
    for case in plan['cases']:
        seed = case['seed']
        for seat in plan['seats']:
            base = keyed['base', seed, seat]; noop = keyed['cash_noop', seed, seat]
            assert (base['action_hash'], base['rewards']) == (noop['action_hash'], noop['rewards'])
            for arm in ['legacy', *manifest]:
                row = keyed[arm, seed, seat]
                events = [json.loads(l) for l in gzip.decompress((OUT/f'cash_smoke.{seed}.{arm}.{seat}.units.jsonl.gz').read_bytes()).decode().splitlines()]
                fed = [e for e in events if e['action'] == ['FEED'] and e['fed']]
                assert all(e['inventory_delta'].get('WHEAT') == -1 for e in fed)
                assert len(fed) == row['feed_accepted']
                assert not any(v for report in row['reports'].values() for k, v in report.items() if 'error' in k and isinstance(v, (int, float)))
                private = row['terminal_private']
                assert sum(private['shed'].values()) + sum(sum(i.values()) for i in private['inventories']) == 0
                summary.append(dict(seed=seed, seat=seat, arm=arm, changed_action_turns=row['changed_action_turns'],
                                    early_swaps=row['reports'].get('_EC_REPORT', {}).get('events', []),
                                    quotes=row['reports'].get('_CF_REPORT', {}).get('quotes', []),
                                    wheat_bought_191=row['wheat_bought_191'], feed_accepted=row['feed_accepted'],
                                    same_shops=row['shops'] == base['shops'], escapes=row['escapes']))
    # Reproduce the original diagnosed failure and unchanged reference; these
    # are implementation checks, not selection by a new development outcome.
    for seat in plan['seats']:
        assert keyed['base', 1018001, seat]['wheat_bought_191'] == 7
        assert keyed['legacy', 1018001, seat]['wheat_bought_191'] == 0
        assert len(keyed['legacy', 1018001, seat]['escapes']) == 3
    report = dict(passed=True, development_games=42, noop_exact_turns=6*719,
                  candidate_hashes={n: r['sha256'] for n, r in manifest.items()},
                  legacy_hash=plan['agents']['legacy']['sha256'],
                  max_turn_ms=max(r['max_turn_ms'] for r in rows),
                  note='Development confirms implementation and describes funding/escapes; no competitive promotion from these worlds.',
                  summary=summary)
    assert report['max_turn_ms'] < 1000
    (OUT/'cash_validation.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
