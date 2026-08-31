"""Evolución 9: re-dimensionar sobre INTEGRAL_LECTOR, seleccionando por WIN-RATE.

Cambio metodológico (2026-09-02): las ocho evoluciones previas usaron el dinero
medio como fitness. La prueba decisiva de hoy mostró que los mecanismos ganadores
(opp_read + sell_rank + order_budget) son NEUTROS en dinero y duplican el
win-rate (15.0% -> 33.3%, 3.4 sigma) — el proxy viejo los habría descartado.
Aquí el fitness es win-rate primario con dinero como desempate, que es
exactamente lo que premia el Elo de Kaggle.

Mecanismos validados forzados en todos los candidatos: router, hire_late,
opp_read, sell_rank, order_budget. Se buscan: granja (animales/cultivos/peones/
cuadrantes/crop_tiles), perillas fase 2 (sell_floor, hands_per_quadrant,
fert_crops) y los gateados sin veredicto (beat_wave + wave_min_value,
melon_max, smart_overflow, scorer_v2).

Uso: ./.venv/bin/python evolucion9.py --gens 8 --pop 30 --eps-seeds 3
"""
import argparse
import json
import os
import random
import time
from collections import defaultdict
from multiprocessing import Pool

from autopsia import autopsy, print_report
from bots.arquetipos import INTEGRAL, INTEGRAL_LECTOR, LN_CLONE_V4
from evolucion5 import load_registry
from evolucion5 import mutate as _mut5
from evolucion5 import sample as _smp5
from evolucion5 import signature as _sig5
from evolucion5 import to_cfg
from harness import run_episode, spec_name

BARNYARD = os.path.abspath("bots/sparring_barnyard.py")
CINTA = os.path.abspath("bots/sparring_v16.py")

FORCED = {"router": True, "hire_late": True, "opp_read": True,
          "sell_rank": True, "order_budget": True, "zoning": False,
          "multi_feeder": False, "phased": False}
NEW_CHOICES = {
    "sell_floor": [0, 0.3, 0.4, 0.5],
    "hands_per_quadrant": [0, 3, 4, 5],
    "fert_crops": [[], ["STRAWBERRY"], ["STRAWBERRY", "TOMATO"]],
    "crop_tiles": [22, 30, 40],
    "beat_wave": [False, True],
    "wave_min_value": [1000, 2000, 4000],
    "melon_max": [0, 8, 12],
    "smart_overflow": [False, True],
    "scorer_v2": [False, True],
}
DEFAULTS = {"sell_floor": 0.4, "hands_per_quadrant": 4, "fert_crops": ["STRAWBERRY", "TOMATO"],
            "crop_tiles": 30, "beat_wave": False, "wave_min_value": 2000, "melon_max": 0,
            "smart_overflow": False, "scorer_v2": False}


def _force(cfg):
    c = dict(cfg)
    c.update(FORCED)
    for k, v in DEFAULTS.items():
        c.setdefault(k, v)
    c["fert_crops"] = sorted(c.get("fert_crops") or [])
    return c


def signature(cfg):
    return _sig5(_force(dict(cfg)))


def sample(rng):
    c = _force(_smp5(rng))
    for k, choices in NEW_CHOICES.items():
        c[k] = rng.choice(choices)
    c["fert_crops"] = sorted(c["fert_crops"])
    return c


def mutate(cfg, rng):
    c = _force(_mut5(cfg, rng))
    if rng.random() < 0.55:
        k = rng.choice(list(NEW_CHOICES))
        c[k] = rng.choice(NEW_CHOICES[k])
        if k == "fert_crops":
            c[k] = sorted(c[k])
    return c


def evaluate(cands, panel, seed0, eps_seeds, steps, procs):
    """Devuelve (win_rate, dinero_medio, fitness) por candidato.
    fitness = win_rate*1e6 + dinero  -> victorias primero, dinero desempata."""
    jobs, meta = [], []
    for c in cands:
        for opp in panel:
            for s in range(seed0, seed0 + eps_seeds):
                jobs.append((c, opp, s, steps)); meta.append((spec_name(c), 0))
                jobs.append((opp, c, s, steps)); meta.append((spec_name(c), 1))
    with Pool(procs) as pool:
        res = pool.map(run_episode, jobs)
    agg = defaultdict(lambda: {"w": 0.0, "n": 0, "money": 0.0})
    for r, (name, side) in zip(res, meta):
        my, their = r["money"][side], r["money"][1 - side]
        a = agg[name]
        a["n"] += 1
        # el EMPATE vale 0.5, no 0: el motor es determinista y un cambio inocuo
        # produce empates exactos que antes se contaban como derrotas (ver
        # medicion.py y BITACORA 2026-09-05)
        a["w"] += 1.0 if my > their else (0.5 if my == their else 0.0)
        a["money"] += my
    out = {}
    for name, a in agg.items():
        wr = a["w"] / max(1, a["n"])
        mm = a["money"] / max(1, a["n"])
        out[name] = (wr, mm, wr * 1e6 + mm)
    return out, len(jobs)


def seeded_gen0():
    return [
        ("lector", dict(INTEGRAL_LECTOR)),
        ("lector_wave", dict(INTEGRAL_LECTOR, beat_wave=True)),
        ("lector_t40", dict(INTEGRAL_LECTOR, crop_tiles=40, hands=9, max_quadrants=3)),
        ("lector_melon8", dict(INTEGRAL_LECTOR, melon_max=8, smart_overflow=True)),
        ("lector_v2", dict(INTEGRAL_LECTOR, scorer_v2=True)),
        ("lector_xl", dict(INTEGRAL_LECTOR, animals=[("COW", 6), ("SHEEP", 6)],
                           crop_tiles=40, hands=10, max_quadrants=3)),
    ]


def main(gens=8, pop=30, eps_seeds=3, steps=720, procs=None, out="results/evolucion9.json"):
    procs = procs or max(1, (os.cpu_count() or 2) - 1)
    rng = random.Random(20260902)
    registry = load_registry()
    for path in ("results/evolucion5.json", "results/evolucion6.json",
                 "results/evolucion7.json", "results/evolucion8.json"):
        if os.path.exists(path):
            with open(path) as f:
                for v in json.load(f).values():
                    cfg = dict(v["cfg"])
                    cfg["animals"] = [tuple(a) for a in cfg.get("animals", [])]
                    registry.add(signature(cfg))
    print(f"registro inicial: {len(registry)} firmas de gens 1-8", flush=True)

    all_time = {}
    panel = [("cfg", "p_lector", _force(dict(INTEGRAL_LECTOR))), BARNYARD, CINTA]

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
        population.append(("cfg", f"t0_{len(population):02d}", cfg))

    t0all = time.time()
    total_eps = 0
    for g in range(gens):
        seed0 = 3_000_000 + 997 * g
        t0 = time.time()
        res, n_eps = evaluate(population, panel, seed0, eps_seeds, steps, procs)
        total_eps += n_eps
        by_name = {spec_name(c): c for c in population}
        ranked = sorted(res, key=lambda n: -res[n][2])
        for n in ranked:
            all_time[n] = (res[n][0], res[n][1], res[n][2], by_name[n][2])
        best = ranked[0]
        wr, mm, _ = res[best]
        bc = by_name[best][2]
        print(f"gen {g:02d} | {n_eps} eps en {time.time() - t0:.0f}s | mejor: {best} "
              f"WR {wr:.1%} ${mm:,.0f} | an={bc.get('animals')} tiles={bc.get('crop_tiles')} "
              f"wave={bc.get('beat_wave')} melon={bc.get('melon_max')} | total {total_eps}", flush=True)
        with open(out, "w") as f:
            json.dump({n: {"win_rate": v[0], "money": v[1], "cfg": v[3]} for n, v in all_time.items()},
                      f, indent=1, default=str)
        if g == gens - 1:
            break
        elites = [by_name[n] for n in ranked[:5]]
        panel[0] = ("cfg", "p_best", dict(elites[0][2]))   # coevolución
        nxt = [("cfg", f"t{g + 1}e_{i}", dict(e[2])) for i, e in enumerate(elites)]
        tries = 0
        while len(nxt) < pop - 6 and tries < 4000:
            tries += 1
            mu = mutate(rng.choice(elites)[2], rng)
            if signature(mu) in registry:
                continue
            registry.add(signature(mu))
            nxt.append(("cfg", f"t{g + 1}m_{len(nxt):02d}", _force(to_cfg(mu))))
        while len(nxt) < pop and tries < 8000:
            tries += 1
            cfg = sample(rng)
            if signature(cfg) in registry:
                continue
            registry.add(signature(cfg))
            nxt.append(("cfg", f"t{g + 1}i_{len(nxt):02d}", cfg))
        population = nxt

    # ---- final: top 6 histórico + lector, TODOS contra el mismo panel fijo ----
    seen = {signature(dict(INTEGRAL_LECTOR))}
    finalists = [("cfg", "lector_ref", _force(to_cfg(dict(INTEGRAL_LECTOR))))]
    for n in sorted(all_time, key=lambda k: -all_time[k][2]):
        cfg = _force(to_cfg(all_time[n][3]))
        sig = signature(cfg)
        if sig in seen:
            continue
        seen.add(sig)
        finalists.append(("cfg", n, cfg))
        if len(finalists) >= 7:
            break
    fpanel = [("cfg", "f_lector", _force(dict(INTEGRAL_LECTOR))), BARNYARD, CINTA,
              ("cfg", "f_clon", dict(LN_CLONE_V4)), ("cfg", "f_integral", dict(INTEGRAL))]
    print(f"\nFINAL: {len(finalists)} finalistas x panel de 5 x 6 seeds", flush=True)
    fres, fn = evaluate(finalists, fpanel, 3_100_000, 6, steps, procs)
    print(f"({fn} episodios)", flush=True)
    fin_by = {spec_name(c): c for c in finalists}
    order = sorted(fres, key=lambda n: -fres[n][2])
    for n in order:
        wr, mm, _ = fres[n]
        print(f"  {n:14s} WR {wr:5.1%} | ${mm:,.0f} | {json.dumps(fin_by[n][2], default=str)[:150]}", flush=True)

    winner = order[0]
    if winner != "lector_ref":
        print(f"\nCONFIRMACIÓN head-to-head en seeds vírgenes: {winner} vs INTEGRAL_LECTOR", flush=True)
        cjobs = []
        ref = ("cfg", "ref", _force(dict(INTEGRAL_LECTOR)))
        for s in range(3_200_000, 3_200_000 + 25):
            cjobs.append((fin_by[winner], ref, s, steps))
            cjobs.append((ref, fin_by[winner], s, steps))
        with Pool(procs) as pool:
            cres = pool.map(run_episode, cjobs)
        w = l = 0
        wm, rm = [], []
        for i, r in enumerate(cres):
            side = i % 2
            my, their = r["money"][side], r["money"][1 - side]
            wm.append(my); rm.append(their)
            w += my > their; l += their > my
        print(f"  {winner}: gana {w}, pierde {l} de {len(cres)} | ${sum(wm)/len(wm):,.0f} vs ${sum(rm)/len(rm):,.0f}", flush=True)
        print(f"\n=== AUTOPSIA: {winner} ===", flush=True)
        print_report(winner, autopsy(fin_by[winner], "starter", n_seeds=2, seed0=3_300_000))
        with open("results/evolucion9_winner.json", "w") as f:
            json.dump({"name": winner, "cfg": fin_by[winner][2], "wins": w, "losses": l,
                       "money": sum(wm)/len(wm), "ref_money": sum(rm)/len(rm)}, f, indent=1, default=str)
    else:
        print("\nINTEGRAL_LECTOR retiene el título.", flush=True)
    print(f"\nTOTAL: {total_eps + fn} episodios en {(time.time() - t0all)/60:.0f} min", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--gens", type=int, default=8)
    ap.add_argument("--pop", type=int, default=30)
    ap.add_argument("--eps-seeds", type=int, default=3)
    ap.add_argument("--procs", type=int, default=None)
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    if args.smoke:
        main(gens=2, pop=6, eps_seeds=1, steps=240)
    else:
        main(gens=args.gens, pop=args.pop, eps_seeds=args.eps_seeds, procs=args.procs)
