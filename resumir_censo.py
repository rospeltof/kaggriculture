"""Resume la salida de censo_linajes.py: composicion por linaje de los asientos.

Uso: resumir_censo.py <censo.json> [--sin-rospel]
Clases por asiento (mejor candidato): exacta (partida completa, <=2 turnos
distintos), casi (completa, 3-24 distintos), parcial (>=100 turnos comparados y
>80% iguales antes de abortar), otro.
"""
import collections, json, sys


def clasificar(xs):
    xs = [x for x in xs if "error" not in x]
    best = max(xs, key=lambda x: (x["iguales"] / max(1, x["n"]) if x["n"] >= 100 else 0, x["iguales"]))
    full = best.get("completo") and best["n"] >= 700
    if full and best["fallos"] <= 2:
        return "exacta", best
    if full:
        return "casi", best
    if best["n"] >= 100 and best["iguales"] / best["n"] > .8:
        return "parcial", best
    return "otro", best


def main(path, sin_rospel=False):
    res = json.load(open(path))
    por = collections.defaultdict(list)
    for x in res:
        por[(x["replay"], x["seat"])].append(x)
    comp = collections.Counter(); ratings = collections.defaultdict(list)
    for (r, seat), xs in por.items():
        d = json.load(open(r)); nm = d["info"]["TeamNames"][seat]
        if sin_rospel and nm == "Rospel":
            continue
        tipo, best = clasificar(xs)
        comp[(best["cand"] if tipo != "otro" else "-", tipo)] += 1
    total = sum(comp.values())
    print(f"{total} asientos")
    for (cand, tipo), n in sorted(comp.items(), key=lambda kv: -kv[1]):
        print(f"  {n:3d} ({100 * n / total:4.1f}%)  {tipo:8s} {cand}")


if __name__ == "__main__":
    main(sys.argv[1], "--sin-rospel" in sys.argv)
