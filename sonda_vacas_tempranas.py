"""Execution audit of early substitutions; fixed known world, never selection."""
from copy import deepcopy
import argparse
import gzip
import hashlib
import importlib
import json
from pathlib import Path
import sys
import tarfile
import time

from construir_vacas_tempranas import BASE, OUT as AGENTS
from sonda_fallo_forecast import run

OUT = Path('docs/evidencia/loop_publicos_20260925')
TAG = 'early_cow_smoke'


def main(seed=1004000, tag=TAG):
    variants = json.loads((AGENTS/'manifest.json').read_text())
    arms = {'base': str(BASE), **{n: r['path'] for n, r in variants.items()}}
    noop = AGENTS/'noop.py'
    noop.write_bytes(Path(arms['cow_d3_y1_m100']).read_bytes()+b'\n_EC_START=8\n')
    arms['noop'] = str(noop)
    plan = dict(seed=seed, seats=[0, 1], opponent='submission/main_publico_arshs3_arsgorynich.py',
                purpose='Known sheep world, physical execution and exact noop only. No performance selection.',
                agents={n: dict(path=p, sha256=hashlib.sha256(Path(p).read_bytes()).hexdigest()) for n, p in arms.items()})
    plan_path = OUT/(tag+'.plan.json')
    if plan_path.exists():
        raise FileExistsError(plan_path)
    plan_path.write_text(json.dumps(plan, indent=2)+'\n')
    with tarfile.open(OUT/(tag+'.sources.tgz'), 'x:gz') as tar:
        for n, path in arms.items():
            tar.add(path, arcname=n+'.py')
    engine = importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    original = engine._apply_unit_action
    baseline, results = {}, []
    for name, path in arms.items():
        for seat in (0, 1):
            ns = {}
            exec(compile(Path(path).read_bytes(), path, 'exec'), ns)
            entry = [v for v in ns.values() if callable(v)][-1]
            elapsed, events, buys, converted_sites = [], [], [], set()
            def timed(obs, config=None):
                start = time.perf_counter()
                action = entry(obs, config)
                elapsed.append((time.perf_counter()-start)*1000)
                orders = [o for o in action.get('market', []) if o and o[0] == 'BUY_ANIMAL']
                if orders:
                    buys.append(dict(step=int(obs['step']), orders=deepcopy(orders),
                                     shops=list(obs['town']['unlocked_shops']), money=obs['farms'][seat]['money'],
                                     route=ns['_IMPL'].chassis.players.get(seat, {}).get('route')))
                if int(obs['step']) < 192 and ns.get('_EC_REPORT', {}).get('events'):
                    converted_sites.update(ns['_Y_STATES'].get(seat, {}).get('sites', {}))
                return action
            def instrument(farm, private, idx, action, *args, **kwargs):
                frame = sys._getframe(1)
                owned = frame.f_code is engine.interpreter.__code__ and frame.f_locals.get('i') == seat
                pos = tuple(farm['farmer'] if idx == 0 else farm['hands'][idx-1])
                before = dict(private['inventories'][idx]) if owned else {}
                result = original(farm, private, idx, action, *args, **kwargs)
                if owned:
                    after = private['inventories'][idx]
                    delta = {k: after.get(k, 0)-before.get(k, 0) for k in set(before)|set(after)}
                    delta = {k: v for k, v in delta.items() if v}
                    if pos in converted_sites and action[0] in ('PLACE', 'HARVEST', 'CARE', 'FEED'):
                        events.append(dict(step=frame.f_locals['step'], actor=idx, xy=pos,
                                           action=deepcopy(action), inventory_delta=delta))
                return result
            engine._apply_unit_action = instrument
            try:
                env, ledger = run(timed, plan['opponent'], plan['seed'], seat)
            finally:
                engine._apply_unit_action = original
            actions = [[s.action for s in turn] for turn in env.steps[1:]]
            rewards = [s.reward for s in env.steps[-1]]
            if name == 'base':
                baseline[seat] = actions, rewards
            if name == 'noop':
                assert (actions, rewards) == baseline[seat]
            reports = {k: deepcopy(ns.get(k, {})) for k in ('_EC_REPORT', '_Y_REPORT', '_CS_REPORT', '_HD2_REPORT', '_V233_REPORT', '_R51_INPUT_REPORT', '_CA_REPORT', '_V92_P_REPORT')}
            errors = {key: {k: v for k, v in d.items() if 'error' in k and isinstance(v, (int, float)) and v} for key, d in reports.items()}
            assert not any(errors.values()), errors
            physical_sites, escapes = {}, []
            for xy in sorted(converted_sites):
                x, y = xy
                seen = False
                for step, row in enumerate(env.steps):
                    tile = row[0].observation.farms[seat].tiles[y][x]
                    present = isinstance(tile, dict) and tile.get('animal') == 'SHEEP'
                    if present and not seen:
                        physical_sites[str(xy)] = dict(first_seen=step, placed_day=tile['placed_day'])
                    if seen and not present:
                        escapes.append(dict(step=step, xy=xy))
                    seen = present
            sales = {}
            for r in ledger:
                if r['player'] == seat and r['op'] == 'SELL':
                    q, cash = sales.get(r['item'], [0, 0]); sales[r['item']] = [q+1, cash+r['value']]
            private = env.steps[-1][seat].observation.private
            row = dict(arm=name, seat=seat, rewards=rewards, reports=reports, buys=buys,
                       physical_sites=physical_sites, escapes=escapes,
                       site_wool_harvest=sum(e['inventory_delta'].get('WOOL', 0) for e in events if e['action'] == ['HARVEST']),
                       terminal_private=private, sales=sales, max_turn_ms=max(elapsed),
                       remaining_credit={str(k): v for k, v in ns.get('_Y_STATES', {}).get(seat, {}).get('credit', {}).items()},
                       changed_action_turns=sum(a[seat] != b[seat] for a, b in zip(actions, baseline[seat][0])),
                       action_hash=hashlib.sha256(json.dumps(actions, sort_keys=True).encode()).hexdigest())
            results.append(row)
            for kind, data in (('ledger', ledger), ('units', events)):
                (OUT/f'{tag}.{name}.{seat}.{kind}.jsonl.gz').write_bytes(gzip.compress(('\n'.join(json.dumps(r) for r in data)+'\n').encode(), mtime=0))
            print(json.dumps({k: row[k] for k in ('arm', 'seat', 'rewards', 'physical_sites', 'escapes', 'site_wool_harvest', 'remaining_credit', 'changed_action_turns', 'max_turn_ms')}), flush=True)
    (OUT/(tag+'.json')).write_text(json.dumps(results, indent=2)+'\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=1004000)
    parser.add_argument('--tag', default=TAG)
    args = parser.parse_args()
    main(args.seed, args.tag)
