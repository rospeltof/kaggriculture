"""Instrument actual engine unit commits, including PLACE just before midnight."""
import importlib
import json
from pathlib import Path
import sys

from sonda_fallo_forecast import run

AGENTS = Path('results/rebano_adicional_v2_20260925')
OUT = Path('docs/evidencia/loop_publicos_20260925/sheep_space_delivery_v2.json')


def main():
    if OUT.exists():
        raise FileExistsError(OUT)
    engine = importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    original = engine._apply_unit_action
    results = []
    for name in ('forced2', 'forced3', 'forced6'):
        for seat in (0, 1):
            path = AGENTS / (name+'.py')
            ns = {}
            exec(compile(path.read_bytes(), str(path), 'exec'), ns)
            entry = [v for v in ns.values() if callable(v)][-1]
            events = []
            def instrument(farm, private, idx, action, *args, **kwargs):
                # Only the real interpreter invocation, never an agent's clone
                # simulation. Frame locals identify seat and step before market.
                frame = sys._getframe(1)
                actual = frame.f_code is engine.interpreter.__code__
                player = frame.f_locals.get('i') if actual else None
                owned = player == seat and idx in ns['_SG_STATE'].get(seat, {}).get('workers', {})
                before = private['inventories'][idx].get('WOOL', 0) if owned else 0
                result = original(farm, private, idx, action, *args, **kwargs)
                if owned and (action == ['HARVEST'] or action[:2] == ['PLACE', 'WOOL']):
                    after = private['inventories'][idx].get('WOOL', 0)
                    events.append(dict(step=frame.f_locals['step'], actor=idx, action=action,
                                       wool_change=after-before))
                return result
            engine._apply_unit_action = instrument
            try:
                env, ledger = run(entry, 'submission/main_publico_arshs3_arsgorynich.py', 1004000, seat)
            finally:
                engine._apply_unit_action = original
            harvest = sum(r['wool_change'] for r in events if r['action'] == ['HARVEST'])
            placed = -sum(r['wool_change'] for r in events if r['action'][:2] == ['PLACE', 'WOOL'])
            assert harvest == ns['_SG_REPORT']['wool_harvested'] > 0
            assert harvest == placed, (name, seat, harvest, placed)
            results.append(dict(arm=name, seat=seat, harvested=harvest, deposited=placed,
                                rewards=[p.reward for p in env.steps[-1]], events=events))
            print(name, seat, harvest, placed, flush=True)
    OUT.write_text(json.dumps(results, indent=2)+'\n')


if __name__ == '__main__':
    main()
