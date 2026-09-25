"""Check the transformation control and runtime before the registered tournament."""
import hashlib
import json
from pathlib import Path
import tarfile
import time

from construir_patrones_adaptativos import BASE, OUT as AGENTS
from sonda_fallo_forecast import run

OUT = Path('docs/evidencia/loop_publicos_20260925')


def main():
    manifest = json.loads((AGENTS / 'manifest.json').read_text())
    arms = {'base': str(BASE), **{n: r['path'] for n, r in manifest.items()}}
    plan = dict(seed=1012000, seats=[0, 1], opponent='submission/main_publico_arshs3_arsgorynich.py',
                purpose='Development, transformation control, no performance selection',
                agents={n: dict(path=p, sha256=hashlib.sha256(Path(p).read_bytes()).hexdigest()) for n, p in arms.items()})
    dest = OUT / 'patterns_smoke.plan.json'
    if dest.exists():
        raise FileExistsError(dest)
    dest.write_text(json.dumps(plan, indent=2) + '\n')
    with tarfile.open(OUT / 'patterns_smoke.sources.tgz', 'x:gz') as tar:
        for name, path in arms.items():
            tar.add(path, arcname=name+'.py')
    results, baseline = [], {}
    for name, path in arms.items():
        for seat in plan['seats']:
            ns = {}
            exec(compile(Path(path).read_bytes(), path, 'exec'), ns)
            entry = [v for v in ns.values() if callable(v)][-1]
            times = []
            def timed(obs, config=None):
                started = time.perf_counter()
                result = entry(obs, config)
                times.append((time.perf_counter()-started)*1000)
                return result
            env, ledger = run(timed, plan['opponent'], plan['seed'], seat)
            actions = [[p.action for p in states] for states in env.steps[1:]]
            rewards = [p.reward for p in env.steps[-1]]
            if name == 'base':
                baseline[seat] = actions, rewards
            own_changes = sum(a[seat] != b[seat] for a, b in zip(actions, baseline[seat][0]))
            if name == 'transform_noop':
                assert actions == baseline[seat][0] and rewards == baseline[seat][1]
            assert ns['_V92_P_REPORT']['pred_errors'] == 0
            result = dict(arm=name, seat=seat, rewards=rewards, changed_action_turns=own_changes,
                          max_turn_ms=max(times), mean_turn_ms=sum(times)/len(times),
                          patterns=ns.get('_PM_REPORT',{}), forecast=ns['_V92_P_REPORT'],
                          action_hash=hashlib.sha256(json.dumps(actions,sort_keys=True).encode()).hexdigest(),
                          ledger_operations=len(ledger))
            results.append(result)
            print(json.dumps(result), flush=True)
    (OUT / 'patterns_smoke.json').write_text(json.dumps(results, indent=2) + '\n')


if __name__ == '__main__':
    main()
