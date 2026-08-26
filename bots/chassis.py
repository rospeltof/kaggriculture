"""Chasis compartido de bots arquetipo.

Un arquetipo = configuración (qué plantar, qué animales, cuántos peones,
política de venta). El chasis resuelve cada turno: generación de tareas con
prioridades, asignación greedy unidad-más-cercana, logística de wheat para
FEED, órdenes de mercado y cierre de temporada.

Constantes verificadas contra el motor (docs/RULES.md S3.9, S4.x).
"""

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
SHED = (4, 4)
LAST_DAY = 29


def _dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


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
                tasks.append((cfg.get("prio_dig", 8), (x, y), ["DIG"]))
                continue
            if kind == "PLANT":
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

    # ---- plantar según plan ----
    plant_claims = {}
    for crop, target in cfg.get("plants", {}).items():
        c = CROP[crop]
        if day > c["last_plant"]:
            continue
        deficit = target - planted_count.get(crop, 0)
        avail_seeds = seeds.get(crop, 0)
        n = min(deficit, avail_seeds, len(empty_tiles))
        for _ in range(max(0, n)):
            far = not cfg.get("plant_near")
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

    for prio, pos, op in tasks:
        if pos in used_tiles and op[0] not in ("PICKUP",):
            continue
        need_wheat = op[0] == "FEED"
        cands = []
        for i in range(n_units):
            if actions[i] is not None:
                continue
            if need_wheat and invs[i].get("WHEAT", 0) <= 0:
                continue
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
    shed_load = sum(shed.values())
    sellable = []
    for it in SELLABLE:
        n = shed.get(it, 0) - (wheat_buffer if it == "WHEAT" else 0)
        if it in PREMIUM and day < hold_day and day < 28 and shed_load < 85:
            continue  # hold; con el shed casi lleno (>=85) se vende igual para no perder por overflow
        if n > 0:
            sellable.append((it, n))
    sellable.sort(key=lambda kv: -kv[1])
    sell_cap = 8 if (cfg.get("endgame") and day >= 28) else 4
    for it, n in sellable[:sell_cap]:
        orders.append(["SELL", it, n])

    if hour == 0 and day <= 27:
        for _ in range(cfg.get("hands", 0)):
            orders.append(["HIRE"])

    if day <= 27:
        # semillas para el deficit del plan (2 ordenes max)
        seed_orders = []
        for crop, target in cfg.get("plants", {}).items():
            c = CROP[crop]
            if day > c["last_plant"]:
                continue
            deficit = target - planted_count.get(crop, 0) - seeds.get(crop, 0)
            if deficit > 0 and money > c["seed"] * deficit + 100:
                seed_orders.append(["BUY_SEED", crop, deficit])
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
        for animal, count in cfg.get("animals", []):
            a = ANIMAL[animal]
            if owned.get(animal, 0) < count and day <= a.get("last_buy", 22) and money > a["cost"] + cfg.get("cash_buffer", 200):
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
            if price and money > price + 600 and len(empty_tiles) < 6 and day <= 20:
                orders.append(["BUY_LAND"])

    return {"farmer": actions[0], "hands": actions[1:], "market": orders[:10]}
