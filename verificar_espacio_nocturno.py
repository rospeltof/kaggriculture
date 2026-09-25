"""Validate the full frozen night-stock development evidence before tournament."""
import gzip
import hashlib
import json
from pathlib import Path
import tarfile

OUT = Path('docs/evidencia/loop_publicos_20260925')
TAG = 'night_smoke_v2'


def main():
    plan = json.loads((OUT/(TAG+'.plan.json')).read_text())
    rows = json.loads((OUT/(TAG+'.json')).read_text())
    manifest = json.loads((OUT/'night_variants.json').read_text())
    with tarfile.open(OUT/(TAG+'.sources.tgz'), 'r:gz') as tar:
        for name, spec in plan['agents'].items():
            assert hashlib.sha256(tar.extractfile(name+'.py').read()).hexdigest() == spec['sha256']
            assert hashlib.sha256(Path(spec['path']).read_bytes()).hexdigest() == spec['sha256']
            if name in manifest:
                assert manifest[name]['sha256'] == spec['sha256']
    keyed = {(r['arm'], r['seed'], r['seat']): r for r in rows}
    expected = {(a, s, p) for a in plan['agents'] for s in plan['seeds'] for p in plan['seats']}
    assert len(rows) == len(keyed) == 36 and set(keyed) == expected
    summary = []
    predictions = 0
    for seed in plan['seeds']:
        for seat in plan['seats']:
            base = keyed['base', seed, seat]
            noop = keyed['night_noop', seed, seat]
            assert (base['action_hash'], base['rewards']) == (noop['action_hash'], noop['rewards'])
            base_unfed = [(r['step'], r['unfed']) for r in base['nights']]
            for arm in manifest:
                row = keyed[arm, seed, seat]
                assert len(row['predictions']) == len(row['prediction_validation'])
                assert all(r['final_matches'] and r['loss_matches'] for r in row['prediction_validation'])
                assert row['reports']['_NF_REPORT']['nf_errors'] == 0
                assert row['reports']['_V92_P_REPORT']['pred_errors'] == row['reports']['_VQ_REPORT']['errors'] == 0
                predictions += len(row['predictions'])
                private = row['terminal_private']
                assert sum(private['shed'].values()) + sum(sum(i.values()) for i in private['inventories']) == 0
                ledger = [json.loads(l) for l in gzip.decompress((OUT/f'{TAG}.{seed}.{arm}.{seat}.ledger.jsonl.gz').read_bytes()).decode().splitlines()]
                for event in row['predictions']:
                    for item, quantity in event['sold'].items():
                        accepted = sum(r['player'] == seat and r['step'] == event['step'] and r['op'] == 'SELL' and r['item'] == item for r in ledger)
                        assert accepted >= quantity
                summary.append(dict(seed=seed, seat=seat, arm=arm, activations=len(row['predictions']),
                                    lost_base=base['lost'], lost_candidate=row['lost'],
                                    changed_action_turns=row['changed_action_turns'],
                                    unfed_matches_base=base_unfed == [(r['step'], r['unfed']) for r in row['nights']],
                                    escapes=row['escapes'], same_shops=row['shops'] == base['shops']))
    assert predictions > 0
    report = dict(passed=True, development_games=36, noop_exact_turns=6*719,
                  source_archive=TAG+'.sources.tgz', candidate_hashes={n: r['sha256'] for n, r in manifest.items()},
                  predictions_validated=predictions, max_turn_ms=max(r['max_turn_ms'] for r in rows),
                  note='Mechanism validation, not competitive selection. Unfed and escapes are retained for comparison; a reserve is not a universal proof.',
                  summary=summary)
    assert report['max_turn_ms'] < 1000
    (OUT/'night_validation.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
