"""Capa CC3: contra-copia de FERTILIZER tras el disparo de GS (= capa CC2/ccF) + APAGADO PROPIO del par.

Parte de los bytes de f29g (final_29 + capa GS) y anade al final UNA capa cuyo ultimo callable,
`guarda_cc3_agent`, envuelve directamente a `guarda_agent`. Antes del disparo de GS la accion es exactamente la de
f29g (= final_29). Tras el disparo y mientras el par siga activo, la accion es exactamente la de f29g2_ccF
(sha 0666c714): mismas reglas, mismo X, mismas colocaciones (BUY FERT X en 0, SELL FERT X en 1, compra base en 9;
con ventas delante solo mueve la compra base al 9).

Apagado propio (nuevo). El revisor de ccF construyo un copiador en escalera (pares BUY/SELL 40/16/4 desde el
indice 0, patron real de porosyonok): su SELL de idx 1 va en lockstep con la nuestra y el par pierde
~0,2*c*(X-c) por paso (c = su trozo en idx 0/1). Tras cada paso en que CC puso su par, en el paso siguiente se
reutiliza la maquinaria exacta de GS (`_gs_gap`): simulacion exacta del mercado con NUESTRA cola final del paso y
un rival benigno (una orden por producto en cualquier indice) que explique el inventario observado; gap =
minimo benigno de nuestro dinero - dinero observado. Si gap > b (un golpe) o gap > g en k pasos con par, el par
queda desactivado el resto de la partida para ese jugador. En los datos de calibracion (semillas 5340040-43, 6
copiadores + 4 rivales con disparo forzado, 402 pasos con par) el gap coincide EXACTAMENTE con -P&L del par en un
paso (motor exacto, cinta rival fija): es el P&L del par deducido de la simulacion exacta.

Sondeo (--sonda, por defecto 45): la primera perdida contra la escalera llega con el primer par grande (X ~ 81 frente
a su trozo c = 40: -0,2*c*(X-c-1) ~ -320 propio, ~ -650 de margen) y el apagado solo la corta despues. Mientras el
par no este validado, X se topa en el nivel de sondeo; un solo golpe > g_sonda (20) apaga; un par topado (x >= tope)
con gap <= 0 valida el nivel y el tope sube al siguiente (o desaparece). Contra un par en lockstep con trozo c, el par
X pierde solo si X > c + 1, asi que el tope 45 detecta trozos c <= ~41 perdiendo como mucho ~0,2*c*(44-c).
Fuera de la fase de sondeo rigen b/g/k. Tras el apagado (--tras_off):
  fin   en los pasos en que ccF habria puesto el par, solo se mueve la compra base al indice 9 (ccF menos el par);
        los pasos 'fin' de ccF (ventas delante) siguen igual.
  nada  se vuelve a la accion de f29g (sin mover la compra base).

Opcion --redim (variante f29g3r; la salida por defecto no cambia): si el par topado del sondeo pierde (gap > g_sonda),
en vez de apagar se despeja el trozo c del par rival en lockstep de gap = 0,2*c*(X-1-c) (raiz mayor) y X queda fijo en
(c+1)//2, que gana 0,2*X*(c+1-X) si la hipotesis es cierta; cada par re-dimensionado se evalua y un golpe > g_res (10)
apaga el par. Sin raiz real (la perdida no la explica un par en lockstep) apaga igual que f29g3.

Seguridad: todo en try/except; ante cualquier error se devuelve la accion de f29g sin tocar. Estado por jugador
(_CC3_STATE[jugador]) que se reinicia al empezar partida (step 0 o step menor que el ultimo visto). Solo lee
_GS_STATE; actualiza _RACE_STATE['prev_action'] como las demas capas.

Uso: apilar_guarda_ms3.py <f29g.py> <salida.py> [--tras_off fin|nada] [--b 150] [--g 40] [--k 2] [--sonda 45] [--g_sonda 20] [--redim] [--g_res 10]
                          [--fallback fin|nada] [--xmax 90] [--margen_precio 40] [--reserva 500] [--t0 144] [--t1 700]
"""
import argparse, hashlib, json, sys
from pathlib import Path

CAPA = r'''

# ==== Capa CC3: contra-copia de FERTILIZER tras el disparo de GS + apagado propio del par (kaggriculture local, 2026-09-29): __CFG__ ====
_CC3_CFG = __CFG__
_CC3_AGENT = [v for v in list(globals().values()) if callable(v)][-1]
import time as _cc3_time
_CC3_REPORT = dict(pares=0, unidades=0, finales=0, finales_off=0, bloqueos_caja=0, errores=0, errores_eval=0, evals=0,
                   abstenciones=0, golpes=0, apagados=0, apagados_sonda=0, validaciones=0, topados=0, sin_foto=0,
                   max_ms=0.0, jugadores={})
_CC3_STATE = {}
_CC3_FIJO = {'GOOSE': 300, 'COW': 400, 'SHEEP': 500, 'WHEAT': 10, 'CARROT': 20, 'TOMATO': 50, 'STRAWBERRY': 100, 'MELON': 80}
_CC3_OK = bool(getattr(_CC3_AGENT, '__name__', '') == 'guarda_agent' and isinstance(globals().get('_GS_STATE'), dict)
               and globals().get('_GS_OK') and callable(globals().get('_gs_gap')) and callable(globals().get('_gs_conf_ok'))
               and callable(globals().get('_gs_price')))


def _cc3_n(o):
    try:
        return int(o[2])
    except Exception:
        return 0


def _cc3_fijo(q):
    c = 0.0
    for o in q:
        if o[0] == 'HIRE':
            c += 100
        elif o[0] == 'BUY_LAND':
            c += 4000
        elif o[0] in ('BUY_SEED', 'BUY_ANIMAL') and len(o) > 2:
            c += max(0, _cc3_n(o)) * _CC3_FIJO.get(o[1], 500)
    return c


def _cc3_es(o, op, it):
    return len(o) > 2 and o[0] == op and o[1] == it and _cc3_n(o) > 0


def _cc3_estado(p):
    st = _CC3_STATE.get(p)
    if st is None:
        st = _CC3_STATE[p] = dict(prev=None, off=False, golpes=0, off_step=-1, last=-1, nivel=0, log=[])
        _CC3_REPORT['jugadores'][p] = st
    return st


def _cc3_antes(observation):
    """reinicio de partida y evaluacion del par del paso anterior (gap de GS)."""
    s = int(observation.get('step', 0)); p = int(observation.get('player', 0))
    st = _cc3_estado(p)
    if s == 0 or s < st['last']:
        st.update(prev=None, off=False, golpes=0, off_step=-1, nivel=0, log=[])
    st['last'] = s
    pv = st['prev']; st['prev'] = None
    if st['off'] or pv is None or pv['step'] != s - 1:
        return
    t0 = _cc3_time.perf_counter()
    try:
        gap = _gs_gap(pv, observation['market']['inventory'], observation['farms'][p]['money'], t0)
    except Exception:
        gap = None; _CC3_REPORT['errores_eval'] += 1
    dt = (_cc3_time.perf_counter() - t0) * 1000.0
    _CC3_REPORT['evals'] += 1
    _CC3_REPORT['max_ms'] = max(_CC3_REPORT['max_ms'], round(dt, 3))
    if len(st['log']) < 400:
        st['log'].append((pv['step'], pv['x'], pv['cap'], None if gap is None else round(gap, 3), round(dt, 2)))
    if gap is None:
        _CC3_REPORT['abstenciones'] += 1
        return
    if pv['cap'] is not None:
        # fase de sondeo: un solo golpe > g_sonda apaga; un par topado (x >= tope) que no pierde valida el nivel
        if gap > _CC3_CFG['g_sonda']:
            st['off'] = True; _CC3_REPORT['apagados_sonda'] += 1
        elif pv['x'] >= pv['cap'] and gap <= 0 and st['nivel'] == pv['nivel']:
            st['nivel'] += 1; _CC3_REPORT['validaciones'] += 1
    elif gap > _CC3_CFG['b']:
        st['off'] = True
    elif gap > _CC3_CFG['g']:
        st['golpes'] += 1; _CC3_REPORT['golpes'] += 1
        if st['golpes'] >= _CC3_CFG['k']:
            st['off'] = True
    if st['off']:
        st['off_step'] = s; _CC3_REPORT['apagados'] += 1


def _cc3_cola(observation, action, st):
    """(nueva cola, tipo) o (None, None) = dejar la accion de f29g. tipo: 'par' | 'fin' | 'fin_off'.
    Mientras el par este activo, identico a _cc_cola de f29g2_ccF."""
    if not _CC3_OK or not isinstance(action, dict):
        return None, None
    p = int(observation.get('player', 0)); s = int(observation.get('step', 0))
    gs = _GS_STATE.get(p)
    if not gs or not gs.get('off') or not (_CC3_CFG['t0'] <= s < _CC3_CFG['t1']):
        return None, None
    if st['off'] and _CC3_CFG['tras_off'] != 'fin':
        return None, None
    raw = list(action.get('market') or [])
    if len(raw) > 10 or any(not isinstance(o, list) or not o for o in raw):
        return None, None
    q = [list(o) for o in raw]
    it = 'FERTILIZER'
    B = [o for o in q if _cc3_es(o, 'BUY_PRODUCT', it)]
    if not B or any(len(o) > 1 and o[0] == 'SELL' and o[1] == it for o in q):
        return None, None
    if len(q) == 10 and q[9][0] == 'SELL':
        return None, None
    i0 = next(i for i, o in enumerate(q) if _cc3_es(o, 'BUY_PRODUCT', it))
    m = sum(_cc3_n(o) for o in B)
    rest = [o for o in q if not _cc3_es(o, 'BUY_PRODUCT', it)]
    prices = observation['market']['prices']
    money = float(observation['farms'][p]['money'])
    pf = float(prices.get(it, 0))
    if pf <= 0:
        return None, None
    gasto = _cc3_fijo(q) + sum(max(0, _cc3_n(o)) * (float(prices.get(o[1], 0)) + 3) for o in q if o[0] == 'BUY_PRODUCT' and len(o) > 2)
    if money - gasto < 100:
        _CC3_REPORT['bloqueos_caja'] += 1
        return None, None
    if any(o[0] == 'SELL' for o in q[:i0]):
        if _CC3_CFG['fallback'] != 'fin':
            return None, None
        pad = 10 - len(rest) - len(B)
        if pad < 0:
            return None, None
        _CC3_REPORT['finales'] += 1
        return rest + [[] for _ in range(pad)] + B, 'fin'
    ocupado = sum(max(0, int(v)) for v in projected_shed(dict(action, market=q), FarmView(observation)).values())
    x = int(min(_CC3_CFG['xmax'], 100 - ocupado - m - 6, (money - gasto - _CC3_CFG['reserva']) // (pf + _CC3_CFG['margen_precio'])))
    if x < 3:
        return None, None
    cap = None; topado = False
    if not st['off'] and st['nivel'] < len(_CC3_CFG['sonda']):
        cap = int(_CC3_CFG['sonda'][st['nivel']])
        if x > cap:
            x = cap; topado = True
    nuevo = [['BUY_PRODUCT', it, x], ['SELL', it, x]] + rest
    pad = 10 - len(nuevo) - len(B)
    if pad < 0:
        return None, None
    if st['off']:
        _CC3_REPORT['finales_off'] += 1
        return rest + [[] for _ in range(pad + 2)] + B, 'fin_off'
    _CC3_REPORT['pares'] += 1; _CC3_REPORT['unidades'] += x; _CC3_REPORT['topados'] += int(topado)
    st['_x'] = x; st['_cap'] = cap
    return nuevo + [[] for _ in range(pad)] + B, 'par'


def _cc3_foto(observation, configuration, action, q, st):
    """foto del paso con par, en el formato exacto de _gs_despues, para evaluarlo en el paso siguiente."""
    if not _gs_conf_ok(configuration):
        _CC3_REPORT['sin_foto'] += 1
        return
    s = int(observation.get('step', 0)); p = int(observation.get('player', 0))
    mk = observation['market']
    inv = {k: int(v) for k, v in dict(mk['inventory']).items()}
    precios = dict(mk['prices'])
    if any(it not in inv or _gs_price(it, inv[it]) != int(precios.get(it, -1)) for it in _GS_PRODUCTS):
        _CC3_REPORT['sin_foto'] += 1
        return
    farm = observation['farms'][p]
    q = [list(o) if isinstance(o, list) else o for o in q[:10]]
    shed = projected_shed(dict(action, market=[o for o in q if o]), FarmView(observation))
    st['prev'] = dict(step=s, kind='CC', x=st.get('_x'), cap=st.get('_cap'), nivel=st['nivel'], market=q, inv=inv, money=float(farm['money']),
                      hires=int(farm.get('hires_today', 0) or 0), nquad=len(farm.get('unlocked_quadrants') or ['NW']),
                      shed={k: max(0, int(v)) for k, v in dict(shed).items()},
                      shops=list(observation['town']['unlocked_shops']))


def guarda_cc3_agent(observation, configuration=None):
    try:
        _cc3_antes(observation)
    except Exception:
        try:
            _CC3_REPORT['errores'] += 1
        except Exception:
            pass
    action = _CC3_AGENT(observation, configuration)
    try:
        s = int(observation.get('step', 0)); p = int(observation.get('player', 0))
        if s == 0:
            for k in _CC3_REPORT:
                if k != 'jugadores':
                    _CC3_REPORT[k] = 0 if k != 'max_ms' else 0.0
        st = _cc3_estado(p)
        q, tipo = _cc3_cola(observation, action, st)
        if q is None:
            return action
        nueva = dict(action, market=q[:10])
        if tipo == 'par':
            try:
                _cc3_foto(observation, configuration, nueva, q, st)
            except Exception:
                st['prev'] = None; _CC3_REPORT['sin_foto'] += 1
        rs = _RACE_STATE.get(p)
        if rs is not None and rs.get('prev_action') is not None and rs.get('step') == s:
            rs['prev_action'] = nueva
        return nueva
    except Exception:
        try:
            _CC3_REPORT['errores'] += 1
        except Exception:
            pass
    return action


guarda_cc3_agent.telemetry = _CC3_REPORT
'''


# Parches opcionales (--redim): se aplican sobre CAPA solo con --redim, asi que la salida por defecto (f29g3) no cambia.
# Re-dimensionado: si el par topado del sondeo pierde (gap > g_sonda), en vez de apagar se ajusta el modelo de un par
# rival en lockstep (BUY c en idx 0 / SELL c en idx 1): P&L = s*min(X,c)*(c+1-X), s = pendiente del precio de FERT
# (0,2 por unidad). Con gap observado a X se despeja c (raiz mayor) y se fija X = (c+1)//2, que maximiza el P&L si la
# hipotesis es cierta. Cada par re-dimensionado se evalua igual; un golpe > g_res apaga el par (tras_off).
REDIM = [
    ("""_CC3_REPORT = dict(pares=0,""", """_CC3_REPORT = dict(redimensionados=0, apagados_res=0, pares=0,"""),
    ("""nivel=0, log=[])""", """nivel=0, xfix=None, log=[])"""),
    ("""def _cc3_antes(observation):""", """def _cc3_xfix(x, gap):
    """ + '"""' + """trozo c de un par rival en lockstep que explica gap = s*c*(x-1-c); raiz mayor; X = (c+1)//2 o None.""" + '"""' + """
    base, T, bf, bt, af, at = _GS_PARAMS['FERTILIZER']
    if bf != 'linear':
        return None
    sl = bt * base / float(T)
    if sl <= 0:
        return None
    disc = (x - 1) ** 2 - 4.0 * gap / sl
    if disc < 0:
        return None
    c = ((x - 1) + disc ** 0.5) / 2.0
    xf = int((c + 1) // 2)
    return xf if xf >= 3 else None


def _cc3_antes(observation):"""),
    ("""    if pv['cap'] is not None:
        # fase de sondeo""", """    if pv.get('xfix') is not None:
        if gap > _CC3_CFG['g_res']:
            st['off'] = True; _CC3_REPORT['apagados_res'] += 1
    elif pv['cap'] is not None:
        # fase de sondeo"""),
    ("""        if gap > _CC3_CFG['g_sonda']:
            st['off'] = True; _CC3_REPORT['apagados_sonda'] += 1""", """        if gap > _CC3_CFG['g_sonda']:
            xf = _cc3_xfix(pv['x'], gap)
            if xf is None:
                st['off'] = True; _CC3_REPORT['apagados_sonda'] += 1
            else:
                st['xfix'] = xf; _CC3_REPORT['redimensionados'] += 1"""),
    ("""            x = cap; topado = True
""", """            x = cap; topado = True
    if not st['off'] and st.get('xfix') is not None and x > st['xfix']:
        x = st['xfix']
"""),
    ("""cap=st.get('_cap'), nivel=st['nivel'],""", """cap=st.get('_cap'), nivel=st['nivel'], xfix=st.get('xfix'),"""),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('base'); ap.add_argument('salida')
    ap.add_argument('--tras_off', default='fin', choices=['fin', 'nada'])
    ap.add_argument('--b', type=float, default=150.0)
    ap.add_argument('--g', type=float, default=40.0)
    ap.add_argument('--k', type=int, default=2)
    ap.add_argument('--sonda', default='45', help="topes de X crecientes durante el sondeo, separados por comas ('' = sin sondeo)")
    ap.add_argument('--g_sonda', type=float, default=20.0)
    ap.add_argument('--fallback', default='fin', choices=['fin', 'nada'])
    ap.add_argument('--xmax', type=int, default=90)
    ap.add_argument('--margen_precio', type=float, default=40.0)
    ap.add_argument('--reserva', type=float, default=500.0)
    ap.add_argument('--t0', type=int, default=144)
    ap.add_argument('--t1', type=int, default=700)
    ap.add_argument('--redim', action='store_true', help='tras un golpe en el sondeo, re-dimensionar X frente a la escalera en vez de apagar')
    ap.add_argument('--g_res', type=float, default=10.0)
    a = ap.parse_args()
    b = Path(a.base).read_bytes()
    if b'# ==== Capa GS:' not in b or b'def guarda_agent(' not in b:
        sys.exit('la base no tiene la capa GS (f29g)')
    if b'# ==== Capa CC' in b:
        sys.exit('la base ya tiene una capa CC')
    sonda = [int(v) for v in a.sonda.split(',') if v.strip()]
    assert sonda == sorted(sonda) and all(3 <= v < a.xmax for v in sonda), sonda
    cfg = dict(modo='cc3', tras_off=a.tras_off, b=a.b, g=a.g, k=a.k, sonda=sonda, g_sonda=a.g_sonda, fallback=a.fallback, xmax=a.xmax,
               margen_precio=a.margen_precio, reserva=a.reserva, t0=a.t0, t1=a.t1)
    capa = CAPA
    if a.redim:
        assert sonda, '--redim necesita sondeo'
        cfg.update(redim=1, g_res=a.g_res)
        for x, y in REDIM:
            n = capa.count(x)
            assert n == (2 if x == 'nivel=0, log=[])' else 1), (x, n)
            capa = capa.replace(x, y)
    out = b + capa.replace('__CFG__', json.dumps(cfg)).encode()
    Path(a.salida).write_bytes(out)
    ns = {}
    exec(compile(out.decode(), a.salida, 'exec'), ns)
    ultimo = [v for v in ns.values() if callable(v)][-1]
    assert ultimo.__name__ == 'guarda_cc3_agent', ultimo
    assert ns['_CC3_AGENT'].__name__ == 'guarda_agent' and ns['_CC3_OK'] is True
    assert ns['_GS_OK'] and ns['_FR_PARENT'] is ns['_gs_conmutador']
    assert out[:len(b)] == b
    print(a.salida, cfg, 'sha', hashlib.sha256(out).hexdigest(), 'prefijo', hashlib.sha256(b).hexdigest()[:8])


if __name__ == '__main__':
    main()
