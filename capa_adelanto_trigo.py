"""Move an existing wheat purchase earlier and repay its native commitment."""
_BW_PARENT = [v for v in list(globals().values()) if callable(v)][-1]
_BW_ROUTE = _IMPL.chassis._route_action
_BW_PENDING = {}
_BW_REPAY = None
_BW_REPORT = {}
_BW_EVENTS = []


def _bw_route_action(route, step):
    action = _BW_ROUTE(route, step)
    debt = _BW_REPAY
    if debt is None or step != debt['due'] or route != debt['route']:
        return action
    orders = action.get('market') or []
    index = debt['native_index']
    if index >= len(orders) or orders[index] != ['BUY_PRODUCT','WHEAT',debt['native_quantity']]:
        return action
    # This method can be consulted by planners too. It has no economic state
    # side effects: every call returns the same adjusted copy, never the tape.
    debt['hook_calls'] += 1
    result = copy.deepcopy(action)
    result['market'][index][2] -= debt['bought']
    return result


_IMPL.chassis._route_action = _bw_route_action


def _bw_advance(obs, action):
    step = int(obs['step']); player = int(obs['player'])
    if not 288 <= step <= 693 or step%24 > 21:
        return action
    orders = action.get('market') or []
    if len(orders) >= 10 or any(o[:2] in (['BUY_PRODUCT','WHEAT'],['SELL','WHEAT']) for o in orders):
        return action
    future = _sr_tape(player,step+1)
    matches = [(i,o) for i,o in enumerate(future.get('market') or [])
               if len(o)>=3 and o[:2]==['BUY_PRODUCT','WHEAT']]
    if len(matches)!=1 or int(matches[0][1][2])<20:
        return action
    index,order = matches[0]; planned = int(order[2])
    following = _sr_tape(player,step+2)
    sell = sum(int(o[2]) for o in following.get('market',[]) if len(o)>=3 and o[:2]==['SELL','WHEAT'])
    if sell < (planned+1)//2:
        return action
    if any(c and c[0] in ('DROP','PLACE') for c in [future.get('farmer'),*(future.get('hands') or [])]):
        return action
    _BW_REPORT['eligible'] += 1
    farm, private = _r127_fields(obs,action)
    stock, original_buys, _ = _r97_market_stock(private['shed'],orders)
    quantity = min(planned,max(0,100-sum(stock.values())))
    if not quantity:
        _BW_REPORT['capacity_declines'] += 1
        return action
    proposed = copy.deepcopy(orders)+[['BUY_PRODUCT','WHEAT',quantity]]
    budget = dict(obs,farms=[dict(f) for f in obs['farms']])
    budget['farms'][player]['money'] -= 3000
    if not _r97_budget(budget,proposed):
        _BW_REPORT['budget_declines'] += 1
        return action
    after, buys, _ = _r97_market_stock(private['shed'],proposed)
    if any(buys.get(i,0)<q for i,q in original_buys.items()) or buys.get(len(orders),0)!=quantity:
        _BW_REPORT['capacity_declines'] += 1
        return action
    route = 2 if step+1>=648 else _IMPL.chassis.players[player]['route']
    event = dict(kind='advance',step=step,due=step+1,route=route,native_index=index,
                 native_quantity=planned,quantity=quantity,before_wheat=stock.get('WHEAT',0),
                 predicted_after=after.get('WHEAT',0),projected_shed=copy.deepcopy(private['shed']),
                 original=copy.deepcopy(orders),modified=copy.deepcopy(proposed),
                 native_next=copy.deepcopy(future),next_sale=sell,hook_calls=0)
    _BW_PENDING[player] = event
    _BW_EVENTS.append(event)
    _BW_REPORT['advances'] += 1; _BW_REPORT['requested'] += quantity
    return dict(action,market=proposed)


def wheat_advance_agent(observation,configuration=None):
    global _BW_REPAY
    step = int(observation['step']); player = int(observation['player'])
    if step==0:
        _BW_PENDING.clear(); _BW_EVENTS.clear(); _BW_REPAY=None; _BW_REPORT.clear()
        _BW_REPORT.update(eligible=0,advances=0,requested=0,bought=0,cancelled=0,
                          errors=0,cancel_errors=0,observation_errors=0,
                          capacity_declines=0,budget_declines=0)
    debt = _BW_PENDING.pop(player,None)
    _BW_REPAY = None
    if debt is not None:
        bought = int(observation['private']['shed'].get('WHEAT',0))-debt['before_wheat']
        debt['observed_step']=step; debt['bought']=bought
        if step!=debt['due'] or not 0<=bought<=debt['quantity']:
            _BW_REPORT['observation_errors'] += 1
        else:
            _BW_REPAY=debt; _BW_REPORT['bought'] += bought
    try:
        result = _BW_PARENT(observation,configuration)
    finally:
        _BW_REPAY = None
    if debt is not None:
        debt['final_market']=copy.deepcopy(result.get('market') or [])
        if debt['hook_calls']:
            _BW_REPORT['cancelled'] += debt['bought']
        else:
            _BW_REPORT['cancel_errors'] += 1
        return result
    if not _BW_ENABLED:
        return result
    try:
        return _bw_advance(observation,result)
    except Exception:
        _BW_REPORT['errors'] += 1
        return result
