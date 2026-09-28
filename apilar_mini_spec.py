"""Capa MS: opción gratis alrededor de las compras de trigo/fertilizante del espejo.

Hecho (motor 1.32.7): una compra se cotiza al inventario−1, así que comprar X y revender X
en el mismo paso contra un mercado sin cambios da exactamente 0 ("a buy/sell round-trip
against an unchanged market nets zero"). En espejos de la familia tds27 ambos compramos
trigo/fertilizante en los mismos pasos y cantidades; con BP nuestra compra va antes que la
suya. Si compramos X de más en nuestro índice y revendemos X en el índice 9, cuando el
espejo compra entre medias nuestra reventa se cotiza con su compra ya hecha (inventario más
bajo, precio más alto): ganancia ≈ X · pendiente · n. Si nadie compra en medio, ≈ 0.

Regla (antes de FR; reasigna `_FR_PARENT` con una fabrica que se borra): desde el paso 144
y antes del 700, si nuestra lista compra FERTILIZER (si no, WHEAT) y no vende ese producto,
se suman X unidades a la primera compra y se añade SELL X en el índice 9 (relleno con
órdenes vacías). X = min(Xmax, hueco del cobertizo − 6, caja tras todas las compras y órdenes fijas − $500). No actúa en
pasos donde FR puede actuar (cinta con compra de trigo >= 20 en t o t+1, o venta 20..999
en t+1) ni si la lista ya tiene 9 o más órdenes.

Uso: apilar_mini_spec.py <base.py> <salida.py> <Xmax>
"""
import hashlib, sys
from pathlib import Path

CAPA = '''

# ==== Capa MS: opcion de reventa alrededor de compras del espejo, Xmax={xmax} (kaggriculture local, 2026-09-28) ====
_MS_REPORT = globals().get('_MS_REPORT') or dict(trades=0, units=0, skips_fr=0, errors=0)
def _ms_fabrica(padre, xmax):
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
    def mini_spec(observation, configuration=None):
        action = padre(observation, configuration)
        try:
            step = int(observation.get('step', 0)); player = int(observation.get('player', 0))
            if step < 144 or step >= 700:
                return action
            market = [list(o) for o in (action.get('market') or []) if o]
            if len(market) >= 9:
                return action
            native = _IMPL.chassis.players.get(player) or {{}}
            if _cinta_trigo(native, step) >= 20 or _cinta_trigo(native, step + 1) >= 20 or _cinta_trigo(native, step + 1, venta=True) > 0:
                _MS_REPORT['skips_fr'] += 1
                return action
            prices = observation['market']['prices']
            money = float(observation['farms'][player]['money'])
            ocupado = sum(max(0, int(v)) for v in projected_shed(dict(action, market=market), FarmView(observation)).values())
            for item in ('FERTILIZER', 'WHEAT'):
                idx = [i for i, o in enumerate(market) if o[0] == 'BUY_PRODUCT' and len(o) > 2 and o[1] == item and int(o[2]) > 0]
                if not idx or any(o[0] == 'SELL' and len(o) > 1 and o[1] == item for o in market):
                    continue
                m = sum(int(market[i][2]) for i in idx)
                gasto = sum(int(o[2]) * (float(prices.get(o[1], 0)) + 3) for o in market if o[0] == 'BUY_PRODUCT' and len(o) > 2)
                for o in market:
                    if o[0] == 'HIRE':
                        gasto += 100
                    elif o[0] == 'BUY_LAND':
                        gasto += 4000
                    elif o[0] in ('BUY_SEED', 'BUY_ANIMAL') and len(o) > 2:
                        gasto += int(o[2]) * {{'GOOSE': 300, 'COW': 400, 'SHEEP': 500, 'WHEAT': 10, 'CARROT': 20, 'TOMATO': 50, 'STRAWBERRY': 100, 'MELON': 80}}.get(o[1], 500)
                hueco = 100 - ocupado - m - 6
                caja = money - gasto - 500
                x = int(min(xmax, hueco, caja // (float(prices.get(item, 0)) + 3)))
                if x < 3:
                    continue
                market[idx[0]] = ['BUY_PRODUCT', item, int(market[idx[0]][2]) + x]
                while len(market) < 9:
                    market.append([])
                market.append(['SELL', item, x])
                _MS_REPORT['trades'] += 1; _MS_REPORT['units'] += x
                action = dict(action, market=market)
                st = _RACE_STATE.get(player)
                if st is not None and st.get('prev_action') is not None and st.get('step') == step:
                    st['prev_action'] = action
                break
        except Exception:
            _MS_REPORT['errors'] += 1
        return action
    return mini_spec
_FR_PARENT = _ms_fabrica(_FR_PARENT, {xmax})
del _ms_fabrica
'''


def main(base, salida, xmax):
    b = Path(base).read_bytes()
    assert b"_FR_PARENT" in b
    Path(salida).write_bytes(b + CAPA.format(xmax=int(xmax)).encode())
    print(salida, xmax, hashlib.sha256(Path(salida).read_bytes()).hexdigest()[:12])


if __name__ == "__main__":
    main(*sys.argv[1:4])
