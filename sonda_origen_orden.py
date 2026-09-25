"""Locate the earliest market-order difference for the reproduced hash-seed issue."""
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import sys

from kaggle_environments import make
from kaggle_environments.agent import build_agent

OUT = Path('docs/evidencia/loop_publicos_20260925')


def main():
    hs = os.environ['PYTHONHASHSEED']; assert hs in ('0', '2')
    target = OUT / f'confirm19.order_origin_hash{hs}.json'; assert not target.exists()
    source = 'results/publicos/wzhengbiao_kaggriculture-hybu-submit/main.py'
    own, _ = build_agent('submission/main_publico_arshs3_vq_top3.py', {}, 'kaggriculture')
    rival, _ = build_agent(source, {}, 'kaggriculture')
    events = []

    def profile(frame, event, value):
        if event != 'return' or frame.f_code.co_filename != source:
            return
        if isinstance(value, dict) and isinstance(value.get('market'), list):
            market = value['market']
        elif isinstance(value, list) and value and all(isinstance(o, (list, tuple)) and o and isinstance(o[0], str) and o[0] in ('SELL', 'BUY_PRODUCT', 'BUY_SEED') for o in value):
            market = value
        else:
            return
        events.append(dict(function=frame.f_code.co_name, line=frame.f_code.co_firstlineno, market=deepcopy(market)))

    def opponent(obs, config):
        if int(obs['step']) != 466:
            return rival(obs, config)
        sys.setprofile(profile)
        try:
            return rival(obs, config)
        finally:
            sys.setprofile(None)

    env = make('kaggriculture', configuration={'seed': 1047024, 'episodeSteps': 720}, debug=False)
    env.run([own, opponent])
    assert len(env.steps) == 720 and [s.status for s in env.steps[-1]] == ['DONE', 'DONE']
    target.write_text(json.dumps(dict(hash_seed=hs, source=source, source_sha256=hashlib.sha256(Path(source).read_bytes()).hexdigest(),
                                     seed=1047024, step=466, events=events, rewards=[s.reward for s in env.steps[-1]]), indent=2) + '\n')
    print(json.dumps(dict(hash_seed=hs, traced_returns=len(events))))


if __name__ == '__main__':
    main()
