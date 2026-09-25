"""All changed-WLT rival/seed cells in confirm20, representative seat0 and all three policies."""
from collections import Counter
from copy import deepcopy
import gzip
import hashlib
import importlib
import json
from pathlib import Path
import sys

from sonda_fallo_forecast import run

OUT = Path('docs/evidencia/loop_publicos_20260925')


def main():
    meta = json.loads((OUT/'confirm20.meta.json').read_text()); assert meta['state'] == 'complete'
    rows = [json.loads(l) for l in (OUT/'confirm20.jsonl').read_text().splitlines()]
    keyed = {(r['a'], r['b'], r['seed'], r['seat']): r for r in rows}
    arms = ('base','town20','town50')
    cases = {}
    for r in rows:
        if r['a'] != 'base' or r['b'] in ('base', 'noop', *arms) or r['seat'] != 0:
            continue
        cell = (r['b'], r['seed'], 0)
        if any(keyed[n,*cell]['score'] != r['score'] for n in arms[1:]):
            for n in arms:
                assert keyed[n,r['b'],r['seed'],0]['score'] == keyed[n,r['b'],r['seed'],1]['score']
            cases[f"{r['b']}_{r['seed']}"] = cell
    cases = dict(sorted(cases.items()))
    target = OUT/'confirm20.physical.plan.json'; assert not target.exists()
    target.write_text(json.dumps(dict(rule='All changed-WLT opponent/seed cells from closed confirmation; both seats have identical scores, use seat0 per cell. All three policies, including all observed damage. Mechanism only, not independent WLT estimate.', cases=cases, arms=arms, agents=meta['agentes']), indent=2)+'\n')
    engine = importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    original = engine._apply_unit_action; results = []
    for case, (opponent, seed, seat) in cases.items():
        for arm in arms:
            spec = meta['agentes'][arm]; path = Path(spec['ruta']); data = path.read_bytes()
            assert hashlib.sha256(data).hexdigest() == spec['sha256']
            opp = meta['agentes'][opponent]; assert hashlib.sha256(Path(opp['ruta']).read_bytes()).hexdigest() == opp['sha256']
            ns = {}; exec(compile(data, str(path), 'exec'), ns); entry = [v for v in ns.values() if callable(v)][-1]
            digest = hashlib.sha256(); events = []; harvest = Counter(); accepted = Counter()
            def traced(obs, config=None):
                action = entry(obs, config)
                digest.update(json.dumps(action, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()+b'\n')
                return action
            def instrument(farm, private, actor, action, *args, **kwargs):
                frame = sys._getframe(1)
                watch = frame.f_code is engine.interpreter.__code__ and frame.f_locals.get('i') == seat and action and action[0] in ('FEED', 'HARVEST')
                if watch:
                    x, y = farm['farmer'] if actor == 0 else farm['hands'][actor-1]
                    tile = deepcopy(farm['tiles'][y][x]); before = dict(private['inventories'][actor])
                    subject = str(tile.get('animal') or tile.get('crop') or tile.get('kind')) if isinstance(tile, dict) else str(tile)
                result = original(farm, private, actor, action, *args, **kwargs)
                if watch:
                    after = private['inventories'][actor]; new = farm['tiles'][y][x]
                    delta = {k: after.get(k, 0)-before.get(k, 0) for k in set(before)|set(after)}
                    if action[0] == 'HARVEST':
                        gain = {k: q for k, q in delta.items() if q > 0}; harvest.update(gain); ok = bool(gain)
                    else:
                        ok = isinstance(tile, dict) and isinstance(new, dict) and not tile.get('fed_today') and new.get('fed_today')
                        if ok: assert delta.get('WHEAT') == -1
                    if ok: accepted[action[0]+':'+subject] += 1
                    events.append(dict(step=frame.f_locals['step'], actor=actor, xy=[x,y], action=deepcopy(action),
                                       subject=subject, successful=bool(ok), before_tile=tile, before_inventory=before,
                                       inventory_delta={k: v for k, v in delta.items() if v}))
                return result
            engine._apply_unit_action = instrument
            try: env, ledger = run(traced, opp['ruta'], seed, seat)
            finally: engine._apply_unit_action = original
            expected = keyed[arm, opponent, seed, seat]; rewards = [s.reward for s in env.steps[-1]]
            assert rewards == expected['rewards'] and digest.hexdigest() == expected['action_hashes'][seat]
            escapes, additions, daily = [], [], []
            for step in range(719):
                a = env.steps[step][0].observation['farms'][seat]['tiles']; b = env.steps[step+1][0].observation['farms'][seat]['tiles']
                for y in range(10):
                    for x in range(10):
                        old = a[y][x].get('animal') if isinstance(a[y][x], dict) else None
                        new = b[y][x].get('animal') if isinstance(b[y][x], dict) else None
                        if old and old != new: escapes.append(dict(step=step, xy=[x,y], animal=old))
                        if new and old != new: additions.append(dict(step=step, xy=[x,y], animal=new))
            for day in range(30):
                farm = env.steps[day*24][0].observation['farms'][seat]
                daily.append(dict(day=day, money=farm['money'], animals=dict(Counter(t['animal'] for line in farm['tiles'] for t in line if isinstance(t, dict) and t.get('animal')))))
            reports = {k: deepcopy(ns.get(k, {})) for k in ('_TR_REPORT', '_Y_REPORT', '_R85_REPORT')}
            assert not any(v for report in reports.values() for k, v in report.items() if 'error' in k and isinstance(v, (int, float)))
            flows = {}
            for e in ledger:
                if e['player'] == seat:
                    key = e['op']+':'+str(e['item']); q, cash = flows.get(key, [0,0]); flows[key] = [q+1, cash+e['value']]
            row = dict(case=case, arm=arm, opponent=opponent, seed=seed, seat=seat, rewards=rewards,
                       margin=rewards[seat]-rewards[1-seat], action_hash=digest.hexdigest(), reports=reports,
                       accepted=dict(accepted), harvested=dict(harvest), escapes=escapes, additions=additions,
                       edits=deepcopy(ns.get('_TR_EVENTS',[])), daily=daily, flows=flows, shops=env.steps[-1][0].observation['town']['unlocked_shops'],
                       terminal_private=env.steps[-1][seat].observation['private'])
            results.append(row)
            for kind, data in (('ledger', ledger), ('units', events)):
                dest = OUT/f'confirm20.physical.{case}.{arm}.{kind}.jsonl.gz'; assert not dest.exists()
                dest.write_bytes(gzip.compress(('\n'.join(json.dumps(e) for e in data)+'\n').encode(), mtime=0))
            print(json.dumps({k: row[k] for k in ('case','arm','seed','margin','escapes','harvested')}), flush=True)
    (OUT/'confirm20.physical.json').write_text(json.dumps(results, indent=2)+'\n')


if __name__ == '__main__': main()
