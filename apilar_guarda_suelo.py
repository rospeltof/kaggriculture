"""Capa FG: no vender productos caros a precio de suelo mientras quede partida.

Hecho (sondas 28-sep): en mercados saturados ambos jugadores venden leche, fresa y lana a
<= 10% del precio base durante cientos de pasos (p. ej. 140 de 192 leches a <= $16). El
motor no sube el inventario con ventas a $1 ("Sales at $1 do not increase market supply"),
asi que tirar a $1 no presiona al rival: solo regala el producto. Guardar esas unidades en
el cobertizo y venderlas cuando el consumo del pueblo recupere el precio domina a tirarlas,
salvo que el cobertizo se llene o se acabe la partida.

Regla (antes de FR, reasignando `_FR_PARENT` con una fabrica que se borra; parametros en
el cierre): desde el paso 144 y antes de `hasta`, para cada producto de la lista, si el
precio actual <= umbral * base y la ocupacion del cobertizo (antes del mercado) < `lleno`,
se quitan las ordenes SELL de ese producto.

Uso: apilar_guarda_suelo.py <base.py> <salida.py> <umbral> <hasta> <lleno> ITEM [ITEM ...]
  ej.: apilar_guarda_suelo.py base.py out.py 0.10 690 85 WOOL MILK STRAWBERRY
"""
import hashlib, sys
from pathlib import Path

CAPA = '''

# ==== Capa FG: sin vender {items} a <= {umbral} * base antes del paso {hasta} (kaggriculture local, 2026-09-28) ====
_FG_REPORT = globals().get('_FG_REPORT') or dict(held_turns=0, held_units=0, errors=0)
def _fg_fabrica(padre, items, umbral, hasta, lleno):
    def guarda_suelo(observation, configuration=None):
        action = padre(observation, configuration)
        try:
            step = int(observation.get('step', 0)); player = int(observation.get('player', 0))
            if step < 144 or step >= hasta:
                return action
            market = [list(o) for o in (action.get('market') or []) if o]
            prices = observation['market']['prices']
            bajos = {{it for it in items if float(prices.get(it, 0)) <= umbral * float(_R37_MARKET_PARAMS[it]['base'])}}
            if not bajos or not any(o[0] == 'SELL' and len(o) > 1 and o[1] in bajos for o in market):
                return action
            ocupado = sum(max(0, int(v)) for v in projected_shed(dict(action, market=market), FarmView(observation)).values())
            if ocupado >= lleno:
                return action
            quitadas = sum(max(0, int(o[2])) for o in market if o[0] == 'SELL' and len(o) > 2 and o[1] in bajos)
            market = [o for o in market if not (o[0] == 'SELL' and len(o) > 1 and o[1] in bajos)]
            _FG_REPORT['held_turns'] += 1; _FG_REPORT['held_units'] += quitadas
            action = dict(action, market=market)
            st = _RACE_STATE.get(player)
            if st is not None and st.get('prev_action') is not None and st.get('step') == step:
                st['prev_action'] = action
        except Exception:
            _FG_REPORT['errors'] += 1
        return action
    return guarda_suelo
_FR_PARENT = _fg_fabrica(_FR_PARENT, {items!r}, {umbral}, {hasta}, {lleno})
del _fg_fabrica
'''


def main(base, salida, umbral, hasta, lleno, *items):
    b = Path(base).read_bytes()
    assert b"_FR_PARENT" in b
    Path(salida).write_bytes(b + CAPA.format(items=tuple(items), umbral=float(umbral), hasta=int(hasta), lleno=int(lleno)).encode())
    print(salida, umbral, hasta, lleno, items, hashlib.sha256(Path(salida).read_bytes()).hexdigest()[:12])


if __name__ == "__main__":
    main(*sys.argv[1:])
