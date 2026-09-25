"""Measure same-tile work available at actual PASS execution, without changing it."""
from collections import Counter
from copy import deepcopy
import hashlib
import importlib
import json
from pathlib import Path
import sys

from investigar_lider import compact_state
from sonda_fallo_forecast import run

OUT = Path('docs/evidencia/loop_publicos_20260925/pass_opportunities_v2.json')
SOURCES = [Path('replays/top3_current')/f'episode-{e}-replay.json'
           for e in (113108628, 113107623, 113107458, 113106269)]
SOURCES += [Path('replays/top3_current_0339')/f'episode-{e}-replay.json'
            for e in (113127276, 113126108, 113124966, 113125627)]


def main():
    if OUT.exists():
        raise FileExistsError(OUT)
    engine = importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    original = engine._apply_unit_action
    original_night = engine._end_of_day
    results = []
    for path in SOURCES:
        raw = path.read_bytes()
        replay = json.loads(raw)
        seat = replay['info']['TeamNames'].index('Rospel')
        events, total_pass, nights = [], [0], {}
        def instrument(farm, private, actor, action, *args, **kwargs):
            frame = sys._getframe(1)
            if frame.f_code is engine.interpreter.__code__ and frame.f_locals.get('i') == seat and action == ['PASS']:
                total_pass[0] += 1
                step = frame.f_locals['step']; day = step // 24
                x, y = farm['farmer'] if actor == 0 else farm['hands'][actor-1]
                tile = farm['tiles'][y][x]
                inv = private['inventories'][actor]
                available = []
                if isinstance(tile, dict) and tile.get('animal'):
                    spec = engine.ANIMALS[tile['animal']]
                    first = tile['placed_day'] + spec['first_yield_day']
                    future = [d for d in range(max(day+1, first), 30) if (d-first) % spec['interval'] == 0]
                    # Today's CARE is banked after tonight's production; it can
                    # only pay on a later production refresh, with headroom.
                    if (not tile['cared_today'] and any(d >= day+2 for d in future)
                            and tile.get('pending_care_bonus', 0) < spec['max_held']-1):
                        available.append('CARE_FED' if tile['fed_today'] else 'CARE_UNFED')
                    if not tile['fed_today'] and inv.get('WHEAT', 0) > 0 and future:
                        available.append('FEED')
                    if tile.get('yield_units', 0) > 0:
                        available.append('HARVEST_ANIMAL')
                    if tile.get('fertilizer_available'):
                        available.append('COLLECT_FERTILIZER')
                elif isinstance(tile, dict) and tile.get('crop'):
                    spec = engine.CROPS[tile['crop']]
                    age = day-tile['planted_day']
                    if not tile['watered_today'] and day < 29:
                        available.append('WATER')
                    if tile.get('yield_units', 0) > 0 and age >= spec['first_yield_day']:
                        available.append('HARVEST_ONGOING' if spec['ongoing'] else 'HARVEST_ONETIME')
                    if inv.get('FERTILIZER', 0) > 0 and tile.get('fertilized_until_day', -1) < day and day < 29:
                        available.append('FERTILIZE')
                if available:
                    events.append(dict(step=step, actor=actor, xy=[x,y], available=available,
                                       tile=deepcopy(tile), inventory=dict(inv)))
            return original(farm, private, actor, action, *args, **kwargs)
        def midnight(state, env, day):
            nights[day] = deepcopy(state[0].observation.farms[seat].tiles)
            return original_night(state, env, day)
        def tape(player):
            def agent(obs):
                return deepcopy(replay['steps'][int(obs['step'])+1][player]['action'])
            return agent
        engine._apply_unit_action = instrument
        engine._end_of_day = midnight
        try:
            env, ledger = run(tape(0), tape(1), replay['info']['seed'], 0)
        finally:
            engine._apply_unit_action = original
            engine._end_of_day = original_night
        assert all(compact_state(a) == compact_state(b) for a, b in zip(env.steps, replay['steps']))
        for event in events:
            day = event['step']//24; x, y = event['xy']; old = event['tile']
            tile = nights[day][y][x] if day in nights else None
            missed = []
            if isinstance(tile, dict) and tile.get('animal') == old.get('animal') and 'animal' in old and tile.get('placed_day') == old.get('placed_day'):
                for op in event['available']:
                    if op.startswith('CARE_') and tile['fed_today'] and not tile['cared_today']:
                        missed.append('CARE')
                    elif op == 'FEED' and not tile['fed_today']:
                        missed.append('FEED')
                    elif op == 'COLLECT_FERTILIZER' and tile.get('fertilizer_available'):
                        missed.append(op)
                    elif op == 'HARVEST_ANIMAL':
                        spec = engine.ANIMALS[tile['animal']]
                        age = day+1-tile['placed_day']-spec['first_yield_day']
                        bonus = tile.get('pending_care_bonus', 0) if tile['fed_today'] else 0
                        if age >= 0 and age % spec['interval'] == 0 and tile.get('yield_units', 0)+1+bonus > spec['max_held']:
                            missed.append('HARVEST_CAP')
            elif isinstance(tile, dict) and 'crop' in old and tile.get('crop') == old['crop'] and tile.get('planted_day') == old.get('planted_day'):
                if 'WATER' in event['available'] and not tile['watered_today']:
                    missed.append('WATER')
                if 'FERTILIZE' in event['available'] and tile.get('fertilized_until_day', -1) < day:
                    missed.append('FERTILIZE_UNCOVERED')
            event['unserved_at_close'] = missed
            event['tile_before_night'] = tile
        totals = Counter(op for e in events for op in e['available'])
        unique = {op: len({(e['step']//24, tuple(e['xy'])) for e in events if op in e['available']}) for op in totals}
        missed = {op: len({(e['step']//24, tuple(e['xy'])) for e in events if op in e['unserved_at_close']})
                  for op in sorted({op for e in events for op in e['unserved_at_close']})}
        row = dict(path=str(path), sha256=hashlib.sha256(raw).hexdigest(), seat=seat,
                   states_exact=720, cash_reconciled=True, total_pass=total_pass[0],
                   opportunities=dict(totals), unique_day_tiles=unique,
                   unserved_day_tiles=missed, events=events)
        results.append(row)
        print(path.name, total_pass[0], 'unserved unique day/tiles', missed, flush=True)
    OUT.write_text(json.dumps(dict(selection='All eight previously selected top3 real episodes; no new outcome filter.',
                                   note='Potential same-tile operations at actual PASS execution. Repeated visits are not independent benefits; this does not measure extra output, feasibility of future delivery, or W/L.',
                                   replays=results), indent=2)+'\n')


if __name__ == '__main__':
    main()
