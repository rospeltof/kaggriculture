"""Evolución 3: búsqueda sobre configuración + POLÍTICA (el cerebro como perillas).

Además del espacio de granja (animales, cultivos, peones — ahora hasta 10),
explora el comportamiento del scheduler: prioridades de feed/water/harvest/care/
plant, urgencia por hora, bonus de ventana, zonificación de unidades y su
umbral de escalamiento. El registro anti-repetición carga las firmas de las
generaciones 1 y 2. Panel: ocho_manos (campeón) + vacas_melon; coevolución.

Uso:
    ./.venv/bin/python evolucion3.py --gens 14 --pop 40 --eps-seeds 3
    ./.venv/bin/python evolucion3.py --smoke
"""
import argparse
import json
import os
import random
import time
from collections import defaultdict
from multiprocessing import Pool

from autopsia import autopsy, print_report
from bots.arquetipos import OCHO_MANOS, VACAS_MELON
from evolucion2 import eval_candidates
from harness import run_episode, spec_name

CROP_OPTS = {"CARROT": 10, "MELON": 14, "TOMATO": 6, "STRAWBERRY": 6}
ANIMAL_MAX = {"SHEEP": 8, "COW": 10, "GOOSE": 10}
MAX_HANDS = 10

KNOB_DEFAULTS = {
    "care": False, "collect_fert": False, "buy_land": False, "fert_prio": 18,
    "animal_harvest_at": 2, "premium_hold_day": 0, "max_quadrants": 2, "hands": 0,
    "zoning": False, "zone_fallback_prio": 70,
    "prio_feed": 88, "prio_water": 50, "prio_urgency": 25, "prio_win_bonus": 12,
    "prio_harvest": 62, "prio_care": 46, "prio_plant": 40,
}
KNOB_CHOICES = {
    "zone_fallback_prio": [60, 70, 80, 90],
    "prio_feed": [75, 82, 88, 94],
    "prio_water": [38, 44, 50, 58, 66],
    "prio_urgency": [0, 12, 25, 40],
    "prio_win_bonus": [0, 6, 12, 20],
    "prio_harvest": [50, 56, 62, 70, 78],
    "prio_care": [25, 35, 46, 58, 70],
    "prio_plant": [28, 34, 40, 48],
    "fert_prio": [18, 35, 45, 60, 75],
    "animal_harvest_at": [1, 2, 3, 4],
    "premium_hold_day": [0, 8, 12, 16, 20],
}


def normalize(cfg):
    out = dict(cfg)
    out["animals"] = sorted([list(a) for a in cfg.get("animals", []) if a[1] > 0])
    out["plants"] = {k: v for k, v in sorted(cfg.get("plants", {}).items()) if v > 0}
    for k, default in KNOB_DEFAULTS.items():
        out.setdefault(k, default)
    return out


def signature(cfg):
    return json.dumps(normalize(cfg), sort_keys=True, default=str)


def repair(cfg):
    total_an = sum(n for _, n in cfg["animals"])
    if total_an:
        cfg["plants"]["WHEAT"] = max(cfg["plants"].get("WHEAT", 0), total_an)
    tiles = total_an + sum(cfg["plants"].values())
    if tiles > 20:
        cfg["buy_land"] = True
        cfg["max_quadrants"] = max(cfg.get("max_quadrants", 2), 2 if tiles <= 40 else 3)
    return cfg


def sample(rng):
    animals = []
    for an, mx in ANIMAL_MAX.items():
        n = rng.choice([0, 0, 0, 1, 2, 3, rng.randint(0, mx)])
        if n:
            animals.append((an, n))
    plants = {"WHEAT": rng.choice([0, 4, 6, 8, 10, 12, 16])}
    for crop, mx in CROP_OPTS.items():
        n = rng.choice([0, 0, 0, 3, 5, rng.randint(0, mx)])
        if n:
            plants[crop] = n
    cfg = dict(
        hands=rng.randint(2, MAX_HANDS),
        animals=animals,
        plants=plants,
        care=rng.random() < 0.9,
        collect_fert=rng.random() < 0.85,
        zoning=rng.random() < 0.5,
        buy_land=False,
        max_quadrants=2,
    )
    for k, choices in KNOB_CHOICES.items():
        cfg[k] = rng.choice(choices)
    return repair(cfg)


def mutate(cfg, rng):
    c = json.loads(json.dumps(normalize(cfg)))
    c["animals"] = [tuple(a) for a in c["animals"]]
    for _ in range(rng.randint(1, 3)):
        m = rng.random()
        if m < 0.22 and c["animals"]:
            i = rng.randrange(len(c["animals"]))
            an, n = c["animals"][i]
            n = max(0, min(ANIMAL_MAX[an], n + rng.choice([-2, -1, 1, 1, 2])))
            c["animals"][i] = (an, n)
            c["animals"] = [(a, k) for a, k in c["animals"] if k > 0]
        elif m < 0.30:
            an = rng.choice(list(ANIMAL_MAX))
            if an not in dict(c["animals"]):
                c["animals"].append((an, rng.randint(1, 3)))
        elif m < 0.48:
            crop = rng.choice(["WHEAT"] + list(CROP_OPTS))
            mx = 16 if crop == "WHEAT" else CROP_OPTS[crop]
            c["plants"][crop] = max(0, min(mx, c["plants"].get(crop, 0) + rng.choice([-3, -2, 2, 3])))
        elif m < 0.58:
            c["hands"] = max(1, min(MAX_HANDS, c["hands"] + rng.choice([-1, 1, 1])))
        elif m < 0.66:
            c["zoning"] = not c.get("zoning", False)
        else:
            k = rng.choice(list(KNOB_CHOICES))
            c[k] = rng.choice(KNOB_CHOICES[k])
    c["plants"] = {k: v for k, v in c["plants"].items() if v > 0}
    return repair(c)


def seeded_gen0():
    return [
        ("om_zonas", dict(OCHO_MANOS, zoning=True)),
        ("om_zonas_esc80", dict(OCHO_MANOS, zoning=True, zone_fallback_prio=80)),
        ("om_10manos", dict(OCHO_MANOS, hands=10)),
        ("om_10manos_zonas", dict(OCHO_MANOS, hands=10, zoning=True)),
        ("om_care_alto", dict(OCHO_MANOS, prio_care=70)),
        ("om_urgencia0", dict(OCHO_MANOS, prio_urgency=0)),
    ]


def load_registry():
    registry = set()
    for path in ("results/evolucion_gen1.json", "results/evolucion2.json"):
        if not os.path.exists(path):
            continue
        with open(path) as f:
            data = json.load(f)
        cfgs = data["candidatos"].values() if "candidatos" in data else [v["cfg"] for v in data.values()]
        for cfg in cfgs:
            cfg = dict(cfg)
            cfg["animals"] = [tuple(a) for a in cfg.get("animals", [])]
            registry.add(signature(cfg))
    return registry


def main(gens=14, pop=40, eps_seeds=3, steps=720, procs=None, out="results/evolucion3.json"):
    procs = procs or max(1, (os.cpu_count() or 2) - 1)
    rng = random.Random(20260818)
    registry = load_registry()
    print(f"registro inicial: {len(registry)} firmas de gens 1-2 (no se repetirán)", flush=True)

    all_time = {}
    panel = [("cfg", "panel_om", dict(OCHO_MANOS)), ("cfg", "panel_vm", dict(VACAS_MELON))]

    population = []
    for name, cfg in seeded_gen0():
        cfg = repair(json.loads(json.dumps(normalize(cfg))))
        cfg["animals"] = [tuple(a) for a in cfg["animals"]]
        if signature(cfg) not in registry:
            registry.add(signature(cfg))
            population.append(("cfg", name, cfg))
    while len(population) < pop:
        cfg = sample(rng)
        if signature(cfg) in registry:
            continue
        registry.add(signature(cfg))
        population.append(("cfg", f"h0_{len(population):02d}", cfg))

    t_start = time.time()
    total_eps = 0
    for g in range(gens):
        seed0 = 50_000 + 997 * g
        t0 = time.time()
        fit, wins, n_eps = eval_candidates(population, panel, seed0, eps_seeds, steps, procs)
        total_eps += n_eps
        by_name = {spec_name(c): c for c in population}
        ranked = sorted(fit, key=lambda n: -fit[n])
        for n in ranked:
            all_time[n] = (fit[n], wins[n], by_name[n][2])
        best = ranked[0]
        print(f"gen {g:02d} | {n_eps} eps en {time.time() - t0:.0f}s | mejor: {best} ${fit[best]:,.0f} "
              f"({wins[best]}/{2 * eps_seeds * len(panel)} vs panel) | acumulado {total_eps} eps", flush=True)
        with open(out, "w") as f:
            json.dump({n: {"fitness": v[0], "wins": v[1], "cfg": v[2]} for n, v in all_time.items()},
                      f, indent=1, default=str)
        if g == gens - 1:
            break
        elites = [by_name[n] for n in ranked[:6]]
        panel[1] = ("cfg", "panel_best", dict(elites[0][2]))
        nxt = [("cfg", f"h{g + 1}e_{i}", dict(e[2])) for i, e in enumerate(elites)]
        tries = 0
        while len(nxt) < pop - 10 and tries < 4000:
            tries += 1
            m = mutate(rng.choice(elites)[2], rng)
            if signature(m) in registry:
                continue
            registry.add(signature(m))
            nxt.append(("cfg", f"h{g + 1}m_{len(nxt):02d}", m))
        while len(nxt) < pop and tries < 8000:
            tries += 1
            cfg = sample(rng)
            if signature(cfg) in registry:
                continue
            registry.add(signature(cfg))
            nxt.append(("cfg", f"h{g + 1}i_{len(nxt):02d}", cfg))
        population = nxt

    # ---- final: top 9 histórico distinto + ocho_manos ----
    seen = set()
    finalists = [("cfg", "ocho_manos", dict(OCHO_MANOS))]
    seen.add(signature(dict(OCHO_MANOS)))
    for n in sorted(all_time, key=lambda k: -all_time[k][0]):
        cfg = dict(all_time[n][2])
        cfg["animals"] = [tuple(a) for a in cfg["animals"]]
        sig = signature(cfg)
        if sig in seen:
            continue
        seen.add(sig)
        finalists.append(("cfg", n, cfg))
        if len(finalists) >= 10:
            break

    fjobs = []
    for i in range(len(finalists)):
        for j in range(i + 1, len(finalists)):
            for s in range(60_000, 60_000 + 3):
                fjobs.append((finalists[i], finalists[j], s, steps))
                fjobs.append((finalists[j], finalists[i], s, steps))
    print(f"\nFINAL: {len(finalists)} finalistas, {len(fjobs)} episodios", flush=True)
    with Pool(procs) as pool:
        fresults = pool.map(run_episode, fjobs)
    pts = defaultdict(float)
    fmoney = defaultdict(list)
    for r in fresults:
        n0, n1 = spec_name(r["p0"]), spec_name(r["p1"])
        m0, m1 = r["money"]
        fmoney[n0].append(m0)
        fmoney[n1].append(m1)
        pts[n0] += 1 if m0 > m1 else (0.5 if m0 == m1 else 0)
        pts[n1] += 1 if m1 > m0 else (0.5 if m0 == m1 else 0)
    order = sorted(fmoney, key=lambda n: -pts[n])
    fin_by_name = {spec_name(c): c for c in finalists}
    print(f"\n=== TABLA FINAL (de {2 * 3 * (len(finalists) - 1)} episodios c/u) ===", flush=True)
    for n in order:
        print(f"  {n:18s} {pts[n]:5.1f} | ${sum(fmoney[n]) / len(fmoney[n]):,.0f} | {json.dumps(fin_by_name[n][2], default=str)}", flush=True)

    winner = order[0]
    if winner != "ocho_manos":
        print(f"\nCONFIRMACIÓN en seeds vírgenes: {winner} vs ocho_manos (50 eps)", flush=True)
        cjobs = []
        for s in range(70_000, 70_000 + 25):
            cjobs.append((fin_by_name[winner], finalists[0], s, steps))
            cjobs.append((finalists[0], fin_by_name[winner], s, steps))
        with Pool(procs) as pool:
            cres = pool.map(run_episode, cjobs)
        w = l = 0
        wm, om = [], []
        for r in cres:
            side = 0 if spec_name(r["p0"]) == winner else 1
            my, their = r["money"][side], r["money"][1 - side]
            wm.append(my)
            om.append(their)
            if my > their:
                w += 1
            elif their > my:
                l += 1
        print(f"  {winner}: gana {w}, pierde {l} de {len(cres)} | ${sum(wm) / len(wm):,.0f} vs ${sum(om) / len(om):,.0f}", flush=True)
        print(f"\n=== AUTOPSIA: {winner} ===", flush=True)
        print_report(winner, autopsy(fin_by_name[winner], "starter", n_seeds=2, seed0=71_000))
    else:
        print("\nocho_manos retiene el título.", flush=True)
    print(f"\nTOTAL: {total_eps + len(fjobs)} episodios en {(time.time() - t_start) / 60:.0f} min | histórico en {out}", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--gens", type=int, default=14)
    ap.add_argument("--pop", type=int, default=40)
    ap.add_argument("--eps-seeds", type=int, default=3)
    ap.add_argument("--procs", type=int, default=None)
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    if args.smoke:
        main(gens=2, pop=8, eps_seeds=1, steps=240)
    else:
        main(gens=args.gens, pop=args.pop, eps_seeds=args.eps_seeds, procs=args.procs)
