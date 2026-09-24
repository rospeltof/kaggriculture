"""Kaggriculture: top11_seek_112344897 + guardia de caja del d0 (reserve=8).
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
