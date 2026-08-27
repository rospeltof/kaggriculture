"""Evolución 7: redimensionar la granja para el motor con router (opción B, fase 1).

El router liberó ~35% de capacidad (movimiento −36%) que la granja actual no
usa. Todos los candidatos corren con router=True + hire_late; la búsqueda decide
cuánta granja cabe ahora. Panel: la cinta de 2913 + mimada_v5r.

Uso: ./.venv/bin/python evolucion7.py --gens 10 --pop 36 --eps-seeds 3
"""
import argparse
import json
import os
import random
import time
from collections import defaultdict
from multiprocessing import Pool

from autopsia import autopsy, print_report
from bots.arquetipos import MIMADA_V4, MIMADA_V5R, MIMADA_V5RXL
from evolucion2 import eval_candidates
from evolucion5 import load_registry
from evolucion5 import mutate as _mut5
from evolucion5 import sample as _smp5
from evolucion5 import signature, to_cfg
from harness import run_episode, spec_name

SPARRING = os.path.abspath("bots/sparring_v16.py")


def _force(cfg):
    cfg = dict(cfg)
    cfg["router"] = True
    cfg["hire_late"] = True
    cfg["zoning"] = False
    cfg["multi_feeder"] = False
    return cfg


def sample(rng):
    return _force(_smp5(rng))


def mutate(cfg, rng):
    return _force(_mut5(cfg, rng))


def seeded_gen0():
    return [
        ("v5r", dict(MIMADA_V5R)),
        ("v5rxl", dict(MIMADA_V5RXL)),
        ("v5r_8c4s", _force(dict(MIMADA_V4, animals=[("COW", 8), ("SHEEP", 4)], hands=10,
                                 max_quadrants=3, crop_tiles=30, fert_prio=75))),
        ("v5r_t30", _force(dict(MIMADA_V4, crop_tiles=30, hands=9, max_quadrants=3))),
        ("v5r_straw", _force(dict(MIMADA_V4, adaptive=False, hands=10, max_quadrants=3,
                                  plants={"CARROT": 1, "MELON": 6, "STRAWBERRY": 14, "WHEAT": 12},
                                  fert_prio=75))),
    ]


def main(gens=10, pop=36, eps_seeds=3, steps=720, procs=None, out="results/evolucion7.json"):
    procs = procs or max(1, (os.cpu_count() or 2) - 1)
    rng = random.Random(20260830)
    registry = load_registry()
    for path in ("results/evolucion5.json", "results/evolucion6.json"):
        if os.path.exists(path):
            with open(path) as f:
                for v in json.load(f).values():
                    cfg = dict(v["cfg"])
                    cfg["animals"] = [tuple(a) for a in cfg.get("animals", [])]
                    registry.add(signature(cfg))
    print(f"registro inicial: {len(registry)} firmas de gens 1-6", flush=True)

    all_time = {}
    panel = [SPARRING, ("cfg", "panel_v5r", _force(dict(MIMADA_V5R)))]

    population = []
    for name, cfg in seeded_gen0():
        cfg = _force(to_cfg(cfg))
        if signature(cfg) not in registry:
            registry.add(signature(cfg))
            population.append(("cfg", name, cfg))
    while len(population) < pop:
        cfg = sample(rng)
        if signature(cfg) in registry:
            continue
        registry.add(signature(cfg))
        population.append(("cfg", f"r0_{len(population):02d}", cfg))

    t_start = time.time()
    total_eps = 0
    for g in range(gens):
        seed0 = 800_000 + 997 * g
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
              f"({wins[best]}/{2 * eps_seeds * len(panel)}, an={bc.get('animals')}, "
              f"tiles={bc.get('crop_tiles')}, adapt={bc.get('adaptive')}) | total {total_eps}", flush=True)
        with open(out, "w") as f:
            json.dump({n: {"fitness": v[0], "wins": v[1], "cfg": v[2]} for n, v in all_time.items()},
                      f, indent=1, default=str)
        if g == gens - 1:
            break
        elites = [by_name[n] for n in ranked[:5]]
        panel[1] = ("cfg", "panel_best", dict(elites[0][2]))
        nxt = [("cfg", f"r{g + 1}e_{i}", dict(e[2])) for i, e in enumerate(elites)]
        tries = 0
        while len(nxt) < pop - 8 and tries < 4000:
            tries += 1
            mu = mutate(rng.choice(elites)[2], rng)
            if signature(mu) in registry:
                continue
            registry.add(signature(mu))
            nxt.append(("cfg", f"r{g + 1}m_{len(nxt):02d}", _force(to_cfg(mu))))
        while len(nxt) < pop and tries < 8000:
            tries += 1
            cfg = sample(rng)
            if signature(cfg) in registry:
                continue
            registry.add(signature(cfg))
            nxt.append(("cfg", f"r{g + 1}i_{len(nxt):02d}", cfg))
        population = nxt

    seen = {signature(_force(to_cfg(dict(MIMADA_V5R))))}
    finalists = [("cfg", "mimada_v5r", _force(to_cfg(dict(MIMADA_V5R))))]
    for n in sorted(all_time, key=lambda k: -all_time[k][0]):
        cfg = _force(to_cfg(all_time[n][2]))
        sig = signature(cfg)
        if sig in seen:
            continue
        seen.add(sig)
        finalists.append(("cfg", n, cfg))
        if len(finalists) >= 9:
            break
    fjobs = []
    for f1 in finalists:
        for s in range(810_000, 810_000 + 4):
            fjobs.append((f1, SPARRING, s, steps))
            fjobs.append((SPARRING, f1, s, steps))
    print(f"\nFINAL: {len(finalists)} finalistas x 8 eps vs LA CINTA", flush=True)
    with Pool(procs) as pool:
        fresults = pool.map(run_episode, fjobs)
    stats = defaultdict(lambda: {"w": 0, "money": [], "tape": []})
    for r in fresults:
        for side in (0, 1):
            name = spec_name(r["p0"] if side == 0 else r["p1"])
            if name == SPARRING:
                continue
            my, their = r["money"][side], r["money"][1 - side]
            stats[name]["money"].append(my)
            stats[name]["tape"].append(their)
            stats[name]["w"] += my > their
    fin_by = {spec_name(c): c for c in finalists}
    order = sorted(stats, key=lambda n: -sum(stats[n]["money"]) / len(stats[n]["money"]))
    print("\n=== VS LA CINTA (8 eps c/u) ===", flush=True)
    for n in order:
        s = stats[n]
        print(f"  {n:12s} gana {s['w']}/8 | propio ${sum(s['money']) / 8:,.0f} | cinta ${sum(s['tape']) / 8:,.0f} | "
              f"{json.dumps(fin_by[n][2], default=str)[:170]}", flush=True)
    winner = order[0]
    print(f"\n=== AUTOPSIA: {winner} ===", flush=True)
    print_report(winner, autopsy(fin_by[winner], "starter", n_seeds=2, seed0=820_000))
    print(f"\nTOTAL: {total_eps + len(fjobs)} episodios en {(time.time() - t_start) / 60:.0f} min", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--gens", type=int, default=10)
    ap.add_argument("--pop", type=int, default=36)
    ap.add_argument("--eps-seeds", type=int, default=3)
    ap.add_argument("--procs", type=int, default=None)
    args = ap.parse_args()
    main(gens=args.gens, pop=args.pop, eps_seeds=args.eps_seeds, procs=args.procs)
