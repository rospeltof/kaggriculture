"""Evolución 8: afinar la combinación de los mecanismos fase 2.

La ablación (2026-08-31) mostró: land_early +$3.5k, town_forecast +$3.5k solos;
fert/floor/idle_plant ~neutros solos; hpq4 -$7.1k solo; PERO el paquete completo
+$11.3k — interacciones fuertes. La búsqueda decide qué flags van juntos y con
qué perillas (piso %, peones/cuadrante, cultivos a fertilizar).

Uso: ./.venv/bin/python evolucion8.py --gens 10 --pop 36 --eps-seeds 3
"""
import argparse
import json
import os
import random
import time
from collections import defaultdict
from multiprocessing import Pool

from autopsia import autopsy, print_report
from bots.arquetipos import MIMADA_V5R, RUTERA
from evolucion2 import eval_candidates
from evolucion5 import load_registry
from evolucion5 import mutate as _mut5
from evolucion5 import sample as _smp5
from evolucion5 import signature as _sig5
from evolucion5 import to_cfg
from harness import run_episode, spec_name

SPARRING = os.path.abspath("bots/sparring_v16.py")
FASE2_DEFAULTS = {"sell_floor": 0, "idle_plant": False, "hands_per_quadrant": 0,
                  "land_early": False, "fert_crops": [], "town_forecast": False}
FASE2_CHOICES = {
    "sell_floor": [0, 0.3, 0.4, 0.5],
    "hands_per_quadrant": [0, 3, 4, 5],
    "fert_crops": [[], ["STRAWBERRY"], ["STRAWBERRY", "TOMATO"]],
}
TODO = dict(RUTERA, sell_floor=0.4, idle_plant=True, hands_per_quadrant=4,
            land_early=True, town_forecast=True, fert_crops=["STRAWBERRY", "TOMATO"])


def _force(cfg):
    cfg = dict(cfg)
    cfg["router"] = True
    cfg["hire_late"] = True
    cfg["zoning"] = False
    cfg["multi_feeder"] = False
    for k, v in FASE2_DEFAULTS.items():
        cfg.setdefault(k, v)
    cfg["fert_crops"] = sorted(cfg.get("fert_crops") or [])
    return cfg


def signature(cfg):
    return _sig5(_force(dict(cfg)))


def sample(rng):
    cfg = _force(_smp5(rng))
    cfg["sell_floor"] = rng.choice(FASE2_CHOICES["sell_floor"])
    cfg["idle_plant"] = rng.random() < 0.6
    cfg["hands_per_quadrant"] = rng.choice(FASE2_CHOICES["hands_per_quadrant"])
    cfg["land_early"] = rng.random() < 0.7
    cfg["town_forecast"] = rng.random() < 0.7
    cfg["fert_crops"] = sorted(rng.choice(FASE2_CHOICES["fert_crops"]))
    return cfg


def mutate(cfg, rng):
    c = _force(_mut5(cfg, rng))
    if rng.random() < 0.5:
        k = rng.choice(list(FASE2_DEFAULTS))
        if k in FASE2_CHOICES:
            c[k] = rng.choice(FASE2_CHOICES[k])
            if k == "fert_crops":
                c[k] = sorted(c[k])
        else:
            c[k] = not c.get(k, False)
    return c


def seeded_gen0():
    return [
        ("todo", dict(TODO)),
        ("todo_sin_hpq", dict(TODO, hands_per_quadrant=0)),
        ("heroes", dict(RUTERA, land_early=True, town_forecast=True)),
        ("heroes_fert", dict(RUTERA, land_early=True, town_forecast=True,
                             fert_crops=["STRAWBERRY", "TOMATO"], idle_plant=True)),
        ("todo_floor50", dict(TODO, sell_floor=0.5)),
        ("todo_hpq5", dict(TODO, hands_per_quadrant=5, hands_cap=13)),
    ]


def main(gens=10, pop=36, eps_seeds=3, steps=720, procs=None, out="results/evolucion8.json"):
    procs = procs or max(1, (os.cpu_count() or 2) - 1)
    rng = random.Random(20260831)
    registry = load_registry()
    for path in ("results/evolucion5.json", "results/evolucion6.json", "results/evolucion7.json"):
        if os.path.exists(path):
            with open(path) as f:
                for v in json.load(f).values():
                    cfg = dict(v["cfg"])
                    cfg["animals"] = [tuple(a) for a in cfg.get("animals", [])]
                    registry.add(signature(cfg))
    print(f"registro inicial: {len(registry)} firmas de gens 1-7", flush=True)

    all_time = {}
    panel = [SPARRING, ("cfg", "panel_todo", _force(dict(TODO)))]

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
        population.append(("cfg", f"s0_{len(population):02d}", cfg))

    t_start = time.time()
    total_eps = 0
    for g in range(gens):
        seed0 = 1_000_000 + 997 * g
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
              f"({wins[best]}/{2 * eps_seeds * len(panel)}, floor={bc.get('sell_floor')}, hpq={bc.get('hands_per_quadrant')}, "
              f"fert={bc.get('fert_crops')}, land={bc.get('land_early')}, fc={bc.get('town_forecast')}) | total {total_eps}", flush=True)
        with open(out, "w") as f:
            json.dump({n: {"fitness": v[0], "wins": v[1], "cfg": v[2]} for n, v in all_time.items()},
                      f, indent=1, default=str)
        if g == gens - 1:
            break
        elites = [by_name[n] for n in ranked[:5]]
        panel[1] = ("cfg", "panel_best", dict(elites[0][2]))
        nxt = [("cfg", f"s{g + 1}e_{i}", dict(e[2])) for i, e in enumerate(elites)]
        tries = 0
        while len(nxt) < pop - 8 and tries < 4000:
            tries += 1
            mu = mutate(rng.choice(elites)[2], rng)
            if signature(mu) in registry:
                continue
            registry.add(signature(mu))
            nxt.append(("cfg", f"s{g + 1}m_{len(nxt):02d}", _force(to_cfg(mu))))
        while len(nxt) < pop and tries < 8000:
            tries += 1
            cfg = sample(rng)
            if signature(cfg) in registry:
                continue
            registry.add(signature(cfg))
            nxt.append(("cfg", f"s{g + 1}i_{len(nxt):02d}", cfg))
        population = nxt

    seen = {signature(dict(TODO)), signature(dict(MIMADA_V5R))}
    finalists = [("cfg", "todo_ref", _force(to_cfg(dict(TODO)))), ("cfg", "v5r_ref", _force(to_cfg(dict(MIMADA_V5R))))]
    for n in sorted(all_time, key=lambda k: -all_time[k][0]):
        cfg = _force(to_cfg(all_time[n][2]))
        sig = signature(cfg)
        if sig in seen:
            continue
        seen.add(sig)
        finalists.append(("cfg", n, cfg))
        if len(finalists) >= 10:
            break
    fjobs = []
    for f1 in finalists:
        for s in range(1_010_000, 1_010_000 + 4):
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
        print(f"  {n:14s} gana {s['w']}/8 | propio ${sum(s['money']) / 8:,.0f} | cinta ${sum(s['tape']) / 8:,.0f} | "
              f"{json.dumps(fin_by[n][2], default=str)[:170]}", flush=True)
    winner = order[0]
    print(f"\n=== AUTOPSIA: {winner} ===", flush=True)
    print_report(winner, autopsy(fin_by[winner], "starter", n_seeds=2, seed0=1_020_000))
    print(f"\nTOTAL: {total_eps + len(fjobs)} episodios en {(time.time() - t_start) / 60:.0f} min", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--gens", type=int, default=10)
    ap.add_argument("--pop", type=int, default=36)
    ap.add_argument("--eps-seeds", type=int, default=3)
    ap.add_argument("--procs", type=int, default=None)
    args = ap.parse_args()
    main(gens=args.gens, pop=args.pop, eps_seeds=args.eps_seeds, procs=args.procs)
