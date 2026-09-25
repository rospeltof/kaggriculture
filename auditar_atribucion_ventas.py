"""Audit inferred rival sales against real receipts, without modifying either policy."""
import argparse
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path

from auditar_feedback_real import OUT, SOURCES
from investigar_lider import compact_state
from sonda_fallo_forecast import run


def main(suffix):
    prefix = OUT / f'feedback_{suffix}.attribution'
    target = Path(str(prefix) + '.json')
    plan_path = Path(str(prefix) + '.plan.json')
    assert not target.exists() and not plan_path.exists()
    controls = json.loads((OUT / f'feedback_{suffix}.audit.json').read_text())['results']
    receipts = {r['id']: r for r in json.loads((OUT / f'feedback_{suffix}.fetch.json').read_text())}
    plan = dict(created_at=datetime.now(timezone.utc).isoformat(),
                rule='Every original policy and recorded opponent in this recency sample, no outcome filter. Inspect internal own-sale snapshot, final action and accepted market inventory increments; no policy edits or candidate selection.',
                episodes=[r['episode'] for r in controls],
                sources={name: dict(path=p, sha256=hashlib.sha256(Path(p).read_bytes()).hexdigest()) for name, p in SOURCES.items()})
    plan_path.write_text(json.dumps(plan, indent=2) + '\n')
    results = []
    for control in controls:
        episode = control['episode']; seat = control['seat']; receipt = receipts[episode]
        raw = Path(receipt['path']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == receipt['sha256'] == control['replay_sha256']
        replay = json.loads(raw); source = Path(SOURCES[control['policy']]); ns = {}
        assert hashlib.sha256(source.read_bytes()).hexdigest() == control['source_sha256']
        exec(compile(source.read_bytes(), str(source), 'exec'), ns)
        entry = [v for v in ns.values() if callable(v)][-1]
        snapshots = []

        def opponent(obs):
            return deepcopy(replay['steps'][int(obs['step']) + 1][1-seat]['action'])

        def agent(obs, config=None):
            action = entry(obs, config)
            step = int(obs['step']); prev = deepcopy(ns.get('_V9_RACE', {}).get(seat, {}).get('prev'))
            assert prev is not None and prev['step'] == step
            inferred = ns.get('_V92_P', {}).get(seat, {}).get('obs', {})
            forecasts = ns.get('_V92_P', {}).get(seat, {}).get('best', [])
            items = ns['_V92_P_ITEMS']
            snapshots.append(dict(step=step, race_prev=prev,
                                  inference_previous={item: inferred.get((step-1, i)) for i, item in enumerate(items)},
                                  next_predictions={item: [sum(ev.get((step+dt, i), 0) for dt in (1,2)) for ev in forecasts]
                                                    for i, item in enumerate(items)},
                                  final_market=deepcopy(action.get('market') or [])))
            return action

        env, ledger = run(agent, opponent, control['seed'], seat)
        assert all(compact_state(a) == compact_state(b) for a, b in zip(env.steps, replay['steps']))
        assert all(env.steps[t+1][seat].action == replay['steps'][t+1][seat]['action'] for t in range(719))
        assert [s.reward for s in env.steps[-1]] == control['rewards']
        original_ledger = [json.loads(line) for line in gzip.decompress((OUT / f'feedback_{suffix}.{episode}.ledger.jsonl.gz').read_bytes()).decode().splitlines()]
        assert ledger == original_ledger
        fills = Counter((e['step'], e['player'], e['item']) for e in ledger if e['op'] == 'SELL')
        increments = Counter((e['step'], e['player'], e['item']) for e in ledger if e['op'] == 'SELL' and e['value'] > 1)
        compared = []; summary = Counter()
        for step in range(718):
            prev = snapshots[step]['race_prev']
            after = env.steps[step+1][0].observation['market']['inventory']
            draw = ns['_v9_town_draw'](prev['shops'], step)
            for item in ns['_V92_P_ITEMS']:
                if prev['prices'].get(item, 0) <= 3:
                    continue
                own_count = int(prev['own'].get(item, 0))
                own_actual = fills[step, seat, item]
                own_added = increments[step, seat, item]
                other_actual = fills[step, 1-seat, item]
                other_added = increments[step, 1-seat, item]
                residual = int(after[item]) - int(prev['inventory'][item]) + draw.get(item, 0)
                assert residual == own_added + other_added, (episode, step, item, residual, own_added, other_added)
                estimate = residual-own_count
                recorded = snapshots[step+1]['inference_previous'][item]
                assert recorded == (estimate if estimate >= 2 else None), (episode, step, item, recorded, estimate)
                summary['eligible_item_turns'] += 1
                summary['own_snapshot_differs_from_accepted_qty'] += own_count != own_actual
                summary['own_snapshot_differs_from_inventory_added'] += own_count != own_added
                summary['false_event_vs_actual_sales'] += recorded is not None and other_actual < 2
                summary['missed_event_vs_actual_sales'] += recorded is None and other_actual >= 2
                summary['false_event_vs_inventory_added'] += recorded is not None and other_added < 2
                summary['missed_event_vs_inventory_added'] += recorded is None and other_added >= 2
                if own_count != own_added or recorded is not None or other_actual:
                    compared.append(dict(step=step, item=item, own_snapshot=own_count,
                                         own_accepted=own_actual, own_inventory_added=own_added,
                                         rival_accepted=other_actual, rival_inventory_added=other_added,
                                         inferred_quantity=estimate, recorded_event=recorded,
                                         final_market=snapshots[step]['final_market']))
        for kind, data in [('snapshots', snapshots), ('comparisons', compared)]:
            Path(str(prefix) + f'.{episode}.{kind}.jsonl.gz').write_bytes(gzip.compress(
                ('\n'.join(json.dumps(r) for r in data)+'\n').encode(), mtime=0))
        results.append(dict(episode=episode, policy=control['policy'], opponent=control['opponent'],
                            source_sha256=control['source_sha256'], exact_actions=719, exact_states=720,
                            ledger_exact=True, summary=dict(summary)))
        print(json.dumps(results[-1]), flush=True)
    target.write_text(json.dumps(dict(plan=plan, results=results), indent=2) + '\n')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('suffix'); main(ap.parse_args().suffix)
