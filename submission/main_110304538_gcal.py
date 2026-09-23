"""Kaggriculture: top2_majkel1337_110304538 + guardia de caja del d0 (reserve=8).
Autocontenido; generado por empaquetar_cinta_guard.py. No consulta red ni archivos.
"""
import base64
import gzip
import json

# ---- bots/guardia_cinta.py (copia literal) ----
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

# ---- fin guardia ----

_TRACE = json.loads(gzip.decompress(base64.b64decode('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')))
_COMMIT = {}


def agent(obs, config=None):
    step = int(obs.get("step", 0) or 0)
    if step == 0:
        _COMMIT.clear()
    if step >= len(_TRACE):
        return {"farmer": ["PASS"], "hands": [], "market": []}
    action = guard_cash(obs, json.loads(json.dumps(_TRACE[step])), reserve=8)
    return guard_commitments(obs, action, _COMMIT)
