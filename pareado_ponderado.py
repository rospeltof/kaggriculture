"""Delta pareado ponderado por la composicion real de rivales (censo del ladder).

Uso: pareado_ponderado.py <torneo.jsonl> <ref> <cand> <pesos.json>
pesos.json: {"linajes": {"cha22": {"cha22": 0.27, "cha22sfko": 0.27}, ...}}

Por semilla: delta(rival, semilla) = media de asientos (cand - ref) en pp;
ponderado(semilla) = sum_r w_r * delta(r, semilla). IC95 t sobre semillas.
Por linaje: media ponderada dentro del linaje (pesos renormalizados), IC por semilla.
"""
import json, math, statistics as st, sys
from collections import defaultdict
from scipy.stats import t as tdist


def ic(xs):
    m = st.mean(xs)
    if len(xs) < 2:
        return m, float("nan"), float("nan")
    h = tdist.ppf(.975, len(xs) - 1) * st.stdev(xs) / math.sqrt(len(xs))
    return m, m - h, m + h


def main(path, ref, cand, pesos):
    lin = json.load(open(pesos))["linajes"]
    w = {r: x for d in lin.values() for r, x in d.items()}
    rows = [json.loads(l) for l in open(path)]
    bad = [r for r in rows if not r["valid"]]
    cel = defaultdict(list)
    for r in rows:
        if r["valid"] and r["a"] in (ref, cand) and r["b"] in w:
            cel[(r["a"], r["b"], r["seed"])].append(r["score"])
    seeds = sorted({s for _, _, s in cel})
    d = {(b, s): 100 * (st.mean(cel[(cand, b, s)]) - st.mean(cel[(ref, b, s)])) for b in w for s in seeds}
    tot = sum(w.values())
    pond = [sum(w[b] * d[(b, s)] for b in w) / tot for s in seeds]
    m, lo, hi = ic(pond)
    print(f"{cand} - {ref}: {len(w)} rivales x {len(seeds)} semillas; invalidos {len(bad)}")
    print(f"  PONDERADO {m:+.2f} pp  IC95 semilla [{lo:+.2f}; {hi:+.2f}]")
    for nombre, dd in lin.items():
        sw = sum(dd.values())
        xs = [sum(x * d[(b, s)] for b, x in dd.items()) / sw for s in seeds]
        m, lo, hi = ic(xs)
        print(f"  linaje {nombre:10s} peso {sw:.3f}: {m:+6.2f} pp  IC95 [{lo:+.2f}; {hi:+.2f}]")
    directo = [r for r in rows if r["valid"] and {r["a"], r["b"]} == {ref, cand}]
    if directo:
        sc = [r["score"] if r["a"] == cand else 1 - r["score"] for r in directo]
        print(f"  directo {cand} vs {ref}: {100 * st.mean(sc):.1f}% ({len(sc)} ep)")


if __name__ == "__main__":
    main(*sys.argv[1:5])
