"""Censo de linajes: ¿de que agente conocido es copia cada rival del ladder?

Para cada replay y cada asiento, alimenta a cada agente candidato (instancia
fresca, cargada como Kaggle) con las observaciones de ese asiento y compara su
accion con la que el replay registra en el turno siguiente. Un rival que es
copia byte-exacta (o de comportamiento identico) de un candidato coincide en
~100% de los turnos. Se aborta un candidato en cuanto acumula demasiados fallos.

Control positivo: nuestro asiento ("Rospel") debe coincidir con la submission
que jugo la partida.

Uso: censo_linajes.py <salida.json> <carpeta_replays> [...] -- nombre=ruta ...
"""
import glob, json, multiprocessing as mp, sys, time
from pathlib import Path

MAX_FALLOS = 25      # aborta el candidato tras tantos turnos distintos
MIN_TURNOS = 150     # turnos minimos comparados para declarar copia


def norm(a):
    if not isinstance(a, dict):
        return a
    return {"farmer": a.get("farmer") or ["PASS"], "hands": [list(h) for h in (a.get("hands") or [])],
            "market": [list(m) for m in (a.get("market") or []) if m]}


def comparar(job):
    replay, seat, nombre, ruta = job
    from kaggle_environments import make
    from kaggle_environments.agent import get_last_callable
    from kaggle_environments.utils import structify
    d = json.load(open(replay))
    steps = d["steps"]
    cfg = structify(make("kaggriculture").configuration)
    t0 = time.monotonic()
    try:
        fn = get_last_callable(open(ruta).read(), path=ruta)
    except Exception as e:
        return dict(replay=replay, seat=seat, cand=nombre, error=f"carga: {e}")
    iguales = fallos = n = 0
    primero = None
    for t in range(len(steps) - 1):
        obs = dict(steps[t][seat]["observation"])
        obs["step"] = steps[t][0]["observation"].get("step", t)
        real = steps[t + 1][seat].get("action")
        if real is None:
            continue
        try:
            a = fn(structify(obs), cfg) if fn.__code__.co_argcount >= 2 else fn(structify(obs))
        except Exception as e:
            return dict(replay=replay, seat=seat, cand=nombre, error=f"t{t}: {type(e).__name__}", n=n, iguales=iguales)
        n += 1
        if norm(a) == norm(real):
            iguales += 1
        else:
            fallos += 1
            if primero is None:
                primero = t
            if fallos >= MAX_FALLOS:
                break
    return dict(replay=replay, seat=seat, cand=nombre, n=n, iguales=iguales, fallos=fallos,
                primer_fallo=primero, completo=(n >= len(steps) - 2 and fallos < MAX_FALLOS),
                segundos=round(time.monotonic() - t0, 1))


def main():
    arg = sys.argv[1:]
    corte = arg.index("--")
    salida, carpetas, cands = arg[0], arg[1:corte], dict(x.split("=", 1) for x in arg[corte + 1:])
    replays = sorted(f for c in carpetas for f in glob.glob(f"replays/{c}/*.json"))
    jobs = []
    for r in replays:
        nombres = json.load(open(r))["info"]["TeamNames"]
        for seat in (0, 1):
            for n, p in cands.items():
                jobs.append((r, seat, n, p))
    print(f"{len(replays)} replays, {len(cands)} candidatos, {len(jobs)} comparaciones", flush=True)
    res = []
    with mp.Pool(11, maxtasksperchild=4) as pool:
        for i, x in enumerate(pool.imap_unordered(comparar, jobs), 1):
            res.append(x)
            if i % 200 == 0:
                print(f"  {i}/{len(jobs)}", flush=True)
    Path(salida).write_text(json.dumps(res))
    # resumen por (replay, asiento): mejor candidato
    por = {}
    for x in res:
        por.setdefault((x["replay"], x["seat"]), []).append(x)
    filas = []
    for (r, seat), xs in sorted(por.items()):
        d = json.load(open(r)); nombres = d["info"]["TeamNames"]
        rew = [s.get("reward") for s in d["steps"][-1]]
        mejor = max(xs, key=lambda x: (x.get("completo", False), x.get("iguales", 0)))
        copia = mejor.get("completo") and mejor.get("n", 0) >= MIN_TURNOS
        res_ = "V" if rew[seat] > rew[1 - seat] else ("D" if rew[seat] < rew[1 - seat] else "E")
        filas.append((Path(r).parent.name, nombres[seat], res_, mejor["cand"] if copia else "-", mejor.get("iguales"), mejor.get("n")))
    for f in filas:
        print("  ", *f)


if __name__ == "__main__":
    main()
