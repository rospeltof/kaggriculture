"""Immediate marginal water analysis on reconstructed end-of-day states."""
import importlib
import json
from pathlib import Path

OUT = Path('docs/evidencia/loop_publicos_20260925')


def main():
    engine = importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    audit = json.loads((OUT/'pass_opportunities_v2.json').read_text())
    output = []
    for row in audit['replays']:
        used, water = set(), []
        for event in row['events']:
            if 'WATER' not in event['unserved_at_close']:
                continue
            day = event['step']//24; key = day, tuple(event['xy'])
            if key in used:
                continue
            used.add(key)
            tile = event['tile_before_night']; spec = engine.CROPS[tile['crop']]
            age = day-tile['planted_day']
            fertile = tile.get('fertilized_until_day', -1) >= day
            gain = 0
            if not spec['ongoing'] and (spec['max_yield_day']+1)//2 <= age <= spec['max_yield_day']:
                gain = min(spec['max_yield']-tile['yield_units'], 2 if fertile else 1)
            if spec['ongoing']:
                since = day+1-tile['planted_day']-spec['first_yield_day']
                if since >= 0 and since % spec['interval'] == 0 and since//spec['interval']+1 <= spec['max_yield'] and fertile:
                    gain = max(0, min(spec['max_yield'], tile['yield_units']+2)-min(spec['max_yield'], tile['yield_units']+1))
            water.append(dict(step=event['step'], xy=event['xy'], crop=tile['crop'],
                              extra_immediate_or_next_dawn_units=gain,
                              prevents_drought_death=tile['consecutive_unwatered'] >= 1))
        output.append(dict(path=row['path'], unserved_day_tiles=row['unserved_day_tiles'], water=water))
    result = dict(note='Analytical immediate/next-dawn marginal water from engine rules, unique day/tile. Does not simulate future policy changes or prove no long-term effect.', replays=output)
    (OUT/'pass_marginal_water.json').write_text(json.dumps(result, indent=2)+'\n')
    print('water gaps', sum(len(r['water']) for r in output),
          'immediate extra units', sum(e['extra_immediate_or_next_dawn_units'] for r in output for e in r['water']))


if __name__ == '__main__':
    main()
