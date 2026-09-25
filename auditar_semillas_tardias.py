"""Account for seeds and atomic PLANT reserves in 18 already reproduced replays."""
from collections import Counter
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path

OUT = Path('docs/evidencia/loop_publicos_20260925')
COST = dict(WHEAT=10, CARROT=20, TOMATO=50, STRAWBERRY=100, MELON=80)


def main():
    target = OUT / 'late_seed_audit.json'; assert not target.exists()
    inputs = []
    old = json.loads((OUT / 'forecast_pair_replays_0653.json').read_text())
    for row in old['episodes']:
        policy = row['real_policy']; actual = row['runs'][policy]
        inputs.append(dict(episode=row['episode'], policy=policy, seat=row['seat'], path=row['replay'],
                           replay_sha256=row['replay_sha256'], ledger=actual['ledger']))
    for suffix in ('0742', '0828'):
        audit = json.loads((OUT / f'feedback_{suffix}.audit.json').read_text())
        receipts = {r['id']: r for r in json.loads((OUT / f'feedback_{suffix}.fetch.json').read_text())}
        for row in audit['results']:
            assert row['own_actions_exact'] == 719 and row['states_exact'] == 720
            inputs.append(dict(episode=row['episode'], policy=row['policy'], seat=row['seat'], path=receipts[row['episode']]['path'],
                               replay_sha256=row['replay_sha256'], ledger=str(OUT / f'feedback_{suffix}.{row["episode"]}.ledger.jsonl.gz')))
    assert len(inputs) == len({r['episode'] for r in inputs}) == 18
    plan = dict(created_at=datetime.now(timezone.utc).isoformat(), inputs=inputs, late_from=624,
                rule='All18 already recency-selected source controls, no outcome filter. Seed accounting from accepted market ledger and consecutive observations. Frozen-command removal diagnostic only; not a deployable policy or causal profit estimate.')
    (OUT / 'late_seed_audit.plan.json').write_text(json.dumps(plan, indent=2) + '\n')
    results = []
    for item in inputs:
        raw = Path(item['path']).read_bytes(); assert hashlib.sha256(raw).hexdigest() == item['replay_sha256']
        replay = json.loads(raw); seat = item['seat']; steps = replay['steps']; assert len(steps) == 720
        ledger = [json.loads(line) for line in gzip.decompress(Path(item['ledger']).read_bytes()).decode().splitlines()]
        buys = Counter((e['step'], e['item']) for e in ledger if e['player'] == seat and e['op'] == 'BUY_SEED')
        events = []; total_used = Counter()
        for step in range(719):
            before = steps[step][seat]['observation']['private']['seeds']
            after = steps[step+1][seat]['observation']['private']['seeds']
            action = steps[step+1][seat]['action']
            requested = Counter(c[1] for c in [action.get('farmer') or ['PASS'], *(action.get('hands') or [])]
                                if len(c) >= 2 and c[0] == 'PLANT')
            used = {crop: int(before.get(crop, 0)) + buys[step, crop] - int(after.get(crop, 0)) for crop in COST}
            assert all(0 <= used[crop] <= requested[crop] for crop in COST), (item['episode'], step)
            total_used.update(used)
            events.append(dict(step=step, before=before, after=after, requested=dict(requested), used=used,
                               bought={crop: buys[step, crop] for crop in COST}))
        final = steps[-1][seat]['observation']['private']['seeds']
        initial = steps[0][seat]['observation']['private']['seeds']
        crops = {}
        for crop in COST:
            total_bought = sum(buys[step, crop] for step in range(719))
            assert int(initial.get(crop, 0)) + total_bought - total_used[crop] == int(final.get(crop, 0))
            late_bought = sum(buys[step, crop] for step in range(624, 719))
            possible = min(int(final.get(crop, 0)), late_bought)
            accepted = None
            for amount in range(possible, -1, -1):
                cut = {}; left = amount
                for step in range(718, 623, -1):
                    n = min(left, buys[step, crop]); cut[step] = n; left -= n
                assert left == 0
                balance = int(initial.get(crop, 0)); good = True
                for event in events:
                    # Atomic validation counts even PLANTs that target occupied tiles.
                    if event['used'][crop] and balance < event['requested'].get(crop, 0):
                        good = False; break
                    balance += event['bought'][crop] - cut.get(event['step'], 0) - event['used'][crop]
                    if balance < 0:
                        good = False; break
                if good:
                    accepted = dict(units=amount, nominal_cost=amount*COST[crop], cuts={str(t): n for t, n in cut.items() if n})
                    break
            assert accepted is not None
            crops[crop] = dict(bought=total_bought, planted=total_used[crop], terminal=int(final.get(crop, 0)),
                               late_bought=late_bought, frozen_command_removal=accepted,
                               last_purchase=max((t for t in range(719) if buys[t, crop]), default=None),
                               last_consumption=max((e['step'] for e in events if e['used'][crop]), default=None))
        result = dict(**item, seed=replay['info']['seed'], opponent=replay['info']['TeamNames'][1-seat], crops=crops,
                      late_events=[e for e in events if e['step'] >= 624 and (any(e['bought'].values()) or any(e['requested'].values()))])
        results.append(result)
        print(json.dumps(dict(episode=item['episode'], policy=item['policy'], wheat=crops['WHEAT'], carrot=crops['CARROT'])), flush=True)
    target.write_text(json.dumps(dict(plan=plan, results=results), indent=2) + '\n')


if __name__ == '__main__':
    main()
