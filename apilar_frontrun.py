"""Capa FR: adelantarse a las compras de trigo de la cinta de ruta (defensa + ataque).

Hecho (replays 28-sep): las compras grandes de trigo de los agentes de ruta
(BUY_PRODUCT WHEAT 48..89) vienen tal cual de la cinta, y todas las familias
publicas comparten las tablas de rutas: dos agentes que ven las mismas dos primeras
tiendas siguen la misma cinta. Rivales privados (Jun_value, David Goldrajch) compran
en t-1 lo que la cinta comprara en t y lo venden en t en el indice 9 (despues de la
compra de la victima): +$8-11k por partida contra nosotros.

Esta capa, al final de la cadena:
  1. Pre-compra en t-1 la compra de trigo que la cinta propia hace en t (N >= MIN) y la
     quita en t (defensa: el especulador vende en t sin demanda).
  2. Si el rival se confirma como seguidor de la cinta (su compra en pasos anteriores
     aparece en el inventario del mercado), compra ademas X = min(N, hueco) en t-1 y
     vende X en t en el indice 9 (rellenando con SELL WHEAT 0, que ocupa hueco sin efecto).
Deteccion: rival_compra(s) = -(dInv - dPropio + consumo) con el consumo del pueblo del
motor (cada 4 pasos 1 por tienda con trigo, 1 extra cada 24).

Uso: apilar_frontrun.py <base.py> <salida.py> [--sin-ataque] [--preventa]
"""
import hashlib, sys
from pathlib import Path

CAPA = '''

# ==== Capa FR: adelantarse a las compras de trigo de la cinta (kaggriculture local, 2026-09-28) ====
_FR_PARENT = [v for v in list(globals().values()) if callable(v)][-1]
_FR_ATAQUE = {ataque}
_FR_PREVENTA = {preventa}
_FR_MIN = 20
_FR_STATE = {{}}
_FR_REPORT = dict(presells=0, presell_units=0, prebuys=0, prebuy_units=0, spec_buys=0, spec_units=0, spec_sells=0, hits=0, misses=0, errors=0)
_FR_WHEAT_SHOPS = {{'BAKERY': 1, 'PIZZA_SHOP': 1, 'BRUNCH_SPOT': 1, 'ICE_CREAM_SHOP': 1, 'FARMERS_MARKET': 1}}


def _fr_tape_wheat_buy(native, t):
    if t >= 719:
        return 0
    tape = _IMPL.chassis.routes.get(2 if t >= 648 else native.get('route'))
    if not tape or t >= len(tape):
        return 0
    return sum(max(0, int(o[2])) for o in (tape[t].get('market') or []) if o and len(o) > 2 and o[:2] == ['BUY_PRODUCT', 'WHEAT'])


def _fr_draw(shops, step):
    d = 0
    if step % 4 == 0:
        d += sum(1 for s in shops if s in _FR_WHEAT_SHOPS)
    if step % 24 == 0:
        d += 1
    return d


def frontrun_agent(observation, configuration=None):
    step = int(observation.get('step', 0)); player = int(observation.get('player', 0))
    if step == 0:
        _FR_STATE[player] = dict(pending={{}}, own={{}}, sold={{}}, prev=None, score=0, hist=[])
        for k in _FR_REPORT:
            _FR_REPORT[k] = 0
    st = _FR_STATE.setdefault(player, dict(pending={{}}, own={{}}, sold={{}}, prev=None, score=0, hist=[]))
    action = _FR_PARENT(observation, configuration)
    try:
        native = _IMPL.chassis.players.get(player) or {{}}
        inv = int(observation['market']['inventory']['WHEAT'])
        shops = list(observation['town']['unlocked_shops'])
        prev = st.get('prev')
        # --- deteccion del rival seguidor de cinta (paso anterior)
        if prev is not None and prev['step'] == step - 1 and prev['tape_n'] >= _FR_MIN:
            d_inv = inv - prev['inv']
            own_net = prev['own_sell'] - prev['own_buy']
            rival_buy = -(d_inv - own_net + _fr_draw(prev['shops'], prev['step']))
            hit = rival_buy >= 0.7 * prev['tape_n']
            st['hist'] = (st['hist'] + [hit])[-4:]
            _FR_REPORT['hits' if hit else 'misses'] += 1
        victim = _FR_ATAQUE and len(st['hist']) >= 2 and sum(st['hist'][-3:]) >= 2 and st['hist'][-1]
        market = [list(o) for o in (action.get('market') or []) if o]
        # --- en t: quitar la compra propia ya adelantada y vender la especulativa en el indice 9
        pre = st['own'].pop(step, 0)
        if pre:
            restante = pre
            nuevo = []
            for o in market:
                if restante > 0 and len(o) > 2 and o[:2] == ['BUY_PRODUCT', 'WHEAT']:
                    q = max(0, int(o[2])); quita = min(q, restante); restante -= quita
                    if q - quita > 0:
                        nuevo.append(['BUY_PRODUCT', 'WHEAT', q - quita])
                    continue
                nuevo.append(o)
            market = nuevo
        vendido = st['sold'].pop(step, 0)
        if vendido:
            restante = vendido; nuevo = []
            for o in market:
                if restante > 0 and len(o) > 2 and o[:2] == ['SELL', 'WHEAT'] and 20 <= int(o[2]) < 1000:
                    q = max(0, int(o[2])); quita = min(q, restante); restante -= quita
                    if q - quita > 0:
                        nuevo.append(['SELL', 'WHEAT', q - quita])
                    continue
                nuevo.append(o)
            market = nuevo
        x = st['pending'].pop(step, 0)
        if x > 0:
            if len(market) <= 9:
                while len(market) < 9:
                    market.append(['SELL', 'WHEAT', 0])
                market.append(['SELL', 'WHEAT', x])
                _FR_REPORT['spec_sells'] += 1
        # --- mirar t+1: venta de la cinta propia (20..999; 1000 = vender todo) -> adelantarla
        if _FR_PREVENTA and 144 <= step < 700 and not x:
            t1 = step + 1
            tape1 = _IMPL.chassis.routes.get(2 if t1 >= 648 else native.get('route')) or []
            nv = sum(max(0, int(o[2])) for o in ((tape1[t1].get('market') or []) if t1 < len(tape1) else []) if o and len(o) > 2 and o[:2] == ['SELL', 'WHEAT'] and 20 <= int(o[2]) < 1000)
            disp = int(observation['private']['shed'].get('WHEAT', 0)) - sum(max(0, int(o[2])) for o in market if len(o) > 2 and o[:2] == ['SELL', 'WHEAT'])
            nv = min(nv, max(0, disp))
            if nv > 0 and len(market) <= 9:
                while len(market) < 9:
                    market.append(['SELL', 'WHEAT', 0])
                market.append(['SELL', 'WHEAT', nv])
                st['sold'][t1] = nv; _FR_REPORT['presells'] += 1; _FR_REPORT['presell_units'] += nv
        # --- mirar t+1: compra de la cinta propia
        n = _fr_tape_wheat_buy(native, step + 1) if 144 <= step < 700 else 0
        compra = 0
        if n >= _FR_MIN and len(market) < 9:
            stock = projected_shed(dict(action, market=market), FarmView(observation))
            ocupado = sum(max(0, int(v)) for v in stock.values())
            hueco = 100 - ocupado - 4
            precio = float(observation['market']['prices']['WHEAT'])
            caja = float(observation['farms'][player]['money']) - 600
            propio = max(0, min(n, hueco, int(caja // (precio + 4))))
            spec = 0
            if victim and propio == n:
                spec = max(0, min(n, hueco - propio, int((caja - propio * (precio + 4)) // (precio + 8))))
            compra = propio + spec
            if compra > 0:
                market.append(['BUY_PRODUCT', 'WHEAT', compra])
                if propio:
                    st['own'][step + 1] = propio; _FR_REPORT['prebuys'] += 1; _FR_REPORT['prebuy_units'] += propio
                if spec:
                    st['pending'][step + 1] = spec; _FR_REPORT['spec_buys'] += 1; _FR_REPORT['spec_units'] += spec
        own_buy = sum(max(0, int(o[2])) for o in market if len(o) > 2 and o[:2] == ['BUY_PRODUCT', 'WHEAT'])
        shed_w = int(observation['private']['shed'].get('WHEAT', 0))
        own_sell = min(shed_w + own_buy, sum(max(0, int(o[2])) for o in market if len(o) > 2 and o[:2] == ['SELL', 'WHEAT']))
        st['prev'] = dict(step=step, inv=inv, shops=shops, own_buy=own_buy, own_sell=own_sell,
                          tape_n=_fr_tape_wheat_buy(native, step) if 144 <= step < 700 else 0)
        if market != [list(o) for o in (action.get('market') or []) if o]:
            action = dict(action, market=market[:10])
            rs = _RACE_STATE.get(player)
            if rs is not None and rs.get('prev_action') is not None and rs.get('step') == step:
                rs['prev_action'] = action
    except Exception:
        _FR_REPORT['errors'] += 1
    return action


frontrun_agent.telemetry = _FR_REPORT
'''


def main(base, salida, *flags):
    ataque = "--sin-ataque" not in flags
    preventa = "--preventa" in flags
    b = Path(base).read_bytes()
    Path(salida).write_bytes(b + CAPA.format(ataque=ataque, preventa=preventa).encode())
    print(salida, "ataque" if ataque else "solo-defensa", hashlib.sha256(Path(salida).read_bytes()).hexdigest()[:12])


if __name__ == "__main__":
    main(*sys.argv[1:])
