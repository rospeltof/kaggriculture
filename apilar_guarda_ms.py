"""Capa GS: guarda online contra copiadores de MS/MSS (compra-reventa en el mismo paso).

Hallazgo (133 replays de final_29, FINAL29_LADDER_0929a): rivales recientes copian el truco de MS/MSS.
Compran X de mas pronto (indice 0) y revenden X en un indice <= 8, antes de nuestra reventa en el 9;
nos quitan de 1.100 a 6.500 $ por partida. No reaccionan a nosotros: actuan segun su propia cinta.

Deteccion (solo lee; guard_senal validada sobre 133 partidas: 0/124 falsos positivos, 8/8 detectados):
tras cada paso t en que nuestra accion FINAL lleva la firma MS (10 ordenes; en el indice 9 una SELL de
WHEAT/FERTILIZER con una BUY_PRODUCT del mismo producto en 0-8 y ninguna SELL) o MSS (lo simetrico), al
recibir la observacion de t+1 se simula exactamente el mercado de t contra un rival "benigno" (a lo sumo
una orden por producto, en cualquier indice, con la cantidad que reproduce el inventario observado).
gap = minimo benigno de nuestro dinero - dinero observado. Se apaga con gap > B (150), o al K-esimo (2)
golpe con gap > G_MS (20) en paso MS o > G_MSS (60) en paso MSS. Abstencion (sin golpe) si nuestra lista
falla por caja, si ninguna hipotesis cuadra, si se pasa el presupuesto de tiempo o si los precios de la
observacion no coinciden con la formula por defecto del motor.

Accion al disparar: MS y MSS dejan de actuar el resto de la partida. Mecanismo: en final_29 la cadena es
frontrun_agent -> _FR_PARENT = MSS(MS(BP(XP(base)))), y frontrun_agent busca `_FR_PARENT` en globals en
cada llamada. La capa localiza por los cierres (`padre`) la funcion BP que MS envuelve y reasigna
`_FR_PARENT` a un conmutador: sin disparo llama a MSS (cadena intacta, acciones identicas a la base);
tras disparar, a BP (lo que MS habria recibido; equivale a final_xc1_sa_bp desde ese paso). La nueva
funcion `guarda_agent` es el ultimo callable del modulo y envuelve a frontrun_agent. Todo el codigo nuevo
va en try/except: ante error, la accion es la de la base. Estado por jugador; se reinicia con step == 0 o
step menor que el anterior.

No toca nada del fichero base: salida = base + capa. Uso:
  apilar_guarda_ms.py <base.py> <salida.py> [--b 150] [--g_ms 20] [--g_mss 60] [--k 2] [--t0 144] [--t1 700]
                      [--presupuesto_ms 60]
"""
import argparse, hashlib, json, sys
from pathlib import Path

CAPA = r'''

# ==== Capa GS: guarda anti-copiadores de MS/MSS (kaggriculture local, 2026-09-29): __CFG__ ====
_GS_CFG = __CFG__
_GS_AGENT = [v for v in list(globals().values()) if callable(v)][-1]
import math as _gs_math
import time as _gs_time
_GS_REPORT = dict(evals=0, abstenciones=0, golpes=0, disparos=0, precio_distinto=0, errores=0, max_ms=0.0,
                  estructura_ok=False, jugadores={})
_GS_STATE = {}
_GS_PRODUCTS = ('WHEAT', 'CARROT', 'TOMATO', 'STRAWBERRY', 'MELON', 'EGG', 'MILK', 'WOOL', 'FERTILIZER')
_GS_RACE = ('WHEAT', 'FERTILIZER')
_GS_PARAMS = {'WHEAT': (25, 400, 'sqrt', 0.8, 'log', 0.2), 'CARROT': (35, 450, 'hinge', 1.0, 'sqrt', 0.7),
              'TOMATO': (60, 200, 'hinge', 0.4, 'sqrt', 0.6), 'STRAWBERRY': (120, 100, 'sqrt', 0.7, 'linear', 1.6),
              'MELON': (250, 300, 'log', 0.2, 'sq', 3.6), 'EGG': (50, 332, 'hinge', 0.4, 'log', 0.2),
              'MILK': (160, 122, 'sqrt', 0.6, 'linear', 1.6), 'WOOL': (200, 105, 'log', 0.2, 'sq', 3.2),
              'FERTILIZER': (100, 200, 'linear', 0.4, 'linear', 0.4)}
_GS_I0 = 10000
_GS_SEED = {'WHEAT': 10, 'CARROT': 20, 'TOMATO': 50, 'STRAWBERRY': 100, 'MELON': 80}
_GS_ANIMAL = {'GOOSE': 300, 'COW': 400, 'SHEEP': 500}
_GS_LAND = (1000, 2000, 4000)
_GS_SHOPS = {'BAKERY': ('EGG', 'WHEAT'), 'PIZZA_SHOP': ('MILK', 'TOMATO', 'WHEAT'), 'BRUNCH_SPOT': ('EGG', 'WHEAT', 'STRAWBERRY'),
             'YARN_STORE': ('WOOL',), 'ICE_CREAM_SHOP': ('STRAWBERRY', 'MILK', 'WHEAT'), 'PET_CAFE': ('CARROT',),
             'SMOOTHIE_SHOP': ('STRAWBERRY', 'MILK'), 'FARMERS_MARKET': ('WHEAT', 'CARROT', 'TOMATO', 'STRAWBERRY')}
_GS_CAP = 100
_GS_CONF_DEF = {'shedCapacity': 100, 'maxMarketOrdersPerTurn': 10, 'farmHandCostMult': 1,
                'townShopSellInterval': 4, 'townCenterSellInterval': 24}
_GS_PC = {}
_GS_FL = {}


def _gs_shape(func, x, T):
    x = max(0.0, x)
    if func == 'linear':
        return x
    if func == 'sq':
        return x * x
    if func == 'sqrt':
        return _gs_math.sqrt(x)
    if func == 'log':
        return _gs_math.log(1.0 + x)
    if func == 'hinge':
        u = x / T
        return u + 8.0 * max(0.0, u - 1.0) ** 2
    return x


def _gs_price(item, inv):
    k = (item, inv)
    v = _GS_PC.get(k)
    if v is None:
        base, T, bf, bt, af, at = _GS_PARAMS[item]
        if inv < _GS_I0:
            pr = base + bt * base / _gs_shape(bf, T, T) * _gs_shape(bf, _GS_I0 - inv, T)
        else:
            pr = base - at * base / _gs_shape(af, T, T) * _gs_shape(af, inv - _GS_I0, T)
        v = max(1, int(round(pr)))
        if len(_GS_PC) > 100000:
            _GS_PC.clear()
        _GS_PC[k] = v
    return v


def _gs_floor(item):
    """primer inventario con precio <= 1 (vender ahi no suma oferta); None si nunca."""
    if item not in _GS_FL:
        lo, hi = _GS_I0, _GS_I0 + 200000
        if _gs_price(item, hi) > 1:
            _GS_FL[item] = None
        else:
            while lo < hi:
                m = (lo + hi) // 2
                if _gs_price(item, m) <= 1:
                    hi = m
                else:
                    lo = m + 1
            _GS_FL[item] = lo
    return _GS_FL[item]


def _gs_parse(o):
    """= kaggriculture._parse_order."""
    if not isinstance(o, list) or not o:
        return None
    if o[0] in ('HIRE', 'BUY_LAND'):
        return [o[0], None, 1]
    if o[0] in ('BUY_SEED', 'BUY_PRODUCT', 'BUY_ANIMAL', 'SELL') and len(o) >= 3:
        try:
            n = int(o[2])
        except (TypeError, ValueError):
            return None
        return [o[0], o[1], n] if n > 0 else None
    return None


def _gs_kind(q):
    """'MS' / 'MSS' si la lista FINAL lleva la firma (10 ordenes, indice 9 = pata de reventa/recompra)."""
    if len(q) != 10 or not (isinstance(q[9], list) and len(q[9]) >= 3) or q[9][1] not in _GS_RACE:
        return None
    op, it = q[9][0], q[9][1]
    def mismo(o, x):
        return isinstance(o, list) and len(o) > 1 and o[0] == x and o[1] == it
    if op == 'SELL' and any(mismo(o, 'BUY_PRODUCT') for o in q[:9]) and not any(mismo(o, 'SELL') for o in q[:9]):
        return 'MS'
    if op == 'BUY_PRODUCT' and any(mismo(o, 'SELL') for o in q[:9]) and not any(mismo(o, 'BUY_PRODUCT') for o in q[:9]):
        return 'MSS'
    return None


def _gs_town(shops, step):
    out = {}
    if step % 4 == 0:
        for s in shops:
            ps = _GS_SHOPS.get(s, ())
            for it in ps:
                out[it] = out.get(it, 0) + (2 if len(ps) == 1 else 1)
    if step % 24 == 0:
        for it in _GS_PRODUCTS:
            if it != 'FERTILIZER':
                out[it] = out.get(it, 0) + 1
    return out


def _gs_base_sim(snap):
    """nuestra lista sola (rival vacio), logica exacta del motor -> (dinero, {idx: [op, item, ejecutadas, fallo]})."""
    money, hires, nq = snap['money'], snap['hires'], snap['nquad']
    inv = dict(snap['inv']); shed = dict(snap['shed']); tot = sum(shed.values()); log = {}
    for i, o in enumerate(snap['market'][:10]):
        p = _gs_parse(o)
        if p is None:
            continue
        op, it, n = p
        log[i] = [op, it, 0, None]
        if op == 'HIRE':
            a, b = 1, 1
            for _ in range(hires):
                a, b = b, a + b
            if money >= a:
                money -= a; hires += 1; log[i][2] = 1
            else:
                log[i][3] = 'cash'
            continue
        if op == 'BUY_LAND':
            k = nq - 1
            if k < len(_GS_LAND):
                if money >= _GS_LAND[k]:
                    money -= _GS_LAND[k]; nq += 1; log[i][2] = 1
                else:
                    log[i][3] = 'cash'
            continue
        for _ in range(n):
            if op == 'SELL' and it in _GS_PARAMS:
                if shed.get(it, 0) <= 0:
                    log[i][3] = 'stock'; break
                q = _gs_price(it, inv[it]); shed[it] -= 1; tot -= 1; money += q
                if q > 1:
                    inv[it] += 1
            elif op == 'BUY_PRODUCT' and it in _GS_RACE:
                q = _gs_price(it, inv[it] - 1)
                if money < q:
                    log[i][3] = 'cash'; break
                if tot >= _GS_CAP:
                    log[i][3] = 'shed'; break
                money -= q; shed[it] = shed.get(it, 0) + 1; tot += 1; inv[it] -= 1
            elif op == 'BUY_SEED' and it in _GS_SEED:
                if money < _GS_SEED[it]:
                    log[i][3] = 'cash'; break
                money -= _GS_SEED[it]
            elif op == 'BUY_ANIMAL' and it in _GS_ANIMAL:
                if money < _GS_ANIMAL[it]:
                    log[i][3] = 'cash'; break
                if tot >= _GS_CAP:
                    log[i][3] = 'shed'; break
                money -= _GS_ANIMAL[it]; shed[it] = shed.get(it, 0) + 1; tot += 1
            else:
                log[i][3] = 'malformed'; break
            log[i][2] += 1
    return money, log


def _gs_psim(item, inv, orders, stock, j, s):
    """mercado de UN producto: nuestras ordenes [(idx, op, ejecutadas)] + rival con UNA orden de s unidades
    (s>0 SELL, s<0 BUY) en el indice j; lockstep exacto, resto del rival en bloque."""
    cash = 0; fl = _gs_floor(item); om = {o[0]: o for o in orders}
    for i in sorted(set(list(om) + ([j] if s else []))):
        o = om.get(i); oop = o[1] if o else None; oq = o[2] if o else 0
        rn = abs(s) if (s and i == j) else 0; rsell = s > 0
        while oq > 0 and rn > 0:
            qo = _gs_price(item, inv) if oop == 'SELL' else _gs_price(item, inv - 1)
            qr = _gs_price(item, inv) if rsell else _gs_price(item, inv - 1)
            if oop == 'SELL':
                if stock <= 0:
                    oq = 0
                else:
                    stock -= 1; cash += qo; oq -= 1
                    if qo > 1:
                        inv += 1
            else:
                cash -= qo; stock += 1; inv -= 1; oq -= 1
            inv += (1 if qr > 1 else 0) if rsell else -1
            rn -= 1
        while oq > 0:
            if oop == 'SELL':
                if stock <= 0:
                    break
                q = _gs_price(item, inv); stock -= 1; cash += q; oq -= 1
                if q > 1:
                    inv += 1
            else:
                q = _gs_price(item, inv - 1); cash -= q; stock += 1; inv -= 1; oq -= 1
        if rn > 0:
            if not rsell:
                inv -= rn
            elif fl is None:
                inv += rn
            elif inv < fl:
                inv = min(inv + rn, fl)
    return inv, cash


def _gs_solve(item, inv0, orders, stock, j, target):
    buy_ok = item in _GS_RACE
    def f(s):
        return _gs_psim(item, inv0, orders, stock, j, s)[0]
    s0 = target - f(0)
    if (s0 >= 0 or buy_ok) and f(s0) == target and f(s0 + 1) != target and (f(s0 - 1) != target or (s0 == 0 and not buy_ok)):
        return s0, s0
    lo, hi = (-3000 - abs(s0) if buy_ok else 0), 3000 + abs(s0)
    if f(lo) > target or f(hi) < target:
        return None
    a, b = lo, hi
    while a < b:
        m = (a + b) // 2
        if f(m) >= target:
            b = m
        else:
            a = m + 1
    if f(a) != target:
        return None
    s_lo, a, b = a, a, hi
    while a < b:
        m = (a + b + 1) // 2
        if f(m) <= target:
            a = m
        else:
            b = m - 1
    return s_lo, min(a, s_lo + 1000)


def _gs_gap(snap, inv1, money1, t0):
    """min sobre rivales benignos de nuestro dinero - dinero observado. None = abstenerse."""
    presupuesto = _GS_CFG['presupuesto_ms'] / 1000.0
    m_base, log = _gs_base_sim(snap)
    if any(v[3] == 'cash' for v in log.values()):
        return None
    por = {}
    for i, (op, it, n, _) in log.items():
        if n > 0 and ((op == 'SELL' and it in _GS_PARAMS) or (op == 'BUY_PRODUCT' and it in _GS_RACE)):
            por.setdefault(it, []).append((i, op, n))
    tc = _gs_town(snap['shops'], snap['step'])
    total = m_base
    for it, orders in por.items():
        stock = int(snap['shed'].get(it, 0)); inv0 = int(snap['inv'][it])
        total -= _gs_psim(it, inv0, orders, stock, 0, 0)[1]
        target = int(inv1[it]) + tc.get(it, 0)
        K = [o[0] for o in orders]; vistos = set(); best = None
        for j in range(10):
            key = (sum(1 for k in K if k < j), j in K)
            if key in vistos:
                continue
            vistos.add(key)
            iv = _gs_solve(it, inv0, orders, stock, j, target)
            if iv is not None:
                for s in set(iv):
                    c = _gs_psim(it, inv0, orders, stock, j, s)[1]
                    best = c if best is None else min(best, c)
            if _gs_time.perf_counter() - t0 > presupuesto:
                return None
        if best is None:
            return None
        total += best
    return total - float(money1)


def _gs_cell(fn, nombre):
    try:
        return fn.__closure__[fn.__code__.co_freevars.index(nombre)].cell_contents
    except Exception:
        return None


# cadena de final_29: frontrun_agent -> _FR_PARENT = MSS(MS(BP(...))). _GS_SIN = primera capa bajo MS/MSS.
_GS_CON = globals().get('_FR_PARENT')
_GS_SIN = _GS_CON
_GS_SALTADAS = []
while callable(_GS_SIN) and getattr(_GS_SIN, '__name__', '') in ('mini_spec_venta', 'mini_spec'):
    _GS_SALTADAS.append(_GS_SIN.__name__)
    _GS_SIN = _gs_cell(_GS_SIN, 'padre')
_GS_OK = bool(getattr(_GS_AGENT, '__name__', '') == 'frontrun_agent' and _GS_SALTADAS and callable(_GS_SIN)
              and getattr(_GS_SIN, '__name__', '') not in ('mini_spec_venta', 'mini_spec'))
_GS_REPORT['estructura_ok'] = _GS_OK
_GS_REPORT['saltadas'] = list(_GS_SALTADAS)


def _gs_estado(p):
    st = _GS_STATE.get(p)
    if st is None:
        st = _GS_STATE[p] = dict(prev=None, golpes=0, off=False, off_step=-1, last=-1, log=[])
        _GS_REPORT['jugadores'][p] = st
    return st


def _gs_conmutador(observation, configuration=None):
    off = False
    try:
        st = _GS_STATE.get(int(observation.get('player', 0)))
        off = bool(st and st['off'])
    except Exception:
        off = False
    if off:
        return _GS_SIN(observation, configuration)
    return _GS_CON(observation, configuration)


if _GS_OK:
    _FR_PARENT = _gs_conmutador


def _gs_conf_ok(configuration):
    if configuration is None:
        return True
    for k, v in _GS_CONF_DEF.items():
        try:
            x = configuration.get(k, v) if hasattr(configuration, 'get') else getattr(configuration, k, v)
        except Exception:
            x = v
        if x is not None and int(x) != v:
            return False
    return True


def _gs_antes(observation, configuration):
    s = int(observation.get('step', 0)); p = int(observation.get('player', 0))
    st = _gs_estado(p)
    if s == 0 or s < st['last']:
        st.update(prev=None, golpes=0, off=False, off_step=-1, log=[])
    st['last'] = s
    pv = st['prev']; st['prev'] = None
    if st['off'] or pv is None or pv['step'] != s - 1:
        return
    t0 = _gs_time.perf_counter()
    try:
        gap = _gs_gap(pv, observation['market']['inventory'], observation['farms'][p]['money'], t0)
    except Exception:
        gap = None; _GS_REPORT['errores'] += 1
    dt = (_gs_time.perf_counter() - t0) * 1000.0
    _GS_REPORT['evals'] += 1
    _GS_REPORT['max_ms'] = max(_GS_REPORT['max_ms'], round(dt, 3))
    if len(st['log']) < 400:
        st['log'].append((pv['step'], pv['kind'], None if gap is None else round(gap, 3), round(dt, 2)))
    if gap is None:
        _GS_REPORT['abstenciones'] += 1
        return
    if gap > _GS_CFG['b']:
        st['off'] = True
    elif gap > (_GS_CFG['g_ms'] if pv['kind'] == 'MS' else _GS_CFG['g_mss']):
        st['golpes'] += 1; _GS_REPORT['golpes'] += 1
        if st['golpes'] >= _GS_CFG['k']:
            st['off'] = True
    if st['off']:
        st['off_step'] = s; _GS_REPORT['disparos'] += 1


def _gs_despues(observation, configuration, action):
    s = int(observation.get('step', 0)); p = int(observation.get('player', 0))
    st = _gs_estado(p)
    st['prev'] = None
    if not _GS_OK or st['off'] or not (_GS_CFG['t0'] <= s < _GS_CFG['t1']) or not isinstance(action, dict):
        return
    q = [list(o) if isinstance(o, list) else o for o in list(action.get('market') or [])[:10]]
    kind = _gs_kind(q)
    if not kind or not _gs_conf_ok(configuration):
        return
    mk = observation['market']
    inv = {k: int(v) for k, v in dict(mk['inventory']).items()}
    precios = dict(mk['prices'])
    if any(it not in inv or _gs_price(it, inv[it]) != int(precios.get(it, -1)) for it in _GS_PRODUCTS):
        _GS_REPORT['precio_distinto'] += 1
        return
    farm = observation['farms'][p]
    shed = projected_shed(dict(action, market=[o for o in q if o]), FarmView(observation))
    st['prev'] = dict(step=s, kind=kind, market=q, inv=inv, money=float(farm['money']),
                      hires=int(farm.get('hires_today', 0) or 0), nquad=len(farm.get('unlocked_quadrants') or ['NW']),
                      shed={k: max(0, int(v)) for k, v in dict(shed).items()},
                      shops=list(observation['town']['unlocked_shops']))


def guarda_agent(observation, configuration=None):
    try:
        _gs_antes(observation, configuration)
    except Exception:
        _GS_REPORT['errores'] += 1
    action = _GS_AGENT(observation, configuration)
    try:
        _gs_despues(observation, configuration, action)
    except Exception:
        _GS_REPORT['errores'] += 1
    return action


guarda_agent.telemetry = _GS_REPORT
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('base'); ap.add_argument('salida')
    ap.add_argument('--b', type=float, default=150.0)
    ap.add_argument('--g_ms', type=float, default=20.0)
    ap.add_argument('--g_mss', type=float, default=60.0)
    ap.add_argument('--k', type=int, default=2)
    ap.add_argument('--t0', type=int, default=144)
    ap.add_argument('--t1', type=int, default=700)
    ap.add_argument('--presupuesto_ms', type=float, default=60.0)
    a = ap.parse_args()
    b = Path(a.base).read_bytes()
    for marca in (b'# ==== Capa FR:', b'# ==== Capa MS:', b'# ==== Capa MSS:', b'def frontrun_agent('):
        if marca not in b:
            sys.exit(f'la base no tiene {marca!r}: la guarda solo sabe envolver la cadena de final_29')
    if b'# ==== Capa GS:' in b:
        sys.exit('la base ya tiene una capa GS')
    cfg = dict(b=a.b, g_ms=a.g_ms, g_mss=a.g_mss, k=a.k, t0=a.t0, t1=a.t1, presupuesto_ms=a.presupuesto_ms)
    out = b + CAPA.replace('__CFG__', json.dumps(cfg)).encode()
    Path(a.salida).write_bytes(out)
    # comprobacion de carga: ultimo callable = guarda_agent y estructura reconocida
    ns = {}
    exec(compile(out.decode(), a.salida, 'exec'), ns)
    ultimo = [v for v in ns.values() if callable(v)][-1]
    assert ultimo.__name__ == 'guarda_agent', ultimo
    assert ns['_GS_OK'] and ns['_GS_SALTADAS'] == ['mini_spec_venta', 'mini_spec'], ns['_GS_SALTADAS']
    assert ns['_FR_PARENT'] is ns['_gs_conmutador'] and ns['_GS_SIN'].__name__ == 'compra_tras_ventas'
    assert out[:len(b)] == b
    print(a.salida, cfg, hashlib.sha256(out).hexdigest())


if __name__ == '__main__':
    main()
