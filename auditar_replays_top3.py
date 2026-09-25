"""Exact accepted transactions from the four replays selected by recency."""
from collections import defaultdict
from copy import deepcopy
import gzip
import json
from pathlib import Path

from investigar_lider import compact_state
from sonda_fallo_forecast import run

OUT = Path('docs/evidencia/loop_publicos_20260925')


def main():
    summaries = json.loads((OUT / 'top3_real_diagnostics_0234.json').read_text())
    output = OUT / 'top3_accepted_transactions_0234.json'
    if output.exists():
        raise FileExistsError(output)
    for row in summaries:
        replay = json.loads(Path(row['path']).read_text())
        def tape(player):
            def agent(obs):
                return deepcopy(replay['steps'][int(obs['step']) + 1][player]['action'])
            return agent
        env, ledger = run(tape(0), tape(1), row['seed'], 0)
        assert len(env.steps) == len(replay['steps']) == 720
        assert all(compact_state(a) == compact_state(b) for a, b in zip(env.steps, replay['steps']))
        path = OUT / f"top3_{row['id']}.ledger.jsonl.gz"
        if path.exists():
            raise FileExistsError(path)
        path.write_bytes(gzip.compress(('\n'.join(json.dumps(r) for r in ledger)+'\n').encode(), mtime=0))
        row['states_exact'] = 720
        row['cashflow'] = []
        for player in (row['me'], 1-row['me']):
            by = defaultdict(lambda: [0, 0])
            for event in ledger:
                if event['player'] == player:
                    key = event['op'], event['item']
                    by[key][0] += 1
                    by[key][1] += event['value']
            row['cashflow'].append([dict(op=op, item=item, units=units, cash=cash)
                                    for (op, item), (units, cash) in by.items()])
        print(row['id'], row['opponent'], '720 exact states, cash reconciled', flush=True)
    output.write_text(json.dumps(summaries, indent=2, ensure_ascii=False)+'\n')


if __name__ == '__main__':
    main()
