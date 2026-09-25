"""Attribute private-stock loss during the real nightly transfer."""
from collections import Counter
from copy import deepcopy
import importlib
import json
from pathlib import Path

from investigar_lider import compact_state
from sonda_fallo_forecast import run

OUT = Path('docs/evidencia/loop_publicos_20260925/c0nrad_inventory_audit.json')


def main():
    if OUT.exists():
        raise FileExistsError(OUT)
    replay = json.loads(Path('replays/top3_current/episode-113107623-replay.json').read_text())
    engine = importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    original = engine._end_of_day
    losses = []
    def totals(private):
        result = Counter(private['shed'])
        for inventory in private['inventories']:
            result.update(inventory)
        return result
    def midnight(state, env, day):
        before = [totals(s.observation.private) for s in state]
        private = [deepcopy(s.observation.private) for s in state]
        prices = dict(state[0].observation.market.prices)
        result = original(state, env, day)
        for player, s in enumerate(state):
            after = totals(s.observation.private)
            lost = before[player]-after
            if lost:
                losses.append(dict(step=day*24+23, player=player, lost=dict(lost),
                                   before_total=sum(before[player].values()),
                                   after_total=sum(after.values()), prices=prices, before_private=private[player]))
        return result
    def tape(player):
        def agent(obs):
            return deepcopy(replay['steps'][int(obs['step'])+1][player]['action'])
        return agent
    engine._end_of_day = midnight
    try:
        env, ledger = run(tape(0), tape(1), replay['info']['seed'], 0)
    finally:
        engine._end_of_day = original
    assert all(compact_state(a) == compact_state(b) for a, b in zip(env.steps, replay['steps']))
    summary = []
    for player, name in enumerate(replay['info']['TeamNames']):
        total = Counter()
        for row in losses:
            if row['player'] == player:
                total.update(row['lost'])
        summary.append(dict(player=player, name=name, units_lost=dict(total)))
    OUT.write_text(json.dumps(dict(episode=113107623, states_exact=720, cash_reconciled=True,
                                   note='Private inventory difference immediately around real _end_of_day. Prices shown are diagnostic quotes, not counterfactual sale revenue.',
                                   summary=summary, losses=losses), indent=2)+'\n')
    print(json.dumps(summary, indent=2))
    for row in losses:
        print(row['step'], row['player'], row['lost'], row['before_total'], row['after_total'])


if __name__ == '__main__':
    main()
