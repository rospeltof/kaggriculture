"""Torneo en bucle cerrado entre agentes-fichero, cargados exactamente como Kaggle
(kaggle_environments ejecuta el fichero y usa el ULTIMO callable; le pasa obs y
configuracion segun co_argcount).

Uso:
  torneo.py --out results/torneo_X --seeds 10 --seed0 910000 --workers 11 \
            nombre=ruta.py nombre2=ruta2.py ... [--vs nombre]

--vs limita a las parejas que incluyen a ese agente; sin --vs, todos contra todos.
Escribe <out>.jsonl (una fila por episodio) y <out>.meta.json (sha256 de cada fichero).
"""
import argparse, hashlib, itertools, json, multiprocessing as mp, statistics as st, sys, time
from pathlib import Path


def episodio(job):
    a, pa, b, pb, seed, seat = job
    t0 = time.monotonic()
    r = dict(a=a, b=b, seed=seed, seat=seat, valid=False)
    try:
        from kaggle_environments import make
        agents = [None, None]
        agents[seat], agents[1 - seat] = pa, pb
        env = make("kaggriculture", configuration={"seed": seed, "episodeSteps": 720}, debug=False)
        env.run(agents)
        final = env.steps[-1]
        rew = [s.reward for s in final]
        stat = [str(s.status) for s in final]
        errs = [(t, p, str(s.status)) for t, step in enumerate(env.steps) for p, s in enumerate(step)
                if str(s.status) in ("ERROR", "TIMEOUT", "INVALID")]
        dur = [[], []]
        for logs in env.logs:
            for p, lg in enumerate(logs or []):
                if isinstance(lg, dict) and "duration" in lg:
                    dur[p].append(lg["duration"])
        mine, theirs = rew[seat], rew[1 - seat]
        r.update(rewards=rew, statuses=stat, n_err=len(errs), errors=errs[:5], steps=len(env.steps),
                 score=1.0 if mine > theirs else 0.0 if mine < theirs else 0.5, margin=mine - theirs,
                 ms=[dict(mean=1000 * st.mean(d), max=1000 * max(d)) if d else None for d in dur])
        r["valid"] = not errs and stat == ["DONE", "DONE"] and len(env.steps) == 720
    except Exception as exc:
        r["error"] = f"{type(exc).__name__}: {exc}"
    r["seconds"] = time.monotonic() - t0
    return r


def resumen(rows, nombres):
    ok = [r for r in rows if r["valid"]]
    print(f"episodios validos {len(ok)}/{len(rows)}; con error: {len(rows) - len(ok)}")
    for r in rows:
        if not r["valid"]:
            print("  INVALIDO", r["a"], r["b"], r["seed"], r["seat"], r.get("error"), r.get("errors"))
    total = {n: [] for n in nombres}
    print(f"\n{'A':>10s} {'B':>10s}  W-L-T de A   %A    margen medio A   semillas A>B")
    for a, b in sorted({(r["a"], r["b"]) for r in ok}):
        rr = [r for r in ok if r["a"] == a and r["b"] == b]
        w = sum(r["score"] == 1 for r in rr); l = sum(r["score"] == 0 for r in rr); t = len(rr) - w - l
        pct = 100 * st.mean(r["score"] for r in rr)
        por_semilla = {}
        for r in rr:
            por_semilla.setdefault(r["seed"], []).append(r["score"])
        gana = sum(st.mean(v) > .5 for v in por_semilla.values())
        print(f"{a:>10s} {b:>10s}  {w:3d}-{l:3d}-{t:2d}  {pct:5.1f}  {st.mean(r['margin'] for r in rr):+10.0f}   {gana}/{len(por_semilla)}")
        total[a] += [r["score"] for r in rr]
        total[b] += [1 - r["score"] for r in rr]
    print("\nPuntuacion media contra todos los demas:")
    for n, v in sorted(total.items(), key=lambda kv: -st.mean(kv[1]) if kv[1] else 0):
        if v:
            print(f"  {n:>10s} {100 * st.mean(v):5.1f}%  ({len(v)} ep)")
    ms = {}
    for r in ok:
        for p, m in enumerate(r["ms"]):
            if m:
                n = r["a"] if p == r["seat"] else r["b"]
                ms.setdefault(n, []).append(m["max"])
    print("\nms max por turno (peor episodio): " + ", ".join(f"{n} {max(v):.0f}" for n, v in ms.items()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("agentes", nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--seed0", type=int, default=910000)
    ap.add_argument("--workers", type=int, default=11)
    ap.add_argument("--vs", default=None)
    args = ap.parse_args()
    ag = dict(x.split("=", 1) for x in args.agentes)
    for n, p in ag.items():
        if not Path(p).exists():
            sys.exit(f"no existe {p}")
    meta = dict(agentes={n: dict(ruta=p, sha256=hashlib.sha256(Path(p).read_bytes()).hexdigest()) for n, p in ag.items()},
                seeds=list(range(args.seed0, args.seed0 + args.seeds)), vs=args.vs, inicio=time.strftime("%Y-%m-%d %H:%M:%S"))
    parejas = [(a, b) for a, b in itertools.combinations(ag, 2) if args.vs in (None, a, b)]
    if args.vs:
        parejas = [(args.vs, b if a == args.vs else a) for a, b in parejas]
    jobs = [(a, ag[a], b, ag[b], s, seat) for a, b in parejas for s in meta["seeds"] for seat in (0, 1)]
    print(f"{len(ag)} agentes, {len(parejas)} parejas, {len(jobs)} episodios", flush=True)
    rows = []
    with mp.Pool(args.workers) as pool, open(args.out + ".jsonl", "w") as f:
        for i, r in enumerate(pool.imap_unordered(episodio, jobs), 1):
            rows.append(r)
            f.write(json.dumps(r) + "\n"); f.flush()
            if i % 50 == 0:
                print(f"  {i}/{len(jobs)}", flush=True)
    for n, p in ag.items():
        if hashlib.sha256(Path(p).read_bytes()).hexdigest() != meta["agentes"][n]["sha256"]:
            print(f"!! {n}: el fichero cambio durante el torneo")
    meta["fin"] = time.strftime("%Y-%m-%d %H:%M:%S")
    Path(args.out + ".meta.json").write_text(json.dumps(meta, indent=2))
    resumen(rows, list(ag))


if __name__ == "__main__":
    main()
