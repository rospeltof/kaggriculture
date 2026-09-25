"""Validate sources, controls and actual grain consumption before feed tournament."""
import gzip
import hashlib
import json
from pathlib import Path
import tarfile

OUT = Path('docs/evidencia/loop_publicos_20260925')


def main():
    plan = json.loads((OUT/'feed_smoke.plan.json').read_text())
    rows = json.loads((OUT/'feed_smoke.json').read_text())
    manifest = json.loads((OUT/'feed_variants.json').read_text())
    with tarfile.open(OUT/'feed_smoke.sources.tgz', 'r:gz') as tar:
        for name, spec in plan['agents'].items():
            assert hashlib.sha256(tar.extractfile(name+'.py').read()).hexdigest() == spec['sha256']
            assert hashlib.sha256(Path(spec['path']).read_bytes()).hexdigest() == spec['sha256']
            if name in manifest:
                assert manifest[name]['sha256'] == spec['sha256']
    keyed = {(r['arm'], r['seed'], r['seat']): r for r in rows}
    expected = {(a, s, p) for a in plan['agents'] for s in plan['seeds'] for p in plan['seats']}
    assert len(rows) == len(keyed) == 36 and set(keyed) == expected
    summary = []
    for seed in plan['seeds']:
        for seat in plan['seats']:
            base = keyed['base', seed, seat]; noop = keyed['feed_noop', seed, seat]
            assert (base['action_hash'], base['rewards']) == (noop['action_hash'], noop['rewards'])
            for arm in manifest:
                row = keyed[arm, seed, seat]
                events = [json.loads(l) for l in gzip.decompress((OUT/f'feed_smoke.{seed}.{arm}.{seat}.units.jsonl.gz').read_bytes()).decode().splitlines()]
                fed = [e for e in events if e['action'] == ['FEED'] and e['successful']]
                assert all(e['inventory_delta'].get('WHEAT') == -1 for e in fed)
                assert len(fed) == sum(q for k, q in row['successful'].items() if k.startswith('FEED:'))
                assert not any(v for report in row['reports'].values() for k, v in report.items() if 'error' in k and isinstance(v, (int, float)))
                private = row['terminal_private']
                assert sum(private['shed'].values()) + sum(sum(i.values()) for i in private['inventories']) == 0
                summary.append(dict(seed=seed, seat=seat, arm=arm, changed_action_turns=row['changed_action_turns'],
                                    feed_skips=row['reports']['_R85_REPORT']['feed_skips'],
                                    feed_base={k: v for k, v in base['successful'].items() if k.startswith('FEED:')},
                                    feed_candidate={k: v for k, v in row['successful'].items() if k.startswith('FEED:')},
                                    harvested_base=base['harvested'], harvested_candidate=row['harvested'],
                                    same_shops=row['shops'] == base['shops'], escapes=row['escapes'],
                                    losses_base=base['losses'], losses_candidate=row['losses']))
    report = dict(passed=True, development_games=36, noop_exact_turns=6*719,
                  source_archive='feed_smoke.sources.tgz', candidate_hashes={n: r['sha256'] for n, r in manifest.items()},
                  max_turn_ms=max(r['max_turn_ms'] for r in rows),
                  note='Actual FEED consumes one WHEAT; these development games validate implementation, not competitive benefit.',
                  summary=summary)
    assert report['max_turn_ms'] < 1000
    (OUT/'feed_validation.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
