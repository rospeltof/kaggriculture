"""Delta pareado entre dos brazos de un torneo (torneo.py --vs ref,cand).

Uso: pareado_torneo.py <torneo.jsonl> <ref> <cand>

Unidad: celda (rival, semilla) con la puntuacion media de los dos asientos.
Delta = cand - ref en puntos porcentuales. IC95 por semilla (t sobre la media de
cada semilla) y a dos vias (rival x semilla, Cameron-Gelbach-Miller), igual que
evaluar_lider.uncertainty. El directo ref vs cand se informa aparte.
"""
import json, math, statistics as st, sys
from collections import defaultdict
from scipy.stats import t as tdist


def main(path, ref, cand):
    rows = [json.loads(l) for l in open(path)]
    bad = [r for r in rows if not r["valid"]]
    if bad:
        print(f"!! {len(bad)} episodios invalidos: se excluyen sus celdas")
    cel = defaultdict(list)
    for r in rows:
        if r["valid"] and r["a"] in (ref, cand) and r["b"] not in (ref, cand):
            cel[(r["a"], r["b"], r["seed"])].append(r["score"])
    rivales = sorted({b for _, b, _ in cel})
    semillas = sorted({s for _, _, s in cel})
    M = []
    for b in rivales:
        fila = []
        for s in semillas:
            x, y = cel.get((ref, b, s)), cel.get((cand, b, s))
            if not x or not y:
                sys.exit(f"falta celda {b} {s}")
            fila.append(100 * (st.mean(y) - st.mean(x)))
        M.append(fila)
    nr, ns = len(M), len(M[0]); n = nr * ns
    flat = [v for f in M for v in f]; mean = st.mean(flat)
    by_seed = [st.mean(f[s] for f in M) for s in range(ns)]
    se = st.stdev(by_seed) / math.sqrt(ns)
    m1 = tdist.ppf(.975, ns - 1) * se
    vr = nr / (nr - 1) * sum((sum(f) - ns * mean) ** 2 for f in M) / n ** 2
    vs = ns / (ns - 1) * sum((sum(f[s] for f in M) - nr * mean) ** 2 for s in range(ns)) / n ** 2
    vc = n / (n - 1) * sum((v - mean) ** 2 for v in flat) / n ** 2
    var = vr + vs - vc
    m2 = tdist.ppf(.975, min(nr, ns) - 1) * math.sqrt(var) if var > 0 else float("nan")
    base = st.mean(st.mean(cel[(ref, b, s)]) for b in rivales for s in semillas)
    print(f"{cand} - {ref}: {nr} rivales x {ns} semillas = {n} celdas; ref {100 * base:.1f}%")
    print(f"  delta {mean:+.2f} pts | IC95 semilla [{mean - m1:+.2f}; {mean + m1:+.2f}] | "
          f"dos vias [{mean - m2:+.2f}; {mean + m2:+.2f}]")
    cambios = sum(v != 0 for v in flat)
    print(f"  celdas cambiadas {cambios}/{n}: {sum(v > 0 for v in flat)} a favor, {sum(v < 0 for v in flat)} en contra")
    for b, f in zip(rivales, M):
        print(f"    vs {b:>8s} {st.mean(f):+6.1f}")
    directo = [r for r in rows if r["valid"] and {r["a"], r["b"]} == {ref, cand}]
    if directo:
        sc = [r["score"] if r["a"] == cand else 1 - r["score"] for r in directo]
        print(f"  directo {cand} vs {ref}: {100 * st.mean(sc):.1f}% ({len(sc)} ep)")


if __name__ == "__main__":
    main(*sys.argv[1:4])
