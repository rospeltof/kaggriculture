"""Disección agregada de los replays del top del leaderboard (ambos jugadores).

Verifica las observaciones del usuario (2026-08-29): apertura con 4 peones,
cultivos caros primero, animales día 1, ~0 weeds, 3 cuadrantes antes del día 10,
venta total al cierre, adaptación tardía a precios.

Uso: ./.venv/bin/python analizar_titanes.py ~/Downloads/*.json
"""
import json
import sys
from collections import defaultdict

from analizar_replay import composition, tile_value_on_board


def analyze_player(d, p):
    steps = d["steps"]
    name = d["info"]["TeamNames"][p]
    r = {"name": name, "money": d["rewards"][p]}
    hires_by_day = defaultdict(int)
    plants_by_phase = defaultdict(lambda: defaultdict(int))
    sells = defaultdict(int)
    sells_late = defaultdict(int)
    n_pass = n_ops = 0
    for t in range(1, len(steps)):
        day = (t - 1) // 24
        act = steps[t][p].get("action") or {}
        ops = [act.get("farmer") or ["PASS"]] + list(act.get("hands") or [])
        n_ops += len(ops)
        n_pass += sum(1 for o in ops if not o or o[0] == "PASS")
        phase = "d0-2" if day <= 2 else ("d3-9" if day <= 9 else ("d10-19" if day <= 19 else "d20+"))
        for o in ops:
            if o and o[0] == "PLANT" and len(o) > 1:
                plants_by_phase[phase][o[1]] += 1
        for m in act.get("market") or []:
            if not m:
                continue
            if m[0] == "HIRE":
                hires_by_day[day] += 1
            elif m[0] == "SELL" and len(m) >= 3:
                sells[m[1]] += int(m[2])
                if day >= 28:
                    sells_late[m[1]] += int(m[2])
    r["pass_rate"] = n_pass / max(1, n_ops)
    r["hires"] = [hires_by_day.get(dd, 0) for dd in range(30)]
    r["plants"] = {k: dict(v) for k, v in plants_by_phase.items()}
    r["sells"] = dict(sells)
    r["sells_late"] = dict(sells_late)

    land = {}
    weeds = []
    for dd in range(1, 30):
        obs = steps[min(dd * 24, len(steps) - 1)][0]["observation"]
        farm = obs["farms"][p]
        nq = len(farm["unlocked_quadrants"])
        if nq not in land:
            land[nq] = dd
        weeds.append(composition(farm)["WEED"])
    r["land"] = land
    r["weeds_max"] = max(weeds)
    r["weeds_mean"] = sum(weeds) / len(weeds)

    for dd in (5, 15, 25):
        obs = steps[dd * 24][0]["observation"]
        r[f"comp_d{dd}"] = dict(composition(obs["farms"][p]))
    last = steps[-1][0]["observation"]
    an_val, pl_val = tile_value_on_board(last["farms"][p], last["day"])
    r["final_en_tablero"] = an_val + pl_val
    priv = steps[-1][p]["observation"].get("private") or {}
    shed = priv.get("shed") or {}
    prices = last["market"]["prices"]
    r["final_shed"] = sum(n * prices.get(it, 0) for it, n in shed.items()) if shed else None
    return r


def merge(rs):
    out = defaultdict(list)
    for r in rs:
        for k, v in r.items():
            out[k].append(v)
    return out


if __name__ == "__main__":
    by_player = defaultdict(list)
    for path in sys.argv[1:]:
        d = json.load(open(path))
        for p in (0, 1):
            r = analyze_player(d, p)
            by_player[r["name"]].append(r)

    for name, rs in by_player.items():
        m = merge(rs)
        print(f"\n===== {name} ({len(rs)} partidas, dinero medio ${sum(m['money']) / len(rs):,.0f}) =====")
        print(f"PASS rate: {sum(m['pass_rate']) / len(rs):.1%} | weeds max medio: {sum(m['weeds_max']) / len(rs):.1f} | "
              f"final en tablero: ${sum(m['final_en_tablero']) / len(rs):,.0f} | "
              f"final en shed: {[f'{s:,.0f}' if s is not None else '?' for s in m['final_shed'][:3]]}")
        h = [sum(x) / len(rs) for x in zip(*m["hires"])]
        print(f"peones/día: d0={h[0]:.1f} d1={h[1]:.1f} d2={h[2]:.1f} d5={h[5]:.1f} d10={h[10]:.1f} d15={h[15]:.1f} d20={h[20]:.1f} d25={h[25]:.1f} d29={h[29]:.1f}")
        lands = defaultdict(list)
        for r in rs:
            for nq, dd in r["land"].items():
                lands[nq].append(dd)
        print("desbloqueo de cuadrantes:", {nq: f"día {sum(v) / len(v):.1f}" for nq, v in sorted(lands.items())})
        agg_plants = defaultdict(lambda: defaultdict(float))
        for r in rs:
            for phase, crops in r["plants"].items():
                for c, n in crops.items():
                    agg_plants[phase][c] += n / len(rs)
        for phase in ("d0-2", "d3-9", "d10-19", "d20+"):
            row = {c: round(n, 1) for c, n in sorted(agg_plants[phase].items(), key=lambda kv: -kv[1])}
            print(f"  plantado {phase}: {row}")
        agg_sells = defaultdict(float)
        for r in rs:
            for it, n in r["sells"].items():
                agg_sells[it] += n / len(rs)
        print("  ventas/partida:", {k: round(v) for k, v in sorted(agg_sells.items(), key=lambda kv: -kv[1])})
        print("  comp d5: ", dict(rs[0]["comp_d5"]))
        print("  comp d15:", dict(rs[0]["comp_d15"]))
        print("  comp d25:", dict(rs[0]["comp_d25"]))

    # traza cruda de la apertura del campeón (partida 1, día 0, horas 0-5)
    d = json.load(open(sys.argv[1]))
    champ = 0 if d["info"]["TeamNames"][0] == "Crop Dusta" else 1
    print("\n===== traza de apertura de Crop Dusta (día 0, horas 0-5) =====")
    for t in range(1, 7):
        act = d["steps"][t][champ].get("action") or {}
        print(f"h{t - 1}: farmer={act.get('farmer')} hands={act.get('hands')} market={act.get('market')}")
