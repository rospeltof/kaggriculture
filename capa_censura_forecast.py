# Do not treat an unobservable premium-sale event as negative evidence.
_CF_PARENT = [value for value in list(globals().values()) if callable(value)][-1]
_CF_FORECAST_PARENT = _v92_p_forecast
_CF_MASKS = {}
_CF_REPORT = {}
_CF_EVENTS = []


def _cf_forecast(obs, st):
    if not _CF_ENABLED:
        return _CF_FORECAST_PARENT(obs, st)
    step = int(obs['step']); player = int(obs['player'])
    masks = _CF_MASKS.get(player, {})
    shops = tuple(obs['town']['unlocked_shops'][:2])
    candidates = _v92_p_pair(shops)
    if _V92_EP is not None:
        candidates = [c for c in candidates if c[0] % 2 != _V92_EP % 2]
    seen = st['obs']; lo = step-240
    recent = [(t, i) for t, i in seen if t >= lo]
    scored = []; original = []; ignored = 0
    for index, (_, events) in enumerate(candidates):
        matches = 0; false = 0; native_false = 0
        for t, i in events:
            if not lo <= t < step-1:
                continue
            if any((t+d, i) in seen for d in (-1, 0, 1)):
                matches += 1
            else:
                native_false += 1
                if all(masks.get((t+d, i), False) for d in (-1, 0, 1)):
                    false += 1
                else:
                    ignored += 1
        missing = sum(not any((t+d, i) in events for d in (-1, 0, 1)) for t, i in recent)
        scored.append((matches-.5*false-.5*missing, index))
        original.append((matches-.5*native_false-.5*missing, index))
    selected = [i for _, i in sorted(scored, key=lambda x: -x[0])[:_V92_P_TOP]]
    native = [i for _, i in sorted(original, key=lambda x: -x[0])[:_V92_P_TOP]]
    result = [candidates[i][1] for i in selected]
    changed = result != [candidates[i][1] for i in native]
    _CF_REPORT['forecasts'] += 1
    _CF_REPORT['changed_rankings'] += changed
    _CF_REPORT['ignored_penalties'] += ignored
    _CF_EVENTS.append(dict(step=step, selected=selected, native_selected=native,
                           changed=changed, ignored_penalties=ignored))
    return result


_v92_p_forecast = _cf_forecast


def censored_forecast_agent(observation, configuration=None):
    player = int(observation['player']); step = int(observation['step'])
    if step == 0:
        _CF_MASKS.clear(); _CF_EVENTS.clear(); _CF_REPORT.clear()
        _CF_REPORT.update(forecasts=0, changed_rankings=0, ignored_penalties=0,
                          item_turns=0, unobservable=0, errors=0)
    if _CF_ENABLED:
        try:
            masks = _CF_MASKS.setdefault(player, {})
            prev = (_V9_RACE.get(player) or {}).get('prev')
            if prev is not None and prev['step'] == step-1:
                draw = _v9_town_draw(prev['shops'], step-1)
                params = _v44y_params(observation) if _CF_MODE == 'floor' else None
                for i, item in enumerate(_V92_P_ITEMS):
                    visible = prev['prices'].get(item, 0) > 3
                    if visible and _CF_MODE == 'floor':
                        stock = int(observation['market']['inventory'][item]) + draw.get(item, 0)
                        visible = _r37_market_price(item, stock, params) > 1
                    masks[step-1, i] = visible
                    _CF_REPORT['item_turns'] += 1
                    _CF_REPORT['unobservable'] += not visible
        except Exception:
            _CF_REPORT['errors'] += 1
    return _CF_PARENT(observation, configuration)


censored_forecast_agent.telemetry = _CF_REPORT
censored_forecast_submission = censored_forecast_agent
