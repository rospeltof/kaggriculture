"""Evolución 5: escala contra el meta — panel des-endogamizado y mecánicas de ejecución.

Cambios vs evolución 4:
  - Panel: mimada_v4 + LN_CLONE_V4 (huella de mercado distinta a la nuestra;
    la ecología deja de ser de gemelos) + coevolución.
  - Techos altos: vacas hasta 16, ovejas 10, wheat 45, crop_tiles 50, 4 cuadrantes.
  - Mecánicas de ejecución como genes: multi_feeder, phased (fase de capital),
    tiles_per_unit (capacidad de riego por unidad).

Uso:
    ./.venv/bin/python evolucion5.py --gens 10 --pop 36 --eps-seeds 3
    ./.venv/bin/python evolucion5.py --smoke
"""
import argparse
import json
import os
import random
import time
from collections import defaultdict
from multiprocessing import Pool

from autopsia import autopsy, print_report
from bots.arquetipos import LN_CLONE_V4, MIMADA_V4
from evolucion2 import eval_candidates
from evolucion4 import KNOB_CHOICES as KC4
from evolucion4 import KNOB_DEFAULTS as KD4
from harness import run_episode, spec_name

CROP_OPTS = {"CARROT": 10, "MELON": 14, "TOMATO": 6, "STRAWBERRY": 24}
ANIMAL_MAX = {"SHEEP": 10, "COW": 16, "GOOSE": 10}
MAX_HANDS = 10

KNOB_DEFAULTS = dict(KD4, multi_feeder=False, phased=False, tiles_per_unit=5)
KNOB_CHOICES = dict(
    KC4,
    crop_tiles=[22, 30, 40, 50],
    tiles_per_unit=[4, 5, 6, 8],
)


def normalize(cfg):
    out = dict(cfg)
    out["animals"] = sorted([list(a) for a in cfg.get("animals", []) if a[1] > 0])
    out["plants"] = {k: v for k, v in sorted(cfg.get("plants", {}).items()) if v > 0}
    for k, default in KNOB_DEFAULTS.items():
        out.setdefault(k, default)
    if out.get("wheat_floor") == "auto":
        out.pop("wheat_floor")
        out["wheat_floor_auto"] = True
    return out


def signature(cfg):
    return json.dumps(normalize(cfg), sort_keys=True, default=str)


def to_cfg(cfg):
    c = json.loads(json.dumps(normalize(cfg)))
    c["animals"] = [tuple(a) for a in c["animals"]]
    c.pop("wheat_floor_auto", None)
    return c


def repair(cfg):
    total_an = sum(n for _, n in cfg["animals"])
    if total_an:
        cfg["plants"]["WHEAT"] = max(cfg["plants"].get("WHEAT", 0), min(total_an, 20))
    tiles = total_an + (cfg.get("crop_tiles", 22) if cfg.get("adaptive") else sum(cfg["plants"].values()))
    if tiles > 20:
        cfg["buy_land"] = True
        cfg["max_quadrants"] = max(cfg.get("max_quadrants", 2), 2 if tiles <= 40 else 3)
    if total_an > 10:
        cfg["multi_feeder"] = True   # rebaños grandes sin logística paralela = escapes
    return cfg


def sample(rng):
    animals = []
    for an, mx in ANIMAL_MAX.items():
        n = rng.choice([0, 0, 1, 3, rng.randint(0, mx), rng.randint(0, mx)])
        if n:
            animals.append((an, n))
    plants = {"WHEAT": rng.choice([4, 8, 12, 20, 30, 45])}
    for crop, mx in CROP_OPTS.items():
        n = rng.choice([0, 0, 3, 5, rng.randint(0, mx)])
        if n:
            plants[crop] = n
    cfg = dict(
        hands=rng.randint(6, MAX_HANDS),
        animals=animals,
        plants=plants,
        care=True,
        collect_fert=rng.random() < 0.85,
        zoning=rng.random() < 0.25,
        plant_near=rng.random() < 0.85,
        endgame=rng.random() < 0.9,
        adaptive=rng.random() < 0.5,
        multi_feeder=rng.random() < 0.6,
        phased=rng.random() < 0.6,
        buy_land=False,
        max_quadrants=rng.choice([2, 3, 3, 4]),
    )
    for k, choices in KNOB_CHOICES.items():
        cfg[k] = rng.choice(choices)
    return repair(cfg)


def mutate(cfg, rng):
    c = dict(to_cfg(cfg))
    for _ in range(rng.randint(1, 3)):
        m = rng.random()
        if m < 0.20 and c["animals"]:
            i = rng.randrange(len(c["animals"]))
            an, n = c["animals"][i]
            n = max(0, min(ANIMAL_MAX[an], n + rng.choice([-3, -1, 1, 2, 3])))
            c["animals"][i] = (an, n)
            c["animals"] = [(a, k) for a, k in c["animals"] if k > 0]
        elif m < 0.30:
            an = rng.choice(list(ANIMAL_MAX))
            if an not in dict(c["animals"]):
                c["animals"].append((an, rng.randint(1, 4)))
        elif m < 0.46:
            crop = rng.choice(["WHEAT"] + list(CROP_OPTS))
            mx = 45 if crop == "WHEAT" else CROP_OPTS[crop]
            c["plants"][crop] = max(0, min(mx, c["plants"].get(crop, 0) + rng.choice([-4, -2, 2, 4])))
        elif m < 0.54:
            c["hands"] = max(4, min(MAX_HANDS, c["hands"] + rng.choice([-1, 1])))
        elif m < 0.62:
            c["adaptive"] = not c.get("adaptive", False)
        elif m < 0.70:
            c["multi_feeder"] = not c.get("multi_feeder", False)
        elif m < 0.78:
            c["phased"] = not c.get("phased", False)
        elif m < 0.84:
            c["max_quadrants"] = rng.choice([2, 3, 4])
        else:
            k = rng.choice(list(KNOB_CHOICES))
            c[k] = rng.choice(KNOB_CHOICES[k])
    c["plants"] = {k: v for k, v in c["plants"].items() if v > 0}
    return repair(c)


def seeded_gen0():
    return [
        ("v4_base", dict(MIMADA_V4)),
        ("v4_mecanicas", dict(MIMADA_V4, multi_feeder=True, phased=True)),
        ("v4_escalada", dict(MIMADA_V4, crop_tiles=40, animals=[("COW", 8), ("SHEEP", 6)],
                             multi_feeder=True, phased=True, max_quadrants=3, tiles_per_unit=6, hands=10)),
        ("v4_titan", dict(MIMADA_V4, crop_tiles=50, animals=[("COW", 12), ("SHEEP", 6)],
                          multi_feeder=True, phased=True, max_quadrants=4, tiles_per_unit=8, hands=10)),
        ("clon_ln", dict(LN_CLONE_V4)),
        ("straw_meta", dict(hands=10, animals=[("COW", 8), ("SHEEP", 4)],
                            plants={"WHEAT": 20, "STRAWBERRY": 20}, care=True, collect_fert=True,
                            fert_prio=45, prio_care=70, prio_dig=45, plant_near=True, endgame=True,
                            multi_feeder=True, phased=True, buy_land=True, max_quadrants=3)),
    ]


def load_registry():
    registry = set()
    for path in ("results/evolucion_gen1.json", "results/evolucion2.json",
                 "results/evolucion3.json", "results/evolucion4.json"):
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


def main(gens=10, pop=36, eps_seeds=3, steps=720, procs=None, out="results/evolucion5.json"):
    procs = procs or max(1, (os.cpu_count() or 2) - 1)
    rng = random.Random(20260828)
    registry = load_registry()
    print(f"registro inicial: {len(registry)} firmas de gens 1-4", flush=True)

    all_time = {}
    panel = [("cfg", "panel_v4", dict(MIMADA_V4)), ("cfg", "panel_clon", dict(LN_CLONE_V4))]

    population = []
    for name, cfg in seeded_gen0():
        cfg = to_cfg(repair(to_cfg(cfg)))
        if signature(cfg) not in registry:
            registry.add(signature(cfg))
            population.append(("cfg", name, cfg))
    while len(population) < pop:
        cfg = sample(rng)
        if signature(cfg) in registry:
            continue
        registry.add(signature(cfg))
        population.append(("cfg", f"m0_{len(population):02d}", cfg))

    t_start = time.time()
    total_eps = 0
    for g in range(gens):
        seed0 = 400_000 + 997 * g
        t0 = time.time()
        fit, wins, n_eps = eval_candidates(population, panel, seed0, eps_seeds, steps, procs)
        total_eps += n_eps
        by_name = {spec_name(c): c for c in population}
        ranked = sorted(fit, key=lambda n: -fit[n])
        for n in ranked:
            all_time[n] = (fit[n], wins[n], by_name[n][2])
        best = ranked[0]
        bc = by_name[best][2]
        print(f"gen {g:02d} | {n_eps} eps en {time.time() - t0:.0f}s | mejor: {best} ${fit[best]:,.0f} "
              f"({wins[best]}/{2 * eps_seeds * len(panel)}, adapt={bc.get('adaptive')}, mf={bc.get('multi_feeder')}, "
              f"ph={bc.get('phased')}) | total {total_eps}", flush=True)
        with open(out, "w") as f:
            json.dump({n: {"fitness": v[0], "wins": v[1], "cfg": v[2]} for n, v in all_time.items()},
                      f, indent=1, default=str)
        if g == gens - 1:
            break
        elites = [by_name[n] for n in ranked[:5]]
        panel[1] = ("cfg", "panel_best", dict(elites[0][2]))
        nxt = [("cfg", f"m{g + 1}e_{i}", dict(e[2])) for i, e in enumerate(elites)]
        tries = 0
        while len(nxt) < pop - 8 and tries < 4000:
            tries += 1
            mu = mutate(rng.choice(elites)[2], rng)
            if signature(mu) in registry:
                continue
            registry.add(signature(mu))
            nxt.append(("cfg", f"m{g + 1}m_{len(nxt):02d}", to_cfg(mu)))
        while len(nxt) < pop and tries < 8000:
            tries += 1
            cfg = sample(rng)
            if signature(cfg) in registry:
                continue
            registry.add(signature(cfg))
            nxt.append(("cfg", f"m{g + 1}i_{len(nxt):02d}", cfg))
        population = nxt

    seen = {signature(dict(MIMADA_V4)), signature(dict(LN_CLONE_V4))}
    finalists = [("cfg", "mimada_v4", to_cfg(dict(MIMADA_V4))), ("cfg", "clon_ln_v4", to_cfg(dict(LN_CLONE_V4)))]
    for n in sorted(all_time, key=lambda k: -all_time[k][0]):
        cfg = to_cfg(all_time[n][2])
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
            for s in range(410_000, 410_000 + 3):
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
    fin_by = {spec_name(c): c for c in finalists}
    print("\n=== TABLA FINAL ===", flush=True)
    for n in order:
        print(f"  {n:14s} {pts[n]:5.1f} | ${sum(fmoney[n]) / len(fmoney[n]):,.0f} | {json.dumps(fin_by[n][2], default=str)}", flush=True)

    winner = order[0]
    if winner != "mimada_v4":
        print(f"\nCONFIRMACIÓN seeds vírgenes: {winner} vs mimada_v4 (50 eps)", flush=True)
        cjobs = []
        for s in range(420_000, 420_000 + 25):
            cjobs.append((fin_by[winner], finalists[0], s, steps))
            cjobs.append((finalists[0], fin_by[winner], s, steps))
        with Pool(procs) as pool:
            cres = pool.map(run_episode, cjobs)
        w = l = 0
        wm, vm = [], []
        for r in cres:
            side = 0 if spec_name(r["p0"]) == winner else 1
            my, their = r["money"][side], r["money"][1 - side]
            wm.append(my)
            vm.append(their)
            w += my > their
            l += their > my
        print(f"  {winner}: gana {w}, pierde {l} de {len(cres)} | ${sum(wm) / len(wm):,.0f} vs ${sum(vm) / len(vm):,.0f}", flush=True)
        print_report(winner, autopsy(fin_by[winner], "starter", n_seeds=2, seed0=430_000))
    else:
        print("\nmimada_v4 retiene el título.", flush=True)
    print(f"\nTOTAL: {total_eps + len(fjobs)} episodios en {(time.time() - t_start) / 60:.0f} min", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--gens", type=int, default=10)
    ap.add_argument("--pop", type=int, default=36)
    ap.add_argument("--eps-seeds", type=int, default=3)
    ap.add_argument("--procs", type=int, default=None)
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    if args.smoke:
        main(gens=2, pop=8, eps_seeds=1, steps=240)
    else:
        main(gens=args.gens, pop=args.pop, eps_seeds=args.eps_seeds, procs=args.procs)
