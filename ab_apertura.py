"""A/B de variantes de APERTURA contra un panel, por win-rate y dinero.

Uso: ./.venv/bin/python ab_apertura.py -n 12 --seed0 3000000
"""
import argparse
import copy
import math
import os
import sys
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import run_episode          # noqa: E402
from bots.arquetipos import CAMPEONA     # noqa: E402


def var(name, **kw):
    c = copy.deepcopy(CAMPEONA)
    c.update(kw)
    return ("cfg", name, c)


def run(variants, panel, n_seeds, seed0, steps=720, procs=None):
    jobs, meta = [], []
    for v in variants:
        for opp in panel:
            for s in range(seed0, seed0 + n_seeds):
                jobs.append((v, opp, s, steps)); meta.append((v[1], opp[1], 0))
                jobs.append((opp, v, s, steps)); meta.append((v[1], opp[1], 1))
    with Pool(procs or max(1, (os.cpu_count() or 2) - 1)) as pool:
        res = pool.map(run_episode, jobs)
    agg = {}
    for (vname, oname, side), r in zip(meta, res):
        mine, theirs = r["money"][side], r["money"][1 - side]
        a = agg.setdefault(vname, {"w": 0, "n": 0, "m": [], "byopp": {}})
        a["n"] += 1
        a["w"] += 1 if mine > theirs else (0.5 if mine == theirs else 0)
        a["m"].append(mine)
        b = a["byopp"].setdefault(oname, [0, 0])
        b[0] += 1 if mine > theirs else 0
        b[1] += 1
    return agg


def show(agg):
    print(f"\n{'variante':28s} {'win-rate':>10s} {'±':>6s} {'dinero':>10s}   por-oponente")
    for name, a in sorted(agg.items(), key=lambda kv: -kv[1]["w"] / kv[1]["n"]):
        wr = a["w"] / a["n"]
        se = math.sqrt(max(wr * (1 - wr), 1e-9) / a["n"])
        mm = sum(a["m"]) / len(a["m"])
        bo = " ".join(f"{o}:{v[0]}/{v[1]}" for o, v in sorted(a["byopp"].items()))
        print(f"{name:28s} {wr:9.1%} {se:6.1%} {mm:10,.0f}   {bo}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", "--seeds", type=int, default=12)
    ap.add_argument("--seed0", type=int, default=3000000)
    ap.add_argument("-j", "--procs", type=int, default=None)
    ap.add_argument("--which", default="all")
    args = ap.parse_args()

    VARIANTS = [
        var("base_CAMPEONA"),
        var("A_struct_jit", struct_jit=True),
        var("B_pickup_dedup", pickup_dedup=True),
        var("C_bulk_animals", bulk_animals=True),
        var("D_d0_premium", d0_premium=True),
        var("E_sheep_first", animals=[("SHEEP", 4), ("COW", 4)]),
        var("TODO", struct_jit=True, pickup_dedup=True, bulk_animals=True,
            d0_premium=True, animals=[("SHEEP", 4), ("COW", 4)]),
    ]
    if args.which != "all":
        keep = set(args.which.split(","))
        VARIANTS = [v for v in VARIANTS if v[1] in keep]
    PANEL = [("cfg", "gemela", copy.deepcopy(CAMPEONA)),
             "bots/sparring_barnyard.py", "bots/sparring_v16.py"]
    PANEL = [p if isinstance(p, tuple) else (p, os.path.basename(p).replace("sparring_", "").replace(".py", "")) for p in PANEL]
    PANEL = [p if p[0] == "cfg" else (p[0],) for p in PANEL]
    # panel con nombre legible
    PANEL = [("cfg", "gemela", copy.deepcopy(CAMPEONA)),
             ("bots/sparring_barnyard.py", "barnyard"),
             ("bots/sparring_v16.py", "cinta")]
    class Named(str):
        pass
    panel = []
    for p in PANEL:
        if p[0] == "cfg":
            panel.append(p)
        else:
            s = Named(os.path.abspath(p[0]))
            panel.append(s)
    # run_episode necesita specs; usamos tuplas ("cfg",..) o rutas str
    def pname(p):
        return p[1] if isinstance(p, tuple) else os.path.basename(p).replace("sparring_", "").replace(".py", "")
    jobs_panel = [p if isinstance(p, tuple) else p for p in panel]
    # parche: envolvemos para que `run` pueda nombrar
    class P:
        def __init__(self, spec, name):
            self.spec, self.name = spec, name
    wrapped = [(p if isinstance(p, tuple) else (p, pname(p))) for p in panel]

    # simplificamos: usamos lista de (spec, nombre)
    def run2(variants, panel_pairs, n_seeds, seed0, steps=720, procs=None):
        jobs, meta = [], []
        for v in variants:
            for spec, oname in panel_pairs:
                for s in range(seed0, seed0 + n_seeds):
                    jobs.append((v, spec, s, steps)); meta.append((v[1], oname, 0))
                    jobs.append((spec, v, s, steps)); meta.append((v[1], oname, 1))
        with Pool(procs or max(1, (os.cpu_count() or 2) - 1)) as pool:
            res = pool.map(run_episode, jobs)
        agg = {}
        for (vname, oname, side), r in zip(meta, res):
            mine, theirs = r["money"][side], r["money"][1 - side]
            a = agg.setdefault(vname, {"w": 0, "n": 0, "m": [], "byopp": {}})
            a["n"] += 1
            a["w"] += 1 if mine > theirs else (0.5 if mine == theirs else 0)
            a["m"].append(mine)
            b = a["byopp"].setdefault(oname, [0, 0])
            b[0] += 1 if mine > theirs else 0
            b[1] += 1
        return agg

    pairs = [(("cfg", "gemela", copy.deepcopy(CAMPEONA)), "gemela"),
             (os.path.abspath("bots/sparring_barnyard.py"), "barnyard"),
             (os.path.abspath("bots/sparring_v16.py"), "cinta")]
    agg = run2(VARIANTS, pairs, args.seeds, args.seed0, procs=args.procs)
    show(agg)
