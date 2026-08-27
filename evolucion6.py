"""Evolución 6: contra el rey del meta — la cinta de 2913 en el panel de fitness.

Panel: bots/sparring_v16.py (cinta reconstruida del bot top de Nikita Lugovoy,
~2913 en el ladder) + mimada_v4. Por primera vez el fitness mide "cuánto dinero
hago compartiendo mercado con el meta real", no con nuestros gemelos.

Reutiliza el espacio de búsqueda y los operadores de evolucion5.

Uso:
    ./.venv/bin/python evolucion6.py --gens 10 --pop 36 --eps-seeds 3
"""
import argparse
import json
import os
import random
import time
from collections import defaultdict
from multiprocessing import Pool

from autopsia import autopsy, print_report
from bots.arquetipos import LN_CLONE_V4, MIMADA_V4, MIMADA_XL
from evolucion2 import eval_candidates
from evolucion5 import load_registry, mutate, sample, signature, to_cfg
from harness import run_episode, spec_name

SPARRING = os.path.abspath("bots/sparring_v16.py")


def seeded_gen0():
    return [
        ("v4_base", dict(MIMADA_V4)),
        ("xl_base", dict(MIMADA_XL)),
        ("xl_fert75", dict(MIMADA_XL, fert_prio=75)),
        ("v4_8c4s", dict(MIMADA_V4, animals=[("COW", 8), ("SHEEP", 4)], multi_feeder=True,
                         max_quadrants=3, hands=10, crop_tiles=30, fert_prio=75)),
        ("xl_conveyor", dict(MIMADA_XL, adaptive=False,
                             plants={"CARROT": 1, "MELON": 5, "STRAWBERRY": 10, "WHEAT": 24},
                             crop_tiles=40, fert_prio=75, tiles_per_unit=6)),
        ("clon_ln", dict(LN_CLONE_V4)),
    ]


def main(gens=10, pop=36, eps_seeds=3, steps=720, procs=None, out="results/evolucion6.json"):
    procs = procs or max(1, (os.cpu_count() or 2) - 1)
    rng = random.Random(20260829)
    registry = load_registry()
    if os.path.exists("results/evolucion5.json"):
        with open("results/evolucion5.json") as f:
            for v in json.load(f).values():
                cfg = dict(v["cfg"])
                cfg["animals"] = [tuple(a) for a in cfg.get("animals", [])]
                registry.add(signature(cfg))
    print(f"registro inicial: {len(registry)} firmas de gens 1-5", flush=True)

    all_time = {}
    panel = [SPARRING, ("cfg", "panel_v4", dict(MIMADA_V4))]

    population = []
    for name, cfg in seeded_gen0():
        cfg = to_cfg(cfg)
        if signature(cfg) not in registry:
            registry.add(signature(cfg))
            population.append(("cfg", name, cfg))
    while len(population) < pop:
        cfg = sample(rng)
        if signature(cfg) in registry:
            continue
        registry.add(signature(cfg))
        population.append(("cfg", f"n0_{len(population):02d}", cfg))

    t_start = time.time()
    total_eps = 0
    for g in range(gens):
        seed0 = 600_000 + 997 * g
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
              f"({wins[best]}/{2 * eps_seeds * len(panel)}, adapt={bc.get('adaptive')}, "
              f"an={bc.get('animals')}) | total {total_eps}", flush=True)
        with open(out, "w") as f:
            json.dump({n: {"fitness": v[0], "wins": v[1], "cfg": v[2]} for n, v in all_time.items()},
                      f, indent=1, default=str)
        if g == gens - 1:
            break
        elites = [by_name[n] for n in ranked[:5]]
        # coevolución solo en el asiento 2: la cinta (asiento 1) es el ancla del meta
        panel[1] = ("cfg", "panel_best", dict(elites[0][2]))
        nxt = [("cfg", f"n{g + 1}e_{i}", dict(e[2])) for i, e in enumerate(elites)]
        tries = 0
        while len(nxt) < pop - 8 and tries < 4000:
            tries += 1
            mu = mutate(rng.choice(elites)[2], rng)
            if signature(mu) in registry:
                continue
            registry.add(signature(mu))
            nxt.append(("cfg", f"n{g + 1}m_{len(nxt):02d}", to_cfg(mu)))
        while len(nxt) < pop and tries < 8000:
            tries += 1
            cfg = sample(rng)
            if signature(cfg) in registry:
                continue
            registry.add(signature(cfg))
            nxt.append(("cfg", f"n{g + 1}i_{len(nxt):02d}", cfg))
        population = nxt

    # final: top 8 histórico + v4, todos contra TODOS incluida la cinta como rival fijo
    seen = {signature(to_cfg(dict(MIMADA_V4)))}
    finalists = [("cfg", "mimada_v4", to_cfg(dict(MIMADA_V4)))]
    for n in sorted(all_time, key=lambda k: -all_time[k][0]):
        cfg = to_cfg(all_time[n][2])
        sig = signature(cfg)
        if sig in seen:
            continue
        seen.add(sig)
        finalists.append(("cfg", n, cfg))
        if len(finalists) >= 9:
            break

    fjobs = []
    for i, f1 in enumerate(finalists):
        for s in range(610_000, 610_000 + 4):
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
    print("\n=== VS LA CINTA (8 eps c/u) ===", flush=True)
    fin_by = {spec_name(c): c for c in finalists}
    order = sorted(stats, key=lambda n: -sum(stats[n]["money"]) / len(stats[n]["money"]))
    for n in order:
        s = stats[n]
        print(f"  {n:12s} gana {s['w']}/8 | propio ${sum(s['money']) / 8:,.0f} | cinta ${sum(s['tape']) / 8:,.0f} | "
              f"{json.dumps(fin_by[n][2], default=str)[:180]}", flush=True)
    winner = order[0]
    print(f"\n=== AUTOPSIA: {winner} ===", flush=True)
    print_report(winner, autopsy(fin_by[winner], "starter", n_seeds=2, seed0=620_000))
    print(f"\nTOTAL: {total_eps + len(fjobs)} episodios en {(time.time() - t_start) / 60:.0f} min", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--gens", type=int, default=10)
    ap.add_argument("--pop", type=int, default=36)
    ap.add_argument("--eps-seeds", type=int, default=3)
    ap.add_argument("--procs", type=int, default=None)
    args = ap.parse_args()
    main(gens=args.gens, pop=args.pop, eps_seeds=args.eps_seeds, procs=args.procs)
