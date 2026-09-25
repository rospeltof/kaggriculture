"""Trace physical seed use, planting and production for the registered loop26 development."""
from collections import Counter
from copy import deepcopy
import gzip
import hashlib
import importlib
import json
import os
from pathlib import Path
import sys
import tarfile
import time

from auditar_forecast_pareado_real import inspect_env
from construir_semillas_tardias import BASE, OUT as AGENTS, EVIDENCE as OUT
from sonda_fallo_forecast import run


def packed(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def main():
    assert os.environ.get('PYTHONHASHSEED') == '0'
    manifest = json.loads((AGENTS / 'manifest.json').read_text())
    arms = dict(base=str(BASE), **{name: row['path'] for name, row in manifest.items()})
    plan = dict(seeds=[1065000, 1065001, 102886466, 1943089929], seats=[0, 1], expected_games=40,
                opponent='submission/main_publico_arshs3_arsgorynich.py', runtime_hash_seed='0',
                agents={name: dict(path=path, sha256=hashlib.sha256(Path(path).read_bytes()).hexdigest()) for name, path in arms.items()},
                purpose='Registered seed commitment development, accepted mechanics and preservation checks; rewards do not select arms.')
    target = OUT / 'late_seed_smoke.json'; plan_path = OUT / 'late_seed_smoke.plan.json'
    assert not target.exists() and not plan_path.exists()
    plan_path.write_text(json.dumps(plan, indent=2) + '\n')
    with tarfile.open(OUT / 'late_seed_smoke.sources.tgz', 'x:gz') as archive:
        for name, path in arms.items():
            archive.add(path, arcname=f'agents/{name}.py')
        archive.add(plan['opponent'], arcname='opponent.py')
        archive.add(__file__, arcname=Path(__file__).name)
    engine = importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    original_unit = engine._apply_unit_action; original_night = engine._end_of_day
    baseline = {}; results = []
    for seed in plan['seeds']:
        for name, path in arms.items():
            for seat in plan['seats']:
                raw = Path(path).read_bytes(); assert hashlib.sha256(raw).hexdigest() == plan['agents'][name]['sha256']
                ns = {}; exec(compile(raw, path, 'exec'), ns)
                entry = [v for v in ns.values() if callable(v)][-1]
                elapsed = []; emitted = []; units = []; nights = []
                planted = Counter(); accepted = Counter(); harvest = Counter()

                def agent(obs, config=None):
                    start = time.perf_counter(); action = entry(obs, config)
                    elapsed.append(1000 * (time.perf_counter()-start)); emitted.append(deepcopy(action)); return action

                def instrument(farm, private, actor, command, *args, **kwargs):
                    frame = sys._getframe(1)
                    actual = frame.f_code is engine.interpreter.__code__ and frame.f_locals.get('i') == seat
                    watched = actual and command and command[0] in ('PLANT', 'FEED', 'CARE', 'HARVEST', 'FERTILIZE')
                    if watched:
                        x, y = farm['farmer'] if actor == 0 else farm['hands'][actor-1]
                        tile = deepcopy(farm['tiles'][y][x]); inv = dict(private['inventories'][actor]); seeds_before = dict(private['seeds'])
                        subject = tile.get('animal') or tile.get('crop') or tile.get('kind') if isinstance(tile, dict) else None
                    result = original_unit(farm, private, actor, command, *args, **kwargs)
                    if watched:
                        after = private['inventories'][actor]
                        delta = {item: after.get(item, 0)-inv.get(item, 0) for item in set(after)|set(inv)}
                        used = {crop: seeds_before.get(crop, 0)-private['seeds'].get(crop, 0) for crop in seeds_before}
                        success = False
                        if command[0] == 'PLANT':
                            planted.update({crop: n for crop, n in used.items() if n > 0}); success = any(n > 0 for n in used.values())
                        elif command[0] == 'HARVEST':
                            gained = {item: n for item, n in delta.items() if n > 0}; harvest.update(gained); success = bool(gained)
                        elif command[0] == 'FEED':
                            success = delta.get('WHEAT', 0) < 0
                        elif command[0] == 'FERTILIZE':
                            success = delta.get('FERTILIZER', 0) < 0
                        elif isinstance(tile, dict) and isinstance(farm['tiles'][y][x], dict):
                            success = not tile.get('cared_today') and farm['tiles'][y][x].get('cared_today', False)
                        if success:
                            accepted[command[0]+':'+str(subject)] += 1
                        units.append(dict(step=frame.f_locals['step'], actor=actor, xy=[x, y], command=deepcopy(command),
                                          accepted=bool(success), seed_consumption={k: v for k, v in used.items() if v},
                                          inventory_delta={k: v for k, v in delta.items() if v}))
                    return result

                def midnight(state, env, day):
                    private = deepcopy(state[seat].observation.private)
                    before = Counter(private['shed'])
                    for bag in private['inventories']:
                        before.update(bag)
                    result = original_night(state, env, day)
                    after = Counter(state[seat].observation.private['shed'])
                    nights.append(dict(step=day*24+23, loss=dict(before-after)))
                    return result

                engine._apply_unit_action, engine._end_of_day = instrument, midnight
                try:
                    env, ledger = run(agent, plan['opponent'], seed, seat)
                finally:
                    engine._apply_unit_action, engine._end_of_day = original_unit, original_night
                actions = [[s.action for s in row] for row in env.steps[1:]]
                assert len(emitted) == 719 and emitted == [row[seat] for row in actions]
                rewards = [s.reward for s in env.steps[-1]]
                unit_vectors = [[a.get('farmer') or ['PASS'], *(a.get('hands') or [])] for a in emitted]
                shops = [row[0].observation['town'] for row in env.steps]
                if name == 'base':
                    baseline[seed, seat] = dict(actions=deepcopy(actions), rewards=rewards, units=unit_vectors, shops=shops)
                reference = baseline[seed, seat]
                if name == 'seed_noop':
                    assert reference['actions'] == actions and reference['rewards'] == rewards
                buys = Counter((e['step'], e['item']) for e in ledger if e['player'] == seat and e['op'] == 'BUY_SEED')
                balances = []
                for step in range(719):
                    before = env.steps[step][seat].observation['private']['seeds']
                    after = env.steps[step+1][seat].observation['private']['seeds']
                    commands = unit_vectors[step]
                    requested = Counter(c[1] for c in commands if len(c) >= 2 and c[0] == 'PLANT')
                    used = {crop: int(before.get(crop, 0))+buys[step, crop]-int(after.get(crop, 0)) for crop in before}
                    assert all(0 <= amount <= requested[crop] for crop, amount in used.items())
                    if step >= 624 and (requested or buys[step, 'WHEAT']):
                        balances.append(dict(step=step, before=dict(before), requested=dict(requested), used=used,
                                             bought_wheat=buys[step, 'WHEAT'], after=dict(after)))
                reports = {key: deepcopy(ns.get(key, {})) for key in ('_LS_REPORT', '_E402_REPORT', '_CA_REPORT', '_VQ_REPORT', '_R127_REPORT')}
                assert not any(value for report in reports.values() for key, value in report.items() if 'error' in key and isinstance(value, (int, float)))
                label = f'late_seed_smoke.{seed}.{name}.{seat}'
                for suffix, content in (('ledger', ledger), ('units', units)):
                    (OUT / f'{label}.{suffix}.jsonl.gz').write_bytes(gzip.compress(b'\n'.join(packed(row) for row in content)+b'\n', mtime=0))
                result = dict(arm=name, seed=seed, seat=seat, source_sha256=plan['agents'][name]['sha256'],
                              action_hash=hashlib.sha256(b'\n'.join(packed(a) for a in emitted)+b'\n').hexdigest(),
                              max_turn_ms=max(elapsed), reports=reports, edits=deepcopy(ns.get('_LS_EVENTS', [])),
                              planted=dict(planted), accepted=dict(accepted), harvested=dict(harvest), nights=nights,
                              same_unit_actions=unit_vectors == reference['units'], same_shops=shops == reference['shops'],
                              changed_action_turns=sum(a != b for a, b in zip(actions, reference['actions'])),
                              seed_balances=balances, **inspect_env(env, ledger, seat))
                results.append(result)
                print(json.dumps({k: result[k] for k in ('arm', 'seed', 'seat', 'same_unit_actions', 'same_shops', 'changed_action_turns', 'max_turn_ms')}), flush=True)
    assert len(results) == 40
    target.write_text(json.dumps(dict(plan=plan, results=results), indent=2) + '\n')


if __name__ == '__main__':
    main()
