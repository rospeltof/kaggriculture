"""Capa para concatenar al agente público: tomate en suelo SE ya comprado.

No compra tierra ni modifica trabajadores del padre. Cuatro tiles por peón,
sin fertilizante, campaña finita y caja reservada para las obligaciones previas.
"""
_IF_PARENT=[v for v in list(globals().values()) if callable(v)][-1]
_IF_STATES={}
_IF_REPORT={}


def _if_projection(obs,groups):
    day=int(obs['step'])//24;seat=int(obs['player']);n=4*len(groups)
    inventory=float(obs['market']['inventory']['TOMATO'])
    shops=float(sum(s in ('PIZZA_SHOP','FARMERS_MARKET') for s in obs['town']['unlocked_shops']))
    unlocked=len(obs['town']['unlocked_shops']);supply={}
    for farm in obs['farms']:
        for row in farm['tiles']:
            for tile in row:
                if not isinstance(tile,dict) or tile.get('crop')!='TOMATO':continue
                birth=int(tile['planted_day'])
                supply[day]=supply.get(day,0)+max(0,int(tile.get('yield_units',0)))
                for d in range(max(day+1,birth+8),min(day+11,birth+11)+1):
                    units=2 if tile.get('fertilized_until_day',-1)>=d-1 else 1
                    supply[d]=supply.get(d,0)+units
    revenue=0.0
    for d in range(day,day+12):
        if d>day and d%3==0 and unlocked<8:shops+=.25;unlocked+=1
        inventory-=max(0,1+6*shops-2.4)
        inventory+=supply.get(d,0)
        if d in (day+9,day+11):
            for _ in range(2*n):
                revenue+=_r37_market_price('TOMATO',int(round(inventory)))
                inventory+=1
    native=_IMPL.chassis.players[seat];labor=0
    for age in (0,2,4,6,8,9,10,11):
        planned=_v219_native_day(native,day+age)
        baseline=max(len(a.get('hands',[])) for a in planned)
        if _V233_STATES.get(seat,{}).get('committed'):baseline+=2
        elif _V219_STATES.get(seat,{}).get('committed'):baseline+=3
        labor+=sum(_v219_fib(baseline+i) for i in range(len(groups)))
    return revenue,n*50+labor


def _if_groups(obs):
    farm=obs['farms'][int(obs['player'])]
    if _IF_SIZE==0 or len(farm['tiles'])!=10 or 'SE' not in farm['unlocked_quadrants']:return []
    groups=[[(5,7),(6,7),(6,8),(5,8)]]
    if _IF_SIZE==8:groups.append([(7,7),(8,7),(8,8),(7,8)])
    for group in groups:
        for x,y in group:
            tile=farm['tiles'][y][x]
            if tile is not None and not (isinstance(tile,dict) and tile.get('kind')=='WEED'):return []
    return groups


def _if_parent_ready(obs,action):
    day=int(obs['step'])//24;hour=int(obs['step'])%24;seat=int(obs['player'])
    native=_IMPL.chassis.players.get(seat)
    if native is None:return False
    planned=_v219_native_day(native,day)
    if any(o and o[0]=='HIRE' for a in planned[hour+1:] for o in a.get('market',[])):return False
    # Other committed overlays retain first claim on their indices and orders.
    for all_states in (_V233_STATES,_V219_STATES):
        other=all_states.get(seat,{})
        if other.get('committed') and other.get('requested_day')!=day:return False
    return True


def _if_request(obs,action,st):
    step=int(obs['step']);day=step//24;hour=step%24;age=day-_IF_START
    # R51 may hire during hours1..3 and rejects unowned workers. Let that
    # window close before adding our crew, so it keeps first claim on labor.
    if not 0<=age<=11 or not 4<=hour<=6 or st.get('requested_day')==day:return action
    if age in (1,3,5,7):return action
    if not st.get('committed') and (age!=0 or st.get('declined')):return action
    if not _if_parent_ready(obs,action):return action
    seat=int(obs['player']);farm=obs['farms'][seat];initial=not st.get('committed')
    groups=st.get('groups') if not initial else _if_groups(obs)
    if not groups:return action
    if initial:
        revenue,cost=_if_projection(obs,groups)
        _IF_REPORT['quotes'].append(dict(day=day,revenue=round(revenue),cost=round(cost)))
        if revenue<cost+_IF_MARGIN:
            st['declined']=True;_IF_REPORT['economic_declines']+=1;return action
    n=4*len(groups);orders=list(action.get('market') or [])
    extra=([['BUY_SEED','TOMATO',n]] if initial else [])+[['HIRE'] for _ in groups]
    if len(orders)+len(extra)>MAX_ORDERS:return action
    parent_hires=sum(bool(o) and o[0]=='HIRE' for o in orders)
    first=len(farm['hands'])+parent_hires+1
    cost=50*n*initial+sum(_v219_fib(farm['hires_today']+i) for i in range(parent_hires+len(groups)))
    # No speculative sale proceeds; reserve every current parent purchase as well.
    for o in orders:
        if not o:continue
        if o[0]=='HIRE':continue
        if o[0]=='BUY_LAND':return action
        if o[0]=='BUY_PRODUCT':cost+=int(o[2])*(int(obs['market']['prices'][o[1]])+10)
        elif o[0]=='BUY_ANIMAL':cost+=int(o[2])*{'COW':400,'SHEEP':500,'GOOSE':300}[o[1]]
        elif o[0]=='BUY_SEED':cost+=int(o[2])*{'WHEAT':10,'CARROT':20,'TOMATO':50,'STRAWBERRY':100,'MELON':80}[o[1]]
    if farm['money']<cost+4000:_IF_REPORT['budget_declines']+=1;return action
    paths=[]
    for i,group in enumerate(groups):
        _,spawn=_r62_input_start(obs,action,i)
        path=_sl_path(spawn,group)
        if initial:
            weeds=sum(isinstance(farm['tiles'][y][x],dict) for x,y in path)
            work=_sl_dist(spawn,path[0])+sum(_sl_dist(a,b) for a,b in zip(path,path[1:]))+8+weeds
            if work>23-hour:_IF_REPORT['time_declines']+=1;return action
        paths.append(path)
    st['pending']=dict(first=first,count=len(groups),initial=initial,paths=paths)
    st['groups']=groups;st['requested_day']=day
    _IF_REPORT['hire_requests']+=len(groups)
    if initial:_IF_REPORT['commit_requests']+=1
    result=dict(action,market=orders+extra)
    return result


def _if_worker(obs,actor,targets,st):
    day=int(obs['step'])//24;step=int(obs['step']);age=day-_IF_START
    farm=obs['farms'][int(obs['player'])];pos=tuple(farm['hands'][actor-1]);inv=obs['private']['inventories'][actor]
    home=_v219_home(pos);distance=_sl_dist(pos,home)
    if step>=718-distance and inv.get('TOMATO',0):return _v219_walk(pos,home) or ['PLACE','TOMATO',inv['TOMATO']]
    todo=[]
    for x,y in targets:
        tile=farm['tiles'][y][x];tomato=isinstance(tile,dict) and tile.get('crop')=='TOMATO' and tile.get('planted_day')==_IF_START
        if tomato and (x,y) not in st['seen']:
            st['seen'].add((x,y));_IF_REPORT['confirmed_plants']+=1
        command=None
        if tomato:
            # Unfertilized tomatoes survive one dry day. Separate watering
            # (even ages) from the two-unit harvests at ages9 and11, leaving
            # enough time to deliver before the shed's midnight overflow.
            if age in (0,2,4,6,8,10) and not tile.get('watered_today'):command=['WATER']
            elif age in (9,11) and tile.get('yield_units',0)>0:command=['HARVEST']
        elif age==0:
            if tile is None and obs['private']['seeds'].get('TOMATO',0)>0:command=['PLANT','TOMATO']
            elif isinstance(tile,dict) and tile.get('kind')=='WEED':command=['DIG']
        if command:todo.append(((x,y),command))
    if todo:
        target,command=min(todo,key=lambda pair:(_sl_dist(pos,pair[0]),targets.index(pair[0])))
        return _v219_walk(pos,target) or command
    if inv.get('TOMATO',0):return _v219_walk(pos,home) or ['PLACE','TOMATO',inv['TOMATO']]
    return ['PASS']


def infill_tomato_agent(observation,configuration=None):
    action=_IF_PARENT(observation,configuration)
    step=int(observation['step']);seat=int(observation['player']);day=step//24
    st=_IF_STATES.get(seat)
    if st is None or step<=st['step']:
        st=_IF_STATES[seat]=dict(step=-1,day=-1,workers={},seen=set(),last={})
        _IF_REPORT.clear();_IF_REPORT.update(commit_requests=0,committed=0,confirmed_plants=0,hire_requests=0,
            hires_confirmed=0,hire_shortfalls=0,harvested=0,economic_declines=0,budget_declines=0,time_declines=0,quotes=[])
    st['step']=step
    if not _ig_standard(configuration) or day<_IF_START:return action
    private=observation['private'];farm=observation['farms'][seat]
    for actor,(previous,before) in st['last'].items():
        if previous==step-1 and actor<len(private['inventories']):
            _IF_REPORT['harvested']+=max(0,private['inventories'][actor].get('TOMATO',0)-before)
    st['last']={}
    if st['day']!=day:st['day']=day;st['workers']={}
    pending=st.pop('pending',None)
    if pending:
        if len(farm['hands'])>=pending['first']+pending['count']-1:
            for i,path in enumerate(pending['paths']):st['workers'][pending['first']+i]=list(path)
            _IF_REPORT['hires_confirmed']+=pending['count']
            if pending['initial']:st['committed']=True;_IF_REPORT['committed']+=1
        else:_IF_REPORT['hire_shortfalls']+=1
    result=_if_request(observation,action,st)
    if st['workers']:
        commands=[result.get('farmer') or ['PASS'],*result.get('hands',[])]
        commands+=[['PASS'] for _ in range(len(farm['hands'])+1-len(commands))]
        for actor,targets in st['workers'].items():
            if actor>=len(commands):continue
            command=_if_worker(observation,actor,targets,st);commands[actor]=command
            if command==['HARVEST']:st['last'][actor]=(step,private['inventories'][actor].get('TOMATO',0))
        result=dict(result,farmer=commands[0],hands=commands[1:])
    if st.get('committed') and len(result['market'])<MAX_ORDERS:
        stock=projected_shed(result,FarmView(observation)).get('TOMATO',0)
        planned=sum(int(o[2]) for o in result['market'] if len(o)>=3 and o[:2]==['SELL','TOMATO'])
        if stock>planned:result=dict(result,market=result['market']+[['SELL','TOMATO',stock-planned]])
    return result


infill_tomato_agent.telemetry=_IF_REPORT
