"""Exact engine/cash audit for a preselected recent-episode sample."""
import argparse
from collections import defaultdict
from copy import deepcopy
import gzip
import hashlib
import json
from pathlib import Path

from investigar_lider import compact_state, composition
from sonda_fallo_forecast import run


def main(selection, replay_dir, prefix):
    plan = json.loads(selection.read_text())
    output = Path(str(prefix)+'.json')
    if output.exists():
        raise FileExistsError(output)
    results = []
    for selected in plan['episodes']:
        episode = selected['id']
        path = replay_dir/f'episode-{episode}-replay.json'
        raw = path.read_bytes()
        replay = json.loads(raw)
        names = replay['info']['TeamNames']
        me = names.index('Rospel')
        def tape(player):
            def agent(obs):
                return deepcopy(replay['steps'][int(obs['step'])+1][player]['action'])
            return agent
        env, ledger = run(tape(0), tape(1), replay['info']['seed'], 0)
        assert len(env.steps) == len(replay['steps']) == 720
        assert all(compact_state(a) == compact_state(b) for a, b in zip(env.steps, replay['steps']))
        assert [s.reward for s in env.steps[-1]] == replay['rewards']
        by_player, escapes = [], []
        for player in (me, 1-me):
            totals = defaultdict(lambda: [0, 0])
            for row in ledger:
                if row['player'] == player:
                    sums = totals[(row['op'], row['item'])]
                    sums[0] += 1; sums[1] += row['value']
            by_player.append([dict(op=op, item=item, units=q, cash=c) for (op, item), (q, c) in totals.items()])
            lost = []
            for step in range(719):
                a = replay['steps'][step][0]['observation']['farms'][player]['tiles']
                b = replay['steps'][step+1][0]['observation']['farms'][player]['tiles']
                for y in range(len(a)):
                    for x in range(len(a[y])):
                        if isinstance(a[y][x], dict) and a[y][x].get('animal'):
                            after = b[y][x].get('animal') if isinstance(b[y][x], dict) else None
                            if after != a[y][x]['animal']:
                                lost.append(dict(step=step, x=x, y=y, animal=a[y][x]['animal']))
            escapes.append(lost)
        target = Path(str(prefix)+f'.{episode}.ledger.jsonl.gz')
        target.write_bytes(gzip.compress(('\n'.join(json.dumps(r) for r in ledger)+'\n').encode(), mtime=0))
        snapshots = {}
        for day in (3, 6, 10, 15, 20, 25, 29):
            obs = replay['steps'][day*24][0]['observation']
            snapshots[day] = dict(shops=obs['town']['unlocked_shops'],
                players=[dict(money=obs['farms'][p]['money'], composition=composition(obs['farms'][p])) for p in (me, 1-me)])
        row = dict(id=episode, path=str(path), sha256=hashlib.sha256(raw).hexdigest(),
                   seed=replay['info']['seed'], me=me, opponent=names[1-me],
                   rewards=replay['rewards'], margin=replay['rewards'][me]-replay['rewards'][1-me],
                   statuses=replay['statuses'], states_exact=720, cash_reconciled=True,
                   cashflow=by_player, escapes=escapes, snapshots=snapshots,
                   terminal_private=[replay['steps'][-1][p]['observation']['private'] for p in (me, 1-me)],
                   ledger=str(target), ledger_sha256=hashlib.sha256(target.read_bytes()).hexdigest())
        results.append(row)
        print(episode, row['opponent'], row['margin'], 'exact720, reconciled', 'escapes', list(map(len, escapes)), flush=True)
    output.write_text(json.dumps(results, indent=2, ensure_ascii=False)+'\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--selection', type=Path, required=True)
    parser.add_argument('--replay-dir', type=Path, required=True)
    parser.add_argument('--prefix', type=Path, required=True)
    args = parser.parse_args()
    main(args.selection, args.replay_dir, args.prefix)
