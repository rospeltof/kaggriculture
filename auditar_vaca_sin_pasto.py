"""Offline evidence chain for the unplaced cow in preregistered feedback1050."""
import hashlib
import json
from pathlib import Path

OUT = Path('docs/evidencia/loop_publicos_20260925')


def main():
    receipt = next(row for row in json.loads((OUT / 'feedback_1050.fetch.json').read_text()) if row['id'] == 113252591)
    raw = Path(receipt['path']).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == receipt['sha256']
    replay = json.loads(raw)
    seat = replay['info']['TeamNames'].index('Rospel')
    events = []
    for step in (23, 24, 33, 34, 51, 65, 66, 69, 70, 71, 72, 718):
        for player in (seat, 1-seat):
            obs = replay['steps'][step][player]['observation']
            farm = obs['farms'][player]
            action = replay['steps'][step+1][player]['action']
            events.append(dict(step=step, player=player, own=player == seat, tile=farm['tiles'][2][4],
                               positions=[farm['farmer'], *farm['hands']], private=obs['private'], action=action))
    row = {(event['step'], event['player']): event for event in events}
    assert row[24, seat]['tile'] == {'kind': 'WEED'} and row[24, 1-seat]['tile'] is None
    assert row[33, seat]['action']['hands'][1] == ['DIG']
    assert row[33, 1-seat]['action']['hands'][1] == ['BUILD_PASTURE']
    assert row[34, seat]['tile'] is None and row[34, 1-seat]['tile'] == {'kind': 'PASTURE'}
    for player in (seat, 1-seat):
        assert row[69, player]['action']['farmer'] == ['PLACE', 'COW']
        assert row[69, player]['positions'][0] == [4, 2]
        assert row[69, player]['private']['inventories'][0]['COW'] == 1
    assert row[70, seat]['tile'] is None and row[70, 1-seat]['tile']['animal'] == 'COW'
    assert row[72, seat]['private']['shed']['COW'] == 1
    assert replay['steps'][-1][seat]['observation']['private']['shed']['COW'] == 1
    summary = dict(passed=True, new_simulations=0, episode=receipt['id'], seed=replay['info']['seed'], seat=seat,
                   replay_sha256=receipt['sha256'], events=events,
                   explanation='Own weed at24 replaces native BUILD_PASTURE33 with DIG; worker leaves34 without rebuilding. PLACE_COW69 still emitted on empty terrain and fails. The cow returns to shed72 and remains at the end. Opponent has no weed there and places the same purchase. This is a verified execution chain, not isolated attribution of the full4616 margin deficit or a tested repair.')
    (OUT / 'feedback_1050.unplaced_cow.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps({key: value for key, value in summary.items() if key != 'events'}))


if __name__ == '__main__':
    main()
