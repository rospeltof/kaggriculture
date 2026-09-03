"""Búsqueda offline del plan de apertura (días 0-4). FRENTE CERRADO 2026-09-02.

NO RELANZAR sin leer docs/BITACORA.md 2026-09-02. Dos motivos:
  1. La palanca es de un solo sentido: 6 aperturas aleatorias razonables sacan
     0-6% contra el 50% de nuestro scorer. La superficie es una meseta estrecha
     rodeada de acantilados, y el hill-climbing rechaza ~99% de las mutaciones.
  2. Este buscador tiene un WINNER'S CURSE: guarda la puntuación del titular como
     estimación única sin re-evaluarla, así que el primer golpe de suerte congela
     la referencia. Si se reusa, hay que re-evaluar al titular cada iteración.
El mecanismo `opening_plan` del chasis SÍ sirve y queda (plan_until=4 da +$2,866).


Por qué esto y no otra cosa: el 83% de las acciones de unidad del top-1 no miran
al rival — el campo es casi un problema de UN jugador y admite optimización
offline; solo el mercado interactúa. Y el horizonte correcto es corto: barrido
medido, plan_until 0 reproduce la base al dólar, 2 da +$1,855, 4 da +$2,866 y
12 da −$5,223 (congelar de más destruye adaptación que sí vale).

Método: hill-climbing con NÚMEROS ALEATORIOS COMUNES — cada candidato se evalúa
en los MISMOS pares (cinta, seed) que el titular y se compara pareado, que es lo
que baja la sd de ~50 puntos a unos pocos (ver docs/METODO.md §3).

Objetivo: win-rate contra el panel de 5 cintas reales, no dinero (§1).

Uso: ./.venv/bin/python buscar_apertura.py --iters 200 --seeds 12
"""
import argparse
import copy
import json
import math
import os
import random
import statistics as st
import sys
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

TAPES = ["axel_ahmer", "takahirohon", "artfix", "masih_pemula_beneran", "zihao_zeng"]
SEMILLAS = ["WHEAT", "MELON", "STRAWBERRY", "CARROT", "TOMATO"]
ANIMALES = ["COW", "SHEEP", "GOOSE"]
DIAS = [0, 1, 2, 3, 4]


def _una(args):
    plan, seed, tape, seat = args
    from kaggle_environments import make
    from bots.chassis import make_agent
    from bots.arquetipos import CAMPEONA_RUTA
    from harness import materialize
    cfg = dict(CAMPEONA_RUTA, opening_plan=plan, plan_until=4)
    yo = make_agent(cfg)
    riv = materialize(f"bots.meta.tape:{tape}")
    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=False)
    env.run([yo, riv] if seat == 0 else [riv, yo])
    f = env.steps[-1]
    mio = f[seat].reward or 0
    suyo = f[1 - seat].reward or 0
    return 1.0 if mio > suyo else (0.5 if mio == suyo else 0.0)


def evaluar(plan, seeds, pool):
    trabajos = [(plan, s, t, seat) for t in TAPES for s in seeds for seat in (0, 1)]
    res = pool.map(_una, trabajos)
    # agrupar por par (cinta, seed) -> media del espejo
    pares = {}
    for (_, s, t, _seat), r in zip(trabajos, res):
        pares.setdefault((t, s), []).append(r)
    return [sum(v) / len(v) for v in pares.values()]


def mutar(plan, rng):
    p = copy.deepcopy(plan)
    d = rng.choice(DIAS)
    e = p.setdefault(d, {"seeds": {}, "animals": {}, "land": 0})
    q = rng.random()
    if q < 0.45:                                    # mover cantidad de semilla
        c = rng.choice(SEMILLAS)
        e["seeds"][c] = max(0, e["seeds"].get(c, 0) + rng.choice([-4, -2, -1, 1, 2, 4]))
        if e["seeds"][c] == 0:
            e["seeds"].pop(c)
    elif q < 0.80:                                  # mover un animal
        a = rng.choice(ANIMALES)
        e["animals"][a] = max(0, e["animals"].get(a, 0) + rng.choice([-1, 1]))
        if e["animals"][a] == 0:
            e["animals"].pop(a)
    else:                                           # trasladar una compra de dia
        d2 = rng.choice([x for x in DIAS if x != d])
        e2 = p.setdefault(d2, {"seeds": {}, "animals": {}, "land": 0})
        if e["seeds"]:
            c = rng.choice(list(e["seeds"]))
            n = min(e["seeds"][c], rng.choice([1, 2, 4]))
            e["seeds"][c] -= n
            if e["seeds"][c] == 0:
                e["seeds"].pop(c)
            e2["seeds"][c] = e2["seeds"].get(c, 0) + n
    return p


def main(iters, n_seeds, semilla, salida):
    rng = random.Random(semilla)
    base = {int(k): v for k, v in json.load(open("results/plan_base.json")).items()}
    base = {d: base.get(d, {"seeds": {}, "animals": {}, "land": 0}) for d in DIAS}
    seeds = list(range(71000, 71000 + n_seeds))
    log = open(salida, "a")
    with Pool(max(1, (os.cpu_count() or 2) - 1)) as pool:
        mejor = base
        s_mejor = evaluar(mejor, seeds, pool)
        print(f"titular: {100*st.mean(s_mejor):.1f}%  ({len(s_mejor)} pares)", flush=True)
        aceptadas = 0
        for it in range(iters):
            cand = mutar(mejor, rng)
            s_cand = evaluar(cand, seeds, pool)
            d = [a - b for a, b in zip(s_cand, s_mejor)]
            m = st.mean(d)
            sd = st.stdev(d) if len(d) > 1 else 0.0
            t = m / (sd / math.sqrt(len(d))) if sd else (0.0 if m == 0 else 9.9)
            ok = t > 1.0                       # umbral laxo para explorar; se valida al final
            linea = (f"it{it:03d} cand {100*st.mean(s_cand):.1f}% vs {100*st.mean(s_mejor):.1f}% "
                     f"delta {100*m:+.1f} t{t:+.2f} {'ACEPTA' if ok else ''}")
            print(linea, flush=True)
            log.write(linea + "\n")
            log.flush()
            if ok:
                mejor, s_mejor = cand, s_cand
                aceptadas += 1
                json.dump({str(k): v for k, v in mejor.items()},
                          open("results/plan_mejor.json", "w"), indent=1)
        print(f"\naceptadas {aceptadas}/{iters}. Plan en results/plan_mejor.json", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--iters", type=int, default=200)
    ap.add_argument("--n_seeds", "--seeds", type=int, default=12, dest="n_seeds")
    ap.add_argument("--semilla", type=int, default=1)
    ap.add_argument("--salida", default="results/busqueda_apertura.log")
    main(**vars(ap.parse_args()))
