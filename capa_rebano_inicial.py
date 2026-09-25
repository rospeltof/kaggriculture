# Initial composition only; later shop-conditioned substitutions stay native.
_IH_PARENT = [v for v in list(globals().values()) if callable(v)][-1]
_IH_CONTROLLER = _y_controller
_IH_REPORT = {}


def _y_controller(obs, action, state, cfg):
    result = _IH_CONTROLLER(obs, action, state, cfg)
    step = int(obs['step'])
    if step == 0:
        _IH_REPORT.clear()
        _IH_REPORT.update(events=[], declined=0)
    if step != 1 or not _IH_QTY:
        return result
    if state['pending'] or any(state['credit'].values()):
        _IH_REPORT['declined'] += 1
        return result
    market = result.get('market') or []
    matches = [i for i,o in enumerate(market) if len(o) >= 3 and o[:2] == ['BUY_ANIMAL', _IH_FROM]]
    if len(matches) != 1:
        _IH_REPORT['declined'] += 1
        return result
    idx = matches[0]
    original_qty = int(market[idx][2])
    if original_qty != 2 or not 1 <= _IH_QTY <= original_qty:
        _IH_REPORT['declined'] += 1
        return result
    remaining = original_qty-_IH_QTY
    replacement = ([['BUY_ANIMAL', _IH_FROM, remaining]] if remaining else [])
    replacement.append(['BUY_ANIMAL', _IH_TO, _IH_QTY])
    trial = [list(o) for o in market[:idx]]+replacement+[list(o) for o in market[idx+1:]]
    margin = _y_cash(obs, result, trial)
    if len(trial) > 10 or margin < 100:
        _IH_REPORT['declined'] += 1
        return result
    # The native controller confirms physical stock gain on the next turn.
    state['pending'].append({'from': _IH_FROM, 'to': _IH_TO, 'qty': _IH_QTY,
                             'before': int(obs['private']['shed'].get(_IH_TO, 0))})
    _Y_REPORT['swaps'] += _IH_QTY
    _IH_REPORT['events'].append(dict(step=step, before=_y_copy.deepcopy(market),
                                     after=_y_copy.deepcopy(trial), margin=margin,
                                     source=_IH_FROM, target=_IH_TO, qty=_IH_QTY))
    return dict(result, market=trial)


def initial_herd_agent(observation, configuration=None):
    return _IH_PARENT(observation, configuration)
