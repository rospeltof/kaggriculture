"""Capa TP: la cinta propia como episodio de la biblioteca de PREDICT (_V92_P).

Los agentes de ruta publicos que ven las mismas dos primeras tiendas siguen la misma
cinta que nosotros. PREDICT elige los episodios de su biblioteca que mejor encajan con
las ventas observadas del rival y adelanta nuestras ventas si esos episodios anuncian
una venta grande del rival en 1-2 turnos. Aqui se anade a los candidatos de cada par de
tiendas un episodio construido con las VENTAS de nuestra cinta (ruta propia hasta el
paso 647, ruta 2 despues): contra un seguidor de cinta encaja casi exacto y se elige;
contra otro rival pierde el emparejamiento y no se usa.

Se envuelve _v92_p_pair (lectura en tiempo de llamada), sin funciones globales nuevas
tras la entrada: el envoltorio se crea con una fabrica que se borra del espacio global.

Uso: apilar_predict_cinta.py <base.py> <salida.py>
"""
import hashlib, sys
from pathlib import Path

CAPA = '''

# ==== Capa TP: cinta propia como episodio de PREDICT (kaggriculture local, 2026-09-28) ====
_TP_CINTA = {}
def _tp_fabrica(original):
    def par(shops):
        out = list(original(shops))
        try:
            ch = _IMPL.chassis
            for jugador, nat in list(ch.players.items()):
                ruta = nat.get('route')
                clave = jugador
                if clave not in _TP_CINTA:
                    if ruta is None or not (nat.get('router_state') or {}).get('day6'):
                        continue
                    ev = {}
                    for t in range(144, 719):
                        tape = ch.routes.get(2 if t >= 648 else ruta) or []
                        if t >= len(tape):
                            continue
                        for o in (tape[t].get('market') or []):
                            if o and len(o) > 2 and o[0] == 'SELL' and o[1] in _V92_P_ITEMS and int(o[2]) >= 2:
                                i = _V92_P_ITEMS.index(o[1]); ev[(t, i)] = ev.get((t, i), 0) + min(100, int(o[2]))
                    _TP_CINTA[clave] = ev
                if _TP_CINTA[clave]:
                    out.append((-2, _TP_CINTA[clave]))
                break
        except Exception:
            pass
        return out
    return par
_v92_p_pair = _tp_fabrica(_v92_p_pair)
del _tp_fabrica
'''


def main(base, salida):
    b = Path(base).read_bytes()
    Path(salida).write_bytes(b + CAPA.encode())
    print(salida, hashlib.sha256(Path(salida).read_bytes()).hexdigest()[:12])


if __name__ == "__main__":
    main(*sys.argv[1:3])
