"""Evolución multi-generacional de estrategias, con novedad garantizada.

Cada generación: élites re-evaluadas + mutaciones de élites + inmigrantes
aleatorios frescos. Un registro de firmas canónicas (incluida la gen 1 previa)
garantiza que ninguna config se evalúe dos veces. Los seeds rotan por
generación para no sobreajustar; el panel de oponentes incluye al campeón
vigente y al mejor de la generación anterior (coevolución).

Fases finales: round-robin del top 10 histórico (seeds frescos) +
confirmación del ganador vs vacas_melon en seeds vírgenes + autopsia.

Uso:
    ./.venv/bin/python evolucion2.py --gens 14 --pop 40 --eps-seeds 3
    ./.venv/bin/python evolucion2.py --smoke     # validación rápida del loop
"""
import argparse
import json
import os
import random
import time
from collections import defaultdict
from multiprocessing import Pool

from autopsia import autopsy, print_report
from bots.arquetipos import OVEJAS_VACAS, VACAS_MELON
from harness import run_episode, spec_name

CROP_OPTS = {"CARROT": 10, "MELON": 14, "TOMATO": 6, "STRAWBERRY": 6}
ANIMAL_MAX = {"SHEEP": 8, "COW": 10, "GOOSE": 10}


def normalize(cfg):
    out = dict(cfg)
    out["animals"] = sorted([list(a) for a in cfg.get("animals", []) if a[1] > 0])
    out["plants"] = {k: v for k, v in sorted(cfg.get("plants", {}).items()) if v > 0}
    for k, default in (("care", False), ("collect_fert", False), ("buy_land", False),
                       ("fert_prio", 18), ("animal_harvest_at", 2), ("premium_hold_day", 0),
                       ("max_quadrants", 2), ("hands", 0)):
        out.setdefault(k, default)
    return out


def signature(cfg):
    return json.dumps(normalize(cfg), sort_keys=True, default=str)


def repair(cfg):
    """Coherencia mínima: wheat para alimentar, tierra si no cabe."""
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
        hands=rng.randint(1, 8),
        animals=animals,
        plants=plants,
        care=rng.random() < 0.9,
        collect_fert=rng.random() < 0.8,
        fert_prio=rng.choice([18, 35, 45, 60, 75]),
        animal_harvest_at=rng.choice([1, 2, 3, 4]),
        premium_hold_day=rng.choice([0, 0, 0, 8, 12, 16, 20]),
        buy_land=False,
        max_quadrants=2,
    )
    return repair(cfg)


def mutate(cfg, rng):
    c = json.loads(json.dumps(normalize(cfg)))
    c["animals"] = [tuple(a) for a in c["animals"]]
    for _ in range(rng.randint(1, 3)):
        m = rng.random()
        if m < 0.30 and c["animals"]:
            i = rng.randrange(len(c["animals"]))
            an, n = c["animals"][i]
            n = max(0, min(ANIMAL_MAX[an], n + rng.choice([-2, -1, 1, 1, 2])))
            c["animals"][i] = (an, n)
            c["animals"] = [(a, k) for a, k in c["animals"] if k > 0]
        elif m < 0.40:
            an = rng.choice(list(ANIMAL_MAX))
            if an not in dict(c["animals"]):
                c["animals"].append((an, rng.randint(1, 3)))
        elif m < 0.65:
            crop = rng.choice(["WHEAT"] + list(CROP_OPTS))
            mx = 16 if crop == "WHEAT" else CROP_OPTS[crop]
            cur = c["plants"].get(crop, 0)
            c["plants"][crop] = max(0, min(mx, cur + rng.choice([-3, -2, 2, 3])))
        elif m < 0.75:
            c["hands"] = max(1, min(8, c["hands"] + rng.choice([-1, 1])))
        elif m < 0.85:
            c["fert_prio"] = rng.choice([18, 35, 45, 60, 75])
        elif m < 0.92:
            c["animal_harvest_at"] = rng.choice([1, 2, 3, 4])
        else:
            c["premium_hold_day"] = rng.choice([0, 8, 12, 16, 20])
    c["plants"] = {k: v for k, v in c["plants"].items() if v > 0}
    return repair(c)


# Hipótesis dirigidas nuevas para la generación 0 (ninguna probada antes)
def seeded_gen0():
    return [
        ("vm_XL", dict(VACAS_MELON, animals=[("COW", 7)], plants={"WHEAT": 8, "MELON": 12, "STRAWBERRY": 3},
                       hands=6, max_quadrants=3)),
        ("vm_hold14", dict(VACAS_MELON, premium_hold_day=14)),
        ("vm_cosecha1", dict(VACAS_MELON, animal_harvest_at=1)),
        ("lecheria8", dict(hands=5, animals=[("COW", 8)], plants={"WHEAT": 10, "CARROT": 4}, care=True,
                           collect_fert=True, fert_prio=60, buy_land=True, max_quadrants=2)),
        ("fert_factory", dict(hands=5, animals=[("GOOSE", 10)], plants={"WHEAT": 12}, care=False,
                              collect_fert=True, fert_prio=75, buy_land=True, max_quadrants=2)),
        ("melonar", dict(hands=4, animals=[], plants={"MELON": 14, "CARROT": 8, "WHEAT": 4},
                         care=False, collect_fert=False, buy_land=True, max_quadrants=2)),
    ]


def eval_candidates(cands, panel, seed0, eps_seeds, steps, procs):
    jobs = []
    for c in cands:
        for opp in panel:
            for s in range(seed0, seed0 + eps_seeds):
                jobs.append((c, opp, s, steps))
                jobs.append((opp, c, s, steps))
    with Pool(procs) as pool:
        results = pool.map(run_episode, jobs)
    money = defaultdict(list)
    wins = defaultdict(int)
    cand_names = {spec_name(c) for c in cands}
    for r in results:
        for side in (0, 1):
            name = spec_name(r["p0"] if side == 0 else r["p1"])
            if name not in cand_names:
                continue
            my, their = r["money"][side], r["money"][1 - side]
            money[name].append(my)
            if my > their:
                wins[name] += 1
    fit = {n: sum(v) / len(v) for n, v in money.items()}
    return fit, wins, len(jobs)


def main(gens=14, pop=40, eps_seeds=3, steps=720, procs=None, out="results/evolucion2.json"):
    procs = procs or max(1, (os.cpu_count() or 2) - 1)
    rng = random.Random(20260817)
    registry = set()
    if os.path.exists("results/evolucion_gen1.json"):
        with open("results/evolucion_gen1.json") as f:
            for cfg in json.load(f)["candidatos"].values():
                cfg = dict(cfg)
                cfg["animals"] = [tuple(a) for a in cfg.get("animals", [])]
                registry.add(signature(cfg))
        print(f"registro inicial: {len(registry)} firmas de la gen 1 (no se repetirán)", flush=True)

    all_time = {}   # name -> (fitness, wins, cfg)
    panel = [("cfg", "panel_vm", dict(VACAS_MELON)), ("cfg", "panel_ov", dict(OVEJAS_VACAS))]

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
        population.append(("cfg", f"g0_{len(population):02d}", cfg))

    t_start = time.time()
    total_eps = 0
    for g in range(gens):
        seed0 = 10_000 + 997 * g
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
        # siguiente generación: élites + mutantes + inmigrantes
        elites = [by_name[n] for n in ranked[:6]]
        panel[1] = ("cfg", "panel_best", dict(elites[0][2]))  # coevolución
        nxt = [("cfg", f"g{g + 1}e_{i}", dict(e[2])) for i, e in enumerate(elites)]
        tries = 0
        while len(nxt) < pop - 10 and tries < 3000:
            tries += 1
            m = mutate(rng.choice(elites)[2], rng)
            if signature(m) in registry:
                continue
            registry.add(signature(m))
            nxt.append(("cfg", f"g{g + 1}m_{len(nxt):02d}", m))
        while len(nxt) < pop and tries < 6000:
            tries += 1
            cfg = sample(rng)
            if signature(cfg) in registry:
                continue
            registry.add(signature(cfg))
            nxt.append(("cfg", f"g{g + 1}i_{len(nxt):02d}", cfg))
        population = nxt

    # ---- final: top 10 histórico (configs distintas) + campeón vigente ----
    seen = set()
    finalists = [("cfg", "vacas_melon", dict(VACAS_MELON))]
    seen.add(signature(dict(VACAS_MELON)))
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
            for s in range(20_000, 20_000 + 3):
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
    print(f"\n=== TABLA FINAL (de {2 * 3 * (len(finalists) - 1)} episodios c/u) ===", flush=True)
    fin_by_name = {spec_name(c): c for c in finalists}
    for n in order:
        print(f"  {n:16s} {pts[n]:5.1f} | ${sum(fmoney[n]) / len(fmoney[n]):,.0f} | {json.dumps(fin_by_name[n][2], default=str)}", flush=True)

    winner = order[0]
    if winner != "vacas_melon":
        print(f"\nCONFIRMACIÓN en seeds vírgenes: {winner} vs vacas_melon (50 eps)", flush=True)
        cjobs = []
        for s in range(30_000, 30_000 + 25):
            cjobs.append((fin_by_name[winner], finalists[0], s, steps))
            cjobs.append((finalists[0], fin_by_name[winner], s, steps))
        with Pool(procs) as pool:
            cres = pool.map(run_episode, cjobs)
        w = l = 0
        wm, vm = [], []
        for r in cres:
            side = 0 if spec_name(r["p0"]) == winner else 1
            my, their = r["money"][side], r["money"][1 - side]
            wm.append(my)
            vm.append(their)
            if my > their:
                w += 1
            elif their > my:
                l += 1
        print(f"  {winner}: gana {w}, pierde {l} de {len(cres)} | ${sum(wm) / len(wm):,.0f} vs ${sum(vm) / len(vm):,.0f}", flush=True)
        print(f"\n=== AUTOPSIA: {winner} ===", flush=True)
        print_report(winner, autopsy(fin_by_name[winner], "starter", n_seeds=2, seed0=31_000))
    else:
        print("\nvacas_melon retiene el título.", flush=True)
    print(f"\nTOTAL: {total_eps + len(fjobs)} episodios evolutivos+finales en {(time.time() - t_start) / 60:.0f} min | histórico en {out}", flush=True)


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
