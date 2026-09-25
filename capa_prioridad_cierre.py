"""Preserve the native market queue when closing a town wheat roundtrip."""
_CQ_PARENT = [value for value in list(globals().values()) if callable(value)][-1]
_CQ_ENABLED = True
_CQ_REPORT = dict(closes=0, reordered=0, errors=0)
_CQ_EVENTS = []


def _cq_queue(original, quantity):
    if not quantity:
        return [list(order) for order in original]
    result = []
    inserted = False
    for order in original:
        if len(order) >= 3 and list(order[:2]) == ['SELL', 'WHEAT']:
            if not inserted:
                result.append(['SELL', 'WHEAT', quantity])
                inserted = True
        else:
            result.append(list(order))
    if not inserted:
        result.append(['SELL', 'WHEAT', quantity])
    assert len(result) <= 10
    return result


def close_queue_agent(observation, configuration=None):
    step = int(observation['step'])
    if step == 0:
        _CQ_EVENTS.clear()
        for key in _CQ_REPORT:
            _CQ_REPORT[key] = 0
    action = _CQ_PARENT(observation, configuration)
    if not _CQ_ENABLED or not _TR_EVENTS:
        return action
    event = _TR_EVENTS[-1]
    if event['kind'] != 'close' or event['step'] != step:
        return action
    try:
        assert action.get('market') == event['modified']
        queue = _cq_queue(event['original'], event['quantity'])
        _CQ_REPORT['closes'] += 1
        _CQ_REPORT['reordered'] += queue != event['modified']
        _CQ_EVENTS.append(dict(step=step, native=copy.deepcopy(event['original']),
                               town_computed=copy.deepcopy(event['modified']),
                               emitted=copy.deepcopy(queue), quantity=event['quantity'],
                               bought=event['bought']))
        return dict(action, market=queue)
    except Exception:
        _CQ_REPORT['errors'] += 1
        return action


close_queue_agent.telemetry = _CQ_REPORT
close_queue_submission = close_queue_agent
