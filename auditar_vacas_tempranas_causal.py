"""Trace investment/animal failures in preselected favorable and harmful cow cells."""
from collections import Counter
from copy import deepcopy
import gzip
import importlib
import json
from pathlib import Path

from sonda_fallo_forecast import run

OUT = Path('docs/evidencia/loop_publicos_20260925')
CASES = ('pilot10.cow_d3_y2_m100.mechanism', 'pilot10.cow_d3_y1_m100.harm')


def main():
    target = OUT/'pilot10.physical_audit.json'
    if target.exists():
        raise FileExistsError(target)
    meta = json.loads((OUT/'pilot10.meta.json').read_text())
    engine = importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    original = engine._end_of_day
    results = []
    for tag in CASES:
        case = json.loads((OUT/(tag+'.json')).read_text())
        seat = case['seat']
        for index, arm in enumerate(('base', case['candidate'])):
            ns = {}; path = meta['agentes'][arm]['ruta']
            exec(compile(Path(path).read_bytes(), path, 'exec'), ns)
            entry = [v for v in ns.values() if callable(v)][-1]
            nights = []
            def midnight(state, env, day):
                farm = state[0].observation.farms[seat]
                animals = [dict(x=x, y=y, **deepcopy(t)) for y, line in enumerate(farm.tiles)
                           for x, t in enumerate(line) if isinstance(t, dict) and t.get('animal')]
                nights.append(dict(day=day, money=farm.money, animals=animals))
                return original(state, env, day)
            engine._end_of_day = midnight
            try:
                env, ledger = run(entry, meta['agentes'][case['opponent']]['ruta'], case['seed'], seat)
            finally:
                engine._end_of_day = original
            assert [s.reward for s in env.steps[-1]] == case['final_rewards'][index]
            additions, escapes = [], []
            for step in range(719):
                a = env.steps[step][0].observation.farms[seat].tiles
                b = env.steps[step+1][0].observation.farms[seat].tiles
                for y in range(10):
                    for x in range(10):
                        old = a[y][x].get('animal') if isinstance(a[y][x], dict) else None
                        new = b[y][x].get('animal') if isinstance(b[y][x], dict) else None
                        if new and new != old:
                            additions.append(dict(step=step, xy=[x,y], animal=new))
                        if old and old != new:
                            escapes.append(dict(step=step, xy=[x,y], animal=old))
            daily = []
            for day in range(30):
                events = [e for e in ledger if e['player'] == seat and e['step']//24 == day]
                farm = env.steps[day*24][0].observation.farms[seat]
                animals = Counter(t['animal'] for line in farm.tiles for t in line if isinstance(t, dict) and t.get('animal'))
                flow = Counter()
                for e in events:
                    flow[e['op']+':'+str(e['item'])] += 1
                daily.append(dict(day=day, money=farm.money, animals=dict(animals), accepted_units=dict(flow)))
            replay_path = OUT/(tag+'.'+arm+'.replay.json.gz')
            replay_path.write_bytes(gzip.compress(json.dumps(dict(steps=env.steps, info=env.info), separators=(',', ':')).encode(), mtime=0))
            row = dict(case=tag, arm=arm, seed=case['seed'], seat=seat, rewards=case['final_rewards'][index],
                       replay=str(replay_path), additions=additions, escapes=escapes, daily=daily,
                       before_night=nights, early_animal_buys=[e for e in ledger if e['player'] == seat and e['op'] == 'BUY_ANIMAL' and e['step'] < 288],
                       reports={k: deepcopy(ns.get(k)) for k in ('_EC_REPORT','_Y_REPORT','_R85_REPORT','_V233_REPORT')})
            results.append(row)
            print(tag, arm, 'escapes', escapes, 'additions', Counter(e['animal'] for e in additions), flush=True)
    target.write_text(json.dumps(results, indent=2)+'\n')


if __name__ == '__main__':
    main()
