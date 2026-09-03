"""Rivales de fuerza graduable, derivados de la cinta C95.

El panel del proyecto estaba saturado: 0% contra todo el meta y 100% contra
nuestras generaciones viejas, sin nada en medio -> ciego a las mejoras (solo
detectaba regresiones). Como C95 ejecuta un schedule FIJO, se puede degradar de
forma determinista y reproducible: NO se pueden anular acciones de unidad:
la cinta no tiene holgura y al desincronizar la cadena PICKUP/PLACE/FEED la granja
colapsa a $0 (medido: p=0.30, 0.50 y 0.70 dan todas $0). Se degrada por el mercado,
que sí tiene margen: se limita cuántas unidades puede vender por turno. Eso modela
una debilidad REAL (liquidar demasiado despacio), mantiene la granja intacta y deja
al rival compitiendo por el mismo mercado.

Determinista por (step, indice de peon) -> mismo seed = misma partida.
Uso: bots.meta.c95_handicap:h30  (p=0.30)
"""
import importlib.util as _ilu
import os as _os

_spec = _ilu.spec_from_file_location(
    "_c95_base", _os.path.join(_os.path.dirname(__file__), "c95_main.py"))
_mod = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
_BASE = _mod.c94_submission_agent


def _make(cap):
    """cap = maximo de unidades vendibles por turno (None = sin limite)."""
    def agent(obs, config=None):
        action = _BASE(obs, config)
        try:
            if cap is not None:
                out, left = [], cap
                for o in (action.get("market") or []):
                    if isinstance(o, list) and len(o) >= 3 and o[0] == "SELL":
                        q = min(int(o[2] or 0), left)
                        left -= q
                        if q > 0:
                            out.append(["SELL", o[1], q])
                    else:
                        out.append(o)
                action["market"] = out[:10]
        except Exception:
            pass
        return action
    return agent


s2 = _make(2)
s4 = _make(4)
s8 = _make(8)
s16 = _make(16)
s10 = _make(10)
s11 = _make(11)
s12 = _make(12)
s14 = _make(14)
s32 = _make(32)
