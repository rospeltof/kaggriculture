"""Evolución 4: ¿planificación adaptativa al mercado o mix fijo? Que decida la selección.

Espacio: chasis v2 (plant_near + endgame de serie) con la capa adaptativa y sus
perillas (mkt_opp_factor, wheat_floor, crop_tiles) compitiendo contra planes
fijos, más todas las perillas previas. Registro anti-repetición con gens 1-3.
Panel: mimada_v2 (campeón vigente) + mejor de la generación anterior.

Uso:
    ./.venv/bin/python evolucion4.py --gens 10 --pop 36 --eps-seeds 3
    ./.venv/bin/python evolucion4.py --smoke
"""
import argparse
import json
import os
import random
import time
from collections import defaultdict
from multiprocessing import Pool

from autopsia import autopsy, print_report
from bots.arquetipos import MIMADA_V2, MIMADA_V3
from evolucion2 import eval_candidates
from evolucion3 import ANIMAL_MAX, CROP_OPTS, MAX_HANDS
from evolucion3 import KNOB_CHOICES as KC3
from evolucion3 import KNOB_DEFAULTS as KD3
from harness import run_episode, spec_name

KNOB_DEFAULTS = dict(KD3, plant_near=False, endgame=False, grow=False, prio_dig=8,
                     adaptive=False, crop_tiles=22, wheat_floor="auto", mkt_opp_factor=2)
KNOB_CHOICES = dict(
    KC3,
    prio_dig=[8, 20, 30, 45],
    crop_tiles=[16, 20, 22, 26, 30],
    wheat_floor=["auto", 4, 6, 8, 10],
    mkt_opp_factor=[1, 2, 3],
)


def normalize(cfg):
    out = dict(cfg)
    out["animals"] = sorted([list(a) for a in cfg.get("animals", []) if a[1] > 0])
    out["plants"] = {k: v for k, v in sorted(cfg.get("plants", {}).items()) if v > 0}
    for k, default in KNOB_DEFAULTS.items():
        out.setdefault(k, default)
    if out.get("wheat_floor") == "auto":
        out.pop("wheat_floor")   # el chasis usa el rebaño como default
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
        cfg["plants"]["WHEAT"] = max(cfg["plants"].get("WHEAT", 0), total_an)
    tiles = total_an + (cfg.get("crop_tiles", 22) if cfg.get("adaptive") else sum(cfg["plants"].values()))
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
    plants = {"WHEAT": rng.choice([0, 4, 6, 8, 10, 12])}
    for crop, mx in CROP_OPTS.items():
        n = rng.choice([0, 0, 0, 3, 5, rng.randint(0, mx)])
        if n:
            plants[crop] = n
    cfg = dict(
        hands=rng.randint(4, MAX_HANDS),
        animals=animals,
        plants=plants,
        care=True,
        collect_fert=rng.random() < 0.85,
        zoning=False,
        plant_near=rng.random() < 0.8,
        endgame=rng.random() < 0.8,
        adaptive=rng.random() < 0.5,
        buy_land=False,
        max_quadrants=rng.choice([2, 2, 2, 3]),
    )
    for k, choices in KNOB_CHOICES.items():
        cfg[k] = rng.choice(choices)
    return repair(cfg)


def mutate(cfg, rng):
    c = dict(to_cfg(cfg))
    for _ in range(rng.randint(1, 3)):
        m = rng.random()
        if m < 0.18 and c["animals"]:
            i = rng.randrange(len(c["animals"]))
            an, n = c["animals"][i]
            n = max(0, min(ANIMAL_MAX[an], n + rng.choice([-2, -1, 1, 1, 2])))
            c["animals"][i] = (an, n)
            c["animals"] = [(a, k) for a, k in c["animals"] if k > 0]
        elif m < 0.34:
            crop = rng.choice(["WHEAT"] + list(CROP_OPTS))
            mx = 16 if crop == "WHEAT" else CROP_OPTS[crop]
            c["plants"][crop] = max(0, min(mx, c["plants"].get(crop, 0) + rng.choice([-3, -2, 2, 3])))
        elif m < 0.42:
            c["hands"] = max(2, min(MAX_HANDS, c["hands"] + rng.choice([-1, 1])))
        elif m < 0.52:
            c["adaptive"] = not c.get("adaptive", False)
        elif m < 0.60:
            c["plant_near"] = not c.get("plant_near", False)
        elif m < 0.66:
            c["endgame"] = not c.get("endgame", False)
        else:
            k = rng.choice(list(KNOB_CHOICES))
            c[k] = rng.choice(KNOB_CHOICES[k])
    c["plants"] = {k: v for k, v in c["plants"].items() if v > 0}
    return repair(c)


def seeded_gen0():
    return [
        ("v3_actual", dict(MIMADA_V3)),
        ("v3_opp1", dict(MIMADA_V3, mkt_opp_factor=1)),
        ("v3_opp3", dict(MIMADA_V3, mkt_opp_factor=3)),
        ("v3_tiles28", dict(MIMADA_V3, crop_tiles=28, buy_land=True, max_quadrants=3)),
        ("v3_wf4", dict(MIMADA_V3, wheat_floor=4)),
        ("v3_wf10", dict(MIMADA_V3, wheat_floor=10)),
        ("v2_dig30", dict(MIMADA_V2, prio_dig=30)),
    ]


def load_registry():
    registry = set()
    for path in ("results/evolucion_gen1.json", "results/evolucion2.json", "results/evolucion3.json"):
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


def main(gens=10, pop=36, eps_seeds=3, steps=720, procs=None, out="results/evolucion4.json"):
    procs = procs or max(1, (os.cpu_count() or 2) - 1)
    rng = random.Random(20260827)
    registry = load_registry()
    print(f"registro inicial: {len(registry)} firmas de gens 1-3", flush=True)

    all_time = {}
    panel = [("cfg", "panel_v2", dict(MIMADA_V2)), ("cfg", "panel_best", dict(MIMADA_V3))]

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
        population.append(("cfg", f"k0_{len(population):02d}", cfg))

    t_start = time.time()
    total_eps = 0
    for g in range(gens):
        seed0 = 200_000 + 997 * g
        t0 = time.time()
        fit, wins, n_eps = eval_candidates(population, panel, seed0, eps_seeds, steps, procs)
        total_eps += n_eps
        by_name = {spec_name(c): c for c in population}
        ranked = sorted(fit, key=lambda n: -fit[n])
        for n in ranked:
            all_time[n] = (fit[n], wins[n], by_name[n][2])
        best = ranked[0]
        ad = by_name[best][2].get("adaptive")
        print(f"gen {g:02d} | {n_eps} eps en {time.time() - t0:.0f}s | mejor: {best} ${fit[best]:,.0f} "
              f"({wins[best]}/{2 * eps_seeds * len(panel)}, adaptive={ad}) | total {total_eps}", flush=True)
        with open(out, "w") as f:
            json.dump({n: {"fitness": v[0], "wins": v[1], "cfg": v[2]} for n, v in all_time.items()},
                      f, indent=1, default=str)
        if g == gens - 1:
            break
        elites = [by_name[n] for n in ranked[:5]]
        panel[1] = ("cfg", "panel_best", dict(elites[0][2]))
        nxt = [("cfg", f"k{g + 1}e_{i}", dict(e[2])) for i, e in enumerate(elites)]
        tries = 0
        while len(nxt) < pop - 8 and tries < 4000:
            tries += 1
            m = mutate(rng.choice(elites)[2], rng)
            if signature(m) in registry:
                continue
            registry.add(signature(m))
            nxt.append(("cfg", f"k{g + 1}m_{len(nxt):02d}", to_cfg(m)))
        while len(nxt) < pop and tries < 8000:
            tries += 1
            cfg = sample(rng)
            if signature(cfg) in registry:
                continue
            registry.add(signature(cfg))
            nxt.append(("cfg", f"k{g + 1}i_{len(nxt):02d}", cfg))
        population = nxt

    # final: top 9 distinto + mimada_v2
    seen = {signature(dict(MIMADA_V2))}
    finalists = [("cfg", "mimada_v2", to_cfg(dict(MIMADA_V2)))]
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
            for s in range(210_000, 210_000 + 3):
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
    if winner != "mimada_v2":
        print(f"\nCONFIRMACIÓN seeds vírgenes: {winner} vs mimada_v2 (50 eps)", flush=True)
        cjobs = []
        for s in range(220_000, 220_000 + 25):
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
        print_report(winner, autopsy(fin_by[winner], "starter", n_seeds=2, seed0=230_000))
    else:
        print("\nmimada_v2 retiene el título.", flush=True)
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
