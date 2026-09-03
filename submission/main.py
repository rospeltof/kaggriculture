"""Kaggriculture submission — generada por empaquetar.py.

Config: CAMPEONA_HOZ (campeón vigente de la evolución local; ver docs/BITACORA.md).
Chasis: bots/chassis.py inline (Python puro, sin dependencias).
"""

"""Chasis compartido de bots arquetipo.

Un arquetipo = configuración (qué plantar, qué animales, cuántos peones,
política de venta). El chasis resuelve cada turno: generación de tareas con
prioridades, asignación greedy unidad-más-cercana, logística de wheat para
FEED, órdenes de mercado y cierre de temporada.

Constantes verificadas contra el motor (docs/RULES.md S3.9, S4.x).
"""
import math

CROP = {
    "WHEAT":      dict(seed=10,  first=2,  peak=4,  win=(2, 4),  last_plant=25, ongoing=False),
    "CARROT":     dict(seed=20,  first=2,  peak=3,  win=(2, 3),  last_plant=26, ongoing=False),
    "MELON":      dict(seed=80,  first=10, peak=10, win=(6, 12), last_plant=19, ongoing=False),
    "TOMATO":     dict(seed=50,  first=8,  peak=None, iv=1, last_plant=21, ongoing=True),
    "STRAWBERRY": dict(seed=100, first=10, peak=None, iv=2, last_plant=19, ongoing=True),
}
ANIMAL = {
    "GOOSE": dict(cost=300, structure="COOP",    first=4, iv=1, cap=4, prod="EGG"),
    "COW":   dict(cost=400, structure="PASTURE", first=8, iv=2, cap=6, prod="MILK"),
    "SHEEP": dict(cost=500, structure="PASTURE", first=6, iv=3, cap=6, prod="WOOL"),
}
SELLABLE = ["WOOL", "MILK", "MELON", "STRAWBERRY", "EGG", "TOMATO", "CARROT", "WHEAT", "FERTILIZER"]
PREMIUM = {"WOOL", "MILK", "MELON", "STRAWBERRY"}

# Espejo verificado de la curva de precios del motor (RULES.md S5.1, motor v1.32.7):
# (base, T, below_func, below_target, above_func, above_target)
MKT = {
    "WHEAT":      (25, 400, "sqrt", 0.80, "log", 0.20),
    "CARROT":     (35, 450, "hinge", 1.00, "sqrt", 0.70),
    "TOMATO":     (60, 200, "hinge", 0.40, "sqrt", 0.60),
    "STRAWBERRY": (120, 100, "sqrt", 0.70, "linear", 1.60),
    "MELON":      (250, 300, "log", 0.20, "sq", 3.60),
    "EGG":        (50, 332, "hinge", 0.40, "log", 0.20),
    "MILK":       (160, 122, "sqrt", 0.60, "linear", 1.60),
    "WOOL":       (200, 105, "log", 0.20, "sq", 3.20),
    "FERTILIZER": (100, 200, "linear", 0.40, "linear", 0.40),
}
# (unidades al pico sin fert, días de ocupación de la tile aprox)
CROP_ECON = {"WHEAT": (4, 5), "CARROT": (3, 4), "MELON": (6, 11), "TOMATO": (4, 13), "STRAWBERRY": (4, 18)}

BASE_PRICE = {"WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120, "MELON": 250,
              "EGG": 50, "MILK": 160, "WOOL": 200, "FERTILIZER": 100}

# Demanda del town (verificada S7.1): cada tienda consume 1 de cada producto suyo
# cada 4 turnos (x2 si es mono-producto) = 6 o 12/día; el town center 1/día.
SHOP_DEMANDS = {
    "BAKERY": ("EGG", "WHEAT"),
    "PIZZA_SHOP": ("MILK", "TOMATO", "WHEAT"),
    "BRUNCH_SPOT": ("EGG", "WHEAT", "STRAWBERRY"),
    "YARN_STORE": ("WOOL",),
    "ICE_CREAM_SHOP": ("STRAWBERRY", "MILK", "WHEAT"),
    "PET_CAFE": ("CARROT",),
    "SMOOTHIE_SHOP": ("STRAWBERRY", "MILK"),
    "FARMERS_MARKET": ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY"),
}


def _town_drain_per_day(town, item):
    drain = 1  # town center
    for shop in (town or {}).get("unlocked_shops", []) or []:
        prods = SHOP_DEMANDS.get(shop, ())
        if item in prods:
            drain += 12 if len(prods) == 1 else 6
    return drain


def _fshape(f, x, T):
    if f == "linear":
        return x
    if f == "sq":
        return x * x
    if f == "sqrt":
        return math.sqrt(x)
    if f == "log":
        return math.log(1.0 + x)
    if f == "hinge":
        u = x / T
        return u + 8.0 * max(0.0, u - 1.0) ** 2
    return x


def _avg_price_over(crop, inv_start, qty):
    """Precio medio REALIZADO vendiendo qty unidades desde inv_start (integral
    discreta de la curva). En curvas 'sq' (melón/lana) el promedio de la ráfaga
    queda muy por debajo del marginal — el sesgo que infló al melón."""
    if qty <= 0:
        return _price_at(crop, inv_start)
    n = min(int(qty), 12) or 1
    chunk = qty / n
    return sum(_price_at(crop, inv_start + chunk * (i + 0.5)) for i in range(n)) / n


def _price_at(crop, inv):
    """Precio del motor si el inventario de mercado fuera `inv` (floor $1)."""
    base, T, bf, bt, af, at_ = MKT[crop]
    if inv < 10000:
        amp = bt * base / _fshape(bf, T, T)
        p = base + amp * _fshape(bf, 10000 - inv, T)
    else:
        amp = at_ * base / _fshape(af, T, T)
        p = base - amp * _fshape(af, inv - 10000, T)
    return max(1.0, p)
SHED = (4, 4)
SHED_ACCESS = ((4, 4), (5, 4), (4, 5), (5, 5))
LAST_DAY = 29


def _dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# ---------- Router (opción B, fase 1): planear la jornada al amanecer ----------
# El día es la unidad natural: al alba todo se resetea y el 95% del trabajo se
# conoce. Las tiles con servicio se ordenan en serpentina (ruta de cortacésped),
# se parten en trozos de costo balanceado (uno por unidad) y cada unidad ejecuta
# su ruta haciendo TODO lo pendiente de cada tile antes de moverse (bundling).
_ROUTER_STATE = {}


def _router_state(player, step):
    st = _ROUTER_STATE.setdefault(player, {"last_step": -1})
    if step == 0 or step < st.get("last_step", -1):
        st.clear()
        st["last_step"] = -1
    st["last_step"] = step
    return st


def _plantables(empty_tiles, farm, cfg):
    """Tiles donde SI se puede plantar. Con shed_hub, las de acceso al shed
    quedan reservadas para COOP/PASTURE."""
    if not cfg.get("shed_hub"):
        return empty_tiles
    libres = [t for t in empty_tiles if t not in SHED_ACCESS]
    return libres or empty_tiles          # nunca bloquear del todo el plantado


def _plan_routes(serve, n_units, tiles, balance=False):
    """serve: [(x, y, costo)] -> rutas por unidad. Serpentina espacial, corte por
    costo acumulado, y dentro de cada ruta los animales primero (están cerca del
    shed, donde la unidad amanece y recoge su wheat)."""
    serve = sorted(serve, key=lambda t: (t[0], t[1] if t[0] % 2 == 0 else -t[1]))
    total = sum(c for _, _, c in serve) or 1.0
    target = total / max(1, n_units)
    if balance:
        # BUG del bucket residual (observado por el usuario en replays reales: el
        # 4o peon 70-74% en PASS los dias 2-3). El corte de abajo se hace DESPUES
        # de añadir la tile que cruza el umbral, asi que cada una de las primeras
        # n-1 rutas se PASA del objetivo y la ultima hereda el sobrante acumulado
        # de todos los redondeos: medido [6,6,4,5,1] sobre 22 tiles, y [.,.,.,.,0]
        # el dia 1. Aqui la tile se asigna por su coste ACUMULADO PREVIO, que
        # reparte el residuo entre todas y conserva la contiguidad de la
        # serpentina (no es work_steal: no se reasigna nada despues de rutear).
        routes = [[] for _ in range(max(1, n_units))]
        acc = 0.0
        for x, y, c in serve:
            idx = min(n_units - 1, int(acc / target)) if target > 0 else 0
            routes[idx].append((x, y))
            acc += c
    else:
        routes, cur, acc = [], [], 0.0
        for x, y, c in serve:
            cur.append((x, y))
            acc += c
            if acc >= target and len(routes) < n_units - 1:
                routes.append(cur)
                cur, acc = [], 0.0
        routes.append(cur)
        while len(routes) < n_units:
            routes.append([])

    def is_animal(t):
        cell = tiles[t[1]][t[0]]
        return isinstance(cell, dict) and cell.get("animal")

    return [sorted(r, key=lambda t: 0 if is_animal(t) else 1) for r in routes]



def _fert_due(c, age, cfg):
    """¿Vale la pena fertilizar HOY esta planta? Alineado a los ticks reales:
    la ventana del fertilizante dura 3 días (hoy, +1, +2), así que aplicarlo en
    edad tick-2..tick cubre ese tick. Sin alineación se gastaba una aplicación
    desde edad first-2 que a veces no cubría ningún tick."""
    if not cfg.get("fert_tick_aligned"):
        return age >= c["first"] - 2
    if not c["ongoing"]:
        return c["first"] - 2 <= age <= c["peak"]
    iv = max(1, c.get("iv", 1))
    if cfg.get("fert_phase_lock"):
        # La ventana tick-2..tick acepta NUEVE edades seguidas en la fresa (8..16)
        # cuando solo DOS pagan. El motor (L777-800) tickea usando next_day, asi
        # que el riego que cobra el x2 es el de la VISPERA del tick: edades 9,11,
        # 13,15 en fresa y 7,8,9,10 en tomate. Una aplicacion cubre hoy..hoy+2,
        # asi que fertilizar en la edad `first-1` y luego cada `step` cubre el
        # maximo de ticks por aplicacion: fresa 9 y 13, tomate 7 y 10.
        base = c["first"] - 1
        step = iv * (2 // iv + 1)
        ult = base + iv * 3          # max_yield = 4 ticks en ambos ongoing
        return base <= age <= ult and (age - base) % step == 0
    for k in range(4):
        tick = c["first"] + k * iv
        if tick - 2 <= age <= tick:
            return True
    return False



def _animal_score(animal, day, town, market_inv, mine, opp, cfg):
    """$/tile-día esperado de comprar ESTE animal hoy — mismo modelo de valor
    que el scorer de cultivos (la lección del fallback_fix: dos caminos de
    decisión con dos economías distintas es como se plantan zanahorias con la
    fresa a 6x).

    Tres cosas que el rebaño fijo 4+4 nunca vio:
      · EGG es el ÚNICO producto con curva de glut logarítmica: +400 unidades
        lo dejan en ~$40. WOOL se hunde al piso con +59 y MILK con +76. Por eso
        oveja y vaca se auto-estrangulan al escalar y el ganso no.
      · El sumidero del town varía 15x entre partidas (la lana va de 30 a 750
        unidades de temporada según cuántos YARN_STORE salgan) y nosotros
        producíamos 111 siempre.
      · La oferta del RIVAL compite por el mismo sumidero.
    """
    a = ANIMAL[animal]
    item = a["prod"]
    dias = LAST_DAY - day
    if dias <= a["first"]:
        return -1e9                      # no alcanza a producir ni una vez
    ticks = (dias - a["first"]) // max(1, a["iv"]) + 1
    unidades = ticks * 1.0
    if unidades <= 0:
        return -1e9
    # oferta que ya presiona ese mercado: la nuestra en pie + la visible del rival
    supply = (mine.get(animal, 0) + opp.get(animal, 0)) * ticks
    # Horizonte del drenaje: restar el consumo del town de TODA la temporada
    # finge una escasez que no existe cuando vendo (el scorer de cultivos usa la
    # ocupación del cultivo, no los 30 días). Con el horizonte largo el modelo
    # veía leche a precio de oro y compraba 14 vacas en monocultivo.
    horizonte = min(dias, cfg.get("herd_drain_days", 8))
    inv = market_inv.get(item, 10000) - _town_drain_per_day(town, item) * horizonte
    precio = _avg_price_over(item, inv + supply, unidades)
    # coste: estructura + animal + forraje de los días que quedan
    forraje = dias * cfg.get("feed_cost", 34)
    neto = unidades * precio - a["cost"] - forraje
    return neto / max(1, dias)


def _herd_target(day, town, market_inv, mine, opp, cfg):
    """¿Cuál es el siguiente animal que conviene, si alguno? Devuelve None
    cuando ninguno paga: a diferencia de sheep6/sheep8 (que solo sabían SUBIR),
    esto puede quedarse quieto cuando el town no demanda."""
    mejor, mejor_s = None, cfg.get("herd_min_score", 0.0)
    for animal in ("GOOSE", "COW", "SHEEP"):
        s = _animal_score(animal, day, town, market_inv, mine, opp, cfg)
        if s > mejor_s:
            mejor, mejor_s = animal, s
    return mejor


def _water_pays(c, tile, age, day):
    """¿El riego de HOY compra algo, o sólo evita la muerte?

    Motor (kaggriculture.py L428-444 y L777-800):
      - one-time: la acción WATER suma +1 al instante sólo si win[0] <= edad <= peak.
      - ongoing: el tick nocturno suma +1 SIEMPRE; el x2 exige `was_watered` Y
        fertilizada. El tick del refresh de hoy usa `next_day`, así que el riego
        que paga es el de la VÍSPERA del tick: edad+1-first múltiplo del intervalo.
      - muerte: sólo con consecutive_unwatered >= 2 -> se puede regar día por medio.
    Fuera de esos casos el riego rinde exactamente 0.
    """
    if tile.get("consecutive_unwatered", 0) >= 1:
        return True  # saltarlo hoy la mata esta noche
    if not c["ongoing"]:
        lo, hi = c["win"]
        return lo <= age <= hi
    iv = max(1, c.get("iv", 1))
    ds = age + 1 - c["first"]
    return (ds >= 0 and ds % iv == 0
            and tile.get("fertilized_until_day", -1) >= day)


def _service_ops(tile, day, cfg, has_fert=False):
    """Próxima acción pendiente en esta tile del circuito, o None si está servida."""
    if not isinstance(tile, dict):
        return None
    kind = tile.get("kind")
    if kind == "WEED":
        return ["DIG"]
    if kind == "PLANT":
        c = CROP[tile["crop"]]
        age = day - tile["planted_day"]
        yu = tile.get("yield_units", 0)
        watered = tile.get("watered_today")
        # fertilizar ANTES de regar (el bonus x2 aplica al riego del mismo día);
        # solo si la unidad carga fertilizer (has_fert) y el cultivo lo amerita
        if ((has_fert or cfg.get("fert_pickup")) and tile["crop"] in cfg.get("fert_crops", ())
                and day <= 26 and tile.get("fertilized_until_day", -1) < day
                and _fert_due(c, age, cfg)):
            return ["FERTILIZE"]
        # DIA FINAL = SIEGA. Aqui WATER se evalua ANTES que HARVEST y retorna de
        # inmediato: el dia 29 una planta con rendimiento y sin regar se REGABA
        # (bonus que ya no hay manana para cobrar) en vez de cosecharse, y la de
        # un corte con age < peak no entraba nunca en la rama de HARVEST.
        # Medido: $1994/partida en pie al cerrar (fresa $692, trigo $419,
        # zanahoria $395, tomate $296, melon $192).
        if cfg.get("endgame_reap") and day >= LAST_DAY and yu > 0 and age >= c["first"]:
            return ["HARVEST"]
        if not watered and day <= LAST_DAY:
            if not (not c["ongoing"] and age > c["peak"]) and not (
                    day == LAST_DAY and not (age >= c["first"] and yu > 0)):
                if not cfg.get("water_cadence") or _water_pays(c, tile, age, day):
                    return ["WATER"]
        if yu > 0 and age >= c["first"]:
            if not c["ongoing"]:
                if age >= c["peak"] and (watered or age > c["peak"] or day == LAST_DAY):
                    return ["HARVEST"]
            elif yu >= 2 or day >= 28:
                return ["HARVEST"]
        return None
    if kind in ("COOP", "PASTURE") and tile.get("animal"):
        a = ANIMAL[tile["animal"]]
        h_at = cfg.get("animal_harvest_at", 2)
        if cfg.get("endgame") and day >= 26:
            h_at = 1
        yu = tile.get("yield_units", 0)
        if not tile.get("fed_today") and day <= 28:
            return ["FEED"]
        if cfg.get("care") and tile.get("fed_today") and not tile.get("cared_today") and day <= 27:
            return ["CARE"]
        if yu >= min(h_at, a["cap"] - 1) or (yu >= 1 and day >= 28):
            return ["HARVEST"]
        if cfg.get("collect_fert") and tile.get("fertilizer_available"):
            return ["COLLECT_FERTILIZER"]
    return None


_SERVICE_OPS = {"WATER", "FEED", "CARE", "HARVEST", "COLLECT_FERTILIZER", "DIG"}


def _step_toward(pos, target):
    dx, dy = target[0] - pos[0], target[1] - pos[1]
    if dx == 0 and dy == 0:
        return None
    if abs(dx) >= abs(dy):
        return "EAST" if dx > 0 else "WEST"
    return "SOUTH" if dy > 0 else "NORTH"


def make_agent(cfg):
    def agent(obs):
        return decide(obs, cfg)
    return agent


def decide(obs, cfg):
    p = obs["player"]
    farm = obs["farms"][p]
    tiles = farm["tiles"]
    day, hour = obs["day"], obs["hour"]
    priv = obs["private"]
    shed = priv.get("shed", {}) or {}
    seeds = priv.get("seeds", {}) or {}
    money = farm["money"]
    market_inv = obs["market"]["inventory"]
    market_prices = obs["market"]["prices"]
    town = obs.get("town", {}) or {}

    # Lectura de la granja rival (pública, con planted_day): su oferta futura por
    # cultivo, y las "olas anunciadas" (barnyard-economist, sección 12).
    # Revisión adversarial 2026-09-02 — tres correcciones sobre la v1 ingenua:
    #  (a) la ventana no tiene piso: una tile MADURA sigue en el tablero hasta que
    #      el rival la cosecha, y el dump ocurre en/después del pico (la v1 con
    #      to_peak>=0 se apagaba justo el día de la venta);
    #  (b) se agrupa por planted_day: un BLOQUE sincronizado es un anuncio fechado,
    #      el goteo estacionario no (la v1 marcaba ola el 46-54% de los turnos
    #      porque la ventana cubre el 75% de la vida del carrot);
    #  (c) el umbral es por VALOR entrante, no por número de tiles (5 carrots = $525
    #      es ruido; 5 melones = $7,500 es una amenaza).
    opp_incoming = {}
    wave_soon = set()
    if cfg.get("opp_read") or cfg.get("beat_wave"):
        ofarm = obs["farms"][1 - p]
        blocks = {}
        for _row in ofarm["tiles"]:
            for _tc in _row:
                if not (isinstance(_tc, dict) and _tc.get("kind") == "PLANT"):
                    continue
                c2 = _tc.get("crop")
                if c2 not in CROP_ECON:
                    continue
                cd2 = CROP[c2]
                pd2 = _tc.get("planted_day", 0)
                age2 = day - pd2
                # oferta fantasma fuera: lo que no alcanza a rendir antes del cierre
                if pd2 + cd2["first"] > LAST_DAY:
                    continue
                if cd2["ongoing"]:
                    # solo los ticks que faltan (los ya producidos ya están en su shed
                    # o vendidos, y el pipeline propio los ve por el inventario)
                    done = max(0, (age2 - cd2["first"]) // max(1, cd2["iv"]) + 1) if age2 >= cd2["first"] else 0
                    units2 = max(0, CROP_ECON[c2][0] - done)
                else:
                    units2 = CROP_ECON[c2][0]
                opp_incoming[c2] = opp_incoming.get(c2, 0) + units2
                if not cd2["ongoing"] and cd2["peak"] - age2 <= 2:
                    key2 = (c2, pd2)
                    blocks[key2] = blocks.get(key2, 0) + 1
        if cfg.get("beat_wave"):
            min_val = cfg.get("wave_min_value", 2000)
            for (c3, _pd3), n3 in blocks.items():
                if n3 * CROP_ECON[c3][0] * BASE_PRICE.get(c3, 0) >= min_val:
                    wave_soon.add(c3)

    unit_pos = [tuple(farm["farmer"])] + [tuple(h) for h in farm["hands"]]
    invs = list(priv.get("inventories", [{}]))
    while len(invs) < len(unit_pos):
        invs.append({})
    n_units = len(unit_pos)

    # Perillas de política ("el cerebro" es buscable): prioridades del scheduler.
    ph = cfg.get("prio_harvest", 62)
    pw = cfg.get("prio_water", 50)
    p_urg = cfg.get("prio_urgency", 25)
    p_win = cfg.get("prio_win_bonus", 12)
    p_feed = cfg.get("prio_feed", 88)
    p_care = cfg.get("prio_care", 46)
    p_plant = cfg.get("prio_plant", 40)

    router_on = bool(cfg.get("router"))
    serve_tiles = []
    rst = None
    plan_stale = False
    if router_on:
        rst = _router_state(p, obs.get("step", day * 24 + hour))
        plan_stale = rst.get("day") != day

    # ---- escaneo del tablero -> tareas (prio, (x, y), op) ----
    tasks = []
    hungry = 0            # animales sin alimentar hoy
    empty_tiles = []
    # SHED HUB: las tiles de acceso al shed son de las ESTRUCTURAS, no del plantador.
    # El top-1 (tetsuya) ocupa 3.0 de 4 con animales; nosotros 1.0. Consecuencia
    # medida en sus replays: sus unidades estan sobre el shed el 18.0% de los
    # turnos de media jornada contra nuestro 10.7%, y hacen 206 DROP/partida
    # contra nuestros 35 — el 71% en un turno que TAMBIEN vende. Atender animales
    # les pasa por el shed, asi que el DROP sale gratis y la mercancia llega al
    # mercado el MISMO dia en vez del siguiente (S5.3).
    my_structures = {"COOP": 0, "PASTURE": 0}   # incluye ocupadas
    empty_structs = []    # (x, y, kind)
    planted_count = {}

    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            if tile == "LOCKED":
                continue
            if tile is None:
                empty_tiles.append((x, y))
                continue
            kind = tile.get("kind")
            if kind == "WEED":
                if router_on:
                    serve_tiles.append((x, y, 1.0))
                tasks.append((cfg.get("prio_dig", 8), (x, y), ["DIG"]))
                continue
            if kind == "PLANT":
                if router_on:
                    serve_tiles.append((x, y, 1.5))
                crop = tile["crop"]
                c = CROP[crop]
                planted_count[crop] = planted_count.get(crop, 0) + 1
                age = day - tile["planted_day"]
                watered = tile["watered_today"]
                yu = tile.get("yield_units", 0)
                urgency = p_urg if hour >= 16 else 0
                if not c["ongoing"]:
                    ready = age >= c["peak"]
                    overdue = age > c["peak"]
                    # El dia final NO hay manana: el bonus del riego pre-cosecha
                    # ya no se puede cobrar y el HARVEST solo aparece dentro de
                    # `ready`, asi que un cultivo de un corte con rendimiento pero
                    # age < peak se REGABA y no se cosechaba nunca. Medido: $1006
                    # por partida en trigo/zanahoria/melon en pie al cerrar.
                    _siega = (cfg.get("endgame_reap") and day >= LAST_DAY
                              and yu > 0 and age >= c["first"])
                    if _siega:
                        tasks.append((95, (x, y), ["HARVEST"]))
                    elif ready:
                        if not watered and not overdue and day <= LAST_DAY:
                            tasks.append((78, (x, y), ["WATER"]))     # riego pre-cosecha (bonus del día pico)
                        elif yu > 0 and age >= c["first"]:
                            tasks.append((85 if overdue else ph, (x, y), ["HARVEST"]))
                    elif not watered:
                        in_win = c["win"][0] <= age <= c["win"][1]
                        prio = pw + (p_win if in_win else 0) + urgency
                        if tile.get("consecutive_unwatered", 0) >= 1:
                            prio += 20
                        if day == LAST_DAY and not (age >= c["first"] and yu > 0):
                            continue  # día final: no regar lo que no se cosecha hoy
                        tasks.append((prio, (x, y), ["WATER"]))
                else:
                    if not watered and day < LAST_DAY:
                        prio = pw + urgency + (20 if tile.get("consecutive_unwatered", 0) >= 1 else 0)
                        tasks.append((prio, (x, y), ["WATER"]))
                    if yu > 0 and age >= c["first"]:
                        if cfg.get("endgame_reap") and day >= LAST_DAY:
                            # fresa/tomate en pie al cerrar: $988 por partida
                            tasks.append((95, (x, y), ["HARVEST"]))
                        elif yu >= 3 or day >= 28:
                            tasks.append((ph + 10, (x, y), ["HARVEST"]))
                        elif yu >= 2:
                            tasks.append((ph - 10, (x, y), ["HARVEST"]))
                continue
            if kind in ("COOP", "PASTURE"):
                my_structures[kind] += 1
                animal = tile.get("animal")
                if not animal:
                    empty_structs.append((x, y, kind))
                    continue
                a = ANIMAL[animal]
                yu = tile.get("yield_units", 0)
                if router_on:
                    serve_tiles.append((x, y, 3.0))
                if not tile.get("fed_today") and day <= 28:
                    hungry += 1
                    tasks.append((p_feed + (6 if hour >= 16 else 0), (x, y), ["FEED"]))
                if cfg.get("care") and tile.get("fed_today") and not tile.get("cared_today") and day <= 27:
                    tasks.append((p_care, (x, y), ["CARE"]))
                h_at = cfg.get("animal_harvest_at", 2)
                if cfg.get("endgame") and day >= 26:
                    h_at = 1  # cierre: no acumular producto en el animal
                if yu >= a["cap"] - 1:
                    tasks.append((ph + 12, (x, y), ["HARVEST"]))
                elif yu >= h_at or (yu >= 1 and day >= 28):
                    tasks.append((ph - 8, (x, y), ["HARVEST"]))
                if cfg.get("collect_fert") and tile.get("fertilizer_available"):
                    tasks.append((cfg.get("fert_prio", 18), (x, y), ["COLLECT_FERTILIZER"]))

    # ---- construcción de estructuras pendientes del plan ----
    want_structs = {"COOP": 0, "PASTURE": 0}
    if cfg.get("herd_demand"):
        # con el rebaño dirigido por demanda, la lista fija cfg["animals"] ya no
        # manda: las estructuras se derivan de los animales que REALMENTE
        # tenemos (en tile, en shed o en mano) más un hueco de margen para el
        # siguiente. Sin esto un GOOSE comprado no tendría COOP donde vivir —
        # nunca habíamos construido uno.
        tengo = {"COOP": 0, "PASTURE": 0}
        for row in tiles:
            for t in row:
                if isinstance(t, dict) and t.get("animal"):
                    tengo[ANIMAL[t["animal"]]["structure"]] += 1
        pend = {"COOP": 0, "PASTURE": 0}
        for an, n in shed.items():
            if an in ANIMAL:
                pend[ANIMAL[an]["structure"]] += n
        for i in range(n_units):
            for k, n in invs[i].items():
                if k in ANIMAL:
                    pend[ANIMAL[k]["structure"]] += n
        # el margen solo se abre para la estructura del animal que el scorer
        # elegiría hoy, para no sembrar el mapa de pastures vacías
        siguiente = _herd_target(day, town, market_inv, {}, {}, cfg) if day <= cfg.get("herd_until", 22) else None
        for kind in ("COOP", "PASTURE"):
            margen = 1 if (siguiente and ANIMAL[siguiente]["structure"] == kind) else 0
            want_structs[kind] = tengo[kind] + pend[kind] + margen
    else:
        for animal, count in cfg.get("animals", []):
            want_structs[ANIMAL[animal]["structure"]] += count
    for kind in ("COOP", "PASTURE"):
        deficit = want_structs[kind] - my_structures[kind]
        if cfg.get("phased") and deficit > 0:
            # construir solo con el animal a la vista: animales ya adquiridos de este
            # tipo de estructura + 2 de margen — no gastar tiles en pastures vacías
            acquired = sum(1 for row in tiles for t in row
                           if isinstance(t, dict) and t.get("animal")
                           and ANIMAL[t["animal"]]["structure"] == kind)
            acquired += sum(n for an, n in shed.items()
                            if an in ANIMAL and ANIMAL[an]["structure"] == kind)
            deficit = min(deficit, max(0, acquired + 2 - my_structures[kind]))
        if deficit > 0 and empty_tiles and day <= 24:
            spots = sorted(empty_tiles, key=lambda t: _dist(t, SHED))[:deficit]
            for s in spots:
                tasks.append((64, s, ["BUILD_COOP" if kind == "COOP" else "BUILD_PASTURE"]))
                empty_tiles.remove(s)

    # ---- colocar animales comprados (están en el shed) ----
    carriers = {i for i in range(n_units) if any(k in ANIMAL for k in invs[i])}
    # COLA DE ANIMALES (animal_queue). `next()` sobre `shed` tomaba el PRIMERO en
    # orden del dict, asi que con {COW: 2, SHEEP: 1} los tres pastos vacios pedian
    # COW y la oveja no recibia orden hasta agotar las vacas. Medido en 25 replays
    # reales: la oveja espera 17.1 turnos de media contra 9.8 la vaca, el 12% de
    # los animales pasa mas de un DIA entero en el shed y se pierden 107
    # turnos-animal por partida. Es capital muerto: $500 sin producir, y como
    # `placed_day` fija todo el calendario de la rampa (S4.9), cruzar la
    # medianoche cuesta una tanda entera. Aqui se descuenta lo ya reclamado, asi
    # que cada estructura vacia pide un animal DISTINTO.
    _cola = {an: n for an, n in shed.items() if an in ANIMAL and n > 0} if cfg.get("animal_queue") else None
    if empty_structs:
        for x, y, kind in empty_structs:
            if _cola is not None:
                match = next((an for an in _cola if ANIMAL[an]["structure"] == kind and _cola[an] > 0), None)
                if match:
                    _cola[match] -= 1
            else:
                match = next((an for an in shed if an in ANIMAL and ANIMAL[an]["structure"] == kind and shed[an] > 0), None)
            carrier_has = next((i for i in carriers if any(ANIMAL.get(k, {}).get("structure") == kind for k in invs[i])), None)
            if carrier_has is not None:
                an = next(k for k in invs[carrier_has] if k in ANIMAL)
                tasks.append((66, (x, y), ["PLACE", an, 1]))
            elif match:
                tasks.append((65, SHED, ["PICKUP", match, 1]))

    # ---- plantar: plan fijo, o adaptativo a los precios del mercado ----
    plant_claims = {}
    adaptive_best, adaptive_need = None, 0
    # El deficit que dispara la compra es de TILES (global, cualquier cultivo),
    # pero se descontaba solo el stock del `best` de HOY. Cada vez que `best`
    # cambia, el lote anterior deja de contar y se compra uno nuevo para las
    # MISMAS tiles: medido, 40.3 semillas sobrantes y $2005 muertos por partida.
    _seed_stock = sum(n for cr, n in seeds.items()
                      if cr in CROP and day <= CROP[cr]["last_plant"])
    far = not cfg.get("plant_near")
    # regla de oro (phased): nunca plantar más de lo que la plantilla puede regar
    plant_cap = 10 ** 9
    if cfg.get("phased"):
        plant_cap = n_units * cfg.get("tiles_per_unit", 5)
    if cfg.get("adaptive"):
        # score = $/tile-día esperado, con el precio evaluado en el inventario
        # actual MÁS nuestro propio pipeline sin vender (no inundar el mercado).
        budget = cfg.get("crop_tiles", sum(cfg.get("plants", {}).values()))
        deficit = budget - sum(planted_count.values())
        # 1) piso de wheat: el rebaño come 1 wheat/día/animal; comprarlo cuesta
        #    ~10x más que cultivarlo. Cubrir la demanda interna antes de especular.
        herd = sum(n for _, n in cfg.get("animals", []))
        # buy_feed: NO reservar tiles para el forraje. La premisa original
        # ("comprarlo cuesta ~10x mas que cultivarlo") mira la CAJA e ignora la
        # TIERRA: 8 animales x 29 dias = 232 unidades = 58 plantas = 290 TILE-DIAS.
        # Comprarlas cuesta $5,800; esos tile-dias rinden $7,250 (fresa al margen)
        # a $32,770 (melon). Idea marcada como #1 de la cola pendiente en la
        # bitacora y nunca medida. El forraje se compra en el bloque de mercado.
        wheat_floor = 0 if cfg.get("buy_feed") else min(
            cfg.get("wheat_floor", herd), max(0, budget // 3))
        wheat_gap = 0
        if day <= CROP["WHEAT"]["last_plant"]:
            wheat_gap = max(0, wheat_floor - planted_count.get("WHEAT", 0))
        # 2) resto del budget: mejor $/tile-día, precio evaluado al MARGEN —
        #    inventario + 2x nuestro pipeline (el rival vende parecido) + esta tile.
        best, best_s = None, -1e9
        for crop, (u, occ) in CROP_ECON.items():
            if day > CROP[crop]["last_plant"]:
                continue
            u_eff = u
            if cfg.get("scorer_v2") and crop in cfg.get("fert_crops", ()) and crop in ("STRAWBERRY", "TOMATO"):
                u_eff = 7  # ticks x2 con fertilizer (el fert es gratis del rebaño)
            if cfg.get("season_aware"):
                # Rendimiento REAL según los días que quedan de temporada. El
                # scorer miope valoraba una fresa del día 18 igual que una del
                # día 5, pero la primera solo alcanza 1 tick de 4: en la derrota
                # vs Akshay V teníamos 50 tiles de fresa y vendimos 130 unidades
                # contra sus 265 — mismas tiles, mitad de cosecha, porque
                # llegamos tarde. Aquí un cultivo que no alcanza a rendir se
                # devalúa solo, y los de ciclo largo valen más TEMPRANO.
                cdx = CROP[crop]
                if cdx["ongoing"]:
                    first_day = day + cdx["first"]
                    ticks = 0 if first_day > LAST_DAY else min(
                        u, (LAST_DAY - first_day) // max(1, cdx["iv"]) + 1)
                    if crop in cfg.get("fert_crops", ()):
                        ticks *= 2   # fertilizado, cada tick rinde 2
                    u_eff = ticks
                else:
                    if day + cdx["peak"] > LAST_DAY:
                        dias_utiles = LAST_DAY - day - cdx["first"]
                        u_eff = 0 if dias_utiles < 0 else max(0, min(u, 1 + dias_utiles))
            pipeline = planted_count.get(crop, 0) * u_eff + shed.get(crop, 0)
            opp = cfg.get("mkt_opp_factor", 2)
            supply = int(opp * pipeline)
            if cfg.get("opp_read"):
                # oferta rival OBSERVADA (sus tiles públicas) en vez del factor ciego
                supply = pipeline + opp_incoming.get(crop, 0)
            proj_inv = market_inv.get(crop, 10000)
            if cfg.get("town_forecast"):
                # el town drenará inventario hasta la cosecha -> precio proyectado sube
                _hz = occ
                if cfg.get("hinge_forecast") and MKT.get(crop, (0,0,""))[2] == "hinge":
                    # CARROT/TOMATO/EGG usan la curva `hinge` del parche 1.32.7
                    # (RULES S5.1): bajo el codo es lineal, pasado el codo el precio
                    # se dispara al cuadrado. Nadie las ofrece — ni nosotros ni la
                    # cinta del meta, cuya tabla _MP es ANTERIOR al parche y las
                    # valora mal. Como el déficit sólo crece mientras nadie ofrece,
                    # el precio relevante no es el de la cosecha sino el del CIERRE.
                    _hz = max(occ, LAST_DAY - day)
                proj_inv -= _town_drain_per_day(town, crop) * _hz
            if cfg.get("scorer_v2"):
                # precio medio de vender la RÁFAGA completa (pipeline + esta tile)
                price = _avg_price_over(crop, proj_inv, supply + u_eff)
            else:
                price = _price_at(crop, proj_inv + supply + u_eff)
            s = (u_eff * price - CROP[crop]["seed"]) / occ
            if s > best_s:
                best, best_s = crop, s
        # tope concurrente genérico por cultivo (crop_max) — misma disciplina que
        # melon_max, pero para los premium cuya curva toca el piso de $1 a ~+100
        # unidades (fresa/lana/leche): producir por encima del drenaje del town
        # rinde ~$1/unidad. Se resuelve reutilizando la rama del fallback.
        _cmax = cfg.get("crop_max") or {}
        if best is not None and _cmax.get(best) and planted_count.get(best, 0) >= _cmax[best]:
            best = None if best != "MELON" else best
            if best is None:
                _blocked = [c for c in _cmax if planted_count.get(c, 0) >= _cmax[c]]
                b2, b2s = None, -1e9
                for crop2, (u2, occ2) in CROP_ECON.items():
                    if crop2 in _blocked or day > CROP[crop2]["last_plant"]:
                        continue
                    cd2 = CROP[crop2]
                    ue2 = u2
                    if cfg.get("season_aware"):
                        if cd2["ongoing"]:
                            fd2 = day + cd2["first"]
                            tk2 = 0 if fd2 > LAST_DAY else min(
                                u2, (LAST_DAY - fd2) // max(1, cd2["iv"]) + 1)
                            if crop2 in cfg.get("fert_crops", ()):
                                tk2 *= 2
                            ue2 = tk2
                        elif day + cd2["peak"] > LAST_DAY:
                            du2 = LAST_DAY - day - cd2["first"]
                            ue2 = 0 if du2 < 0 else max(0, min(u2, 1 + du2))
                    pipe2 = planted_count.get(crop2, 0) * ue2 + shed.get(crop2, 0)
                    sup2 = pipe2 + opp_incoming.get(crop2, 0) if cfg.get("opp_read") else int(
                        cfg.get("mkt_opp_factor", 2) * pipe2)
                    pi2 = market_inv.get(crop2, 10000)
                    if cfg.get("town_forecast"):
                        pi2 -= _town_drain_per_day(town, crop2) * occ2
                    pr2 = _price_at(crop2, pi2 + sup2 + ue2)
                    s2 = (ue2 * pr2 - CROP[crop2]["seed"]) / occ2
                    if s2 > b2s:
                        b2, b2s = crop2, s2
                best, best_s = b2, b2s
        if cfg.get("melon_max") and best == "MELON" and planted_count.get("MELON", 0) >= cfg["melon_max"]:
            # melón al tope concurrente (acota la ola de cosecha y la cantidad total
            # de temporada — la curva sq hace que el melón marginal >~120u valga poco):
            # elegir el segundo mejor cultivo
            # El fallback DEBE puntuar con el mismo modelo que el scorer principal.
            # Antes usaba unidades crudas (sin season_aware ni el x2 del fertilizante)
            # y ahí la fresa se hundía bajo la oferta rival y ganaba el carrot:
            # medido en la partida vs Omkar Kadam, 44 carrots a $42 el día 11 con
            # la fresa a $186 y cero tiles nuestras de fresa.
            second, second_s = None, -1e9
            for crop2, (u2, occ2) in CROP_ECON.items():
                if crop2 == "MELON" or day > CROP[crop2]["last_plant"]:
                    continue
                if not cfg.get("fallback_fix"):
                    pipe0 = planted_count.get(crop2, 0) * u2 + shed.get(crop2, 0)
                    if cfg.get("opp_read"):
                        pipe0 += opp_incoming.get(crop2, 0)
                    pr0 = _price_at(crop2, market_inv.get(crop2, 10000) + pipe0 + u2)
                    s0 = (u2 * pr0 - CROP[crop2]["seed"]) / occ2
                    if s0 > second_s:
                        second, second_s = crop2, s0
                    continue
                cd2 = CROP[crop2]
                ue2 = u2
                if cfg.get("scorer_v2") and crop2 in cfg.get("fert_crops", ()) and crop2 in ("STRAWBERRY", "TOMATO"):
                    ue2 = 7
                if cfg.get("season_aware"):
                    if cd2["ongoing"]:
                        fd2 = day + cd2["first"]
                        tk2 = 0 if fd2 > LAST_DAY else min(u2, (LAST_DAY - fd2) // max(1, cd2["iv"]) + 1)
                        if crop2 in cfg.get("fert_crops", ()):
                            tk2 *= 2
                        ue2 = tk2
                    elif day + cd2["peak"] > LAST_DAY:
                        du2 = LAST_DAY - day - cd2["first"]
                        ue2 = 0 if du2 < 0 else max(0, min(u2, 1 + du2))
                pipe2 = planted_count.get(crop2, 0) * ue2 + shed.get(crop2, 0)
                sup2 = int(cfg.get("mkt_opp_factor", 2) * pipe2)
                if cfg.get("opp_read"):
                    sup2 = pipe2 + opp_incoming.get(crop2, 0)
                inv2 = market_inv.get(crop2, 10000)
                if cfg.get("town_forecast"):
                    inv2 -= _town_drain_per_day(town, crop2) * occ2
                if cfg.get("scorer_v2"):
                    pr2 = _avg_price_over(crop2, inv2, sup2 + ue2)
                else:
                    pr2 = _price_at(crop2, inv2 + sup2 + ue2)
                s2 = (ue2 * pr2 - CROP[crop2]["seed"]) / occ2
                if s2 > second_s:
                    second, second_s = crop2, s2
            best = second
        adaptive_best = best
        for crop, n_want in (("WHEAT", min(wheat_gap, deficit)), (best, deficit - min(wheat_gap, deficit))):
            if not crop or n_want <= 0:
                continue
            if crop == "MELON" and cfg.get("melon_max"):
                n_want = min(n_want, max(0, cfg["melon_max"] - planted_count.get("MELON", 0)))
                if n_want <= 0:
                    continue
            n = min(n_want, seeds.get(crop, 0) - plant_claims.get(crop, 0), len(empty_tiles))
            for _ in range(max(0, n)):
                _pool = _plantables(empty_tiles, farm, cfg)
                if not _pool:
                    break
                spot = (max if far else min)(_pool, key=lambda t: _dist(t, SHED))
                empty_tiles.remove(spot)
                tasks.append((p_plant + (4 if crop == "WHEAT" else 0), spot, ["PLANT", crop]))
                plant_claims[crop] = plant_claims.get(crop, 0) + 1
        _held = _seed_stock if cfg.get("seed_stock_aware") else (seeds.get(best, 0) if best else 0)
        adaptive_need = max(0, wheat_gap - seeds.get("WHEAT", 0)) if wheat_gap else (
            max(0, deficit - _held) if best else 0)
        if wheat_gap:
            adaptive_best = "WHEAT"
    else:
        for crop, target in cfg.get("plants", {}).items():
            c = CROP[crop]
            if day > c["last_plant"]:
                continue
            deficit = target - planted_count.get(crop, 0)
            avail_seeds = seeds.get(crop, 0)
            room = plant_cap - sum(planted_count.values()) - sum(plant_claims.values())
            n = min(deficit, avail_seeds, len(empty_tiles), max(0, room))
            for _ in range(max(0, n)):
                _pool = _plantables(empty_tiles, farm, cfg)
                if not _pool:
                    break
                spot = (max if far else min)(_pool, key=lambda t: _dist(t, SHED))
                empty_tiles.remove(spot)
                tasks.append((p_plant + (4 if crop == "WHEAT" else 0), spot, ["PLANT", crop]))
                plant_claims[crop] = plant_claims.get(crop, 0) + 1

    # ---- reinversión ("grow"): plantar toda tile vacía con el mejor cultivo vigente ----
    if cfg.get("grow") and day <= 26 and empty_tiles:
        best = next((c for c in ("MELON", "STRAWBERRY", "CARROT", "WHEAT") if day <= CROP[c]["last_plant"]), None)
        if best:
            avail = seeds.get(best, 0) - plant_claims.get(best, 0)
            for _ in range(min(avail, len(empty_tiles))):
                spot = min(empty_tiles, key=lambda t: _dist(t, SHED))
                empty_tiles.remove(spot)
                tasks.append((cfg.get("prio_plant", 40) - 2, spot, ["PLANT", best]))
                plant_claims[best] = plant_claims.get(best, 0) + 1

    # ---- router: (re)planear la jornada y suprimir tareas ya ruteadas ----
    if router_on:
        if plan_stale:
            hire_limit = 29 if cfg.get("hire_late") else 27
            exp_hands = cfg.get("hands", 0)
            if cfg.get("hands_per_quadrant"):
                exp_hands = min(cfg["hands_per_quadrant"] * len(farm["unlocked_quadrants"]),
                                cfg.get("hands_cap", 12))
            n_expected = 1 + (exp_hands if day <= hire_limit else 0)
            rst["day"] = day
            rst["routes"] = _plan_routes(serve_tiles, max(n_expected, n_units), tiles,
                                         balance=bool(cfg.get("route_balance")))
            rst["idx"] = [0] * len(rst["routes"])
        routed_pending = set()
        for i, rt in enumerate(rst.get("routes", [])):
            start = rst["idx"][i] if i < len(rst.get("idx", [])) else 0
            routed_pending.update(tuple(t) for t in rt[start:])
        tasks = [t for t in tasks if not (t[1] in routed_pending and t[2][0] in _SERVICE_OPS)]

    # ---- asignación: greedy global, o zonificada si cfg["zoning"] ----
    # Zonificación: las tiles activas (no LOCKED) se parten en bloques contiguos,
    # uno por unidad; cada unidad atiende primero su bloque. Tareas cuya zona
    # está ocupada solo escalan a cualquier unidad si prio >= zone_fallback_prio.
    zone_owner = {}
    if cfg.get("zoning"):
        active = [(x, y) for y in range(len(tiles)) for x in range(len(tiles[y])) if tiles[y][x] != "LOCKED"]
        block = max(1, -(-len(active) // n_units))
        for idx, t in enumerate(active):
            zone_owner[t] = min(n_units - 1, idx // block)
    zone_fallback = cfg.get("zone_fallback_prio", 70)

    tasks.sort(key=lambda t: -t[0])
    actions = [None] * n_units
    used_tiles = set()
    wheat_needed = hungry  # unidades de FEED sin wheat encima haran fetch

    # ---- cierre de temporada: llevar la carga al shed ANTES de que acabe el juego ----
    # (el auto-drop nocturno del día 29 es inútil: ya no hay turnos para vender)
    if cfg.get("endgame") and day >= 28:
        shed_tiles = {(4, 4), (5, 4), (4, 5), (5, 5)}
        for i in range(n_units):
            tot = sum(invs[i].values())
            if tot >= 3 or (day == 29 and hour >= 16 and tot > 0):
                if unit_pos[i] in shed_tiles:
                    actions[i] = ["DROP"]
                else:
                    actions[i] = [_step_toward(unit_pos[i], SHED)]

    # ---- ANIMAL URGENTE: un animal en el shed es capital muerto -------------
    # El ejecutor de rutas corre ANTES que la lista de tareas y consume todas las
    # unidades, asi que PICKUP/PLACE de animal (que viven en la lista) solo se
    # atienden cuando a alguien se le acaba la ruta. Medido en 25 replays reales:
    # la oveja espera 17.1 turnos y la vaca 9.8; el 12% pasa mas de un DIA entero
    # en el shed; 107 turnos-animal perdidos por partida. Y como `placed_day` fija
    # todo el calendario de la rampa de CARE (S4.9), cruzar la medianoche cuesta
    # una tanda entera de produccion. Aqui se preempta la ruta, igual que hace el
    # bloque de cierre de temporada.
    if cfg.get("animal_urgent") and empty_structs:
        _pend = {an: n for an, n in shed.items() if an in ANIMAL and n > 0}
        _libres = list(empty_structs)
        for i in range(n_units):
            if actions[i] is not None or not _libres:
                continue
            _mio = next((k for k in invs[i] if k in ANIMAL), None)
            if _mio:                                   # ya lo lleva: colocarlo
                _dest = next((t for t in _libres
                              if t[2] == ANIMAL[_mio]["structure"]), None)
                if _dest is None:
                    continue
                _libres.remove(_dest)
                if unit_pos[i] == (_dest[0], _dest[1]):
                    actions[i] = ["PLACE", _mio, 1]
                else:
                    actions[i] = [_step_toward(unit_pos[i], (_dest[0], _dest[1]))]
            elif _pend and unit_pos[i] in {(4, 4), (5, 4), (4, 5), (5, 5)}:
                _an = next((a for a in _pend
                            if _pend[a] > 0 and any(t[2] == ANIMAL[a]["structure"]
                                                    for t in _libres)), None)
                if _an:
                    _pend[_an] -= 1
                    actions[i] = ["PICKUP", _an, 1]

    # ---- logística matinal multi-feeder: repartir el wheat del shed entre varios
    # alimentadores en paralelo. Con rebaños grandes, un solo feeder cargando todo
    # el wheat tarda más de un día en alimentar 15 animales (causa de los escapes
    # del writeup y del colapso del clon de "ln"). Al alba todos están en el shed.
    # ---- ejecutor de rutas: cada unidad sirve su circuito con bundling ----
    if router_on:
        shed_adj = {(4, 4), (5, 4), (4, 5), (5, 5)}
        routes = rst.get("routes", [])
        idxs = rst.get("idx", [])
        # work stealing: una unidad que acabó su circuito toma tiles pendientes de
        # los circuitos más cargados. Sin esto, la unidad con ruta corta se queda
        # PARADA el resto del día (medido: 20 turnos con 17 PASS en (4,4), d2-d3).
        if cfg.get("work_steal"):
            for i in range(min(n_units, len(routes))):
                if idxs[i] < len(routes[i]):
                    continue
                donante, resto = -1, 0
                for j in range(min(n_units, len(routes))):
                    if j == i:
                        continue
                    pend = len(routes[j]) - idxs[j]
                    if pend > resto:
                        donante, resto = j, pend
                if donante >= 0 and resto >= 2:
                    # le quita la MITAD de lo que le queda al más cargado
                    corte = len(routes[donante]) - resto // 2
                    routes[i] = routes[i] + routes[donante][corte:]
                    routes[donante] = routes[donante][:corte]

        # ---- carga de fertilizante al ALBA (coste de movimiento CERO) ----------
        # El doblado de ticks fallaba por LOGÍSTICA, no por scoring: la unidad
        # llega a la fresa con las manos vacías y `_service_ops` no puede emitir
        # FERTILIZE (está gateado en has_fert). Resultado medido: fresa 3.38 u/planta
        # contra 8.08 de la cinta, y tomate 3.5 — los ongoing al 42% de su potencial
        # mientras el melón (one-time, sin fertilizante) va al 100%.
        # Esto NO es el `fert_pickup` que falló: aquel caminaba al shed A MEDIA RUTA
        # y rompía la localidad de la serpentina (el mismo modo de fallo que mató a
        # work_steal). Aquí no hay viaje: por S1.1/S6.2 el motor garantiza que al
        # amanecer TODAS las unidades están en una tile de acceso al shed, así que
        # un solo PICKUP carga la cuota del día entero.
        if cfg.get("fert_dawn_load") and shed.get("FERTILIZER", 0) > 0:
            if rst.get("fl_day") != day:
                rst["fl_day"] = day
                rst["fl_done"] = set()
            done = rst.setdefault("fl_done", set())
            for i in range(min(n_units, len(routes))):
                if actions[i] is not None or i in done:
                    continue
                if unit_pos[i] not in shed_adj:
                    continue
                done.add(i)
                if invs[i].get("FERTILIZER", 0) > 0:
                    continue
                need = 0
                for ax, ay in routes[i][idxs[i]:]:
                    t2 = tiles[ay][ax]
                    if not (isinstance(t2, dict) and t2.get("crop") in cfg.get("fert_crops", ())):
                        continue
                    if t2.get("fertilized_until_day", -1) >= day:
                        continue
                    if _fert_due(CROP[t2["crop"]], day - t2["planted_day"], cfg):
                        need += 1
                if need > 0:
                    actions[i] = ["PICKUP", "FERTILIZER",
                                  min(need, shed["FERTILIZER"])]

        for i in range(min(n_units, len(routes))):
            if actions[i] is not None:
                continue
            route = routes[i]
            while idxs[i] < len(route):
                tx, ty = route[idxs[i]]
                op = _service_ops(tiles[ty][tx], day, cfg, invs[i].get("FERTILIZER", 0) > 0)
                if op is None:
                    idxs[i] += 1
                    continue
                if op[0] == "FERTILIZE" and invs[i].get("FERTILIZER", 0) <= 0:
                    if cfg.get("fert_pickup") and shed.get("FERTILIZER", 0) > 0:
                        rem = sum(1 for ax, ay in route[idxs[i]:]
                                  if isinstance(tiles[ay][ax], dict)
                                  and tiles[ay][ax].get("crop") in cfg.get("fert_crops", ()))
                        if unit_pos[i] in shed_adj:
                            actions[i] = ["PICKUP", "FERTILIZER",
                                          min(max(1, rem), shed["FERTILIZER"])]
                        else:
                            actions[i] = [_step_toward(unit_pos[i], SHED)]
                        break
                    idxs[i] += 1
                    continue
                if op[0] == "FEED" and invs[i].get("WHEAT", 0) <= 0:
                    if shed.get("WHEAT", 0) > 0:
                        rem = sum(1 for ax, ay in route[idxs[i]:]
                                  if isinstance(tiles[ay][ax], dict) and tiles[ay][ax].get("animal"))
                        if unit_pos[i] in shed_adj:
                            actions[i] = ["PICKUP", "WHEAT", min(max(1, rem), shed["WHEAT"])]
                        else:
                            actions[i] = [_step_toward(unit_pos[i], SHED)]
                        break
                    idxs[i] += 1  # sin wheat en ninguna parte: saltar este animal
                    continue
                if unit_pos[i] == (tx, ty):
                    actions[i] = op
                else:
                    actions[i] = [_step_toward(unit_pos[i], (tx, ty))]
                break

    if cfg.get("multi_feeder") and not router_on and hungry > 3 and hour <= 2:
        mf_shed_tiles = {(4, 4), (5, 4), (4, 5), (5, 5)}
        shed_wheat = shed.get("WHEAT", 0)
        n_feeders = min(max(1, -(-hungry // 5)), n_units)
        share = max(1, -(-hungry // n_feeders))
        assigned = 0
        for i in range(n_units):
            if assigned >= n_feeders or shed_wheat <= 0:
                break
            if actions[i] is None and invs[i].get("WHEAT", 0) == 0 and unit_pos[i] in mf_shed_tiles:
                take = min(share, shed_wheat)
                actions[i] = ["PICKUP", "WHEAT", take]
                shed_wheat -= take
                assigned += 1

    for prio, pos, op in tasks:
        if pos in used_tiles and op[0] not in ("PICKUP",):
            continue
        need_wheat = op[0] == "FEED"
        need_animal = op[1] if op[0] == "PLACE" and len(op) > 1 else None
        cands = []
        for i in range(n_units):
            if actions[i] is not None:
                continue
            if need_wheat and invs[i].get("WHEAT", 0) <= 0:
                continue
            if need_animal and invs[i].get(need_animal, 0) <= 0:
                continue  # PLACE solo al que carga el animal (antes fallaba en silencio)
            cands.append((_dist(unit_pos[i], pos), i))
        if zone_owner and cands:
            zoned = [c for c in cands if zone_owner.get(pos, -1) == c[1]]
            if zoned:
                cands = zoned
            elif prio < zone_fallback:
                continue  # la zona está ocupada y la tarea no amerita sacar a nadie de la suya
        if not cands and need_wheat and shed.get("WHEAT", 0) > 0:
            # nadie carga wheat: la unidad libre más cercana al shed va a buscarlo
            free = [(_dist(unit_pos[i], SHED), i) for i in range(n_units) if actions[i] is None]
            if free:
                _, i = min(free)
                if unit_pos[i] == SHED or _dist(unit_pos[i], SHED) == 0:
                    actions[i] = ["PICKUP", "WHEAT", max(1, min(wheat_needed, shed.get("WHEAT", 0)))]
                else:
                    actions[i] = [_step_toward(unit_pos[i], SHED)]
                used_tiles.add(pos)
            continue
        if not cands:
            continue
        _, i = min(cands)
        if unit_pos[i] == pos:
            actions[i] = list(op)
        else:
            actions[i] = [_step_toward(unit_pos[i], pos)]
        used_tiles.add(pos)

    # trabajo infinito: peón ocioso + tile vacía + semilla disponible = PLANTA.
    # (el budget capa el plan, pero el ocio con tierra y semillas es inaceptable)
    if cfg.get("idle_plant") and day <= 26:
        _MOV = {"NORTH", "SOUTH", "EAST", "WEST"}
        for i in range(n_units):
            if not empty_tiles:
                continue
            a_i = actions[i]
            libre = a_i is None
            if not libre and cfg.get("idle_plant_walkers") and a_i and a_i[0] in _MOV:
                # va de camino: si tiene una tile vacía AL LADO y semilla, planta
                # antes (medido d12: 16 tiles vacías con 42 semillas en el bolsillo
                # porque idle_plant solo miraba unidades sin acción)
                cerca = min((t for t in empty_tiles), key=lambda t: _dist(unit_pos[i], t), default=None)
                libre = cerca is not None and _dist(unit_pos[i], cerca) <= cfg.get("idle_plant_radius", 1)
            if not libre:
                continue
            crop = None
            # El fallback "planta la pila de semillas mas grande" no consulta al
            # scorer: es la misma incoherencia que fallback_fix mato en el camino
            # del melon (dos caminos de decision con dos economias). Gateado.
            _cands = ([adaptive_best] if adaptive_best else [])
            if not cfg.get("idle_best_only"):
                _cands = _cands + sorted(seeds, key=lambda k: -seeds.get(k, 0))
            for cand in _cands:
                if (cand and cand in CROP and day <= CROP[cand]["last_plant"]
                        and seeds.get(cand, 0) - plant_claims.get(cand, 0) > 0):
                    crop = cand
                    break
            if not crop:
                break
            _pool = _plantables(empty_tiles, farm, cfg)
            if not _pool:
                break
            spot = min(_pool, key=lambda t: _dist(unit_pos[i], t))
            empty_tiles.remove(spot)
            if unit_pos[i] == spot:
                actions[i] = ["PLANT", crop]
                plant_claims[crop] = plant_claims.get(crop, 0) + 1
            else:
                actions[i] = [_step_toward(unit_pos[i], spot)]

    # ---- depósito oportunista: cerrar la latencia de un día ------------------
    # El único DROP del chasis estaba en el endgame (día>=28). Antes de eso todo
    # lo cosechado espera al auto-drop nocturno (S6.3) y sólo es vendible a h0 del
    # día SIGUIENTE. Pero S5.3 (sonda P3) está verificada: las acciones de unidad
    # se procesan antes que el mercado, así que DROP en el turno T ya es vendible
    # por una orden SELL del MISMO turno T. Esto no es una política de precio:
    # elimina una latencia, así que compone con cualquier política de venta.
    # No es el "fetch" de fertilizante que falló (aquel PAGABA viaje hacia el shed):
    # aquí la unidad ya está en una tile de acceso y la acción sustituida ya era
    # PASS o un paso suelto. Es la forma que sobrevivió en el C72 del meta
    # (1 paso / valor 2000; los umbrales 500/1000 y 2 pasos perdieron 0-8).
    if cfg.get("drop_deposit") and day >= cfg.get("drop_from_day", 8):
        _shed_tiles = {(4, 4), (5, 4), (4, 5), (5, 5)}
        _MOVES = {"NORTH", "SOUTH", "EAST", "WEST"}
        _minval = cfg.get("drop_value", 2000)
        if cfg.get("shed_hub"):
            _minval = cfg.get("drop_value_hub", 200)
        for i in range(n_units):
            a_i = actions[i]
            if not (a_i is None or a_i == ["PASS"] or (a_i and a_i[0] in _MOVES)):
                continue
            if unit_pos[i] not in _shed_tiles:
                continue
            val = sum(invs[i].get(k, 0) * market_prices.get(k, 0)
                      for k in invs[i] if k in SELLABLE)
            if val >= _minval:
                actions[i] = ["DROP"]

    for i in range(n_units):
        if actions[i] is None:
            actions[i] = ["PASS"]

    # ---- órdenes de mercado (max 10; las ventas primero financian compras) ----
    orders = []
    wheat_buffer = 0
    if day <= 28:
        placed = sum(1 for row in tiles for t in row
                     if isinstance(t, dict) and t.get("animal"))
        wheat_buffer = min(2 * placed, 20)
    hold_day = cfg.get("premium_hold_day", 0)   # aguantar premium hasta este día
    floor_frac = cfg.get("sell_floor", 0)       # no vender bajo este % del precio base
    shed_load = sum(shed.values())
    sellable = []
    for it in SELLABLE:
        n = shed.get(it, 0) - (wheat_buffer if it == "WHEAT" else 0)
        if it == "FERTILIZER" and (cfg.get("fert_pickup") or cfg.get("fert_dawn_load")) and day <= 26:
            # reservar el fertilizante para los cultivos que lo duplican
            n -= min(cfg.get("fert_reserve", 20), sum(
                1 for row in tiles for t2 in row
                if isinstance(t2, dict) and t2.get("crop") in cfg.get("fert_crops", ())))
        if (cfg.get("hinge_hold") and MKT.get(it, (0,0,""))[2] == "hinge"
                and day < cfg.get("hinge_hold_day", 27) and shed_load < 85
                and _town_drain_per_day(town, it) > 1):
            # Al revés que en los premium: aquí el mercado está en DÉFICIT y sólo
            # el town lo profundiza, así que aguantar sube el precio y no le regala
            # nada al rival (no tiene stock de esto). Sólo con tienda real
            # (drain > 1 = hay una tienda, no sólo el town center).
            continue
        cap_load = 95 if (cfg.get("smart_overflow") and it in PREMIUM) else 85
        if (floor_frac and it != "FERTILIZER" and day < 28 and shed_load < cap_load
                and it not in wave_soon
                and market_prices.get(it, 0) < floor_frac * BASE_PRICE.get(it, 100)):
            continue  # mercado estrellado: aguantar; el town drena y el precio se recupera
        if it == "MELON" and cfg.get("melon_max") and it not in wave_soon:
            n = min(n, 12)  # pacing: acotar la caminata por la curva en cada orden
        if (cfg.get("sell_marginal") and it in MKT and day < 28
                and shed_load < 85 and it not in wave_soon):
            # PACING MARGINAL. sell_floor sólo decide SI vender, mirando el precio
            # ACTUAL; la orden sigue llevando todo el stock y somos nosotros los
            # que estrellamos la curva. Medido en autopsia: 162 unidades/partida
            # a <=30% del base. Aquí acotamos n para que la unidad MARGINAL siga
            # cobrando por encima del piso; el resto espera al drenaje del town
            # (S7.1) que repone el precio. Es el mismo bucle que _plan_sells de
            # C95 (que el autor dejó dormido: su cinta ya trae el schedule a mano;
            # un planner reactivo como el nuestro sí lo necesita).
            _inv0 = market_inv.get(it, 10000)
            _resv = cfg.get("sell_marginal_floor", 0.5) * BASE_PRICE.get(it, 100)
            _k = 0
            while _k < n and _price_at(it, _inv0 + _k) >= _resv:
                _k += 1
            n = _k
        if n > 0:
            sellable.append((it, n))
    if cfg.get("sell_rank"):
        # defender la posición en la cola lockstep: primero el producto cuya
        # cotización más se daña al vender n unidades (curvas sq/linear frágiles)
        # daño TOTAL en dólares (unitario x volumen), no caída unitaria: la curva
        # sq del melón es casi plana cerca de I0, y por fragilidad unitaria el
        # rubro más valioso quedaba fuera del cupo de la cola (hallazgo revisor).
        def _damage(kv):
            it2, n2 = kv
            if it2 in MKT:
                inv2 = market_inv.get(it2, 10000)
                return n2 * (_price_at(it2, inv2) - _price_at(it2, inv2 + n2))
            return 0.0
        sellable.sort(key=lambda kv: -_damage(kv))
    else:
        sellable.sort(key=lambda kv: -kv[1])
    sell_cap = 8 if (cfg.get("endgame") and day >= 28) else 4
    # el cupo es de 10 órdenes/turno y las extras se descartan EN SILENCIO (S5.5):
    # reservar sitio para los HIRE del cierre, que si no se perdían (hallazgo revisor)
    if cfg.get("order_budget") and hour <= 3 and day <= (29 if cfg.get("hire_late") else 27):
        _n_h = cfg.get("hands", 0)
        if cfg.get("hands_per_quadrant"):
            _n_h = min(cfg["hands_per_quadrant"] * len(farm["unlocked_quadrants"]), cfg.get("hands_cap", 12))
        sell_cap = max(2, min(sell_cap, 10 - max(0, min(_n_h - len(farm["hands"]), 6))))
    for it, n in sellable[:sell_cap]:
        orders.append(["SELL", it, n])

    if hour <= 3 and day <= (29 if cfg.get("hire_late") else 27):
        n_h = cfg.get("hands", 0)
        hpq = cfg.get("hands_per_quadrant", 0)
        if hpq:  # staffing al ritmo del territorio (el patrón de los top: 4/cuadrante)
            n_h = min(hpq * len(farm["unlocked_quadrants"]), cfg.get("hands_cap", 12))
        if cfg.get("hire_by_work"):
            # Staffing al ritmo del TRABAJO, no del territorio. La cinta del meta
            # corre 1-3 peones los días 1-5 y 10-14 en el pico (media 8.3); nosotros
            # 4 y luego 12 planos (media ~11). Cada peón de más paga el commute
            # desde el shed (S1.1: todos reaparecen en el acceso al shed cada alba)
            # sin trabajo que amortice el viaje: ahí está el exceso de ~950 pasos
            # medido contra la cinta. Una planta = 1 servicio/día; un animal = ~3
            # (FEED+CARE+COLLECT, y HARVEST cada tantos).
            _plants = _animals = 0
            for _row in farm["tiles"]:
                for _t in _row:
                    if not isinstance(_t, dict):
                        continue
                    if _t.get("kind") == "PLANT":
                        _plants += 1
                    elif _t.get("animal"):
                        _animals += 1
            _work = _plants + 3 * _animals
            _tpu = max(1, cfg.get("tiles_per_unit", 5))
            n_h = max(1, min(cfg.get("hands_cap", 12),
                             -(-_work // _tpu) - 1))  # -1 = el granjero ya trabaja
        missing = n_h - len(farm["hands"])
        for _ in range(max(0, min(missing, 6))):  # por tandas: no comerse el cupo de órdenes
            orders.append(["HIRE"])

    # Caja COMPROMETIDA en este mismo turno. El motor procesa las órdenes en
    # secuencia y cada guard miraba `money` sin descontar lo ya encolado, así
    # que las semillas se comían la caja del animal y el BUY_ANIMAL se
    # rechazaba en silencio (medido: 26% de ellos). Con order_funding cada
    # compra consulta la caja REALMENTE disponible.
    _committed = [0.0]

    def _afford(cost, buf=0):
        if not cfg.get("order_funding"):
            return money > cost + buf
        return money - _committed[0] > cost + buf

    def _commit(cost):
        if cfg.get("order_funding"):
            _committed[0] += cost

    def _bloque_animal():
        owned = {}
        for row in tiles:
            for t in row:
                if isinstance(t, dict) and t.get("animal"):
                    owned[t["animal"]] = owned.get(t["animal"], 0) + 1
        for an in shed:
            if an in ANIMAL:
                owned[an] = owned.get(an, 0) + shed[an]
        for i in range(n_units):
            for k in invs[i]:
                if k in ANIMAL:
                    owned[k] = owned.get(k, 0) + invs[i][k]
        owned_total = sum(owned.values())
        feed_secure = (not cfg.get("phased")) or (
            planted_count.get("WHEAT", 0) + shed.get("WHEAT", 0) >= owned_total + 1)
        if cfg.get("herd_demand"):
            if (owned_total < cfg.get("herd_max", 14) and feed_secure
                    and cfg.get("herd_from", 0) <= day <= cfg.get("herd_until", 22)):
                opp_an = {}
                _rival = obs["farms"][1 - obs["player"]]
                for row in (_rival.get("tiles") or []):
                    for t in row:
                        if isinstance(t, dict) and t.get("animal"):
                            opp_an[t["animal"]] = opp_an.get(t["animal"], 0) + 1
                elegido = _herd_target(day, town, market_inv, owned, opp_an, cfg)
                if elegido and _afford(ANIMAL[elegido]["cost"], cfg.get("cash_buffer", 200)):
                    orders.append(["BUY_ANIMAL", elegido, 1])
                    _commit(ANIMAL[elegido]["cost"])
                    return True
            return False
        for animal, count in cfg.get("animals", []):
            a = ANIMAL[animal]
            if (owned.get(animal, 0) < count and day <= a.get("last_buy", 22) and feed_secure
                    and _afford(a["cost"], cfg.get("cash_buffer", 200))):
                orders.append(["BUY_ANIMAL", animal, 1])
                _commit(a["cost"])
                return True
        return False

    if day <= 27:
        if cfg.get("animal_first"):
            _bloque_animal()
        # semillas: para el mejor cultivo del mercado (adaptive) o el deficit del plan
        if cfg.get("adaptive"):
            if adaptive_best and adaptive_need > 0:
                n = min(adaptive_need, 6)
                if _afford(CROP[adaptive_best]["seed"] * n, 100):
                    orders.append(["BUY_SEED", adaptive_best, n])
                    _commit(CROP[adaptive_best]["seed"] * n)
        else:
            seed_orders = []
            for crop, target in cfg.get("plants", {}).items():
                c = CROP[crop]
                if day > c["last_plant"]:
                    continue
                deficit = target - planted_count.get(crop, 0) - seeds.get(crop, 0)
                if deficit <= 0:
                    continue
                if cfg.get("phased"):
                    # baratas-primero con tope de gasto: nunca fundir la caja en semillas
                    seed_orders.append(["BUY_SEED", crop, deficit])
                elif _afford(c["seed"] * deficit, 100):
                    seed_orders.append(["BUY_SEED", crop, deficit])
                    _commit(c["seed"] * deficit)
            if cfg.get("phased"):
                seed_orders.sort(key=lambda o: CROP[o[1]]["seed"])
                budget_seeds = max(150, money * 0.35)
                capped = []
                for op in seed_orders:
                    unit_cost = CROP[op[1]]["seed"]
                    n = min(op[2], int(budget_seeds // unit_cost))
                    if n > 0:
                        capped.append([op[0], op[1], n])
                        budget_seeds -= n * unit_cost
                seed_orders = capped
            orders.extend(seed_orders[:2])

        # semillas para el modo grow: cubrir las tiles vacías con el mejor cultivo
        if cfg.get("grow"):
            best = next((c for c in ("MELON", "STRAWBERRY", "CARROT", "WHEAT") if day <= CROP[c]["last_plant"]), None)
            if best:
                n_empty = sum(1 for row in tiles for t in row if t is None)
                need = n_empty - seeds.get(best, 0)
                _cash = money - (_committed[0] if cfg.get("order_funding") else 0.0)
                afford = max(0, int((_cash - 400) // CROP[best]["seed"]))
                n = min(need, afford, 12)
                if n > 0:
                    orders.append(["BUY_SEED", best, n])
                    _commit(CROP[best]["seed"] * n)

        # semillas para el trabajo infinito: cubrir tiles vacías que los ociosos plantarán
        if cfg.get("idle_plant"):
            best = adaptive_best if (adaptive_best and day <= CROP[adaptive_best]["last_plant"]) else (
                "WHEAT" if day <= CROP["WHEAT"]["last_plant"] else None)
            if best:
                spare = sum(1 for row in tiles for t in row if t is None)
                _h2 = _seed_stock if cfg.get("seed_stock_aware") else seeds.get(best, 0)
                n = min(spare - _h2, 8)
                if n > 0 and _afford(CROP[best]["seed"] * n, 300):
                    orders.append(["BUY_SEED", best, n])
                    _commit(CROP[best]["seed"] * n)

        # siguiente animal del plan (1 por turno) — salvo que ya se haya
        # resuelto arriba con animal_first
        if not cfg.get("animal_first"):
            _bloque_animal()

        # puente de wheat para alimentar
        total_wheat = shed.get("WHEAT", 0) + sum(inv.get("WHEAT", 0) for inv in invs)
        if hungry > 0 and total_wheat < hungry and _afford(30 * (hungry - total_wheat), 100):
            orders.append(["BUY_PRODUCT", "WHEAT", hungry - total_wheat])
            _commit(30 * (hungry - total_wheat))

        # buy_feed: cubrir el consumo del dia con margen, en vez de esperar al
        # hambre. Va DENTRO del mismo bloque de compras (indentacion 8).
        if cfg.get("buy_feed") and hour <= 2 and day <= 28:
            _animales = sum(1 for row in tiles for t in row
                            if isinstance(t, dict) and t.get("animal"))
            _tengo = shed.get("WHEAT", 0) + sum(i.get("WHEAT", 0) for i in invs)
            _falta = max(0, int(_animales * cfg.get("feed_days", 2)) - _tengo)
            if _falta > 0 and _afford(_falta * market_prices.get("WHEAT", 25), 300):
                orders.append(["BUY_PRODUCT", "WHEAT", _falta])
                _commit(_falta * market_prices.get("WHEAT", 25))

        # tierra
        if cfg.get("buy_land") and len(farm["unlocked_quadrants"]) < cfg.get("max_quadrants", 2):
            n_extra = len(farm["unlocked_quadrants"]) - 1
            price = [1000, 2000, 4000][n_extra] if n_extra < 3 else None
            land_buffer = 1500 if cfg.get("phased") else 600
            if cfg.get("land_early"):
                # comprar por capacidad planeada (los top: día ~6), no cuando ya no hay tiles
                if price and _afford(price, 900) and day >= 4 and day <= 20:
                    orders.append(["BUY_LAND"])
                    _commit(price)
            elif price and _afford(price, land_buffer) and len(empty_tiles) < 6 and day <= 20:
                orders.append(["BUY_LAND"])
                _commit(price)

    # ---- PLAN DE APERTURA optimizado offline ---------------------------------
    # El 83% de las acciones de unidad del top-1 no miran al rival: el campo es
    # casi un problema de UN jugador y se puede optimizar fuera de linea; solo el
    # mercado interactua. Aqui, para los dias <= plan_until, las ordenes de COMPRA
    # (semillas/animales/tierra) las dicta un calendario buscado offline en vez
    # del scorer. Las VENTAS y los HIRE siguen siendo del chasis (reactivos), y
    # el router/planter ejecutan igual: solo cambia QUE capital se despliega y
    # CUANDO, que es donde vive la estructura de fases.
    _plan = cfg.get("opening_plan")
    if _plan and day <= cfg.get("plan_until", 12):
        _dia = _plan.get(day) or _plan.get(str(day)) or {}
        _resto = [o for o in orders if not (isinstance(o, list) and o and
                  o[0] in ("BUY_SEED", "BUY_ANIMAL", "BUY_LAND"))]
        _compras = []
        for _an, _n in (_dia.get("animals") or {}).items():
            if _n > 0:
                _compras.append(["BUY_ANIMAL", _an, int(_n)])
        for _ in range(int(_dia.get("land", 0) or 0)):
            if len(farm["unlocked_quadrants"]) < cfg.get("max_quadrants", 3):
                _compras.append(["BUY_LAND"])
        for _cr, _n in (_dia.get("seeds") or {}).items():
            if _n > 0:
                _compras.append(["BUY_SEED", _cr, int(_n)])
        if hour == 0:                      # el plan se ejecuta al alba
            orders = _compras + _resto
        else:
            orders = _resto

    return {"farmer": actions[0], "hands": actions[1:], "market": orders[:10]}


CONFIG = {'hands': 8,
 'animals': [('COW', 4), ('SHEEP', 4)],
 'plants': {'CARROT': 1, 'MELON': 11, 'STRAWBERRY': 5, 'WHEAT': 8},
 'care': True,
 'collect_fert': True,
 'fert_prio': 45,
 'animal_harvest_at': 4,
 'premium_hold_day': 8,
 'buy_land': True,
 'max_quadrants': 3,
 'prio_care': 70,
 'prio_urgency': 25,
 'plant_near': True,
 'endgame': True,
 'adaptive': True,
 'crop_tiles': 30,
 'zoning': False,
 'zone_fallback_prio': 70,
 'prio_feed': 75,
 'prio_water': 44,
 'prio_win_bonus': 12,
 'prio_harvest': 76,
 'prio_plant': 40,
 'grow': False,
 'prio_dig': 8,
 'mkt_opp_factor': 1,
 'router': True,
 'hire_late': True,
 'multi_feeder': False,
 'phased': False,
 'tiles_per_unit': 5,
 'sell_floor': 0,
 'idle_plant': True,
 'hands_per_quadrant': 4,
 'land_early': True,
 'town_forecast': True,
 'fert_crops': ['STRAWBERRY', 'TOMATO'],
 'opp_read': True,
 'sell_rank': True,
 'order_budget': True,
 'beat_wave': True,
 'wave_min_value': 2000,
 'melon_max': 8,
 'smart_overflow': False,
 'scorer_v2': False,
 'fallback_fix': True,
 'fert_dawn_load': True,
 'fert_tick_aligned': True,
 'fert_phase_lock': True,
 'seed_stock_aware': True}


def agent(obs):
    return decide(obs, CONFIG)
