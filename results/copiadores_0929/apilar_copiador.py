"""Rival copiador SINTETICO: capa de ida-y-vuelta en el mismo paso (WHEAT/FERTILIZER) sobre un agente base.

Reconstruida de 133 replays reales de final_29 (FINAL29_LADDER_0929a). Se anade al final del fichero base;
la funcion nueva es el ultimo callable del modulo (get_last_callable), asi que envuelve al agente base.

Lado compra (copia de MS): si la cola base compra P y no vende P, el copiador compra X de mas ANTES de que
nosotros lleguemos a nuestro indice de reventa (9) y revende X en un indice k <= 8. Con el espejo comprando
entre medias, su reventa se cotiza con nuestra compra ya hecha.
Lado venta (copia de MSS): si la cola base vende P y no lo compra, vende X de mas y recompra X en un indice
anterior a nuestro 9.

Colocaciones (--coloc), observadas en los replays:
  xl       Xiang Li: la compra base se FUSIONA (m+X) y se mueve a `dest` (primer indice tras el bloque inicial de
           ventas de productos que no son WHEAT/FERTILIZER); SELL X
           ocupa el sitio original de la compra base. Si dest == indice original, no actua.
  dd       dodoshark / Mahmoud Nasser: orden SEPARADA BUY X en el indice 0; SELL X justo antes de la compra base.
           Requiere que la compra base no sea la primera orden de la cola.
  ady      ikevayansky (trigo) / Kaggriculture Agent / Mahmoud: BUY X separada en `dest`, SELL X inmediatamente
           despues (k = b+1); la compra base queda detras.
  tras     Paing / Kaggriculture Agent (k=2): BUY X separada en `dest`, la compra base justo detras y SELL X
           justo despues de la compra base (k = b+2).
  escalera porosyonok: X se descompone en trozos (40, 16, 4) y cada trozo es un par BUY q / SELL q adyacente,
           todos desde `dest`, antes de la compra base.
  fin      (anadido 2026-09-29, indice intermedio) BUY X separada en el indice 0, la cola base detras y SELL X al
           final de SU cola, rellenando con ordenes vacias hasta el indice --k (5-6; Paing/ikevayansky FERT
           3-7, koucha 5-7). No actua si la SELL quedaria en el indice 9 o mas. Con --venta_coloc fin, el lado
           venta suma X a la venta base y recompra X en max(fin de su cola, --k).
Regla de X (--x):
  ms90r0   min(90, (dinero - otros gastos)//(p+3) - m, 100 - cobertizo_pre - m - 2), X >= 1   (Xiang Li)
  ms90     la de nuestra MS: min(90, 100 - cob - m - 6, (dinero - gastos - 500)//(p+3)), X >= 3 (ikevayansky ~)
  q16      16*floor(min(96, 100 - cob)/16), X >= 32, exige caja >= X*(p+3) + gastos + 500      (dodoshark)
  q20      20*floor(min(80, 100 - cob - m - 2)/20), X >= 20, reserva 500                          (Paing)
  q24      el mayor de (48, 24, 12) que cabe, reserva 500                                          (Kaggriculture Agent)
  fijo24   24 si cabe, reserva 500                                                                  (koucha, compra)
  esc      trozos de (40, 16, 4) hasta min(96, hueco, caja)                                         (porosyonok)
Otros: --p 1.0 (probabilidad determinista por paso de actuar en un paso elegible; los copiadores selectivos
reales actuan en ~15-45% de sus pasos elegibles de trigo), --lado compra|venta|ambos, --mixto 1 (actua tambien si la cola base compra y vende P: pasos h1-h3 del
fertilizante; Paing, ikevayansky, open5), --t0 144 --t1 700, prioridad FERTILIZER y luego WHEAT, un producto
por paso.

Uso: apilar_copiador.py <base.py> <salida.py> [--coloc xl] [--x ms90r0] [--lado compra] [--mixto 0]
                         [--t0 144] [--t1 700] [--venta_coloc ady|ultimo] [--vxmax 60]
"""
import argparse, hashlib, json
from pathlib import Path

CAPA = r'''

# ==== Copiador sintetico de MS/MSS (kaggriculture local, 2026-09-29): __CFG__ ====
_CP_CFG = __CFG__
import random as _cp_random
_CP_REPORT = dict(compras=0, unidades_c=0, ventas=0, unidades_v=0, saltos_dest=0, saltos_x=0, saltos_p=0, errores=0)
_CP_PARENT = [v for v in list(globals().values()) if callable(v)][-1]
_CP_FIJO = {'GOOSE': 300, 'COW': 400, 'SHEEP': 500, 'WHEAT': 10, 'CARROT': 20, 'TOMATO': 50, 'STRAWBERRY': 100, 'MELON': 80}


def _cp_gasto(market, prices, excluir=None):
    g = 0.0
    for o in market:
        if not o:
            continue
        if o[0] == 'BUY_PRODUCT' and len(o) > 2 and o[1] != excluir:
            g += int(o[2]) * (float(prices.get(o[1], 0)) + 3)
        elif o[0] == 'HIRE':
            g += 100
        elif o[0] == 'BUY_LAND':
            g += 4000
        elif o[0] in ('BUY_SEED', 'BUY_ANIMAL') and len(o) > 2:
            g += int(o[2]) * _CP_FIJO.get(o[1], 500)
    return g


def _cp_dest(market, item):
    """primer indice tras el bloque inicial de ventas de productos que no son WHEAT/FERTILIZER."""
    d = 0
    while d < len(market):
        o = market[d]
        if o and o[0] == 'SELL' and len(o) > 1 and o[1] not in ('WHEAT', 'FERTILIZER'):
            d += 1
        else:
            break
    return d


def _cp_x(regla, money, gasto_otros, m, precio, cob):
    p3 = precio + 3
    if regla == 'ms90r0':
        x = min(90, int((money - gasto_otros) // p3) - m, 100 - cob - m - 2)
        return x if x >= 1 else 0
    if regla == 'ms90':
        x = min(90, 100 - cob - m - 6, int((money - gasto_otros - m * p3 - 500) // p3))
        return x if x >= 3 else 0
    caja = int((money - gasto_otros - m * p3 - 500) // p3)
    if regla == 'q16':
        x = 16 * (min(96, 100 - cob, caja) // 16)
        return x if x >= 32 else 0
    if regla == 'q20':
        x = 20 * (min(80, 100 - cob - m - 2, caja) // 20)
        return x if x >= 20 else 0
    if regla == 'q24':
        lim = min(100 - cob - m - 2, caja)
        return next((q for q in (48, 24, 12) if q <= lim), 0)
    if regla == 'fijo24':
        return 24 if min(100 - cob - m - 2, caja) >= 24 else 0
    if regla == 'esc':
        x = min(96, 100 - cob - m - 2, caja)
        return x if x >= 4 else 0
    return 0


def _cp_trozos(x):
    out = []
    for q in (40, 16, 4):
        while x >= q and len(out) < 3:
            out.append(q); x -= q
    return out


def _cp_compra(market, item, X, coloc):
    """devuelve la cola nueva o None si la colocacion no es posible."""
    ib = [i for i, o in enumerate(market) if o and o[0] == 'BUY_PRODUCT' and len(o) > 2 and o[1] == item and int(o[2]) > 0]
    orig = ib[0]; base = market[orig]
    dest = _cp_dest(market, item)
    if coloc == 'xl':
        if dest >= orig:
            return None
        q = market[:dest] + [['BUY_PRODUCT', item, int(base[2]) + X]] + market[dest:orig] + [['SELL', item, X]] + market[orig + 1:]
    elif coloc == 'dd':
        if orig == 0:
            return None
        q = [['BUY_PRODUCT', item, X]] + market[:orig] + [['SELL', item, X]] + market[orig:]
    elif coloc == 'ady':
        resto = market[:orig] + market[orig + 1:]
        d = min(dest, len(resto))
        q = resto[:d] + [['BUY_PRODUCT', item, X], ['SELL', item, X], base] + resto[d:]
    elif coloc == 'tras':
        resto = market[:orig] + market[orig + 1:]
        d = min(dest, len(resto))
        q = resto[:d] + [['BUY_PRODUCT', item, X], base, ['SELL', item, X]] + resto[d:]
    elif coloc == 'fin':
        q = [['BUY_PRODUCT', item, X]] + market
        while len(q) < _CP_CFG.get('k', 6):
            q.append([])
        q = q + [['SELL', item, X]]
        return q if len(q) <= 9 else None
    elif coloc == 'escalera':
        resto = market[:orig] + market[orig + 1:]
        d = min(dest, len(resto))
        pares = []
        for t in _cp_trozos(X):
            pares += [['BUY_PRODUCT', item, t], ['SELL', item, t]]
        q = resto[:d] + pares + [base] + resto[d:]
    else:
        return None
    return q if len(q) <= 10 else None


def _cp_venta(market, item, X, coloc):
    iv = [i for i, o in enumerate(market) if o and o[0] == 'SELL' and len(o) > 2 and o[1] == item and 0 < int(o[2]) < 1000]
    i0 = iv[0]
    if coloc == 'fin':      # recompra en max(fin de su cola, k), siempre antes de nuestro 9
        q = list(market); q[i0] = ['SELL', item, int(q[i0][2]) + X]
        while len(q) < _CP_CFG.get('k', 6):
            q.append([])
        q = q + [['BUY_PRODUCT', item, X]]
    elif coloc == 'ultimo':   # koucha: se suma X a la venta base y se recompra en la ultima posicion de SU cola (< 9)
        q = list(market); q[i0] = ['SELL', item, int(q[i0][2]) + X]; q = q + [['BUY_PRODUCT', item, X]]
    else:                   # Kaggriculture Agent: SELL X separada en 0 y recompra justo despues
        q = [['SELL', item, X], ['BUY_PRODUCT', item, X]] + market
    return q if len(q) <= 9 else None


def copiador_sintetico(observation, configuration=None):
    action = _CP_PARENT(observation, configuration)
    try:
        cfg = _CP_CFG
        step = int(observation.get('step', 0)); player = int(observation.get('player', 0))
        if step < cfg['t0'] or step >= cfg['t1']:
            return action
        market = [list(o) for o in (action.get('market') or []) if o]
        prices = observation['market']['prices']
        money = float(observation['farms'][player]['money'])
        cob = sum(max(0, int(v)) for v in projected_shed(dict(action, market=market), FarmView(observation)).values())
        nuevo = None
        for item in ('FERTILIZER', 'WHEAT'):
            if cfg['p'] < 1 and _cp_random.Random(step * 7919 + player * 104729 + len(item)).random() >= cfg['p']:
                _CP_REPORT['saltos_p'] += 1; continue
            compra = [o for o in market if o[0] == 'BUY_PRODUCT' and len(o) > 2 and o[1] == item and int(o[2]) > 0]
            venta = [o for o in market if o[0] == 'SELL' and len(o) > 2 and o[1] == item and 0 < int(o[2]) < 1000]
            if cfg['lado'] in ('compra', 'ambos') and compra and (not venta or cfg['mixto']):
                m = sum(int(o[2]) for o in compra)
                X = _cp_x(cfg['x'], money, _cp_gasto(market, prices, excluir=item), m, float(prices.get(item, 0)), cob)
                if X <= 0:
                    _CP_REPORT['saltos_x'] += 1; continue
                nuevo = _cp_compra(market, item, X, cfg['coloc'])
                if nuevo is None:
                    _CP_REPORT['saltos_dest'] += 1; continue
                _CP_REPORT['compras'] += 1; _CP_REPORT['unidades_c'] += X
                break
            if cfg['lado'] in ('venta', 'ambos') and venta and not compra:
                stock = int((observation.get('private') or {}).get('shed', {}).get(item, 0)) - sum(int(o[2]) for o in venta)
                X = int(min(cfg['vxmax'], stock, max(0, money - 500) // (float(prices.get(item, 0)) + 3)))
                if X < 3:
                    continue
                nuevo = _cp_venta(market, item, X, cfg['venta_coloc'])
                if nuevo is None:
                    continue
                _CP_REPORT['ventas'] += 1; _CP_REPORT['unidades_v'] += X
                break
        if nuevo is not None:
            action = dict(action, market=nuevo[:10])
            rs = globals().get('_RACE_STATE', {}).get(player)
            if rs is not None and rs.get('prev_action') is not None and rs.get('step') == step:
                rs['prev_action'] = action
    except Exception:
        _CP_REPORT['errores'] += 1
    return action
copiador_sintetico.telemetry = _CP_REPORT
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('base'); ap.add_argument('salida')
    ap.add_argument('--coloc', default='xl', choices=['xl', 'dd', 'ady', 'tras', 'escalera', 'fin'])
    ap.add_argument('--x', default='ms90r0', choices=['ms90r0', 'ms90', 'q16', 'q20', 'q24', 'fijo24', 'esc'])
    ap.add_argument('--lado', default='compra', choices=['compra', 'venta', 'ambos'])
    ap.add_argument('--mixto', type=int, default=0)
    ap.add_argument('--t0', type=int, default=144); ap.add_argument('--t1', type=int, default=700)
    ap.add_argument('--venta_coloc', default='ady', choices=['ady', 'ultimo', 'fin'])
    ap.add_argument('--vxmax', type=int, default=60)
    ap.add_argument('--k', type=int, default=6, help="coloc/venta_coloc fin: indice minimo de la pata de cierre")
    ap.add_argument('--p', type=float, default=1.0, help='probabilidad de actuar en un paso elegible (determinista por paso)')
    a = ap.parse_args()
    cfg = dict(coloc=a.coloc, x=a.x, lado=a.lado, mixto=bool(a.mixto), t0=a.t0, t1=a.t1, venta_coloc=a.venta_coloc, vxmax=a.vxmax, p=a.p, k=a.k)
    b = Path(a.base).read_bytes()
    Path(a.salida).write_bytes(b + CAPA.replace('__CFG__', json.dumps(cfg).replace('true', 'True').replace('false', 'False')).encode())
    print(a.salida, cfg, hashlib.sha256(Path(a.salida).read_bytes()).hexdigest()[:12])


if __name__ == '__main__':
    main()
