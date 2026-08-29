"""Análisis forense de partidas: puntos de inflexión, ocio localizado, apertura,
uso de cuadrantes y lógica de mezcla de cultivos.

Responde las preguntas del usuario (2026-09-03):
  A) trayectoria del margen día a día -> ¿dónde se pierde/gana la ventaja?
  B) ¿qué producto explica el cambio de margen en esos días?
  C) unidades quietas muchos turnos en la misma tile (¿bug?)
  D) auditoría del día 0-1 (lo que más compone)
  E) uso del 3er cuadrante tras comprarlo
  F) por qué el scorer elige carrot/melón sobre fresa

Uso: ./.venv/bin/python forense.py replays/episode-XXXX-replay.json [...]
"""
import json
import sys
from collections import defaultdict

BASE = {"WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120, "MELON": 250,
        "EGG": 50, "MILK": 160, "WOOL": 200, "FERTILIZER": 100}
PROD = {"GOOSE": "EGG", "COW": "MILK", "SHEEP": "WOOL"}


def load(path):
    d = json.load(open(path))
    n = d["info"]["TeamNames"]
    me = 0 if n[0].startswith("Rospel") else 1
    return d, me, n[1 - me]


def margen_diario(d, me):
    """Dinero propio, del rival y margen al final de cada día."""
    out = []
    steps = d["steps"]
    for day in range(30):
        t = min(day * 24, len(steps) - 1)
        f = steps[t][0]["observation"]["farms"]
        out.append((day, f[me]["money"], f[1 - me]["money"]))
    return out


def ventas_por_dia(d, player):
    """{(dia, item): (unidades, ingreso)} a precio del momento."""
    steps = d["steps"]
    out = defaultdict(lambda: [0, 0.0])
    for t in range(1, len(steps)):
        obs = steps[t - 1][0]["observation"]
        act = steps[t][player].get("action") or {}
        for m in act.get("market") or []:
            if m and m[0] == "SELL" and len(m) >= 3:
                pr = obs["market"]["prices"].get(m[1], 0)
                k = (obs["day"], m[1])
                out[k][0] += int(m[2])
                out[k][1] += int(m[2]) * pr
    return out


def quietud(d, me, min_turns=6):
    """Unidades que pasan >=min_turns consecutivos en la misma tile sin acción
    productiva (solo PASS/movimiento fallido). Devuelve lista de episodios."""
    steps = d["steps"]
    streak = {}
    out = []
    for t in range(1, len(steps)):
        obs = steps[t - 1][0]["observation"]
        farm = obs["farms"][me]
        act = steps[t][me].get("action") or {}
        ops = [act.get("farmer") or ["PASS"]] + list(act.get("hands") or [])
        pos = [tuple(farm["farmer"])] + [tuple(h) for h in farm["hands"]]
        for i, (p, o) in enumerate(zip(pos, ops)):
            idle = (not o) or o[0] == "PASS"
            key = i
            prev = streak.get(key)
            if idle and prev and prev[0] == p:
                streak[key] = (p, prev[1] + 1, prev[2])
            elif idle:
                streak[key] = (p, 1, obs["day"] * 24 + obs["hour"])
            else:
                if prev and prev[1] >= min_turns:
                    out.append((key, prev[0], prev[1], prev[2]))
                streak.pop(key, None)
    for key, v in streak.items():
        if v[1] >= min_turns:
            out.append((key, v[0], v[1], v[2]))
    return out


def apertura(d, me, days=2):
    """Qué hace cada unidad los primeros `days` días: conteo de ops y tiles usadas."""
    steps = d["steps"]
    ops_count = defaultdict(int)
    planted = defaultdict(int)
    for t in range(1, min(days * 24 + 1, len(steps))):
        act = steps[t][me].get("action") or {}
        for o in [act.get("farmer") or ["PASS"]] + list(act.get("hands") or []):
            if o:
                ops_count[o[0]] += 1
                if o[0] == "PLANT" and len(o) > 1:
                    planted[o[1]] += 1
    obs = steps[min(days * 24, len(steps) - 1)][0]["observation"]
    farm = obs["farms"][me]
    used = sum(1 for row in farm["tiles"] for c in row if isinstance(c, dict))
    empty = sum(1 for row in farm["tiles"] for c in row if c is None)
    return dict(ops_count), dict(planted), used, empty


def uso_cuadrantes(d, me):
    """Por día: cuadrantes desbloqueados, tiles ocupadas y vacías."""
    steps = d["steps"]
    out = []
    for day in range(30):
        t = min(day * 24, len(steps) - 1)
        farm = steps[t][0]["observation"]["farms"][me]
        nq = len(farm["unlocked_quadrants"])
        occ = sum(1 for row in farm["tiles"] for c in row if isinstance(c, dict))
        emp = sum(1 for row in farm["tiles"] for c in row if c is None)
        out.append((day, nq, occ, emp))
    return out


def mezcla_cultivos(d, me):
    """Composición de cultivos por día (para ver carrot vs strawberry vs melon)."""
    steps = d["steps"]
    out = []
    for day in range(0, 30, 3):
        t = min(day * 24, len(steps) - 1)
        farm = steps[t][0]["observation"]["farms"][me]
        c = defaultdict(int)
        for row in farm["tiles"]:
            for tile in row:
                if isinstance(tile, dict) and tile.get("kind") == "PLANT":
                    c[tile["crop"]] += 1
        out.append((day, dict(c)))
    return out


if __name__ == "__main__":
    for path in sys.argv[1:]:
        d, me, opp = load(path)
        print(f"\n{'=' * 78}\n{path.split('/')[-1]}  vs {opp}  ({d['rewards'][me]:,.0f} vs {d['rewards'][1-me]:,.0f})\n{'=' * 78}")
        mg = margen_diario(d, me)
        print("día:  yo      rival    margen   (deltas del día)")
        prev = 0
        for day, my, their in mg:
            m = my - their
            dd = m - prev
            flag = "  <<<" if abs(dd) > 6000 and day > 0 else ""
            print(f"  d{day:2d}: {my:>8,.0f} {their:>8,.0f} {m:>+9,.0f}  ({dd:>+8,.0f}){flag}")
            prev = m

        # --- qué producto explica los saltos de margen ---
        vd_me, vd_op = ventas_por_dia(d, me), ventas_por_dia(d, 1 - me)
        saltos = []
        prev = 0
        for day, my, their in mg:
            m = my - their
            if day > 0 and abs(m - prev) > 6000:
                saltos.append(day)
            prev = m
        print(f"\n-- días de quiebre ({saltos}) --")
        for day in saltos:
            mine = {k[1]: (v[0], round(v[1])) for k, v in vd_me.items() if k[0] == day}
            theirs = {k[1]: (v[0], round(v[1])) for k, v in vd_op.items() if k[0] == day}
            print(f"  d{day}: yo vendí {mine or '—'}")
            print(f"        él vendió {theirs or '—'}")

        # --- ingresos acumulados por producto (quién nos mató) ---
        tot_me, tot_op = defaultdict(float), defaultdict(float)
        for k, v in vd_me.items():
            tot_me[k[1]] += v[1]
        for k, v in vd_op.items():
            tot_op[k[1]] += v[1]
        print("\n-- ingreso total por producto (yo | rival) --")
        for it in sorted(set(tot_me) | set(tot_op), key=lambda x: -(tot_op[x] + tot_me[x])):
            print(f"  {it:11s} ${tot_me[it]:>9,.0f} | ${tot_op[it]:>9,.0f}   ({tot_op[it]-tot_me[it]:+,.0f})")

        # --- unidades quietas ---
        q = quietud(d, me)
        if q:
            top = sorted(q, key=lambda x: -x[2])[:6]
            print(f"\n-- unidades quietas >=6 turnos en la misma tile: {len(q)} episodios --")
            for unit, pos, n, start in top:
                print(f"  unidad {unit} en {pos}: {n} turnos seguidos desde d{start//24}h{start%24}")
        else:
            print("\n-- sin unidades quietas >=6 turnos --")

        # --- apertura ---
        ops, planted, used, empty = apertura(d, me, days=2)
        print(f"\n-- apertura (días 0-1): tiles ocupadas {used}, vacías {empty} --")
        print(f"  ops: {dict(sorted(ops.items(), key=lambda kv: -kv[1]))}")
        print(f"  plantado: {planted}")

        # --- cuadrantes ---
        uc = uso_cuadrantes(d, me)
        print("\n-- cuadrantes/ocupación (día: quads occ vacías) --")
        print("  " + "  ".join(f"d{day}:{nq}q {occ}/{occ+emp}" for day, nq, occ, emp in uc if day % 4 == 0))

        # --- mezcla ---
        print("\n-- mezcla de cultivos --")
        for day, c in mezcla_cultivos(d, me):
            if c:
                print(f"  d{day:2d}: {c}")
