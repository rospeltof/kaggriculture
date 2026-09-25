"""Official-engine two-turn wheat economics; synthetic diagnostics, not games."""
from copy import deepcopy
import hashlib
import importlib
import json
from pathlib import Path

from kaggle_environments import make

OUT = Path('docs/evidencia/loop_publicos_20260925')


def main():
    target = OUT/'town_roundtrip_probe.json'
    if target.exists(): raise FileExistsError(target)
    source = Path('submission/main_publico_arshs3_vq_top3.py'); ns = {}
    exec(compile(source.read_bytes(), str(source), 'exec'), ns)
    engine = importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    env = make('kaggriculture', configuration={'seed': 1048000, 'episodeSteps': 720}, debug=False)
    template = deepcopy(env.reset())
    scenarios = {
        'passive': (0, [], []),
        'buy30_sell30': (0, [['BUY_PRODUCT', 'WHEAT', 30]], [['SELL', 'WHEAT', 30]]),
        'buy90_sell90': (0, [['BUY_PRODUCT', 'WHEAT', 90]], [['SELL', 'WHEAT', 90]]),
        'sell30_now': (30, [['SELL', 'WHEAT', 30]], []),
        'sell30_next': (30, [], [['SELL', 'WHEAT', 30]]),
    }
    plan = dict(inventories=[10100, 10000, 9700, 9300], town_drains=[0, 1, 3, 6], quantities=[0, 10, 30, 60, 90],
                scenarios=scenarios, money_each=30000, own_initial_wheat=0, steps=[4, 5],
                scope='400 synthetic two-market scenarios. No unit actions, no learned opponent, no population effect or tournament selection.',
                source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                engine_sha256=hashlib.sha256(Path(engine.__file__).read_bytes()).hexdigest())
    (OUT/'town_roundtrip_probe.plan.json').write_text(json.dumps(plan, indent=2)+'\n')
    rows = []
    for inventory in plan['inventories']:
        for drain in plan['town_drains']:
            for scenario, (held, other_buy, other_sell) in scenarios.items():
                for quantity in plan['quantities']:
                    state = deepcopy(template)
                    obs = state[0].observation
                    for farm in obs.farms: farm.money = plan['money_each']
                    obs.market.inventory.WHEAT = inventory; engine._refresh_prices(obs.market)
                    obs.town.unlocked_shops = ['BAKERY']*drain
                    state[0].observation.private.shed.WHEAT = 0
                    state[1].observation.private.shed.WHEAT = held
                    params = ns['_v44y_params'](obs)
                    predicted = [0.0, 0.0]; receipts = []; inv = inventory; stocks = [0, held]
                    for leg, others in enumerate((other_buy, other_sell)):
                        own = [[['BUY_PRODUCT', 'WHEAT', quantity]], [['SELL', 'WHEAT', quantity]]][leg]
                        schedules = [own, others]
                        model = ns['_v44y_lockstep'](own, others, {'WHEAT': inv},
                            {'WHEAT': stocks[0]}, {'WHEAT': stocks[1]}, {'WHEAT': params['WHEAT']})
                        before = [farm['money'] for farm in obs.farms]
                        for player in (0, 1): state[player].action = dict(farmer=['PASS'], hands=[], market=deepcopy(schedules[player]))
                        engine._process_market(state, env)
                        actual = [farm['money']-money for farm, money in zip(obs.farms, before)]
                        assert actual == list(model), (inventory, drain, scenario, quantity, leg, model, actual)
                        for player, orders in enumerate(schedules):
                            for op, _, count in orders:
                                delta = count if op == 'BUY_PRODUCT' else -count
                                stocks[player] += delta; inv -= delta
                            assert state[player].observation.private.shed['WHEAT'] == stocks[player]
                            predicted[player] += model[player]
                        assert obs.market.inventory['WHEAT'] == inv
                        receipts.append(actual)
                        if leg == 0:
                            engine._town_consume(env, state, 4); inv -= drain
                            assert obs.market.inventory['WHEAT'] == inv
                    expected_alone = sum(engine.market_price('WHEAT', inventory-i-drain)-engine.market_price('WHEAT', inventory-i)
                                         for i in range(1, quantity+1))
                    if scenario == 'passive': assert predicted[0] == expected_alone
                    assert stocks[0] == 0 and [f['money'] for f in obs.farms] == [plan['money_each']+x for x in predicted]
                    rows.append(dict(inventory=inventory, drain=drain, scenario=scenario, quantity=quantity,
                                     own_net=predicted[0], rival_net=predicted[1], no_rival_model=expected_alone,
                                     receipts=receipts, ending_stocks=stocks))
    keyed = {(r['inventory'], r['drain'], r['scenario'], r['quantity']): r for r in rows}
    for row in rows:
        base = keyed[row['inventory'], row['drain'], row['scenario'], 0]
        row['margin_delta_vs_no_trade'] = (row['own_net']-row['rival_net'])-(base['own_net']-base['rival_net'])
    target.write_text(json.dumps(rows, indent=2)+'\n')
    print(json.dumps(dict(scenarios=len(rows), exact_market_legs=2*len(rows), source_hashes=plan['source_sha256'],
                         losses_despite_positive_no_rival_model=sum(r['own_net'] < 0 and r['no_rival_model'] > 0 for r in rows),
                         margin_losses_despite_positive_own_profit=sum(r['own_net'] > 0 and r['margin_delta_vs_no_trade'] < 0 for r in rows))))


if __name__ == '__main__': main()
