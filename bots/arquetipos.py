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

control = make_agent(CONTROL)
gansos = make_agent(GANSOS)
ovejas_vacas = make_agent(OVEJAS_VACAS)
writeup = make_agent(WRITEUP)
vacas_melon = make_agent(VACAS_MELON)
ocho_manos = make_agent(OCHO_MANOS)
mimada = make_agent(MIMADA)
mimada_v2 = make_agent(MIMADA_V2)
