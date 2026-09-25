# Incremental sheep project over the public Apache-2.0 agent.
# No land purchase or reassignment of the parent's actors.
_SG_PARENT = [v for v in list(globals().values()) if callable(v)][-1]
_SG_STATE = {}
_SG_REPORT = {}


def _sg_groups(obs):
    if _SG_SIZE == 0:
        return []
    farm = obs['farms'][int(obs['player'])]
    if 'SE' not in farm['unlocked_quadrants']:
        return []
    groups = [[(x, 7) for x in range(5, 5+min(_SG_SIZE, 3))]]
    if _SG_SIZE == 6:
        groups.append([(x, 8) for x in range(5, 8)])
    for group in groups:
        for x, y in group:
            tile = farm['tiles'][y][x]
            if tile is not None and not (isinstance(tile, dict) and tile.get('kind') == 'WEED'):
                return []
    return groups


def _sg_quote(obs, groups):
    day = int(obs['step']) // 24
    seat = int(obs['player'])
    n = sum(map(len, groups))
    inventory = float(obs['market']['inventory']['WOOL'])
    yarn = obs['town']['unlocked_shops'].count('YARN_STORE')
    existing = {}
    private = obs['private']
    own_unplaced = int(private['shed'].get('SHEEP', 0))+sum(int(inv.get('SHEEP', 0)) for inv in private['inventories'])
    own_held_wool = int(private['shed'].get('WOOL', 0))+sum(int(inv.get('WOOL', 0)) for inv in private['inventories'])
    inventory += own_held_wool
    # Already purchased parent animals are committed supply, not hypothetical
    # future investment. Assume placement today, before our new project begins.
    for d in range(day+6, 30, 3):
        existing[d] = own_unplaced*(6 if d == day+6 else 4)
    for farm in obs['farms']:
        for row in farm['tiles']:
            for tile in row:
                if not isinstance(tile, dict) or tile.get('animal') != 'SHEEP':
                    continue
                inventory += int(tile.get('yield_units', 0))
                born = int(tile['placed_day'])
                for d in range(day+1, 30):
                    if d >= born+6 and (d-born-6) % 3 == 0:
                        existing[d] = existing.get(d, 0) + (6 if d == born+6 else 4)
    revenue = 0
    # Only already visible yarn stores. No speculative future shop demand.
    for d in range(day, 30):
        inventory -= 1+12*yarn
        inventory += existing.get(d, 0)
        if d >= day+6 and (d-day-6) % 3 == 0:
            # Discount the initial care ramp: construction may consume its first day.
            for _ in range(n*(5 if d == day+6 else 3)):
                price = _r37_market_price('WOOL', int(round(inventory)))
                revenue += price
                if price > 1:
                    inventory += 1
    last = day+6+3*((29-day-6)//3)
    feed = n*(last-day)*(int(obs['market']['prices']['WHEAT'])+5)
    native = _IMPL.chassis.players[seat]
    labor = 0
    for d in range(day, last+1):
        baseline = max(len(a.get('hands', [])) for a in _v219_native_day(native, d))
        if _V233_STATES.get(seat, {}).get('committed'):
            baseline += 2
        elif _V219_STATES.get(seat, {}).get('committed'):
            baseline += 3
        labor += sum(_v219_fib(baseline+i) for i in range(len(groups)))
    return dict(revenue=round(revenue), animals=n*500, feed=feed, labor=labor,
                cost=n*500+feed+labor, yarn=yarn, last_yield_day=last,
                own_unplaced_sheep=own_unplaced, own_held_wool=own_held_wool)


def _sg_ready(obs):
    day, hour = divmod(int(obs['step']), 24)
    seat = int(obs['player'])
    native = _IMPL.chassis.players.get(seat)
    if native is None:
        return False
    if any(o and o[0] == 'HIRE' for a in _v219_native_day(native, day)[hour+1:] for o in a.get('market', [])):
        return False
    for states in (_V219_STATES, _V233_STATES):
        other = states.get(seat, {})
        if other.get('committed') and other.get('requested_day') != day:
            return False
    return True


def _sg_request(obs, action, st):
    day, hour = divmod(int(obs['step']), 24)
    if not 4 <= hour <= 6 or st.get('requested_day') == day or not _sg_ready(obs):
        return action
    initial = not st.get('committed')
    if initial and (day != _SG_START or st.get('declined')):
        return action
    groups = _sg_groups(obs) if initial else st['groups']
    if not groups:
        return action
    if initial:
        quote = _sg_quote(obs, groups)
        _SG_REPORT['quotes'].append(quote)
        if quote['yarn'] < 2 or quote['revenue'] < quote['cost']+_SG_MARGIN:
            st['declined'] = True
            _SG_REPORT['economic_declines'] += 1
            return action
        st['last_yield_day'] = quote['last_yield_day']
    farm = obs['farms'][int(obs['player'])]
    last = st['last_yield_day']
    if not initial and day >= last:
        groups = [group for group in groups if any(
            isinstance(farm['tiles'][y][x], dict) and farm['tiles'][y][x].get('yield_units', 0)
            for x, y in group)]
        if not groups:
            return action
    n = sum(map(len, groups))
    food = n if day < last else 0
    orders = list(action.get('market') or [])
    extra = ([['BUY_ANIMAL', 'SHEEP', n]] if initial else [])
    if food:
        extra.append(['BUY_PRODUCT', 'WHEAT', food])
    extra += [['HIRE'] for _ in groups]
    if len(orders)+len(extra) > MAX_ORDERS:
        return action
    parent_hires = sum(bool(o) and o[0] == 'HIRE' for o in orders)
    cost = n*500*initial + food*(int(obs['market']['prices']['WHEAT'])+10)
    incoming = n*initial+food
    cost += sum(_v219_fib(farm['hires_today']+i) for i in range(parent_hires+len(groups)))
    for order in orders:
        if not order or order[0] == 'HIRE':
            continue
        if order[0] == 'BUY_LAND':
            return action
        if order[0] == 'BUY_PRODUCT':
            cost += int(order[2])*(int(obs['market']['prices'][order[1]])+10)
            incoming += int(order[2])
        elif order[0] == 'BUY_ANIMAL':
            cost += int(order[2])*{'SHEEP': 500, 'COW': 400, 'GOOSE': 300}[order[1]]
            incoming += int(order[2])
        elif order[0] == 'BUY_SEED':
            cost += int(order[2])*{'WHEAT': 10, 'CARROT': 20, 'TOMATO': 50, 'STRAWBERRY': 100, 'MELON': 80}[order[1]]
    if farm['money'] < cost+(4000 if initial else 1000):
        _SG_REPORT['budget_declines'] += 1
        return action
    if sum(projected_shed(action, FarmView(obs)).values())+incoming > 100:
        _SG_REPORT['capacity_declines'] += 1
        return action
    # Initial construction must leave time to place and feed every new animal.
    for index, group in enumerate(groups):
        if not initial:
            continue
        _, spawn = _r62_input_start(obs, action, index)
        path = _sl_path(spawn, group)
        travel = _sl_dist(spawn, path[0])+sum(_sl_dist(a, b) for a, b in zip(path, path[1:]))
        weeds = sum(isinstance(farm['tiles'][y][x], dict) for x, y in group)
        if 2+travel+3*len(group)+weeds > 23-hour:
            _SG_REPORT['time_declines'] += 1
            return action
    st['pending'] = dict(first=len(farm['hands'])+parent_hires+1, groups=groups,
                         initial=initial, animals=n if initial else 0)
    st['requested_day'] = day
    if initial:
        st['groups'] = groups
    _SG_REPORT['hire_requests'] += len(groups)
    _SG_REPORT['feed_requested'] += food
    return dict(action, market=orders+extra)


def _sg_worker(obs, actor, targets, last):
    day, hour = divmod(int(obs['step']), 24)
    farm = obs['farms'][int(obs['player'])]
    pos = tuple(farm['hands'][actor-1])
    inv = obs['private']['inventories'][actor]
    home = _v219_home(pos)
    cargo = [item for item in ('WOOL', 'FERTILIZER') if inv.get(item, 0)]
    deadline = 22 if day == 29 else 23
    if cargo and hour >= deadline-_sl_dist(pos, home)-(len(cargo)-1):
        return _v219_walk(pos, home) or ['PLACE', cargo[0], inv[cargo[0]]]
    missing = sum(not (isinstance(farm['tiles'][y][x], dict) and farm['tiles'][y][x].get('animal') == 'SHEEP') for x, y in targets)
    if missing and day == _SG_START and not inv.get('SHEEP', 0) and obs['private']['shed'].get('SHEEP', 0):
        return _v219_walk(pos, home) or ['PICKUP', 'SHEEP', min(missing, obs['private']['shed']['SHEEP'])]
    hungry = sum(not (isinstance(farm['tiles'][y][x], dict) and farm['tiles'][y][x].get('fed_today')) for x, y in targets)
    if day < last and hungry and not inv.get('WHEAT', 0) and obs['private']['shed'].get('WHEAT', 0):
        return _v219_walk(pos, home) or ['PICKUP', 'WHEAT', min(hungry, obs['private']['shed']['WHEAT'])]
    essential, care, productive = [], [], []
    for target in targets:
        x, y = target
        tile = farm['tiles'][y][x]
        command = None
        if day == _SG_START:
            if tile is None:
                command = ['BUILD_PASTURE']
            elif isinstance(tile, dict) and tile.get('kind') == 'WEED':
                command = ['DIG']
            elif isinstance(tile, dict) and tile.get('kind') == 'PASTURE' and not tile.get('animal') and inv.get('SHEEP', 0):
                command = ['PLACE', 'SHEEP']
        sheep = isinstance(tile, dict) and tile.get('animal') == 'SHEEP'
        if sheep and day < last and not tile.get('fed_today') and inv.get('WHEAT', 0):
            command = ['FEED']
        if command:
            essential.append((target, command))
        if sheep:
            if day < last-1 and not tile.get('cared_today'):
                care.append((target, ['CARE']))
            if tile.get('yield_units', 0):
                productive.append((target, ['HARVEST']))
            elif day < last and tile.get('fertilizer_available'):
                productive.append((target, ['COLLECT_FERTILIZER']))
    mandatory = essential if day == _SG_START and essential else essential+care
    # Do not start optional work whose cargo cannot reach a shed today. Waiting
    # on the animal is safer than forcing an unplanned midnight deposit.
    deliverable = []
    for target, command in productive:
        item = 'WOOL' if command == ['HARVEST'] else 'FERTILIZER'
        drops = len(set(cargo) | {item})
        work = _sl_dist(pos, target)+1+_sl_dist(target, _v219_home(target))+drops
        if work <= deadline-hour+1:
            deliverable.append((target, command))
    productive = deliverable
    harvests = [task for task in productive if task[1] == ['HARVEST']]
    tasks = mandatory or harvests or productive
    if tasks:
        target, command = min(tasks, key=lambda pair: (_sl_dist(pos, pair[0]), targets.index(pair[0])))
        if cargo and _sl_dist(pos, target)+1+_sl_dist(target, _v219_home(target))+len(cargo) > deadline-hour+1:
            return _v219_walk(pos, home) or ['PLACE', cargo[0], inv[cargo[0]]]
        return _v219_walk(pos, target) or command
    if cargo:
        return _v219_walk(pos, home) or ['PLACE', cargo[0], inv[cargo[0]]]
    return ['PASS']


def sheep_space_agent(observation, configuration=None):
    action = _SG_PARENT(observation, configuration)
    step = int(observation['step'])
    day = step//24
    seat = int(observation['player'])
    st = _SG_STATE.get(seat)
    if st is None or step <= st['step']:
        st = _SG_STATE[seat] = dict(step=-1, day=-1, workers={}, work={}, credit={'WOOL': 0, 'FERTILIZER': 0}, placed=set())
        _SG_REPORT.clear()
        _SG_REPORT.update(committed=0, hires_confirmed=0, hire_shortfalls=0, purchase_shortfalls=0,
                          hire_requests=0, feed_requested=0, economic_declines=0, budget_declines=0,
                          capacity_declines=0, time_declines=0, sheep_placed=0, wool_harvested=0,
                          fertilizer_collected=0, feed_sales_reserved=0, quotes=[])
    st['step'] = step
    if not _ig_standard(configuration) or day < _SG_START:
        return action
    private = observation['private']
    farm = observation['farms'][seat]
    for actor, (previous, item, before) in st['work'].items():
        if previous == step-1 and actor < len(private['inventories']):
            gain = max(0, private['inventories'][actor].get(item, 0)-before)
            st['credit'][item] += gain
            _SG_REPORT['wool_harvested' if item == 'WOOL' else 'fertilizer_collected'] += gain
    st['work'] = {}
    if st['day'] != day:
        st['day'] = day
        st['workers'] = {}
    pending = st.pop('pending', None)
    if pending:
        if pending['initial'] and private['shed'].get('SHEEP', 0) < pending['animals']:
            _SG_REPORT['purchase_shortfalls'] += 1
            st['declined'] = True
        elif len(farm['hands']) < pending['first']+len(pending['groups'])-1:
            _SG_REPORT['hire_shortfalls'] += 1
            st['declined'] = True
        else:
            st['workers'] = {pending['first']+i: group for i, group in enumerate(pending['groups'])}
            _SG_REPORT['hires_confirmed'] += len(pending['groups'])
            if pending['initial']:
                st['committed'] = True
                _SG_REPORT['committed'] += 1
    result = _sg_request(observation, action, st)
    if not st.get('committed') and not st.get('pending'):
        return action
    commands = [result.get('farmer') or ['PASS'], *result.get('hands', [])]
    commands += [['PASS'] for _ in range(len(farm['hands'])+1-len(commands))]
    reserve = 0
    for actor, targets in st['workers'].items():
        command = _sg_worker(observation, actor, targets, st['last_yield_day'])
        commands[actor] = command
        item = {'HARVEST': 'WOOL', 'COLLECT_FERTILIZER': 'FERTILIZER'}.get(command[0])
        if item:
            st['work'][actor] = step, item, private['inventories'][actor].get(item, 0)
        for x, y in targets:
            tile = farm['tiles'][y][x]
            if isinstance(tile, dict) and tile.get('animal') == 'SHEEP' and (x, y) not in st['placed']:
                st['placed'].add((x, y))
                _SG_REPORT['sheep_placed'] += 1
        if day < st['last_yield_day']:
            hungry = sum(not (isinstance(farm['tiles'][y][x], dict) and farm['tiles'][y][x].get('fed_today')) for x, y in targets)
            carried = private['inventories'][actor].get('WHEAT', 0)
            picked = int(command[2]) if command[:2] == ['PICKUP', 'WHEAT'] else 0
            reserve += max(0, hungry-carried-picked)
    result = dict(result, farmer=commands[0], hands=commands[1:])
    stock = projected_shed(result, FarmView(observation))
    allowed_wheat = max(0, stock.get('WHEAT', 0)-reserve)
    orders = []
    for order in result.get('market', []):
        if reserve and len(order) >= 3 and order[:2] == ['SELL', 'WHEAT']:
            amount = min(int(order[2]), allowed_wheat)
            _SG_REPORT['feed_sales_reserved'] += int(order[2])-amount
            allowed_wheat -= amount
            if amount:
                orders.append(['SELL', 'WHEAT', amount])
        else:
            orders.append(order)
    if st.get('committed'):
        for item in ('WOOL', 'FERTILIZER'):
            planned = sum(int(o[2]) for o in orders if len(o) >= 3 and o[:2] == ['SELL', item])
            qty = min(st['credit'][item], max(0, stock.get(item, 0)-planned))
            if qty and len(orders) < MAX_ORDERS:
                orders.append(['SELL', item, qty])
                st['credit'][item] -= qty
    return dict(result, market=orders)
