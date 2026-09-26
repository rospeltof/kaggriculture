"""cha22cc: cha22sfko + capa PREDICT (_V92_P) de top3 con la biblioteca contra-cha22.

Copia literal (por AST) desde los ficheros exactos:
  top3   (arshs3+VQ+TOP3): import de la capa, constantes _V92_P_*, _V92_EP,
         _v92_p_lib/_pair/_update/_forecast, la extension forecast4 de arshs3
         (_HP_STATS, _hp_quantity, _HP_WINDOW y su _v92_predict, la ultima definida).
  top3cc: la biblioteca ampliada (_V92_P_BLOB, _V92_P_INDEX: ultimas asignaciones).
El envoltorio replica el de top3 (estado _V92_P por jugador, reinicio al paso 0) y
se apila al final de cha22sfko; _V92_P_TOP = 3 como en top3.
Dependencias en la base (se comprueban): _V9_RACE, _v9_town_draw, projected_shed,
FarmView, MAX_ORDERS, _IMPL.

Uso: construir_cha22cc.py <cha22sfko.py> <top3.py> <top3cc.py> <salida.py>
"""
import ast, hashlib, sys
from pathlib import Path


def nodos(src):
    return ast.parse(src).body


def seg(src, nodo):
    return ast.get_source_segment(src, nodo)


def ultimo(src, nombre, tipo):
    hit = None
    for n in nodos(src):
        if tipo == "def" and isinstance(n, ast.FunctionDef) and n.name == nombre:
            hit = n
        if tipo == "asig" and isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == nombre for t in n.targets):
            hit = n
    if hit is None:
        raise SystemExit(f"no encuentro {tipo} {nombre}")
    return seg(src, hit)


def primero(src, nombre, tipo):
    for n in nodos(src):
        if tipo == "def" and isinstance(n, ast.FunctionDef) and n.name == nombre:
            return seg(src, n)
        if tipo == "asig" and isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == nombre for t in n.targets):
            return seg(src, n)
    raise SystemExit(f"no encuentro {tipo} {nombre}")


def main(base, top3, top3cc, salida):
    b = Path(base).read_bytes(); sb = b.decode()
    t3 = Path(top3).read_text(); tc = Path(top3cc).read_text()
    definidos = set()
    for n in nodos(sb):
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            definidos.add(n.name)
        if isinstance(n, ast.Assign):
            definidos |= {t.id for t in n.targets if isinstance(t, ast.Name)}
    faltan = [d for d in ("_V9_RACE", "_v9_town_draw", "projected_shed", "FarmView", "MAX_ORDERS", "_IMPL") if d not in definidos]
    if faltan:
        raise SystemExit(f"la base no define {faltan}")
    if any(x.startswith("_V92_P") or x.startswith("_v92_p") for x in definidos):
        raise SystemExit("la base ya tiene capa PREDICT")
    imp = next(seg(t3, n) for n in nodos(t3) if isinstance(n, ast.Import) and any(a.asname == "_v92_zlib" for a in n.names))
    partes = [imp]
    for nombre in ("_V92_P_ITEMS", "_V92_P_USE", "_V92_P_H", "_V92_P_K", "_V92_P_EVERY", "_V92_EP",
                   "_V92_P_LIB", "_V92_P", "_V92_P_REPORT"):
        partes.append(primero(t3, nombre, "asig"))
    partes.append("_V92_P_TOP = 3")
    partes.append(ultimo(tc, "_V92_P_BLOB", "asig"))
    partes.append(ultimo(tc, "_V92_P_INDEX", "asig"))
    partes.append("_V92_P_RAW = None")
    for nombre in ("_v92_p_lib", "_v92_p_pair", "_v92_p_update", "_v92_p_forecast"):
        partes.append(primero(t3, nombre, "def"))
    partes.append(ultimo(t3, "_HP_STATS", "asig"))
    partes.append(ultimo(t3, "_hp_quantity", "def"))
    partes.append(ultimo(t3, "_HP_WINDOW", "asig"))
    partes.append(ultimo(t3, "_v92_predict", "def"))
    envoltorio = '''def v92_stack_agent(observation, configuration=None):
    player, step = int(observation["player"]), int(observation["step"])
    if step == 0:
        for k in _HP_STATS:
            _HP_STATS[k] = 0
    st = _V92_P.get(player)
    if st is None or step <= st["step"]:
        st = _V92_P[player] = {"step": -1, "obs": {}}
    st["step"] = step
    action = _V92_STACK_PARENT(observation, configuration)
    try:
        return _v92_predict(observation, action, st)
    except Exception:
        _V92_P_REPORT["pred_errors"] += 1
        return action


v92_stack_agent.telemetry = _V92_P_REPORT'''
    texto = ("\n\n# ==== Capa PREDICT de top3 + biblioteca contra-cha22 (kaggriculture local, 2026-09-26) ====\n"
             f"# Copiada por AST de top3 (sha256 {hashlib.sha256(Path(top3).read_bytes()).hexdigest()[:16]}) y "
             f"top3cc (sha256 {hashlib.sha256(Path(top3cc).read_bytes()).hexdigest()[:16]}); Apache-2.0 heredada.\n"
             + "# El padre se captura ANTES de definir funciones nuevas (regla del ultimo callable).\n"
             + "_V92_STACK_PARENT = [v for v in list(globals().values()) if callable(v)][-1]\n\n"
             + "\n\n".join(partes) + "\n\n\n" + envoltorio + "\n")
    Path(salida).write_bytes(b + texto.encode())
    print(salida, hashlib.sha256(Path(salida).read_bytes()).hexdigest()[:12])


if __name__ == "__main__":
    main(*sys.argv[1:5])
