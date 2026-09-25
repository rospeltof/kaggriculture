"""Verify the public agent's entry correction without changing its policy."""
from copy import deepcopy
import gzip
import hashlib
import json
from pathlib import Path
import tarfile
import time

from sonda_fallo_forecast import run

OUT = Path('docs/evidencia/loop_publicos_20260925')
ROOT = Path('results/publicos_0400_20260925/leoprovorov_a-song-of-ice-and-fire-fixed-flexible')


def main():
    files = {'named_upstream': ROOT/'main.py', 'fixed_official': ROOT/'main_entry_fixed.py'}
    plan = dict(seeds=[1023000, 1023001], seats=[0, 1],
                opponent='submission/main_publico_arshs3_vq_top3.py',
                purpose='Packaging equivalence, runtime and execution; not a population estimate.',
                files={n: dict(path=str(p), sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for n, p in files.items()})
    p = OUT/'marketshock_smoke.plan.json'
    if p.exists():
        raise FileExistsError(p)
    p.write_text(json.dumps(plan, indent=2)+'\n')
    with tarfile.open(OUT/'marketshock_smoke.sources.tgz', 'x:gz') as tar:
        for name, path in files.items():
            tar.add(path, arcname=name+'.py')
        tar.add(plan['opponent'], arcname='opponent.py')
    baseline, rows = {}, []
    for name, path in files.items():
        for seed in plan['seeds']:
            for seat in (0, 1):
                ns = {}
                exec(compile(path.read_bytes(), str(path), 'exec'), ns)
                entry = ns['agent'] if name == 'named_upstream' else [v for v in ns.values() if callable(v)][-1]
                assert entry.__name__ == 'installed'
                timings = []
                def timed(obs, config=None):
                    start = time.perf_counter()
                    result = entry(obs, config)
                    timings.append((time.perf_counter()-start)*1000)
                    return result
                env, ledger = run(timed, plan['opponent'], seed, seat)
                actions = [[s.action for s in step] for step in env.steps[1:]]
                rewards = [s.reward for s in env.steps[-1]]
                if name == 'named_upstream':
                    baseline[seed, seat] = actions, rewards
                else:
                    assert (actions, rewards) == baseline[seed, seat]
                reports = {k: deepcopy(ns[k]) for k in ('_WR_REPORT', '_ALT_REPORT', '_V92_P_REPORT')}
                assert not any(v for r in reports.values() for k, v in r.items() if 'error' in k and isinstance(v, (int, float)))
                row = dict(arm=name, seed=seed, seat=seat, rewards=rewards,
                           margin=rewards[seat]-rewards[1-seat], max_turn_ms=max(timings), reports=reports,
                           action_hash=hashlib.sha256(json.dumps(actions, sort_keys=True).encode()).hexdigest())
                rows.append(row)
                (OUT/f'marketshock_smoke.{name}.{seed}.{seat}.ledger.jsonl.gz').write_bytes(gzip.compress(('\n'.join(json.dumps(r) for r in ledger)+'\n').encode(), mtime=0))
                print(json.dumps(row), flush=True)
    (OUT/'marketshock_smoke.json').write_text(json.dumps(rows, indent=2)+'\n')


if __name__ == '__main__':
    main()
