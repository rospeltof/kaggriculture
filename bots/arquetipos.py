"""Los cuatro arquetipos del torneo — hipótesis en forma de bot.

Cada uno es una config sobre el chasis compartido. Funciones a nivel de módulo
para que el harness las importe en los workers ("bots.arquetipos:gansos").
"""
from bots.chassis import make_agent

# Control: solo cultivos, sin animales.
CONTROL = dict(
    hands=2,
    animals=[],
    plants={"CARROT": 8, "WHEAT": 6, "MELON": 6, "TOMATO": 4},
)

# Hipótesis del usuario: wheat + melón en menor proporción + gansos rápido.
GANSOS = dict(
    hands=3,
    animals=[("GOOSE", 6)],
    plants={"WHEAT": 8, "MELON": 4, "CARROT": 4},
    care=True,
    collect_fert=True,
)

# Hipótesis de Claude: wheat + melón + ovejas/vacas con care.
OVEJAS_VACAS = dict(
    hands=3,
    animals=[("SHEEP", 3), ("COW", 3)],
    plants={"WHEAT": 8, "MELON": 4, "CARROT": 3},
    care=True,
    collect_fert=True,
)

# Estilo writeup: fresas + 4 ovejas + 8 vacas (necesita comprar tierra).
WRITEUP = dict(
    hands=4,
    animals=[("SHEEP", 4), ("COW", 8)],
    plants={"WHEAT": 12, "STRAWBERRY": 5},
    care=True,
    collect_fert=True,
    buy_land=True,
    max_quadrants=2,
)

# Campeón de la generación 1 de búsqueda en masa (evolucion.py, config g1_02
# encontrada por muestreo aleatorio): vacas escaladas + premium crops + fertilizer.
VACAS_MELON = dict(
    hands=4,
    animals=[("COW", 5)],
    plants={"WHEAT": 5, "MELON": 8, "STRAWBERRY": 3},
    care=True,
    collect_fert=True,
    fert_prio=45,
    buy_land=True,
    max_quadrants=2,
)

# Campeón de la evolución multi-generacional (evolucion2.py, mutante g11m_11):
# rebaño mixto + melón pesado + 8 peones (el máximo permitido) + cosecha inmediata.
# Confirmado 50-0 vs vacas_melon en seeds vírgenes ($53.4k vs $34.6k).
OCHO_MANOS = dict(
    hands=8,
    animals=[("COW", 4), ("SHEEP", 2)],
    plants={"CARROT": 1, "MELON": 12, "STRAWBERRY": 3, "WHEAT": 9},
    care=True,
    collect_fert=True,
    fert_prio=45,
    animal_harvest_at=1,
    premium_hold_day=8,
    buy_land=True,
    max_quadrants=2,
)

# Campeón de la evolución 3 (policy search, mutante h7m_10): rebaño mixto 4+4,
# CARE con prioridad alta (70), cosecha animal acumulada (harvest_at=4), sin
# urgencia horaria y SIN zonificación (la evolución la rechazó unánimemente).
# Confirmado 50-0 vs ocho_manos en seeds vírgenes ($59.4k vs $49.9k).
MIMADA = dict(
    hands=8,
    animals=[("COW", 4), ("SHEEP", 4)],
    # OJO: el ORDEN del dict de plantas es parte de la estrategia (el chasis
    # compra/planta iterando en orden de inserción). h7m_10 usaba orden
    # alfabético; transcribir en otro orden lo debilita (ver BITACORA 2026-08-19).
    plants={"CARROT": 1, "MELON": 9, "STRAWBERRY": 3, "WHEAT": 9},
    care=True,
    collect_fert=True,
    fert_prio=45,
    animal_harvest_at=4,
    premium_hold_day=8,
    buy_land=True,
    max_quadrants=2,
    prio_care=70,
    prio_urgency=25,
)

# v2 tras análisis de replays reales + ablación (BITACORA 2026-08-26): SOLO los
# dos fixes que ganaron 16/16 aislados — plantar cerca del shed y protocolo de
# cierre (cosechar/cargar/DROP/vender). grow y land3 resultaron venenos; dig30 neutro.
MIMADA_V2 = dict(
    MIMADA,
    plant_near=True,
    endgame=True,
)

# v3: v2 + planificación de cultivos adaptativa al mercado — score $/tile-día
# con el precio evaluado en inventario + pipeline propio (espejo verificado de
# la curva del motor). Nunca inunda su propio mercado; explota escaseces (hinge).
MIMADA_V3 = dict(
    MIMADA_V2,
    adaptive=True,
    crop_tiles=22,
)

# Campeón de la evolución 4 (k8m_22): la planificación ADAPTATIVA al mercado
# gana con mkt_opp_factor=1 (menos pesimista que el ajuste manual) y wheat_floor
# auto (= rebaño). Final 52/54; confirmado 50-0 vs mimada_v2 en seeds vírgenes.
# Transcripción VERBATIM del output normalizado (el orden de dicts es ADN).
MIMADA_V4 = {
    "hands": 8,
    "animals": [("COW", 4), ("SHEEP", 4)],
    "plants": {"CARROT": 1, "MELON": 11, "STRAWBERRY": 3, "WHEAT": 8},
    "care": True,
    "collect_fert": True,
    "fert_prio": 45,
    "animal_harvest_at": 4,
    "premium_hold_day": 8,
    "buy_land": True,
    "max_quadrants": 2,
    "prio_care": 70,
    "prio_urgency": 25,
    "plant_near": True,
    "endgame": True,
    "adaptive": True,
    "crop_tiles": 22,
    "zoning": False,
    "zone_fallback_prio": 70,
    "prio_feed": 88,
    "prio_water": 44,
    "prio_win_bonus": 12,
    "prio_harvest": 62,
    "prio_plant": 40,
    "grow": False,
    "prio_dig": 8,
    "mkt_opp_factor": 1,
}

# Clon aproximado de "ln" (rank 862, score 1794, nos ganó con $161.7k): wheat
# masivo como columna vertebral (alimenta el rebaño Y vende a prueba de gluts),
# fresas a escala (demanda del town), 11 vacas + 4 ovejas, 3 cuadrantes día 7.
# Sirve como oponente de panel representativo del meta real (perfilar_rivales.py).
LN_CLONE = dict(
    hands=10,
    animals=[("COW", 11), ("SHEEP", 4)],
    plants={"STRAWBERRY": 19, "WHEAT": 41},
    care=True,
    collect_fert=True,
    fert_prio=45,
    animal_harvest_at=2,
    buy_land=True,
    max_quadrants=3,
    prio_care=70,
    plant_near=True,
    endgame=True,
)

control = make_agent(CONTROL)
gansos = make_agent(GANSOS)
ovejas_vacas = make_agent(OVEJAS_VACAS)
writeup = make_agent(WRITEUP)
vacas_melon = make_agent(VACAS_MELON)
ocho_manos = make_agent(OCHO_MANOS)
mimada = make_agent(MIMADA)
mimada_v2 = make_agent(MIMADA_V2)
mimada_v3 = make_agent(MIMADA_V3)
mimada_v4 = make_agent(MIMADA_V4)
ln_clone = make_agent(LN_CLONE)

# Iteración de fidelidad del clon: multi_feeder (logística matinal en paralelo)
# y variante con zonificación — a gran escala la asignación greedy se ahoga.
LN_CLONE_V2 = dict(LN_CLONE, multi_feeder=True)
LN_CLONE_V2Z = dict(LN_CLONE, multi_feeder=True, zoning=True, zone_fallback_prio=80)
ln_clone_v2 = make_agent(LN_CLONE_V2)
ln_clone_v2z = make_agent(LN_CLONE_V2Z)

# Fase de capital (phased): semillas baratas-primero con tope de gasto,
# estructuras solo con animal a la vista, ningún animal sin pipeline de comida.
LN_CLONE_V3 = dict(LN_CLONE, multi_feeder=True, phased=True)
ln_clone_v3 = make_agent(LN_CLONE_V3)

# v4 del clon: WHEAT primero en el dict (pipeline de comida y caja antes que
# fresas), y DIG alto para reciclar las tumbas de fresas cosechadas.
LN_CLONE_V4 = dict(LN_CLONE_V3, plants={"WHEAT": 41, "STRAWBERRY": 19}, prio_dig=45)
ln_clone_v4 = make_agent(LN_CLONE_V4)

# Subcampeón de la evolución 5 (m8m_08): la v4 ESCALADA — 12 animales + 3er
# cuadrante + multi_feeder (adoptado por 8/9 finalistas evolucionados). Perdió
# el cara-a-cara vs v4 (45/54) pero fue el MEJOR en dinero medio del campo
# ($64.2k vs $56.6k de v4): contra oponentes diversos (= el ladder) produce más;
# contra el gemelo, su volumen estrella los mercados compartidos. VERBATIM.
MIMADA_XL = {
    "hands": 9,
    "animals": [("COW", 6), ("SHEEP", 6)],
    "plants": {"CARROT": 1, "MELON": 11, "STRAWBERRY": 3, "WHEAT": 12},
    "care": True,
    "collect_fert": True,
    "fert_prio": 45,
    "animal_harvest_at": 4,
    "premium_hold_day": 8,
    "buy_land": True,
    "max_quadrants": 3,
    "prio_care": 70,
    "prio_urgency": 25,
    "plant_near": True,
    "endgame": True,
    "adaptive": True,
    "crop_tiles": 22,
    "zoning": False,
    "zone_fallback_prio": 70,
    "prio_feed": 88,
    "prio_water": 44,
    "prio_win_bonus": 12,
    "prio_harvest": 78,
    "prio_plant": 40,
    "grow": False,
    "prio_dig": 8,
    "mkt_opp_factor": 1,
    "multi_feeder": True,
    "phased": False,
    "tiles_per_unit": 5,
}
mimada_xl = make_agent(MIMADA_XL)

# Opción B fase 1: router de jornada (plan al alba, serpentina balanceada,
# bundling por tile, reparación) + contratación hasta el día 29.
MIMADA_V5R = dict(MIMADA_V4, router=True, hire_late=True)
mimada_v5r = make_agent(MIMADA_V5R)

# v5r con la granja expandida para usar la capacidad que el router libera.
MIMADA_V5RXL = dict(MIMADA_V5R, animals=[("COW", 6), ("SHEEP", 6)], crop_tiles=40,
                    max_quadrants=3, hands=10, fert_prio=75)
mimada_v5rxl = make_agent(MIMADA_V5RXL)

# Campeón de la evolución 7 (r4e_1): la granja redimensionada para el router —
# crop_tiles 30 (adaptativo), fresas 5, 3er cuadrante, 7 peones. $80.6k bajo
# presión de mercado de la cinta (v5r: $63.2k) y $100.2k vs débil — nivel
# absoluto de las finales del título. VERBATIM de results/evolucion7.json.
RUTERA = {
    "hands": 7,
    "animals": [("COW", 4), ("SHEEP", 4)],
    "plants": {"CARROT": 1, "MELON": 11, "STRAWBERRY": 5, "WHEAT": 8},
    "care": True,
    "collect_fert": True,
    "fert_prio": 45,
    "animal_harvest_at": 4,
    "premium_hold_day": 8,
    "buy_land": True,
    "max_quadrants": 3,
    "prio_care": 70,
    "prio_urgency": 25,
    "plant_near": True,
    "endgame": True,
    "adaptive": True,
    "crop_tiles": 30,
    "zoning": False,
    "zone_fallback_prio": 70,
    "prio_feed": 88,
    "prio_water": 44,
    "prio_win_bonus": 12,
    "prio_harvest": 62,
    "prio_plant": 40,
    "grow": False,
    "prio_dig": 8,
    "mkt_opp_factor": 1,
    "router": True,
    "hire_late": True,
    "multi_feeder": False,
    "phased": False,
    "tiles_per_unit": 5,
}
rutera = make_agent(RUTERA)

# Campeona de la evolución 8: RUTERA + los 6 mecanismos fase 2 (las observaciones
# del usuario hechas sistema). La evolución no encontró nada mejor que el paquete
# con floor=0.4, hpq=4, fert fresas+tomate — las perillas ya estaban bien.
# $85.1k bajo mercado de la cinta (v5r: $54.9k) y $119.4k absoluto (récord).
INTEGRAL = dict(
    RUTERA,
    sell_floor=0.4,
    idle_plant=True,
    hands_per_quadrant=4,
    land_early=True,
    town_forecast=True,
    fert_crops=["STRAWBERRY", "TOMATO"],
)
integral = make_agent(INTEGRAL)

# Candidata 2026-09-02 — INTEGRAL + los mecanismos del notebook barnyard, ya
# depurados por revisión adversarial (5 bugs) y validados por WIN-RATE, no por
# dinero: 33.3% vs 15.0% de la base en 120 episodios c/u (+18.3 pts, 3.4 sigma),
# con dinero estadísticamente idéntico ($71.8k vs $69.0k). La ganancia es pura
# conversión de duelos cerrados — exactamente lo que paga el Elo.
#   opp_read     lee el pipeline anunciado del rival (tiles + planted_day) y lo
#                mete al scorer en vez del factor ciego mkt_opp_factor
#   sell_rank    ordena nuestra cola de ventas por daño total de cotización
#                (defiende posición en el lockstep)
#   order_budget reserva slots del cupo de 10 para los HIRE del cierre
INTEGRAL_LECTOR = dict(
    INTEGRAL,
    opp_read=True,
    sell_rank=True,
    order_budget=True,
)
integral_lector = make_agent(INTEGRAL_LECTOR)

# Campeona de la evolución 9 (t5e_3) — primera evolución seleccionada por
# WIN-RATE en vez de dinero. Final 60.0% WR (lector: 48.3%); confirmación
# head-to-head en seeds vírgenes: 46-4 vs INTEGRAL_LECTOR ($90.9k vs $81.6k);
# $118.0k absoluto y 8% de ocio en autopsia.
# La evolución ADOPTÓ dos gateados que solos eran neutros: beat_wave (ya
# corregido, con umbral de valor $2,000) y melon_max=8 — la disciplina de melón
# que el usuario pidió, validada dentro de la combinación correcta. También subió
# a 3 cuadrantes y bajó prio_feed a 75. VERBATIM de results/evolucion9_winner.json.
CAMPEONA = {
    "hands": 8,
    "animals": [("COW", 4), ("SHEEP", 4)],
    "plants": {"CARROT": 1, "MELON": 11, "STRAWBERRY": 5, "WHEAT": 8},
    "care": True,
    "collect_fert": True,
    "fert_prio": 45,
    "animal_harvest_at": 4,
    "premium_hold_day": 8,
    "buy_land": True,
    "max_quadrants": 3,
    "prio_care": 70,
    "prio_urgency": 25,
    "plant_near": True,
    "endgame": True,
    "adaptive": True,
    "crop_tiles": 30,
    "zoning": False,
    "zone_fallback_prio": 70,
    "prio_feed": 75,
    "prio_water": 44,
    "prio_win_bonus": 12,
    "prio_harvest": 62,
    "prio_plant": 40,
    "grow": False,
    "prio_dig": 8,
    "mkt_opp_factor": 1,
    "router": True,
    "hire_late": True,
    "multi_feeder": False,
    "phased": False,
    "tiles_per_unit": 5,
    "sell_floor": 0.4,
    "idle_plant": True,
    "hands_per_quadrant": 4,
    "land_early": True,
    "town_forecast": True,
    "fert_crops": ["STRAWBERRY", "TOMATO"],
    "opp_read": True,
    "sell_rank": True,
    "order_budget": True,
    "beat_wave": True,
    "wave_min_value": 2000,
    "melon_max": 8,
    "smart_overflow": False,
    "scorer_v2": False,
}
campeona = make_agent(CAMPEONA)
