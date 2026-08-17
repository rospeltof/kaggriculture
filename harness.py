"""Harness de evaluación de agentes Kaggriculture.

Corre N episodios entre dos agentes, en paralelo, con seeds fijos, y reporta
estadística suficiente para decidir si A es mejor que B:

  - win/loss/tie y score (empate = 0.5) con intervalo de confianza Wilson 95%
  - dinero final medio de cada lado
  - estados de error/timeout de los agentes (un bot que crashea se detecta aquí)
  - guarda un .jsonl por corrida en results/ con la curva de dinero por día
    de cada episodio, para análisis posterior

Con espejo (default) cada seed se juega dos veces con los lados invertidos,
para cancelar la asimetría de player 0 (HIRE/BUY_LAND atómicos resuelven
primero para el jugador 0 — RULES.md S5.4).

Agentes: nombre builtin ("starter", "random", "pass") o ruta a un .py con
función `agent` — el mismo formato de una submission real.

Uso:
    ./.venv/bin/python harness.py starter random -n 10
    ./.venv/bin/python harness.py bots/mi_bot.py starter -n 25 --seed0 2000
"""
import argparse
import json
import math
import os
import time
from multiprocessing import Pool

BUILTINS = {"starter", "random", "pass"}


def resolve_agent(spec):
    if spec in BUILTINS or ":" in spec:
        return spec
    path = os.path.abspath(spec)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Agente no encontrado: {spec}")
    return path


def materialize(spec):
    """Convierte un spec en algo que env.run acepte. 'mod.sub:func' se importa
    aquí (dentro del worker) porque las closures no se picklean entre procesos."""
    if isinstance(spec, str) and ":" in spec and not os.path.exists(spec):
        import importlib

        mod, fn = spec.split(":", 1)
        return getattr(importlib.import_module(mod), fn)
    return spec


def run_episode(job):
    """Corre un episodio en un worker. job = (agente_p0, agente_p1, seed, steps)."""
    a0, a1, seed, steps = job
    from kaggle_environments import make

    t0 = time.time()
    env = make("kaggriculture", configuration={"episodeSteps": steps, "seed": seed})
    env.run([materialize(a0), materialize(a1)])
    elapsed = time.time() - t0

    final = env.steps[-1]
    obs0 = env.steps[-1][0].observation
    money = [obs0["farms"][i]["money"] for i in range(2)]
    curves = [
        [env.steps[t][0].observation["farms"][i]["money"] for t in range(0, len(env.steps), 24)]
        for i in range(2)
    ]
    return {
        "p0": a0,
        "p1": a1,
        "seed": seed,
        "money": money,
        "statuses": [s.status for s in final],
        "curves": curves,
        "seconds": round(elapsed, 2),
    }


def wilson95(wins, n, z=1.96):
    if n == 0:
        return (0.0, 1.0)
    p = wins / n
    denom = 1 + z * z / n
    center = p + z * z / (2 * n)
    radius = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((center - radius) / denom, (center + radius) / denom)


def evaluate(spec_a, spec_b, n_seeds=10, seed0=1000, steps=720, mirror=True, procs=None, out_dir="results"):
    a, b = resolve_agent(spec_a), resolve_agent(spec_b)
    seeds = list(range(seed0, seed0 + n_seeds))
    jobs = [(a, b, s, steps) for s in seeds]
    if mirror:
        jobs += [(b, a, s, steps) for s in seeds]

    t0 = time.time()
    with Pool(procs or max(1, (os.cpu_count() or 2) - 1)) as pool:
        results = pool.map(run_episode, jobs)
    total_time = time.time() - t0

    wins = losses = ties = 0
    money_a, money_b = [], []
    bad = []
    for r in results:
        side_a = 0 if r["p0"] == a else 1
        ma, mb = r["money"][side_a], r["money"][1 - side_a]
        money_a.append(ma)
        money_b.append(mb)
        if ma > mb:
            wins += 1
        elif mb > ma:
            losses += 1
        else:
            ties += 1
        for i, st in enumerate(r["statuses"]):
            if st != "DONE":
                bad.append((r["seed"], r["p0"] if i == 0 else r["p1"], st))

    n = len(results)
    score = (wins + 0.5 * ties) / n
    lo, hi = wilson95(wins + 0.5 * ties, n)

    def mean_sd(xs):
        m = sum(xs) / len(xs)
        sd = math.sqrt(sum((x - m) ** 2 for x in xs) / len(xs))
        return m, sd

    ma, sa = mean_sd(money_a)
    mb, sb = mean_sd(money_b)

    os.makedirs(out_dir, exist_ok=True)
    tag = f"{os.path.basename(spec_a)}_vs_{os.path.basename(spec_b)}_{int(time.time())}"
    out_path = os.path.join(out_dir, f"{tag}.jsonl")
    with open(out_path, "w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")

    print(f"A = {spec_a}   B = {spec_b}")
    print(f"episodios: {n} ({n_seeds} seeds {seed0}-{seed0 + n_seeds - 1}{', espejo' if mirror else ''}), {steps} steps")
    print(f"A: gana {wins}, pierde {losses}, empata {ties}  ->  score {score:.1%}  IC95 [{lo:.0%}, {hi:.0%}]")
    print(f"dinero final medio: A ${ma:,.0f} (sd {sa:,.0f}) | B ${mb:,.0f} (sd {sb:,.0f})")
    print(f"tiempo: {total_time:.0f}s total, {sum(r['seconds'] for r in results) / n:.1f}s/episodio")
    if bad:
        print(f"AGENTES NO-DONE: {bad}")
    else:
        print("errores de agente: ninguno")
    print(f"resultados: {out_path}")
    return {"score": score, "ci": (lo, hi), "wins": wins, "losses": losses, "ties": ties,
            "money_a": ma, "money_b": mb, "out_path": out_path}


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Evalúa agente A vs agente B con estadística.")
    ap.add_argument("agent_a")
    ap.add_argument("agent_b")
    ap.add_argument("-n", "--seeds", type=int, default=10, help="número de seeds (episodios = 2n con espejo)")
    ap.add_argument("--seed0", type=int, default=1000)
    ap.add_argument("--steps", type=int, default=720)
    ap.add_argument("--no-mirror", action="store_true")
    ap.add_argument("-j", "--procs", type=int, default=None)
    args = ap.parse_args()
    evaluate(args.agent_a, args.agent_b, n_seeds=args.seeds, seed0=args.seed0,
             steps=args.steps, mirror=not args.no_mirror, procs=args.procs)
