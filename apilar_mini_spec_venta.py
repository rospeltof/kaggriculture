"""Capa MSS: la opción de MS por el lado de la venta (trigo/fertilizante).

Una venta de X y su recompra de X en el mismo paso contra un mercado sin cambios dan $0
(la compra se cotiza al inventario−1). Si el rival VENDE ese producto entre nuestra venta y
nuestra recompra, recompramos más barato y él vendió más barato. En espejos, cuando vendemos
fertilizante o trigo el espejo también vende en ese paso.

Regla (antes de FR; reasigna `_FR_PARENT` con una fabrica que se borra): desde el paso 144 y
antes del 700, si nuestra lista vende FERTILIZER (si no, WHEAT) y no lo compra, y el
cobertizo tiene stock libre, se suman X = min(Xmax, stock libre) a esa venta (misma orden,
mismo indice) y se añade BUY_PRODUCT X en el ultimo indice libre (8 o 9; relleno con
ordenes vacias). No actua donde FR puede actuar ni si la lista ya ocupa el indice 9.

Uso: apilar_mini_spec_venta.py <base.py> <salida.py> <Xmax>
"""
import hashlib, sys
from pathlib import Path

CAPA = '''

# ==== Capa MSS: opcion de recompra alrededor de ventas del espejo, Xmax={xmax} (kaggriculture local, 2026-09-28) ====
_MSS_REPORT = globals().get('_MSS_REPORT') or dict(trades=0, units=0, errors=0)
def _mss_fabrica(padre, xmax):
    def _cinta_trigo(native, t, venta=False):
        tape = _IMPL.chassis.routes.get(2 if t >= 648 else native.get('route'))
        if not tape or t >= len(tape) or t > 718:
            return 0
        tot = 0
        for o in (tape[t].get('market') or []):
            if o and len(o) > 2 and o[1] == 'WHEAT':
                q = max(0, int(o[2]))
                if not venta and o[0] == 'BUY_PRODUCT':
                    tot += q
                elif venta and o[0] == 'SELL' and 20 <= q < 1000:
                    tot += q
        return tot
    def mini_spec_venta(observation, configuration=None):
        action = padre(observation, configuration)
        try:
            step = int(observation.get('step', 0)); player = int(observation.get('player', 0))
            if step < 144 or step >= 700:
                return action
            raw = list(action.get('market') or [])
            if len(raw) >= 10:
                return action
            market = [list(o) if o else [] for o in raw]
            native = _IMPL.chassis.players.get(player) or {{}}
            if _cinta_trigo(native, step) >= 20 or _cinta_trigo(native, step + 1) >= 20 or _cinta_trigo(native, step + 1, venta=True) > 0:
                return action
            stock = projected_shed(dict(action, market=[o for o in market if o]), FarmView(observation))
            prices = observation['market']['prices']
            money = float(observation['farms'][player]['money'])
            for item in ('FERTILIZER', 'WHEAT'):
                idx = [i for i, o in enumerate(market) if o and o[0] == 'SELL' and len(o) > 2 and o[1] == item and 0 < int(o[2]) < 1000]
                if not idx or any(o and o[0] == 'BUY_PRODUCT' and len(o) > 1 and o[1] == item for o in market):
                    continue
                vendiendo = sum(int(market[i][2]) for i in idx)
                libre = int(stock.get(item, 0)) - vendiendo
                x = int(min(xmax, libre, max(0, money - 500) // (float(prices.get(item, 0)) + 3)))
                if x < 3:
                    continue
                market[idx[0]] = ['SELL', item, int(market[idx[0]][2]) + x]
                while len(market) < 9:
                    market.append([])
                market.append(['BUY_PRODUCT', item, x])
                _MSS_REPORT['trades'] += 1; _MSS_REPORT['units'] += x
                action = dict(action, market=market[:10])
                st = _RACE_STATE.get(player)
                if st is not None and st.get('prev_action') is not None and st.get('step') == step:
                    st['prev_action'] = action
                break
        except Exception:
            _MSS_REPORT['errors'] += 1
        return action
    return mini_spec_venta
_FR_PARENT = _mss_fabrica(_FR_PARENT, {xmax})
del _mss_fabrica
'''


def main(base, salida, xmax):
    b = Path(base).read_bytes()
    assert b"_FR_PARENT" in b
    Path(salida).write_bytes(b + CAPA.format(xmax=int(xmax)).encode())
    print(salida, xmax, hashlib.sha256(Path(salida).read_bytes()).hexdigest()[:12])


if __name__ == "__main__":
    main(*sys.argv[1:4])
