"""Capa BP: las compras de producto justo despues de las ventas (antes de contratar/sembrar).

Hecho (28-sep): contra copias de tds27 las partidas sin YARN se deciden por $6-66 y las
dos listas son casi iguales. Una copia del ladder (Ryu Sonoda) compra trigo antes de sus
HIRE y nos gano asi: en el lockstep por indice, quien compra en un indice menor paga las
unidades mas baratas. BF (compras al indice 0) perdia porque empujaba las ventas detras de
las del espejo; aqui las ventas no se mueven: la compra solo salta por encima de ordenes de
precio fijo (HIRE, BUY_SEED, BUY_ANIMAL, BUY_LAND), que no interactuan en precio.

Regla (antes de FR; reasigna `_FR_PARENT` con una fabrica que se borra): desde el paso 144,
si hay BUY_PRODUCT (WHEAT/FERTILIZER) detras de alguna orden de precio fijo, y el producto
no se vende en la misma lista, se mueve cada compra justo detras de la ultima venta que la
precedia (o al indice 0 si no habia venta antes), conservando el orden de todo lo demas.
Guardia de caja: dinero actual - coste de las compras >= coste de las ordenes de precio
fijo que quedan detras + $100.

Uso: apilar_compra_tras_ventas.py <base.py> <salida.py>
"""
import hashlib, sys
from pathlib import Path

CAPA = '''

# ==== Capa BP: BUY_PRODUCT tras las ventas, antes de las ordenes de precio fijo (kaggriculture local, 2026-09-28) ====
_BP_REPORT = globals().get('_BP_REPORT') or dict(moved=0, cash_blocks=0, errors=0)
def _bp_fabrica(padre):
    fijo = ('HIRE', 'BUY_SEED', 'BUY_ANIMAL', 'BUY_LAND')
    coste = {{'GOOSE': 300, 'COW': 400, 'SHEEP': 500, 'WHEAT': 10, 'CARROT': 20, 'TOMATO': 50, 'STRAWBERRY': 100, 'MELON': 80}}
    def compra_tras_ventas(observation, configuration=None):
        action = padre(observation, configuration)
        try:
            step = int(observation.get('step', 0)); player = int(observation.get('player', 0))
            if step < 144:
                return action
            market = [list(o) for o in (action.get('market') or []) if o]
            vendidos = {{o[1] for o in market if o[0] == 'SELL' and len(o) > 1}}
            prices = observation['market']['prices']
            nuevo = list(market); cambio = False
            for _ in range(len(market)):
                idx = next((i for i, o in enumerate(nuevo) if o[0] == 'BUY_PRODUCT' and len(o) > 2 and o[1] in ('WHEAT', 'FERTILIZER')
                            and o[1] not in vendidos and any(p[0] in fijo for p in nuevo[:i])
                            and not any(p[0] in fijo for p in nuevo[i + 1:i + 1] if False)), None)
                if idx is None:
                    break
                ultima_venta = max([j for j in range(idx) if nuevo[j][0] == 'SELL'], default=-1)
                destino = ultima_venta + 1
                saltadas = [p for p in nuevo[destino:idx] if p[0] in fijo]
                if not saltadas:
                    break
                c_fijo = 0.0
                for p in saltadas:
                    if p[0] == 'HIRE':
                        c_fijo += 100
                    elif p[0] == 'BUY_LAND':
                        c_fijo += 4000
                    elif len(p) > 2:
                        c_fijo += int(p[2]) * coste.get(p[1], 500)
                o = nuevo[idx]
                c_compra = int(o[2]) * (float(prices.get(o[1], 0)) + 3)
                if float(observation['farms'][player]['money']) - c_compra < c_fijo + 100:
                    _BP_REPORT['cash_blocks'] += 1
                    break
                nuevo = nuevo[:destino] + [o] + nuevo[destino:idx] + nuevo[idx + 1:]
                cambio = True
            if cambio and nuevo != market:
                _BP_REPORT['moved'] += 1
                action = dict(action, market=nuevo)
                st = _RACE_STATE.get(player)
                if st is not None and st.get('prev_action') is not None and st.get('step') == step:
                    st['prev_action'] = action
        except Exception:
            _BP_REPORT['errors'] += 1
        return action
    return compra_tras_ventas
_FR_PARENT = _bp_fabrica(_FR_PARENT)
del _bp_fabrica
'''


def main(base, salida):
    b = Path(base).read_bytes()
    assert b"_FR_PARENT" in b
    Path(salida).write_bytes(b + CAPA.format().encode())
    print(salida, hashlib.sha256(Path(salida).read_bytes()).hexdigest()[:12])


if __name__ == "__main__":
    main(*sys.argv[1:3])
