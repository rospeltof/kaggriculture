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
    plants={"MELON": 12, "WHEAT": 9, "STRAWBERRY": 3, "CARROT": 1},
    care=True,
    collect_fert=True,
    fert_prio=45,
    animal_harvest_at=1,
    premium_hold_day=8,
    buy_land=True,
    max_quadrants=2,
)

control = make_agent(CONTROL)
gansos = make_agent(GANSOS)
ovejas_vacas = make_agent(OVEJAS_VACAS)
writeup = make_agent(WRITEUP)
vacas_melon = make_agent(VACAS_MELON)
ocho_manos = make_agent(OCHO_MANOS)
