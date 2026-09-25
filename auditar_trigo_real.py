"""Reproduce the real wheat-loss game with our actual source and frozen rival actions."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path

from investigar_lider import compact_state
from sonda_fallo_forecast import run

OUT = Path('docs/evidencia/loop_publicos_20260925')


def main():
    path = Path('submission/main_publico_arshs3_vq_top3.py')
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == '9668e30ad08f79d485bd230a3c660d4cc420b9382e87f9387b6908e3c94a5145'
    replay = json.loads(Path('results/top3_replays_0548_20260925/episode-113164976-replay.json').read_text())
    seat = replay['info']['TeamNames'].index('Rospel')
    ns = {}; exec(compile(raw, str(path), 'exec'), ns)
    entry = [v for v in ns.values() if callable(v)][-1]
    differences, decisions = [], []
    def ours(obs, config=None):
        step = int(obs['step']); action = entry(obs, config)
        expected = replay['steps'][step+1][seat]['action']
        if json.dumps(action, sort_keys=True) != json.dumps(expected, sort_keys=True):
            differences.append(dict(step=step, expected=expected, actual=deepcopy(action)))
        buys = [(i, o[2]) for i, o in enumerate(action.get('market', [])) if len(o) >= 3 and o[:2] == ['BUY_PRODUCT', 'WHEAT']]
        if 288 <= step <= 695 and len(buys) == 1 and buys[0][1] >= 20:
            decisions.append(dict(step=step, money=obs['farms'][seat]['money'],
                private=deepcopy(obs['private']), price=obs['market']['prices']['WHEAT'],
                market_inventory=obs['market']['inventory']['WHEAT'],
                emitted=deepcopy(action['market']),
                native_current=deepcopy(ns['_sr_tape'](seat, step).get('market', [])),
                native_next=deepcopy(ns['_sr_tape'](seat, step+1).get('market', []))))
        return action
    def rival(obs, config=None):
        return deepcopy(replay['steps'][int(obs['step'])+1][1-seat]['action'])
    env, ledger = run(ours, rival, replay['info']['seed'], seat)
    equal_states = sum(compact_state(a) == compact_state(b) for a, b in zip(env.steps, replay['steps']))
    report = dict(episode=113164976, source_sha256=hashlib.sha256(raw).hexdigest(),
                  scope='Reproduce our actual policy on the real trajectory; opponent is frozen replay, not a competitive counterfactual.',
                  action_differences=differences, exact_states=equal_states,
                  rewards=[s.reward for s in env.steps[-1]], decisions=decisions)
    target = OUT/'top3_0548_wheat_policy_trace.json'
    if target.exists(): raise FileExistsError(target)
    target.write_text(json.dumps(report, indent=2)+'\n')
    assert not differences and equal_states == 720 and report['rewards'] == replay['rewards']
    print(json.dumps(dict(exact_actions=719, exact_states=equal_states, large_buy_decisions=len(decisions), rewards=report['rewards'])))


if __name__ == '__main__': main()
