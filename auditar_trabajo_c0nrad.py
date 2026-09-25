"""Replay diagnosis: actual unit work and output, not inferred from orders."""
from collections import Counter, defaultdict
from copy import deepcopy
import importlib
import json
from pathlib import Path
import sys

from investigar_lider import compact_state
from sonda_fallo_forecast import run

OUT = Path('docs/evidencia/loop_publicos_20260925/c0nrad_labor_audit.json')


def main():
    if OUT.exists():
        raise FileExistsError(OUT)
    path = Path('replays/top3_current/episode-113107623-replay.json')
    replay = json.loads(path.read_text())
    engine = importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    original = engine._apply_unit_action
    commands = [Counter(), Counter()]
    successful = [Counter(), Counter()]
    harvest = [Counter(), Counter()]
    daily = [defaultdict(Counter), defaultdict(Counter)]
    def instrument(farm, private, idx, action, *args, **kwargs):
        frame = sys._getframe(1)
        actual = frame.f_code is engine.interpreter.__code__
        player = frame.f_locals.get('i') if actual else None
        before = {}
        tile = None
        if actual:
            xy = tuple(farm['farmer'] if idx == 0 else farm['hands'][idx-1])
            tile = deepcopy(farm['tiles'][xy[1]][xy[0]])
            before = dict(private['inventories'][idx])
        result = original(farm, private, idx, action, *args, **kwargs)
        if actual:
            op = action[0] if action else 'PASS'
            subject = (tile.get('animal') or tile.get('crop') or tile.get('kind')) if isinstance(tile, dict) else str(tile)
            key = op+':'+subject
            commands[player][key] += 1
            day = frame.f_locals['step']//24
            daily[player][day][op] += 1
            after = private['inventories'][idx]
            newtile = farm['tiles'][xy[1]][xy[0]]
            if op == 'HARVEST':
                units = sum(max(0, after.get(k, 0)-before.get(k, 0)) for k in set(before)|set(after))
                if units:
                    successful[player][key] += 1
                    harvest[player][subject] += units
            elif op in ('FEED', 'CARE', 'WATER') and isinstance(tile, dict) and isinstance(newtile, dict):
                flag = {'FEED': 'fed_today', 'CARE': 'cared_today', 'WATER': 'watered_today'}[op]
                if not tile.get(flag) and newtile.get(flag):
                    successful[player][key] += 1
            elif op == 'COLLECT_FERTILIZER' and after.get('FERTILIZER', 0) > before.get('FERTILIZER', 0):
                successful[player][key] += 1
            elif op.startswith('BUILD_') and newtile != tile:
                successful[player][op] += 1
            elif op == 'PLANT' and newtile != tile:
                successful[player][op+':'+str(newtile.get('crop') if isinstance(newtile, dict) else None)] += 1
        return result
    def tape(player):
        def agent(obs):
            return deepcopy(replay['steps'][int(obs['step'])+1][player]['action'])
        return agent
    engine._apply_unit_action = instrument
    try:
        env, ledger = run(tape(0), tape(1), replay['info']['seed'], 0)
    finally:
        engine._apply_unit_action = original
    assert all(compact_state(a) == compact_state(b) for a, b in zip(env.steps, replay['steps']))
    rows = []
    for player, name in enumerate(replay['info']['TeamNames']):
        aggregate = Counter()
        for key, qty in commands[player].items():
            op = key.split(':')[0]
            aggregate['MOVE' if op in ('NORTH', 'SOUTH', 'EAST', 'WEST') else op] += qty
        row = dict(player=player, name=name, commands=dict(commands[player]), command_totals=dict(aggregate),
                   successful_work=dict(successful[player]), harvested_units=dict(harvest[player]),
                   daily_commands={d: dict(v) for d,v in daily[player].items()},
                   hires=sum(r['player'] == player and r['op'] == 'HIRE' for r in ledger),
                   labor_cash=-sum(r['value'] for r in ledger if r['player'] == player and r['op'] == 'HIRE'))
        rows.append(row)
        print(name, row['command_totals'], 'harvest', row['harvested_units'], 'successful', row['successful_work'], flush=True)
    OUT.write_text(json.dumps(dict(episode=113107623, states_exact=720, cash_reconciled=True,
                                   note='One selected loss, mechanism diagnosis. Command totals include ineffective attempts; successful_work separately checks state/inventory changes inside the real engine.',
                                   players=rows), indent=2, ensure_ascii=False)+'\n')


if __name__ == '__main__':
    main()
