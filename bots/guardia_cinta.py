"""Guardia de caja para cintas: evita el filo de navaja del alba del d1.

Hallazgo REAL (60 partidas de ladder de maj_107674293, 2026-09-21): las manos
del d1 predicen el resultado (0-2 manos: 0% WR en 12 partidas; 3: 23%; 4: 60%).
Los peones desaparecen cada noche y la cinta emite HIRE al alba con lo que le
quede; cuatro BUY_SEED WHEAT 1 en los pasos 18-21 la dejan en $0..$9 y fib(n)
necesita $7 para 4 manos. El panel local NO reproduce el fallo (71.5% local vs
40% real): los rivales reales mueven el mercado del d0, las cintas pasivas no.

Regla: en los pasos [0, until_step) se descartan las ordenes BUY_SEED/BUY_PRODUCT
que dejarian la caja por debajo de `reserve`. Fuera de ese tramo no interviene.
"""
SEED_COST = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50, "STRAWBERRY": 100, "MELON": 80}


def guard_cash(obs, action, reserve=12, until_step=24):
    step = int(obs.get("step", 0) or 0)
    if step >= until_step:
        return action
    money = float(obs["farms"][obs["player"]]["money"])
    prices = obs.get("market", {}).get("prices", {}) or {}
    out = []
    for o in action.get("market") or []:
        if isinstance(o, list) and o and o[0] in ("BUY_SEED", "BUY_PRODUCT") and len(o) >= 3:
            item, n = o[1], int(o[2])
            unit = SEED_COST.get(item, 0) if o[0] == "BUY_SEED" else float(prices.get(item, 0)) + 2
            cost = unit * n
            if money - cost < reserve:
                k = int(max(0, money - reserve) // unit) if unit > 0 else 0
                if k <= 0:
                    continue                      # descartar: dejaria la caja bajo la reserva
                o = [o[0], item, k]; cost = unit * k
            money -= cost
        out.append(o)
    action = dict(action); action["market"] = out
    return action


# ---------------------------------------------------------------------------
# Reintento de COMPROMISOS de capital (2026-09-22). Segunda clase de filo de
# navaja: la cinta 107606658 emite BUY_LAND en el paso 149 con \$807 en caja
# (la original tenia \$1.819); falla, y todo lo que sigue asume un cuadrante
# que no existe: 4 animales en vez de 11, 17 plantas en vez de 32. Sin
# recuperacion posible porque la cinta nunca vuelve a intentarlo.
# Regla: si la cinta emitio BUY_LAND/BUY_ANIMAL y en el paso siguiente el estado
# no lo refleja, se reemite cada paso (antes que el resto) hasta que entre o
# hasta `max_retry` pasos despues. Si la compra entro a la primera, no cambia
# NADA: es estrictamente dominante para la cinta.
# ---------------------------------------------------------------------------
LAND_COST = (1000, 2000, 4000)
ANIMAL_COST = {"GOOSE": 300, "COW": 400, "SHEEP": 500}


def _animales(obs, item):
    """Total de `item` poseidos: en tiles, en shed y en manos. El shed solo no
    sirve: la cinta hace PICKUP del animal en el mismo paso en que lo compra."""
    farm = obs["farms"][obs["player"]]; priv = obs.get("private", {}) or {}
    n = sum(1 for row in farm["tiles"] for t in row if isinstance(t, dict) and t.get("animal") == item)
    n += (priv.get("shed", {}) or {}).get(item, 0)
    n += sum(i.get(item, 0) for i in (priv.get("inventories") or []))
    return n


def guard_commitments(obs, action, state, max_retry=48):
    """`state` es un dict persistente del agente (se crea vacio en el paso 0)."""
    step = int(obs.get("step", 0) or 0)
    farm = obs["farms"][obs["player"]]
    quads = len(farm.get("unlocked_quadrants") or [])
    if step == 0 or "pend" not in state:
        state.clear(); state.update(pend=[])
    # 1) comprobar si los compromisos del paso anterior entraron
    nuevos = []
    for c in state["pend"]:
        if c["tipo"] == "BUY_LAND":
            ok = quads > c["antes"]
        else:
            ok = _animales(obs, c["item"]) > c["antes"]
        if not ok and step - c["step"] <= max_retry:
            nuevos.append(c)
    state["pend"] = nuevos
    # 2) reemitir los pendientes (primero) si hay caja
    money = float(farm["money"]); extra = []
    for c in state["pend"]:
        cost = LAND_COST[min(quads - 1, 2)] if c["tipo"] == "BUY_LAND" else ANIMAL_COST.get(c["item"], 0)
        if money >= cost and not any(o and o[0] == c["tipo"] and (c["tipo"] == "BUY_LAND" or o[1] == c["item"])
                                     for o in action.get("market") or []):
            extra.append(["BUY_LAND"] if c["tipo"] == "BUY_LAND" else ["BUY_ANIMAL", c["item"], 1])
            money -= cost
    # 3) registrar los compromisos que emite la cinta HOY
    for o in action.get("market") or []:
        if not (isinstance(o, list) and o):
            continue
        if o[0] == "BUY_LAND":
            state["pend"].append(dict(tipo="BUY_LAND", step=step, antes=quads))
        elif o[0] == "BUY_ANIMAL" and len(o) >= 2:
            state["pend"].append(dict(tipo="BUY_ANIMAL", item=o[1], step=step, antes=_animales(obs, o[1])))
    if extra:
        action = dict(action); action["market"] = (extra + list(action.get("market") or []))[:10]
    return action


# ---------------------------------------------------------------------------
# Calibracion automatica de la reserva (2026-09-23). `reserve=6` fijo dejaba a
# 72 de 79 cintas candidatas por debajo de lo que necesitan: casi todas emiten
# 5 HIRE al alba del d1 y usan 4 manos, que cuestan fib = 1+1+2+3 = $7. La
# reserva correcta es el coste de las manos que la cinta USA en el d1, +1.
# Para 107570947 da 8, el valor de la submission 56449108.
# ---------------------------------------------------------------------------
_FIB = (1, 1, 2, 3, 5, 8, 13, 21, 34, 55)


def reserve_auto(trace, margin=1):
    """Reserva de caja que garantiza las manos del d1 de una cinta."""
    usadas = max(len(trace[s].get("hands") or []) for s in range(25, 48))
    pedidas = sum(1 for o in trace[24].get("market") or [] if o and o[0] == "HIRE")
    k = min(usadas, pedidas)
    return (sum(_FIB[:k]) + margin) if k else 0
