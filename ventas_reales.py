"""Reconstrucción EXACTA de las ventas de ambos jugadores desde el inventario
del mercado (las órdenes emitidas mienten: un SELL de 200 con 30 en el shed
vende 30).

Identidad del motor por turno (RULES.md S5.x, S7.1):
    Δinv[item] = ventas_totales - compras_totales - consumo_town
=>  ventas_totales = Δinv + compras + consumo_town

consumo_town es determinista: cada tienda desbloqueada consume 1 de cada
producto suyo cuando step%4==0 (x2 si es mono-producto) y el town center 1 de
cada producto no-fertilizer cuando step%24==0.
Nuestras ventas se conocen exactas por el delta de nuestro shed; el resto es del
rival.
"""
import json
import sys
from collections import defaultdict

SHOPS = {
    "BAKERY": ("EGG", "WHEAT"),
    "PIZZA_SHOP": ("MILK", "TOMATO", "WHEAT"),
    "BRUNCH_SPOT": ("EGG", "WHEAT", "STRAWBERRY"),
    "YARN_STORE": ("WOOL",),
    "ICE_CREAM_SHOP": ("STRAWBERRY", "MILK", "WHEAT"),
    "PET_CAFE": ("CARROT",),
    "SMOOTHIE_SHOP": ("STRAWBERRY", "MILK"),
    "FARMERS_MARKET": ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY"),
}
PRODUCTS = ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER"]


def town_consume(town, step):
    out = defaultdict(int)
    if step % 4 == 0:
        for shop in town.get("unlocked_shops", []) or []:
            prods = SHOPS.get(shop, ())
            mult = 2 if len(prods) == 1 else 1
            for it in prods:
                out[it] += mult
    if step % 24 == 0:
        for it in PRODUCTS:
            if it != "FERTILIZER":
                out[it] += 1
    return out


def reconstruir(d, me):
    """Devuelve (ventas_reales[player][item] -> (unidades, ingreso), por_dia)."""
    steps = d["steps"]
    sold = {0: defaultdict(lambda: [0, 0.0]), 1: defaultdict(lambda: [0, 0.0])}
    por_dia = {0: defaultdict(lambda: defaultdict(float)), 1: defaultdict(lambda: defaultdict(float))}
    for t in range(1, len(steps)):
        prev, cur = steps[t - 1][0]["observation"], steps[t][0]["observation"]
        step = prev.get("step", t - 1)
        day = prev["day"]
        prices = prev["market"]["prices"]
        tc = town_consume(prev["town"], step)
        # nuestras ventas reales: delta del shed propio (bajadas) menos lo consumido
        # por FEED/FERTILIZE no aplica al shed (esos salen de inventarios de unidad)
        my_prev = (steps[t - 1][me]["observation"].get("private") or {}).get("shed") or {}
        my_cur = (steps[t][me]["observation"].get("private") or {}).get("shed") or {}
        my_act = steps[t][me].get("action") or {}
        my_orders = defaultdict(int)
        for m in my_act.get("market") or []:
            if m and m[0] == "SELL" and len(m) >= 3:
                my_orders[m[1]] += int(m[2])
        buys = defaultdict(int)
        for pl in (0, 1):
            for m in (steps[t][pl].get("action") or {}).get("market") or []:
                if m and m[0] == "BUY_PRODUCT" and len(m) >= 3:
                    buys[m[1]] += int(m[2])
        for it in PRODUCTS:
            dinv = cur["market"]["inventory"].get(it, 0) - prev["market"]["inventory"].get(it, 0)
            total_sold = dinv + buys.get(it, 0) + tc.get(it, 0)
            if total_sold <= 0:
                continue
            # nuestra parte: acotada por la orden emitida y por el stock disponible
            mine = min(my_orders.get(it, 0), max(0, my_prev.get(it, 0)), total_sold)
            theirs = max(0, total_sold - mine)
            # OJO (corregido 2026-09-03): total_sold incluye las COMPRAS del rival
            # (un BUY_PRODUCT suyo baja el inventario igual que su venta lo sube,
            # y aquí el residuo se le atribuía como venta). El rival compra ~390
            # wheat por partida: sin este ajuste el gap de wheat era un espejismo
            # y "planta más wheat" habría sido la recomendación #1, siendo falsa.
            their_buys = 0
            for m in (steps[t][1 - me].get("action") or {}).get("market") or []:
                if m and m[0] == "BUY_PRODUCT" and len(m) >= 3 and m[1] == it:
                    their_buys += int(m[2])
            theirs = max(0, theirs - their_buys)
            pr = prices.get(it, 0)
            sold[me][it][0] += mine
            sold[me][it][1] += mine * pr
            sold[1 - me][it][0] += theirs
            sold[1 - me][it][1] += theirs * pr
            por_dia[me][day][it] += mine * pr
            por_dia[1 - me][day][it] += theirs * pr
    return sold, por_dia


if __name__ == "__main__":
    for path in sys.argv[1:]:
        d = json.load(open(path))
        n = d["info"]["TeamNames"]
        me = 0 if n[0].startswith("Rospel") else 1
        sold, por_dia = reconstruir(d, me)
        print(f"\n=== {path.split('/')[-1]} vs {n[1-me]} "
              f"({d['rewards'][me]:,.0f} vs {d['rewards'][1-me]:,.0f}) ===")
        print("ingreso REAL por producto (yo | rival):")
        tot_me = tot_op = 0
        rows = []
        for it in PRODUCTS:
            a, b = sold[me][it], sold[1 - me][it]
            if a[0] or b[0]:
                rows.append((b[1] - a[1], it, a, b))
                tot_me += a[1]
                tot_op += b[1]
        for gap, it, a, b in sorted(rows, key=lambda r: -abs(r[0])):
            print(f"  {it:11s} {a[0]:>4.0f}u ${a[1]:>8,.0f} | {b[0]:>4.0f}u ${b[1]:>8,.0f}   gap {gap:>+9,.0f}")
        print(f"  {'TOTAL':11s}      ${tot_me:>8,.0f} |      ${tot_op:>8,.0f}   gap {tot_op-tot_me:>+9,.0f}")
