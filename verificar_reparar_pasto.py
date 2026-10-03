"""Check loop33 against official construction, animal inventory and care transitions."""
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import tarfile

from construir_reparar_pasto import OUT as AGENTS, EVIDENCE as OUT


def main():
    data = json.loads((OUT / 'animal_build_smoke.json').read_text())
    rows, plan = data['results'], data['plan']
    manifest = json.loads((AGENTS / 'manifest.json').read_text())
    keyed = {(r['arm'], r['seed'], r['seat']): r for r in rows}
    expected = {(name, seed, seat) for name in plan['agents'] for seed in plan['seeds'] for seat in (0, 1)}
    assert len(rows) == len(keyed) == 36 and set(keyed) == expected
    with tarfile.open(OUT / 'animal_build_smoke.sources.tgz') as archive:
        for name, spec in plan['agents'].items():
            assert hashlib.sha256(Path(spec['path']).read_bytes()).hexdigest() == spec['sha256']
            assert hashlib.sha256(archive.extractfile(f'agents/{name}.py').read()).hexdigest() == spec['sha256']
        assert hashlib.sha256(archive.extractfile('opponent.py').read()).hexdigest() == plan['opponent']['sha256']
    noops = 0; activation = Counter(); builds = Counter(); placements = Counter(); cares = Counter(); aborts = Counter(); summaries = []
    for row in rows:
        name, seed, seat = row['arm'], row['seed'], row['seat']
        assert row['max_turn_ms'] < 1000
        assert not any(value for report in row['reports'].values() for key, value in report.items()
                       if 'error' in key and isinstance(value, (int, float)))
        if name in ('base', 'top3'):
            continue
        spec = manifest[name]; reference = keyed[spec['behavior_reference'], seed, seat]
        if not spec['config']['enabled']:
            assert row['action_hashes'] == reference['action_hashes'] and row['rewards'] == reference['rewards']
            assert row['changed_own_turns'] == row['changed_rival_turns'] == 0 and not row['edits']
            noops += 719
            continue
        stem = f'animal_build_smoke.{seed}.{name}.{seat}'
        ledger = [json.loads(line) for line in gzip.decompress((OUT / (stem + '.ledger.jsonl.gz')).read_bytes()).splitlines()]
        units = [json.loads(line) for line in gzip.decompress((OUT / (stem + '.units.jsonl.gz')).read_bytes()).splitlines()]
        assert 3000 + sum(event['value'] for event in ledger if event['player'] == seat) == row['rewards'][seat]
        stats = row['reports']['_AB_REPORT']
        assert stats['build_requests'] == len(row['edits'])
        assert stats['place_requests'] == stats['observed_builds'] == sum(len(event['phases']) >= 2 for event in row['edits'])
        assert stats['care_requests'] == stats['observed_placements'] == sum(len(event['phases']) == 3 for event in row['edits'])
        assert stats['aborts'] == sum('aborted_at' in event for event in row['edits'])
        verified = []
        for event in row['edits']:
            step, actor, animal = event['step'], event['actor'], event['animal']
            assert step < 648 and step % 24 <= 21
            assert event['planned_next'] == [['CARE'], ['PASS']]
            assert event['phases'][0]['original'][:2] == ['PLACE', animal]
            assert event['phases'][0]['tile_before'] is None
            assert event['phases'][0]['bag_before'].get(animal, 0) >= 1
            if len(event['phases']) == 3:
                assert event['all_phases_requested'] and 'aborted_at' not in event
            else:
                assert 'aborted_at' in event
            for index, phase in enumerate(event['phases']):
                expected_command = [['BUILD_' + event['structure']], ['PLACE', animal], ['CARE']][index]
                assert phase['step'] == step+index and phase['emitted'] == expected_command
                assert (step+index)//24 == step//24
                emitted = row['emitted_edits'][str(step+index)]
                commands = [emitted.get('farmer'), *(emitted.get('hands') or [])]
                assert commands[actor] == expected_command
                executed = [unit for unit in units if unit['step'] == step+index and unit['actor'] == actor and unit['command'] == expected_command]
                assert len(executed) == 1 and executed[0]['xy'] == event['xy'] and executed[0]['accepted']
                unit = executed[0]
                if index == 0:
                    assert unit['tile_before'] is None and unit['tile_after'] == {'kind': event['structure']}
                    assert unit['bag_before'] == unit['bag_after']
                    builds[name] += 1
                elif index == 1:
                    assert not unit['tile_before'].get('animal') and unit['tile_after']['animal'] == animal
                    assert unit['tile_after']['placed_day'] == step//24 and unit['delta'].get(animal) == -1
                    placements[name] += 1
                else:
                    assert not unit['tile_before']['cared_today'] and unit['tile_after']['cared_today']
                    assert unit['tile_after']['animal'] == animal
                    cares[name] += 1
            aborts[name] += 'aborted_at' in event
            verified.append(event)
        activation[name] += row['changed_own_turns'] > 0
        summaries.append(dict(arm=name, seed=seed, seat=seat, changed_own_turns=row['changed_own_turns'],
                              same_shops=row['same_shops'], same_losses=row['nights'] == reference['nights'],
                              base_harvest=reference['harvested'], candidate_harvest=row['harvested'],
                              base_work=reference['accepted'], candidate_work=row['accepted'],
                              base_escapes=reference['escapes'], candidate_escapes=row['escapes'],
                              base_terminal_private=reference['terminal_private'], candidate_terminal_private=row['terminal_private'],
                              base_margin=reference['margin'], candidate_margin=row['margin'], repairs=verified))
    candidates = {name: spec for name, spec in manifest.items() if spec['config']['enabled']}
    assert noops == 8628 and all(activation[name] > 0 and builds[name] > 0 and placements[name] > 0 and cares[name] > 0 for name in candidates)
    result = dict(passed=True, competitive_ready=True, games=36, noop_exact_turns=noops,
                  max_turn_ms=max(row['max_turn_ms'] for row in rows), activated_cells=dict(activation),
                  builds=dict(builds), placements=dict(placements), cares=dict(cares), aborts=dict(aborts),
                  candidate_hashes={name: spec['sha256'] for name, spec in candidates.items()},
                  base_hash=plan['agents']['base']['sha256'], control_hash=plan['agents']['top3']['sha256'], summary=summaries,
                  note='Native windows and official BUILD/PLACE/CARE transitions verified. Changes to production, shops, losses, terminal inventory and scores remain diagnostic.')
    (OUT / 'animal_build_validation.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({key: value for key, value in result.items() if key != 'summary'}))


if __name__ == '__main__':
    main()
