"""Analiza un replay real de Kaggle: desperdicio propio + inteligencia del rival.

Checks (hipótesis del usuario, 2026-08-26):
  1. Turnos ociosos: ¿hay turnos donde ninguna unidad hace nada? ¿coinciden con
     turnos de mercado (que son gratis y en paralelo)?
  2. Weeds tras desbloquear el 2do terreno: ¿mueren plantas por riego fallido?
  3. (Coops/pastures se verificaron en sondas; aquí: ¿estructuras vacías?)
  4. Fuga de fin de juego: valor sin vender al step 719 — shed, inventarios de
     unidades, producto acumulado EN animales y cosecha EN plantas.

Uso: ./.venv/bin/python analizar_replay.py replays/episode-XXX-replay.json
"""
import json
import sys
from collections import defaultdict

BASE = {"WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120, "MELON": 250,
        "EGG": 50, "MILK": 160, "WOOL": 200, "FERTILIZER": 100}
PROD = {"GOOSE": "EGG", "COW": "MILK", "SHEEP": "WOOL"}
CROP_FIRST = {"WHEAT": 2, "CARROT": 2, "MELON": 10, "TOMATO": 8, "STRAWBERRY": 10}


def composition(farm):
    c = defaultdict(int)
    for row in farm["tiles"]:
        for t in row:
            if t is None or t == "LOCKED":
                continue
            k = t.get("kind")
            if k == "PLANT":
                c[t["crop"]] += 1
            elif k == "WEED":
                c["WEED"] += 1
            elif k in ("COOP", "PASTURE"):
                c[t.get("animal") or f"{k}_VACIA"] += 1
    c["quadrants"] = len(farm["unlocked_quadrants"])
    return c


def tile_value_on_board(farm, day):
    """Valor cosechable parado en el tablero: producto en animales + plantas maduras."""
    animals = plants = 0.0
    for row in farm["tiles"]:
        for t in row:
            if not isinstance(t, dict):
                continue
            if t.get("animal"):
                animals += t.get("yield_units", 0) * BASE[PROD[t["animal"]]]
            elif t.get("kind") == "PLANT":
                age = day - t["planted_day"]
                if age >= CROP_FIRST[t["crop"]]:
                    plants += t.get("yield_units", 0) * BASE[t["crop"]]
    return animals, plants


def analyze(path, my_prefix="Rospel"):
    d = json.load(open(path))
    names = d["info"]["TeamNames"]
    me = 0 if names[0].startswith(my_prefix) else 1
    opp = 1 - me
    steps = d["steps"]
    rewards = d["rewards"]
    print(f"=== {path.split('/')[-1]} | yo={names[me]} (p{me}) vs {names[opp]} | "
          f"${rewards[me]:,.0f} vs ${rewards[opp]:,.0f} -> {'GANE' if rewards[me] > rewards[opp] else 'PERDI'} ===")

    # 1. turnos ociosos por jugador
    stats = {p: defaultdict(int) for p in (0, 1)}
    for t in range(1, len(steps)):
        for p in (0, 1):
            act = steps[t][p].get("action") or {}
            ops = [act.get("farmer") or ["PASS"]] + list(act.get("hands") or [])
            n_pass = sum(1 for o in ops if not o or o[0] == "PASS")
            stats[p]["unit_turns"] += len(ops)
            stats[p]["pass_turns"] += n_pass
            if n_pass == len(ops):
                stats[p]["all_pass"] += 1
                if act.get("market"):
                    stats[p]["all_pass_con_mercado"] += 1
    for p, label in ((me, "yo"), (opp, "rival")):
        s = stats[p]
        print(f"  [{label}] unidades-PASS: {s['pass_turns']}/{s['unit_turns']} ({s['pass_turns'] / max(1, s['unit_turns']):.0%}) | "
              f"turnos TODO-PASS: {s['all_pass']}/719 (con mercado: {s['all_pass_con_mercado']})")

    # 2. muertes de plantas y weeds por día; momento de compra de tierra
    deaths = {0: 0, 1: 0}
    land_day = {0: None, 1: None}
    weed_series = {0: [], 1: []}
    for t in range(1, len(steps)):
        obs0 = steps[t][0]["observation"]
        prev0 = steps[t - 1][0]["observation"]
        for p in (0, 1):
            farm, pfarm = obs0["farms"][p], prev0["farms"][p]
            if land_day[p] is None and len(farm["unlocked_quadrants"]) > 1:
                land_day[p] = obs0["day"]
            for y in range(len(farm["tiles"])):
                for x in range(len(farm["tiles"][y])):
                    a, b = pfarm["tiles"][y][x], farm["tiles"][y][x]
                    if isinstance(a, dict) and a.get("kind") == "PLANT" and isinstance(b, dict) and b.get("kind") == "WEED":
                        deaths[p] += 1
        if t % 24 == 0:
            for p in (0, 1):
                weed_series[p].append(composition(obs0["farms"][p])["WEED"])
    for p, label in ((me, "yo"), (opp, "rival")):
        print(f"  [{label}] plantas muertas: {deaths[p]} | tierra comprada día {land_day[p]} | "
              f"weeds por día (5,10,15,20,25,29): {[weed_series[p][i] for i in (5, 10, 15, 20, 25, 29) if i < len(weed_series[p])]}")

    # composición al día 10 y 25
    for dday in (10, 25):
        o = steps[dday * 24][0]["observation"]
        for p, label in ((me, "yo"), (opp, "rival")):
            print(f"  [{label}] día {dday}: {dict(composition(o['farms'][p]))}")

    # 4. fuga final (step 719)
    last = steps[-1]
    obs = last[0]["observation"]
    day = obs["day"]
    for p, label in ((me, "yo"), (opp, "rival")):
        an_val, pl_val = tile_value_on_board(obs["farms"][p], day)
        line = f"  [{label}] SIN VENDER al final: en animales ${an_val:,.0f} | en plantas maduras ${pl_val:,.0f}"
        if p == me:
            priv = last[me]["observation"].get("private", {}) or {}
            prices = obs["market"]["prices"]
            shed_v = sum(n * prices.get(it, 0) for it, n in (priv.get("shed") or {}).items())
            inv_v = sum(n * prices.get(it, 0) for inv in (priv.get("inventories") or []) for it, n in inv.items())
            line += f" | en shed ${shed_v:,.0f} | en inventarios de unidades ${inv_v:,.0f}"
        print(line)

    # ventas de los últimos 2 días (nuestras)
    sells = 0
    for t in range(672, len(steps)):
        act = steps[t][me].get("action") or {}
        sells += sum(int(o[2]) for o in (act.get("market") or []) if o and o[0] == "SELL" and len(o) >= 3)
    print(f"  [yo] unidades vendidas días 28-29: {sells}")
    print()


if __name__ == "__main__":
    for path in sys.argv[1:]:
        analyze(path)
