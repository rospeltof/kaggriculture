"""Evolución 10 — búsqueda ESTRUCTURAL con el instrumento arreglado.

Por qué estructural: nueve mecanismos incrementales medidos el 2026-09-05 con
el panel validado dieron entre +0.0σ y -1.5σ. Ninguno mueve la aguja porque
todos son parches sobre la MISMA granja. El diagnóstico que sí quedó firme, de
las 22 partidas de CAMPEONA_FB:

  · nosotros: WATER 51% de las acciones, 62 tiles de cultivo, 8 animales
  · Around30 (nos hizo $150,822): WATER 17%, FEED+CARE+COLLECT 56%,
    9 tiles de cultivo y 38 estructuras — con los MISMOS 12 peones

O sea: nuestra granja tiene demasiado cultivo para la mano de obra que tiene, y
el riego se come el presupuesto de acciones. Añadir animales ENCIMA ya falló
tres veces (sheep8, MIMADA_XL, herd_demand) porque el cuello no es el rebaño:
es la proporción. Aquí la proporción es el gen.

Instrumento (lecciones del 2026-09-05, ver BITACORA):
  · medicion.evaluar: empates a 0.5 y sigma agrupada por par (seed, rival)
  · medicion.panel_oficial: [barnyard + campeona + rutera], validado — base
    65.2%, _noop +0.0σ, _peor -2.8σ. Ni saturado ni ciego.
  · fitness = score del panel (con empates), dinero como desempate
"""
import argparse
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bots.arquetipos import CAMPEONA_FB
from medicion import evaluar, panel_oficial

# fallback_fix va FORZADO: es la única mejora validada del ladder (802.8 vs 771)
FORCED = {"router": True, "hire_late": True, "opp_read": True, "sell_rank": True,
          "order_budget": True, "fallback_fix": True, "adaptive": True,
          "zoning": False, "multi_feeder": False, "phased": False,
          "scorer_v2": False, "grow": False}

# --- el espacio ESTRUCTURAL: proporción de la granja ---
REBANOS = [
    [("COW", 4), ("SHEEP", 4)],                    # el actual
    [("COW", 6), ("SHEEP", 2)],
    [("COW", 4), ("SHEEP", 2), ("GOOSE", 4)],      # el ganso que usa el top-1
    [("COW", 6), ("SHEEP", 4), ("GOOSE", 4)],
    [("COW", 8), ("SHEEP", 4)],
    [("GOOSE", 6), ("COW", 4), ("SHEEP", 2)],
    [("COW", 10), ("SHEEP", 4)],
    [("COW", 4), ("SHEEP", 6), ("GOOSE", 2)],
]
GENES = {
    "crop_tiles": [12, 16, 20, 24, 30],            # la hipótesis: bajar
    "animals": REBANOS,
    "hands_per_quadrant": [3, 4, 5],
    "max_quadrants": [2, 3],
    "animal_harvest_at": [1, 2, 4],
    "melon_max": [0, 4, 8],
    "fert_crops": [[], ["STRAWBERRY"], ["STRAWBERRY", "TOMATO"]],
    "order_funding": [False, True],
    "animal_first": [False, True],
    "prio_feed": [60, 75, 88],
    "prio_water": [30, 44, 60],
    "sell_floor": [0.3, 0.4, 0.5],
}


def _norm(cfg):
    c = dict(cfg)
    c.update(FORCED)
    c["fert_crops"] = sorted(c.get("fert_crops") or [])
    return c


def firma(cfg):
    c = _norm(cfg)
    return json.dumps({k: c.get(k) for k in sorted(GENES)}, sort_keys=True, default=str)


def muestrear(rng):
    c = _norm(dict(CAMPEONA_FB))
    for k, opciones in GENES.items():
        c[k] = rng.choice(opciones)
    return _norm(c)


def mutar(cfg, rng):
    c = _norm(dict(cfg))
    for _ in range(rng.choice([1, 1, 2])):
        k = rng.choice(list(GENES))
        c[k] = rng.choice(GENES[k])
    return _norm(c)


def main(gens=6, pop=22, seeds=3, procs=7, out="results/evolucion10.json"):
    rng = random.Random(20260905)
    panel = panel_oficial()
    vistos = set()
    # gen 0: el campeón actual + variantes estructurales dirigidas + aleatorias
    dirigidas = [
        dict(_norm(dict(CAMPEONA_FB))),                                   # control
        _norm(dict(CAMPEONA_FB, crop_tiles=20, animals=[("COW", 6), ("SHEEP", 4), ("GOOSE", 4)])),
        _norm(dict(CAMPEONA_FB, crop_tiles=16, animals=[("COW", 8), ("SHEEP", 4)])),
        _norm(dict(CAMPEONA_FB, crop_tiles=12, animals=[("COW", 10), ("SHEEP", 4)])),
        _norm(dict(CAMPEONA_FB, crop_tiles=20, animals=[("GOOSE", 6), ("COW", 4), ("SHEEP", 2)])),
    ]
    poblacion = dirigidas + [muestrear(rng) for _ in range(pop - len(dirigidas))]
    historia = []
    mejor_global = None

    for g in range(gens):
        cands, nombres = [], []
        for i, c in enumerate(poblacion):
            f = firma(c)
            if f in vistos and g > 0:
                c = mutar(c, rng)
                f = firma(c)
            vistos.add(f)
            n = f"g{g}_{i:02d}"
            nombres.append(n)
            cands.append(("cfg", n, c))
        base_cfg = dict(_norm(dict(CAMPEONA_FB)))
        # SUCCESSIVE HALVING. La primera versión daba `seeds`=3 a todos: 18
        # episodios por candidato, ±33 puntos de intervalo. Con ese margen el
        # ranking es RUIDO, los élites se eligen por azar y la búsqueda deriva
        # (por eso convergió sola a la config de partida). Aquí el presupuesto
        # se concentra: muchos candidatos con pocos seeds para descartar en
        # masa, y muchos seeds solo para los que siguen vivos.
        rondas = [(len(cands), seeds), (max(6, len(cands) // 3), seeds * 4),
                  (3, seeds * 12)]
        vivos = list(cands)
        res = {}
        for ri, (cuantos, s_ronda) in enumerate(rondas):
            vivos = vivos[:cuantos]
            if len(vivos) <= 1:
                break
            r = evaluar(vivos, panel, 20_000_000 + g * 1000 + ri * 97, s_ronda,
                        procs=procs, base=base_cfg, controles=(g == 0 and ri == 0))
            res.update({k: v for k, v in r.items() if not k.startswith("_")})
            vivos.sort(key=lambda c: (-res[c[1]]["score"], -res[c[1]]["money"]))
            print(f"    ronda {ri}: {cuantos} candidatos x {s_ronda} seeds "
                  f"-> mejor {vivos[0][1]} {res[vivos[0][1]]['score']:.1%} "
                  f"±{1.96*res[vivos[0][1]]['se']:.1%}")
        rank = sorted((n for n in nombres if n in res),
                      key=lambda n: (-res[n]["score"], -res[n]["money"]))
        top = rank[: max(4, pop // 5)]
        cfgs = {n: c for (_, n, c), in [((x,),) for x in cands]} if False else {
            n: c for (_, n, c) in cands}
        if mejor_global is None or res[rank[0]]["score"] > mejor_global[1]["score"]:
            mejor_global = (cfgs[rank[0]], res[rank[0]])
        print(f"\n--- generación {g} ---")
        for n in rank[:6]:
            r = res[n]
            marca = " <-- CONTROL (campeón actual)" if n.endswith("_00") and g == 0 else ""
            print(f"  {n} score {r['score']:5.1%} ±{1.96*r['se']:.1%} | ${r['money']:>8,.0f} "
                  f"| crop {cfgs[n].get('crop_tiles')} animales {cfgs[n].get('animals')}{marca}")
        historia.append({"gen": g, "top": [{"n": n, "score": res[n]["score"],
                                            "money": res[n]["money"], "cfg": cfgs[n]} for n in top]})
        # siguiente generación: élites + mutantes + inmigrantes
        elites = [cfgs[n] for n in top]
        nueva = list(elites)
        while len(nueva) < pop - 3:
            nueva.append(mutar(rng.choice(elites), rng))
        nueva += [muestrear(rng) for _ in range(3)]
        poblacion = nueva

    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as fh:
        json.dump({"historia": historia,
                   "mejor": {"cfg": mejor_global[0], "score": mejor_global[1]["score"],
                             "money": mejor_global[1]["money"]}}, fh, indent=1, default=str)
    print(f"\n=== MEJOR: score {mejor_global[1]['score']:.1%} | ${mejor_global[1]['money']:,.0f} ===")
    print(json.dumps(mejor_global[0], indent=1, default=str)[:900])
    print(f"\nescrito {out}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--gens", type=int, default=6)
    ap.add_argument("--pop", type=int, default=22)
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--procs", type=int, default=7)
    main(**vars(ap.parse_args()))
