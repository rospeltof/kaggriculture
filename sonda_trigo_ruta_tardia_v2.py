"""Remaining legal combined diagnostic intervention; v1 archived, no repeated games."""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
import gzip
import hashlib
import importlib
import json
import os
from pathlib import Path
import sys

from auditar_forecast_pareado_real import inspect_env
from sonda_fallo_forecast import run

OUT = Path('docs/evidencia/loop_publicos_20260925')


def packed(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def main():
    assert os.environ.get('PYTHONHASHSEED') == '0'
    control = json.loads((OUT / 'late_escapes_1080001.plan.json').read_text())
    trace = [json.loads(line) for line in gzip.decompress((OUT / 'late_escapes_1080001.trace.jsonl.gz').read_bytes()).splitlines()]
    at = {row['step']: row for row in trace}
    assert at[650]['action']['hands'][1] == ['PICKUP', 'WHEAT', 5]
    assert at[650]['action']['hands'][2] == at[650]['action']['hands'][6] == ['PICKUP', 'WHEAT', 2]
    assert ['SELL', 'WHEAT', 6] in at[649]['action']['market']
    plan = dict(created_at=datetime.now(timezone.utc).isoformat(), control=control, step=649,
                quantity=9, arms=['drop_sale_buy9'],
                reason='At650 three native workers request5+2+2 wheat and receive zero after the sale at649. Execute only the preregistered combined intervention. v1 completed drop_sale, then correctly failed buy9 because it would exceed ten orders; preserve that failure. This combined arm removes one sale before adding one buy, so it has ten. No repeat of the completed control or drop_sale. Not deployable, no population WLT estimate.')
    target = OUT / 'late_route_wheat_probe_v2.plan.json'
    assert not target.exists()
    target.write_text(json.dumps(plan, indent=2) + '\n')
    preflight=[o for o in at[649]['action']['market'] if o[:2]!=['SELL','WHEAT']]
    assert len(preflight)+1==10
    engine = importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    original_unit = engine._apply_unit_action
    results = []
    for arm in plan['arms']:
        source = Path(control['source']['path'])
        assert hashlib.sha256(source.read_bytes()).hexdigest() == control['source']['sha256']
        assert hashlib.sha256(Path(control['opponent']['path']).read_bytes()).hexdigest() == control['opponent']['sha256']
        ns = {}
        exec(compile(source.read_bytes(), str(source), 'exec'), ns)
        entry = [value for value in ns.values() if callable(value)][-1]
        interventions = []; accepted = Counter(); harvest = Counter(); units = []

        def agent(obs, config=None):
            action = entry(obs, config)
            if int(obs['step']) == plan['step']:
                assert action == at[649]['action']
                orders = deepcopy(action['market'])
                if arm in ('drop_sale', 'drop_sale_buy9'):
                    orders = [order for order in orders if order[:2] != ['SELL', 'WHEAT']]
                if arm in ('buy9', 'drop_sale_buy9'):
                    orders.insert(0, ['BUY_PRODUCT', 'WHEAT', plan['quantity']])
                assert len(orders) <= 10
                modified = dict(action, market=orders)
                interventions.append(dict(step=plan['step'], original=deepcopy(action), modified=deepcopy(modified)))
                return modified
            return action

        def unit(farm, private, actor, command, *args, **kwargs):
            frame = sys._getframe(1)
            watch = frame.f_code is engine.interpreter.__code__ and frame.f_locals.get('i') == 0 and command and command[0] in ('FEED', 'HARVEST', 'PICKUP')
            if watch:
                x, y = farm['farmer'] if actor == 0 else farm['hands'][actor-1]
                tile = deepcopy(farm['tiles'][y][x]); before = dict(private['inventories'][actor])
            result = original_unit(farm, private, actor, command, *args, **kwargs)
            if watch:
                after = private['inventories'][actor]
                delta = {k: after.get(k, 0)-before.get(k, 0) for k in set(before) | set(after)}
                subject = (tile.get('animal') or tile.get('crop') or tile.get('kind')) if isinstance(tile, dict) else None
                if command[0] == 'HARVEST':
                    gains = {k: v for k, v in delta.items() if v > 0}; harvest.update(gains); ok = bool(gains)
                elif command[0] == 'FEED':
                    ok = delta.get('WHEAT', 0) < 0
                else:
                    ok = any(v > 0 for v in delta.values())
                if ok: accepted[command[0] + ':' + str(subject)] += 1
                units.append(dict(step=frame.f_locals['step'], actor=actor, xy=[x, y], command=deepcopy(command),
                                  accepted=bool(ok), delta={k: v for k, v in delta.items() if v}))
            return result

        engine._apply_unit_action = unit
        try:
            env, ledger = run(agent, control['opponent']['path'], control['seed'], control['seat'])
        finally:
            engine._apply_unit_action = original_unit
        assert len(interventions) == 1
        assert all(env.steps[t+1][0].action == at[t]['action'] for t in range(624, 649))
        row = dict(arm=arm, interventions=interventions, accepted=dict(accepted), harvested=dict(harvest),
                   at650_pickups=[event for event in units if event['step'] == 650 and event['command'][:2] == ['PICKUP', 'WHEAT']],
                   wheat_receipts_at649=[e for e in ledger if e['player'] == 0 and e['step'] == 649 and e['item'] == 'WHEAT'],
                   **inspect_env(env, ledger, 0))
        for kind, data in [('ledger', ledger), ('units', units)]:
            dest = OUT / f'late_route_wheat_probe_v2.{arm}.{kind}.jsonl.gz'
            assert not dest.exists()
            dest.write_bytes(gzip.compress(b'\n'.join(packed(event) for event in data)+b'\n', mtime=0))
        results.append(row)
        print(json.dumps({k: row[k] for k in ('arm', 'margin', 'escapes', 'harvested', 'at650_pickups')}), flush=True)
    (OUT / 'late_route_wheat_probe_v2.json').write_text(json.dumps(dict(plan=plan, results=results), indent=2) + '\n')


if __name__ == '__main__':
    main()
