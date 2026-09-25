"""Explain the shared late escapes seen in loop31 development; one exact control."""
from copy import deepcopy
from datetime import datetime, timezone
import gzip
import hashlib
import json
import os
from pathlib import Path

from sonda_fallo_forecast import run

OUT = Path('docs/evidencia/loop_publicos_20260925')


def packed(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def main():
    assert os.environ.get('PYTHONHASHSEED') == '0'
    development = json.loads((OUT / 'close_queue_smoke.json').read_text())
    control = next(row for row in development['results'] if (row['arm'], row['seed'], row['seat']) == ('base', 1080001, 0))
    plan = dict(created_at=datetime.now(timezone.utc).isoformat(), seed=1080001, seat=0,
                reason='Five own animals escape at695 in every one of the eight loop31 development arms. Reproduce the base once; explain the existing event before considering a change. No new policy or causal benefit claim.',
                source=development['plan']['agents']['base'], opponent=development['plan']['opponent'],
                expected_rewards=control['rewards'], expected_hashes=control['action_hashes'])
    target = OUT / 'late_escapes_1080001.plan.json'
    assert not target.exists()
    target.write_text(json.dumps(plan, indent=2) + '\n')
    for spec in (plan['source'], plan['opponent']):
        assert hashlib.sha256(Path(spec['path']).read_bytes()).hexdigest() == spec['sha256']
    namespace = {}
    source = Path(plan['source']['path'])
    exec(compile(source.read_bytes(), str(source), 'exec'), namespace)
    entry = [value for value in namespace.values() if callable(value)][-1]
    traces = []

    def agent(obs, config=None):
        step = int(obs['step'])
        before = deepcopy(namespace.get('_R85_REPORT', {}))
        action = entry(obs, config)
        if step >= 624:
            traces.append(dict(step=step, observation=deepcopy(obs), action=deepcopy(action),
                               feed_skips_before=before.get('feed_skips', 0),
                               feed_skips_after=namespace.get('_R85_REPORT', {}).get('feed_skips', 0)))
        return action

    env, ledger = run(agent, plan['opponent']['path'], plan['seed'], plan['seat'])
    rewards = [state.reward for state in env.steps[-1]]
    hashes = [hashlib.sha256(b'\n'.join(packed(row[p].action) for row in env.steps[1:])+b'\n').hexdigest() for p in (0, 1)]
    assert rewards == control['rewards'] and hashes == control['action_hashes']
    for kind, data in [('trace', traces), ('ledger', ledger)]:
        dest = OUT / f'late_escapes_1080001.{kind}.jsonl.gz'
        assert not dest.exists()
        dest.write_bytes(gzip.compress(b'\n'.join(packed(row) for row in data)+b'\n', mtime=0))
    result = dict(passed=True, full_games=1, exact_both_action_hashes=hashes, rewards=rewards,
                  actions_traced=len(traces), source_sha256=plan['source']['sha256'],
                  escapes=control['escapes'], reports={key: deepcopy(namespace.get(key, {})) for key in ('_R85_REPORT', '_V233_REPORT', '_VQ_REPORT')})
    (OUT / 'late_escapes_1080001.control.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
