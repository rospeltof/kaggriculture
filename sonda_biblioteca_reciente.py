"""Verify exact noops, library activation and runtime; no performance selection."""
import gzip
import hashlib
import json
from pathlib import Path
import tarfile
import time

from construir_biblioteca_reciente import BASE, OUT as AGENTS
from sonda_fallo_forecast import run

OUT = Path('docs/evidencia/loop_publicos_20260925')


def main():
    manifest = json.loads((AGENTS/'manifest.json').read_text())
    arms = {'base': str(BASE), **{n: r['path'] for n, r in manifest.items()}}
    plan = dict(seeds=[1004000, 1272457736], seats=[0, 1],
                opponent='submission/main_publico_arshs3_arsgorynich.py',
                purpose='Known absent-pair and YARN-pair worlds. Activation/noop/runtime only, not held-out competitive evidence.',
                agents={n: dict(path=p, sha256=hashlib.sha256(Path(p).read_bytes()).hexdigest()) for n, p in arms.items()})
    dest = OUT/'library_smoke.plan.json'
    if dest.exists():
        raise FileExistsError(dest)
    dest.write_text(json.dumps(plan, indent=2)+'\n')
    with tarfile.open(OUT/'library_smoke.sources.tgz', 'x:gz') as tar:
        for name, path in arms.items():
            tar.add(path, arcname=name+'.py')
    baseline, results = {}, []
    for seed in plan['seeds']:
        for name, path in arms.items():
            for seat in (0, 1):
                ns = {}
                exec(compile(Path(path).read_bytes(), path, 'exec'), ns)
                entry = [v for v in ns.values() if callable(v)][-1]
                elapsed = []
                def timed(obs, config=None):
                    start = time.perf_counter()
                    action = entry(obs, config)
                    elapsed.append((time.perf_counter()-start)*1000)
                    return action
                env, ledger = run(timed, plan['opponent'], seed, seat)
                actions = [[s.action for s in turn] for turn in env.steps[1:]]
                rewards = [s.reward for s in env.steps[-1]]
                if name == 'base':
                    baseline[seed, seat] = actions, rewards
                if name == 'library_noop' or seed == 1004000:
                    assert (actions, rewards) == baseline[seed, seat]
                assert ns['_V92_P_REPORT']['pred_errors'] == 0
                assert ns['_VQ_REPORT']['errors'] == 0
                row = dict(arm=name, seed=seed, seat=seat, rewards=rewards,
                           changed_action_turns=sum(a[seat] != b[seat] for a, b in zip(actions, baseline[seed, seat][0])),
                           max_turn_ms=max(elapsed), library=ns.get('_LB_REPORT', {}),
                           forecast=ns['_V92_P_REPORT'],
                           action_hash=hashlib.sha256(json.dumps(actions, sort_keys=True).encode()).hexdigest())
                results.append(row)
                ledger_path = OUT/f'library_smoke.{seed}.{name}.{seat}.ledger.jsonl.gz'
                ledger_path.write_bytes(gzip.compress(('\n'.join(json.dumps(r) for r in ledger)+'\n').encode(), mtime=0))
                print(json.dumps(row), flush=True)
    (OUT/'library_smoke.json').write_text(json.dumps(results, indent=2)+'\n')


if __name__ == '__main__':
    main()
