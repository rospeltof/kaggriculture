"""Protect next-turn native pickups from a late wheat sale, with funded top-up."""
_RW_PARENT = [value for value in list(globals().values()) if callable(value)][-1]
_RW_ENABLED = True
_RW_REPORT = {}
_RW_EVENTS = []
_RW_PENDING = None


def _rw_supply(obs, action):
    step = int(obs['step']); player = int(obs['player'])
    if not 648 <= step <= 694 or step % 24 == 23:
        return action
    orders = action.get('market') or []
    if not any(len(order) >= 3 and order[:2] == ['SELL', 'WHEAT'] for order in orders):
        return action
    if any(order[:2] == ['BUY_PRODUCT', 'WHEAT'] for order in orders):
        return action
    _RW_REPORT['checks'] += 1
    future = _IMPL.chassis.routes[2][step+1]
    commands = [future.get('farmer') or ['PASS'], *(future.get('hands') or [])]
    farm, private = _r127_fields(obs, action)
    positions = [tuple(farm['farmer']), *map(tuple, farm['hands'])]
    access = ((4, 4), (5, 4), (4, 5), (5, 5))
    pickups = []
    # Count only actors already present after this turn's field actions.
    for actor, (position, command, bag) in enumerate(zip(positions, commands, private['inventories'])):
        if position in access and command[:2] == ['PICKUP', 'WHEAT']:
            # Official PICKUP clips only to shed availability. Personal bags
            # have no ten-unit capacity; do not import that planning heuristic.
            quantity = max(0, int(command[2]) if len(command) > 2 else 1)
            if quantity:
                pickups.append(dict(actor=actor, position=list(position), command=list(command),
                                    quantity=quantity, bag=copy.deepcopy(bag)))
    need = sum(row['quantity'] for row in pickups)
    if not need:
        return action
    before, old_buys, _ = _r97_market_stock(private['shed'], orders)
    if before.get('WHEAT', 0) >= need:
        return action
    held = int(private['shed'].get('WHEAT', 0))
    allowance = max(0, held-need)
    mapped = []
    for index, order in enumerate(orders):
        modified = list(order)
        if len(order) >= 3 and order[:2] == ['SELL', 'WHEAT']:
            take = min(max(0, int(order[2])), allowance)
            allowance -= take
            if not take:
                continue
            modified[2] = take
        mapped.append((index, modified))
    shortage = max(0, need-held)
    if shortage:
        if shortage > max(0, 100-sum(private['shed'].values())):
            _RW_REPORT['capacity_declines'] += 1
            return action
        mapped.insert(0, (None, ['BUY_PRODUCT', 'WHEAT', shortage]))
    proposed = [order for index, order in mapped]
    if len(proposed) > 10:
        _RW_REPORT['slot_declines'] += 1
        return action
    budget = dict(obs, farms=[dict(farm) for farm in obs['farms']])
    budget['farms'][player]['money'] -= 5000
    if not _r97_budget(budget, proposed):
        _RW_REPORT['budget_declines'] += 1
        return action
    after, buys, _ = _r97_market_stock(private['shed'], proposed)
    if (after.get('WHEAT', 0) < need
            or any(buys.get(new, 0) < old_buys.get(old, 0)
                   for new, (old, order) in enumerate(mapped) if old is not None)):
        _RW_REPORT['capacity_declines'] += 1
        return action
    event = dict(step=step, need=need, pickups=pickups, held_after_units=held,
                 projected_shed=copy.deepcopy(private['shed']), original=copy.deepcopy(orders),
                 modified=copy.deepcopy(proposed), purchased=shortage,
                 predicted_before=int(before.get('WHEAT', 0)), predicted_after=int(after.get('WHEAT', 0)),
                 units=copy.deepcopy([action.get('farmer'), *(action.get('hands') or [])]))
    _RW_EVENTS.append(event)
    global _RW_PENDING
    _RW_PENDING = event
    _RW_REPORT['changes'] += 1
    _RW_REPORT['requested_units'] += shortage
    _RW_REPORT['protected_units'] += event['predicted_after']-event['predicted_before']
    return dict(action, market=proposed)


def route_wheat_agent(observation, configuration=None):
    global _RW_PENDING
    step = int(observation['step'])
    if step == 0:
        _RW_EVENTS.clear(); _RW_PENDING = None; _RW_REPORT.clear()
        _RW_REPORT.update(checks=0, changes=0, requested_units=0, protected_units=0,
                          errors=0, prediction_errors=0, capacity_declines=0,
                          slot_declines=0, budget_declines=0)
    pending = _RW_PENDING
    _RW_PENDING = None
    if pending is not None:
        pending['observed_next_step'] = step
        pending['observed_next_wheat'] = int(observation['private']['shed'].get('WHEAT', 0))
        if step != pending['step']+1 or pending['observed_next_wheat'] != pending['predicted_after']:
            _RW_REPORT['prediction_errors'] += 1
    result = _RW_PARENT(observation, configuration)
    if pending is not None:
        pending['next_emitted_units'] = copy.deepcopy([result.get('farmer'), *(result.get('hands') or [])])
    if not _RW_ENABLED:
        return result
    standard = configuration is None or all(configuration.get(key, value) == value for key, value in (
        ('boardSize', 10), ('turnsPerDay', 24), ('shedCapacity', 100),
        ('maxMarketOrdersPerTurn', 10), ('farmHandCostMult', 1)))
    if not standard:
        return result
    try:
        return _rw_supply(observation, result)
    except Exception:
        _RW_REPORT['errors'] += 1
        return result


route_wheat_agent.telemetry = _RW_REPORT
route_wheat_submission = route_wheat_agent
