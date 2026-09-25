"""Actual feed/care/harvest and losses for the registered feed-value ablations."""
from collections import Counter
from copy import deepcopy
import gzip
import hashlib
import importlib
import json
from pathlib import Path
import sys
import tarfile
import time

from construir_alimentacion_economica import BASE, OUT as AGENTS, EVIDENCE as OUT
from sonda_fallo_forecast import run

TAG = 'feed_smoke'


def main():
    manifest = json.loads((AGENTS/'manifest.json').read_text())
    arms = {'base': str(BASE), **{n: r['path'] for n, r in manifest.items()}}
    plan = dict(seeds=[1030000, 1004000, 1272457736], seats=[0, 1],
                opponent='submission/main_publico_arshs3_arsgorynich.py',
                purpose='Feed mechanics with a reactive rival; no development reward selection.',
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
    original_unit, original_night = engine._apply_unit_action, engine._end_of_day
    baseline, results = {}, []
    for seed in plan['seeds']:
        for name, path in arms.items():
            for seat in plan['seats']:
                ns = {}
                exec(compile(Path(path).read_bytes(), path, 'exec'), ns)
                entry = [v for v in ns.values() if callable(v)][-1]
                elapsed, events, nights = [], [], []
                attempts, successful, harvested = Counter(), Counter(), Counter()
                def timed(obs, config=None):
                    start = time.perf_counter()
                    result = entry(obs, config)
                    elapsed.append((time.perf_counter()-start)*1000)
                    return result
                def instrument(farm, private, actor, action, *args, **kwargs):
                    frame = sys._getframe(1)
                    actual = frame.f_code is engine.interpreter.__code__ and frame.f_locals.get('i') == seat
                    watched = actual and action and action[0] in ('FEED', 'CARE', 'HARVEST', 'FERTILIZE')
                    if watched:
                        pos = farm['farmer'] if actor == 0 else farm['hands'][actor-1]
                        x, y = pos; tile = deepcopy(farm['tiles'][y][x])
                        before = dict(private['inventories'][actor])
                        subject = str(tile.get('animal') or tile.get('crop') or tile.get('kind')) if isinstance(tile, dict) else str(tile)
                        key = action[0]+':'+subject; attempts[key] += 1
                    result = original_unit(farm, private, actor, action, *args, **kwargs)
                    if watched:
                        after = private['inventories'][actor]; newtile = farm['tiles'][y][x]
                        delta = {k: after.get(k, 0)-before.get(k, 0) for k in set(before)|set(after)}
                        ok = False
                        if action[0] == 'HARVEST':
                            gained = {k: q for k, q in delta.items() if q > 0}
                            harvested.update(gained); ok = bool(gained)
                        elif isinstance(tile, dict) and isinstance(newtile, dict):
                            if action[0] in ('FEED', 'CARE'):
                                flag = {'FEED': 'fed_today', 'CARE': 'cared_today'}[action[0]]
                                ok = not tile.get(flag) and newtile.get(flag)
                            else:
                                ok = delta.get('FERTILIZER', 0) < 0
                        if ok:
                            successful[key] += 1
                        events.append(dict(step=frame.f_locals['step'], actor=actor, xy=list(pos),
                                           action=deepcopy(action), subject=subject, successful=bool(ok),
                                           inventory_delta={k: q for k, q in delta.items() if q}))
                    return result
                def midnight(state, env, day):
                    private = deepcopy(state[seat].observation.private)
                    before = Counter(private['shed'])
                    for inv in private['inventories']:
                        before.update(inv)
                    tiles = state[0].observation.farms[seat].tiles
                    unfed = [dict(x=x, y=y, animal=t['animal']) for y, line in enumerate(tiles)
                             for x, t in enumerate(line) if isinstance(t, dict) and t.get('animal') and not t['fed_today']]
                    result = original_night(state, env, day)
                    after = Counter(state[seat].observation.private['shed'])
                    nights.append(dict(step=day*24+23, loss=dict(before-after), unfed=unfed))
                    return result
                engine._apply_unit_action, engine._end_of_day = instrument, midnight
                try:
                    env, ledger = run(timed, plan['opponent'], seed, seat)
                finally:
                    engine._apply_unit_action, engine._end_of_day = original_unit, original_night
                actions = [[s.action for s in turn] for turn in env.steps[1:]]
                rewards = [s.reward for s in env.steps[-1]]
                key = seed, seat
                if name == 'base':
                    baseline[key] = actions, rewards
                if name == 'feed_noop':
                    assert (actions, rewards) == baseline[key]
                reports = {k: deepcopy(ns.get(k, {})) for k in ('_R85_REPORT', '_V92_P_REPORT', '_VQ_REPORT')}
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
                losses = Counter()
                for night in nights:
                    losses.update(night['loss'])
                flows = {}
                for e in ledger:
                    if e['player'] == seat:
                        item = e['op']+':'+str(e['item']); q, cash = flows.get(item, [0, 0])
                        flows[item] = [q+1, cash+e['value']]
                row = dict(seed=seed, arm=name, seat=seat, rewards=rewards, reports=reports,
                           attempts=dict(attempts), successful=dict(successful), harvested=dict(harvested),
                           flows=flows, nights=nights, losses=dict(losses), escapes=escapes,
                           terminal_private=env.steps[-1][seat].observation.private,
                           shops=env.steps[-1][0].observation.town.unlocked_shops,
                           max_turn_ms=max(elapsed), action_hash=hashlib.sha256(json.dumps(actions, sort_keys=True).encode()).hexdigest(),
                           changed_action_turns=sum(a[seat] != b[seat] for a, b in zip(actions, baseline[key][0])))
                results.append(row)
                for kind, data in (('ledger', ledger), ('units', events)):
                    (OUT/f'{TAG}.{seed}.{name}.{seat}.{kind}.jsonl.gz').write_bytes(gzip.compress(('\n'.join(json.dumps(e) for e in data)+'\n').encode(), mtime=0))
                print(json.dumps({k: row[k] for k in ('seed','arm','seat','rewards','max_turn_ms','changed_action_turns','successful','harvested','escapes')}), flush=True)
    (OUT/(TAG+'.json')).write_text(json.dumps(results, indent=2)+'\n')


if __name__ == '__main__':
    main()
