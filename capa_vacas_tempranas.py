# Earlier COW -> SHEEP purchases using the inherited physical-credit controller.
# Existing animals, routes, labor and the native days 8-11 policy stay intact.
_EC_PARENT = [v for v in list(globals().values()) if callable(v)][-1]
_EC_Y_CONTROLLER = _y_controller
_EC_REPORT = {}


def _y_controller(obs, action, state, cfg):
    step = int(obs['step'])
    if step == 0:
        _EC_REPORT.clear()
        _EC_REPORT.update(events=[], declined_inventory=0, declined_demand=0)
    day = step // 24
    # Days 8-11 are already handled by the public parent. Only extend backwards.
    if not _EC_START <= day <= 7:
        return _EC_Y_CONTROLLER(obs, action, state, cfg)
    buys = [o for o in action.get('market', [])
            if len(o) >= 3 and o[:2] == ['BUY_ANIMAL', 'COW'] and 1 <= int(o[2]) <= 2]
    if not buys:
        return _EC_Y_CONTROLLER(obs, action, state, cfg)
    yarn = obs['town']['unlocked_shops'].count('YARN_STORE')
    if yarn < _EC_MIN_YARN:
        _EC_REPORT['declined_demand'] += 1
        return _EC_Y_CONTROLLER(obs, action, state, cfg)
    private = obs['private']
    if any(inv.get(a, 0) for inv in [private['shed'], *private['inventories']]
           for a in ('COW', 'SHEEP', 'GOOSE')) or any(state['credit'].values()):
        _EC_REPORT['declined_inventory'] += 1
        return _EC_Y_CONTROLLER(obs, action, state, cfg)
    trial = dict(cfg, days=(_EC_START, 7), yarnsheep=True, yarngeese=False,
                 nosheep=False, nogeese=False, margin=_EC_MARGIN)
    # A zero threshold is exclusively a development control. The inherited
    # target still requires visible YARN; no future shops are synthesized.
    result = _EC_Y_CONTROLLER(obs, action, state, trial)
    after = [o for o in result.get('market', []) if len(o) >= 3 and o[0] == 'BUY_ANIMAL']
    before = [o for o in action.get('market', []) if len(o) >= 3 and o[0] == 'BUY_ANIMAL']
    if before != after:
        _EC_REPORT['events'].append(dict(step=step, yarn=yarn, before=before, after=after,
                                        pending=[dict(p) for p in state['pending']]))
    return result


def early_cow_agent(observation, configuration=None):
    return _EC_PARENT(observation, configuration)
