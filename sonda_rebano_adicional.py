"""Known-world development; test execution and parent coexistence, not strength."""
from copy import deepcopy
import gzip
import hashlib
import json
from pathlib import Path
import tarfile
import time

from construir_rebano_adicional import BASE, OUT as AGENTS
from sonda_fallo_forecast import run

OUT = Path('docs/evidencia/loop_publicos_20260925')
TAG = 'sheep_space_smoke_v4'


def main():
    variants = json.loads((AGENTS / 'manifest.json').read_text())
    arms = {'base': str(BASE), **{n: r['path'] for n, r in variants.items()}}
    for name, parent, extra in (
        ('noop', 'sheep2_d12', '_SG_SIZE=0'),
        ('forced2', 'sheep2_d12', '_SG_MARGIN=-1e12'),
        ('forced3', 'sheep3_d12', '_SG_MARGIN=-1e12'),
        ('forced6', 'sheep6_d14', '_SG_MARGIN=-1e12'),
    ):
        path = AGENTS / (name+'.py')
        raw = Path(arms[parent]).read_bytes()+('\n# Development only; never submit.\n'+extra+'\n').encode()
        if path.exists():
            assert path.read_bytes() == raw
        else:
            path.write_bytes(raw)
        arms[name] = str(path)
    plan = dict(seed=1004000, seats=[0, 1], candidate_version=3, source_archive=TAG+'.sources.tgz', opponent='submission/main_publico_arshs3_arsgorynich.py',
                purpose='Known sheep SE world. Execution, cash reconciliation, noop; never performance selection.',
                agents={n: dict(path=p, sha256=hashlib.sha256(Path(p).read_bytes()).hexdigest()) for n, p in arms.items()})
    path = OUT / (TAG+'.plan.json')
    if path.exists():
        raise FileExistsError(path)
    path.write_text(json.dumps(plan, indent=2)+'\n')
    source_archive = OUT / (TAG+'.sources.tgz')
    if source_archive.exists():
        with tarfile.open(source_archive, 'r:gz') as tar:
            for name, path in arms.items():
                assert tar.extractfile(name+'.py').read() == Path(path).read_bytes()
    else:
        with tarfile.open(source_archive, 'x:gz') as tar:
            for name, path in arms.items():
                tar.add(path, arcname=name+'.py')
    baseline, results = {}, []
    for name, path in arms.items():
        for seat in plan['seats']:
            ns = {}
            exec(compile(Path(path).read_bytes(), path, 'exec'), ns)
            entry = [v for v in ns.values() if callable(v)][-1]
            times = []
            cargo_trace = []
            def timed(obs, config=None):
                begin = time.perf_counter()
                result = entry(obs, config)
                times.append((time.perf_counter()-begin)*1000)
                st = ns.get('_SG_STATE', {}).get(seat, {})
                for actor in st.get('workers', {}):
                    command = result['hands'][actor-1]
                    inv = obs['private']['inventories'][actor]
                    if command[:2] == ['PLACE', 'WOOL'] or (int(obs['step']) % 24 == 23 and inv.get('WOOL', 0)):
                        cargo_trace.append(dict(step=int(obs['step']), actor=actor, command=deepcopy(command), wool=inv.get('WOOL', 0)))
                return result
            env, ledger = run(timed, plan['opponent'], plan['seed'], seat)
            actions = [[s.action for s in turn] for turn in env.steps[1:]]
            rewards = [s.reward for s in env.steps[-1]]
            if name == 'base':
                baseline[seat] = actions, rewards
            if name == 'noop':
                assert (actions, rewards) == baseline[seat]
            stats = deepcopy(ns.get('_SG_REPORT', {}))
            parent = {key: deepcopy(ns.get(key, {})) for key in ('_V233_REPORT', '_R51_INPUT_REPORT', '_CA_REPORT', '_V92_P_REPORT')}
            errors = {key: {k: v for k, v in report.items() if 'error' in k and isinstance(v, (int, float)) and v}
                      for key, report in parent.items()}
            assert not any(errors.values()), errors
            assert stats.get('hire_shortfalls', 0) == stats.get('purchase_shortfalls', 0) == 0, stats
            escapes, hungry_days, max_sheep = [], 0, 0
            for t, states in enumerate(env.steps):
                tiles = states[0].observation.farms[seat].tiles
                count = 0
                for y in (7, 8):
                    for x in range(5, 8):
                        tile = tiles[y][x]
                        if isinstance(tile, dict) and tile.get('animal') == 'SHEEP':
                            count += 1
                            if t % 24 == 0:
                                hungry_days += tile.get('consecutive_unfed', 0) > 0
                            if t < 719:
                                after = env.steps[t+1][0].observation.farms[seat].tiles[y][x]
                                if not isinstance(after, dict) or after.get('animal') != 'SHEEP':
                                    escapes.append(dict(step=t, xy=[x, y]))
                max_sheep = max(max_sheep, count)
            last = ns.get('_SG_STATE', {}).get(seat, {}).get('last_yield_day')
            early_escapes = [r for r in escapes if r['step']//24 < last] if last is not None else []
            # PLACE at hour23 precedes the reset of hands, so use its requested
            # quantity as diagnostic only; other drops are confirmed by inventory.
            confirmed_drop = sum(r['wool']-env.steps[r['step']+1][seat].observation.private.inventories[r['actor']].get('WOOL', 0)
                for r in cargo_trace if r['command'][:2] == ['PLACE', 'WOOL'] and r['step'] % 24 != 23)
            results.append(dict(arm=name, seat=seat, rewards=rewards,
                changed_action_turns=sum(a[seat] != b[seat] for a, b in zip(actions, baseline[seat][0])),
                report=stats, parent=parent, max_sheep=max_sheep, hungry_animal_days=hungry_days,
                escapes=escapes, early_escapes=early_escapes, max_turn_ms=max(times),
                wool_drop_confirmed_before_midnight=confirmed_drop, cargo_trace=cargo_trace,
                action_hash=hashlib.sha256(json.dumps(actions, sort_keys=True).encode()).hexdigest(),
                wool_sold=sum(r['player'] == seat and r['op'] == 'SELL' and r['item'] == 'WOOL' for r in ledger)))
            ledger_path = OUT / f'{TAG}.{name}.{seat}.ledger.jsonl.gz'
            ledger_path.write_bytes(gzip.compress(('\n'.join(json.dumps(r) for r in ledger)+'\n').encode(), mtime=0))
            print(json.dumps(results[-1]), flush=True)
    (OUT / (TAG+'.json')).write_text(json.dumps(results, indent=2)+'\n')


if __name__ == '__main__':
    main()
