"""Apila sobre un agente publico de base V39 los dos recortes de fin de partida de
tetsutani/demand-preserving-turn-sale-timing (22-sep, busyaprime, Apache-2.0),
copiados literalmente:

  sf  _33_seedfloat_agent: desde el paso 648 limita las compras de semilla de
      trigo/zanahoria a lo que la ruta 2 todavia puede plantar (nada plantado
      despues del dia 27 se cosecha antes del paso 718).
  ko  _33_knock_agent: quita BUY_PRODUCT FERTILIZER entre los pasos 696 y 719.

Motivo: ahorros de fin de partida que nunca reducen produccion cosechable; en un
espejo (misma politica en ambos asientos, que empata) cualquier dolar extra gana.
Dependencias en la base: _IMPL.chassis.routes[2], _CA_DROP, _CA_MARGIN, _CA_TO.

Uso: apilar_fin_partida.py <base.py> <tds_22sep.py> <salida.py>
"""
import ast, hashlib, sys
from pathlib import Path


def main(base, tds, salida):
    b = Path(base).read_bytes()
    t = Path(tds).read_text()
    ini = t.index("# busyaprime, 2026-09-21, Apache-2.0. Seed float trim")
    fin = t.index("agent = _33_knock_agent\nkaggle_submission_agent = agent")
    bloque = t[ini:fin].rstrip() + "\n"
    definidos = {x.id for n in ast.parse(b.decode()).body if isinstance(n, ast.Assign) for x in n.targets if isinstance(x, ast.Name)}
    faltan = [d for d in ("_IMPL", "_CA_DROP", "_CA_MARGIN", "_CA_TO") if d not in definidos]
    if faltan:
        raise SystemExit(f"la base no define {faltan}")
    texto = (f"\n\n# ==== Recortes de fin de partida apilados (kaggriculture local, 2026-09-26) ====\n"
             f"# Copiados de tetsutani/demand-preserving-turn-sale-timing 22-sep (Apache-2.0, "
             f"sha256 {hashlib.sha256(Path(tds).read_bytes()).hexdigest()}).\n" + bloque)
    Path(salida).write_bytes(b + texto.encode())
    print(salida, hashlib.sha256(Path(salida).read_bytes()).hexdigest()[:12])


if __name__ == "__main__":
    main(*sys.argv[1:4])
