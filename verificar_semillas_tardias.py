"""Verify accepted seed edits and physical preservation before loop26 can run."""
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import tarfile

from construir_semillas_tardias import BASE, OUT as AGENTS, EVIDENCE as OUT


def main():
    record = json.loads((OUT / 'late_seed_smoke.json').read_text())
    plan = record['plan']; rows = record['results']; manifest = json.loads((AGENTS / 'manifest.json').read_text())
    keys = {(r['arm'], r['seed'], r['seat']) for r in rows}
    expected = {(arm, seed, seat) for arm in plan['agents'] for seed in plan['seeds'] for seat in (0, 1)}
    assert len(rows) == len(keys) == 40 and keys == expected
    indexed = {(r['arm'], r['seed'], r['seat']): r for r in rows}
    with tarfile.open(OUT / 'late_seed_smoke.sources.tgz') as archive:
        for arm, spec in plan['agents'].items():
            assert hashlib.sha256(Path(spec['path']).read_bytes()).hexdigest() == spec['sha256']
            assert hashlib.sha256(archive.extractfile(f'agents/{arm}.py').read()).hexdigest() == spec['sha256']
    noops = 0; activation = Counter(); accepted_edits = []; summary = []
    for r in rows:
        assert r['max_turn_ms'] < 1000
        assert not any(value for report in r['reports'].values() for key, value in report.items()
                       if 'error' in key and isinstance(value, (int, float)))
        base = indexed['base', r['seed'], r['seat']]
        if r['arm'] == 'seed_noop':
            assert r['action_hash'] == base['action_hash'] and r['rewards'] == base['rewards']
            assert r['changed_action_turns'] == 0  # probe compared both players' full actions
            noops += 719
        if r['arm'] not in ('seed_kind', 'seed_jit'):
            continue
        assert r['same_unit_actions'] and r['same_shops'], (r['arm'], r['seed'], r['seat'])
        for field in ('planted', 'accepted', 'harvested', 'nights', 'escapes', 'final_composition'):
            assert r[field] == base[field], (r['arm'], r['seed'], field)
        private = r['terminal_private'][0]
        assert not any(private['shed'].values()) and not any(any(bag.values()) for bag in private['inventories'])
        ledger = [json.loads(line) for line in gzip.decompress((OUT / f'late_seed_smoke.{r["seed"]}.{r["arm"]}.{r["seat"]}.ledger.jsonl.gz').read_bytes()).decode().splitlines()]
        buys = Counter(e['step'] for e in ledger if e['player'] == r['seat'] and e['op'] == 'BUY_SEED' and e['item'] == 'WHEAT')
        for edit in r['edits']:
            before, after = edit['before'], edit['after']
            assert 624 <= edit['step'] <= 718 and len(after) <= 10
            assert len(before) <= len(after) <= len(before)+1
            for i, order in enumerate(before):
                if order and order[:2] != ['BUY_SEED', 'WHEAT']:
                    assert after[i] == order
            assert buys[edit['step']] == edit['final_qty'], (r['arm'], r['seed'], edit)
            if edit['projected_seed'] is not None:
                balance = next((x for x in r['seed_balances'] if x['step'] == edit['step']), None)
                if balance is not None:
                    actual_prebuy = balance['after'].get('WHEAT', 0)-balance['bought_wheat']
                    assert edit['projected_seed'] == actual_prebuy
            accepted_edits.append(dict(arm=r['arm'], seed=r['seed'], seat=r['seat'], step=edit['step'],
                                       original_requested=edit['original_qty'], final_requested=edit['final_qty'],
                                       actually_bought=buys[edit['step']]))
        activation[r['arm']] += bool(r['edits'])
        def wheat_cost(row):
            return next((x for x in row['cashflow'][0] if x['op'] == 'BUY_SEED' and x['item'] == 'WHEAT'), dict(units=0, cash=0))
        original, actual = wheat_cost(base), wheat_cost(r)
        assert (original['units']-actual['units']) == base['terminal_private'][0]['seeds'].get('WHEAT', 0)-private['seeds'].get('WHEAT', 0)
        assert actual['cash']-original['cash'] == 10*(original['units']-actual['units'])
        summary.append(dict(arm=r['arm'], seed=r['seed'], seat=r['seat'], changed_turns=len(r['edits']),
                            bought_before=original['units'], bought_after=actual['units'],
                            seed_cost_saved=actual['cash']-original['cash'], planted=r['planted'],
                            terminal_wheat_seeds=private['seeds'].get('WHEAT', 0),
                            base_margin=base['margin'], candidate_margin=r['margin']))
    assert noops == 5752 and all(activation[name] > 0 for name in ('seed_kind', 'seed_jit'))
    assert any(x['arm'] == 'seed_jit' and x['original_requested'] == 0 and x['actually_bought'] > 0 for x in accepted_edits), 'No replacement purchase tested'
    validation = dict(passed=True, competitive_ready=True, games=40, noop_exact_turns=noops,
                      max_turn_ms=max(r['max_turn_ms'] for r in rows), activation=dict(activation),
                      candidate_hashes={n: r['sha256'] for n, r in manifest.items() if r['config'].get('enabled')},
                      base_hash=hashlib.sha256(BASE.read_bytes()).hexdigest(), control_hash=manifest['top3']['sha256'],
                      edits_checked=len(accepted_edits), note='All declared seed edits accepted; exact own unit actions, planting, feed/care/harvest, shops, losses and escapes preserved in development. No claim of global invariance or WLT gain.',
                      summary=summary)
    (OUT / 'late_seed_execution.json').write_text(json.dumps(accepted_edits, indent=2) + '\n')
    (OUT / 'late_seed_validation.json').write_text(json.dumps(validation, indent=2) + '\n')
    print(json.dumps({k: v for k, v in validation.items() if k != 'summary'}))


if __name__ == '__main__':
    main()
