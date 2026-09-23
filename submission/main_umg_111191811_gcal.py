"""Kaggriculture: top4_umg_111191811 + guardia de caja del d0 (reserve=8).
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
