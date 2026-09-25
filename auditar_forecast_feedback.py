"""Opposite submitted policy against every frozen rival in a completed recency audit."""
import argparse
from copy import deepcopy
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import time

from auditar_feedback_real import OUT, SOURCES
from auditar_forecast_pareado_real import inspect_env
from sonda_fallo_forecast import run


def main(suffix):
    source = OUT / f'feedback_{suffix}.audit.json'
    audit = json.loads(source.read_text())
    receipts = {row['id']: row for row in json.loads((OUT / f'feedback_{suffix}.fetch.json').read_text())}
    prefix = OUT / f'feedback_{suffix}.opposite'
    target = Path(str(prefix) + '.json')
    assert not target.exists() and not Path(str(prefix) + '.plan.json').exists()
    plan = dict(created_at=datetime.now(timezone.utc).isoformat(), audit=str(source),
                audit_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                episodes=[row['episode'] for row in audit['results']],
                sources={name: dict(path=path, sha256=hashlib.sha256(Path(path).read_bytes()).hexdigest()) for name, path in SOURCES.items()},
                rule='Every completed source-control game in this recency audit, no outcome filter. Opposite submitted policy against frozen rival. Conditional mechanism diagnostic, not reactive WLT.')
    Path(str(prefix) + '.plan.json').write_text(json.dumps(plan, indent=2) + '\n')
    results = []
    for original in audit['results']:
        episode = original['episode']; seat = original['seat']; actual_policy = original['policy']
        counter_policy = 'vq' if actual_policy == 'top3' else 'top3'
        receipt = receipts[episode]; raw = Path(receipt['path']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == original['replay_sha256'] == receipt['sha256']
        replay = json.loads(raw)
        assert original['own_actions_exact'] == 719 and original['states_exact'] == 720
        actual_source = Path(SOURCES[actual_policy])
        assert hashlib.sha256(actual_source.read_bytes()).hexdigest() == original['source_sha256']
        counter_source = Path(SOURCES[counter_policy]); namespace = {}
        counter_bytes = counter_source.read_bytes()
        assert hashlib.sha256(counter_bytes).hexdigest() == plan['sources'][counter_policy]['sha256']
        exec(compile(counter_bytes, str(counter_source), 'exec'), namespace)
        entry = [v for v in namespace.values() if callable(v)][-1]
        elapsed = []

        def opponent(obs):
            return deepcopy(replay['steps'][int(obs['step']) + 1][1-seat]['action'])

        def agent(obs, config=None):
            start = time.perf_counter(); result = entry(obs, config)
            elapsed.append(1000 * (time.perf_counter() - start)); return result

        env, ledger = run(agent, opponent, original['seed'], seat)
        assert hashlib.sha256(counter_source.read_bytes()).hexdigest() == plan['sources'][counter_policy]['sha256']
        reports = {k: deepcopy(namespace.get(k, {})) for k in ('_VQ_REPORT', '_V92_P_REPORT', '_R85_REPORT')}
        assert not any(v for report in reports.values() for k, v in report.items() if 'error' in k and isinstance(v, (int, float)))
        changed = [t for t in range(719) if env.steps[t+1][seat].action != replay['steps'][t+1][seat]['action']]
        first = changed[0] if changed else None
        counter = dict(**inspect_env(env, ledger, seat), max_turn_ms=max(elapsed), reports=reports,
                       source_sha256=hashlib.sha256(counter_source.read_bytes()).hexdigest())
        row = dict(episode=episode, actual_policy=actual_policy, counter_policy=counter_policy,
                   seed=original['seed'], seat=seat, opponent=original['opponent'],
                   changed_action_turns=len(changed), first_difference=first,
                   first_actions=None if first is None else dict(actual=replay['steps'][first+1][seat]['action'],
                                                                counter=env.steps[first+1][seat].action),
                   shops_preserved=all(a[0].observation['town'] == b[0]['observation']['town'] for a, b in zip(env.steps, replay['steps'])),
                   actual_margin=original['margin'], counter=counter,
                   top3_minus_vq_margin_fixed_rival=(counter['margin']-original['margin']) * (1 if counter_policy == 'top3' else -1))
        Path(str(prefix) + f'.{episode}.{counter_policy}.ledger.jsonl.gz').write_bytes(
            gzip.compress(('\n'.join(json.dumps(e) for e in ledger) + '\n').encode(), mtime=0))
        results.append(row)
        print(json.dumps({k: row[k] for k in ('episode', 'actual_policy', 'changed_action_turns', 'shops_preserved', 'top3_minus_vq_margin_fixed_rival')}), flush=True)
    target.write_text(json.dumps(dict(plan=plan, results=results), indent=2) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('suffix'); main(parser.parse_args().suffix)
