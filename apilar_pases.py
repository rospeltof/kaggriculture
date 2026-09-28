"""Capa XP: pases extra de la clausura de orden de ventas (nivel k+1) antes de la capa FR.

Hecho (28-sep): tds27 y hl836 terminan con 41 pases de `_s793_reorder` (cierres
"fixedsell"); cada pase es la mejor respuesta de orden (ventas/ordenes de precio fijo)
contra un espejo que juega la lista del pase anterior (`_v44y_factor_margin`, lockstep
por unidad). Contra un espejo de 41 pases, un pase mas es la mejor respuesta a su lista.
cha22 tiene un solo pase `_cxd_reorder`.

La capa envuelve el padre de FR (reasignando el global `_FR_PARENT`, que conserva su
posicion) con una fabrica que se borra: el ultimo callable del modulo sigue siendo FR,
y las ventas especulativas de FR en el indice 9 no se reordenan.

Uso: apilar_pases.py <base.py> <salida.py> <n_pases> [--cxd]
  --cxd: los pases usan `_cxd_reorder` (contrario D) en vez de `_s793_reorder`.
"""
import hashlib, sys
from pathlib import Path

CAPA = '''

# ==== Capa XP: {n} pase(s) extra de {op} antes de FR (kaggriculture local, 2026-09-28) ====
_XP_N = {n}
_XP_REPORT = dict(calls=0, changed=0, errors=0)
def _xp_fabrica(padre):
    def pases(observation, configuration=None):
        action = padre(observation, configuration)
        try:
            step = int(observation.get('step', 0))
            if step == 0:
                _XP_REPORT.update(calls=0, changed=0, errors=0)
            _XP_REPORT['calls'] += 1
            res = action
            for _ in range(_XP_N):
                res = {op}(observation, res)
            if _s834_key(res) != _s834_key(action):
                _XP_REPORT['changed'] += 1
                st = _RACE_STATE.get(int(observation.get('player', 0)))
                if st is not None and st.get('prev_action') is not None and st.get('step') == step:
                    st['prev_action'] = res
            return res
        except Exception:
            _XP_REPORT['errors'] += 1
            return action
    return pases
_FR_PARENT = _xp_fabrica(_FR_PARENT)
del _xp_fabrica
'''


def main(base, salida, n, *flags):
    op = "_cxd_reorder" if "--cxd" in flags else "_s793_reorder"
    b = Path(base).read_bytes()
    assert b"_FR_PARENT" in b, "la base debe tener la capa FR"
    Path(salida).write_bytes(b + CAPA.format(n=int(n), op=op).encode())
    print(salida, op, n, hashlib.sha256(Path(salida).read_bytes()).hexdigest()[:12])


if __name__ == "__main__":
    main(*sys.argv[1:])
