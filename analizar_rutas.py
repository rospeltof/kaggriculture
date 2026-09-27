"""Analisis por par de tiendas de una criba de rutas (torneo.py con shops2).

Uso: analizar_rutas.py <torneo.jsonl> <ref> <cand> <salida_pares.json> [min_celdas]

Celda = (rival, semilla), asientos promediados; la partida define el par de tiendas
(identico para ref y cand: juegan igual hasta el paso 144). Para cada par:
delta medio de W/L/T y de margen propio (cand - ref). Regla pre-registrada
(PREREG_RUTAS_2026-09-28): par seleccionado si celdas >= min_celdas, delta W/L/T > 0
y delta de margen > 0. Escribe {"A,B": 0} para los seleccionados (remap a ruta 0).
Tambien informa el desglose por rival para ver si la mejor ruta depende del rival.
"""
import json, statistics as st, sys
from collections import defaultdict


def main(path, ref, cand, salida, min_celdas="4"):
    min_celdas = int(min_celdas)
    rows = [json.loads(l) for l in open(path)]
    cel = defaultdict(lambda: defaultdict(list))
    for r in rows:
        if not r.get("valid") or r["a"] not in (ref, cand) or r["b"] in (ref, cand) or not r.get("shops2"):
            continue
        mine = r["rewards"][r["seat"]]; theirs = r["rewards"][1 - r["seat"]]
        cel[(r["b"], r["seed"])][r["a"]].append((r["score"], mine - theirs, tuple(r["shops2"])))
    pares = defaultdict(list)
    for (riv, seed), d in cel.items():
        if ref not in d or cand not in d or len(d[ref]) != len(d[cand]):
            continue
        par = d[ref][0][2]
        if any(x[2] != par for x in d[ref] + d[cand]):
            continue
        ds = st.mean(x[0] for x in d[cand]) - st.mean(x[0] for x in d[ref])
        dm = st.mean(x[1] for x in d[cand]) - st.mean(x[1] for x in d[ref])
        pares[par].append((riv, ds, dm))
    sel = {}
    print(f"{'par':42s} celdas  dW/L/T   dmargen   por rival (dW/L/T)")
    for par, xs in sorted(pares.items(), key=lambda kv: -len(kv[1])):
        ds = st.mean(x[1] for x in xs); dm = st.mean(x[2] for x in xs)
        por = defaultdict(list)
        for riv, a, _ in xs:
            por[riv].append(a)
        marca = ""
        if len(xs) >= min_celdas and ds > 0 and dm > 0:
            sel[",".join(par)] = 0; marca = "  <= SELECCIONADO"
        detalle = " ".join(f"{k}:{100 * st.mean(v):+.0f}({len(v)})" for k, v in sorted(por.items()))
        print(f"{'/'.join(par):42s} {len(xs):5d}  {100 * ds:+6.1f}  {dm:+8.0f}   {detalle}{marca}")
    json.dump(sel, open(salida, "w"), indent=1)
    print(f"\n{len(sel)} pares seleccionados -> {salida}")


if __name__ == "__main__":
    main(*sys.argv[1:6])
