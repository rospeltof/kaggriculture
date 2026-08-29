"""Auditoría de turnos-unidad DESPERDICIADOS (pregunta 3a).

Clasifica cada turno de cada unidad (granjero + peones) contra el motor:
  OK        -> la acción cambió el estado (o fue un movimiento efectivo)
  PASS      -> ociosidad explícita
  MOVE_NOOP -> movimiento fuera del tablero (posición sin cambio)
  NOOP:<op> -> acción emitida que el motor ignoró en silencio
Un "turno perdido" = PASS | MOVE_NOOP | NOOP.

Convención verificada del replay: la acción de steps[t] se calculó sobre la
observación de steps[t-1] y produjo la observación de steps[t].

Uso: ./.venv/bin/python ocio.py replays/*.json
"""
import json
import sys
from collections import defaultdict, Counter

SHED_ACCESS = {(4, 4), (5, 4), (4, 5), (5, 5)}
MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}
ANIMALS = {"GOOSE": "COOP", "COW": "PASTURE", "SHEEP": "PASTURE"}
FIRST_YIELD = {"WHEAT": 2, "CARROT": 2, "MELON": 10, "TOMATO": 8, "STRAWBERRY": 10}


def load(path):
    d = json.load(open(path))
    n = d["info"]["TeamNames"]
    me = 0 if n[0].startswith("Rospel") else 1
    return d, me, n[1 - me]


def classify(op, pos, tiles, inv, shed, seeds, day):
    """Devuelve None si la acción es efectiva; si no, la etiqueta del desperdicio."""
    if not op:
        return "EMPTY"
    o = op[0]
    x, y = pos
    if o in MOVES:
        dx, dy = MOVES[o]
        nx, ny = x + dx, y + dy
        return None if (0 <= nx < 10 and 0 <= ny < 10) else "MOVE_OFFBOARD"
    if o == "PASS":
        return "PASS"
    tile = tiles[y][x]
    if o == "DROP":
        if pos not in SHED_ACCESS:
            return "NOOP:DROP_far"
        return None if sum(inv.values()) > 0 else "NOOP:DROP_empty"
    if o == "PICKUP":
        if pos not in SHED_ACCESS:
            return "NOOP:PICKUP_far"
        return None if shed.get(op[1], 0) > 0 else "NOOP:PICKUP_nostock"
    if o == "PLACE":
        item = op[1] if len(op) > 1 else None
        if (item in ANIMALS and isinstance(tile, dict)
                and tile.get("kind") == ANIMALS[item] and "animal" not in tile):
            return None if inv.get(item, 0) > 0 else "NOOP:PLACE_nocarry"
        if pos in SHED_ACCESS:
            return None if inv.get(item, 0) > 0 else "NOOP:PLACE_nocarry"
        return "NOOP:PLACE_badtile"
    if tile == "LOCKED":
        return "NOOP:LOCKED"
    if o == "PLANT":
        crop = op[1] if len(op) > 1 else None
        if tile is not None:
            return "NOOP:PLANT_occupied"
        if seeds.get(crop, 0) <= 0:
            return "NOOP:PLANT_noseed"
        return None
    if o == "WATER":
        if not (isinstance(tile, dict) and tile.get("kind") == "PLANT"):
            return "NOOP:WATER_notplant"
        return "NOOP:WATER_already" if tile["watered_today"] else None
    if o == "HARVEST":
        if not isinstance(tile, dict):
            return "NOOP:HARVEST_notile"
        if tile.get("yield_units", 0) <= 0:
            return "NOOP:HARVEST_empty"
        if tile.get("kind") == "PLANT" and day - tile["planted_day"] < FIRST_YIELD[tile["crop"]]:
            return "NOOP:HARVEST_immature"
        return None
    if o == "FERTILIZE":
        if not (isinstance(tile, dict) and tile.get("kind") == "PLANT"):
            return "NOOP:FERT_notplant"
        return None if inv.get("FERTILIZER", 0) > 0 else "NOOP:FERT_nofert"
    if o == "DIG":
        if tile is None:
            return "NOOP:DIG_empty"
        if isinstance(tile, dict) and "animal" in tile:
            return "NOOP:DIG_animal"
        return None
    if o in ("BUILD_COOP", "BUILD_PASTURE"):
        return None if tile is None else "NOOP:BUILD_occupied"
    if o == "FEED":
        if not (isinstance(tile, dict) and "animal" in tile):
            return "NOOP:FEED_noanimal"
        if tile["fed_today"]:
            return "NOOP:FEED_already"
        return None if inv.get("WHEAT", 0) > 0 else "NOOP:FEED_nowheat"
    if o == "COLLECT_FERTILIZER":
        if not (isinstance(tile, dict) and "animal" in tile):
            return "NOOP:CF_noanimal"
        return None if tile["fertilizer_available"] else "NOOP:CF_unavailable"
    if o == "CARE":
        if not (isinstance(tile, dict) and "animal" in tile):
            return "NOOP:CARE_noanimal"
        return "NOOP:CARE_already" if tile["cared_today"] else None
    return None


def audit(path, player_override=None):
    d, me, opp = load(path)
    if player_override is not None:
        me = player_override
    S = d["steps"]
    rows = []          # (t, day, hour, unit_idx, pos, op, label)
    for t in range(1, len(S)):
        o = S[t - 1][me]["observation"]
        if "farms" not in o:
            o = S[t - 1][0]["observation"]
        act = S[t][me].get("action") or {}
        farm = o["farms"][me]
        priv = o.get("private", {})
        tiles = farm["tiles"]
        shed = dict(priv.get("shed", {}) or {})
        seeds = dict(priv.get("seeds", {}) or {})
        invs = list(priv.get("inventories", [{}]))
        pos_list = [tuple(farm["farmer"])] + [tuple(h) for h in farm["hands"]]
        ops = [act.get("farmer")] + list(act.get("hands") or [])
        day, hour = o["day"], o["hour"]
        for i, pos in enumerate(pos_list):
            op = ops[i] if i < len(ops) else None
            inv = dict(invs[i]) if i < len(invs) else {}
            lab = classify(op, pos, tiles, inv, shed, seeds, day)
            rows.append((t, day, hour, i, pos, tuple(op) if op else None, lab))
    return d, me, opp, rows


def streaks(rows, min_len=4):
    """Rachas de turnos perdidos consecutivos de la MISMA unidad en la MISMA tile,
    dentro del mismo día (los peones desaparecen de noche: el índice se reinicia)."""
    cur = {}
    out = []
    last_day = None
    for t, day, hour, i, pos, op, lab in rows:
        if day != last_day:
            for k, v in cur.items():
                if v[2] >= min_len:
                    out.append(v)
            cur = {}
            last_day = day
        if lab is None:
            v = cur.pop(i, None)
            if v and v[2] >= min_len:
                out.append(v)
            continue
        v = cur.get(i)
        if v and v[1] == pos:
            cur[i] = (v[0], pos, v[2] + 1, v[3], v[4] + [lab])
        else:
            if v and v[2] >= min_len:
                out.append(v)
            cur[i] = ((day, hour), pos, 1, i, [lab])
    for k, v in cur.items():
        if v[2] >= min_len:
            out.append(v)
    return out


if __name__ == "__main__":
    grand = Counter()
    grand_days = Counter()
    grand_pos = Counter()
    n_games = 0
    per_game = []
    for path in sys.argv[1:]:
        try:
            d, me, opp, rows = audit(path)
        except Exception as e:
            print(f"{path}: ERROR {e}")
            continue
        n_games += 1
        c = Counter(lab for *_, lab in rows if lab)
        total = len(rows)
        lost = sum(c.values())
        by_day = Counter()
        for t, day, hour, i, pos, op, lab in rows:
            if lab:
                by_day[day] += 1
                grand_pos[pos] += 1
        grand.update(c)
        grand_days.update(by_day)
        st = streaks(rows)
        per_game.append((path.split("/")[-1], opp, total, lost, len(st),
                         sum(v[2] for v in st), c, by_day, st, d["rewards"][me], d["rewards"][1 - me]))
        print(f"\n{'='*80}\n{path.split('/')[-1]} vs {opp}  ({d['rewards'][me]:,.0f} vs {d['rewards'][1-me]:,.0f})")
        print(f"  turnos-unidad totales {total}, perdidos {lost} ({100*lost/max(1,total):.1f}%)")
        print(f"  desglose: {dict(c.most_common(12))}")
        print(f"  por día:  {dict(sorted(by_day.items()))}")
        if st:
            st.sort(key=lambda v: -v[2])
            print(f"  rachas >=4 turnos perdidos misma tile/mismo día: {len(st)} "
                  f"({sum(v[2] for v in st)} turnos)")
            for (day, hour), pos, n, i, labs in st[:8]:
                print(f"    u{i} en {pos} d{day}h{hour}: {n} turnos  {Counter(labs).most_common(3)}")
    if n_games > 1:
        print(f"\n{'#'*80}\nAGREGADO ({n_games} partidas)")
        tot = sum(g[2] for g in per_game)
        lost = sum(g[3] for g in per_game)
        print(f"  turnos-unidad {tot}, perdidos {lost} ({100*lost/tot:.1f}%) "
              f"= {lost/n_games:.0f} turnos perdidos por partida")
        print(f"  desglose global: {dict(grand.most_common(20))}")
        print(f"  perdidos por día (promedio/partida): "
              + " ".join(f"d{k}:{v/n_games:.0f}" for k, v in sorted(grand_days.items())))
        print(f"  top tiles: {grand_pos.most_common(12)}")
        rs = sum(g[5] for g in per_game)
        print(f"  rachas >=4: {sum(g[4] for g in per_game)} ({rs} turnos, {rs/n_games:.0f}/partida)")
