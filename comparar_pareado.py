"""Delta PAREADO de cada brazo contra una referencia, en un mismo bloque.

W/L/T (empate=0.5) por celda (rival, semilla), promediando asientos. IC95 por
semilla (t con n_semillas-1 gl) y a DOS VIAS (Cameron-Gelbach-Miller, rival x
semilla, gl del cluster menor). Desglose opcional por fuente del rival.

Uso: ./.venv/bin/python comparar_pareado.py <episodes.jsonl> [ref] [fuentes.json ...]
"""
import collections, json, math, statistics as st, sys

T95 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365, 8: 2.306, 9: 2.262,
       10: 2.228, 11: 2.201, 15: 2.131, 19: 2.093, 23: 2.069, 31: 2.040}


def tcrit(df):
    return T95.get(df, 1.96 + 2.4 / max(df, 1))


def celdas(path):
    por = collections.defaultdict(lambda: collections.defaultdict(list)); inval = 0
    for line in open(path):
        e = json.loads(line)
        if not e.get("valid"):
            inval += 1; continue
        me, op = e["rewards"][e["seat"]], e["rewards"][1 - e["seat"]]
        por[e["arm"]][(e["opponent"], e["seed"])].append(1.0 if me > op else 0.5 if me == op else 0.0)
    return {a: {k: sum(v) / len(v) for k, v in d.items()} for a, d in por.items()}, inval


def pareado(ca, cb, filtro=None):
    k = sorted(x for x in set(ca) & set(cb) if filtro is None or filtro(x[0]))
    if not k:
        return None
    d = {x: ca[x] - cb[x] for x in k}
    ps = collections.defaultdict(list)
    for x, v in d.items():
        ps[x[1]].append(v)
    med = [st.mean(v) for v in ps.values()]; n = len(med); m = st.mean(med)
    se1 = st.stdev(med) / math.sqrt(n) if n > 1 else float("nan")
    N = len(d); res = {x: v - st.mean(d.values()) for x, v in d.items()}
    def V(f):
        g = collections.defaultdict(float)
        for x, r in res.items():
            g[f(x)] += r
        return sum(s * s for s in g.values()) / (N * N)
    se2 = math.sqrt(max(V(lambda x: x[0]) + V(lambda x: x[1]) - sum(r * r for r in res.values()) / (N * N), 0.0))
    n_riv = len({x[0] for x in k}); tc1 = tcrit(n - 1); tc2 = tcrit(min(n, n_riv) - 1)
    return dict(m=m, ic1=(m - tc1 * se1, m + tc1 * se1), ic2=(m - tc2 * se2, m + tc2 * se2), n_sem=n, n_riv=n_riv)


def main():
    path = sys.argv[1]; ref = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].endswith(".json") else "gcal:top_majkel1337_107570947"
    fuentes = {}
    for f in [a for a in sys.argv[2:] if a.endswith(".json")]:
        for k, v in json.load(open(f)).items():
            for o in v:
                fuentes[o] = k
    cel, inval = celdas(path)
    wr = {a: st.mean(d.values()) for a, d in cel.items()}
    print(f"{path}: {len(cel)} brazos, {inval} episodios invalidos; referencia {ref} WR {100 * wr[ref]:.1f}%\n")
    print(f"{'brazo':38s} {'WR':>6s} {'delta':>7s}  {'IC95 semilla':>17s}  {'IC95 dos vias':>17s}")
    for a in sorted(cel, key=lambda x: -wr[x]):
        if a == ref:
            continue
        r = pareado(cel[a], cel[ref])
        signo = "  >0" if r["ic2"][0] > 0 and r["ic1"][0] > 0 else ("  <0" if r["ic2"][1] < 0 and r["ic1"][1] < 0 else "")
        print(f"{a:38s} {100 * wr[a]:5.1f}% {100 * r['m']:+7.2f}  [{100 * r['ic1'][0]:+6.1f};{100 * r['ic1'][1]:+6.1f}]  "
              f"[{100 * r['ic2'][0]:+6.1f};{100 * r['ic2'][1]:+6.1f}]{signo}")
    if fuentes:
        print("\ndelta vs referencia por FUENTE del rival:")
        srcs = sorted(set(fuentes.values()))
        print(f"{'brazo':38s} " + " ".join(f"{s[:7]:>8s}" for s in srcs))
        for a in sorted(cel, key=lambda x: -wr[x]):
            if a in (ref, "base", "noop"):
                continue
            fila = []
            for s in srcs:
                r = pareado(cel[a], cel[ref], lambda o, s=s: fuentes.get(o) == s)
                fila.append(f"{100 * r['m']:+8.1f}" if r else f"{'-':>8s}")
            print(f"{a:38s} " + " ".join(fila))


if __name__ == "__main__":
    main()
