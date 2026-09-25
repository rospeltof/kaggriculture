# Account for wheat seed commitments without sharing the carrot reserve.
_LS_PARENT = [v for v in list(globals().values()) if callable(v)][-1]
_LS_REPORT = {}
_LS_EVENTS = []
_LS_CACHE = {}


def _ls_plant_count(action):
    return sum(bool(c) and len(c) >= 2 and c[0] == 'PLANT' and c[1] == 'WHEAT'
               for c in [action.get('farmer') or ['PASS'], *(action.get('hands') or [])])


def _ls_future(native, step):
    key = (native['route'], step)
    if key not in _LS_CACHE:
        _LS_CACHE[key] = sum(_ls_plant_count(_IMPL.chassis.routes[2 if t >= 648 else native['route']][t])
                             for t in range(step+1, 719))
    return _LS_CACHE[key]


def _ls_apply(obs, action):
    step = int(obs['step']); player = int(obs['player'])
    if step < 624 or step > 718:
        return action
    orders = action.get('market') or []
    indices = [i for i, order in enumerate(orders) if len(order) >= 3 and order[:2] == ['BUY_SEED', 'WHEAT']]
    if _LS_MODE == 'kind' and not indices:
        return action
    _LS_REPORT['checks'] += 1
    native = _IMPL.chassis.players[player]
    pending = sum(len(c) >= 2 and c[:2] == ['PLANT', 'WHEAT']
                  for queue in native.get('pending', {}).values() for pos, c in queue)
    proposed = copy.deepcopy(orders)
    original_qty = sum(max(0, int(orders[i][2])) for i in indices)
    if _LS_MODE == 'kind':
        available = max(0, int(obs['private']['seeds'].get('WHEAT', 0)) - _ls_plant_count(action))
        need = _ls_future(native, step) + pending
        for i in indices:
            keep = min(max(0, int(orders[i][2])), max(0, need-available))
            proposed[i] = ['BUY_SEED', 'WHEAT', keep] if keep else []
            available += keep
        projected = None
    else:
        assert _LS_MODE == 'jit'
        _, private = _r127_fields(obs, action)
        projected = int(private['seeds'].get('WHEAT', 0))
        _LS_REPORT['projections'] += 1
        future = _IMPL.chassis.routes[2 if step+1 >= 648 else native['route']][step+1] if step < 718 else {}
        need = _ls_plant_count(future) + pending if step < 718 else 0
        desired = max(0, need-projected)
        for i in indices:
            proposed[i] = []
        if desired:
            slot = indices[0] if indices else next((i for i, order in enumerate(proposed) if not order), None)
            if slot is None and len(proposed) < 10:
                slot = len(proposed); proposed.append([])
            if slot is None:
                _LS_REPORT['slot_declines'] += 1
                return action
            proposed[slot] = ['BUY_SEED', 'WHEAT', desired]
        if not _r97_budget(obs, proposed):
            _LS_REPORT['budget_declines'] += 1
            return action
    if proposed == orders:
        return action
    final_qty = sum(max(0, int(order[2])) for order in proposed if len(order) >= 3 and order[:2] == ['BUY_SEED', 'WHEAT'])
    _LS_REPORT['changed_turns'] += 1
    _LS_REPORT['cut_requests'] += max(0, original_qty-final_qty)
    _LS_REPORT['added_requests'] += max(0, final_qty-original_qty)
    _LS_EVENTS.append(dict(step=step, mode=_LS_MODE, pending=pending, need=need,
                           seed_before=int(obs['private']['seeds'].get('WHEAT', 0)), projected_seed=projected,
                           before=copy.deepcopy(orders), after=copy.deepcopy(proposed),
                           original_qty=original_qty, final_qty=final_qty))
    return dict(action, market=proposed)


def late_seed_agent(observation, configuration=None):
    action = _LS_PARENT(observation, configuration)
    if int(observation['step']) == 0:
        _LS_REPORT.clear(); _LS_EVENTS.clear(); _LS_CACHE.clear()
        _LS_REPORT.update(checks=0, changed_turns=0, cut_requests=0, added_requests=0,
                          projections=0, slot_declines=0, budget_declines=0, errors=0)
    if not _LS_ENABLED:
        return action
    try:
        return _ls_apply(observation, action)
    except Exception:
        _LS_REPORT['errors'] += 1
        return action


late_seed_agent.telemetry = _LS_REPORT
late_seed_submission = late_seed_agent
