"""Sonda 004: la rampa de CARE en animales de intervalo largo.

Hipótesis (extrapolando S4.4 del ganso a cow/sheep): el banco de care crece
+1 por noche fed+cared TAMBIÉN durante los días previos al primer yield.
Entonces, colocados el día 0 con feed+care diario:
  SHEEP (1er yield d6): banco 5 al alba d5 -> 1ª producción = min(6, 1+5) = 6 lanas
  COW   (1er yield d8): banco 7           -> 1ª producción = min(6, 1+7) = 6 leches (2 desperdiciadas por cap)
  (el ganso ya lo confirmó P2: 1+3 = 4 = justo su cap)
"""
import sys

sys.path.insert(0, "/Users/rospel/Desktop/kaggriculture")
from lab import run_scenario, obs_at, tile_at

script = {
    0: {"farmer": ["NORTH"], "market": [["BUY_ANIMAL", "COW", 1], ["BUY_ANIMAL", "SHEEP", 1], ["BUY_PRODUCT", "WHEAT", 22]]},
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
    12: {"farmer": ["CARE"]},
    13: {"farmer": ["SOUTH"]},
    14: {"farmer": ["WEST"]},
    15: {"farmer": ["PLACE", "SHEEP"]},
    16: {"farmer": ["FEED"]},
    17: {"farmer": ["CARE"]},
}
for d in range(1, 11):
    base = 24 * d
    script[base] = {"farmer": ["PICKUP", "WHEAT", 2]}
    script[base + 1] = {"farmer": ["NORTH"]}
    script[base + 2] = {"farmer": ["FEED"]}
    script[base + 3] = {"farmer": ["CARE"]}
    script[base + 4] = {"farmer": ["SOUTH"]}
    script[base + 5] = {"farmer": ["WEST"]}
    script[base + 6] = {"farmer": ["FEED"]}
    script[base + 7] = {"farmer": ["CARE"]}

env = run_scenario(script, n_steps=260)
for d in range(4, 11):
    o = obs_at(env, 24 * d)
    cow = tile_at(o, 4, 3)
    sheep = tile_at(o, 3, 4)
    print(
        f"alba d{d}: cow yield={cow.get('yield_units')} banco={cow.get('pending_care_bonus')} | "
        f"sheep yield={sheep.get('yield_units')} banco={sheep.get('pending_care_bonus')}"
    )
