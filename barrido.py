"""Barrido de las prioridades VIVAS contra el panel de 40 rivales reales.

Por que ahora: `muerde.py` (2026-09-03) confirmo que de las perillas de
prioridad solo muerden prio_water, prio_feed, prio_care, prio_harvest,
prio_plant y fert_prio; prio_dig, prio_urgency, prio_win_bonus y
zone_fallback_prio no cambian ni una decision. Y todas las busquedas previas
(evolucion9/10, buscar_apertura) usaron paneles rotos o saturados.

OJO — dos trampas conocidas:
  1. MULTIPLICIDAD: 12 brazos contra la misma base. Con t>2 se espera ~0.5
     falsos positivos por puro azar. Nada se adopta sin CONFIRMAR en semillas
     disjuntas (el protocolo que valido seed_stock_aware).
  2. WINNER'S CURSE: `buscar_apertura.py` congelaba la puntuacion del
     incumbente y competia contra un numero inflado. Aqui la base se re-evalua
     en cada corrida, con su propio brazo _noop de control.

HALLAZGO (2026-09-03): las prioridades son un RANKING, no magnitudes. Tres pares
de brazos salieron identicos celda a celda porque producen la MISMA reordenacion:
  water_30 == feed_85     (ambos ponen FEED siempre por encima de WATER)
  harvest_50 == fert_60   (ambos ponen FERTILIZE por encima del HARVEST de baja)
  plant_55 == fert_30     (ambos ponen PLANT por encima de FERTILIZE)
Y plant_28 == base: bajar una prioridad que ya es la ultima no reordena nada.
Consecuencia: buscar sobre estos numeros como si fueran continuos (evolucion9/10)
explora un espacio con redundancia masiva. El espacio real es el de ORDENES.

Uso:  ./.venv/bin/python barrido.py [seed0] [brazo1,brazo2,...]
"""
import glob, json, math, os, statistics as st, sys
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
BASE = "CAMPEONA_HOZ"
SEED0 = int(sys.argv[1]) if len(sys.argv) > 1 else 92000
SOLO = sys.argv[2].split(",") if len(sys.argv) > 2 else None
N_SEEDS = 8 if SOLO else 4          # menos brazos -> mas semillas -> mas potencia
# S6.1: el HIRE n-esimo del dia cuesta fib(n) -> 1,1,2,3,5,8,13,21,34,55,89,144.
# La mano 12 cuesta $144 DIARIOS y los peones desaparecen cada noche (S6.3).
# OJO: n_h = min(hands_per_quadrant * cuadrantes, hands_cap). Con hpq=4 y 3
# cuadrantes eso es min(12, 12): NI `hands_cap=14` NI `hands_per_quadrant=5`
# pueden morder por separado. Los dos experimentos de plantilla del pasado eran
# estructuralmente incapaces de probar la hipotesis. Hay que mover LAS DOS.
PLANTILLA = {
    "noop":      {},
    "h9":        {"hands_cap": 9},                                  # recorte: solo el tardio
    "h10":       {"hands_cap": 10},
    "h11":       {"hands_cap": 11},
    "hpq5_solo": {"hands_per_quadrant": 5},                         # solo el temprano (tardio sigue 12)
    "h14":       {"hands_per_quadrant": 5, "hands_cap": 14},
    "h15":       {"hands_per_quadrant": 5, "hands_cap": 15},
    "por_trabajo": {"hire_by_work": True},                          # plantilla al ritmo del TRABAJO
}

# GANSOS/HUEVOS. EGG es el unico producto animal con sumidero casi infinito:
# 400 unidades todavia pagan $39.7 (79% del base), mientras MILK y WOOL se
# hunden a $1 pasadas las ~100. Y el ganso es el mejor animal en las tres
# dimensiones: cuesta menos ($300 vs 400/500), produce antes (dia 4 vs 8/6) y
# produce A DIARIO (iv=1 vs 2/3). 32 de 40 rivales no tienen ninguno.
# La base vende 140 MILK + 119 WOOL, muy pasado el colapso: producto regalado.
GANSOS = {
    "noop":   {},
    "g6":     {"animals": [("GOOSE", 6)]},
    "g8":     {"animals": [("GOOSE", 8)]},
    "g10":    {"animals": [("GOOSE", 10)]},
    "g12":    {"animals": [("GOOSE", 12)]},
    "vaca_g": {"animals": [("COW", 4), ("GOOSE", 4)]},
    "mixto":  {"animals": [("COW", 2), ("GOOSE", 6)]},
    "suma_g4":{"animals": [("COW", 4), ("SHEEP", 4), ("GOOSE", 4)]},
}

VARIANTES = {
    "noop":         {},                        # control: DEBE leer +0.0
    "water_30":     {"prio_water": 30},
    "water_60":     {"prio_water": 60},
    "harvest_50":   {"prio_harvest": 50},
    "harvest_76":   {"prio_harvest": 76},
    "feed_65":      {"prio_feed": 65},
    "feed_85":      {"prio_feed": 85},
    "care_55":      {"prio_care": 55},
    "care_80":      {"prio_care": 80},
    "plant_28":     {"prio_plant": 28},
    "plant_55":     {"prio_plant": 55},
    "fert_30":      {"fert_prio": 30},
    "fert_60":      {"fert_prio": 60},
}


if os.environ.get("SET") == "plantilla":
    VARIANTES = PLANTILLA
if os.environ.get("SET") == "gansos":
    VARIANTES = GANSOS
if SOLO:
    VARIANTES = {k: v for k, v in VARIANTES.items() if k in ("noop",) or k in SOLO}


def _una(a):
    nombre, tape, seed, seat = a
    from kaggle_environments import make
    from bots import arquetipos
    from bots.chassis import make_agent
    from harness import materialize
    cfg = dict(getattr(arquetipos, BASE))
    cfg.update(VARIANTES.get(nombre, {}))
    yo, riv = make_agent(cfg), materialize(f"bots.meta.tape:{tape}")
    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=False)
    env.run([yo, riv] if seat == 0 else [riv, yo])
    f = env.steps[-1]
    mio, suyo = f[seat].reward or 0, f[1 - seat].reward or 0
    return (nombre, tape, seed), (1.0 if mio > suyo else (0.5 if mio == suyo else 0.0))


def main():                                     # GUARD OBLIGATORIO
    tapes = [os.path.basename(f)[:-8] for f in glob.glob("bots/meta/tapes/lad_*.json.gz")]
    seeds = list(range(SEED0, SEED0 + N_SEEDS))
    nombres = ["base"] + list(VARIANTES)
    jobs = [(n, t, s, seat) for n in nombres for t in tapes for s in seeds for seat in (0, 1)]
    print(f"{len(nombres)} brazos x {len(tapes)} cintas x {len(seeds)} seeds x 2 asientos "
          f"= {len(jobs)} episodios (seeds {seeds[0]}-{seeds[-1]})", flush=True)
    with Pool(max(1, (os.cpu_count() or 2) - 1)) as pool:
        res = pool.map(_una, jobs)
    por = {}
    for (n, t, s), v in res:
        por.setdefault(n, {}).setdefault((t, s), []).append(v)
    pares = {n: {k: sum(v) / len(v) for k, v in d.items()} for n, d in por.items()}
    json.dump({n: {f"{k[0]}|{k[1]}": v for k, v in d.items()} for n, d in pares.items()},
              open(f"results/barrido_{SEED0}.json", "w"))
    base = pares["base"]
    print(f"\n{'brazo':14s} {'panel 40':>9} {'delta':>8} {'sd':>7} {'t':>7}")
    print(f"{'base':14s} {100*st.mean(list(base.values())):>8.1f}%")
    filas = []
    for n in VARIANTES:
        k = sorted(set(base) & set(pares[n]))
        d = [pares[n][x] - base[x] for x in k]
        m, sd = st.mean(d), st.stdev(d)
        t = m / (sd / math.sqrt(len(d))) if sd else float("nan")
        filas.append((n, 100 * st.mean(list(pares[n].values())), 100 * m, 100 * sd, t))
    for n, wr, m, sd, t in sorted(filas, key=lambda r: -(r[4] if r[4] == r[4] else -9)):
        aviso = "  <-- sd=0: NO DISPARA" if sd == 0 and n != "noop" else ""
        print(f"{n:14s} {wr:>8.1f}% {m:>+7.1f} {sd:>7.1f} {t:>+7.2f}{aviso}")
    print("\nNada se adopta con esta tabla sola: 12 brazos contra una base es"
          "\nmultiplicidad. Los supervivientes van a confirmacion en seeds disjuntas.")


if __name__ == "__main__":
    main()
