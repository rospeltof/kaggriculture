"""Capa BF: las compras de producto (BUY_PRODUCT WHEAT/FERTILIZER) al indice 0.

Hecho (replays reales 28-sep): el 72% de nuestras partidas son espejos de la familia
tds27 (margen final < $1.000) y ambos compran trigo/fertilizante en los mismos pasos y
cantidades (feed/fertilizante propio, no la cinta). En el lockstep por indice, quien
compra en un indice menor paga las unidades baratas y el otro compra despues con el
inventario ya bajado. Los cierres de orden del linaje (s793/cxd) mueven ventas pero
dejan BUY_PRODUCT fijo, asi que nadie de la familia optimiza ese indice; una copia
del ladder (Ryu Sonoda) ya compra trigo antes de contratar.

La capa, antes de FR (reasigna el global `_FR_PARENT` con una fabrica que se borra),
mueve las BUY_PRODUCT al principio conservando el orden relativo del resto, desde el
paso 144, si el producto no se vende en la misma lista, si la caja actual cubre la
compra mas todas las ordenes de precio fijo que iban antes de ella, y si el cobertizo
(antes del mercado) tiene hueco para la compra.

Uso: apilar_compra_primero.py <base.py> <salida.py> [--desde N]
"""
import hashlib, sys
from pathlib import Path

CAPA = '''

# ==== Capa BF: BUY_PRODUCT al indice 0 antes de FR (kaggriculture local, 2026-09-28) ====
_BF_FROM = {desde}
_BF_REPORT = dict(calls=0, moved=0, units=0, cash_blocks=0, room_blocks=0, errors=0)
_BF_FIXED_COST = {{'GOOSE': 300, 'COW': 400, 'SHEEP': 500, 'WHEAT': 10, 'CARROT': 20, 'TOMATO': 50, 'STRAWBERRY': 100, 'MELON': 80}}
def _bf_fabrica(padre):
    def compra_primero(observation, configuration=None):
        action = padre(observation, configuration)
        try:
            step = int(observation.get('step', 0)); player = int(observation.get('player', 0))
            if step == 0:
                for k in _BF_REPORT:
                    _BF_REPORT[k] = 0
            _BF_REPORT['calls'] += 1
            if step < _BF_FROM:
                return action
            market = [list(o) for o in (action.get('market') or []) if o]
            idx = [i for i, o in enumerate(market) if o[0] == 'BUY_PRODUCT' and len(o) > 2 and o[1] in ('WHEAT', 'FERTILIZER') and int(o[2]) > 0]
            if not idx or idx == list(range(len(idx))):
                return action
            items = {{market[i][1] for i in idx}}
            if any(o[0] == 'SELL' and len(o) > 1 and o[1] in items for o in market):
                return action
            prices = observation['market']['prices']
            coste = sum(int(market[i][2]) * (float(prices[market[i][1]]) + 3) for i in idx)
            antes = 0.0
            for o in market[:idx[0]]:
                if o[0] == 'HIRE':
                    antes += 100
                elif o[0] == 'BUY_LAND':
                    antes += 4000
                elif o[0] in ('BUY_SEED', 'BUY_ANIMAL') and len(o) > 2:
                    antes += int(o[2]) * _BF_FIXED_COST.get(o[1], 500)
            dinero = float(observation['farms'][player]['money'])
            if dinero < coste + antes + 50:
                _BF_REPORT['cash_blocks'] += 1
                return action
            ocupado = sum(max(0, int(v)) for v in projected_shed(dict(action, market=market), FarmView(observation)).values())
            if ocupado + sum(int(market[i][2]) for i in idx) > 96:
                _BF_REPORT['room_blocks'] += 1
                return action
            nuevo = [market[i] for i in idx] + [o for i, o in enumerate(market) if i not in set(idx)]
            _BF_REPORT['moved'] += 1; _BF_REPORT['units'] += sum(int(market[i][2]) for i in idx)
            action = dict(action, market=nuevo)
            st = _RACE_STATE.get(player)
            if st is not None and st.get('prev_action') is not None and st.get('step') == step:
                st['prev_action'] = action
        except Exception:
            _BF_REPORT['errors'] += 1
        return action
    return compra_primero
_FR_PARENT = _bf_fabrica(_FR_PARENT)
del _bf_fabrica
'''


def main(base, salida, *flags):
    desde = 144
    if "--desde" in flags:
        desde = int(flags[flags.index("--desde") + 1])
    b = Path(base).read_bytes()
    assert b"_FR_PARENT" in b, "la base debe tener la capa FR"
    Path(salida).write_bytes(b + CAPA.format(desde=desde).encode())
    print(salida, "desde", desde, hashlib.sha256(Path(salida).read_bytes()).hexdigest()[:12])


if __name__ == "__main__":
    main(*sys.argv[1:])
