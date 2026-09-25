"""Ablate quantity and slot of large native wheat buy/next-turn sell sequences."""
_WT_PARENT = [v for v in list(globals().values()) if callable(v)][-1]
_WT_ENABLED = True
_WT_HALF = False
_WT_FRONT = False
_WT_REPORT = dict(eligible=0, changed=0, cut_units=0, moved=0, errors=0)
_WT_EVENTS = []


def _wt_apply(obs, action):
    step = int(obs['step'])
    if not _WT_ENABLED or not 288 <= step <= 695 or step % 24 == 23 or not isinstance(action, dict):
        return action
    orders = action.get('market') or []
    buys = [i for i, o in enumerate(orders) if len(o) >= 3 and o[:2] == ['BUY_PRODUCT', 'WHEAT']]
    if len(buys) != 1: return action
    index = buys[0]; quantity = int(orders[index][2])
    if quantity < 20 or len(orders) > 10: return action
    if any(len(o) < 3 or o[0] != 'BUY_SEED' for i, o in enumerate(orders) if i != index):
        return action
    native = _sr_tape(int(obs['player']), step+1)
    planned = sum(max(0, int(o[2])) for o in native.get('market', [])
                  if len(o) >= 3 and o[:2] == ['SELL', 'WHEAT'])
    if planned < (quantity+1)//2: return action
    _WT_REPORT['eligible'] += 1
    new_quantity = (quantity+1)//2 if _WT_HALF else quantity
    if new_quantity == quantity and (not _WT_FRONT or index == 0): return action
    changed = [list(o) for o in orders]
    changed[index][2] = new_quantity
    if _WT_FRONT: changed.insert(0, changed.pop(index))
    _WT_REPORT['changed'] += 1
    _WT_REPORT['cut_units'] += quantity-new_quantity
    _WT_REPORT['moved'] += int(_WT_FRONT and index > 0)
    _WT_EVENTS.append(dict(step=step, original=copy.deepcopy(orders), modified=copy.deepcopy(changed),
                           original_quantity=quantity, new_quantity=new_quantity,
                           original_index=index, new_index=0 if _WT_FRONT else index,
                           next_native_sale=planned))
    return dict(action, market=changed)


def wheat_retrade_agent(observation, configuration=None):
    if int(observation['step']) == 0:
        _WT_REPORT.update(eligible=0, changed=0, cut_units=0, moved=0, errors=0)
        _WT_EVENTS.clear()
    action = _WT_PARENT(observation, configuration)
    try:
        return _wt_apply(observation, action)
    except Exception:
        _WT_REPORT['errors'] += 1
        return action


wheat_retrade_agent.telemetry = _WT_REPORT
