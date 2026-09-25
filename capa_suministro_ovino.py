# Provision the pending compact sheep worker and the native actors ahead of it.
_SS_PARENT = [v for v in list(globals().values()) if callable(v)][-1]
_SS_REPORT = {}
_SS_EVENTS = []
_SS_PENDING = None


def _ss_supply(obs, action):
    step = int(obs['step']); player = int(obs['player']); day = step//24
    state = _V233_STATES.get(player, {})
    pending = state.get('pending') or {}
    targets = pending.get('targets') or []
    if (not state.get('committed') or pending.get('initial') or
            pending.get('count') != 1 or len(targets) != 6 or
            day >= 28 or step % 24 == 23):
        return action
    _SS_REPORT['checks'] += 1
    orders = action.get('market') or []
    if len(orders) > 10 or not _r97_budget(obs, orders):
        _SS_REPORT['budget_declines'] += 1
        return action
    farm, private = _r127_fields(obs, action)
    access = ((4,4), (5,4), (4,5), (5,5))
    positions = [tuple(farm['farmer']), *map(tuple, farm['hands'])]
    for order in orders:
        if order == ['HIRE']:
            positions.append(min(access, key=lambda p: (positions.count(p), access.index(p))))
    actor = int(pending['first'])
    if actor != len(positions)-1 or positions[actor] not in access:
        _SS_REPORT['position_declines'] += 1
        return action
    tiles = [farm['tiles'][y][x] for x,y in targets]
    if any(not isinstance(t, dict) or t.get('animal') != 'SHEEP' for t in tiles):
        return action
    hungry = sum(not t.get('fed_today') for t in tiles)
    if not hungry:
        return action
    native = _IMPL.chassis.players[player]
    future = _IMPL.chassis.routes[2 if step+1 >= 648 else native['route']][step+1]
    commands = [future.get('farmer') or ['PASS'], *(future.get('hands') or [])]
    native_need = 0
    for i, (pos, command) in enumerate(zip(positions[:actor], commands[:actor])):
        if pos in access and command[:2] == ['PICKUP', 'WHEAT']:
            bag = private['inventories'][i] if i < len(private['inventories']) else {}
            native_need += min(max(0, int(command[2]) if len(command)>2 else 1),
                               max(0, 10-sum(bag.values())))
    need = native_need+hungry
    original, original_buys, _ = _r97_market_stock(private['shed'], orders)
    if original.get('WHEAT', 0) >= need:
        return action
    proposed = copy.deepcopy(orders)
    def project(candidate):
        stock, buys, sales = _r97_market_stock(private['shed'], candidate)
        safe = all(buys.get(i, 0) >= q for i, q in original_buys.items())
        return stock, sales, safe
    if _SS_HOLD:
        for i in range(len(proposed)-1, -1, -1):
            if proposed[i][:2] != ['SELL', 'WHEAT']:
                continue
            stock, sales, _ = project(proposed)
            shortage = max(0, need-stock.get('WHEAT', 0))
            if not shortage:
                break
            old = proposed[i][2]
            proposed[i][2] = max(0, sales.get(i, 0)-shortage)
            after, _, safe = project(proposed)
            if not safe or after.get('WHEAT', 0) <= stock.get('WHEAT', 0):
                proposed[i][2] = old
    stock, _, _ = project(proposed)
    shortage = max(0, need-stock.get('WHEAT', 0))
    if shortage:
        last_sale = max((i for i,o in enumerate(proposed) if o[:2] == ['SELL','WHEAT']), default=-1)
        index = next((i for i in range(len(proposed)-1, last_sale, -1)
                      if proposed[i][:2] == ['BUY_PRODUCT','WHEAT']), None)
        if index is not None:
            proposed[index][2] = int(proposed[index][2])+shortage
        elif len(proposed) < 10:
            proposed.append(['BUY_PRODUCT','WHEAT',shortage])
        else:
            _SS_REPORT['slot_declines'] += 1
            return action
    after, _, safe = project(proposed)
    if not safe or after.get('WHEAT', 0) < need:
        _SS_REPORT['capacity_declines'] += 1
        return action
    if not _r97_budget(obs, proposed):
        _SS_REPORT['budget_declines'] += 1
        return action
    event = dict(step=step, actor=actor, targets=copy.deepcopy(targets), hungry=hungry,
                 native_need=native_need, need=need, predicted_before=original.get('WHEAT',0),
                 predicted_after=after.get('WHEAT',0), original=copy.deepcopy(orders),
                 modified=copy.deepcopy(proposed), projected_shed=copy.deepcopy(private['shed']))
    _SS_EVENTS.append(event)
    global _SS_PENDING
    _SS_PENDING = event
    _SS_REPORT['changes'] += 1
    _SS_REPORT['protected_units'] += after.get('WHEAT',0)-original.get('WHEAT',0)
    return dict(action, market=proposed)


def sheep_supply_agent(observation, configuration=None):
    global _SS_PENDING
    step = int(observation['step'])
    if step == 0:
        _SS_REPORT.clear(); _SS_EVENTS.clear(); _SS_PENDING = None
        _SS_REPORT.update(checks=0, changes=0, protected_units=0, errors=0,
                          prediction_errors=0, slot_declines=0, capacity_declines=0,
                          budget_declines=0, position_declines=0)
    if _SS_PENDING is not None:
        event = _SS_PENDING; _SS_PENDING = None
        event['observed_next'] = observation['private']['shed'].get('WHEAT',0)
        event['observed_step'] = step
        if step != event['step']+1 or event['observed_next'] != event['predicted_after']:
            _SS_REPORT['prediction_errors'] += 1
    result = _SS_PARENT(observation, configuration)
    if not _SS_ENABLED:
        return result
    try:
        return _ss_supply(observation, result)
    except Exception:
        _SS_REPORT['errors'] += 1
        return result
