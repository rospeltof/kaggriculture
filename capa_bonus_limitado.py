# Marginal value uses the physical production cap; native survival guard stays.
_BC_PARENT = [v for v in list(globals().values()) if callable(v)][-1]
_BC_ORIGINAL = _r88_feed_bonus_cost
_BC_REPORT = {}


def _r88_feed_bonus_cost(tile, day):
    original = _BC_ORIGINAL(tile, day)
    if _BC_MODE == 'noop':
        return original
    first, interval = _R88_ANIMAL_DAYS[tile['animal']]
    first += int(tile['placed_day'])
    tomorrow = day+1
    cap = 4 if tile['animal'] == 'GOOSE' else 6
    pending = max(0, int(tile.get('pending_care_bonus', 0)))
    held = max(0, int(tile.get('yield_units', 0)))
    value, reason = original, None
    if tomorrow < first and pending >= cap-1:
        value, reason = 0, 'first_bank_full'
    elif _BC_MODE == 'full' and tomorrow >= first and (tomorrow-first) % interval == 0:
        admitted = min(cap, held+1+pending)-min(cap, held+1)
        # The original value includes pending on production dawns plus the
        # separately valued care banked after that production, if useful later.
        value, reason = max(0, original-pending+admitted), 'production_cap'
    if value != original:
        _BC_REPORT.setdefault('value_changes', []).append(dict(day=day, animal=tile['animal'],
            placed_day=tile['placed_day'], held=held, pending=pending, cap=cap, first=first,
            original=original, value=value, reason=reason))
    return value


def capped_bonus_agent(observation, configuration=None):
    if int(observation['step']) == 0:
        _BC_REPORT.clear()
    return _BC_PARENT(observation, configuration)
