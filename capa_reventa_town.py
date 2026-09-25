"""Create bounded wheat roundtrips on known town consumption pulses."""
_TR_PARENT = [v for v in list(globals().values()) if callable(v)][-1]
_TR_ENABLED = True
_TR_MAX_Q = 20
_TR_PENDING = {}
_TR_REPORT = dict(buys=0, closes=0, requested=0, observed_bought=0, errors=0)
_TR_EVENTS = []


def _tr_shed_action(action):
    return any(c and c[0] in ('PICKUP', 'DROP', 'PLACE')
               for c in [action.get('farmer')] + list(action.get('hands') or []))


def _tr_apply(obs, action):
    player, step = int(obs['player']), int(obs['step'])
    if not _TR_ENABLED or not isinstance(action, dict): return action
    shed = obs['private']['shed']
    pending = _TR_PENDING.pop(player, None)
    if pending is not None:
        assert step == pending['step'] + 1
        bought = int(shed.get('WHEAT', 0)) - pending['before_wheat']
        assert 0 <= bought <= pending['quantity']
        orders = [list(o) for o in action.get('market') or []]
        inherited = sum(int(o[2]) for o in orders if len(o) >= 3 and o[:2] == ['SELL', 'WHEAT'])
        others = [o for o in orders if not (len(o) >= 3 and o[:2] == ['SELL', 'WHEAT'])]
        # Never truncate a parent's order to add our close.
        assert bought == 0 or len(others) < 10
        quantity = max(bought, inherited)
        changed = ([['SELL', 'WHEAT', quantity]] + others) if quantity else orders
        _TR_REPORT['closes'] += 1
        _TR_REPORT['observed_bought'] += bought
        _TR_EVENTS.append(dict(kind='close', step=step, buy_step=pending['step'], bought=bought,
                               quantity=quantity, inherited_sale=inherited, original=orders,
                               modified=changed, units=copy.deepcopy([action.get('farmer')] + list(action.get('hands') or []))))
        return dict(action, market=changed)
    if not 288 <= step <= 695 or step % 24 not in (4, 8, 12, 16, 20): return action
    if action.get('market') or _tr_shed_action(action): return action
    future = _sr_tape(player, step+1)
    if future.get('market') or _tr_shed_action(future): return action
    drain = sum((2 if len(_V9_SHOP_ITEMS.get(shop, ())) == 1 else 1)
                for shop in obs['town']['unlocked_shops'] if 'WHEAT' in _V9_SHOP_ITEMS.get(shop, ()))
    if drain <= 0: return action
    capacity = max(0, 100 - sum(int(v) for v in shed.values()) - 5)
    upper = min(_TR_MAX_Q, capacity)
    inventory = int(obs['market']['inventory']['WHEAT'])
    params = _v44y_params(obs)
    budget = max(0, obs['farms'][player]['money'] - 5000)
    quantity = 0; cost = 0
    for i in range(1, upper+1):
        price = _v44y_price('WHEAT', inventory-100-i, params)
        if cost + price > budget: break
        cost += price; quantity += 1
    if quantity == 0: return action
    naive_profit = sum(_v44y_price('WHEAT', inventory-i-drain, params)
                       - _v44y_price('WHEAT', inventory-i, params) for i in range(1, quantity+1))
    if naive_profit <= 0: return action
    pending = dict(step=step, quantity=quantity, before_wheat=int(shed.get('WHEAT', 0)))
    _TR_PENDING[player] = pending
    _TR_REPORT['buys'] += 1; _TR_REPORT['requested'] += quantity
    _TR_EVENTS.append(dict(kind='buy', **pending, capacity=capacity, estimated_cost=cost,
                           money=obs['farms'][player]['money'], inventory=inventory, drain=drain,
                           naive_profit=naive_profit, original=copy.deepcopy(action),
                           native_next=copy.deepcopy(future)))
    return dict(action, market=[['BUY_PRODUCT', 'WHEAT', quantity]])


def town_roundtrip_agent(observation, configuration=None):
    if int(observation['step']) == 0:
        _TR_PENDING.clear(); _TR_EVENTS.clear()
        for k in _TR_REPORT: _TR_REPORT[k] = 0
    action = _TR_PARENT(observation, configuration)
    try:
        return _tr_apply(observation, action)
    except Exception:
        _TR_REPORT['errors'] += 1
        return action


town_roundtrip_agent.telemetry = _TR_REPORT
