"""Funding quotes, actual purchases and animal care for the preregistered repair."""
from collections import Counter
from copy import deepcopy
import gzip
import hashlib
import importlib
import json
from pathlib import Path
import sys
import tarfile
import time

from construir_caja_alimento import BASE, OUT as AGENTS, EVIDENCE as OUT
from sonda_fallo_forecast import run

TAG = 'cash_smoke'


def main():
    manifest = json.loads((AGENTS/'manifest.json').read_text())
    arms = {'base': str(BASE), 'legacy': 'results/vacas_tempranas_20260925/cow_d3_y1_m100.py',
            **{n: r['path'] for n, r in manifest.items()}}
    cases = [dict(seed=1018001, opponent='results/publicos/arsgorynich_kaggriculture-v40-challenger/main.py'),
             dict(seed=1018011, opponent='results/publicos/wzhengbiao_kaggriculture-hybu-submit/main.py'),
             dict(seed=1033000, opponent='submission/main_publico_arshs3_arsgorynich.py')]
    plan = dict(cases=cases, seats=[0, 1], purpose='Fixed mechanism diagnostics, not reward selection.',
                agents={n: dict(path=p, sha256=hashlib.sha256(Path(p).read_bytes()).hexdigest()) for n, p in arms.items()})
    dest = OUT/(TAG+'.plan.json')
    if dest.exists():
        raise FileExistsError(dest)
    dest.write_text(json.dumps(plan, indent=2)+'\n')
    with tarfile.open(OUT/(TAG+'.sources.tgz'), 'x:gz') as tar:
        for name, path in arms.items():
            tar.add(path, arcname=name+'.py')
        for case in cases:
            tar.add(case['opponent'], arcname=f'opponent_{case["seed"]}.py')
    engine = importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    original_unit = engine._apply_unit_action
    baseline, results = {}, []
    for case in cases:
        seed = case['seed']
        for name, path in arms.items():
            for seat in plan['seats']:
                ns = {}
                exec(compile(Path(path).read_bytes(), path, 'exec'), ns)
                entry = [v for v in ns.values() if callable(v)][-1]
                elapsed, events, attempts = [], [], []
                def timed(obs, config=None):
                    start = time.perf_counter()
                    result = entry(obs, config)
                    elapsed.append((time.perf_counter()-start)*1000)
                    for order in result.get('market', []):
                        if order and order[0] in ('BUY_ANIMAL', 'BUY_PRODUCT'):
                            attempts.append(dict(step=int(obs['step']), order=list(order),
                                                 money=obs['farms'][seat]['money'],
                                                 shed=deepcopy(obs['private']['shed'])))
                    return result
                def instrument(farm, private, actor, action, *args, **kwargs):
                    frame = sys._getframe(1)
                    actual = frame.f_code is engine.interpreter.__code__ and frame.f_locals.get('i') == seat
                    watched = actual and action and action[0] in ('FEED', 'PLACE', 'HARVEST')
                    if watched:
                        pos = farm['farmer'] if actor == 0 else farm['hands'][actor-1]
                        x, y = pos
                        tile = deepcopy(farm['tiles'][y][x])
                        before = dict(private['inventories'][actor])
                    result = original_unit(farm, private, actor, action, *args, **kwargs)
                    if watched:
                        after = private['inventories'][actor]
                        delta = {k: after.get(k, 0)-before.get(k, 0) for k in set(before)|set(after)}
                        newtile = farm['tiles'][y][x]
                        fed = bool(isinstance(tile, dict) and isinstance(newtile, dict) and
                                   not tile.get('fed_today') and newtile.get('fed_today'))
                        events.append(dict(step=frame.f_locals['step'], actor=actor, xy=list(pos),
                                           action=deepcopy(action), tile_before=tile,
                                           wheat_before=before.get('WHEAT', 0), fed=fed,
                                           inventory_delta={k: q for k, q in delta.items() if q}))
                    return result
                engine._apply_unit_action = instrument
                try:
                    env, ledger = run(timed, case['opponent'], seed, seat)
                finally:
                    engine._apply_unit_action = original_unit
                actions = [[s.action for s in turn] for turn in env.steps[1:]]
                rewards = [s.reward for s in env.steps[-1]]
                key = seed, seat
                if name == 'base':
                    baseline[key] = actions, rewards
                if name == 'cash_noop':
                    assert (actions, rewards) == baseline[key]
                reports = {k: deepcopy(ns.get(k, {})) for k in ('_CF_REPORT', '_EC_REPORT', '_Y_REPORT', '_V92_P_REPORT', '_VQ_REPORT')}
                assert not any(v for report in reports.values() for k, v in report.items() if 'error' in k and isinstance(v, (int, float)))
                additions, escapes = [], []
                for step in range(719):
                    a = env.steps[step][0].observation.farms[seat].tiles
                    b = env.steps[step+1][0].observation.farms[seat].tiles
                    for y in range(10):
                        for x in range(10):
                            old = a[y][x].get('animal') if isinstance(a[y][x], dict) else None
                            new = b[y][x].get('animal') if isinstance(b[y][x], dict) else None
                            if new and old != new:
                                additions.append(dict(step=step, xy=[x,y], animal=new))
                            if old and old != new:
                                escapes.append(dict(step=step, xy=[x,y], animal=old))
                flows = {}
                for e in ledger:
                    if e['player'] == seat:
                        k = e['op']+':'+str(e['item']); q, cash = flows.get(k, [0, 0])
                        flows[k] = [q+1, cash+e['value']]
                buys191 = [e for e in ledger if e['player'] == seat and e['step'] == 191 and e['op'] == 'BUY_PRODUCT' and e['item'] == 'WHEAT']
                row = dict(seed=seed, opponent=case['opponent'], arm=name, seat=seat, rewards=rewards,
                           reports=reports, attempts=attempts, flows=flows, additions=additions, escapes=escapes,
                           wheat_bought_191=len(buys191), wheat_cost_191=sum(e['value'] for e in buys191),
                           feed_attempts=sum(e['action'] == ['FEED'] for e in events),
                           feed_accepted=sum(e['action'] == ['FEED'] and e['fed'] for e in events),
                           terminal_private=env.steps[-1][seat].observation.private,
                           shops=env.steps[-1][0].observation.town.unlocked_shops,
                           max_turn_ms=max(elapsed), action_hash=hashlib.sha256(json.dumps(actions, sort_keys=True).encode()).hexdigest(),
                           changed_action_turns=sum(a[seat] != b[seat] for a, b in zip(actions, baseline[key][0])))
                results.append(row)
                for kind, data in (('ledger', ledger), ('units', events)):
                    (OUT/f'{TAG}.{seed}.{name}.{seat}.{kind}.jsonl.gz').write_bytes(gzip.compress(('\n'.join(json.dumps(e) for e in data)+'\n').encode(), mtime=0))
                print(json.dumps({k: row[k] for k in ('seed','arm','seat','rewards','max_turn_ms','changed_action_turns','wheat_bought_191','feed_accepted','escapes')}), flush=True)
    (OUT/(TAG+'.json')).write_text(json.dumps(results, indent=2)+'\n')


if __name__ == '__main__':
    main()
