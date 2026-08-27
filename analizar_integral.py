"""Análisis de sistema de integral en el ladder: las 5 preguntas del usuario (2026-09-01).

1. ¿Qué pasa los días 0-1 (por qué no se planta)?
2. Traza del peón 1 (posiciones/acciones tempranas).
3. Economía del melón: plantados pico, unidades vendidas y PRECIO REALIZADO medio.
4. Volumen de fresa vendido.
5. Lana: volumen, precio realizado, ¿escasez sostenida sin explotar?
Todo agregado sobre victorias Y derrotas.

Uso: ./.venv/bin/python analizar_integral.py replays/episode-101*.json
"""
import json
import sys
from collections import defaultdict

BASE = {"WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120, "MELON": 250,
        "EGG": 50, "MILK": 160, "WOOL": 200, "FERTILIZER": 100}


def analyze(path):
    d = json.load(open(path))
    names = d["info"]["TeamNames"]
    me = 0 if names[0].startswith("Rospel") else 1
    steps = d["steps"]
    r = {"opp": names[1 - me], "mi": d["rewards"][me], "su": d["rewards"][1 - me],
         "gane": d["rewards"][me] > d["rewards"][1 - me]}

    sold = defaultdict(int)
    revenue = defaultdict(float)
    plants_d01 = defaultdict(int)
    melon_peak = 0
    melon_seeds_d25 = 0
    wool_price_days = []
    for t in range(1, len(steps)):
        obs_prev = steps[t - 1][0]["observation"]
        day = obs_prev["day"]
        prices = obs_prev["market"]["prices"]
        act = steps[t][me].get("action") or {}
        ops = [act.get("farmer") or ["PASS"]] + list(act.get("hands") or [])
        if day <= 1:
            for o in ops:
                if o and o[0] == "PLANT" and len(o) > 1:
                    plants_d01[o[1]] += 1
        for m in act.get("market") or []:
            if m and m[0] == "SELL" and len(m) >= 3:
                sold[m[1]] += int(m[2])
                revenue[m[1]] += int(m[2]) * prices.get(m[1], 0)
        if t % 24 == 0:
            farm = obs_prev["farms"][me]
            n_melon = sum(1 for row in farm["tiles"] for c in row
                          if isinstance(c, dict) and c.get("crop") == "MELON")
            melon_peak = max(melon_peak, n_melon)
            wool_price_days.append(prices.get("WOOL", 0))
            if day == 25:
                priv = steps[t - 1][me]["observation"].get("private") or {}
                melon_seeds_d25 = (priv.get("seeds") or {}).get("MELON", 0)
    r["sold"] = dict(sold)
    r["avg_price"] = {k: revenue[k] / sold[k] for k in sold if sold[k]}
    r["plants_d01"] = dict(plants_d01)
    r["melon_peak"] = melon_peak
    r["melon_seeds_d25"] = melon_seeds_d25
    r["wool_min"] = min(wool_price_days) if wool_price_days else None
    r["wool_mean"] = sum(wool_price_days) / len(wool_price_days) if wool_price_days else None
    return r, d, me


if __name__ == "__main__":
    rows = []
    trace_done = False
    for path in sys.argv[1:]:
        r, d, me = analyze(path)
        rows.append(r)
        if not trace_done:  # traza del peón 1: primera partida, día 0 completo
            steps = d["steps"]
            print(f"=== traza peón 1 (día 0, {r['opp']}) ===")
            for t in range(1, 25):
                obs = steps[t - 1][0]["observation"]
                farm = obs["farms"][me]
                act = steps[t][me].get("action") or {}
                hands = act.get("hands") or []
                pos = farm["hands"][0] if farm["hands"] else None
                op = hands[0] if hands else None
                if op or pos:
                    print(f"  h{t - 1}: pos={pos} op={op}")
            trace_done = True

    print(f"\n=== {len(rows)} partidas: {sum(r['gane'] for r in rows)}G-{sum(not r['gane'] for r in rows)}P | "
          f"mi dinero medio ${sum(r['mi'] for r in rows) / len(rows):,.0f} | rival ${sum(r['su'] for r in rows) / len(rows):,.0f} ===")
    for r in rows:
        print(f"  {'G' if r['gane'] else 'P'} vs {r['opp'][:14]:14s} ${r['mi']:>7,.0f}-{r['su']:>7,.0f} | "
              f"melon: pico {r['melon_peak']:2d} tiles, {r['sold'].get('MELON', 0):3d}u a ${r['avg_price'].get('MELON', 0):>3.0f} | "
              f"fresa {r['sold'].get('STRAWBERRY', 0):3d}u a ${r['avg_price'].get('STRAWBERRY', 0):>3.0f} | "
          f"lana {r['sold'].get('WOOL', 0):2d}u a ${r['avg_price'].get('WOOL', 0):>3.0f} (min día ${r['wool_min']:.0f})")
    agg_sold = defaultdict(float)
    agg_rev = defaultdict(float)
    for r in rows:
        for k, v in r["sold"].items():
            agg_sold[k] += v / len(rows)
        for k in r["avg_price"]:
            agg_rev[k] += r["avg_price"][k] * r["sold"][k] / len(rows)
    print("\nventas medias/partida (unidades a precio realizado medio):")
    for k in sorted(agg_sold, key=lambda x: -agg_rev.get(x, 0)):
        print(f"  {k:11s} {agg_sold[k]:6.1f}u a ${agg_rev[k] / agg_sold[k]:>6.1f} (base ${BASE.get(k, 0)}) = ${agg_rev[k]:,.0f}")
    print("\nplantado días 0-1 (medio):", {k: round(sum(r['plants_d01'].get(k, 0) for r in rows) / len(rows), 1)
                                           for k in {c for r in rows for c in r['plants_d01']}})
    print("semillas de melón muertas al día 25 (medio):", round(sum(r['melon_seeds_d25'] for r in rows) / len(rows), 1))
