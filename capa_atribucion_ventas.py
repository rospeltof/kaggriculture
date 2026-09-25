# Synchronize V9's internal sale snapshot with the final emitted market queue.
_SA_PARENT = [value for value in list(globals().values()) if callable(value)][-1]
_SA_REPORT = {}
_SA_EVENTS = []


def sales_attribution_agent(observation, configuration=None):
    step = int(observation['step']); player = int(observation['player'])
    if step == 0:
        _SA_REPORT.clear(); _SA_EVENTS.clear()
        _SA_REPORT.update(checks=0, changed_turns=0, changed_items=0, errors=0)
    action = _SA_PARENT(observation, configuration)
    if not _SA_ENABLED:
        return action
    try:
        state = _V9_RACE.get(player)
        prev = state.get('prev') if state else None
        if prev is None or prev.get('step') != step:
            return action
        _, private = _r127_fields(observation, action)
        stock = {item: max(0, int(private['shed'].get(item, 0))) for item in V9_RACE_ITEMS}
        own = {}
        for order in (action.get('market') or [])[:10]:
            if len(order) >= 3 and order[0] == 'SELL' and order[1] in stock:
                item = order[1]
                quantity = min(max(0, int(order[2])), max(0, stock[item]-own.get(item, 0)))
                own[item] = own.get(item, 0) + quantity
        left = {item: stock[item]-own.get(item, 0) for item in stock}
        changed = [item for item in stock
                   if prev['own'].get(item, 0) != own.get(item, 0)
                   or prev['left'].get(item, 0) != left[item]]
        _SA_REPORT['checks'] += 1
        if changed:
            _SA_REPORT['changed_turns'] += 1
            _SA_REPORT['changed_items'] += len(changed)
            _SA_EVENTS.append(dict(step=step, items=changed, old_own=dict(prev['own']),
                                   new_own=dict(own), old_left=dict(prev['left']), new_left=dict(left)))
        # Commit only after the complete projection succeeds. The emitted action
        # and the other observation fields remain those returned by the parent.
        prev['own'] = own
        prev['left'] = left
    except Exception:
        _SA_REPORT['errors'] += 1
    return action


sales_attribution_agent.telemetry = _SA_REPORT
sales_attribution_submission = sales_attribution_agent
