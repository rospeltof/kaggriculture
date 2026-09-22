"""Kaggriculture: top_majkel1337_107570947 + guardia de caja del d0 (reserve=8).
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
