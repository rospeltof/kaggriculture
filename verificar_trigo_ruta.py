"""Validate loop32 physical projected stock, market fills and next native pickups."""
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import tarfile

from construir_trigo_ruta import OUT as AGENTS, EVIDENCE as OUT


def main():
    data = json.loads((OUT / 'route_wheat_smoke.json').read_text())
    rows, plan = data['results'], data['plan']
    manifest = json.loads((AGENTS / 'manifest.json').read_text())
    keyed = {(r['arm'], r['seed'], r['seat']): r for r in rows}
    expected = {(name, seed, seat) for name in plan['agents'] for seed in plan['seeds'] for seat in (0, 1)}
    assert len(rows) == len(keyed) == 36 and set(keyed) == expected
    with tarfile.open(OUT / 'route_wheat_smoke.sources.tgz') as archive:
        for name, spec in plan['agents'].items():
            assert hashlib.sha256(Path(spec['path']).read_bytes()).hexdigest() == spec['sha256']
            assert hashlib.sha256(archive.extractfile(f'agents/{name}.py').read()).hexdigest() == spec['sha256']
        assert hashlib.sha256(archive.extractfile('opponent.py').read()).hexdigest() == plan['opponent']['sha256']
    noops = 0; activation = Counter(); bought = Counter(); operations = Counter(); pickups_total = Counter(); summaries = []
    for row in rows:
        name, seed, seat = row['arm'], row['seed'], row['seat']
        assert row['max_turn_ms'] < 1000
        assert not any(value for report in row['reports'].values() for key, value in report.items()
                       if 'error' in key and isinstance(value, (int, float)))
        if name in ('base', 'top3'):
            continue
        spec = manifest[name]
        reference = keyed[spec['behavior_reference'], seed, seat]
        if not spec['config']['enabled']:
            assert row['action_hashes'] == reference['action_hashes'] and row['rewards'] == reference['rewards']
            assert row['changed_own_turns'] == row['changed_rival_turns'] == 0 and not row['edits']
            noops += 719
            continue
        stem = f'route_wheat_smoke.{seed}.{name}.{seat}'
        ledger = [json.loads(line) for line in gzip.decompress((OUT / (stem + '.ledger.jsonl.gz')).read_bytes()).splitlines()]
        units = [json.loads(line) for line in gzip.decompress((OUT / (stem + '.units.jsonl.gz')).read_bytes()).splitlines()]
        own = [event for event in ledger if event['player'] == seat]
        assert 3000 + sum(event['value'] for event in own) == row['rewards'][seat]
        stats = row['reports']['_RW_REPORT']
        assert stats['changes'] == len(row['edits'])
        assert stats['requested_units'] == sum(event['purchased'] for event in row['edits'])
        verified = []
        for event in row['edits']:
            step = event['step']; original = event['original']; proposed = event['modified']
            assert 648 <= step <= 694 and step % 24 != 23 and len(proposed) <= 10
            assert any(order[:2] == ['SELL', 'WHEAT'] for order in original)
            assert not any(order[:2] == ['BUY_PRODUCT', 'WHEAT'] for order in original)
            assert event['need'] == sum(pickup['quantity'] for pickup in event['pickups'])
            assert event['need'] > event['predicted_before']
            assert event['observed_next_step'] == step+1
            assert event['observed_next_wheat'] == event['predicted_after'] >= event['need']
            assert event['held_after_units'] == event['projected_shed'].get('WHEAT', 0)
            assert event['purchased'] == max(0, event['need']-event['held_after_units'])
            unaffected = lambda orders: [order for order in orders if order[:2] not in (['SELL', 'WHEAT'], ['BUY_PRODUCT', 'WHEAT'])]
            assert unaffected(original) == unaffected(proposed)
            emitted = row['emitted_edits'][str(step)]
            assert emitted.get('market') == proposed
            assert [emitted.get('farmer'), *(emitted.get('hands') or [])] == event['units']
            paid = [entry for entry in own if entry['step'] == step and entry['op'] == 'BUY_PRODUCT' and entry['item'] == 'WHEAT']
            sold = [entry for entry in own if entry['step'] == step and entry['op'] == 'SELL' and entry['item'] == 'WHEAT']
            assert len(paid) == event['purchased']
            assert event['held_after_units'] + len(paid) - len(sold) == event['observed_next_wheat']
            if event['purchased']:
                assert proposed[0] == ['BUY_PRODUCT', 'WHEAT', event['purchased']]
                assert event['purchased'] <= 100-sum(event['projected_shed'].values())
                assert not sold
            picked = []
            for pickup in event['pickups']:
                actor = pickup['actor']; command = pickup['command']
                assert pickup['quantity'] == (int(command[2]) if len(command) > 2 else 1)
                assert event['next_emitted_units'][actor] == command
                executed = [u for u in units if u['step'] == step+1 and u['actor'] == actor and u['command'] == command]
                assert len(executed) == 1 and executed[0]['delta'].get('WHEAT', 0) == pickup['quantity']
                picked.append(dict(actor=actor, requested=pickup['quantity'], actual=executed[0]['delta']['WHEAT']))
            bought[name] += len(paid); pickups_total[name] += sum(item['actual'] for item in picked)
            verified.append(dict(step=step, bought=len(paid), sold=len(sold), held_after_units=event['held_after_units'],
                                 need=event['need'], next_pickups=picked))
        activation[name] += row['changed_own_turns'] > 0
        operations[name] += len(verified)
        summaries.append(dict(arm=name, seed=seed, seat=seat, changed_own_turns=row['changed_own_turns'],
                              same_shops=row['same_shops'], same_work=row['accepted'] == reference['accepted'],
                              base_harvest=reference['harvested'], candidate_harvest=row['harvested'],
                              base_work=reference['accepted'], candidate_work=row['accepted'],
                              same_losses=row['nights'] == reference['nights'],
                              base_escapes=reference['escapes'], candidate_escapes=row['escapes'],
                              base_margin=reference['margin'], candidate_margin=row['margin'], operations=verified))
    candidates = {name: spec for name, spec in manifest.items() if spec['config']['enabled']}
    assert noops == 8628 and all(activation[name] > 0 and operations[name] > 0 for name in candidates)
    result = dict(passed=True, competitive_ready=True, games=36, noop_exact_turns=noops,
                  max_turn_ms=max(row['max_turn_ms'] for row in rows), activated_cells=dict(activation),
                  operations=dict(operations), bought=dict(bought), next_pickup_units=dict(pickups_total),
                  candidate_hashes={name: spec['sha256'] for name, spec in candidates.items()},
                  base_hash=plan['agents']['base']['sha256'], control_hash=plan['agents']['top3']['sha256'], summary=summaries,
                  note='Emitted stock protection, full fills and next actual pickups verified. Work, production, escapes and margins are diagnostics, not selection criteria.')
    (OUT / 'route_wheat_validation.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({key: value for key, value in result.items() if key != 'summary'}))


if __name__ == '__main__':
    main()
