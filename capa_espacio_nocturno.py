"""Release excess input stock when the final night transfer would destroy cargo.

Appended to top3; all upstream attribution remains in the generated artifact.
This changes the product mix at dawn. Reserves are a testable heuristic, not a
proof that every future pickup succeeds. Actual live inventory order matters.
"""
_NF_ENABLED = True
_NF_DAYS = 1
_NF_FERTILIZER = False
_NF_BUFFER = 6
_NF_PARENT = [v for v in list(globals().values()) if callable(v)][-1]
_NF_REPORT = dict(nf_turns=0, nf_sold=0, nf_saved=0, nf_errors=0)
_NF_EVENTS = []


def _nf_apply(obs, action):
    step, seat = int(obs['step']), int(obs['player'])
    if not _NF_ENABLED or step % 24 != 23 or step >= 717 or not isinstance(action, dict):
        return action
    orders = action.get('market') or []
    if len(orders) >= 10 or not _r97_budget(obs, orders):
        return action
    farm, private = _ov_fields(obs, action)
    stock, _, _ = _r97_market_stock(private['shed'], orders)
    original, loss = _r97_delivery(stock, private, True)
    if not loss:
        return action
    days = min(_NF_DAYS, 29 - step // 24)
    animals = sum(isinstance(tile, dict) and bool(tile.get('animal'))
                  for row in farm['tiles'] for tile in row)
    fert_need = 0
    for future in range(step + 1, min(719, step + 1 + days * 24)):
        native = _sr_tape(seat, future)
        fert_need += sum(1 for c in [native.get('farmer') or ['PASS'], *(native.get('hands') or [])]
                         if c and c[0] == 'FERTILIZE')
    floors = {'WHEAT': min(original.get('WHEAT', 0), days * animals + _NF_BUFFER),
              'FERTILIZER': min(original.get('FERTILIZER', 0), fert_need + _NF_BUFFER)}
    allowed = ('WHEAT', 'FERTILIZER') if _NF_FERTILIZER else ('WHEAT',)
    prices = obs['market']['prices']
    products = sorted((p for p in allowed if stock.get(p, 0) > 0 and prices.get(p, 0) >= 2),
                      key=lambda p: (prices[p], p))
    proposed = [list(order) for order in orders]
    current_final, current_loss = original, loss
    sold = {}
    for item in products:
        if len(proposed) >= 10:
            break
        best = None
        for quantity in range(1, min(stock[item], sum(current_loss.values())) + 1):
            trial = proposed + [['SELL', item, quantity]]
            trial_stock, _, _ = _r97_market_stock(private['shed'], trial)
            final, lost = _r97_delivery(trial_stock, private, True)
            if any(final.get(p, 0) < floor for p, floor in floors.items()):
                continue
            if any(final.get(p, 0) < q for p, q in original.items() if p not in allowed):
                continue
            if sum(lost.values()) < sum(current_loss.values()):
                best = trial, final, lost, quantity
        if best is not None:
            proposed, current_final, current_loss, quantity = best
            sold[item] = quantity
    if not sold:
        return action
    saved = sum(loss.values()) - sum(current_loss.values())
    _NF_REPORT['nf_turns'] += 1
    _NF_REPORT['nf_sold'] += sum(sold.values())
    _NF_REPORT['nf_saved'] += saved
    _NF_EVENTS.append(dict(step=step, sold=sold, floors=floors,
                           original_final=original, predicted_final=current_final,
                           original_loss=loss, predicted_loss=current_loss))
    return dict(action, market=proposed)


def night_stock_agent(observation, configuration=None):
    if int(observation['step']) == 0:
        _NF_REPORT.update(nf_turns=0, nf_sold=0, nf_saved=0, nf_errors=0)
        _NF_EVENTS.clear()
    action = _NF_PARENT(observation, configuration)
    try:
        if configuration is None or all(configuration.get(k, v) == v for k, v in
                                         (('boardSize', 10), ('turnsPerDay', 24), ('shedCapacity', 100), ('maxMarketOrdersPerTurn', 10))):
            return _nf_apply(observation, action)
        return action
    except Exception:
        _NF_REPORT['nf_errors'] += 1
        return action


night_stock_agent.telemetry = _NF_REPORT
