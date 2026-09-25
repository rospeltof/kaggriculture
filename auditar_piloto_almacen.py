"""Physical audit of loop13 pilot cells, without adding statistical samples."""
from collections import Counter
from copy import deepcopy
import argparse
import gzip
import hashlib
import importlib
import json
from pathlib import Path
import sys

from sonda_fallo_forecast import run

OUT = Path('docs/evidencia/loop_publicos_20260925')


def main():
    meta = json.loads((OUT/'pilot13.meta.json').read_text())
    assert meta['state'] == 'complete'
    rows = [json.loads(l) for l in (OUT/'pilot13.jsonl').read_text().splitlines()]
    keyed = {(r['a'], r['b'], r['seed'], r['seat']): r for r in rows}
    arms = ['base', 'night_inputs1', 'night_inputs2']
    rivals = ['arshs3', 'ars40', 'hybu', 'tds']
    benefits, neutral = set(), set()
    for r in rows:
        if r['a'] != 'base' or r['b'] not in rivals or r['seat'] != 0: continue
        cs = [keyed[a, r['b'], r['seed'], 0] for a in arms[1:]]
        cell = r['b'], r['seed'], 0
        if any(c['score'] > r['score'] for c in cs): benefits.add(cell)
        elif all(c['score'] == r['score'] for c in cs) and any(c['action_hashes'][0] != r['action_hashes'][0] for c in cs): neutral.add(cell)
    cells = sorted(benefits) + [sorted(neutral)[0]]
    assert len(benefits) == 3 and len(cells) == 4
    plan = dict(rule='All three WLT-improving pilot cells, plus first sorted changed-action/equal-WLT cell, seat0 only. Diagnostic, no extra statistical samples.',
                cells=cells, arms=arms, agents=meta['agentes'])
    target = OUT/'pilot13.physical.plan.json'
    if target.exists(): raise FileExistsError(target)
    target.write_text(json.dumps(plan, indent=2)+'\n')
    engine = importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    original_unit, original_night = engine._apply_unit_action, engine._end_of_day
    results = []
    for opponent, seed, seat in cells:
        for arm in arms:
            spec = meta['agentes'][arm]; path = Path(spec['ruta']); raw = path.read_bytes()
            assert hashlib.sha256(raw).hexdigest() == spec['sha256']
            oppspec = meta['agentes'][opponent]
            assert hashlib.sha256(Path(oppspec['ruta']).read_bytes()).hexdigest() == oppspec['sha256']
            ns = {}; exec(compile(raw, str(path), 'exec'), ns)
            entry = [v for v in ns.values() if callable(v)][-1]
            digest = hashlib.sha256(); steps = []
            def traced(obs, config=None):
                action = entry(obs, config)
                digest.update(json.dumps(action, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()+b'\n')
                steps.append(int(obs['step']))
                return action
            nights, units, harvest, accepted = [], [], Counter(), Counter()
            def instrument(farm, private, actor, action, *args, **kwargs):
                frame = sys._getframe(1)
                watch = (frame.f_code is engine.interpreter.__code__ and frame.f_locals.get('i') == seat
                         and action and action[0] in ('FEED', 'CARE', 'HARVEST', 'FERTILIZE'))
                if watch:
                    pos = farm['farmer'] if actor == 0 else farm['hands'][actor-1]
                    x, y = pos; tile = deepcopy(farm['tiles'][y][x]); before = dict(private['inventories'][actor])
                    subject = str(tile.get('animal') or tile.get('crop') or tile.get('kind')) if isinstance(tile, dict) else str(tile)
                result = original_unit(farm, private, actor, action, *args, **kwargs)
                if watch:
                    after = private['inventories'][actor]; new = farm['tiles'][y][x]
                    delta = {k: after.get(k, 0)-before.get(k, 0) for k in set(before)|set(after)}
                    if action[0] == 'HARVEST':
                        gain = {k: q for k, q in delta.items() if q > 0}; harvest.update(gain); ok = bool(gain)
                    elif action[0] == 'FERTILIZE': ok = delta.get('FERTILIZER', 0) < 0
                    else:
                        flag = {'FEED': 'fed_today', 'CARE': 'cared_today'}[action[0]]
                        ok = isinstance(tile, dict) and isinstance(new, dict) and not tile.get(flag) and new.get(flag)
                    if ok: accepted[action[0]+':'+subject] += 1
                    units.append(dict(step=frame.f_locals['step'], actor=actor, xy=list(pos), action=deepcopy(action), subject=subject,
                                      successful=bool(ok), inventory_delta={k: v for k, v in delta.items() if v}))
                return result
            def midnight(state, env, day):
                private = deepcopy(state[seat].observation.private); total = Counter(private['shed'])
                for inv in private['inventories']: total.update(inv)
                farm = state[0].observation.farms[seat]
                unfed = [dict(x=x, y=y, animal=t['animal']) for y, line in enumerate(farm.tiles) for x, t in enumerate(line)
                         if isinstance(t, dict) and t.get('animal') and not t.get('fed_today')]
                result = original_night(state, env, day)
                final = dict(state[seat].observation.private.shed); loss = dict(total-Counter(final))
                event = next((e for e in ns.get('_NF_EVENTS', []) if e['step'] == day*24+23), None)
                if event:
                    assert ns['_ov_same'](event['predicted_final'], final)
                    assert ns['_ov_same'](event['predicted_loss'], loss)
                nights.append(dict(step=day*24+23, loss=loss, unfed=unfed, prediction=deepcopy(event)))
                return result
            engine._apply_unit_action, engine._end_of_day = instrument, midnight
            try: env, ledger = run(traced, oppspec['ruta'], seed, seat)
            finally: engine._apply_unit_action, engine._end_of_day = original_unit, original_night
            expected = keyed[arm, opponent, seed, seat]; rewards = [s.reward for s in env.steps[-1]]
            assert rewards == expected['rewards']
            assert steps == list(range(719)) and digest.hexdigest() == expected['action_hashes'][seat]
            reports = {k: deepcopy(ns.get(k, {})) for k in ('_NF_REPORT', '_V92_P_REPORT', '_VQ_REPORT', '_R85_REPORT')}
            assert not any(v for report in reports.values() for k, v in report.items() if 'error' in k and isinstance(v, (int, float)))
            escapes = []
            for t in range(719):
                before = env.steps[t][0].observation.farms[seat].tiles; after = env.steps[t+1][0].observation.farms[seat].tiles
                for y, line in enumerate(before):
                    for x, tile in enumerate(line):
                        if isinstance(tile, dict) and tile.get('animal'):
                            new = after[y][x].get('animal') if isinstance(after[y][x], dict) else None
                            if new != tile['animal']: escapes.append(dict(step=t, xy=[x, y], animal=tile['animal']))
            loss = Counter(); flows = {}
            for night in nights: loss.update(night['loss'])
            for e in ledger:
                if e['player'] == seat:
                    key = e['op']+':'+str(e['item']); q, money = flows.get(key, [0, 0]); flows[key] = [q+1, money+e['value']]
            row = dict(arm=arm, opponent=opponent, seed=seed, seat=seat, rewards=rewards, action_hash=digest.hexdigest(),
                       reports=reports, nights=nights, losses=dict(loss), harvested=dict(harvest), accepted=dict(accepted),
                       flows=flows, escapes=escapes, terminal_private=env.steps[-1][seat].observation.private,
                       shops=env.steps[-1][0].observation.town.unlocked_shops)
            results.append(row)
            for kind, data in (('ledger', ledger), ('units', units)):
                target = OUT/f'pilot13.physical.{opponent}.{seed}.{arm}.{kind}.jsonl.gz'
                if target.exists(): raise FileExistsError(target)
                target.write_bytes(gzip.compress(('\n'.join(json.dumps(e) for e in data)+'\n').encode(), mtime=0))
            print(json.dumps({k: row[k] for k in ('arm', 'opponent', 'seed', 'rewards', 'losses', 'harvested', 'escapes')}), flush=True)
    (OUT/'pilot13.physical.json').write_text(json.dumps(results, indent=2)+'\n')


def summarize():
    rows = json.loads((OUT/'pilot13.physical.json').read_text())
    assert len(rows) == 12
    keyed = {(r['arm'], r['opponent'], r['seed']): r for r in rows}
    def failed_feeds(row):
        path = OUT/f"pilot13.physical.{row['opponent']}.{row['seed']}.{row['arm']}.units.jsonl.gz"
        units = [json.loads(l) for l in gzip.decompress(path.read_bytes()).decode().splitlines()]
        return [e for e in units if e['action'][0] == 'FEED' and not e['successful']]
    def delta(a, b):
        return {k: a.get(k, 0)-b.get(k, 0) for k in a.keys()|b.keys() if a.get(k, 0) != b.get(k, 0)}
    summary = []
    for row in rows:
        if row['arm'] == 'base': continue
        base = keyed['base', row['opponent'], row['seed']]
        summary.append(dict(arm=row['arm'], opponent=row['opponent'], seed=row['seed'],
            margin_base=base['rewards'][0]-base['rewards'][1], margin_candidate=row['rewards'][0]-row['rewards'][1],
            loss_base=sum(base['losses'].values()), loss_candidate=sum(row['losses'].values()),
            harvest_delta=delta(row['harvested'], base['harvested']), accepted_delta=delta(row['accepted'], base['accepted']),
            same_shops=row['shops'] == base['shops'], nf=row['reports']['_NF_REPORT'],
            unfed_differences=[dict(step=b['step'], base=b['unfed'], candidate=c['unfed']) for b, c in zip(base['nights'], row['nights']) if b['unfed'] != c['unfed']],
            failed_FEED_base=failed_feeds(base), failed_FEED_candidate=failed_feeds(row), escapes=row['escapes']))
    (OUT/'pilot13.physical.summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--summarize-only', action='store_true')
    args = parser.parse_args()
    if not args.summarize_only: main()
    summarize()
