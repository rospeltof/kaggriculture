"""Capa WF2: como apilar_lana_primero.py, pero con suelo por producto y parametros en el
cierre de la fabrica (no en globales), para poder apilar varias sin que se pisen.

Regla: desde el paso 144, para cada producto, vender ya (orden en el indice 0; si ya habia
venta se suma y se mueve al 0) el stock libre del cobertizo mientras el precio marginal de
la siguiente unidad sea >= fraccion_producto * precio base. Se aplica antes de FR
(reasigna `_FR_PARENT` con una fabrica que se borra).

Uso: apilar_venta_primero.py <base.py> <salida.py> ITEM:FRAC [ITEM:FRAC ...] [--rival]
  ej.: apilar_venta_primero.py base.py out.py WOOL:0.75 MILK:0.75 STRAWBERRY:0.75 CARROT:0.9
"""
import hashlib, sys
from pathlib import Path

CAPA = '''

# ==== Capa WF2: vender primero {pares} (rival={rival}) (kaggriculture local, 2026-09-28) ====
_WF2_REPORT = globals().get('_WF2_REPORT') or dict(calls=0, fires=0, units=0, errors=0)
def _wf2_fabrica(padre, pares, rival_only):
    fuente = {{'WOOL': 'SHEEP', 'MILK': 'COW', 'EGG': 'GOOSE'}}
    def venta_primero(observation, configuration=None):
        action = padre(observation, configuration)
        try:
            step = int(observation.get('step', 0)); player = int(observation.get('player', 0))
            if step < 144:
                return action
            market = [list(o) for o in (action.get('market') or []) if o]
            stock = projected_shed(dict(action, market=market), FarmView(observation))
            inv_all = observation['market']['inventory']
            rival_prod = None
            if rival_only:
                rival_prod = set()
                for row in observation['farms'][1 - player].get('tiles') or []:
                    for tl in row:
                        if isinstance(tl, dict):
                            rival_prod.add(tl.get('animal')); rival_prod.add(tl.get('crop'))
            cambio = False
            for item, frac in pares:
                if rival_prod is not None and fuente.get(item, item) not in rival_prod:
                    continue
                if any(o[0] == 'BUY_PRODUCT' and len(o) > 1 and o[1] == item for o in market):
                    continue
                vendiendo = sum(max(0, int(o[2])) for o in market if o[0] == 'SELL' and len(o) > 2 and o[1] == item)
                libre = int(stock.get(item, 0)) - vendiendo
                if libre <= 0:
                    continue
                suelo = frac * float(_R37_MARKET_PARAMS[item]['base'])
                inv = int(inv_all.get(item, 0)) + vendiendo
                k = 0
                while k < libre and float(_r37_market_price(item, inv + k)) >= suelo:
                    k += 1
                if k <= 0:
                    continue
                resto = [o for o in market if not (o[0] == 'SELL' and len(o) > 1 and o[1] == item)]
                if len(resto) >= 10:
                    continue
                market = [['SELL', item, vendiendo + k]] + resto
                _WF2_REPORT['fires'] += 1; _WF2_REPORT['units'] += k; cambio = True
            if cambio:
                action = dict(action, market=market[:10])
                st = _RACE_STATE.get(player)
                if st is not None and st.get('prev_action') is not None and st.get('step') == step:
                    st['prev_action'] = action
        except Exception:
            _WF2_REPORT['errors'] += 1
        return action
    return venta_primero
_FR_PARENT = _wf2_fabrica(_FR_PARENT, {pares!r}, {rival})
del _wf2_fabrica
'''


def main(base, salida, *args):
    rival = "--rival" in args
    pares = []
    for a in args:
        if a.startswith("--"):
            continue
        it, fr = a.split(":")
        pares.append((it, float(fr)))
    b = Path(base).read_bytes()
    assert b"_FR_PARENT" in b
    Path(salida).write_bytes(b + CAPA.format(pares=tuple(pares), rival=rival).encode())
    print(salida, pares, "rival" if rival else "", hashlib.sha256(Path(salida).read_bytes()).hexdigest()[:12])


if __name__ == "__main__":
    main(*sys.argv[1:])
