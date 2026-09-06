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
      SET=semillas_parciales N_SEEDS=4 WORKERS=4 ./.venv/bin/python barrido.py 99000

Cada corrida conserva pares JSON compatibles, episodios JSONL incrementales y
un manifiesto .meta.json. Un archivo existente nunca se sobrescribe.
"""
import glob, hashlib, json, math, os, platform, statistics as st, sys, time
from datetime import datetime, timezone
from importlib.metadata import version
from multiprocessing import Pool
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
BASE = "CAMPEONA_HOZ"
SEED0 = int(sys.argv[1]) if len(sys.argv) > 1 else 92000
SOLO = sys.argv[2].split(",") if len(sys.argv) > 2 else None
N_SEEDS = int(os.environ.get("N_SEEDS", 8 if SOLO else 4))
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

# LEAD TIME. Comparados 12 replays de tetsuya con 24 partidas nuestras:
#   MELON      nosotros 20.8 tiles dia medio 7.8  | tetsuya 13.1 dia medio 5.2
#   STRAWBERRY nosotros 41.2 dia medio 11.7       | tetsuya 37.8 dia medio 7.5
# Llegamos 2.6 y 4.2 dias TARDE en los dos cultivos con first=10, que son los
# que generan la caja de los dias 12-18. El dia 0-1 metemos 17 trigos que
# taponan las tiles; ellos ponen 10 trigos y ya fresa el dia 1 y melon el 3.
# Zona muerta medida: d14 +459, d15 +472, d16 -289 contra sus +10204/+7350/+5948.
LEAD = {
    "noop":   {},
    "pf4":    {"premium_first": True, "premium_day": 4},
    "pf6":    {"premium_first": True, "premium_day": 6},
    "pf8":    {"premium_first": True, "premium_day": 8},
    "pf10":   {"premium_first": True, "premium_day": 10},
    "pf6_l8": {"premium_first": True, "premium_day": 6, "premium_lead": 8},
    "pf8_l8": {"premium_first": True, "premium_day": 8, "premium_lead": 8},
    "pf12":   {"premium_first": True, "premium_day": 12},
}

# FORRAJE FANTASMA. `wheat_floor` usaba el rebano PLANEADO (8) desde el dia 0,
# cuando aun no tenemos ningun animal: 8 tiles reservadas para alimentar a nadie,
# y son las tiles que melon y fresa (first=10) necesitan temprano. El trigo tarda
# 4 dias en dar, asi que basta adelantarse unos pocos animales al rebano VIVO.
# (premium_first fallo con sd=0.0: el scorer YA elegia melon/fresa el dia 0-6;
#  el tapon no venia de la eleccion sino de este piso de forraje, que se planta
#  ANTES en el bucle de la linea 819.)
FORRAJE = {
    "noop":   {},
    "wl0":    {"wheat_floor_live": True, "feed_lookahead": 0},
    "wl2":    {"wheat_floor_live": True, "feed_lookahead": 2},
    "wl3":    {"wheat_floor_live": True, "feed_lookahead": 3},
    "wl4":    {"wheat_floor_live": True, "feed_lookahead": 4},
    "wl6":    {"wheat_floor_live": True, "feed_lookahead": 6},
    "wl2_pf": {"wheat_floor_live": True, "feed_lookahead": 2,
               "premium_first": True, "premium_day": 8},
    "wf4":    {"wheat_floor": 4},          # control: bajar el piso fijo sin mas
}

# Compra parcial cuando hay caja para algunas semillas, pero no para el lote.
# El control anterior se carga COMPLETO: un update sobre HOZ conservaria fixes
# nuevos y dejaria de ser CAMPEONA_FB.
SEMILLAS_PARCIALES = {
    "noop": {},
    "_peor": {},
    "partial_batch": {"seed_partial_batch": True},
}
EXACT_CONFIGS = {}

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
if os.environ.get("SET") == "lead":
    VARIANTES = LEAD
if os.environ.get("SET") == "forraje":
    VARIANTES = FORRAJE
# ABLACION de harvest_76 (2026-09-05). CAMPEONA_HOZ YA lleva prio_harvest=76,
# asi que el test correcto es QUITARLO: si vale +2.5, `sin_h76` debe leer ~-2.5.
# 62 es el default del chasis, o sea el valor previo a la adopcion.
# Motivo: la adopcion se hizo con t por celda 2.96, pero el diseno es cruzado y
# a dos vias da t=+1.76 (IC95 [-0.85; +5.85]). Nunca tuvo replica con potencia,
# y un efecto el DOBLE de grande (compra parcial, +4.84) acaba de dar +0.23 al
# replicarlo con 16 semillas.
ABLACION_H76 = {
    "noop": {},
    "_peor": {},
    "sin_h76": {"prio_harvest": 62},
}

if os.environ.get("SET") == "ablacion_h76":
    VARIANTES = ABLACION_H76
    EXACT_CONFIGS = {"_peor": "CAMPEONA_FB"}

if os.environ.get("SET") == "semillas_parciales":
    VARIANTES = SEMILLAS_PARCIALES
    EXACT_CONFIGS = {"_peor": "CAMPEONA_FB"}
if SOLO:
    VARIANTES = {k: v for k, v in VARIANTES.items() if k in ("noop", "_peor") or k in SOLO}


def _hash(value):
    # Conservar orden de diccionarios: el orden de plants forma parte del bot.
    raw = json.dumps(value, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(raw.encode()).hexdigest()


def _config(nombre):
    from bots import arquetipos
    if nombre in EXACT_CONFIGS:
        return dict(getattr(arquetipos, EXACT_CONFIGS[nombre]))
    cfg = dict(getattr(arquetipos, BASE))
    cfg.update(VARIANTES.get(nombre, {}))
    return cfg


def _una(a):
    nombre, tape, seed, seat, cfg = a
    result = dict(arm=nombre, tape=tape, seed=seed, seat=seat, config_hash=_hash(cfg), valid=False)
    start = time.monotonic()
    try:
        from kaggle_environments import make
        from bots.chassis import make_agent
        from harness import materialize
        yo, riv = make_agent(cfg), materialize(f"bots.meta.tape:{tape}")
        hashes = [hashlib.sha256(), hashlib.sha256()]
        counts = [0, 0]

        def traced(agent, player):
            def call(obs):
                action = agent(obs)
                # Serializar antes de entregar al motor: éste puede mutar las
                # listas. La igualdad de resultados no prueba igual conducta.
                raw = json.dumps({"step": obs.get("step"), "action": action},
                                 sort_keys=True, separators=(",", ":"), allow_nan=False)
                hashes[player].update(raw.encode())
                hashes[player].update(b"\n")
                counts[player] += 1
                return action
            return call

        yo, riv = traced(yo, seat), traced(riv, 1 - seat)
        env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=False)
        env.run([yo, riv] if seat == 0 else [riv, yo])
        final = env.steps[-1]
        rewards = [p.reward for p in final]
        statuses = [str(p.status) for p in final]
        bad = [(i, p, str(s.status)) for i, step in enumerate(env.steps)
               for p, s in enumerate(step) if str(s.status) in ("ERROR", "TIMEOUT", "INVALID")]
        result.update(rewards=rewards, statuses=statuses, bad_statuses=bad,
                      steps=len(env.steps),
                      action_hashes=[h.hexdigest() for h in hashes], action_counts=counts)
        if bad or statuses != ["DONE", "DONE"]:
            raise ValueError(f"estado de episodio invalido: final={statuses}, errores={bad[:3]}")
        if any(not isinstance(r, (int, float)) or not math.isfinite(r) for r in rewards):
            raise ValueError(f"recompensas invalidas: {rewards}")
        mio, suyo = rewards[seat], rewards[1 - seat]
        result.update(valid=True, score=1.0 if mio > suyo else (0.5 if mio == suyo else 0.0))
    except Exception as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
    result["seconds"] = time.monotonic() - start
    return result


def _stats(values):
    n = len(values)
    mean = st.mean(values)
    sd = st.stdev(values) if n > 1 else None
    se = sd / math.sqrt(n) if sd is not None else None
    return dict(n=n, mean=mean, sd=sd, se=se, t=mean / se if se else None)


def _summary(pares, records):
    base = pares["base"]
    out = {}
    for nombre, arm in pares.items():
        if set(arm) != set(base):
            raise ValueError(f"celdas incompletas: {nombre}")
        delta = {k: arm[k] - base[k] for k in sorted(base)}
        seeds = sorted({s for _, s in delta})
        by_seed = {s: st.mean([v for (_, seed), v in delta.items() if seed == s]) for s in seeds}
        own = [r for (n, _, _, _), r in records.items() if n == nombre]
        changed = sum(r["action_hashes"][r["seat"]] !=
                      records[("base", r["tape"], r["seed"], r["seat"])]["action_hashes"][r["seat"]]
                      for r in own)
        out[nombre] = dict(win_rate=st.mean(list(arm.values())), cell=_stats(list(delta.values())),
                           seed=_stats(list(by_seed.values())), seed_deltas=by_seed,
                           action_changed_episodes=changed, episodes=len(own))
    return out


def _check_noop(records, tape, seed, seat):
    keys = [(n, tape, seed, seat) for n in ("base", "noop")]
    if not all(k in records for k in keys):
        return
    base, noop = (records[k] for k in keys)
    fields = ("config_hash", "rewards", "statuses", "steps", "action_hashes", "action_counts", "score")
    dif = [f for f in fields if base[f] != noop[f]]
    if dif:
        raise ValueError(f"NOOP distinto de base en {(tape, seed, seat)}: {dif}")


def _file_hashes(paths):
    return {str(p): hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in paths}


def _save_meta(path, meta):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(meta, indent=2, ensure_ascii=False, allow_nan=False) + "\n")
    os.replace(temporary, path)


def _reserve_output():
    Path("results").mkdir(exist_ok=True)
    suffix = 0
    while True:
        stem = Path("results") / (f"barrido_{SEED0}" + (f"_{suffix}" if suffix else ""))
        paths = [Path(str(stem) + ext) for ext in (".json", ".meta.json", ".episodes.jsonl")]
        if not any(p.exists() for p in paths):
            try:
                return (*paths, paths[2].open("x"))
            except FileExistsError:
                pass
        suffix += 1


def main():                                     # GUARD OBLIGATORIO
    if N_SEEDS < 1:
        raise ValueError("N_SEEDS debe ser positivo")
    max_workers = max(1, (os.cpu_count() or 2) - 1)
    requested = int(os.environ.get("WORKERS", max_workers))
    if requested < 1:
        raise ValueError("WORKERS debe ser positivo")
    workers = min(requested, max_workers)
    patron = os.environ.get("TAPES", "lad_")
    tape_paths = sorted(glob.glob(f"bots/meta/tapes/{patron}*.json.gz"))
    if not tape_paths:
        raise ValueError(f"ninguna cinta coincide con TAPES={patron!r}")
    tapes = [os.path.basename(f)[:-8] for f in tape_paths]
    seeds = list(range(SEED0, SEED0 + N_SEEDS))
    nombres = ["base"] + list(VARIANTES)
    configs = {n: _config(n) for n in nombres}
    # Controles juntos a la base: detectar una discrepancia antes de gastar el panel.
    jobs = [(n, t, s, seat, configs[n]) for t in tapes for s in seeds for seat in (0, 1) for n in nombres]
    sources = ["barrido.py", "bots/chassis.py", "bots/arquetipos.py", "bots/meta/tape.py", "harness.py"]
    hashes = _file_hashes(sources + tape_paths)
    pair_path, meta_path, raw_path, raw = _reserve_output()
    meta = dict(schema=1, state="running", started_at=datetime.now(timezone.utc).isoformat(),
                set=os.environ.get("SET", "prioridades"), base=BASE, command=sys.argv,
                seeds=seeds, seed_start=seeds[0], seed_end_inclusive=seeds[-1],
                tapes=tapes, workers=workers, expected_episodes=len(jobs), completed_episodes=0,
                python=platform.python_version(), kaggle_environments=version("kaggle-environments"),
                configs=configs, config_hashes={n: _hash(c) for n, c in configs.items()},
                exact_configs=EXACT_CONFIGS, file_hashes=hashes,
                paths=dict(pairs=str(pair_path), metadata=str(meta_path), episodes=str(raw_path)),
                statistics="Paired W/L/T deltas; cell=(tape,seed), seed=mean delta across fixed tapes.")
    records = {}
    last_progress = time.monotonic()
    _save_meta(meta_path, meta)
    print(f"{len(nombres)} brazos x {len(tapes)} cintas x {len(seeds)} seeds x 2 asientos "
          f"= {len(jobs)} episodios (seeds {seeds[0]}-{seeds[-1]}, workers {workers})\n"
          f"Episodios: {raw_path}; manifiesto: {meta_path}", flush=True)
    try:
        with raw, Pool(workers) as pool:
            for result in pool.imap_unordered(_una, jobs, chunksize=1):
                raw.write(json.dumps(result, ensure_ascii=False, allow_nan=False) + "\n")
                raw.flush()
                key = (result["arm"], result["tape"], result["seed"], result["seat"])
                if key in records:
                    raise ValueError(f"episodio duplicado: {key}")
                records[key] = result
                meta["completed_episodes"] = len(records)
                if not result["valid"]:
                    raise ValueError(f"episodio fallido {key}: {result.get('error')}")
                if result["config_hash"] != meta["config_hashes"][result["arm"]]:
                    raise ValueError(f"config distinta del manifiesto: {key}")
                _check_noop(records, result["tape"], result["seed"], result["seat"])
                if len(records) % 64 == 0 or time.monotonic() - last_progress >= 30:
                    _save_meta(meta_path, meta)
                    print(f"Progreso {len(records)}/{len(jobs)} episodios guardados", flush=True)
                    last_progress = time.monotonic()
        expected = {(n, t, s, seat) for n, t, s, seat, _ in jobs}
        if set(records) != expected:
            raise ValueError("episodios faltantes o inesperados")
        if _file_hashes(sources + tape_paths) != hashes:
            raise ValueError("fuentes o cintas cambiaron durante la corrida")
        pares = {n: {(t, s): st.mean([records[(n, t, s, seat)]["score"] for seat in (0, 1)])
                     for t in tapes for s in seeds} for n in nombres}
        summary = _summary(pares, records)
        meta.update(state="complete", noop="exact rewards, statuses, steps and both action trajectories",
                    summary=summary, finished_at=datetime.now(timezone.utc).isoformat())
        with pair_path.open("x") as output:
            json.dump({n: {f"{t}|{s}": v for (t, s), v in arm.items()} for n, arm in pares.items()}, output)
        _save_meta(meta_path, meta)
    except BaseException as exc:
        meta.update(state="invalid", error=f"{type(exc).__name__}: {exc}",
                    finished_at=datetime.now(timezone.utc).isoformat())
        _save_meta(meta_path, meta)
        raise
    print(f"\nNOOP exacto en {len(tapes) * len(seeds) * 2} episodios. Pares: {pair_path}")
    print(f"{'brazo':14s} {'panel':>8} {'delta':>8} {'sd cel':>8} {'SE cel':>8} {'t cel':>8} {'SE seed':>8} {'t seed':>8} {'acciones':>9}")
    def number(value):
        return f"{value:+8.2f}" if value is not None else f"{'-':>8}"
    for n, r in summary.items():
        cell, seed = r["cell"], r["seed"]
        print(f"{n:14s} {100*r['win_rate']:>7.1f}% {100*cell['mean']:>+7.1f} "
              + " ".join(number(v) for v in (100*cell['sd'] if cell['sd'] is not None else None,
                  100*cell['se'] if cell['se'] is not None else None, cell['t'],
                  100*seed['se'] if seed['se'] is not None else None, seed['t']))
              + f" {r['action_changed_episodes']:>5}/{r['episodes']}")
        if cell["sd"] == 0 and n not in ("base", "noop"):
            print("  sd=0: delta W/L/T constante; no determina si la conducta cambio.")
    if "_peor" in summary:
        print("_peor es CAMPEONA_FB exacta. Revisar su separacion de base antes de interpretar mejoras.")
    print("SE/t por celda conservan el reporte anterior; SE/t por seed agrupan todas las cintas.\n"
          "Nada se adopta con esta tabla sola: confirmar en semillas disjuntas.")


if __name__ == "__main__":
    main()
