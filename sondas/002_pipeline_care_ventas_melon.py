"""Sondas 002: confirmar lecturas del motor (v1.32.7).

P1: pipeline PLANT+WATER en el mismo turno (granjero actúa antes que los peones)
    + costo del primer HIRE ($1) + spawn del peón en (5,4) + actúa desde T+1.
P2: matemática del CARE en un ganso (banco de bonus, primer yield al alba del día 4).
P3: SELL vende solo desde el shed; DROP + SELL funcionan en el mismo turno.
P4: ventana de bonus del melón (edades 6-12, max_yield_day=12 en el motor,
    no 10 como dice la tabla de la página) + HARVEST bloqueado antes de first_yield_day.
"""
import sys

sys.path.insert(0, "/Users/rospel/Desktop/kaggriculture")
from lab import run_scenario, obs_at, tile_at


print("=== P1: pipeline PLANT+WATER mismo turno, orden granjero->peones ===")
env = run_scenario(
    {
        0: {"market": [["BUY_SEED", "WHEAT", 2], ["HIRE"]]},
        1: {"hands": [["WEST"]]},                                # peón (5,4) -> (4,4)
        2: {"farmer": ["PLANT", "WHEAT"], "hands": [["WATER"]]},  # granjero planta, peón riega DESPUÉS
        3: {"farmer": ["WEST"], "hands": [["WEST"]]},             # ambos a (3,4)
        4: {"farmer": ["PASS"], "hands": [["PASS"]]},
        5: {"farmer": ["WATER"], "hands": [["PLANT", "WHEAT"]]},  # granjero riega ANTES de que exista la planta
    },
    n_steps=10,
)
o1 = obs_at(env, 1)
print(f"  obs 1: hands={[list(h) for h in o1['farms'][0]['hands']]}  money={o1['farms'][0]['money']} (esperado 2979 = 3000-20-1)")
o3 = obs_at(env, 3)
t = tile_at(o3, 4, 4)
print(f"  obs 3: tile(4,4) watered_today={t.get('watered_today')} consecutive_unwatered={t.get('consecutive_unwatered')}  <- pipeline OK si True")
o6 = obs_at(env, 6)
t = tile_at(o6, 3, 4)
print(f"  obs 6: tile(3,4) watered_today={t.get('watered_today')}  <- orden granjero-primero si False")

print("=== P2: CARE banking en ganso (colocado día 0, fed+cared diario) ===")
script = {
    0: {"farmer": ["NORTH"], "market": [["BUY_ANIMAL", "GOOSE", 1], ["BUY_PRODUCT", "WHEAT", 5]]},
    1: {"farmer": ["BUILD_COOP"]},
    2: {"farmer": ["SOUTH"]},
    3: {"farmer": ["PICKUP", "GOOSE"]},
    4: {"farmer": ["PICKUP", "WHEAT", 1]},
    5: {"farmer": ["NORTH"]},
    6: {"farmer": ["PLACE", "GOOSE"]},
    7: {"farmer": ["FEED"]},
    8: {"farmer": ["CARE"]},
}
for d in (1, 2, 3):
    base = 24 * d
    script[base] = {"farmer": ["PICKUP", "WHEAT", 1]}
    script[base + 1] = {"farmer": ["NORTH"]}
    script[base + 2] = {"farmer": ["FEED"]}
    script[base + 3] = {"farmer": ["CARE"]}
env = run_scenario(script, n_steps=100)
for t_obs in (72, 96):
    o = obs_at(env, t_obs)
    tile = tile_at(o, 4, 3)
    print(
        f"  obs {t_obs} (día {o['day']}): yield_units={tile.get('yield_units')} "
        f"pending_care_bonus={tile.get('pending_care_bonus')} fertilizer_available={tile.get('fertilizer_available')}"
    )
print("  esperado: día 3 -> yield 0, bonus 3 | día 4 -> yield 4 (1+3, justo el cap), bonus 1")

print("=== P3: SELL solo desde shed; DROP+SELL mismo turno ===")
env = run_scenario(
    {
        0: {"market": [["BUY_PRODUCT", "WHEAT", 3]]},
        1: {"farmer": ["PICKUP", "WHEAT", 3]},
        2: {"market": [["SELL", "WHEAT", 3]]},          # wheat en la mano -> debe fallar
        3: {"farmer": ["DROP"], "market": [["SELL", "WHEAT", 3]]},  # drop y venta mismo turno
    },
    n_steps=8,
)
for t_obs in (2, 3, 4):
    o = obs_at(env, t_obs)
    shed = {k: v for k, v in o["private"]["shed"].items() if v}
    inv = dict(o["private"]["inventories"][0])
    print(f"  obs {t_obs}: money={o['farms'][0]['money']} shed={shed} inv={inv}")

print("=== P4: ventana de bonus del melón + gate de first_yield_day ===")
script = {
    0: {"market": [["BUY_SEED", "MELON", 1]]},
    1: {"farmer": ["PLANT", "MELON"]},
    2: {"farmer": ["WATER"]},
}
for d in range(1, 13):
    script[24 * d] = {"farmer": ["WATER"]}
script[24 * 8 + 1] = {"farmer": ["HARVEST"]}   # edad 8 < first_yield_day 10 -> no-op esperado
env = run_scenario(script, n_steps=300)
curve = []
for d in range(1, 13):
    o = obs_at(env, 24 * d + 2)   # tras el riego del día d
    tile = tile_at(o, 4, 4)
    curve.append((d, tile.get("yield_units") if isinstance(tile, dict) else tile))
print(f"  yield tras riego del día: {curve}")
o = obs_at(env, 24 * 8 + 2)
print(f"  inv tras HARVEST edad 8: {dict(o['private']['inventories'][0])} (esperado vacío: gate first_yield_day)")
