"""Rampa de arranque: cuándo entra cada tile productiva y cada animal.

Mide, por jugador: día de PLACE de cada animal, día de plantado de cada cultivo,
tiles productivas ocupadas por día 0-10, dinero por día 0-10 y "tile-días
premium" perdidos por arrancar tarde.
"""
import json
import sys
from collections import defaultdict

BASE = {"WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120, "MELON": 250,
        "EGG": 50, "MILK": 160, "WOOL": 200}


def ramp(d, p, upto=10):
    steps = d["steps"]
    placed = []
    plants = defaultdict(list)   # crop -> [dia]
    for t in range(1, min(upto * 24 + 1, len(steps))):
        obs = steps[t - 1][0]["observation"]
        day = obs["day"]
        act = steps[t][p].get("action") or {}
        for o in [act.get("farmer") or ["PASS"]] + list(act.get("hands") or []):
            if o and o[0] == "PLACE" and len(o) > 1:
                placed.append((day, obs["hour"], o[1]))
            if o and o[0] == "PLANT" and len(o) > 1:
                plants[o[1]].append(day)
    rows = []
    for day in range(upto + 1):
        t = min(day * 24, len(steps) - 1)
        farm = steps[t][0]["observation"]["farms"][p]
        npl = nan = nst = nem = 0
        for row in farm["tiles"]:
            for c in row:
                if c is None:
                    nem += 1
                elif isinstance(c, dict):
                    k = c.get("kind")
                    if k == "PLANT":
                        npl += 1
                    elif k in ("COOP", "PASTURE"):
                        nst += 1
                        if c.get("animal"):
                            nan += 1
        rows.append((day, farm["money"], npl, nan, nst, nem, len(farm["unlocked_quadrants"])))
    return placed, {k: sorted(v) for k, v in plants.items()}, rows


if __name__ == "__main__":
    both = "--all" in sys.argv
    agg = defaultdict(list)
    for path in [a for a in sys.argv[1:] if not a.startswith("--")]:
        d = json.load(open(path))
        names = d["info"]["TeamNames"]
        for p in (0, 1):
            if not (both or names[p].startswith("Rospel")):
                continue
            placed, plants, rows = ramp(d, p)
            agg[names[p]].append((placed, plants, rows))
    for name, rs in agg.items():
        n = len(rs)
        print(f"\n===== {name} ({n} partidas) =====")
        # animales
        alldays = defaultdict(list)
        for placed, _, _ in rs:
            for i, (day, hour, an) in enumerate(sorted(placed)):
                alldays[i].append(day + hour / 24)
        print("  día de colocación del animal n-ésimo: " +
              " ".join(f"#{i+1}={sum(v)/len(v):.2f}" for i, v in sorted(alldays.items())[:10]))
        kinds = defaultdict(list)
        for placed, _, _ in rs:
            c = defaultdict(list)
            for day, hour, an in placed:
                c[an].append(day + hour / 24)
            for an, v in c.items():
                kinds[an].extend(v)
        print("  por especie (día medio de colocación, n): " +
              " ".join(f"{k}={sum(v)/len(v):.2f}(n={len(v)/n:.1f}/partida)" for k, v in kinds.items()))
        # cultivos
        pc = defaultdict(list)
        for _, plants, _ in rs:
            for c, days in plants.items():
                pc[c].extend(days)
        print("  1er plantado por cultivo (día medio | n medio en d0-10): " +
              " ".join(f"{c}: d{min(v):.0f}/med d{sum(v)/len(v):.1f} n={len(v)/n:.1f}" for c, v in sorted(pc.items())))
        # tabla por día
        print("  día |  dinero | plantas animales estructuras vacías quads")
        for day in range(11):
            cols = [r[2][day] for r in rs]
            m = lambda i: sum(c[i] for c in cols) / n
            print(f"   d{day:<2d} | {m(1):7,.0f} | {m(2):7.1f} {m(3):8.1f} {m(4):12.1f} {m(5):6.1f} {m(6):5.1f}")
