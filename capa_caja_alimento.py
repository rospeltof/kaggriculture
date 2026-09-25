# Future obligations are a conservative quote of the native tape, not a
# simulation of adaptive future orders. No future sale/harvest is credited.
_CF_REPORT = {}


def _cf_margin(obs, action):
    step, seat = int(obs['step']), int(obs['player'])
    day = step // 24
    farm = obs['farms'][seat]
    prices = obs['market']['prices']
    end = min(719, day*24+23 if _CF_HORIZON == 'night' else step+int(_CF_HORIZON))
    hires = int(farm.get('hires_today', 0) or 0)
    quads = len(farm.get('unlocked_quadrants', []) or [])
    # Current-turn expenses are already in _y_cash; only advance the indices
    # used to quote later orders, assuming the current ones are accepted.
    for order in action.get('market', []):
        if order and order[0] == 'HIRE':
            hires += 1
        elif order and order[0] == 'BUY_LAND':
            quads += 1
    cost, obligations = 0.0, []
    for t in range(step+1, end+1):
        if t // 24 != day:
            hires = 0
            day = t // 24
        for order in _ca_tape(seat, t).get('market', []):
            if not order:
                continue
            op = order[0]
            quoted = 0
            if op == 'BUY_PRODUCT' and len(order) >= 3:
                if _CF_ALL or order[1] in ('WHEAT', 'FERTILIZER'):
                    quoted = max(0, int(order[2])) * (float(prices.get(order[1], 0))+10)
            elif _CF_ALL:
                if op == 'BUY_ANIMAL' and len(order) >= 3:
                    quoted = max(0, int(order[2])) * _Y_COST.get(order[1], 500)
                elif op == 'BUY_SEED' and len(order) >= 3:
                    quoted = max(0, int(order[2])) * _Y_SEED.get(order[1], 100)
                elif op == 'BUY_LAND':
                    quoted = (1000, 2000, 4000)[min(2, max(0, quads-1))]
                    quads += 1
                elif op == 'HIRE':
                    quoted = _y_fib(hires)
                    hires += 1
            if quoted:
                cost += quoted
                obligations.append(dict(step=t, order=list(order), cost=quoted))
    margin = 100+cost
    _CF_REPORT.setdefault('quotes', []).append(dict(step=step, end=end, margin=margin,
                                                  money=farm['money'], obligations=obligations))
    return margin


def cash_food_agent(observation, configuration=None):
    if int(observation['step']) == 0:
        _CF_REPORT.clear()
    return _EC_PARENT(observation, configuration)
