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
