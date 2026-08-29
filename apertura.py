"""Auditoría de la APERTURA (días 0-1) — el tramo que más compone.

Para cada jugador de un replay mide, hora por hora:
  - contrataciones (día/hora) y cuántas unidades hay realmente activas por hora
  - compra y COLOCACIÓN de animales (el reloj de S4.9 arranca al PLACE)
  - siembra por cultivo y hora; tiles ocupadas/vacías al cierre de d0 y d1
  - reparto de acciones: movimiento vs producción vs PASS (por día)
  - primer FEED, primer CARE, primer WATER
  - dinero al cierre de d0/d1 y caja ociosa

Uso: ./.venv/bin/python apertura.py replays/*.json          (audita a Rospel)
     ./.venv/bin/python apertura.py --all ~/Downloads/*.json (audita a ambos)
"""
import json
import sys
from collections import defaultdict

MOVE = {"NORTH", "SOUTH", "EAST", "WEST"}
PROD = {"PLANT", "WATER", "HARVEST", "FEED", "CARE", "DIG", "FERTILIZE",
        "BUILD_COOP", "BUILD_PASTURE", "PLACE", "COLLECT_FERTILIZER"}
LOGI = {"PICKUP", "DROP"}


def audit(d, p, days=2):
    steps = d["steps"]
    r = {"name": d["info"]["TeamNames"][p], "money_final": d["rewards"][p]}
    hires = defaultdict(list)          # dia -> horas
    bought = []                        # (dia, hora, animal)
    placed = []                        # (dia, hora, animal)
    planted = []                       # (dia, hora, crop)
    seeds_bought = []                  # (dia, hora, crop, n)
    land = []
    ops = defaultdict(lambda: defaultdict(int))   # dia -> categoria -> n
    opnames = defaultdict(lambda: defaultdict(int))
    firsts = {}
    units_by_hour = []                 # (dia, hora, n_unidades)

    for t in range(1, min(days * 24 + 1, len(steps))):
        obs = steps[t - 1][0]["observation"]
        day, hour = obs["day"], obs["hour"]
        farm = obs["farms"][p]
        n_units = 1 + len(farm["hands"])
        units_by_hour.append((day, hour, n_units))
        act = steps[t][p].get("action") or {}
        unit_ops = [act.get("farmer") or ["PASS"]] + list(act.get("hands") or [])
        for o in unit_ops:
            name = (o or ["PASS"])[0]
            opnames[day][name] += 1
            if name in MOVE:
                ops[day]["mover"] += 1
            elif name in PROD:
                ops[day]["producir"] += 1
            elif name in LOGI:
                ops[day]["logistica"] += 1
            else:
                ops[day]["PASS"] += 1
            if name in ("FEED", "CARE", "WATER", "PLANT", "HARVEST") and name not in firsts:
                firsts[name] = (day, hour)
            if name == "PLANT" and len(o) > 1:
                planted.append((day, hour, o[1]))
            if name == "PLACE" and len(o) > 1:
                placed.append((day, hour, o[1]))
                firsts.setdefault("PLACE", (day, hour))
        for m in act.get("market") or []:
            if not m:
                continue
            if m[0] == "HIRE":
                hires[day].append(hour)
            elif m[0] == "BUY_ANIMAL":
                bought.append((day, hour, m[1], int(m[2]) if len(m) > 2 else 1))
            elif m[0] == "BUY_SEED":
                seeds_bought.append((day, hour, m[1], int(m[2]) if len(m) > 2 else 1))
            elif m[0] == "BUY_LAND":
                land.append((day, hour))

    # --- estado al cierre de cada día ---
    snaps = {}
    for day in range(days + 1):
        t = min(day * 24, len(steps) - 1)
        obs = steps[t][0]["observation"]
        farm = obs["farms"][p]
        occ = plants = animals = structs = empt = 0
        for row in farm["tiles"]:
            for c in row:
                if c is None:
                    empt += 1
                elif isinstance(c, dict):
                    occ += 1
                    k = c.get("kind")
                    if k == "PLANT":
                        plants += 1
                    elif k in ("COOP", "PASTURE"):
                        structs += 1
                        if c.get("animal"):
                            animals += 1
        priv = steps[t][p]["observation"].get("private") or {}
        snaps[day] = dict(money=farm["money"], plantas=plants, animales=animals,
                          estructuras=structs, vacias=empt, ocupadas=occ,
                          semillas=dict(priv.get("seeds") or {}),
                          shed=dict(priv.get("shed") or {}))
    r.update(hires=dict(hires), bought=bought, placed=placed, planted=planted,
             seeds_bought=seeds_bought, land=land, ops={k: dict(v) for k, v in ops.items()},
             opnames={k: dict(v) for k, v in opnames.items()}, firsts=firsts,
             snaps=snaps, units_by_hour=units_by_hour)
    return r


def show(r):
    print(f"\n--- {r['name']}   (final ${r['money_final']:,.0f}) ---")
    for day in (0, 1):
        o = r["ops"].get(day, {})
        tot = sum(o.values()) or 1
        s = r["snaps"][day + 1]
        pl = [c for dd, hh, c in r["planted"] if dd == day]
        cnt = defaultdict(int)
        for c in pl:
            cnt[c] += 1
        print(f"  d{day}: unidades-turno {tot:3d} | mover {o.get('mover',0):3d} ({o.get('mover',0)/tot:4.0%}) "
              f"producir {o.get('producir',0):3d} ({o.get('producir',0)/tot:4.0%}) "
              f"logist {o.get('logistica',0):2d} PASS {o.get('PASS',0):3d} ({o.get('PASS',0)/tot:4.0%})")
        print(f"       hires h={r['hires'].get(day, [])}  plantado={dict(cnt)}  "
              f"animales comprados={[b for b in r['bought'] if b[0]==day]}")
        print(f"       cierre d{day}: ${s['money']:,.0f} | plantas {s['plantas']} animales {s['animales']} "
              f"estructuras {s['estructuras']} vacías {s['vacias']} | semillas {s['semillas']}")
    print(f"  colocaciones: {r['placed'][:8]}")
    print(f"  primeros: {r['firsts']}")
    print(f"  semillas compradas d0-1: {r['seeds_bought'][:10]}")
    uh = r["units_by_hour"]
    print("  unidades activas por hora d0: " + "".join(str(min(9, n)) for dd, hh, n in uh if dd == 0))
    print("  unidades activas por hora d1: " + "".join(str(min(9, n)) for dd, hh, n in uh if dd == 1))


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    both = "--all" in sys.argv
    agg = []
    for path in args:
        d = json.load(open(path))
        names = d["info"]["TeamNames"]
        print(f"\n{'='*78}\n{path.split('/')[-1]}  {names[0]} vs {names[1]}  {d['rewards']}")
        for p in (0, 1):
            if both or names[p].startswith("Rospel"):
                r = audit(d, p)
                show(r)
                agg.append(r)
    # resumen agregado
    if len(agg) > 1:
        by = defaultdict(list)
        for r in agg:
            by[r["name"]].append(r)
        print(f"\n{'='*78}\nRESUMEN AGREGADO")
        for name, rs in by.items():
            n = len(rs)
            def mean(f):
                return sum(f(r) for r in rs) / n
            print(f"\n{name} ({n} partidas, final medio ${mean(lambda r: r['money_final']):,.0f})")
            for day in (0, 1):
                mov = mean(lambda r: r["ops"].get(day, {}).get("mover", 0))
                pro = mean(lambda r: r["ops"].get(day, {}).get("producir", 0))
                pas = mean(lambda r: r["ops"].get(day, {}).get("PASS", 0))
                log = mean(lambda r: r["ops"].get(day, {}).get("logistica", 0))
                tot = mov + pro + pas + log or 1
                print(f"  d{day}: turnos-unidad {tot:5.1f} | mover {mov:5.1f} ({mov/tot:4.0%}) "
                      f"producir {pro:5.1f} ({pro/tot:4.0%}) logist {log:4.1f} PASS {pas:5.1f} ({pas/tot:4.0%})")
                print(f"        hires {mean(lambda r: len(r['hires'].get(day, []))):4.1f} | "
                      f"plantado {mean(lambda r: sum(1 for dd,_,_ in r['planted'] if dd==day)):4.1f} | "
                      f"animales comprados {mean(lambda r: sum(b[3] for b in r['bought'] if b[0]==day)):4.1f} | "
                      f"colocados {mean(lambda r: sum(1 for b in r['placed'] if b[0]==day)):4.1f}")
                s = lambda k: mean(lambda r: r["snaps"][day+1][k])
                print(f"        cierre: ${s('money'):,.0f} | plantas {s('plantas'):4.1f} animales {s('animales'):4.1f} "
                      f"estructuras {s('estructuras'):4.1f} vacías {s('vacias'):4.1f}")
            fh = [r["firsts"].get("PLACE") for r in rs if r["firsts"].get("PLACE")]
            ff = [r["firsts"].get("FEED") for r in rs if r["firsts"].get("FEED")]
            fc = [r["firsts"].get("CARE") for r in rs if r["firsts"].get("CARE")]
            def hstr(xs):
                if not xs:
                    return "nunca en d0-1"
                return f"d{sum(a for a,_ in xs)/len(xs):.1f} h{sum(b for _,b in xs)/len(xs):.1f} (n={len(xs)})"
            print(f"  1er PLACE: {hstr(fh)} | 1er FEED: {hstr(ff)} | 1er CARE: {hstr(fc)}")
