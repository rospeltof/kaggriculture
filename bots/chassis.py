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


def _plan_routes(serve, n_units, tiles):
    """serve: [(x, y, costo)] -> rutas por unidad. Serpentina espacial, corte por
    costo acumulado, y dentro de cada ruta los animales primero (están cerca del
    shed, donde la unidad amanece y recoge su wheat)."""
    serve = sorted(serve, key=lambda t: (t[0], t[1] if t[0] % 2 == 0 else -t[1]))
    total = sum(c for _, _, c in serve) or 1.0
    target = total / max(1, n_units)
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
        if (has_fert and tile["crop"] in cfg.get("fert_crops", ()) and day <= 26
                and tile.get("fertilized_until_day", -1) < day
                and age >= c["first"] - 2):
            return ["FERTILIZE"]
        if not watered and day <= LAST_DAY:
            if not (not c["ongoing"] and age > c["peak"]) and not (
                    day == LAST_DAY and not (age >= c["first"] and yu > 0)):
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
                    if ready:
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
                        if yu >= 3 or day >= 28:
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
    if empty_structs:
        for x, y, kind in empty_structs:
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
        wheat_floor = min(cfg.get("wheat_floor", herd), max(0, budget // 3))
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
            pipeline = planted_count.get(crop, 0) * u_eff + shed.get(crop, 0)
            opp = cfg.get("mkt_opp_factor", 2)
            supply = int(opp * pipeline)
            if cfg.get("opp_read"):
                # oferta rival OBSERVADA (sus tiles públicas) en vez del factor ciego
                supply = pipeline + opp_incoming.get(crop, 0)
            proj_inv = market_inv.get(crop, 10000)
            if cfg.get("town_forecast"):
                # el town drenará inventario hasta la cosecha -> precio proyectado sube
                proj_inv -= _town_drain_per_day(town, crop) * occ
            if cfg.get("scorer_v2"):
                # precio medio de vender la RÁFAGA completa (pipeline + esta tile)
                price = _avg_price_over(crop, proj_inv, supply + u_eff)
            else:
                price = _price_at(crop, proj_inv + supply + u_eff)
            s = (u_eff * price - CROP[crop]["seed"]) / occ
            if s > best_s:
                best, best_s = crop, s
        if cfg.get("melon_max") and best == "MELON" and planted_count.get("MELON", 0) >= cfg["melon_max"]:
            # melón al tope concurrente (acota la ola de cosecha y la cantidad total
            # de temporada — la curva sq hace que el melón marginal >~120u valga poco):
            # elegir el segundo mejor cultivo
            second, second_s = None, -1e9
            for crop2, (u2, occ2) in CROP_ECON.items():
                if crop2 == "MELON" or day > CROP[crop2]["last_plant"]:
                    continue
                pipe2 = planted_count.get(crop2, 0) * u2 + shed.get(crop2, 0)
                if cfg.get("opp_read"):
                    pipe2 += opp_incoming.get(crop2, 0)   # el fallback también ve al rival
                pr2 = _price_at(crop2, market_inv.get(crop2, 10000) + pipe2 + u2)
                s2 = (u2 * pr2 - CROP[crop2]["seed"]) / occ2
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
                spot = (max if far else min)(empty_tiles, key=lambda t: _dist(t, SHED))
                empty_tiles.remove(spot)
                tasks.append((p_plant + (4 if crop == "WHEAT" else 0), spot, ["PLANT", crop]))
                plant_claims[crop] = plant_claims.get(crop, 0) + 1
        adaptive_need = max(0, wheat_gap - seeds.get("WHEAT", 0)) if wheat_gap else (
            max(0, deficit - seeds.get(best, 0)) if best else 0)
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
                spot = (max if far else min)(empty_tiles, key=lambda t: _dist(t, SHED))
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
            rst["routes"] = _plan_routes(serve_tiles, max(n_expected, n_units), tiles)
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

    # ---- logística matinal multi-feeder: repartir el wheat del shed entre varios
    # alimentadores en paralelo. Con rebaños grandes, un solo feeder cargando todo
    # el wheat tarda más de un día en alimentar 15 animales (causa de los escapes
    # del writeup y del colapso del clon de "ln"). Al alba todos están en el shed.
    # ---- ejecutor de rutas: cada unidad sirve su circuito con bundling ----
    if router_on:
        shed_adj = {(4, 4), (5, 4), (4, 5), (5, 5)}
        routes = rst.get("routes", [])
        idxs = rst.get("idx", [])
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
        for i in range(n_units):
            if actions[i] is not None or not empty_tiles:
                continue
            crop = None
            for cand in ([adaptive_best] if adaptive_best else []) + sorted(seeds, key=lambda k: -seeds.get(k, 0)):
                if (cand and cand in CROP and day <= CROP[cand]["last_plant"]
                        and seeds.get(cand, 0) - plant_claims.get(cand, 0) > 0):
                    crop = cand
                    break
            if not crop:
                break
            spot = min(empty_tiles, key=lambda t: _dist(unit_pos[i], t))
            empty_tiles.remove(spot)
            if unit_pos[i] == spot:
                actions[i] = ["PLANT", crop]
                plant_claims[crop] = plant_claims.get(crop, 0) + 1
            else:
                actions[i] = [_step_toward(unit_pos[i], spot)]

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
        if (it in PREMIUM and day < hold_day and day < 28 and shed_load < 85
                and it not in wave_soon):
            continue  # hold; el shed casi lleno (>=85) o una ola rival anunciada lo perforan
        cap_load = 95 if (cfg.get("smart_overflow") and it in PREMIUM) else 85
        if (floor_frac and it != "FERTILIZER" and day < 28 and shed_load < cap_load
                and it not in wave_soon
                and market_prices.get(it, 0) < floor_frac * BASE_PRICE.get(it, 100)):
            continue  # mercado estrellado: aguantar; el town drena y el precio se recupera
        if it == "MELON" and cfg.get("melon_max") and it not in wave_soon:
            n = min(n, 12)  # pacing: acotar la caminata por la curva en cada orden
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
        missing = n_h - len(farm["hands"])
        for _ in range(max(0, min(missing, 6))):  # por tandas: no comerse el cupo de órdenes
            orders.append(["HIRE"])

    if day <= 27:
        # semillas: para el mejor cultivo del mercado (adaptive) o el deficit del plan
        if cfg.get("adaptive"):
            if adaptive_best and adaptive_need > 0:
                n = min(adaptive_need, 6)
                if money > CROP[adaptive_best]["seed"] * n + 100:
                    orders.append(["BUY_SEED", adaptive_best, n])
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
                elif money > c["seed"] * deficit + 100:
                    seed_orders.append(["BUY_SEED", crop, deficit])
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
                afford = max(0, int((money - 400) // CROP[best]["seed"]))
                n = min(need, afford, 12)
                if n > 0:
                    orders.append(["BUY_SEED", best, n])

        # semillas para el trabajo infinito: cubrir tiles vacías que los ociosos plantarán
        if cfg.get("idle_plant"):
            best = adaptive_best if (adaptive_best and day <= CROP[adaptive_best]["last_plant"]) else (
                "WHEAT" if day <= CROP["WHEAT"]["last_plant"] else None)
            if best:
                spare = sum(1 for row in tiles for t in row if t is None)
                n = min(spare - seeds.get(best, 0), 8)
                if n > 0 and money > CROP[best]["seed"] * n + 300:
                    orders.append(["BUY_SEED", best, n])

        # siguiente animal del plan (1 por turno)
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
        for animal, count in cfg.get("animals", []):
            a = ANIMAL[animal]
            if (owned.get(animal, 0) < count and day <= a.get("last_buy", 22) and feed_secure
                    and money > a["cost"] + cfg.get("cash_buffer", 200)):
                orders.append(["BUY_ANIMAL", animal, 1])
                break

        # puente de wheat para alimentar
        total_wheat = shed.get("WHEAT", 0) + sum(inv.get("WHEAT", 0) for inv in invs)
        if hungry > 0 and total_wheat < hungry and money > 30 * (hungry - total_wheat) + 100:
            orders.append(["BUY_PRODUCT", "WHEAT", hungry - total_wheat])

        # tierra
        if cfg.get("buy_land") and len(farm["unlocked_quadrants"]) < cfg.get("max_quadrants", 2):
            n_extra = len(farm["unlocked_quadrants"]) - 1
            price = [1000, 2000, 4000][n_extra] if n_extra < 3 else None
            land_buffer = 1500 if cfg.get("phased") else 600
            if cfg.get("land_early"):
                # comprar por capacidad planeada (los top: día ~6), no cuando ya no hay tiles
                if price and money > price + 900 and day >= 4 and day <= 20:
                    orders.append(["BUY_LAND"])
            elif price and money > price + land_buffer and len(empty_tiles) < 6 and day <= 20:
                orders.append(["BUY_LAND"])

    return {"farmer": actions[0], "hands": actions[1:], "market": orders[:10]}
