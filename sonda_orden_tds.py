"""Isolate Python hash ordering from policy changes in an inert paired cell."""
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


def main():
    label = 'tds_hash_'+os.environ['PYTHONHASHSEED']
    path = OUT / (label+'.json')
    if path.exists():
        raise FileExistsError(path)
    reports, states = [], []
    for name, own in (
        ('base', 'submission/main_publico_arshs3_vq_top3.py'),
        ('infill8_d16', 'results/tomate_relleno_v4_20260925/infill8_d16.py'),
    ):
        traces = [[], []]
        def traced(source, seat):
            agent, _ = build_agent(source, {}, 'kaggriculture')
            def call(obs, config):
                action = agent(obs, config)
                traces[seat].append(deepcopy(action))
                return action
            return call
        env = make('kaggriculture', configuration={'seed': 1010007, 'episodeSteps': 720}, debug=False)
        env.run([traced(own, 0), traced('submission/main_publico_tds_tetsutani.py', 1)])
        assert len(env.steps) == 720 and [r.status for r in env.steps[-1]] == ['DONE', 'DONE']
        hashes = [hashlib.sha256(b''.join(json.dumps(a, sort_keys=True, separators=(',', ':')).encode()+b'\n' for a in actions)).hexdigest() for actions in traces]
        reports.append(dict(arm=name, rewards=[r.reward for r in env.steps[-1]], hashes=hashes))
        (OUT / (label+'.'+name+'.actions.json.gz')).write_bytes(gzip.compress(json.dumps(traces).encode(), mtime=0))
        states.append([compact_state(row) for row in env.steps])
    result = dict(hash_seed=os.environ['PYTHONHASHSEED'], seed=1010007, seat=0, reports=reports,
                  same_states=states[0] == states[1])
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
