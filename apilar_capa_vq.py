"""Construye arshs3 + compactacion de cola de mercado (_vq_compact, tetsutani, Apache-2.0).

Base:  arsgorynich/herd-safe-v3-experimental-risk-aware-feed (sha 4f8637a3...), sin tocar.
Capa:  _ig_standard + _vq_compact copiados literalmente de
       tetsutani/demand-preserving-turn-sale-timing (sha 178ae0f7...).
       Sus dependencias (_r127_fields, _RACE_STATE) son identicas en ambos ficheros
       (comprobado por AST).
La capa quita del mercado las ordenes que seguro no ejecutan (huecos, ventas sin
stock, BUY_LAND con los 4 cuadrantes), de modo que las ejecutables ocupan slots
anteriores en la resolucion en lockstep. No cambia cantidades ni acciones de granja.

Uso: apilar_capa_vq.py <base.py> <tds.py> <salida.py>
"""
import ast, hashlib, sys
from pathlib import Path


def segmento(src, nombre):
    for n in ast.parse(src).body:
        if isinstance(n, ast.FunctionDef) and n.name == nombre:
            return ast.get_source_segment(src, n)
    raise SystemExit(f"no encuentro {nombre}")


def main(base, tds, salida):
    b = Path(base).read_bytes()
    t = Path(tds).read_text()
    capa = f"""


# ==== Capa VQ apilada (kaggriculture local, 2026-09-24) ====
# _ig_standard y _vq_compact copiados literalmente de tetsutani/demand-preserving-turn-sale-timing
# (Apache-2.0, sha256 {hashlib.sha256(Path(tds).read_bytes()).hexdigest()}).
_VQ2_PARENT = [v for v in list(globals().values()) if callable(v)][-1]
_VQ_REPORT = dict(changed_turns=0, holes_removed=0, dead_sales=0, dead_land=0,
                  shifted_orders=0, shifted_slots=0, errors=0)
{segmento(t, "_ig_standard")}

{segmento(t, "_vq_compact")}

def vq_stack_agent(observation, configuration=None):
    if int(observation['step']) == 0:
        for k in _VQ_REPORT:
            _VQ_REPORT[k] = 0
    action = _VQ2_PARENT(observation, configuration)
    try:
        if _ig_standard(configuration):
            return _vq_compact(observation, action)
    except Exception:
        _VQ_REPORT['errors'] += 1
    return action
vq_stack_agent.telemetry = _VQ_REPORT
"""
    Path(salida).write_bytes(b + capa.encode())
    print(salida, hashlib.sha256(Path(salida).read_bytes()).hexdigest()[:12])


if __name__ == "__main__":
    main(*sys.argv[1:4])
