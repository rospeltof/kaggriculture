"""Disparo y cohortes reales del experimento seed_partial_batch.

No estima fuerza: registra acciones emitidas y PLANT confirmados en el tablero.
Uso: ./.venv/bin/python sondas/005_lotes_semillas.py --seed 99000
Puede comparar además el chasis anterior con --reference /tmp/chassis_base.py.
"""
import argparse
import contextlib
import copy
import hashlib
import io
import json
import sys
import time
import types
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from bots import chassis
from bots.arquetipos import CAMPEONA_HOZ
from bots.meta.tape import make as tape_agent


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def planted_events(env, seat):
    """Plantados visibles y cota inferior de compras inferida del stock.

    Si un PLANT muere en el mismo refresh de h23, no queda visible y el
    consumo de esa semilla no se repone en la inferencia de compras. Las
    cohortes sirven para fechar plantas confirmadas vivas, no toda orden.
    """
    events, buys = [], []
    for before, after in zip(env.steps, env.steps[1:]):
        obs0, obs1 = before[0].observation, after[0].observation
        old = obs0['farms'][seat]['tiles']
        new = obs1['farms'][seat]['tiles']
        planted = Counter()
        for y, row in enumerate(new):
            for x, cell in enumerate(row):
                if not isinstance(cell, dict) or cell.get('kind') != 'PLANT':
                    continue
                previous = old[y][x]
                if (isinstance(previous, dict) and previous.get('kind') == 'PLANT'
                        and previous.get('crop') == cell['crop']
                        and previous.get('planted_day') == cell['planted_day']):
                    continue
                events.append({'crop': cell['crop'], 'day': cell['planted_day'],
                               'hour': obs0['hour'], 'x': x, 'y': y})
                planted[cell['crop']] += 1
        seeds0 = before[seat].observation.get('private', {}).get('seeds', {})
        seeds1 = after[seat].observation.get('private', {}).get('seeds', {})
        for crop in chassis.CROP:
            # Las unidades actúan antes que el mercado: reponer lo consumido
            # por PLANT al delta de semillas identifica la compra ejecutada.
            qty = seeds1.get(crop, 0) - seeds0.get(crop, 0) + planted[crop]
            if qty > 0:
                buys.append({'crop': crop, 'day': obs0['day'], 'hour': obs0['hour'], 'qty': qty})
    return events, buys


def run_arm(name, cfg, module, tape, seed, seat):
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        from kaggle_environments import make
    actions, snapshots = [], []

    def agent(obs):
        action = module.decide(obs, cfg)
        actions.append(copy.deepcopy(action))
        snapshots.append({'day': obs['day'], 'hour': obs['hour'],
                          'money': obs['farms'][seat]['money'],
                          'seeds': copy.deepcopy(obs['private'].get('seeds', {}))})
        return action

    module._ROUTER_STATE.clear()
    env = make('kaggriculture', configuration={'episodeSteps': 720, 'seed': seed}, debug=False)
    start = time.monotonic()
    rival = tape_agent(tape)
    env.run([agent, rival] if seat == 0 else [rival, agent])
    statuses = [s.status for s in env.steps[-1]]
    if statuses != ['DONE', 'DONE']:
        raise RuntimeError(f'{name}: estados inválidos {statuses}')
    events, buys = planted_events(env, seat)
    crops = {}
    for crop in chassis.CROP:
        rows = [e for e in events if e['crop'] == crop]
        cohorts = Counter(e['day'] for e in rows)
        crops[crop] = {'first_plant': rows[0] if rows else None,
                       'cohorts_by_day': dict(sorted(cohorts.items())),
                       'planted_by_d6': sum(n for day, n in cohorts.items() if day <= 6),
                       'planted_by_d4': sum(n for day, n in cohorts.items() if day <= 4)}
    result = {'name': name, 'config_sha256': digest(cfg), 'actions_sha256': digest(actions),
              'action_count': len(actions), 'rewards': [s.reward for s in env.steps[-1]],
              'statuses': statuses, 'seconds': round(time.monotonic() - start, 3),
              'crops': crops, 'plant_events': events, 'seed_buys_lower_bound': buys}
    print(f"{name}: {len(actions)} turnos, estados {statuses}", flush=True)
    return result, actions, snapshots


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seed', type=int, default=99000)
    parser.add_argument('--seat', type=int, choices=(0, 1), default=0)
    parser.add_argument('--tape', default=None)
    parser.add_argument('--reference', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    tape = args.tape or sorted(ROOT.glob('bots/meta/tapes/lad_*.json.gz'))[0].name[:-8]
    output = args.output or ROOT / f'results/sonda_lotes_{args.seed}_s{args.seat}.json'
    if output.exists():
        parser.error(f'Ya existe {output}; usa --output para conservar la evidencia previa.')
    plan = [('base', dict(CAMPEONA_HOZ), chassis), ('noop', dict(CAMPEONA_HOZ), chassis),
            ('partial_batch', dict(CAMPEONA_HOZ, seed_partial_batch=True), chassis)]
    if args.reference:
        reference = types.ModuleType('chassis_reference')
        exec(compile(args.reference.read_text(), str(args.reference), 'exec'), reference.__dict__)
        plan.append(('reference', dict(CAMPEONA_HOZ), reference))
    report = {'seed': args.seed, 'seat': args.seat, 'tape': tape,
              'chassis_sha256': hashlib.sha256(Path(chassis.__file__).read_bytes()).hexdigest(),
              'purpose': 'Activación y mecanismo; un episodio no estima win-rate.', 'arms': {}}
    base_actions = None
    for name, cfg, module in plan:
        result, actions, snapshots = run_arm(name, cfg, module, tape, args.seed, args.seat)
        if base_actions is None:
            base_actions = actions
        differing = [i for i in range(max(len(base_actions), len(actions)))
                     if (base_actions[i] if i < len(base_actions) else None)
                     != (actions[i] if i < len(actions) else None)]
        result['different_action_turns'] = len(differing)
        if differing:
            first = differing[0]
            result['first_difference'] = {'turn': first, 'state': snapshots[first],
                                           'base_action': base_actions[first], 'action': actions[first]}
        report['arms'][name] = result
    for name in ('noop', 'reference'):
        if name in report['arms']:
            arm, base = report['arms'][name], report['arms']['base']
            if arm['different_action_turns'] or arm['rewards'] != base['rewards']:
                raise RuntimeError(f'{name} difiere de base: experimento inválido.')
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x') as fh:
        json.dump(report, fh, ensure_ascii=False, indent=2)
    for name, arm in report['arms'].items():
        summary = {c: {'first': arm['crops'][c]['first_plant'],
                       'by_d4': arm['crops'][c]['planted_by_d4'],
                       'by_d6': arm['crops'][c]['planted_by_d6']}
                   for c in ('MELON', 'STRAWBERRY')}
        print(json.dumps({'arm': name, 'different_action_turns': arm['different_action_turns'],
                          'crops': summary}, ensure_ascii=False), flush=True)
    print(f'Evidencia: {output}', flush=True)


if __name__ == '__main__':
    main()
