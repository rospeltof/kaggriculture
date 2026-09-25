# Recent, exact accepted sale streams. The public parent's ranking is unchanged.
_LB_PARENT = [v for v in list(globals().values()) if callable(v)][-1]
_LB_PAIR_PARENT = _v92_p_pair
_LB_FORECAST_PARENT = _v92_p_forecast
_LB_EXTRA = {}
_LB_IDS = {}
_LB_CACHE = {}
_LB_REPORT = {}
for _lb_row in _LB_RECORDS:
    _lb_events = {(t, i): q for t, i, q in _lb_row['sales']}
    _LB_EXTRA.setdefault(tuple(_lb_row['shops']), []).append((_lb_row['episode'], _lb_events))
    _LB_IDS[id(_lb_events)] = _lb_row['episode']


def _v92_p_pair(shops):
    if shops not in _LB_CACHE:
        original = _LB_PAIR_PARENT(shops)
        # Stable sorting in the parent preserves original priority on score ties.
        _LB_CACHE[shops] = original + _LB_EXTRA.get(shops, [])
    return _LB_CACHE[shops]


def _v92_p_forecast(obs, st):
    selected = _LB_FORECAST_PARENT(obs, st)
    _LB_REPORT['fits'] += 1
    _LB_REPORT['new_candidates_exposed'] += len(_LB_EXTRA.get(tuple(obs['town']['unlocked_shops'][:2]), []))
    for events in selected:
        episode = _LB_IDS.get(id(events))
        if episode is not None:
            _LB_REPORT['new_patterns_selected'] += 1
            key = str(episode)
            _LB_REPORT['selected_by_episode'][key] = _LB_REPORT['selected_by_episode'].get(key, 0) + 1
    return selected


def recent_library_agent(observation, configuration=None):
    if int(observation['step']) == 0:
        _LB_REPORT.clear()
        _LB_REPORT.update(fits=0, new_candidates_exposed=0,
                          new_patterns_selected=0, selected_by_episode={})
    return _LB_PARENT(observation, configuration)
