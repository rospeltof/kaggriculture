"""Validate final night predictions against real engine drops, with reactive rivals."""
from collections import Counter
from copy import deepcopy
import gzip
import hashlib
import importlib
import json
from pathlib import Path
import tarfile
import time

from construir_espacio_nocturno import BASE, OUT as AGENTS, EVIDENCE as OUT
from sonda_fallo_forecast import run

TAG = 'night_smoke_v2'

def main():
    manifest = json.loads((AGENTS/'manifest.json').read_text())
    arms = {'base': str(BASE), **{n: r['path'] for n, r in manifest.items()}}
    plan = dict(seeds=[1272457736, 1004000, 1027000], seats=[0, 1],
                opponent='submission/main_publico_arshs3_arsgorynich.py',
                purpose='Night-stock mechanics and no-op; no selection by development rewards.',
                agents={n: dict(path=p, sha256=hashlib.sha256(Path(p).read_bytes()).hexdigest()) for n, p in arms.items()})
    dest = OUT/(TAG+'.plan.json')
    if dest.exists():
        raise FileExistsError(dest)
    dest.write_text(json.dumps(plan, indent=2)+'\n')
    with tarfile.open(OUT/(TAG+'.sources.tgz'), 'x:gz') as tar:
        for name, path in arms.items():
            tar.add(path, arcname=name+'.py')
        tar.add(plan['opponent'], arcname='opponent.py')
    engine = importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    original = engine._end_of_day
    baseline, results = {}, []
    for seed in plan['seeds']:
        for name, path in arms.items():
            for seat in (0, 1):
                ns = {}
                exec(compile(Path(path).read_bytes(), path, 'exec'), ns)
                entry = [v for v in ns.values() if callable(v)][-1]
                elapsed, nights, feedback = [], [], []
                def timed(obs, config=None):
                    start = time.perf_counter()
                    result = entry(obs, config)
                    elapsed.append((time.perf_counter()-start)*1000)
                    return result
                def midnight(state, env, day):
                    private = deepcopy(state[seat].observation.private)
                    before = Counter(private['shed'])
                    for inv in private['inventories']:
                        before.update(inv)
                    farm = state[0].observation.farms[seat]
                    unfed = [dict(x=x, y=y, animal=tile['animal']) for y, row in enumerate(farm['tiles'])
                             for x, tile in enumerate(row) if isinstance(tile, dict) and tile.get('animal') and not tile.get('fed_today')]
                    result = original(state, env, day)
                    after = dict(state[seat].observation.private['shed'])
                    loss = dict(before - Counter(after))
                    event = next((e for e in ns.get('_NF_EVENTS', []) if e['step'] == day*24+23), None)
                    if event is not None:
                        same_final = ns['_ov_same'](event['predicted_final'], after)
                        same_loss = ns['_ov_same'](event['predicted_loss'], loss)
                        feedback.append(dict(step=day*24+23, final_matches=same_final, loss_matches=same_loss))
                        assert same_final and same_loss, (seed, name, seat, day, event, after, loss)
                    nights.append(dict(step=day*24+23, before_total=sum(before.values()),
                                       final=after, loss=loss, unfed=unfed))
                    return result
                engine._end_of_day = midnight
                try:
                    env, ledger = run(timed, plan['opponent'], seed, seat)
                finally:
                    engine._end_of_day = original
                actions = [[s.action for s in turn] for turn in env.steps[1:]]
                rewards = [s.reward for s in env.steps[-1]]
                key = seed, seat
                if name == 'base':
                    baseline[key] = actions, rewards
                if name == 'night_noop':
                    assert (actions, rewards) == baseline[key]
                reports = {k: deepcopy(ns.get(k, {})) for k in ('_NF_REPORT', '_V92_P_REPORT', '_VQ_REPORT')}
                assert not any(v for report in reports.values() for k, v in report.items() if 'error' in k and isinstance(v, (int, float)))
                escapes = []
                for step in range(719):
                    a = env.steps[step][0].observation.farms[seat].tiles
                    b = env.steps[step+1][0].observation.farms[seat].tiles
                    for y in range(10):
                        for x in range(10):
                            if isinstance(a[y][x], dict) and a[y][x].get('animal'):
                                after = b[y][x].get('animal') if isinstance(b[y][x], dict) else None
                                if after != a[y][x]['animal']:
                                    escapes.append(dict(step=step, xy=[x,y], animal=a[y][x]['animal']))
                lost = Counter()
                for night in nights:
                    lost.update(night['loss'])
                sales = {}
                for event in ledger:
                    if event['player'] == seat and event['op'] == 'SELL':
                        q, cash = sales.get(event['item'], [0, 0])
                        sales[event['item']] = [q+1, cash+event['value']]
                row = dict(seed=seed, arm=name, seat=seat, rewards=rewards, reports=reports, sales=sales,
                           nights=nights, lost=dict(lost), predictions=deepcopy(ns.get('_NF_EVENTS', [])),
                           prediction_validation=feedback, escapes=escapes,
                           terminal_private=env.steps[-1][seat].observation.private,
                           shops=env.steps[-1][0].observation.town.unlocked_shops,
                           max_turn_ms=max(elapsed), action_hash=hashlib.sha256(json.dumps(actions, sort_keys=True).encode()).hexdigest(),
                           changed_action_turns=sum(a[seat] != b[seat] for a, b in zip(actions, baseline[key][0])))
                results.append(row)
                (OUT/f'{TAG}.{seed}.{name}.{seat}.ledger.jsonl.gz').write_bytes(gzip.compress(('\n'.join(json.dumps(e) for e in ledger)+'\n').encode(), mtime=0))
                print(json.dumps({k: row[k] for k in ('seed','arm','seat','rewards','max_turn_ms','changed_action_turns','reports','lost','escapes')}), flush=True)
    (OUT/(TAG+'.json')).write_text(json.dumps(results, indent=2)+'\n')


if __name__ == '__main__':
    main()
