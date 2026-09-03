"""Inspeccion dura del chasis: que banderas del campeon MUERDEN de verdad.

La leccion del 2026-09-03: tres arms del panel salieron con sd = 0.0, o sea
identicos al base en las 160 celdas. No eran resultados nulos sino TESTS nulos:
la bandera no cambiaba ni una decision. Causa raiz: el chasis tiene DOS
implementaciones de la misma logica (la lista `tasks` con prioridades y
`_service_ops`, que es la que manda cuando router=True) y los parches tocaban
la mitad muerta.

Este script quita cada clave del config una por una y comprueba si el resultado
cambia. Una clave INERTE o no la lee nadie, o solo la lee codigo inalcanzable
para esta configuracion, o su valor coincide con el default.

OJO con la trampa: si el valor del config COINCIDE con el default del chasis,
quitar la clave es un no-op POR CONSTRUCCION y el test no dice nada. Para esas
claves hay que PERTURBAR el valor. El script lo detecta y lo hace solo.

Uso:  ./.venv/bin/python muerde.py [CONFIG]      # def. CAMPEONA_GRANO
"""
import glob, os, re, sys, json
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
CONFIG = sys.argv[1] if len(sys.argv) > 1 else "CAMPEONA_GRANO"
N_TAPES, SEEDS = 3, (91500, 91501)


_QUITAR = "<<QUITAR>>"   # str, no object(): viaja por pickle sin perder identidad


def _defaults(k, src):
    """Defaults con los que el chasis lee `k` (para detectar redundancia)."""
    return {(m.group(1) or "None").strip() for m in re.finditer(
        r'cfg\.get\(\s*["\']' + re.escape(k) + r'["\']\s*(?:,\s*([^)]*?))?\s*\)', src)}


def _perturbar(v):
    """Un valor claramente distinto, del mismo tipo."""
    if isinstance(v, bool):   return not v
    if isinstance(v, int):    return v + 50 if v < 50 else v // 4   # proporcional:
    # restar una constante a un valor grande (2000 -> 1970) no prueba nada.
    if isinstance(v, float):  return v * 3 + 1
    return _QUITAR


def _una(a):
    clave, tape, seed = a
    from kaggle_environments import make
    from bots import arquetipos
    from bots.chassis import make_agent
    from harness import materialize
    cfg = dict(getattr(arquetipos, CONFIG))
    if clave is not None:
        k, nuevo = clave
        if nuevo == _QUITAR:
            cfg.pop(k, None)
        else:
            cfg[k] = nuevo
    try:
        env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=False)
        env.run([make_agent(cfg), materialize(f"bots.meta.tape:{tape}")])
        return clave, (env.steps[-1][0].reward or 0)
    except Exception as e:                      # quitar la clave puede reventar
        return clave, f"ERROR {type(e).__name__}"


def main():
    from bots import arquetipos
    cfg = getattr(arquetipos, CONFIG)
    tapes = sorted(os.path.basename(f)[:-8]
                   for f in glob.glob("bots/meta/tapes/lad_*.json.gz"))[:N_TAPES]
    src = open("bots/chassis.py").read()
    # si valor == default, quitar no prueba nada: perturbar
    plan = {}
    for k in sorted(cfg):
        d = _defaults(k, src)
        redundante = (len(d) == 1 and next(iter(d)) == repr(cfg[k])) or (
            not cfg[k] and d == {"None"})
        plan[k] = _perturbar(cfg[k]) if redundante else _QUITAR
    claves = [None] + [(k, v) for k, v in plan.items()]
    jobs = [(k, t, s) for k in claves for t in tapes for s in SEEDS]
    print(f"{CONFIG}: {len(claves)-1} claves x {len(tapes)} cintas x {len(SEEDS)} seeds "
          f"= {len(jobs)} episodios", flush=True)
    with Pool(max(1, (os.cpu_count() or 2) - 1)) as p:
        res = p.map(_una, jobs)
    por = {}
    for k, v in res:
        por.setdefault(k, []).append(v)
    base = por[None]
    inertes, vivas, rotas = [], [], []
    for k in sorted(cfg):
        v = por[(k, plan[k])]
        if any(isinstance(x, str) for x in v):
            rotas.append((k, next(x for x in v if isinstance(x, str))))
        elif v == base:
            inertes.append(k)
        else:
            dif = sum(1 for a, b in zip(v, base) if a != b)
            vivas.append((k, dif, len(v)))
    print(f"\nbase: {base}")
    print(f"\n### MUERTAS ({len(inertes)}) — el chasis NO cambia ni una decision en {len(base)} partidas")
    for k in inertes:
        como = "quitada" if plan[k] == _QUITAR else f"-> {plan[k]!r}"
        print(f"  {k:26s} = {str(cfg[k])[:30]:30s} ({como})")
    print(f"\n### VIVAS ({len(vivas)}) — la bandera muerde")
    for k, d, n in sorted(vivas, key=lambda x: -x[1]):
        como = "quitada" if plan[k] == _QUITAR else f"-> {plan[k]!r}"
        print(f"  {k:26s} = {str(cfg[k])[:28]:28s} difiere {d}/{n}  ({como})")
    if rotas:
        print(f"\n### IMPRESCINDIBLES ({len(rotas)}) — quitarlas revienta")
        for k, e in rotas:
            print(f"  {k:26s} {e}")
    json.dump({"inertes": inertes, "vivas": [k for k, _, _ in vivas],
               "rotas": [k for k, _ in rotas]},
              open("results/muerde.json", "w"), indent=1)


if __name__ == "__main__":                      # GUARD OBLIGATORIO
    main()
