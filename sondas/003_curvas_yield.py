"""Sonda 003: curvas de yield día a día de todos los cultivos y animales.

Para cada cultivo: plantar día 0 en (4,4), regar a diario, snapshot del tile
tras el riego de cada día. Variantes fertilizadas para one-time crops
(PICKUP FERTILIZER en la mañana del día de fertilizar — el auto-drop nocturno
devuelve el inventario al shed, así que hay que recogerlo el mismo día).

Predicciones (motor L431-444, L786-802):
  WHEAT  sin fert: 1,1,2,3,4 (pico 4 en edad 4), decay desde día 5 h0
  WHEAT  fert d2:  1,1,3,5,6 (cap 6 en edad 4)
  CARROT sin fert: 1,1,2,3 (pico 3 en edad 3), decay desde día 4
  CARROT fert d2:  1,1,3,4 (cap 4 en edad 3)
  MELON  sin fert: 1×6, luego 2,3,4,5,6 (cap 6 en edad 10), decay desde día 13
  MELON  fert d6:  cap 6 en edad 8 (la página lo afirma; verificar)
  TOMATO:     producciones en los amaneceres de edades 8,9,10,11 (cap 4)
  STRAWBERRY: producciones en los amaneceres de edades 10,12,14,16
  COW: primera leche amanecer día 8, luego cada 2 | SHEEP: lana día 6, luego cada 3
"""
import sys

sys.path.insert(0, "/Users/rospel/Desktop/kaggriculture")
from lab import run_scenario, obs_at, tile_at


def curva_cultivo(crop, days, fert_day=None):
    market = [["BUY_SEED", crop, 1]]
    if fert_day is not None:
        market.append(["BUY_PRODUCT", "FERTILIZER", 1])
    script = {
        0: {"market": market},
        1: {"farmer": ["PLANT", crop]},
        2: {"farmer": ["WATER"]},
    }
    for d in range(1, days):
        base = 24 * d
        if fert_day is not None and d == fert_day:
            script[base] = {"farmer": ["PICKUP", "FERTILIZER"]}
            script[base + 1] = {"farmer": ["FERTILIZE"]}
        script[base + 2] = {"farmer": ["WATER"]}
    env = run_scenario(script, n_steps=24 * days + 6)
    curve = []
    for d in range(days):
        o = obs_at(env, 24 * d + 3)
        t = tile_at(o, 4, 4)
        if isinstance(t, dict):
            curve.append((d, t.get("kind")[0], t.get("yield_units")))
        else:
            curve.append((d, "-", None))
    return curve


def fmt(curve):
    return " ".join(f"d{d}:{y if k == 'P' else k}" for d, k, y in curve)


for crop, days, fert in [
    ("WHEAT", 8, None), ("WHEAT", 6, 2),
    ("CARROT", 7, None), ("CARROT", 6, 2),
    ("MELON", 15, None), ("MELON", 15, 6),
    ("TOMATO", 14, None), ("STRAWBERRY", 18, None),
]:
    label = f"{crop}{f' fert d{fert}' if fert else ''}"
    print(f"{label:16s} {fmt(curva_cultivo(crop, days, fert))}")

print()
print("=== COW (pasture 4,3) y SHEEP (pasture 3,4), alimentados a diario ===")
script = {
    0: {"farmer": ["NORTH"], "market": [["BUY_ANIMAL", "COW", 1], ["BUY_ANIMAL", "SHEEP", 1], ["BUY_PRODUCT", "WHEAT", 20]]},
    1: {"farmer": ["BUILD_PASTURE"]},
    2: {"farmer": ["SOUTH"]},
    3: {"farmer": ["WEST"]},
    4: {"farmer": ["BUILD_PASTURE"]},
    5: {"farmer": ["EAST"]},
    6: {"farmer": ["PICKUP", "COW"]},
    7: {"farmer": ["PICKUP", "SHEEP"]},
    8: {"farmer": ["PICKUP", "WHEAT", 2]},
    9: {"farmer": ["NORTH"]},
    10: {"farmer": ["PLACE", "COW"]},
    11: {"farmer": ["FEED"]},
    12: {"farmer": ["SOUTH"]},
    13: {"farmer": ["WEST"]},
    14: {"farmer": ["PLACE", "SHEEP"]},
    15: {"farmer": ["FEED"]},
}
for d in range(1, 11):
    base = 24 * d
    script[base] = {"farmer": ["PICKUP", "WHEAT", 2]}
    script[base + 1] = {"farmer": ["NORTH"]}
    script[base + 2] = {"farmer": ["FEED"]}
    script[base + 3] = {"farmer": ["SOUTH"]}
    script[base + 4] = {"farmer": ["WEST"]}
    script[base + 5] = {"farmer": ["FEED"]}
env = run_scenario(script, n_steps=260)
for d in range(4, 11):
    o = obs_at(env, 24 * d)
    cow = tile_at(o, 4, 3)
    sheep = tile_at(o, 3, 4)
    print(f"  amanecer d{d}: cow yield={cow.get('yield_units')} | sheep yield={sheep.get('yield_units')}")
