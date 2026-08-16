import sys

sys.path.insert(0, "/Users/rospel/Desktop/kaggriculture")
from lab import run_scenario, obs_at, tile_at


def farmer_pos(o, p=0):
    return list(o["farms"][p]["farmer"])


print("=== SONDA A: ¿el granjero reaparece en el shed al inicio del día? ===")
env = run_scenario({i: {"farmer": ["NORTH"]} for i in range(4)}, n_steps=30)
for t in (4, 23, 24):
    o = obs_at(env, t)
    print(f"  obs {t} (dia {o['day']} h {o['hour']}): farmer en {farmer_pos(o)}")

print("=== SONDA B1: plantar en la ultima hora del dia (h23) sin regar ===")
env = run_scenario(
    {
        0: {"market": [["BUY_SEED", "WHEAT", 1]]},
        23: {"farmer": ["PLANT", "WHEAT"]},
    },
    n_steps=30,
)
o1 = obs_at(env, 1)
print(f"  obs 1: money={o1['farms'][0]['money']}  (E1: compra visible en T+1)")
for t in (24, 26):
    o = obs_at(env, t)
    print(f"  obs {t} (dia {o['day']} h {o['hour']}): tile(4,4) = {tile_at(o, 4, 4)}")

print("=== SONDA B2: plantar h22 + regar h23 ===")
env = run_scenario(
    {
        0: {"market": [["BUY_SEED", "WHEAT", 1]]},
        22: {"farmer": ["PLANT", "WHEAT"]},
        23: {"farmer": ["WATER"]},
    },
    n_steps=30,
)
for t in (23, 24):
    o = obs_at(env, t)
    print(f"  obs {t} (dia {o['day']} h {o['hour']}): tile(4,4) = {tile_at(o, 4, 4)}")

print("=== SONDA C: ¿de donde sale el wheat del FEED? ===")
env = run_scenario(
    {
        0: {"farmer": ["NORTH"], "market": [["BUY_ANIMAL", "GOOSE", 1], ["BUY_PRODUCT", "WHEAT", 2]]},
        1: {"farmer": ["BUILD_COOP"]},
        2: {"farmer": ["SOUTH"]},
        3: {"farmer": ["PICKUP", "GOOSE", 1]},
        4: {"farmer": ["NORTH"]},
        5: {"farmer": ["PLACE", "GOOSE"]},
        6: {"farmer": ["FEED"]},
        7: {"farmer": ["SOUTH"]},
        8: {"farmer": ["PICKUP", "WHEAT", 2]},
        9: {"farmer": ["NORTH"]},
        10: {"farmer": ["FEED"]},
    },
    n_steps=14,
)
o = obs_at(env, 1)
shed1 = {k: v for k, v in o["private"]["shed"].items() if v}
print(f"  obs 1: shed={shed1}  money={o['farms'][0]['money']}")
for t in (6, 7, 9, 11):
    o = obs_at(env, t)
    tile = tile_at(o, 4, 3)
    shed = {k: v for k, v in o["private"]["shed"].items() if v}
    inv = dict(o["private"]["inventories"][0])
    if isinstance(tile, dict):
        desc = f"kind={tile.get('kind')} animal={tile.get('animal')} fed_today={tile.get('fed_today')}"
    else:
        desc = f"tile={tile}"
    print(f"  obs {t}: {desc} | shed={shed} | inv farmer={inv}")
