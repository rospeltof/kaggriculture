"""Comprueba que perturbaciones cambian las acciones observadas del campeon.

Igual win-rate o dinero final NO implica iguales decisiones. Se resume toda la
secuencia de acciones emitidas mediante un hash incremental, antes de que el
motor pueda mutarlas. Dinero y estados finales se registran por separado.
No observar cambios en estas partidas no demuestra que una clave sea inutil
en otros escenarios, ni indica si se ejecuto una rama interna sin cambiar accion.

OJO con la trampa: si el valor del config COINCIDE con el default del chasis,
quitar la clave es un no-op POR CONSTRUCCION y el test no dice nada. Para esas
claves hay que PERTURBAR el valor. El script lo detecta y lo hace solo.

Uso:  ./.venv/bin/python muerde.py [CONFIG]      # def. CAMPEONA_GRANO
"""
import copy, glob, hashlib, os, re, sys, json
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


class _ActionTrace:
    """Huella ordenada de las acciones, sin retener el historial en memoria."""

    def __init__(self):
        self._hash = hashlib.sha256()
        self.count = 0

    def record(self, step, action):
        # Copia ANTES de entregar la accion: el motor puede modificar sus listas.
        snapshot = {"step": step, "action": copy.deepcopy(action)}
        encoded = json.dumps(snapshot, sort_keys=True, separators=(",", ":"),
                             ensure_ascii=True, allow_nan=False).encode("utf-8")
        self._hash.update(encoded)
        self._hash.update(b"\n")
        self.count += 1

    def summary(self):
        return {"actions_sha256": self._hash.hexdigest(), "action_count": self.count}


def _episode_error(result):
    if result.get("error"):
        return result["error"]
    if result["statuses"] != ["DONE", "DONE"]:
        return f"estados finales {result['statuses']}"
    if result["reward"] is None:
        return "reward final ausente"
    return None


def _differences(base, variant):
    """Dimensiones distintas; ninguna se deduce de otra."""
    return {
        "actions_changed": (base["actions_sha256"], base["action_count"]) !=
                           (variant["actions_sha256"], variant["action_count"]),
        "reward_changed": base["reward"] != variant["reward"],
        "statuses_changed": base["statuses"] != variant["statuses"],
    }


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
    trace = _ActionTrace()
    result = {"tape": tape, "seed": seed, "reward": None,
              "statuses": [], "error": None}
    try:
        agent = make_agent(cfg)

        def traced(obs):
            action = agent(obs)
            trace.record(obs.get("step"), action)
            return action

        env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=False)
        env.run([traced, materialize(f"bots.meta.tape:{tape}")])
        final = env.steps[-1]
        result.update(reward=final[0].reward, statuses=[s.status for s in final])
    except Exception as e:                      # quitar la clave puede reventar
        result["error"] = f"{type(e).__name__}: {e}"
    result.update(trace.summary())
    return clave, result


def main():
    from bots import arquetipos
    cfg = getattr(arquetipos, CONFIG)
    tapes = sorted(os.path.basename(f)[:-8]
                   for f in glob.glob("bots/meta/tapes/lad_*.json.gz"))[:N_TAPES]
    if not tapes:
        raise RuntimeError("No hay cintas lad_ para comparar acciones")
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
        por.setdefault(k, {})[(v["tape"], v["seed"])] = v
    base = por[None]
    for cell, result in base.items():
        error = _episode_error(result)
        if error:
            raise RuntimeError(f"Base invalida en {cell}: {error}")
    inertes, vivas, rotas = [], [], []
    detalles = {}
    for k in sorted(cfg):
        v = por[(k, plan[k])]
        if set(v) != set(base):
            raise RuntimeError(f"Celdas incompletas para {k}")
        counts = {name: 0 for name in ("actions_changed", "reward_changed", "statuses_changed")}
        episodes, errors = [], []
        for cell, result in v.items():
            differences = _differences(base[cell], result)
            for name, changed in differences.items():
                counts[name] += int(changed)
            episodes.append(dict(result, **differences))
            error = _episode_error(result)
            if error:
                errors.append(f"{cell}: {error}")
        if errors:
            rotas.append((k, errors[0]))
            label = "error_observado"
        elif not any(counts.values()):
            inertes.append(k)
            label = "sin_cambios_observados"
        else:
            vivas.append((k, counts, len(v)))
            label = "cambios_observados"
        detalles[k] = {"perturbation": plan[k], "classification": label,
                       "counts": counts, "episodes": episodes}
    print(f"\nbase, dinero final: {[r['reward'] for r in base.values()]}")
    print(f"\n### SIN CAMBIOS OBSERVADOS ({len(inertes)}) — acciones, dinero y estados iguales en {len(base)} partidas")
    for k in inertes:
        como = "quitada" if plan[k] == _QUITAR else f"-> {plan[k]!r}"
        print(f"  {k:26s} = {str(cfg[k])[:30]:30s} ({como})")
    print(f"\n### CAMBIOS OBSERVADOS ({len(vivas)}) — episodios distintos por dimension")
    for k, counts, n in sorted(vivas, key=lambda x: -x[1]["actions_changed"]):
        como = "quitada" if plan[k] == _QUITAR else f"-> {plan[k]!r}"
        print(f"  {k:26s} acciones {counts['actions_changed']}/{n}, "
              f"dinero {counts['reward_changed']}/{n}, estados {counts['statuses_changed']}/{n}  ({como})")
    if rotas:
        print(f"\n### ERRORES OBSERVADOS ({len(rotas)}) — estas perturbaciones fallaron")
        for k, e in rotas:
            print(f"  {k:26s} {e}")
    print("\nSin cambios observados no significa clave muerta en todos los escenarios.")
    output = {
        "schema_version": 2, "config": CONFIG, "tapes": tapes, "seeds": list(SEEDS),
        "scope": "Solo las perturbaciones y partidas registradas; no demuestra ejecucion de ramas internas.",
        # Alias historicos para lectores existentes, con alcance explicito.
        "inertes": inertes, "vivas": [k for k, _, _ in vivas], "rotas": [k for k, _ in rotas],
        "sin_cambios_observados": inertes, "cambios_observados": [k for k, _, _ in vivas],
        "base": list(base.values()), "detalles": detalles,
    }
    os.makedirs("results", exist_ok=True)
    with open("results/muerde.json", "w") as fh:
        json.dump(output, fh, indent=1)


if __name__ == "__main__":                      # GUARD OBLIGATORIO
    main()
