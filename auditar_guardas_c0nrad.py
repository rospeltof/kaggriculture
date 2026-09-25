"""Compare native overflow predictions with the engine's live inventory order."""
from collections import Counter
from copy import deepcopy
import hashlib
import importlib
import json
from pathlib import Path

from investigar_lider import compact_state
from sonda_fallo_forecast import run

OUT = Path('docs/evidencia/loop_publicos_20260925/c0nrad_guard_audit.json')
SOURCE = Path('submission/main_publico_arshs3_vq_top3.py')
TARGETS = (527, 575, 623, 647, 671)


def main():
    if OUT.exists():
        raise FileExistsError(OUT)
    replay = json.loads(Path('replays/top3_current/episode-113107623-replay.json').read_text())
    ns = {'__name__': 'guard_diagnostic'}
    exec(compile(SOURCE.read_text(), str(SOURCE), 'exec'), ns)
    engine = importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    original = engine._end_of_day
    records = {}

    def predict(obs, action):
        _, private = ns['_ov_fields'](obs, action)
        stock, _, _ = ns['_r97_market_stock'](private['shed'], action.get('market') or [])
        final, loss = ns['_r97_delivery'](stock, private, True)
        proposed = ns['_ov_apply'](obs, deepcopy(action))
        return dict(private=private, market_stock=stock, predicted_final=final, predicted_loss=loss,
                    inventory_order=[list(inv) for inv in private['inventories']],
                    budget=ns['_r97_budget'](obs, action.get('market') or []),
                    guard_changed=proposed != action, guard_market=proposed.get('market'))

    def midnight(state, env, day):
        step = day * 24 + 23
        if step not in records:
            return original(state, env, day)
        row = records[step]
        private = deepcopy(state[1].observation.private)
        row['actual_private_before_drop'] = private
        row['actual_inventory_order'] = [list(inv) for inv in private['inventories']]
        row['delivery_on_actual_private'] = ns['_r97_delivery'](private['shed'], private, True)
        before = Counter(private['shed'])
        for inv in private['inventories']:
            before.update(inv)
        result = original(state, env, day)
        after = Counter(state[1].observation.private['shed'])
        row['actual_loss'] = dict(before - after)
        row['actual_final'] = dict(after)
        for label in ('live', 'json_replay'):
            row[label]['final_matches'] = ns['_ov_same'](row[label]['predicted_final'], after)
            row[label]['loss_matches'] = ns['_ov_same'](row[label]['predicted_loss'], row['actual_loss'])
        assert ns['_ov_same'](row['delivery_on_actual_private'][0], after)
        return result

    def tape(player):
        def agent(obs):
            step = int(obs['step'])
            action = deepcopy(replay['steps'][step + 1][player]['action'])
            if player == 1 and step in TARGETS:
                raw = deepcopy(replay['steps'][step][player]['observation'])
                # Replays store the shared observation fields only for player 0.
                shared = deepcopy(replay['steps'][step][0]['observation'])
                shared.update(raw)
                shared.update(step=step, player=player)
                records[step] = dict(step=step, action=action, live=predict(obs, action),
                                     json_replay=predict(shared, action))
            return action
        return agent

    engine._end_of_day = midnight
    try:
        env, ledger = run(tape(0), tape(1), replay['info']['seed'], 0)
    finally:
        engine._end_of_day = original
    assert all(compact_state(a) == compact_state(b) for a, b in zip(env.steps, replay['steps']))
    assert set(records) == set(TARGETS)
    OUT.write_text(json.dumps(dict(episode=113107623, states_exact=720, cash_reconciled=True,
                                   source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                                   note='The policy is not rerun. Native guard helpers inspect real replay actions; live agent observations and JSON replay observations are compared. No performance inference.',
                                   records=list(records.values())), indent=2)+'\n')
    for row in records.values():
        print(row['step'], 'actual_loss', row['actual_loss'],
              {key: {k: row[key][k] for k in ('predicted_loss', 'guard_changed', 'final_matches', 'loss_matches')}
               for key in ('live', 'json_replay')}, flush=True)


if __name__ == '__main__':
    main()
