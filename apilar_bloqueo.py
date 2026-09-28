"""Capa BQ (diagnostico): quita de la lista de mercado las ordenes (op, item) desde un paso.

Sirve para medir si compras tardias (fertilizante, semillas, contrataciones) pagan su
coste en las partidas espejo: si quitarlas sube el margen propio sin bajar el W/L, eran
gasto que no se recupera antes del paso 719 (el dinero final es la unica recompensa).
Se aplica antes de FR (reasigna `_FR_PARENT` con una fabrica que se borra).

Uso: apilar_bloqueo.py <base.py> <salida.py> <desde> <OP[:ITEM]> [...]
  ej.: apilar_bloqueo.py base.py out.py 650 BUY_PRODUCT:FERTILIZER
"""
import hashlib, sys
from pathlib import Path

CAPA = '''

# ==== Capa BQ: sin {reglas} desde el paso {desde} (diagnostico, kaggriculture local, 2026-09-28) ====
_BQ_FROM = {desde}
_BQ_RULES = {reglas!r}
_BQ_REPORT = dict(calls=0, removed=0, errors=0)
def _bq_fabrica(padre):
    def bloqueo(observation, configuration=None):
        action = padre(observation, configuration)
        try:
            step = int(observation.get('step', 0))
            if step == 0:
                _BQ_REPORT.update(calls=0, removed=0, errors=0)
            _BQ_REPORT['calls'] += 1
            if step < _BQ_FROM:
                return action
            market = [list(o) for o in (action.get('market') or []) if o]
            keep = [o for o in market if not any(o[0] == op and (it is None or (len(o) > 1 and o[1] == it)) for op, it in _BQ_RULES)]
            if len(keep) != len(market):
                _BQ_REPORT['removed'] += len(market) - len(keep)
                action = dict(action, market=keep)
                st = _RACE_STATE.get(int(observation.get('player', 0)))
                if st is not None and st.get('prev_action') is not None and st.get('step') == step:
                    st['prev_action'] = action
        except Exception:
            _BQ_REPORT['errors'] += 1
        return action
    return bloqueo
_FR_PARENT = _bq_fabrica(_FR_PARENT)
del _bq_fabrica
'''


def main(base, salida, desde, *reglas):
    rs = []
    for r in reglas:
        op, _, it = r.partition(":")
        rs.append((op, it or None))
    b = Path(base).read_bytes()
    assert b"_FR_PARENT" in b
    Path(salida).write_bytes(b + CAPA.format(desde=int(desde), reglas=rs).encode())
    print(salida, desde, rs, hashlib.sha256(Path(salida).read_bytes()).hexdigest()[:12])


if __name__ == "__main__":
    main(*sys.argv[1:])
