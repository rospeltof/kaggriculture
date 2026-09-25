"""Fixed opening quantity; preserve net wheat and every other parent decision."""
_OPN_PARENT = [value for value in list(globals().values()) if callable(value)][-1]
_OPN_REPORT = {}
_OPN_EVENTS = []
_OPN_DAILY_MIN = {}


def opening_quantity_agent(observation, configuration=None):
    step = int(observation['step']); player = int(observation['player'])
    if step == 0:
        _OPN_REPORT.clear(); _OPN_REPORT.update(opening_calls=0, initial_wheat=-1, errors=0)
        _OPN_EVENTS.clear(); _OPN_DAILY_MIN.clear()
    money = float(observation['farms'][player]['money'])
    day = step//24
    _OPN_DAILY_MIN[day] = min(money, _OPN_DAILY_MIN.get(day, money))
    action = _OPN_PARENT(observation, configuration)
    if step == 0:
        _OPN_REPORT['opening_calls'] += 1
        _OPN_EVENTS.append(dict(step=step, quantity=_OPN_Q, market=copy.deepcopy(action.get('market') or [])))
    if step == 1:
        _OPN_REPORT['initial_wheat'] = int(observation['private']['shed'].get('WHEAT', 0))
        _OPN_EVENTS.append(dict(step=step, money=money, shed=copy.deepcopy(observation['private']['shed']),
                                market=copy.deepcopy(action.get('market') or [])))
    return action


opening_quantity_agent.telemetry = _OPN_REPORT
opening_quantity_submission = opening_quantity_agent
