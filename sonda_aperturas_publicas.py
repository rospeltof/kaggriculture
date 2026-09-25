"""Audit opening effects through actual unit and market commits."""
from copy import deepcopy
import gzip
import hashlib
import importlib
import json
from pathlib import Path
import sys
import tarfile
import time

from construir_aperturas_publicas import BASE, OUT as AGENTS
from sonda_fallo_forecast import run

OUT = Path('docs/evidencia/loop_publicos_20260925')


def main():
    manifest = json.loads((AGENTS/'manifest.json').read_text())
    arms = {'base': str(BASE), **{n: r['path'] for n, r in manifest.items()}}
    plan = dict(seed=1024000, seats=[0, 1], opponent='submission/main_publico_arshs3_arsgorynich.py',
                purpose='Opening mechanics, actual crops/animals and exact noop. No reward-based selection.',
                agents={n: dict(path=p, sha256=hashlib.sha256(Path(p).read_bytes()).hexdigest()) for n, p in arms.items()})
    dest = OUT/'opening_smoke.plan.json'
    if dest.exists():
        raise FileExistsError(dest)
    dest.write_text(json.dumps(plan, indent=2)+'\n')
    with tarfile.open(OUT/'opening_smoke.sources.tgz', 'x:gz') as tar:
        for name, path in arms.items():
            tar.add(path, arcname=name+'.py')
    engine = importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    original = engine._apply_unit_action
    baseline, results = {}, []
    for name, path in arms.items():
        for seat in (0, 1):
            ns = {}
            exec(compile(Path(path).read_bytes(), path, 'exec'), ns)
            entry = [v for v in ns.values() if callable(v)][-1]
            elapsed, events = [], []
            def timed(obs, config=None):
                start = time.perf_counter()
                result = entry(obs, config)
                elapsed.append((time.perf_counter()-start)*1000)
                return result
            def instrument(farm, private, idx, action, *args, **kwargs):
                frame = sys._getframe(1)
                owned = frame.f_code is engine.interpreter.__code__ and frame.f_locals.get('i') == seat
                xy = tuple(farm['farmer'] if idx == 0 else farm['hands'][idx-1])
                watched = owned and xy in ((2, 4), (4, 4))
                before = dict(private['inventories'][idx]) if watched else {}
                tile = deepcopy(farm['tiles'][xy[1]][xy[0]]) if watched else None
                result = original(farm, private, idx, action, *args, **kwargs)
                if watched and action[0] in ('PLANT', 'HARVEST', 'PLACE', 'BUILD_PASTURE'):
                    after = private['inventories'][idx]
                    delta = {k: after.get(k, 0)-before.get(k, 0) for k in set(before)|set(after)}
                    events.append(dict(step=frame.f_locals['step'], actor=idx, xy=xy, action=deepcopy(action),
                                       inventory_delta={k: v for k, v in delta.items() if v},
                                       tile_before=tile, tile_after=deepcopy(farm['tiles'][xy[1]][xy[0]])))
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
            if name == 'open_noop':
                assert (actions, rewards) == baseline[seat]
            reports = {k: deepcopy(ns.get(k, {})) for k in ('_ALT_REPORT', '_WR_REPORT', '_V92_P_REPORT', '_VQ_REPORT')}
            assert not any(v for report in reports.values() for k, v in report.items() if 'error' in k and isinstance(v, (int, float)))
            escapes = []
            for step in range(719):
                a = env.steps[step][0].observation.farms[seat].tiles
                b = env.steps[step+1][0].observation.farms[seat].tiles
                for y in range(10):
                    for x in range(10):
                        if isinstance(a[y][x], dict) and a[y][x].get('animal'):
                            after = b[y][x].get('animal') if isinstance(b[y][x], dict) else None
                            if after != a[y][x]['animal']:
                                escapes.append(dict(step=step, xy=[x,y], animal=a[y][x]['animal']))
            sales = {}
            for r in ledger:
                if r['player'] == seat and r['op'] == 'SELL':
                    q, cash = sales.get(r['item'], [0, 0]); sales[r['item']] = [q+1, cash+r['value']]
            row = dict(arm=name, seat=seat, rewards=rewards, reports=reports, sales=sales,
                       initial_animal_buys=[e for e in ledger if e['player'] == seat and e['op'] == 'BUY_ANIMAL' and e['step'] < 24],
                       watched_harvests=[e for e in events if e['action'] == ['HARVEST'] and e['inventory_delta']],
                       terminal_private=env.steps[-1][seat].observation.private,
                       shops=env.steps[-1][0].observation.town.unlocked_shops, escapes=escapes,
                       max_turn_ms=max(elapsed), action_hash=hashlib.sha256(json.dumps(actions, sort_keys=True).encode()).hexdigest(),
                       changed_action_turns=sum(a[seat] != b[seat] for a, b in zip(actions, baseline[seat][0])))
            results.append(row)
            for kind, data in (('ledger', ledger), ('units', events)):
                (OUT/f'opening_smoke.{name}.{seat}.{kind}.jsonl.gz').write_bytes(gzip.compress(('\n'.join(json.dumps(e) for e in data)+'\n').encode(), mtime=0))
            print(json.dumps({k: row[k] for k in ('arm','seat','rewards','max_turn_ms','changed_action_turns','reports','escapes')}), flush=True)
    (OUT/'opening_smoke.json').write_text(json.dumps(results, indent=2)+'\n')


if __name__ == '__main__':
    main()
