"""Capa WF: vender primero los productos de curva empinada mientras el precio aguante.

Hecho (28-sep, sonda xc1 vs cha22 en la semilla 4810003, par BRUNCH/YARN, ruta 9): el
margen se pierde en la carrera de la lana. Ambos producen ~400 de lana; la curva de
precio de WOOL cae de 200 a 1 en ~100 unidades sobre I0 (forma cuadratica). cha22 vende
36 en los pasos 450-451 a $231-200 y nosotros 36 en 453-454 a $212-137; en 521-522 y
665-666 igual, y nuestras ventas acaban a $1-50. Total −$6.300. Entre espejos de la
familia tds27 las ventas de lana coinciden en el mismo paso (lockstep, empate), asi que
el primero que venda gana esas partidas. Con YARN_STORE (~23% de los pares) la lana es
el producto principal.

Regla (antes de FR, reasignando `_FR_PARENT` con una fabrica que se borra; despues del
pase XP si existe): desde el paso 144, para cada producto de la lista, vender ya (orden en
el indice 0; si ya habia venta de ese producto se suma y se mueve al 0) todas las unidades
del cobertizo que no esten ya en venta mientras el precio marginal de la siguiente unidad
se mantenga >= suelo = fraccion * precio base. Las unidades por debajo del suelo esperan.

Uso: apilar_lana_primero.py <base.py> <salida.py> <fraccion> <ITEM> [ITEM ...]
  ej.: apilar_lana_primero.py base.py out.py 0.75 WOOL
"""
import hashlib, sys
from pathlib import Path

CAPA = '''

# ==== Capa WF: vender primero {items} mientras precio >= {frac} * base (kaggriculture local, 2026-09-28) ====
_WF_ITEMS = {items!r}
_WF_FRAC = {frac}
_WF_FROM = 144
_WF_REPORT = dict(calls=0, fires=0, units=0, errors=0)
def _wf_fabrica(padre):
    def lana_primero(observation, configuration=None):
        action = padre(observation, configuration)
        try:
            step = int(observation.get('step', 0)); player = int(observation.get('player', 0))
            if step == 0:
                for k in _WF_REPORT:
                    _WF_REPORT[k] = 0
            _WF_REPORT['calls'] += 1
            if step < _WF_FROM:
                return action
            market = [list(o) for o in (action.get('market') or []) if o]
            stock = projected_shed(dict(action, market=market), FarmView(observation))
            inv_all = observation['market']['inventory']
            cambio = False
            for item in _WF_ITEMS:
                if any(o[0] == 'BUY_PRODUCT' and len(o) > 1 and o[1] == item for o in market):
                    continue
                vendiendo = sum(max(0, int(o[2])) for o in market if o[0] == 'SELL' and len(o) > 2 and o[1] == item)
                libre = int(stock.get(item, 0)) - vendiendo
                if libre <= 0:
                    continue
                suelo = _WF_FRAC * float(_R37_MARKET_PARAMS[item]['base'])
                inv = int(inv_all.get(item, 0)) + vendiendo
                k = 0
                while k < libre and float(_r37_market_price(item, inv + k)) >= suelo:
                    k += 1
                if k <= 0:
                    continue
                total = vendiendo + k
                resto = [o for o in market if not (o[0] == 'SELL' and len(o) > 1 and o[1] == item)]
                if len(resto) >= 10:
                    continue
                market = [['SELL', item, total]] + resto
                _WF_REPORT['fires'] += 1; _WF_REPORT['units'] += k; cambio = True
            if cambio:
                action = dict(action, market=market[:10])
                st = _RACE_STATE.get(player)
                if st is not None and st.get('prev_action') is not None and st.get('step') == step:
                    st['prev_action'] = action
        except Exception:
            _WF_REPORT['errors'] += 1
        return action
    return lana_primero
_FR_PARENT = _wf_fabrica(_FR_PARENT)
del _wf_fabrica
'''


def main(base, salida, frac, *items):
    b = Path(base).read_bytes()
    assert b"_FR_PARENT" in b
    Path(salida).write_bytes(b + CAPA.format(items=tuple(items), frac=float(frac)).encode())
    print(salida, frac, items, hashlib.sha256(Path(salida).read_bytes()).hexdigest()[:12])


if __name__ == "__main__":
    main(*sys.argv[1:])
