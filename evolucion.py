"""Búsqueda en masa sobre el espacio de estrategias — generación 1.

Genera una población de configs no probadas (aleatorias + hipótesis dirigidas),
las criba en masa contra el campeón actual (fitness = dinero propio, con espejo),
y lleva a las mejores a una final round-robin contra campeón y subcampeón.

El fitness contra un rival fijo tiene un sesgo conocido: mide coexistir con el
footprint de mercado del campeón. La final round-robin corrige en parte.

Uso:
    ./.venv/bin/python evolucion.py --poblacion 48 --screen-seeds 3 --final-seeds 4
"""
import argparse
import json
import os
import random
from collections import defaultdict
from multiprocessing import Pool

from autopsia import autopsy, print_report
from bots.arquetipos import GANSOS, OVEJAS_VACAS
from harness import run_episode, spec_name

CHAMP = ("cfg", "campeon", dict(OVEJAS_VACAS))
SUBCAMP = ("cfg", "gansos", dict(GANSOS))

# Hipótesis dirigidas que nunca probamos (motivadas por la autopsia del torneo 001)
SEEDED = [
    ("cfg", "campeon_fert60", dict(OVEJAS_VACAS, fert_prio=60)),
    ("cfg", "puro_ovejas6", dict(hands=4, animals=[("SHEEP", 6)], plants={"WHEAT": 8, "MELON": 4},
                                 care=True, collect_fert=True, fert_prio=60)),
    ("cfg", "vacas_puras6", dict(hands=4, animals=[("COW", 6)], plants={"WHEAT": 8, "CARROT": 4},
                                 care=True, collect_fert=True, fert_prio=60)),
    ("cfg", "granja_fert", dict(hands=4, animals=[("SHEEP", 2), ("COW", 2), ("GOOSE", 4)],
                                plants={"WHEAT": 10}, care=True, collect_fert=True, fert_prio=75)),
    ("cfg", "ovejas_vacas_XL", dict(hands=5, animals=[("SHEEP", 4), ("COW", 4)],
                                    plants={"WHEAT": 10, "MELON": 4}, care=True, collect_fert=True,
                                    fert_prio=60, buy_land=True, max_quadrants=2)),
    ("cfg", "mixto_cultivos", dict(hands=3, animals=[("SHEEP", 2), ("COW", 2)],
                                   plants={"WHEAT": 8, "CARROT": 5, "MELON": 4},
                                   care=True, collect_fert=True, fert_prio=60)),
]


def sample(rng, i):
    sheep = rng.choice([0, 0, 1, 2, 3, 4, 5, 6])
    cow = rng.choice([0, 0, 1, 2, 3, 4, 5, 6])
    goose = rng.choice([0, 0, 0, 2, 4, 6, 8])
    animals = [(a, n) for a, n in (("SHEEP", sheep), ("COW", cow), ("GOOSE", goose)) if n]
    total_an = sheep + cow + goose
    plants = {"WHEAT": max(total_an, rng.choice([0, 4, 6, 8, 10, 12, 14]))}
    for crop, opts in (("CARROT", [0, 0, 3, 5, 8]), ("MELON", [0, 0, 3, 5, 8]),
                       ("TOMATO", [0, 0, 3, 5]), ("STRAWBERRY", [0, 0, 3, 5])):
        n = rng.choice(opts)
        if n:
            plants[crop] = n
    tiles = total_an + sum(plants.values())
    cfg = dict(
        hands=rng.choice([1, 2, 3, 4, 5, 6]),
        animals=animals,
        plants=plants,
        care=rng.random() < 0.85,
        collect_fert=rng.random() < 0.7,
        fert_prio=rng.choice([18, 45, 60]),
        buy_land=tiles > 20,
        max_quadrants=2,
    )
    return ("cfg", f"g1_{i:02d}", cfg)


def main(poblacion=48, screen_seeds=3, final_seeds=4, seed0=3000, rng_seed=7):
    rng = random.Random(rng_seed)
    n_random = poblacion - len(SEEDED)
    candidates = SEEDED + [sample(rng, i) for i in range(n_random)]

    # ---- fase 1: criba en masa contra el campeón ----
    jobs = []
    for cand in candidates:
        for s in range(seed0, seed0 + screen_seeds):
            jobs.append((cand, CHAMP, s, 720))
            jobs.append((CHAMP, cand, s, 720))
    print(f"CRIBA: {len(candidates)} candidatos x {2 * screen_seeds} episodios = {len(jobs)} episodios")
    with Pool(max(1, (os.cpu_count() or 2) - 1)) as pool:
        results = pool.map(run_episode, jobs)

    fitness = defaultdict(list)
    wins_vs_champ = defaultdict(int)
    for r in results:
        for side in (0, 1):
            name = spec_name(r["p0"] if side == 0 else r["p1"])
            if name == "campeon":
                continue
            my, their = r["money"][side], r["money"][1 - side]
            fitness[name].append(my)
            if my > their:
                wins_vs_champ[name] += 1

    ranked = sorted(fitness, key=lambda n: -sum(fitness[n]) / len(fitness[n]))
    print("\nTOP 10 de la criba (dinero propio medio vs campeón | victorias):")
    by_name = {spec_name(c): c for c in candidates}
    for name in ranked[:10]:
        avg = sum(fitness[name]) / len(fitness[name])
        print(f"  {name:20s} ${avg:>9,.0f} | {wins_vs_champ[name]}/{2 * screen_seeds} vs campeón | {json.dumps(by_name[name][2], default=str)}")

    # ---- fase 2: final round-robin (top 6 + campeón + gansos) ----
    finalists = [by_name[n] for n in ranked[:6]] + [CHAMP, SUBCAMP]
    fjobs = []
    for i in range(len(finalists)):
        for j in range(i + 1, len(finalists)):
            for s in range(seed0 + 100, seed0 + 100 + final_seeds):
                fjobs.append((finalists[i], finalists[j], s, 720))
                fjobs.append((finalists[j], finalists[i], s, 720))
    print(f"\nFINAL: {len(finalists)} finalistas, {len(fjobs)} episodios")
    with Pool(max(1, (os.cpu_count() or 2) - 1)) as pool:
        fresults = pool.map(run_episode, fjobs)

    pts = defaultdict(float)
    fmoney = defaultdict(list)
    for r in fresults:
        n0, n1 = spec_name(r["p0"]), spec_name(r["p1"])
        m0, m1 = r["money"]
        fmoney[n0].append(m0)
        fmoney[n1].append(m1)
        if m0 > m1:
            pts[n0] += 1
        elif m1 > m0:
            pts[n1] += 1
        else:
            pts[n0] += 0.5
            pts[n1] += 0.5

    total_per = 2 * final_seeds * (len(finalists) - 1)
    print(f"\n=== TABLA FINAL (episodios ganados de {total_per}) ===")
    order = sorted(fmoney, key=lambda n: -pts[n])
    for name in order:
        avg = sum(fmoney[name]) / len(fmoney[name])
        print(f"  {name:20s} {pts[name]:5.1f} | dinero medio ${avg:,.0f}")

    os.makedirs("results", exist_ok=True)
    with open("results/evolucion_gen1.json", "w") as f:
        json.dump({"candidatos": {spec_name(c): c[2] for c in candidates},
                   "criba": {n: sum(v) / len(v) for n, v in fitness.items()},
                   "final_pts": dict(pts)}, f, indent=1, default=str)
    print("\nguardado: results/evolucion_gen1.json")

    winner = order[0]
    if winner != "campeon":
        print(f"\n=== AUTOPSIA DEL NUEVO CAMPEÓN: {winner} ===")
        print_report(winner, autopsy(by_name.get(winner, CHAMP), "starter", n_seeds=2, seed0=6100))
    return order, by_name


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--poblacion", type=int, default=48)
    ap.add_argument("--screen-seeds", type=int, default=3)
    ap.add_argument("--final-seeds", type=int, default=4)
    args = ap.parse_args()
    main(poblacion=args.poblacion, screen_seeds=args.screen_seeds, final_seeds=args.final_seeds)
