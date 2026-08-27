"""Autopsia de desperdicio ("inting"): dónde pierde valor un agente.

Corre K episodios A vs B y audita, para el lado A, cada categoría de valor
perdido que las reglas permiten perder:

  - plantas muertas (weed por descuido o decay hasta 0), con su valor
  - unidades perdidas por decay (cosecha tardía)
  - animales escapados
  - producción animal capada por max_held (cosecha tardía de animales)
  - fertilizer de animales no recolectado
  - riegos de ventana de bonus perdidos (yield que no se generó)
  - acciones PASS / movimiento / no-op (WATER a tile ya regada, FEED sin wheat)
  - inventario sin vender al final (no cuenta para el score)

Uso:
    ./.venv/bin/python autopsia.py bots.arquetipos:gansos starter -n 3
"""
import argparse
from collections import defaultdict

from harness import materialize

BASE = {"WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120, "MELON": 250,
        "EGG": 50, "MILK": 160, "WOOL": 200, "FERTILIZER": 100}
SEED_COST = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50, "STRAWBERRY": 100, "MELON": 80}
ANIMAL = {"GOOSE": dict(cost=300, first=4, iv=1, cap=4, prod="EGG"),
          "COW": dict(cost=400, first=8, iv=2, cap=6, prod="MILK"),
          "SHEEP": dict(cost=500, first=6, iv=3, cap=6, prod="WOOL")}
CROP_WIN = {"WHEAT": (2, 4), "CARROT": (2, 3), "MELON": (6, 12)}
MOVES = {"NORTH", "SOUTH", "EAST", "WEST"}


def analyze_episode(env, player):
    c = defaultdict(float)
    steps = env.steps
    for t in range(1, len(steps)):
        obs_prev = steps[t - 1][0].observation
        obs_cur = steps[t][0].observation
        prev = obs_prev["farms"][player]["tiles"]
        cur = obs_cur["farms"][player]["tiles"]
        dawn = t % 24 == 0

        for y in range(len(cur)):
            for x in range(len(cur[y])):
                a, b = prev[y][x], cur[y][x]
                if not isinstance(a, dict):
                    continue
                # planta -> weed (muerte por descuido o decay a 0)
                if a.get("kind") == "PLANT":
                    if isinstance(b, dict) and b.get("kind") == "WEED":
                        c["plantas_muertas"] += 1
                        c["plantas_muertas_$"] += a.get("yield_units", 0) * BASE[a["crop"]] + SEED_COST[a["crop"]]
                    elif isinstance(b, dict) and b.get("kind") == "PLANT":
                        drop = a.get("yield_units", 0) - b.get("yield_units", 0)
                        mls = a.get("max_lifespan_step", -1)
                        if drop > 0 and 0 <= mls <= (t - 1):
                            c["decay_unidades"] += drop
                            c["decay_$"] += drop * BASE[a["crop"]]
                    if dawn:
                        # riego de ventana perdido (solo one-time)
                        crop = a["crop"]
                        if crop in CROP_WIN and not a.get("watered_today"):
                            age = obs_prev["day"] - a["planted_day"]
                            lo, hi = CROP_WIN[crop]
                            if lo <= age <= hi:
                                c["riegos_ventana_perdidos"] += 1
                                c["riegos_ventana_$"] += BASE[crop]
                # animal escapado (estructura queda sin animal)
                if a.get("animal"):
                    an = ANIMAL[a["animal"]]
                    if isinstance(b, dict) and b.get("kind") in ("COOP", "PASTURE") and not b.get("animal"):
                        c["animales_escapados"] += 1
                        c["animales_escapados_$"] += an["cost"]
                    if dawn and isinstance(b, dict) and b.get("animal"):
                        prod_day = t // 24
                        since = prod_day - a["placed_day"] - an["first"]
                        if since >= 0 and since % an["iv"] == 0 and a.get("fed_today"):
                            expected = 1 + a.get("pending_care_bonus", 0)
                            actual = b.get("yield_units", 0) - a.get("yield_units", 0)
                            lost = max(0, expected - actual)
                            if lost:
                                c["produccion_capada"] += lost
                                c["produccion_capada_$"] += lost * BASE[an["prod"]]
                        if a.get("fertilizer_available"):
                            c["fertilizer_no_recogido"] += 1
                            c["fertilizer_no_recogido_$"] += BASE["FERTILIZER"]

        # auditoría de acciones (action en steps[t] = lo decidido con la obs t-1)
        act = steps[t][player].action
        if isinstance(act, dict):
            unit_ops = [act.get("farmer") or ["PASS"]] + list(act.get("hands") or [])
            farm_prev = obs_prev["farms"][player]
            unit_pos = [tuple(farm_prev["farmer"])] + [tuple(h) for h in farm_prev["hands"]]
            for i, op in enumerate(unit_ops):
                if not isinstance(op, list) or not op:
                    continue
                name = op[0]
                if name == "PASS":
                    c["acciones_pass"] += 1
                elif name in MOVES:
                    c["acciones_movimiento"] += 1
                else:
                    c["acciones_productivas"] += 1
                    if i < len(unit_pos):
                        x, y = unit_pos[i]
                        tile = farm_prev["tiles"][y][x]
                        if name == "WATER" and isinstance(tile, dict) and tile.get("watered_today"):
                            c["noop_water"] += 1
                        if name == "FEED" and isinstance(tile, dict) and tile.get("fed_today"):
                            c["noop_feed"] += 1
            prices = obs_prev["market"]["prices"]
            for m in act.get("market") or []:
                if m and m[0] == "SELL" and len(m) >= 3:
                    pr = prices.get(m[1], 0)
                    if pr <= 0.3 * BASE.get(m[1], 100):
                        c["ventas_piso"] += int(m[2])
                        c["ventas_piso_$"] += int(m[2]) * (BASE.get(m[1], 100) - pr)

    final = steps[-1][0].observation
    prices = final["market"]["prices"]
    shed = steps[-1][player].observation.get("private", {}).get("shed", {}) or {}
    c["inventario_final_$"] = sum(n * prices.get(it, 0) for it, n in shed.items())
    c["dinero_final"] = final["farms"][player]["money"]
    return c


def autopsy(spec_a, spec_b, n_seeds=3, seed0=5000, steps=720):
    from kaggle_environments import make

    agg = defaultdict(float)
    for s in range(seed0, seed0 + n_seeds):
        env = make("kaggriculture", configuration={"episodeSteps": steps, "seed": s})
        env.run([materialize(spec_a), materialize(spec_b)])
        for k, v in analyze_episode(env, 0).items():
            agg[k] += v / n_seeds
    return dict(agg)


def print_report(name, agg):
    print(f"--- autopsia: {name} (medias por episodio) ---")
    print(f"dinero final: ${agg.get('dinero_final', 0):,.0f} | inventario sin vender: ${agg.get('inventario_final_$', 0):,.0f}")
    rows = [
        ("plantas muertas", "plantas_muertas", "plantas_muertas_$"),
        ("unidades perdidas por decay", "decay_unidades", "decay_$"),
        ("animales escapados", "animales_escapados", "animales_escapados_$"),
        ("producción animal capada", "produccion_capada", "produccion_capada_$"),
        ("fertilizer no recogido", "fertilizer_no_recogido", "fertilizer_no_recogido_$"),
        ("riegos de ventana perdidos", "riegos_ventana_perdidos", "riegos_ventana_$"),
        ("ventas a mercado estrellado", "ventas_piso", "ventas_piso_$"),
    ]
    for label, kc, kd in rows:
        if agg.get(kc):
            print(f"  {label:32s} {agg[kc]:6.1f}  (~${agg.get(kd, 0):,.0f})")
    total_units = agg.get("acciones_pass", 0) + agg.get("acciones_movimiento", 0) + agg.get("acciones_productivas", 0)
    if total_units:
        print(f"  acciones: {agg.get('acciones_productivas', 0):.0f} productivas / "
              f"{agg.get('acciones_movimiento', 0):.0f} movimiento / {agg.get('acciones_pass', 0):.0f} PASS "
              f"({agg.get('acciones_pass', 0) / total_units:.0%} ocioso)")
    if agg.get("noop_water") or agg.get("noop_feed"):
        print(f"  no-ops: WATER {agg.get('noop_water', 0):.0f}, FEED {agg.get('noop_feed', 0):.0f}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("agent_a")
    ap.add_argument("agent_b")
    ap.add_argument("-n", "--seeds", type=int, default=3)
    ap.add_argument("--seed0", type=int, default=5000)
    args = ap.parse_args()
    agg = autopsy(args.agent_a, args.agent_b, n_seeds=args.seeds, seed0=args.seed0)
    print_report(args.agent_a, agg)
