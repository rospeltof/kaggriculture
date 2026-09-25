# Research layer over the Apache-2.0 public agent; upstream notices retained.
# Configuration is inserted before this file. Only past observed sales rank patterns.
_PM_PARENT = [v for v in list(globals().values()) if callable(v)][-1]
_PM_REPORT = dict(calls=0, product_fits=0, shifted_patterns=0)


def _pm_score(events, seen, recent, lo, step, item=None, shift=0):
    matched = false = 0
    for (tt, i), quantity in events.items():
        if item is not None and i != item:
            continue
        tt += shift
        if lo <= tt < step - 1:
            if (tt, i) in seen or (tt - 1, i) in seen or (tt + 1, i) in seen:
                matched += 1
            else:
                false += 1
    missed = sum(
        1 for tt, i in recent
        if (item is None or i == item)
        and (tt - shift, i) not in events
        and (tt - shift - 1, i) not in events
        and (tt - shift + 1, i) not in events
    )
    return matched - 0.5 * false - 0.5 * missed


def _v92_p_forecast(obs, st):
    step = int(obs['step'])
    candidates = _v92_p_pair(tuple(obs['town']['unlocked_shops'][:2]))
    if _V92_EP is not None:
        candidates = [c for c in candidates if c[0] % 2 != _V92_EP % 2]
    seen = st['obs']
    lo = step - _PM_HISTORY
    recent = [(tt, i) for tt, i in seen if tt >= lo]
    _PM_REPORT['calls'] += 1
    ranked = sorted(
        ((_pm_score(ev, seen, recent, lo, step), ev) for _, ev in candidates),
        key=lambda pair: -pair[0],
    )
    fallback = [ev for _, ev in ranked[:_PM_TOP]]
    if _PM_MODE == 'product':
        # Each output stream combines the same rank for each product. This keeps
        # the parent's signal window and quantity gate untouched.
        combined = [{} for _ in fallback]
        for item in range(len(_V92_P_ITEMS)):
            if sum(i == item for _, i in recent) < 3:
                chosen = fallback
            else:
                chosen = [ev for _, ev in sorted(
                    ((_pm_score(ev, seen, recent, lo, step, item), ev) for _, ev in candidates),
                    key=lambda pair: -pair[0],
                )[:_PM_TOP]]
                _PM_REPORT['product_fits'] += 1
            for target, ev in zip(combined, chosen):
                target.update((key, q) for key, q in ev.items() if key[1] == item)
        return combined
    if _PM_MODE == 'phase':
        aligned = []
        for _, ev in candidates:
            original = _pm_score(ev, seen, recent, lo, step)
            best_score, best_shift = original, 0
            for shift in (-2, -1, 1, 2):
                score = _pm_score(ev, seen, recent, lo, step, shift=shift) - 0.25 * abs(shift)
                # Require an improvement over the unshifted stream, and preserve
                # the first winner on ties. Never inspect future observed sales.
                if score > original + 2 and score > best_score:
                    best_score, best_shift = score, shift
            aligned.append((best_score, best_shift, ev))
        aligned.sort(key=lambda row: -row[0])
        result = []
        for _, shift, ev in aligned[:_PM_TOP]:
            _PM_REPORT['shifted_patterns'] += bool(shift)
            result.append(ev if shift == 0 else {(tt + shift, i): q for (tt, i), q in ev.items()})
        return result
    return fallback


def adaptive_patterns_agent(observation, configuration=None):
    if int(observation['step']) == 0:
        for key in _PM_REPORT:
            _PM_REPORT[key] = 0
    return _PM_PARENT(observation, configuration)
