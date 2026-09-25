"""Exact physical wool balance in the recent top3 loss against daviondk."""
from collections import Counter
from copy import deepcopy
import gzip
import hashlib
import importlib
import json
from pathlib import Path
import sys

from investigar_lider import compact_state
from sonda_fallo_forecast import run

OUT = Path('docs/evidencia/loop_publicos_20260925')


def main():
    target = OUT/'davion_wool_audit.json'; assert not target.exists()
    path = Path('replays/top3_feedback_0653/episode-113174624-replay.json')
    replay = json.loads(path.read_bytes()); seat = replay['info']['TeamNames'].index('Rospel')
    source = Path('submission/main_publico_arshs3_vq_top3.py'); data = source.read_bytes()
    assert hashlib.sha256(data).hexdigest() == '9668e30ad08f79d485bd230a3c660d4cc420b9382e87f9387b6908e3c94a5145'
    plan = dict(episode=113174624, seed=replay['info']['seed'], seat=seat,
                rule='Only top3 loss in the four recent episodes already selected by date; physical attribution only, no new population sample.',
                source_sha256=hashlib.sha256(data).hexdigest(), replay_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    (OUT/'davion_wool_audit.plan.json').write_text(json.dumps(plan, indent=2)+'\n')
    ns = {}; exec(compile(data, str(source), 'exec'), ns); entry = [v for v in ns.values() if callable(v)][-1]
    old_feed = ns['_r85_feed']; skipped = []; units = []; nights = []
    def feed(obs, action):
        before = deepcopy(action); revised = old_feed(obs, action)
        farm = obs['farms'][seat]; positions = [farm['farmer'], *farm['hands']]
        old = [before.get('farmer'), *(before.get('hands') or [])]
        new = [revised.get('farmer'), *(revised.get('hands') or [])]
        for actor, (a, b) in enumerate(zip(old, new)):
            if a != ['FEED'] or b == a or actor >= len(positions): continue
            x, y = positions[actor]; tile = farm['tiles'][y][x]
            if isinstance(tile, dict) and tile.get('animal') == 'SHEEP':
                skipped.append(dict(step=int(obs['step']), actor=actor, xy=[x,y], tile=deepcopy(tile),
                                    prices=deepcopy(obs['market']['prices']), bonus=ns['_r88_feed_bonus_cost'](tile, int(obs['step'])//24)))
        return revised
    ns['_r85_feed'] = feed
    engine = importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    old_unit, old_night = engine._apply_unit_action, engine._end_of_day
    def unit(farm, private, actor, action, *args, **kwargs):
        frame = sys._getframe(1); actual = frame.f_code is engine.interpreter.__code__
        watch = actual and action and action[0] in ('FEED', 'CARE', 'HARVEST')
        if watch:
            x,y = farm['farmer'] if actor == 0 else farm['hands'][actor-1]
            tile = deepcopy(farm['tiles'][y][x]); watch = isinstance(tile, dict) and tile.get('animal') == 'SHEEP'
            before = dict(private['inventories'][actor])
        result = old_unit(farm, private, actor, action, *args, **kwargs)
        if watch:
            new = farm['tiles'][y][x]; after = private['inventories'][actor]
            gained = after.get('WOOL', 0)-before.get('WOOL', 0)
            cleared = max(0, tile['yield_units']-new['yield_units']) if action[0] == 'HARVEST' else 0
            flag = {'FEED':'fed_today', 'CARE':'cared_today'}.get(action[0])
            ok = (not tile.get(flag) and new.get(flag)) if flag else gained > 0
            units.append(dict(step=frame.f_locals['step'], player=frame.f_locals['i'], actor=actor, xy=[x,y],
                              action=deepcopy(action), successful=bool(ok), wheat_spent=before.get('WHEAT',0)-after.get('WHEAT',0),
                              wool_gained=gained, harvest_overflow=cleared-gained, tile_before=tile))
        return result
    def night(state, env, day):
        tiles = [deepcopy(f['tiles']) for f in state[0].observation['farms']]
        before_stock = []
        for p in (0,1):
            private = state[p].observation['private']
            before_stock.append(private['shed'].get('WOOL',0)+sum(i.get('WOOL',0) for i in private['inventories']))
        result = old_night(state, env, day)
        for p in (0,1):
            private = state[p].observation['private']; after_stock = private['shed'].get('WOOL',0)+sum(i.get('WOOL',0) for i in private['inventories'])
            events = []
            for y,line in enumerate(tiles[p]):
                for x,tile in enumerate(line):
                    if not isinstance(tile,dict) or tile.get('animal') != 'SHEEP': continue
                    new = state[0].observation['farms'][p]['tiles'][y][x]
                    assert isinstance(new,dict) and new.get('animal') == 'SHEEP'
                    age = day+1-tile['placed_day']-6; produces = age >= 0 and age % 3 == 0
                    bank = tile['pending_care_bonus']; inc = 1+(bank if tile['fed_today'] else 0) if produces else 0
                    expected = min(6,tile['yield_units']+inc)
                    assert new['yield_units'] == expected
                    actual = new['yield_units']-tile['yield_units']
                    feed_gap = max(0,min(6,tile['yield_units']+1+bank)-new['yield_units']) if produces and not tile['fed_today'] else 0
                    events.append(dict(xy=[x,y], before=tile, after=deepcopy(new), produces=produces,
                                       actual_production=actual, cap_loss=inc-actual, immediate_feed_gap=feed_gap))
            nights.append(dict(step=day*24+23, player=p, wool_storage_loss=before_stock[p]-after_stock, animals=events))
        return result
    def rival(obs): return deepcopy(replay['steps'][int(obs['step'])+1][1-seat]['action'])
    engine._apply_unit_action, engine._end_of_day = unit, night
    try: env, ledger = run(entry, rival, replay['info']['seed'], seat)
    finally: engine._apply_unit_action, engine._end_of_day = old_unit, old_night
    assert all(compact_state(a) == compact_state(b) for a,b in zip(env.steps,replay['steps']))
    assert all(env.steps[t+1][seat].action == replay['steps'][t+1][seat]['action'] for t in range(719))
    for e in skipped:
        action = env.steps[e['step']+1][seat].action; cmds = [action.get('farmer'), *(action.get('hands') or [])]
        e['final_command'] = cmds[e['actor']] if e['actor'] < len(cmds) else None
    summaries = []
    for p in (seat,1-seat):
        rows = [n for n in nights if n['player']==p]; events = [e for n in rows for e in n['animals']]
        own = [e for e in units if e['player']==p]
        production = sum(e['actual_production'] for e in events)
        field = sum(t.get('yield_units',0) for line in env.steps[-1][0].observation['farms'][p]['tiles'] for t in line if isinstance(t,dict) and t.get('animal')=='SHEEP')
        private=env.steps[-1][p].observation['private']; held=private['shed'].get('WOOL',0)+sum(i.get('WOOL',0) for i in private['inventories'])
        sales=[e for e in ledger if e['player']==p and e['op']=='SELL' and e['item']=='WOOL']
        overflow=sum(e['harvest_overflow'] for e in own); storage=sum(n['wool_storage_loss'] for n in rows)
        assert production == len(sales)+field+held+overflow+storage
        summaries.append(dict(player=p, production=production, sold=len(sales), sale_cash=sum(e['value'] for e in sales),
                              field_final=field, private_final=held, harvest_overflow=overflow, storage_loss=storage,
                              cap_loss=sum(e['cap_loss'] for e in events), immediate_feed_gap=sum(e['immediate_feed_gap'] for e in events),
                              accepted=dict(Counter(e['action'][0] for e in own if e['successful'])),
                              fed_nights=sum(bool(e['before']['fed_today']) for e in events), cared_nights=sum(bool(e['before']['cared_today']) for e in events)))
    report=dict(plan=plan, states_exact=720, summaries=summaries, economic_feed_skips=skipped,
                note='Immediate feed_gap holds current bank/stock fixed; it excludes future care, routing and market feedback, and is not realizable profit.')
    target.write_text(json.dumps(report,indent=2)+'\n')
    for name, data in [('nights',nights),('units',units)]:
        (OUT/f'davion_wool_audit.{name}.jsonl.gz').write_bytes(gzip.compress(('\n'.join(json.dumps(e) for e in data)+'\n').encode(),mtime=0))
    print(json.dumps(dict(summaries=summaries, economic_feed_skips=len(skipped)),indent=2))


if __name__ == '__main__': main()
