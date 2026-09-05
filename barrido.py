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

# VENTAS. Leido el motor (2026-09-03): _process_market cotiza UNIDAD A UNIDAD
# y recalcula market_price con el inventario ya incrementado, asi que una orden
# de 40 uds recorre la curva 40 veces DENTRO del mismo turno. Ademas
# "Sales at $1 do not increase market supply" (_commit_unit): a piso, la oferta
# deja de subir. Medido sobre campeona_hoz, 16 partidas: 5% de perdida por
# rafaga ($5.897) y ~60 unidades/partida vendidas a $1 (WOOL 29.6 = 25% de la
# lana, MILK 18.1 = 13%). `sell_marginal` acota n para que la unidad MARGINAL
# siga por encima de un piso; existe desde hace tiempo y nunca se midio con el
# panel de 40. `sell_floor` decide SI vender; `sell_marginal`, CUANTAS.
VENTAS = {
    "noop":   {},
    "sm_50":  {"sell_marginal": True},                                   # piso 0.5 (def.)
    "sm_30":  {"sell_marginal": True, "sell_marginal_floor": 0.3},
    "sm_20":  {"sell_marginal": True, "sell_marginal_floor": 0.2},
    "sm_10":  {"sell_marginal": True, "sell_marginal_floor": 0.1},
    "sm_05":  {"sell_marginal": True, "sell_marginal_floor": 0.05},
    "sm_70":  {"sell_marginal": True, "sell_marginal_floor": 0.7},
    "hinge_h":{"hinge_hold": True},
}

# CONTRA-META. Medido contra los 40 rivales reales (80 episodios): la escalera
# es PESADA EN ANIMALES (7.7 COW + 4.4 SHEEP + 0.7 GOOSE) y ligera en cultivos
# (3.2 STRAWBERRY). Al cierre, de 9 mercados solo DOS quedan saturados y los
# inundamos NOSOTROS: FERTILIZER (+368, vendemos 157.9) y MELON (+148,
# vendemos 113.9). Todo lo demas acaba por debajo de 10.000 (el town drena mas
# de lo que aporta el conjunto). WHEAT cierra a -448: escasez pura.
# El fertilizante tiene alternativa: duplica el tick de fresa, nuestro producto
# mas caro ($199/ud). `fert_reserve` (def. 20) decide cuanto guardamos.
CONTRAMETA = {
    "noop":     {},
    "fr_40":    {"fert_reserve": 40},
    "fr_60":    {"fert_reserve": 60},
    "fr_100":   {"fert_reserve": 100},          # de facto: no vender fertilizante
    "melon_5":  {"melon_max": 5},
    "melon_11": {"melon_max": 11},
    "fr60_m5":  {"fert_reserve": 60, "melon_max": 5},
    "sin_fert": {"collect_fert": False},        # ni recogerlo (libera acciones)
}

# SUPERFICIE. Analisis de los 12 replays del TOP1 (tetsuya, 11/12 victorias,
# $115.822 medios contra nuestros ~$94k): cultiva ~58 tiles en el pico del dia 12
# contra nuestras 30, y lleva 15 animales contra nuestros 8. Misma plantilla (12
# manos) pero MOVER 44% / PASS 17% / WATER 12% frente a nuestro 53/8/19: cubre el
# doble de superficie moviendose MENOS. Vende 522 fertilizante (nosotros 158) y
# 367 trigo (nosotros 180) -- y el trigo cierra el mercado a -448, en escasez.
# `crop_tiles` MUERDE (muerde.py 6/6) pero su VALOR nunca se barrio.
SUPERFICIE = {
    "noop":    {},
    "ct_40":   {"crop_tiles": 40},
    "ct_50":   {"crop_tiles": 50},
    "ct_58":   {"crop_tiles": 58},
    "ct_70":   {"crop_tiles": 70},
    "q4":      {"max_quadrants": 4},
    "ct50_q4": {"crop_tiles": 50, "max_quadrants": 4},
    "ct58_q4": {"crop_tiles": 58, "max_quadrants": 4},
}

# REBANO GRANDE. Correccion del 2026-09-04: `crop_tiles=30` NO nos limitaba a 30
# tiles (ya plantamos 66 en el pico, mas que las ~58 del top1) y regamos el 94%
# sin que muera ninguna de sed. Ni superficie ni mano de obra son el cuello.
# La diferencia real con tetsuya esta en los ANIMALES: 15 (7.2 SHEEP + 6.1 COW +
# 1.8 GOOSE) contra nuestros 8. Vende 522 fertilizante (nosotros 158), 192 lana
# (118) y 177 leche (137): los tres salen del rebano. Y `sin_fert` vale -50, o
# sea que infrautilizamos a la mitad nuestra palanca mas fuerte.
# Su blitz de 34 tiles de trigo el dia 24 es FORRAJE: 13 animales comen ~325.
# Nunca probamos esta composicion: q_sheep6 eran 10 animales, no 15.
REBANO = {
    "noop":     {},
    "r10":      {"animals": [("COW", 5), ("SHEEP", 5)]},
    "r12":      {"animals": [("COW", 6), ("SHEEP", 6)]},
    "r13":      {"animals": [("COW", 6), ("SHEEP", 7)]},
    "r15_top1": {"animals": [("COW", 6), ("SHEEP", 7), ("GOOSE", 2)]},
    "r16":      {"animals": [("COW", 8), ("SHEEP", 8)]},
    "r13_ct58": {"animals": [("COW", 6), ("SHEEP", 7)], "crop_tiles": 58},
    "r6":       {"animals": [("COW", 3), ("SHEEP", 3)]},
}

# Contra el TOP1 (TAPES=top_): ¿los brazos que pierden contra la escalera de ~800
# se comportan igual contra un rival de 3040? Si NO, nuestro optimo local es un
# optimo CONTRA ESA POBLACION y no una propiedad del juego.
VS_TOP1 = {
    "noop":     {},
    "r13":      {"animals": [("COW", 6), ("SHEEP", 7)]},
    "r15_top1": {"animals": [("COW", 6), ("SHEEP", 7), ("GOOSE", 2)]},
    "ct_58":    {"crop_tiles": 58},
    "h11":      {"hands_cap": 11},
    "q4":       {"max_quadrants": 4},
}

# FERTILIZAR CULTIVOS DE UN CORTE. Descubierto leyendo el motor (2026-09-04):
# en WHEAT/CARROT/MELON el rendimiento lo anade el RIEGO dentro de la ventana
# win, con bonus x2 si esta fertilizado. Nunca los fertilizamos: fert_crops solo
# lleva STRAWBERRY y TOMATO. Trigo 4->6 unidades (+50%) en un mercado que cierra
# a -448 (escasez, ~$46/ud); zanahoria 3->4; melon alcanza el tope 2 dias antes.
# Una sola aplicacion cubre 3 dias = la ventana entera del trigo.
FERT1 = {
    "noop":   {},
    "fw":     {"fert_crops": ["STRAWBERRY","TOMATO","WHEAT"], "fert_single": True},
    "fwc":    {"fert_crops": ["STRAWBERRY","TOMATO","WHEAT","CARROT"], "fert_single": True},
    "fwcm":   {"fert_crops": ["STRAWBERRY","TOMATO","WHEAT","CARROT","MELON"], "fert_single": True},
    "fm":     {"fert_crops": ["STRAWBERRY","TOMATO","MELON"], "fert_single": True},
    "fw_res": {"fert_crops": ["STRAWBERRY","TOMATO","WHEAT"], "fert_single": True,
               "fert_reserve": 40},
    "fwc_res":{"fert_crops": ["STRAWBERRY","TOMATO","WHEAT","CARROT"], "fert_single": True,
               "fert_reserve": 40},
    "fw_noal":{"fert_crops": ["STRAWBERRY","TOMATO","WHEAT"]},   # sin alinear: control
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
if os.environ.get("SET") == "ventas":
    VARIANTES = VENTAS
if os.environ.get("SET") == "contrameta":
    VARIANTES = CONTRAMETA
if os.environ.get("SET") == "superficie":
    VARIANTES = SUPERFICIE
if os.environ.get("SET") == "rebano":
    VARIANTES = REBANO
if os.environ.get("SET") == "vstop1":
    VARIANTES = VS_TOP1
if os.environ.get("SET") == "fert1":
    VARIANTES = FERT1
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
    patron = os.environ.get("TAPES", "lad_")     # `lad_` = 40 rivales reales de
    # nuestras partidas (~800 de rating). `top_` = las 12 cintas de tetsuya, el
    # TOP1 (3040). Son POBLACIONES DISTINTAS y no deben mezclarse.
    tapes = [os.path.basename(f)[:-8] for f in glob.glob(f"bots/meta/tapes/{patron}*.json.gz")]
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
