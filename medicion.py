"""Medición estadística correcta para las ablaciones.

Nace del incidente del 2026-09-05: el evaluador de evolucion9.py contaba
`a["w"] += my > their`, o sea **el empate como derrota**. Como el motor es
determinista, un cambio inocuo produce empates EXACTOS, así que un brazo
`noop` (cash_buffer 200->201) leía 33.3% en vez del 50% que le corresponde, y
toda variante parecía "veneno". Con ese instrumento se midieron 19 variantes en
un día y las 19 salieron negativas — la firma de un medidor sesgado, no de 19
malas ideas.

Tres correcciones:
  1. EMPATES a 0.5, y reportados aparte (score = (w + 0.5t)/n).
  2. SIGMA AGRUPADA POR SEED: los dos episodios de un par espejado comparten
     semilla y NO son independientes; tratarlos como 2 muestras infla la sigma
     ~40%. La unidad de muestreo es el par (seed, oponente).
  3. BRAZOS DE CONTROL obligatorios, con verdad conocida:
       _noop  -> cambio inocuo; DEBE leer ~50%. Si no, el instrumento miente.
       _peor  -> la generación anterior del ladder (peor conocida por +14.2
                 pts reales). Marca el SUELO de la escala: una variante que
                 pierde MENOS que _peor no es "veneno", es "no resuelto".
"""
import math
from collections import defaultdict
from multiprocessing import Pool

from harness import run_episode, spec_name


def _stats(pares):
    """pares: lista de valores por unidad de muestreo (0, 0.5 o 1)."""
    n = len(pares)
    if n == 0:
        return 0.0, 0.0
    m = sum(pares) / n
    if n < 2:
        return m, 0.0
    var = sum((x - m) ** 2 for x in pares) / (n - 1)
    return m, math.sqrt(var / n)


def evaluar(cands, panel, seed0, n_seeds, steps=720, procs=7,
            base=None, controles=True):
    """Evalúa candidatos contra un panel con mediciones espejadas.

    Devuelve {nombre: dict(score, se, money, w, l, t, n)} donde `score` da 0.5
    a los empates y `se` es el error estándar agrupado por par (seed, rival).
    Si `base` se pasa y `controles`, inyecta los brazos _noop y _peor.
    """
    cands = list(cands)
    if controles and base is not None:
        cands = cands + [
            ("cfg", "_noop", dict(base, cash_buffer=base.get("cash_buffer", 200) + 1)),
            ("cfg", "_peor", dict(base, fallback_fix=False)),
        ]
    jobs, meta = [], []
    for c in cands:
        for oi, opp in enumerate(panel):
            for s in range(seed0, seed0 + n_seeds):
                jobs.append((c, opp, s, steps)); meta.append((spec_name(c), oi, s, 0))
                jobs.append((opp, c, s, steps)); meta.append((spec_name(c), oi, s, 1))
    with Pool(procs) as pool:
        res = pool.map(run_episode, jobs)

    por_par = defaultdict(list)       # (nombre, rival, seed) -> [0|0.5|1, ...]
    agg = defaultdict(lambda: {"w": 0, "l": 0, "t": 0, "n": 0, "money": 0.0})
    for r, (name, oi, s, side) in zip(res, meta):
        my, their = r["money"][side], r["money"][1 - side]
        a = agg[name]
        a["n"] += 1
        a["money"] += my
        if my > their:
            a["w"] += 1; v = 1.0
        elif my < their:
            a["l"] += 1; v = 0.0
        else:
            a["t"] += 1; v = 0.5
        por_par[(name, oi, s)].append(v)

    out = {}
    for name, a in agg.items():
        pares = [sum(v) / len(v) for k, v in por_par.items() if k[0] == name]
        score, se = _stats(pares)
        out[name] = {"score": score, "se": se, "money": a["money"] / max(1, a["n"]),
                     "w": a["w"], "l": a["l"], "t": a["t"], "n": a["n"],
                     "pares": len(pares)}
    return out


def reportar(res, base_name, titulo=""):
    """Imprime la tabla con la lectura correcta y valida los controles."""
    if titulo:
        print(titulo)
    b = res.get(base_name)
    orden = sorted(res, key=lambda k: -res[k]["score"])
    print(f"{'variante':16s} {'score':>7s} {'±2se':>7s} {'W-L-T':>12s} {'dinero':>10s} {'vs base':>9s}")
    for k in orden:
        r = res[k]
        d = ""
        if b and k != base_name:
            dif = r["score"] - b["score"]
            se = math.sqrt(r["se"] ** 2 + b["se"] ** 2)
            d = f"{dif:+.1%} {dif/se if se else 0:+.1f}σ"
        print(f"{k:16s} {r['score']:6.1%} {1.96*r['se']:6.1%} "
              f"{r['w']:>3d}-{r['l']:<3d}-{r['t']:<3d} {r['money']:>10,.0f} {d:>16s}")

    # --- validación del instrumento ---
    # El _noop debe leer igual que la BASE, no igual a 50%: contra un panel
    # externo la base puede estar en 98% legítimamente y el 50% solo aplica al
    # duelo espejo, donde la base juega contra sí misma. (Mi primera versión
    # comparaba contra 50% y declaraba "sesgado" a un panel que funcionaba.)
    print("\n-- control del instrumento --")
    ok = True
    if "_noop" in res and b:
        s = res["_noop"]["score"]
        se = math.sqrt(res["_noop"]["se"] ** 2 + b["se"] ** 2)
        z = (s - b["score"]) / se if se else 0.0
        veredicto = "OK" if abs(z) < 2.5 else "¡SESGADO!"
        print(f"  _noop  {s:.1%} vs base {b['score']:.1%} ({z:+.1f}σ)  [{veredicto}]  "
              f"empates {res['_noop']['t']}/{res['_noop']['n']}")
        ok = ok and abs(z) < 2.5
    if "_peor" in res and b:
        p2 = res["_peor"]
        se2 = math.sqrt(p2["se"] ** 2 + b["se"] ** 2)
        z2 = (p2["score"] - b["score"]) / se2 if se2 else 0.0
        # el panel debe SABER que la generación anterior es peor; si no lo ve,
        # no tiene poder para juzgar nada más
        disc = "OK (el panel discrimina)" if z2 < -2.0 else "¡CIEGO! el panel no ve una diferencia conocida"
        print(f"  _peor  {p2['score']:.1%} ({z2:+.1f}σ vs base)  [{disc}]")
        ok = ok and z2 < -2.0
    if "_peor" in res and b:
        p = res["_peor"]
        print(f"  _peor  {p['score']:.1%} — SUELO de la escala; una variante que pierda "
              f"MENOS que esto es 'no resuelto', no 'veneno'")
    if not ok:
        print("  >>> NO interpretar los deltas: el instrumento no pasa su propio control.")
    return ok
