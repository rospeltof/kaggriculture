"""Capa 'trigo primero' (observada en una casi-copia de tds27 del ladder, Ryu Sonoda):
en la lista de mercado, las ordenes BUY_PRODUCT WHEAT se adelantan a las HIRE,
conservando el orden relativo de todo lo demas. En lockstep la unidad n de cada
jugador se cotiza por indice de cola: comprar antes que un rival que contrata primero
da las unidades mas baratas. Riesgo: con caja justa alguna HIRE posterior puede fallar.

El envoltorio se captura como ultimo callable (entrada de Kaggle) y actualiza
_RACE_STATE[jugador]['prev_action'] como hacen las capas de mercado del linaje.

Uso: apilar_trigo_primero.py <base.py> <salida.py>
"""
import hashlib, sys
from pathlib import Path

CAPA = '''

# ==== Capa trigo-primero (kaggriculture local, 2026-09-28) ====
_TP_PARENT = [v for v in list(globals().values()) if callable(v)][-1]
_TP_REPORT = dict(changed_turns=0, errors=0)


def trigo_primero_agent(observation, configuration=None):
    if int(observation.get('step', 0)) == 0:
        _TP_REPORT.update(changed_turns=0, errors=0)
    action = _TP_PARENT(observation, configuration)
    try:
        market = [list(o) for o in (action.get('market') or []) if o]
        hires = [i for i, o in enumerate(market) if o[0] == 'HIRE']
        wheat = [i for i, o in enumerate(market) if o[0] == 'BUY_PRODUCT' and len(o) > 1 and o[1] == 'WHEAT']
        if hires and wheat and min(wheat) > min(hires):
            first = min(hires)
            moved = [market[i] for i in wheat]
            rest = [o for i, o in enumerate(market) if i not in set(wheat)]
            new = rest[:first] + moved + rest[first:]
            if new != market:
                _TP_REPORT['changed_turns'] += 1
                action = dict(action, market=new)
                st = _RACE_STATE.get(int(observation.get('player', 0)))
                if st is not None and st.get('prev_action') is not None and st.get('step') == int(observation.get('step', 0)):
                    st['prev_action'] = action
    except Exception:
        _TP_REPORT['errors'] += 1
    return action


trigo_primero_agent.telemetry = _TP_REPORT
'''


def main(base, salida):
    b = Path(base).read_bytes()
    Path(salida).write_bytes(b + CAPA.encode())
    print(salida, hashlib.sha256(Path(salida).read_bytes()).hexdigest()[:12])


if __name__ == "__main__":
    main(*sys.argv[1:3])
