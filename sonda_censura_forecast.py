"""Registered loop28 development: observable-sale masks checked against official fills."""
from collections import Counter
from copy import deepcopy
import gzip
import hashlib
import importlib
import json
import os
from pathlib import Path
import sys
import tarfile
import time

from auditar_forecast_pareado_real import inspect_env
from construir_censura_forecast import OUT as AGENTS, EVIDENCE as OUT
from sonda_fallo_forecast import run


def packed(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def main():
    assert os.environ.get('PYTHONHASHSEED') == '0'
    panel = json.loads((OUT / 'close_panel_manifest.json').read_text())
    manifest = json.loads((AGENTS / 'manifest.json').read_text())
    arms = dict(base=panel['controls']['base'], top3=panel['controls']['top3'], **manifest)
    rival = panel['pilot_pool']['public_v7']
    assert hashlib.sha256(Path(rival['path']).read_bytes()).hexdigest() == rival['sha256']
    plan = dict(seeds=[1071000, 1071001, 2111590720], seats=[0, 1],
                expected_games=48, runtime_hash_seed='0', opponent=rival, agents=arms,
                purpose='Registered native/floor observation masks. Reactive mechanics and inference integrity, no reward selection.')
    target = OUT / 'forecast_censor_smoke.json'; plan_path = OUT / 'forecast_censor_smoke.plan.json'
    assert not target.exists() and not plan_path.exists()
    plan_path.write_text(json.dumps(plan, indent=2) + '\n')
    with tarfile.open(OUT / 'forecast_censor_smoke.sources.tgz', 'x:gz') as archive:
        for name, spec in arms.items():
            archive.add(spec['path'], arcname=f'agents/{name}.py')
        archive.add(rival['path'], arcname='opponent.py')
        archive.add(__file__, arcname=Path(__file__).name)
    engine = importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    original_unit = engine._apply_unit_action; original_night = engine._end_of_day
    baseline = {}; results = []
    for seed in plan['seeds']:
        for name, spec in arms.items():
            for seat in plan['seats']:
                path = spec['path']; raw = Path(path).read_bytes()
                assert hashlib.sha256(raw).hexdigest() == spec['sha256']
                ns = {}; exec(compile(raw, path, 'exec'), ns)
                entry = [v for v in ns.values() if callable(v)][-1]
                elapsed = []; snapshots = []; units = []; nights = []; masks = []
                accepted = Counter(); harvest = Counter()

                def agent(obs, config=None):
                    start = time.perf_counter(); action = entry(obs, config)
                    elapsed.append(1000 * (time.perf_counter()-start))
                    snapshots.append(deepcopy(ns['_V9_RACE'][seat]['prev']))
                    if ns.get('_CF_ENABLED') and int(obs['step']) > 0:
                        t = int(obs['step']) - 1
                        masks.append(dict(step=t, visible={item: ns['_CF_MASKS'][seat][t,i] for i,item in enumerate(ns['_V92_P_ITEMS'])}))
                    return action

                def unit(farm, private, actor, command, *args, **kwargs):
                    frame = sys._getframe(1)
                    watch = (frame.f_code is engine.interpreter.__code__ and frame.f_locals.get('i') == seat
                             and command and command[0] in ('FEED', 'CARE', 'HARVEST', 'FERTILIZE', 'PLANT'))
                    if watch:
                        x, y = farm['farmer'] if actor == 0 else farm['hands'][actor-1]
                        tile = deepcopy(farm['tiles'][y][x]); before = dict(private['inventories'][actor])
                        seeds_before = dict(private['seeds'])
                    result = original_unit(farm, private, actor, command, *args, **kwargs)
                    if watch:
                        after = private['inventories'][actor]
                        delta = {k: after.get(k, 0)-before.get(k, 0) for k in set(before)|set(after)}
                        subject = (tile.get('animal') or tile.get('crop') or tile.get('kind')) if isinstance(tile, dict) else None
                        if command[0] == 'HARVEST':
                            gain = {k: v for k, v in delta.items() if v > 0}; harvest.update(gain); ok = bool(gain)
                        elif command[0] == 'FEED': ok = delta.get('WHEAT', 0) < 0
                        elif command[0] == 'FERTILIZE': ok = delta.get('FERTILIZER', 0) < 0
                        elif command[0] == 'PLANT': ok = seeds_before != private['seeds']
                        else:
                            new = farm['tiles'][y][x]
                            ok = isinstance(tile, dict) and isinstance(new, dict) and not tile.get('cared_today') and new.get('cared_today')
                        if ok: accepted[command[0]+':'+str(subject)] += 1
                        units.append(dict(step=frame.f_locals['step'], actor=actor, command=deepcopy(command),
                                          xy=[x,y], accepted=bool(ok), delta={k: v for k, v in delta.items() if v}))
                    return result

                def night(state, env, day):
                    private = deepcopy(state[seat].observation.private); before = Counter(private['shed'])
                    for bag in private['inventories']: before.update(bag)
                    result = original_night(state, env, day)
                    nights.append(dict(step=day*24+23, loss=dict(before-Counter(state[seat].observation.private['shed']))))
                    return result

                engine._apply_unit_action, engine._end_of_day = unit, night
                try: env, ledger = run(agent, rival['path'], seed, seat)
                finally: engine._apply_unit_action, engine._end_of_day = original_unit, original_night
                actions = [[s.action for s in row] for row in env.steps[1:]]
                rewards = [s.reward for s in env.steps[-1]]
                shops = [row[0].observation['town'] for row in env.steps]
                if name in ('base', 'top3'):
                    baseline[name, seed, seat] = dict(actions=deepcopy(actions), rewards=rewards, shops=shops)
                parent = spec.get('behavior_reference', name)
                reference = baseline[parent, seed, seat]
                if name.startswith('censor_noop'):
                    assert actions == reference['actions'] and rewards == reference['rewards']
                fills = Counter((e['step'], e['item']) for e in ledger if e['player'] == seat and e['op'] == 'SELL')
                checked = 0; mismatches = []
                for step, snapshot in enumerate(snapshots):
                    assert snapshot['step'] == step
                    for item in ns['V9_RACE_ITEMS']:
                        checked += 1
                        if int(snapshot['own'].get(item, 0)) != fills[step, item]:
                            mismatches.append(dict(step=step, item=item, projected=snapshot['own'].get(item, 0), accepted=fills[step,item]))
                visible_checks = 0
                increments = Counter((e['step'],e['player'],e['item']) for e in ledger if e['op']=='SELL' and e['value']>1)
                all_fills = Counter((e['step'],e['player'],e['item']) for e in ledger if e['op']=='SELL')
                for mask in masks:
                    for item, visible in mask['visible'].items():
                        if visible and spec['config']['mode']=='floor':
                            t=mask['step'];visible_checks += 1
                            assert sum(increments[t,p,item] for p in (0,1))==sum(all_fills[t,p,item] for p in (0,1)),(name,seed,seat,mask,item)
                if ns.get('_CF_ENABLED'):assert len(masks)==718
                reports = {k: deepcopy(ns.get(k, {})) for k in ('_CF_REPORT','_VQ_REPORT','_V92_P_REPORT','_V9_RACE_REPORT','_R127_REPORT')}
                assert not any(v for d in reports.values() for k,v in d.items() if 'error' in k and isinstance(v,(int,float)))
                result = dict(arm=name, seed=seed, seat=seat, source_sha256=spec['sha256'],
                              action_hashes=[hashlib.sha256(b'\n'.join(packed(a[p]) for a in actions)+b'\n').hexdigest() for p in (0,1)],
                              max_turn_ms=max(elapsed), reports=reports, edits=deepcopy(ns.get('_CF_EVENTS', [])), mask_item_checks=5*len(masks), visible_market_checks=visible_checks,
                              own_sales_checks=checked, own_sales_mismatches=mismatches,
                              changed_own_turns=sum(a[seat] != b[seat] for a,b in zip(actions,reference['actions'])),
                              changed_rival_turns=sum(a[1-seat] != b[1-seat] for a,b in zip(actions,reference['actions'])),
                              same_shops=shops == reference['shops'], accepted=dict(accepted), harvested=dict(harvest),
                              nights=nights, **inspect_env(env,ledger,seat))
                for kind, data in [('ledger',ledger),('units',units),('snapshots',snapshots),('masks',masks)]:
                    (OUT / f'forecast_censor_smoke.{seed}.{name}.{seat}.{kind}.jsonl.gz').write_bytes(
                        gzip.compress(b'\n'.join(packed(r) for r in data)+b'\n',mtime=0))
                results.append(result)
                print(json.dumps({k:result[k] for k in ('arm','seed','seat','changed_own_turns','same_shops','max_turn_ms')}),flush=True)
    assert len(results) == 48
    target.write_text(json.dumps(dict(plan=plan,results=results),indent=2)+'\n')


if __name__ == '__main__':
    main()
