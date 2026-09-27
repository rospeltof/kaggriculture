"""Variantes de ruta sobre un agente de la familia V39/tds27 (router de _IMPL.chassis).

El router original elige la ruta en el paso 144 (dos primeras tiendas) y pasa a la
ruta 2 en el paso 648. Aqui se envuelve _IMPL.chassis.router SIN dejar funciones
nuevas en el espacio global (la entrada de Kaggle es el ultimo callable):

  r0          ruta 0 para todos los pares entre los pasos 144 y 647
  v39         tabla del linaje viejo para todos los pares: _R110_OLD_SHOPS y luego
              _V92_TABLE (lo que el original solo usa si hay YARN_STORE)
  remap:F     F = json {"TIENDA_A,TIENDA_B": ruta}; los pares ausentes quedan igual

Uso: forzar_ruta.py <base.py> <salida.py> <modo>
"""
import hashlib, json, sys
from pathlib import Path

PLANTILLA = '''

# ==== Variante de ruta (kaggriculture local, 2026-09-28): {etiqueta} ====
def _rf_hacer(original, modo, tabla, viejo, v92):
    def router(observation, step, state):
        ruta = original(observation, step, state)
        if not (144 <= step < 648):
            return ruta
        if state.get('_rf_ruta') is None:
            tiendas = tuple((_get(_get(observation, 'town', {{}}), 'unlocked_shops', []) or [])[:2])
            if modo == 'r0':
                nueva = 0
            elif modo == 'v39':
                nueva = v92.get(tiendas, viejo.get(tiendas, 0))
            else:
                nueva = tabla.get(','.join(tiendas), ruta)
            state['_rf_ruta'] = nueva
        state['route'] = state['_rf_ruta']
        return state['_rf_ruta']
    return router
_IMPL.chassis.router = _rf_hacer(_IMPL.chassis.router, {modo!r}, {tabla!r}, _R110_OLD_SHOPS, _V92_TABLE)
del _rf_hacer
'''


def main(base, salida, modo):
    tabla = {}
    etiqueta = modo
    if modo.startswith("remap:"):
        tabla = json.load(open(modo[6:]))
        etiqueta = f"remap de {len(tabla)} pares"
        modo = "remap"
    elif modo not in ("r0", "v39"):
        raise SystemExit("modo invalido")
    b = Path(base).read_bytes()
    Path(salida).write_bytes(b + PLANTILLA.format(etiqueta=etiqueta, modo=modo, tabla=tabla).encode())
    print(salida, hashlib.sha256(Path(salida).read_bytes()).hexdigest()[:12])


if __name__ == "__main__":
    main(*sys.argv[1:4])
