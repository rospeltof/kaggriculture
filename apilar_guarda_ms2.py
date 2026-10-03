"""Capa CC2: respuesta POST-DISPARO de la guarda GS (f29g) contra copiadores de MS/MSS.

Parte de los bytes de f29g (final_29 + capa GS) y anade al final una capa que SOLO actua cuando la guarda ya
disparo para ese jugador (_GS_STATE[jugador]['off'] = True) y 144 <= t < 700. Antes del disparo la accion es
exactamente la de f29g (y por tanto la de final_29). La funcion nueva `guarda_cc_agent` es el ultimo callable
del modulo y envuelve a `guarda_agent` (la guarda sigue ejecutandose dentro, igual que en f29g).

Analisis previo (workflow guarda2/analizar-residual, 96 partidas locales + 20 resimulaciones reales): tras el
disparo el dano residual real es sobre todo el sandwich sobre nuestras compras base de FERTILIZER (el copiador
compra X en el indice 0 y revende en k >= 2). Respuesta ccF (contra-copia de FERTILIZER):

  En pasos cuya cola final compra FERT, no vende FERT y no tiene ninguna SELL antes de la primera compra de
  FERT: [BUY FERT X] en el indice 0 (entrelazada en lockstep con su compra), [SELL FERT X] en el 1 (antes de su
  reventa), el resto en su orden, relleno con [] y la compra base BUY FERT m en el indice 9.
  X = min(xmax, 100 - cobertizo_proyectado - m - 6, (dinero - gastos - reserva)//(p + margen_precio)), X >= 3.
  margen_precio = 40 (endurecido frente a p+3 del prototipo): en lockstep con otra compra el precio de FERT
  sube 0,4 por unidad nuestra, asi que p + 0,4*90 < p + 40 acota el coste real de la pata y la SELL nunca vende
  stock propio por una compra incompleta por caja.
  Con --fallback fin, si hay ventas delante solo se mueve la compra base de FERT al indice 9.
  La compra base solo se mueve si dinero - (ordenes fijas + todas las compras a p+3) >= 100 (mas estricto que BP).
  No actua si la cola tiene entradas vacias o no-lista (no destruir rellenos intencionados), si ya ocupa el
  indice 9 con una SELL (preventa/venta especulativa de FR) o si no cabe en 10 ordenes.

Seguridad: todo en try/except; ante cualquier error se devuelve la accion de f29g sin tocar. Estado solo de
lectura sobre _GS_STATE; actualiza _RACE_STATE['prev_action'] como las demas capas.

Uso: apilar_guarda_ms2.py <f29g.py> <salida.py> [--fallback fin|nada] [--xmax 90] [--margen_precio 40]
                          [--reserva 500] [--t0 144] [--t1 700]
"""
import argparse, hashlib, json, sys
from pathlib import Path

CAPA = r'''

# ==== Capa CC2: contra-copia de FERTILIZER tras el disparo de la guarda GS (kaggriculture local, 2026-09-29): __CFG__ ====
_CC_CFG = __CFG__
_CC_AGENT = [v for v in list(globals().values()) if callable(v)][-1]
_CC_REPORT = dict(pares=0, unidades=0, finales=0, bloqueos_caja=0, errores=0)
_CC_FIJO = {'GOOSE': 300, 'COW': 400, 'SHEEP': 500, 'WHEAT': 10, 'CARROT': 20, 'TOMATO': 50, 'STRAWBERRY': 100, 'MELON': 80}
_CC_OK = bool(getattr(_CC_AGENT, '__name__', '') == 'guarda_agent' and isinstance(globals().get('_GS_STATE'), dict)
              and globals().get('_GS_OK'))


def _cc_n(o):
    try:
        return int(o[2])
    except Exception:
        return 0


def _cc_fijo(q):
    c = 0.0
    for o in q:
        if o[0] == 'HIRE':
            c += 100
        elif o[0] == 'BUY_LAND':
            c += 4000
        elif o[0] in ('BUY_SEED', 'BUY_ANIMAL') and len(o) > 2:
            c += max(0, _cc_n(o)) * _CC_FIJO.get(o[1], 500)
    return c


def _cc_es(o, op, it):
    return len(o) > 2 and o[0] == op and o[1] == it and _cc_n(o) > 0


def _cc_cola(observation, action):
    """nueva cola de mercado o None (= dejar la accion de f29g)."""
    if not _CC_OK or not isinstance(action, dict):
        return None
    p = int(observation.get('player', 0)); s = int(observation.get('step', 0))
    st = _GS_STATE.get(p)
    if not st or not st.get('off') or not (_CC_CFG['t0'] <= s < _CC_CFG['t1']):
        return None
    raw = list(action.get('market') or [])
    if len(raw) > 10 or any(not isinstance(o, list) or not o for o in raw):
        return None
    q = [list(o) for o in raw]
    it = 'FERTILIZER'
    B = [o for o in q if _cc_es(o, 'BUY_PRODUCT', it)]
    if not B or any(len(o) > 1 and o[0] == 'SELL' and o[1] == it for o in q):
        return None
    if len(q) == 10 and q[9][0] == 'SELL':
        return None
    i0 = next(i for i, o in enumerate(q) if _cc_es(o, 'BUY_PRODUCT', it))
    m = sum(_cc_n(o) for o in B)
    rest = [o for o in q if not _cc_es(o, 'BUY_PRODUCT', it)]
    prices = observation['market']['prices']
    money = float(observation['farms'][p]['money'])
    pf = float(prices.get(it, 0))
    if pf <= 0:
        return None
    gasto = _cc_fijo(q) + sum(max(0, _cc_n(o)) * (float(prices.get(o[1], 0)) + 3) for o in q if o[0] == 'BUY_PRODUCT' and len(o) > 2)
    if money - gasto < 100:
        _CC_REPORT['bloqueos_caja'] += 1
        return None
    if any(o[0] == 'SELL' for o in q[:i0]):
        if _CC_CFG['fallback'] != 'fin':
            return None
        pad = 10 - len(rest) - len(B)
        if pad < 0:
            return None
        _CC_REPORT['finales'] += 1
        return rest + [[] for _ in range(pad)] + B
    ocupado = sum(max(0, int(v)) for v in projected_shed(dict(action, market=q), FarmView(observation)).values())
    x = int(min(_CC_CFG['xmax'], 100 - ocupado - m - 6, (money - gasto - _CC_CFG['reserva']) // (pf + _CC_CFG['margen_precio'])))
    if x < 3:
        return None
    nuevo = [['BUY_PRODUCT', it, x], ['SELL', it, x]] + rest
    pad = 10 - len(nuevo) - len(B)
    if pad < 0:
        return None
    _CC_REPORT['pares'] += 1; _CC_REPORT['unidades'] += x
    return nuevo + [[] for _ in range(pad)] + B


def guarda_cc_agent(observation, configuration=None):
    action = _CC_AGENT(observation, configuration)
    try:
        if int(observation.get('step', 0)) == 0:
            for k in _CC_REPORT:
                _CC_REPORT[k] = 0
        q = _cc_cola(observation, action)
        if q is None:
            return action
        nueva = dict(action, market=q[:10])
        p = int(observation.get('player', 0)); s = int(observation.get('step', 0))
        rs = _RACE_STATE.get(p)
        if rs is not None and rs.get('prev_action') is not None and rs.get('step') == s:
            rs['prev_action'] = nueva
        return nueva
    except Exception:
        try:
            _CC_REPORT['errores'] += 1
        except Exception:
            pass
    return action


guarda_cc_agent.telemetry = _CC_REPORT
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('base'); ap.add_argument('salida')
    ap.add_argument('--fallback', default='fin', choices=['fin', 'nada'])
    ap.add_argument('--xmax', type=int, default=90)
    ap.add_argument('--margen_precio', type=float, default=40.0)
    ap.add_argument('--reserva', type=float, default=500.0)
    ap.add_argument('--t0', type=int, default=144)
    ap.add_argument('--t1', type=int, default=700)
    a = ap.parse_args()
    b = Path(a.base).read_bytes()
    if b'# ==== Capa GS:' not in b or b'def guarda_agent(' not in b:
        sys.exit('la base no tiene la capa GS (f29g)')
    if b'# ==== Capa CC' in b:
        sys.exit('la base ya tiene una capa CC')
    cfg = dict(modo='ccF', fallback=a.fallback, xmax=a.xmax, margen_precio=a.margen_precio, reserva=a.reserva,
               t0=a.t0, t1=a.t1)
    out = b + CAPA.replace('__CFG__', json.dumps(cfg)).encode()
    Path(a.salida).write_bytes(out)
    ns = {}
    exec(compile(out.decode(), a.salida, 'exec'), ns)
    ultimo = [v for v in ns.values() if callable(v)][-1]
    assert ultimo.__name__ == 'guarda_cc_agent', ultimo
    assert ns['_CC_AGENT'].__name__ == 'guarda_agent' and ns['_CC_OK'] is True
    assert ns['_GS_OK'] and ns['_FR_PARENT'] is ns['_gs_conmutador']
    assert out[:len(b)] == b
    print(a.salida, cfg, 'sha', hashlib.sha256(out).hexdigest(), 'prefijo', hashlib.sha256(b).hexdigest()[:8])


if __name__ == '__main__':
    main()
