"""Apila capas copiadas literalmente de tetsutani/demand-preserving-turn-sale-timing
(Apache-2.0) sobre un agente publico de la misma base V39, sin tocar la base.

Capas (se aplican en el orden dado; la ultima queda como ultimo callable):
  vq   _ig_standard + _vq_compact: quita del mercado las ordenes que seguro no
       ejecutan (huecos, ventas sin stock, BUY_LAND con 4 cuadrantes) para que las
       ejecutables ocupen slots anteriores en la resolucion en lockstep.
  adv  bloque ADV de Ahmed Berat Ozer (EXP293): adelanta hasta 4 turnos las ventas
       previstas por la cinta si las unidades ya estan en el cobertizo, y ordena la
       lista (ventas, compras de producto, resto). Wrapper renombrado a
       adv_stack_agent para no reasignar `agent` (Kaggle usa el ultimo callable y
       reasignar una clave existente no la mueve al final).
Dependencias (_r127_fields, _RACE_STATE, _IMPL, projected_shed, FarmView) deben
existir en la base; se comprueba antes de escribir.

Uso: apilar_capa_vq.py <base.py> <tds.py> <salida.py> [capa ...]   (por defecto: vq)
"""
import ast, hashlib, sys
from pathlib import Path


def segmento(src, nombre):
    for n in ast.parse(src).body:
        if isinstance(n, ast.FunctionDef) and n.name == nombre:
            return ast.get_source_segment(src, n)
    raise SystemExit(f"no encuentro {nombre}")


def capa_vq(t):
    return f"""
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
""", ("_r127_fields", "_RACE_STATE")


def capa_adv(t):
    ini, fin = "_ADV_PARENT=agent\n", "# Final conservative closure"
    bloque = t[t.index(ini):t.index(fin)].rstrip()
    assert bloque.endswith("agent=globals().pop('agent')")
    bloque = bloque[:-len("agent=globals().pop('agent')")].rstrip()
    bloque = bloque.replace(ini, "_ADV_PARENT = [v for v in list(globals().values()) if callable(v)][-1]\n", 1)
    bloque = bloque.replace("def agent(observation,configuration=None):", "def adv_stack_agent(observation,configuration=None):", 1)
    bloque = bloque.replace("agent.telemetry=_ADV_REPORT", "adv_stack_agent.telemetry=_ADV_REPORT", 1)
    assert "def agent(" not in bloque and "\nagent" not in bloque
    return "\n" + bloque + "\n", ("_IMPL", "projected_shed", "FarmView", "_RACE_STATE")


CAPAS = {"vq": capa_vq, "adv": capa_adv}


def main(base, tds, salida, *capas):
    capas = capas or ("vq",)
    b = Path(base).read_bytes()
    src_base = b.decode()
    definidos = {n.name for n in ast.parse(src_base).body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
    definidos |= {t.id for n in ast.parse(src_base).body if isinstance(n, ast.Assign) for t in n.targets if isinstance(t, ast.Name)}
    t = Path(tds).read_text()
    texto = (f"\n\n# ==== Capas apiladas (kaggriculture local, 2026-09-24): {', '.join(capas)} ====\n"
             f"# Copiadas de tetsutani/demand-preserving-turn-sale-timing (Apache-2.0, "
             f"sha256 {hashlib.sha256(Path(tds).read_bytes()).hexdigest()}).\n")
    for c in capas:
        codigo, deps = CAPAS[c](t)
        faltan = [d for d in deps if d not in definidos]
        if faltan:
            raise SystemExit(f"capa {c}: la base no define {faltan}")
        texto += f"\n# ---- capa {c} ----" + codigo
    Path(salida).write_bytes(b + texto.encode())
    print(salida, hashlib.sha256(Path(salida).read_bytes()).hexdigest()[:12])


if __name__ == "__main__":
    main(*sys.argv[1:])
