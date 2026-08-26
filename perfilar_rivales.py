"""Perfila a todos los rivales de nuestros replays y los cruza con el leaderboard.

Para cada replay: quién era el rival, su dinero, su composición al día 10/25,
sus peones, su % de ocio, cuándo compró tierra — y su rank/score actual en el
leaderboard (los bots fuertes recién subidos pasan por nuestra banda de 600).

Uso: ./.venv/bin/python perfilar_rivales.py <leaderboard.csv> replays/*.json
"""
import csv
import json
import sys
from collections import defaultdict

from analizar_replay import composition

MY_PREFIX = "Rospel"


def profile(path, board):
    d = json.load(open(path))
    names = d["info"]["TeamNames"]
    me = 0 if names[0].startswith(MY_PREFIX) else 1
    opp = 1 - me
    steps = d["steps"]
    rewards = d["rewards"]

    o_pass = o_units = 0
    hires = []
    land_day = None
    for t in range(1, len(steps)):
        act = steps[t][opp].get("action") or {}
        ops = [act.get("farmer") or ["PASS"]] + list(act.get("hands") or [])
        o_units += len(ops)
        o_pass += sum(1 for o in ops if not o or o[0] == "PASS")
        if t % 24 == 0:
            obs = steps[t][0]["observation"]
            farm = obs["farms"][opp]
            hires.append(len(farm["hands"]))
            if land_day is None and len(farm["unlocked_quadrants"]) > 1:
                land_day = obs["day"]
    obs25 = steps[25 * 24][0]["observation"]
    comp25 = dict(composition(obs25["farms"][opp]))
    entry = board.get(names[opp])
    return {
        "ep": d["info"]["EpisodeId"],
        "rival": names[opp],
        "rank": entry[0] if entry else None,
        "score": entry[1] if entry else None,
        "mi_$": rewards[me],
        "su_$": rewards[opp],
        "gane": rewards[me] > rewards[opp],
        "ocio": o_pass / max(1, o_units),
        "peones_max": max(hires) if hires else 0,
        "tierra_dia": land_day,
        "dia25": comp25,
    }


if __name__ == "__main__":
    board = {}
    with open(sys.argv[1], encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            board[row["TeamName"]] = (int(row["Rank"]), float(row["Score"]))

    rows = [profile(p, board) for p in sys.argv[2:]]
    rows.sort(key=lambda r: -(r["score"] or 0))
    print(f"{'rival':22s} {'rank':>5s} {'score':>7s} {'su $':>8s} {'mi $':>8s} res {'ocio':>5s} {'peones':>6s} {'tierra':>6s}")
    for r in rows:
        print(f"{r['rival'][:22]:22s} {str(r['rank'] or '?'):>5s} {str(r['score'] or '?'):>7s} "
              f"{r['su_$']:>8,.0f} {r['mi_$']:>8,.0f} {'G' if r['gane'] else 'P':>3s} "
              f"{r['ocio']:>5.0%} {r['peones_max']:>6d} {str(r['tierra_dia']):>6s}")
    print("\n--- composición día 25 de los 6 rivales con más score ---")
    for r in rows[:6]:
        print(f"{r['rival'][:22]:22s} (rank {r['rank']}): {r['dia25']}")

    fuertes = [r for r in rows if (r["score"] or 0) > 1200]
    if fuertes:
        agg = defaultdict(float)
        keys = set()
        for r in fuertes:
            for k, v in r["dia25"].items():
                agg[k] += v / len(fuertes)
                keys.add(k)
        print(f"\n--- promedio día 25 de los {len(fuertes)} rivales con score >1200 ---")
        print({k: round(agg[k], 1) for k in sorted(keys, key=lambda x: -agg[x])})