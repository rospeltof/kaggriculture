"""Kaggriculture: top8_decem_112000345 + guardia de caja del d0 (reserve=5).
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
    action = guard_cash(obs, json.loads(json.dumps(_TRACE[step])), reserve=5)
    return guard_commitments(obs, action, _COMMIT)
