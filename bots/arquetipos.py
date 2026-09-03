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

# Candidata 2026-09-03 — CAMPEONA + season_aware (rendimiento consciente del
# calendario). Nace del análisis forense de la derrota vs Akshay V: íbamos
# +$11,102 el día 18 y perdimos por $40,791; el 85% del gap fueron FRESAS
# (130u nuestras vs 265u suyas) porque las plantamos tarde — 50 tiles desde el
# día 18, cuando una fresa plantada ese día alcanza 1 de sus 4 tandas.
# El scorer ahora calcula las unidades que un cultivo ALCANZA A RENDIR en los
# días que quedan (fresa: 8 hasta el d12, 2 el d18, 0 el d21) y reconoce que
# fertilizada rinde 8 y no 4. Efecto: fresa temprano, carrot solo al cierre.
# Evidencia: dos mediciones independientes, 248 episodios por variante,
# +12.1 puntos de win-rate (2.9 sigma) y +$4k de economía.
CAMPEONA_SEASON = dict(CAMPEONA, season_aware=True)
campeona_season = make_agent(CAMPEONA_SEASON)

# Candidata 2026-09-04 — CAMPEONA + fallback_fix. Nace de la observación del
# usuario ("¿por qué plantamos zanahorias con la fresa a 6x el precio?") y del
# replay 102786320 (campeona_season vs Omkar Kadam): el día 11 teníamos 44
# CARROTS a $42 con la fresa a $186 y CERO tiles nuestras de fresa.
# Causa: cuando melon_max corta el melón, el fallback elegía el segundo cultivo
# con un modelo DISTINTO al del scorer principal (unidades crudas, sin
# season_aware ni el x2 del fertilizante) -> la fresa se hundía bajo la oferta
# rival estimada y ganaba el carrot. Ahora ambos caminos puntúan igual.
# Evidencia: +14.2 pts de win-rate (3.2σ, 120 eps/variante) y +$2,708;
# head-to-head 62-28 (68.9%, 3.9σ) sobre la variante con season_aware, que
# resulta redundante una vez arreglado el fallback.
CAMPEONA_FB = dict(CAMPEONA, fallback_fix=True)
campeona_fb = make_agent(CAMPEONA_FB)


# --- Candidatas 2026-08-31 (teardown del tape C95 del meta) ---------------
# water_cadence: el motor sólo paga el riego (a) en la ventana de un one-time y
# (b) en la víspera de un tick fertilizado de un ongoing; y una planta sólo muere
# con consecutive_unwatered >= 2. Regábamos las 65 fresas TODOS los días: ~2/3 de
# esos riegos rinden exactamente 0. El tape del meta hace 1,017 riegos; nosotros
# 1,410 con menos producción.
CAMPEONA_WC = dict(CAMPEONA_FB, water_cadence=True)
campeona_wc = make_agent(CAMPEONA_WC)

# Brazo de control obligatorio: idéntico a la base. Debe leer +0.0 sigma.
CAMPEONA_NOOP = dict(CAMPEONA_FB)
campeona_noop = make_agent(CAMPEONA_NOOP)

# Ablación del teardown: aislar water_cadence de sus interacciones.
CAMPEONA_WC_NOIDLE = dict(CAMPEONA_FB, water_cadence=True, idle_plant=False)
campeona_wc_noidle = make_agent(CAMPEONA_WC_NOIDLE)

# crop_max: la curva de precios toca el piso de $1 a ~+100 unidades en FRESA,
# LANA y LECHE (medido con _price_at). Vendemos 220 fresas; las ~145 últimas
# valen ~$1. El tape del meta planta 37 fresas y 138 wheat; nosotros 62 y 73.
# Wheat a +450 unidades sigue pagando $19.9 (80% del base): es el único sumidero
# sin fondo. Hipótesis: cambiar fresa marginal por wheat marginal.
CAMPEONA_CAP = dict(CAMPEONA_FB, crop_max={"STRAWBERRY": 8})
campeona_cap = make_agent(CAMPEONA_CAP)
CAMPEONA_CAP12 = dict(CAMPEONA_FB, crop_max={"STRAWBERRY": 12})
campeona_cap12 = make_agent(CAMPEONA_CAP12)

# hire_by_work: plantilla al ritmo del TRABAJO disponible, no del territorio.
# La cinta corre 1/2/3/3/3/4/7/6/7 peones los días 1-9 y 10-14 en el pico
# (media 8.3); nosotros 4 planos hasta el día 8 y 12 desde el 9 (media ~11).
# El exceso son ~950 pasos de commute sin trabajo que los amortice: 0.70
# productivas/movimiento contra 0.98 de la cinta.
# NOTA: la lista de fallidos midió plantillas PLANAS de 6 a 16; esto es una
# CURVA por día, un objeto distinto que nunca se midió.
CAMPEONA_HW = dict(CAMPEONA_FB, hire_by_work=True)
campeona_hw = make_agent(CAMPEONA_HW)
CAMPEONA_HW6 = dict(CAMPEONA_FB, hire_by_work=True, tiles_per_unit=6)
campeona_hw6 = make_agent(CAMPEONA_HW6)
CAMPEONA_HW_CAP = dict(CAMPEONA_FB, hire_by_work=True, hands_cap=14)
campeona_hw_cap = make_agent(CAMPEONA_HW_CAP)

# sell_marginal: acotar CADA orden para que la unidad marginal siga sobre el piso.
# Distinto de sell_floor (que decide SI vender, al precio actual) y de sell_rank
# (que decide EN QUÉ ORDEN). Es el bucle de _plan_sells de C95.
CAMPEONA_SM = dict(CAMPEONA_FB, sell_marginal=True)
campeona_sm = make_agent(CAMPEONA_SM)
CAMPEONA_SM4 = dict(CAMPEONA_FB, sell_marginal=True, sell_marginal_floor=0.4)
campeona_sm4 = make_agent(CAMPEONA_SM4)
CAMPEONA_SM6 = dict(CAMPEONA_FB, sell_marginal=True, sell_marginal_floor=0.6)
campeona_sm6 = make_agent(CAMPEONA_SM6)

# Prueba de la hipótesis inversa: en un mercado COMPARTIDO en lockstep, aguantar
# inventario para no estrellar el precio se lo regala al rival (su columna sube
# monótonamente con nuestro pacing: 114.6k -> 116.3k -> 118.4k). Si es cierto,
# quitar el piso debería ayudarnos.
CAMPEONA_NOFLOOR = dict(CAMPEONA_FB, sell_floor=0)
campeona_nofloor = make_agent(CAMPEONA_NOFLOOR)
CAMPEONA_FLOOR2 = dict(CAMPEONA_FB, sell_floor=0.2)
campeona_floor2 = make_agent(CAMPEONA_FLOOR2)

# drop_deposit: cerrar la latencia de un día entre cosecha y mercado.
# El chasis sólo hacía DROP en el endgame; todo lo demás esperaba al auto-drop
# nocturno y se vendía a h0 del día siguiente (87% de nuestras ventas a h0 contra
# 52% de C95; primera venta de melón step 288 contra su step 252).
CAMPEONA_DD = dict(CAMPEONA_FB, drop_deposit=True)
campeona_dd = make_agent(CAMPEONA_DD)
CAMPEONA_DD1000 = dict(CAMPEONA_FB, drop_deposit=True, drop_value=1000)
campeona_dd1000 = make_agent(CAMPEONA_DD1000)
# combinación con el único positivo pareado del día
CAMPEONA_DD_NF = dict(CAMPEONA_FB, drop_deposit=True, sell_floor=0)
campeona_dd_nf = make_agent(CAMPEONA_DD_NF)

# --- Tomate/hinge: la única asimetría de información a nuestro favor ----------
# El parche 1.32.7 puso curva `hinge` a CARROT/TOMATO/EGG. La tabla _MP de C95 es
# ANTERIOR al parche (CARROT below_target 0.20, sin hinge): el meta los valora mal.
# Demanda de temporada del tomate ~250u contra oferta combinada de 6u.
# Precio a deficit 300: $144. A 400: $300.
CAMPEONA_HINGE = dict(CAMPEONA_FB, hinge_forecast=True)
campeona_hinge = make_agent(CAMPEONA_HINGE)
CAMPEONA_HINGE_HOLD = dict(CAMPEONA_FB, hinge_forecast=True, hinge_hold=True)
campeona_hinge_hold = make_agent(CAMPEONA_HINGE_HOLD)

# fert_dawn_load: cargar fertilizante en el PRIMER turno del día, cuando el motor
# garantiza que la unidad está en una tile de acceso al shed (S1.1/S6.2) -> cero
# movimiento. Distinto del `fert_pickup` que falló: aquel caminaba al shed a media
# ruta y rompía la localidad de la serpentina.
# Diagnóstico que lo motiva: fresa 3.38 u/planta (máx 8) y tomate 3.5, contra
# melón 6.00 (máx 6). Los ongoing al 42%, los one-time al 100%.
CAMPEONA_FDL = dict(CAMPEONA_FB, fert_dawn_load=True, fert_tick_aligned=True)
campeona_fdl = make_agent(CAMPEONA_FDL)
CAMPEONA_FDL_NA = dict(CAMPEONA_FB, fert_dawn_load=True)   # sin tick_aligned, para separar
campeona_fdl_na = make_agent(CAMPEONA_FDL_NA)

# El trade al revés: si la fresa está saturada, el fertilizante vale MÁS vendido
# que usado ($85/u contra los ~$25 de la fresa marginal). No fertilizar nada.
CAMPEONA_NOFERT = dict(CAMPEONA_FB, fert_crops=[])
campeona_nofert = make_agent(CAMPEONA_NOFERT)
# Y la consecuencia: cada animal vale ~29 fertilizantes/temporada (~$2,400), muy
# por encima de su leche/lana marginal ($127 por 6 vacas). Rebaño por fertilizante.
CAMPEONA_HERD66 = dict(CAMPEONA_FB, animals=[("COW", 6), ("SHEEP", 6)])
campeona_herd66 = make_agent(CAMPEONA_HERD66)


# ============================================================================
# CAMPEONA_CARRERA — campeona 2026-08-31. CAMPEONA_FB sin piso de venta.
# ============================================================================
# El hallazgo: en un mercado COMPARTIDO en lockstep, aguantar inventario para no
# estrellar el precio se lo REGALA al rival. Evidencia directa: al subir nuestro
# pacing, el dinero de C95 subía monótono ($114.6k -> $116.3k -> $118.4k) mientras
# el nuestro bajaba. `sell_floor` decidía NO vender cuando el precio estaba bajo,
# y el rival vendía dentro del precio que nosotros sosteníamos.
# Es la misma conclusión a la que llegó el autor del notebook del meta: su
# maquinaria de reserve-price con forecast de drenaje del town está escrita y
# ENVIADA APAGADA (`_RESERVE = {}`, `_RACE_WEIGHT = 0.0`); lo único encendido es
# `_SORT_KEY='impact'`. Correr, no aguantar.
#
# EVIDENCIA (2026-08-31):
#   - head-to-head vs CAMPEONA_FB: 77-21-2 = 78.0% (IC95 [69%, 85%]), 100 eps,
#     con `_noop` leyendo 50.0% exacto y dinero idéntico al centavo.
#   - panel de cintas reales del ladder (5 rivales reconstruidos de nuestras
#     propias derrotas, 200 eps): +4.5 pts de win-rate, t=+2.23, positivo en 4/5
#     celdas y negativo en ninguna. Controles del panel: `_noop` +0.0 en las cinco,
#     `_peor` -18.5 (t=-3.32).
#   - dinero: $85,780 vs $84,462 (no es la vía; la ganancia es conversión de duelos).
# NOTA: la lente de dinero contra C95 daba solo +$506 (t=1.72) y casi se descarta.
# El Elo paga W/L/T, no margen: medir en win-rate contra panel diverso.
CAMPEONA_CARRERA = dict(CAMPEONA_FB, sell_floor=0)
campeona_carrera = make_agent(CAMPEONA_CARRERA)

# Re-medición sobre CAMPEONA_CARRERA con el panel válido: estos tres se
# descartaron con la lente de dinero vs C95, que acaba de demostrarse ciega.
CARRERA_CAP   = dict(CAMPEONA_CARRERA, crop_max={"STRAWBERRY": 8})
CARRERA_HINGE = dict(CAMPEONA_CARRERA, hinge_forecast=True)
CARRERA_FDL   = dict(CAMPEONA_CARRERA, fert_dawn_load=True, fert_tick_aligned=True)
carrera_cap   = make_agent(CARRERA_CAP)
carrera_hinge = make_agent(CARRERA_HINGE)
carrera_fdl   = make_agent(CARRERA_FDL)

# ============================================================================
# CAMPEONA_ALBA — campeona final 2026-08-31. CARRERA + carga de fertilizante al alba.
# ============================================================================
# El diagnóstico: ejecutábamos los cultivos ONE-TIME al 100% (melón 6.00 u/planta
# de 6) y los ONGOING al 42% (fresa 3.38 de 8, tomate 3.5 de 8). Causa: `_service_ops`
# gatea FERTILIZE en `has_fert`, y la unidad llegaba a la fresa con las manos
# vacías. NO es el `fert_pickup` que falló: aquel caminaba al shed A MEDIA RUTA y
# rompía la localidad de la serpentina. Aquí no hay viaje — por S1.1/S6.2 el motor
# GARANTIZA que al amanecer toda unidad está en una tile de acceso al shed, así que
# un solo PICKUP carga la cuota del día. Coste de movimiento: cero.
# EVIDENCIA: panel de cintas reales +15.5 pts (t=+3.70, 200 eps, positivo en 4/5
# celdas); head-to-head 90-10 = 90.0% vs CAMPEONA_CARRERA (IC95 [83%,94%], 100 eps)
# con `_noop` en 50.0% exacto; dinero $87,198 vs $80,541.
# Candidata: CARRERA + fert_dawn_load. Re-medida sobre el panel válido dio
# +15.5 pts (t=+3.70) — el mayor efecto medido. Con la lente de dinero vs C95
# había leído -$3,879 y se descartó: la caja baja (convierte fertilizante de $85
# en fresa de $25) pero los DUELOS suben, y el Elo paga duelos.
CAMPEONA_ALBA = dict(CAMPEONA_CARRERA, fert_dawn_load=True, fert_tick_aligned=True)
campeona_alba = make_agent(CAMPEONA_ALBA)
CAMPEONA_FDL2 = CAMPEONA_ALBA          # alias histórico
campeona_fdl2 = campeona_alba
CARRERA_NOOP = dict(CAMPEONA_CARRERA)
carrera_noop = make_agent(CARRERA_NOOP)

# --- Item 1: bundling de animales (2026-09-01) -------------------------------
# La cinta hace 203 paradas de 4 acciones productivas; nosotros 55. El servicio
# de animales es casi perfecto (191 de 208 animal-dias con las 3 ops: FEED+CARE+
# COLLECT); la cuarta que falta es HARVEST, bloqueada por animal_harvest_at=4:
# con CARE diario la vaca hace 3 leches/2d y la oveja 4 lanas/3d, asi que el
# umbral solo se cruza cada ~3 dias. La evolucion 2 ya prefirio harvest_at=1 en
# 7/9 finalistas; la 3 lo subio a 4 sin revisarlo despues.
ALBA_H1 = dict(CAMPEONA_ALBA, animal_harvest_at=1)
ALBA_H2 = dict(CAMPEONA_ALBA, animal_harvest_at=2)
alba_h1 = make_agent(ALBA_H1)
alba_h2 = make_agent(ALBA_H2)
ALBA_NOOP = dict(CAMPEONA_ALBA)
alba_noop = make_agent(ALBA_NOOP)

# --- Item 2: el rebaño, re-medido sobre el chasis nuevo (2026-09-01) ---------
# El item 1 falsó el bundling como palanca (harvest_at=1 movio la metrica de
# 1.53 a 1.54, no a 1.85) pero identifico la causa: las paradas de 4 acciones son
# PROPORCIONALES al rebaño, porque un animal solo tiene unidad que cosechar los
# dias que produce (vaca cada 2, oveja cada 3). La cinta: 14 animales -> 203
# paradas de 4. Nosotros: 8 -> 70.
# Prior BAJO y honesto: herd_demand se rechazo con 41.7-50% contra base 97.2% y
# _peor en 81.5% — cayo 31 puntos por DEBAJO del suelo, eso era daño real.
# Angulo nuevo: el chasis cambio debajo (fert_dawn_load hace que cada animal
# doble ticks de fresa; sell_floor=0 cambia la liquidacion).
ALBA_66   = dict(CAMPEONA_ALBA, animals=[("COW", 6), ("SHEEP", 6)])
ALBA_HERD = dict(CAMPEONA_ALBA, herd_demand=True, herd_max=14, herd_until=22)
alba_66   = make_agent(ALBA_66)
alba_herd = make_agent(ALBA_HERD)

# --- Cola de medicion 2026-09-01 (de las lentes cacheadas) --------------------
# fert_phase_lock: _fert_due acepta 9 edades seguidas en la fresa (8..16) cuando
#   solo pagan 2. Encima de fert_dawn_load, que fue la mayor ganancia del dia.
# idle_best_only: el fallback de idle_plant planta la PILA DE SEMILLAS MAS GRANDE
#   sin consultar al scorer — la misma incoherencia que fallback_fix.
# ============================================================================
# CAMPEONA_FASE — campeona 2026-09-01. ALBA + fert_phase_lock.
# ============================================================================
# `_fert_due` aceptaba NUEVE edades seguidas en la fresa (8..16) cuando solo DOS
# pagan. El motor (kaggriculture.py L777-800) tickea usando `next_day`, asi que
# el riego que cobra el x2 es el de la VISPERA del tick: edades 9,11,13,15 en
# fresa. Una aplicacion cubre hoy..hoy+2 -> fertilizar en 9 y en 13 cubre los
# CUATRO ticks con DOS aplicaciones. Antes se gastaban en edades que no cubrian
# ningun tick pagador.
# Verificado: fresa 9 edades -> [9, 13]; tomate 6 -> [7, 10].
# EVIDENCIA: panel de 5 cintas +8.0 pts (t=+2.75, 200 eps), positivo en las 5
# celdas; head-to-head 94-6 = 94.0% (IC95 [88%,97%], 100 eps) vs CAMPEONA_ALBA;
# `_noop` +0.0, `_peor` -38.5. Dinero $80,732 vs $76,476.
CAMPEONA_FASE = dict(CAMPEONA_ALBA, fert_phase_lock=True)
campeona_fase = make_agent(CAMPEONA_FASE)

ALBA_FPL  = dict(CAMPEONA_ALBA, fert_phase_lock=True)
ALBA_IBO  = dict(CAMPEONA_ALBA, idle_best_only=True)
alba_fpl  = make_agent(ALBA_FPL)
alba_ibo  = make_agent(ALBA_IBO)

# --- Lo que la auditoria de replays reales destapo (2026-09-01) ---------------
# En 43 partidas de campeona_alba: emitimos 11.0 ordenes BUY_ANIMAL y terminamos
# con 8.0 animales, con CERO estructuras vacias -> no escaparon (S4.6 deja la
# estructura en pie): las ordenes FALLAN EN SILENCIO. Ya estaba diagnosticado
# (order_funding descuenta la caja ya comprometida en el turno; animal_first pone
# el bloque del animal delante de las semillas) pero se midio contra una base al
# 97.2% —panel saturado, 108-0 sin margen— y quedo "en confirmacion", apagado.
FASE_OF   = dict(CAMPEONA_FASE, order_funding=True)
FASE_OFAF = dict(CAMPEONA_FASE, order_funding=True, animal_first=True)
fase_of   = make_agent(FASE_OF)
fase_ofaf = make_agent(FASE_OFAF)
FASE_NOOP = dict(CAMPEONA_FASE)
fase_noop = make_agent(FASE_NOOP)

# route_balance: arregla el bucket residual de _plan_routes. Hallazgo del usuario
# mirando repeticiones: el 4o peon queda 70-74% en PASS los dias 2-3. Medido en
# 15 replays reales y confirmado instrumentando el planificador: rutas [6,6,4,5,1]
# sobre 22 tiles. El corte se hacia DESPUES de añadir la tile que cruza el umbral,
# asi que la ultima ruta heredaba el sobrante de todos los redondeos.
FASE_RB = dict(CAMPEONA_FASE, route_balance=True)
fase_rb = make_agent(FASE_RB)

# ============================================================================
# CAMPEONA_RUTA — campeona 2026-09-01 (2). FASE + route_balance + order_funding
#                 + animal_first. GANA POR INTERACCION: las partes valen -4.5 y
#                 +5.5, el paquete +10.0.
# ============================================================================
# Dos bugs que se tapaban mutuamente:
#  · route_balance: `_plan_routes` cortaba DESPUES de añadir la tile que cruza el
#    umbral, asi que las primeras n-1 rutas se pasaban y la ULTIMA heredaba el
#    sobrante de todos los redondeos. Medido: rutas [6,6,4,5,1] sobre 22 tiles,
#    y el 4o peon 70-74% en PASS los dias 2-3 en 15 replays reales. Lo vio el
#    usuario mirando repeticiones. NO es work_steal (-1.5 sigma): aquel reasignaba
#    tiles DESPUES de rutear y rompia la localidad; esto arregla la particion
#    inicial conservando la contiguidad de la serpentina.
#  · order_funding + animal_first: emitiamos 11.0 ordenes BUY_ANIMAL y acabábamos
#    con 8.0 animales, con CERO estructuras vacias -> no escapaban (S4.6), las
#    ordenes fallaban EN SILENCIO por caja ya comprometida en el turno.
# Por que interactuan: route_balance le da trabajo al 4o peon, pero sin
# animal_first los animales no llegan y esa capacidad no tiene que hacer.
# EVIDENCIA: panel +10.0 pts (t=+2.49, 200 eps), supera a la base en las 5 celdas
# (85/100/90/80/100); head-to-head 78-22 = 78.0% vs CAMPEONA_FASE y 72-8 = 90.0%
# vs CAMPEONA_ALBA (la que esta subida); `_noop` +0.0, `_peor` -46.5.
CAMPEONA_RUTA = dict(CAMPEONA_FASE, route_balance=True, order_funding=True, animal_first=True)
campeona_ruta = make_agent(CAMPEONA_RUTA)

FASE_RB_AF = dict(CAMPEONA_FASE, route_balance=True, order_funding=True, animal_first=True)
fase_rb_af = make_agent(FASE_RB_AF)

# shed_hub: reservar las tiles de acceso al shed para estructuras de animal, y
# depositar (DROP) cuando la unidad esta ahi con carga vendible. Hallazgo de las
# 12 partidas del top-1 (tetsuya): ocupa 3.0 de 4 tiles de acceso con animales
# contra nuestra 1.0; sus unidades estan sobre el shed el 18.0% de los turnos de
# media jornada (nosotros 10.7%) y hacen 206 DROP/partida (nosotros 35), el 71%
# en un turno que tambien vende. La mercancia llega al mercado el MISMO dia.
RUTA_HUB = dict(CAMPEONA_RUTA, shed_hub=True, drop_deposit=True, drop_from_day=4)
ruta_hub = make_agent(RUTA_HUB)
RUTA_NOOP = dict(CAMPEONA_RUTA)
ruta_noop = make_agent(RUTA_NOOP)

# RUTA_FASES: la cadena completa del top-1, que solo funciona junta.
#   tierra d7/d10 -> rebaño PROGRESIVO hasta d13 -> estructuras sobre las tiles
#   de acceso al shed recien desbloqueadas -> la ruta de animales pasa por el
#   shed -> DROP gratis -> mercancia al mercado el MISMO dia.
# tetsuya arranca con ~$2,300 de animales el d0 (~5) y crece a 15.1.
RUTA_FASES = dict(CAMPEONA_RUTA, shed_hub=True, drop_deposit=True, drop_from_day=4,
                  animals=[("COW", 3), ("SHEEP", 2)],
                  herd_demand=True, herd_max=15, herd_until=14)
ruta_fases = make_agent(RUTA_FASES)

# animal_queue: arregla el `next()` sobre el dict `shed` que hacia que TODAS las
# estructuras vacias pidieran el mismo tipo de animal. Observado por el usuario en
# repeticiones ("la oveja del dia 1 no se coloca") y confirmado en 25 replays:
# oveja 17.1 turnos de espera contra 9.8 la vaca, 107 turnos-animal/partida.
RUTA_AQ = dict(CAMPEONA_RUTA, animal_queue=True)
ruta_aq = make_agent(RUTA_AQ)

# animal_urgent: PICKUP/PLACE de animal preempta la ruta. La causa real de la
# observacion del usuario: el ejecutor de rutas corre antes que la lista de
# tareas y consume todas las unidades, asi que el animal en el shed solo se
# atiende cuando una ruta se agota (medido: oveja 17.1 turnos, 12% mas de un dia).
RUTA_AU = dict(CAMPEONA_RUTA, animal_urgent=True)
ruta_au = make_agent(RUTA_AU)

# --- Ablacion leave-one-out sobre CAMPEONA_RUTA (2026-09-02) ------------------
# El panel de 40 rivales REALES no reproduce el de 5 cintas y si se parece al
# ladder. Hay que re-medir las cuatro adopciones con el instrumento bueno:
# apagar cada una por separado; si es real, apagarla debe BAJAR la puntuacion.
RUTA_SIN_SF  = dict(CAMPEONA_RUTA, sell_floor=0.4)
RUTA_SIN_FDL = dict(CAMPEONA_RUTA, fert_dawn_load=False, fert_tick_aligned=False)
RUTA_SIN_FPL = dict(CAMPEONA_RUTA, fert_phase_lock=False)
RUTA_SIN_PKG = dict(CAMPEONA_RUTA, route_balance=False, order_funding=False, animal_first=False)
ruta_sin_sf  = make_agent(RUTA_SIN_SF)
ruta_sin_fdl = make_agent(RUTA_SIN_FDL)
ruta_sin_fpl = make_agent(RUTA_SIN_FPL)
ruta_sin_pkg = make_agent(RUTA_SIN_PKG)

# --- Cola pendiente de la bitacora, medida con el panel de 40 (2026-09-02) ----
# buy_feed: no reservar tiles de cultivo para el forraje; comprarlo al mercado.
# Marcada como #1 de la cola y NUNCA medida. Aritmetica: 232 unidades de forraje
# = 290 tile-dias cultivandolo; comprarlas cuesta $5,800 y esos tile-dias rinden
# entre $7,250 y $32,770. Coincide con lo que hacen C95 (234 trigos comprados) y
# tetsuya (compra continua).
FASE_BF  = dict(CAMPEONA_FASE, buy_feed=True)
FASE_BF3 = dict(CAMPEONA_FASE, buy_feed=True, feed_days=3)
fase_bf  = make_agent(FASE_BF)
fase_bf3 = make_agent(FASE_BF3)
FASE_NOOP2 = dict(CAMPEONA_FASE)
fase_noop2 = make_agent(FASE_NOOP2)

# --- CUARENTENA re-medida con el panel de 40 (2026-09-02) --------------------
# BITACORA: "el bug solo producia FALSOS NEGATIVOS... en cuarentena (medidos solo
# en espejo): work_steal, fert_pickup, los recortes/ampliaciones de plantilla,
# sheep6/sheep8 y el desempate que descarto season_aware". Y linea 921: funding y
# season_aware se midieron en el panel escalera saturado con 2.9 pts de rango.
Q_WORKSTEAL = dict(CAMPEONA_FASE, work_steal=True)
Q_FERTPICK  = dict(CAMPEONA_FASE, fert_pickup=True)
Q_SEASON    = dict(CAMPEONA_FASE, season_aware=True)
Q_SHEEP6    = dict(CAMPEONA_FASE, animals=[("COW", 4), ("SHEEP", 6)])
Q_HANDS14   = dict(CAMPEONA_FASE, hands_cap=14)
q_worksteal = make_agent(Q_WORKSTEAL)
q_fertpick  = make_agent(Q_FERTPICK)
q_season    = make_agent(Q_SEASON)
q_sheep6    = make_agent(Q_SHEEP6)
q_hands14   = make_agent(Q_HANDS14)

# --- FUGAS TERMINALES medidas sobre 48 episodios (2026-09-03) ----------------
# Instrumento: estado final de la partida, no el replay. Dos fugas duras:
#   1) 40.3 semillas compradas y NUNCA sembradas = $2005/partida muertos
#      (MELON $867, STRAWBERRY $665). Causa: `deficit` es de tiles (global) pero
#      solo se descontaba el stock del `best` de hoy -> cada cambio de `best`
#      compra un lote nuevo para las mismas tiles.
#   2) 10.9 plantas COSECHABLES en pie al cerrar. Causa: el dia 29 el riego
#      pre-cosecha (prio 78) gana al HARVEST y exige una segunda visita.
FUGA_SEMILLA = dict(CAMPEONA_FASE, seed_stock_aware=True)
FUGA_SIEGA   = dict(CAMPEONA_FASE, endgame_reap=True)
FUGA_AMBAS   = dict(CAMPEONA_FASE, seed_stock_aware=True, endgame_reap=True)
fuga_semilla = make_agent(FUGA_SEMILLA)
fuga_siega   = make_agent(FUGA_SIEGA)
fuga_ambas   = make_agent(FUGA_AMBAS)

# --- CAMPEONA_GRANO (2026-09-03) --------------------------------------------
# `seed_stock_aware` ADOPTADO. Descubrimiento: +6.6 (t=+1.86, 160 pares, seeds
# 91000-91003). Confirmacion en semillas NUEVAS: +6.4 (t=+2.62, 320 pares,
# seeds 91100-91107). El efecto replico casi exacto -> no era winner's curse.
# `endgame_reap` NO se adopta: sd=0.0, la bandera nunca llega a morder (parche
# a la rama equivocada; las plantas en pie son continuas, no de un solo corte).
CAMPEONA_GRANO = dict(CAMPEONA_FASE, seed_stock_aware=True)
campeona_grano = make_agent(CAMPEONA_GRANO)
