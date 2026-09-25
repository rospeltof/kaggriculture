"""Submitted-source replay controls and fixed-rival VQ/top3 diagnostics."""
from collections import defaultdict
from copy import deepcopy
import gzip
import hashlib
import json
from pathlib import Path
import time

from investigar_lider import compact_state, composition
from sonda_fallo_forecast import run

OUT = Path('docs/evidencia/loop_publicos_20260925')


def inspect_env(env, ledger, seat):
    cashflow, escapes = [], []
    for player in (seat, 1-seat):
        by = defaultdict(lambda: [0, 0])
        for e in ledger:
            if e['player'] == player:
                by[e['op'], e['item']][0] += 1
                by[e['op'], e['item']][1] += e['value']
        cashflow.append([dict(op=op, item=item, units=v[0], cash=v[1]) for (op, item), v in by.items()])
        lost = []
        for step in range(719):
            a = env.steps[step][0].observation['farms'][player]['tiles']
            b = env.steps[step+1][0].observation['farms'][player]['tiles']
            for y in range(10):
                for x in range(10):
                    if isinstance(a[y][x], dict) and a[y][x].get('animal'):
                        after = b[y][x].get('animal') if isinstance(b[y][x], dict) else None
                        if after != a[y][x]['animal']: lost.append(dict(step=step, x=x, y=y, animal=a[y][x]['animal']))
        escapes.append(lost)
    rewards = [s.reward for s in env.steps[-1]]
    return dict(rewards=rewards, margin=rewards[seat]-rewards[1-seat], cashflow=cashflow,
                escapes=escapes, final_composition=[composition(env.steps[-1][0].observation['farms'][p]) for p in (seat, 1-seat)],
                terminal_private=[env.steps[-1][p].observation['private'] for p in (seat, 1-seat)])


def main():
    plan_path = OUT/'forecast_pair_replays_0653.plan.json'
    plan = json.loads(plan_path.read_text())
    target = OUT/'forecast_pair_replays_0653.json'
    if target.exists(): raise FileExistsError(target)
    results = []
    for selection in plan['selections']:
        real_policy = selection.split('_')[0]
        selected = json.loads((OUT/selection).read_text())
        for row in selected['episodes']:
            episode = row['id']; path = Path(f'replays/{real_policy}_feedback_0653/episode-{episode}-replay.json')
            raw = path.read_bytes(); replay = json.loads(raw)
            seat = replay['info']['TeamNames'].index('Rospel'); seed = replay['info']['seed']
            def opponent(obs):
                return deepcopy(replay['steps'][int(obs['step'])+1][1-seat]['action'])
            runs = {}; envs = {}
            for policy in (real_policy, 'vq' if real_policy == 'top3' else 'top3'):
                source = Path(plan['policies'][policy]); data = source.read_bytes(); ns = {}
                exec(compile(data, str(source), 'exec'), ns)
                entry = [v for v in ns.values() if callable(v)][-1]
                original_predict = ns['_v92_predict']; events = []; elapsed = []
                def predict(obs, action, st):
                    before = deepcopy(action); result = original_predict(obs, action, st)
                    if result != before:
                        step = int(obs['step'])
                        events.append(dict(step=step, market_before=before.get('market'), market_after=deepcopy(result.get('market')),
                                           shed=deepcopy(obs['private']['shed']), inventory=deepcopy(obs['market']['inventory']),
                                           top=int(ns['_V92_P_TOP']),
                                           raw_next_two=[{item: ev.get((step+1, i), 0)+ev.get((step+2, i), 0)
                                                          for i, item in enumerate(ns['_V92_P_ITEMS'])}
                                                         for ev in st.get('best', [])]))
                    return result
                ns['_v92_predict'] = predict
                def timed(obs, config=None):
                    start = time.perf_counter(); result = entry(obs, config)
                    elapsed.append((time.perf_counter()-start)*1000); return result
                env, ledger = run(timed, opponent, seed, seat); envs[policy] = env
                exact = all(compact_state(a) == compact_state(b) for a, b in zip(env.steps, replay['steps']))
                own_exact = all(env.steps[t+1][seat].action == replay['steps'][t+1][seat]['action'] for t in range(719))
                if policy == real_policy:
                    assert len(env.steps) == len(replay['steps']) == 720 and exact and own_exact
                    assert [s.reward for s in env.steps[-1]] == replay['rewards']
                prefix = f'forecast_pair_replays_0653.{episode}.{policy}'
                dest = OUT/(prefix+'.ledger.jsonl.gz'); assert not dest.exists()
                dest.write_bytes(gzip.compress(('\n'.join(json.dumps(e) for e in ledger)+'\n').encode(), mtime=0))
                events_file = OUT/(prefix+'.forecast.json'); events_file.write_text(json.dumps(events, indent=2)+'\n')
                reports = {k: deepcopy(ns.get(k, {})) for k in ('_V92_P_REPORT', '_HP_STATS', '_VQ_REPORT', '_R85_REPORT')}
                assert not any(v for report in reports.values() for k, v in report.items() if 'error' in k and isinstance(v, (int, float)))
                runs[policy] = dict(**inspect_env(env, ledger, seat), source_sha256=hashlib.sha256(data).hexdigest(),
                                    own_actions_exact=own_exact, all_states_exact=exact, max_turn_ms=max(elapsed),
                                    forecast_events=len(events), reports=reports, ledger=str(dest), events=str(events_file))
            other = 'vq' if real_policy == 'top3' else 'top3'
            actual, counter = envs[real_policy], envs[other]
            changed = [t for t in range(719) if actual.steps[t+1][seat].action != counter.steps[t+1][seat].action]
            first = changed[0] if changed else None
            shops = all(a[0].observation['town'] == b[0].observation['town'] for a, b in zip(actual.steps, counter.steps))
            result = dict(episode=episode, real_policy=real_policy, replay=str(path), replay_sha256=hashlib.sha256(raw).hexdigest(),
                          opponent=replay['info']['TeamNames'][1-seat], seed=seed, seat=seat, runs=runs,
                          changed_action_turns=len(changed), first_difference=first, shops_preserved=shops,
                          first_actions=None if first is None else {n: e.steps[first+1][seat].action for n, e in envs.items()},
                          top3_minus_vq_margin_fixed_rival=runs['top3']['margin']-runs['vq']['margin'])
            results.append(result)
            print(json.dumps({k: result[k] for k in ('episode', 'real_policy', 'opponent', 'changed_action_turns', 'first_difference', 'shops_preserved', 'top3_minus_vq_margin_fixed_rival')}), flush=True)
    target.write_text(json.dumps(dict(plan=str(plan_path), note='Actual controls reproduce every own action and state. Counterfactual rival is a tape: these differences do not estimate reactive-rival WLT or rating effects.', episodes=results), indent=2)+'\n')


if __name__ == '__main__': main()
