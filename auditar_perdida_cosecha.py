"""Attribute physical yield loss in the twelve preselected top3 real episodes."""
from collections import Counter
from copy import deepcopy
import hashlib
import importlib
import json
from pathlib import Path
import sys

from investigar_lider import compact_state
from sonda_fallo_forecast import run

OUT = Path('docs/evidencia/loop_publicos_20260925/field_loss_audit.json')
SOURCES = [Path('replays/top3_current')/f'episode-{e}-replay.json'
           for e in (113108628, 113107623, 113107458, 113106269)]
SOURCES += [Path('replays/top3_current_0339')/f'episode-{e}-replay.json'
            for e in (113127276, 113126108, 113124966, 113125627)]
SOURCES += [Path('replays/top3_current_0515')/f'episode-{e}-replay.json'
            for e in (113155577, 113154362, 113153102, 113151865)]


def main():
    if OUT.exists():
        raise FileExistsError(OUT)
    engine = importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    original_decay, original_night, original_unit = engine._decay_plants, engine._end_of_day, engine._apply_unit_action
    results = []
    for path in SOURCES:
        raw = path.read_bytes(); replay = json.loads(raw)
        assert replay['info']['TeamNames'].count('Rospel') == 1
        seat = replay['info']['TeamNames'].index('Rospel')
        events = []
        def decay(farm, step):
            frame = sys._getframe(1)
            assert frame.f_code is engine.interpreter.__code__
            player = next(i for i, f in enumerate(frame.f_locals['obs0'].farms) if f is farm)
            before = {(x,y): deepcopy(t) for y, row in enumerate(farm['tiles']) for x, t in enumerate(row)
                      if isinstance(t, dict) and t.get('kind') == 'PLANT'}
            value = original_decay(farm, step)
            for (x,y), tile in before.items():
                after = farm['tiles'][y][x]
                new = after.get('yield_units', 0) if isinstance(after, dict) and after.get('kind') == 'PLANT' else 0
                lost = max(0, tile.get('yield_units', 0)-new)
                if lost:
                    events.append(dict(kind='DECAY', step=step, player=player, xy=[x,y], product=tile['crop'],
                                       lost=lost, tile_before=tile))
            return value
        def midnight(state, env, day):
            before = [deepcopy(f.tiles) for f in state[0].observation.farms]
            value = original_night(state, env, day)
            for player, tiles in enumerate(before):
                for y, row in enumerate(tiles):
                    for x, tile in enumerate(row):
                        if not isinstance(tile, dict):
                            continue
                        new = state[0].observation.farms[player].tiles[y][x]
                        if tile.get('animal'):
                            spec = engine.ANIMALS[tile['animal']]
                            if not isinstance(new, dict) or new.get('animal') != tile['animal']:
                                continue
                            age = day+1-tile['placed_day']-spec['first_yield_day']
                            if age < 0 or age % spec['interval']:
                                continue
                            old = tile.get('yield_units', 0)
                            increment = 1+(tile.get('pending_care_bonus', 0) if tile['fed_today'] else 0)
                            expected = min(spec['max_held'], old+increment)
                            assert new['yield_units'] == expected
                            lost = old+increment-expected
                            if lost:
                                events.append(dict(kind='ANIMAL_CAP', step=day*24+23, player=player, xy=[x,y],
                                                   product=spec['product'], lost=lost,
                                                   recoverable_by_emptying=min(old, lost), tile_before=tile))
                        elif tile.get('crop'):
                            old = tile.get('yield_units', 0)
                            spec = engine.CROPS[tile['crop']]
                            if not isinstance(new, dict) or new.get('crop') != tile['crop']:
                                events.append(dict(kind='DROUGHT', step=day*24+23, player=player, xy=[x,y],
                                                   product=tile['crop'], lost=old,
                                                   harvestable_before=day-tile['planted_day'] >= spec['first_yield_day'], tile_before=tile))
                                continue
                            age = day+1-tile['planted_day']-spec['first_yield_day']
                            if not spec['ongoing'] or age < 0 or age % spec['interval'] or age//spec['interval']+1 > spec['max_yield']:
                                continue
                            increment = 2 if tile['watered_today'] and tile.get('fertilized_until_day', -1) >= day else 1
                            expected = min(spec['max_yield'], old+increment)
                            assert new['yield_units'] == expected
                            lost = old+increment-expected
                            if lost:
                                events.append(dict(kind='CROP_CAP', step=day*24+23, player=player, xy=[x,y],
                                                   product=tile['crop'], lost=lost, tile_before=tile))
            return value
        def unit(farm, private, actor, action, *args, **kwargs):
            frame = sys._getframe(1)
            watch = frame.f_code is engine.interpreter.__code__ and action and action[0] == 'DIG'
            if watch:
                x,y = farm['farmer'] if actor == 0 else farm['hands'][actor-1]
                tile = deepcopy(farm['tiles'][y][x])
            value = original_unit(farm, private, actor, action, *args, **kwargs)
            if watch and isinstance(tile, dict) and tile.get('crop') and farm['tiles'][y][x] != tile:
                events.append(dict(kind='DIG_CROP', step=frame.f_locals['step'], player=frame.f_locals['i'], xy=[x,y],
                                   product=tile['crop'], lost=tile.get('yield_units', 0), tile_before=tile))
            return value
        def tape(player):
            def agent(obs):
                return deepcopy(replay['steps'][int(obs['step'])+1][player]['action'])
            return agent
        engine._decay_plants, engine._end_of_day, engine._apply_unit_action = decay, midnight, unit
        try:
            env, ledger = run(tape(0), tape(1), replay['info']['seed'], 0)
        finally:
            engine._decay_plants, engine._end_of_day, engine._apply_unit_action = original_decay, original_night, original_unit
        assert len(env.steps) == len(replay['steps']) == 720
        assert all(compact_state(a) == compact_state(b) for a,b in zip(env.steps,replay['steps']))
        summary = []
        for player in (seat, 1-seat):
            totals, terminal = Counter(), []
            for event in events:
                if event['player'] == player:
                    totals[event['kind']+':'+event['product']] += event['lost']
                    if event['kind'] == 'ANIMAL_CAP':
                        totals['EMPTYABLE_CAP:'+event['product']] += event['recoverable_by_emptying']
            for y,row in enumerate(env.steps[-1][0].observation.farms[player].tiles):
                for x,tile in enumerate(row):
                    if not isinstance(tile,dict) or tile.get('yield_units',0) <= 0:
                        continue
                    if tile.get('animal'):
                        product = engine.ANIMALS[tile['animal']]['product']
                    elif tile.get('crop') and 29-tile['planted_day'] >= engine.CROPS[tile['crop']]['first_yield_day']:
                        product = tile['crop']
                    else:
                        continue
                    terminal.append(dict(xy=[x,y],product=product,units=tile['yield_units'],tile=deepcopy(tile)))
            summary.append(dict(player=player,name=replay['info']['TeamNames'][player],losses=dict(totals),terminal_harvestable=terminal))
        result = dict(path=str(path),sha256=hashlib.sha256(raw).hexdigest(),seat=seat,states_exact=720,
                      cash_reconciled=True,summary=summary,events=events)
        results.append(result)
        print(path.name,json.dumps([dict(name=s['name'],losses=s['losses'],terminal_units=sum(t['units'] for t in s['terminal_harvestable'])) for s in summary]),flush=True)
    OUT.write_text(json.dumps(dict(selection='All twelve top3 replays already selected by recency; no additional outcome filter.',
                                   note='Physical losses are not realizable extra income. Emptyable animal cap requires earlier harvest and feasible delivery; initial bonus above capacity cannot be fixed by emptying a zero-yield tile.',
                                   replays=results),indent=2)+'\n')


if __name__ == '__main__':
    main()
