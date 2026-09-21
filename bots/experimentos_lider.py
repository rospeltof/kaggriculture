"""Candidatos locales 2026-09-14; no sustituyen CAMPEONA_HOZ.

Las rutas proceden de replays aportados por el usuario. Selección sólo a partir
de observaciones visibles, sin conocer semillas ni tiendas futuras. No usa motor.
"""
from copy import deepcopy
from bots.meta.tape import _load

IDS = (107673304,107674284,107674293,107675268,107685970,107692988,107696961,107710951)
BRANCH_IDS = (107685970,107692988,107696961,107710951)
ACCESS = {(4,4),(4,5),(5,4),(5,5)}
PRODUCTS = ("WOOL","MILK","MELON","STRAWBERRY","EGG","TOMATO","CARROT")


def projected_shed(obs, action):
    """Sólo transferencias explícitas en shed, en orden de unidades del motor.

    No incluye auto-drop nocturno (sucede DESPUÉS del mercado) ni cosechas que
    siguen en la mano. Replica capacidad para DROP; no mira inventario rival.
    """
    farm=obs["farms"][obs["player"]]
    positions=[farm["farmer"]]+list(farm["hands"])
    invs=obs["private"]["inventories"]
    shed=dict(obs["private"]["shed"])
    for i,(pos,op) in enumerate(zip(positions,[action["farmer"]]+action["hands"])):
        if tuple(pos) not in ACCESS or not op:
            continue
        if op[0]=="DROP":
            for item,qty in invs[i].items():
                n=min(qty,max(0,100-sum(shed.values())))
                shed[item]=shed.get(item,0)+n
        elif op[0]=="PICKUP" and len(op)>=2:
            item=op[1];n=min(max(0,int(op[2] if len(op)>2 else 1)),shed.get(item,0))
            shed[item]=shed.get(item,0)-n
        elif op[0]=="PLACE" and len(op)>=2 and op[1] in PRODUCTS+("WHEAT","FERTILIZER"):
            item=op[1]
            n=min(max(0,int(op[2] if len(op)>2 else 1)),invs[i].get(item,0),max(0,100-sum(shed.values())))
            shed[item]=shed.get(item,0)+n
    return shed


def liquidate(obs,action):
    """Adelanta ventas de no-insumos conservando las demás órdenes de la ruta."""
    shed=projected_shed(obs,action)
    orders=[];covered=set()
    for order in action["market"]:
        if len(order)>=3 and order[0]=="SELL" and order[1] in PRODUCTS:
            item=order[1]
            if item not in covered:
                orders.append(["SELL",item,max(0,int(shed.get(item,0)))])
                covered.add(item)
        else:
            orders.append(order)
    for item in PRODUCTS:
        if item not in covered and shed.get(item,0)>0 and len(orders)<10:
            orders.append(["SELL",item,int(shed[item])])
    action["market"]=orders
    return action


def make(kind):
    state={"route":107685970}
    if kind=="warmstart10":
        from bots.chassis import make_agent
        from bots.arquetipos import CAMPEONA_HOZ
        planner=make_agent(dict(CAMPEONA_HOZ))
    def agent(obs):
        step=int(obs.get("step",obs["day"]*24+obs["hour"]))
        if kind=="warmstart10":
            if step>=240:
                return planner(obs)
            return deepcopy(_load("maj_107710951")[step])
        if step==0:
            state["route"]=107685970
        shops=obs.get("town",{}).get("unlocked_shops",[])
        if step==72:
            first=shops[0] if shops else None
            if first=="PET_CAFE":
                state["route"]=107685970
            elif first in ("BAKERY","BRUNCH_SPOT"):
                state["route"]=107692988
            else:
                state["route"]=107696961 if first=="YARN_STORE" else 107710951
        if step==144 and state["route"] in (107696961,107710951):
            state["route"]=107696961 if "YARN_STORE" in shops else 107710951
        action=deepcopy(_load(f"maj_{state['route']}")[min(step,719)])
        return liquidate(obs,action) if kind=="tree_liquid" else action
    return agent


tree=make("tree")
tree_liquid=make("tree_liquid")
warmstart10=make("warmstart10")
