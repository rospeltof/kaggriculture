"""Trace the four neutral opponent-hash mismatches without changing confirm19."""
from copy import deepcopy
import gzip
import hashlib
import json
import os
from pathlib import Path

from kaggle_environments import make
from kaggle_environments.agent import build_agent
from investigar_lider import compact_state

OUT = Path('docs/evidencia/loop_publicos_20260925')


def packed(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def main():
    plan = json.loads((OUT / 'confirm19.noop_probe.plan.json').read_text())
    hs = os.environ['PYTHONHASHSEED']; prefix = OUT / f'confirm19_hash{hs}'
    assert int(hs) in plan['hash_seeds'] and not prefix.with_suffix('.json').exists()
    reports = []
    for opponent in plan['opponents']:
        for seat in (0, 1):
            for repeat in (0, 1):
                traces = [[], []]

                def traced(name, player):
                    spec = plan['sources'][name]
                    assert hashlib.sha256(Path(spec['ruta']).read_bytes()).hexdigest() == spec['sha256']
                    loaded, _ = build_agent(spec['ruta'], {}, 'kaggriculture')

                    def call(obs, config):
                        action = loaded(obs, config); traces[player].append(deepcopy(action)); return action
                    return call

                agents = [None, None]
                agents[seat] = traced('base', seat); agents[1-seat] = traced(opponent, 1-seat)
                env = make('kaggriculture', configuration={'seed': plan['seed'], 'episodeSteps': 720}, debug=False)
                env.run(agents)
                assert len(env.steps) == 720 and [s.status for s in env.steps[-1]] == ['DONE', 'DONE']
                assert all(s.status not in ('ERROR', 'TIMEOUT', 'INVALID') for state in env.steps for s in state)
                assert list(map(len, traces)) == [719, 719]
                row = dict(hash_seed=int(hs), opponent=opponent, seat=seat, repeat=repeat,
                           rewards=[s.reward for s in env.steps[-1]],
                           action_hashes=[hashlib.sha256(b''.join(packed(a) + b'\n' for a in actions)).hexdigest() for actions in traces],
                           state_hashes=[hashlib.sha256(packed(compact_state(state))).hexdigest() for state in env.steps])
                trace_path = Path(str(prefix) + f'.{opponent}.{seat}.{repeat}.actions.json.gz')
                assert not trace_path.exists()
                trace_path.write_bytes(gzip.compress(packed(traces), mtime=0))
                row['trace'] = str(trace_path); reports.append(row)
                print(json.dumps({k: v for k, v in row.items() if k not in ('state_hashes', 'trace')}), flush=True)
    prefix.with_suffix('.json').write_text(json.dumps(dict(plan=plan, runs=reports), indent=2) + '\n')


if __name__ == '__main__':
    main()
