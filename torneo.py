"""Torneo en bucle cerrado entre agentes-fichero, cargados exactamente como Kaggle
(kaggle_environments ejecuta el fichero y usa el ULTIMO callable; le pasa obs y
configuracion segun co_argcount).

Uso:
  torneo.py --out results/torneo_X --seeds 10 --seed0 910000 --workers 11 \
            nombre=ruta.py nombre2=ruta2.py ... [--vs nombre]

--vs a,b limita a las parejas que incluyen a alguno de esos agentes (brazos): cada brazo
contra todo el pool y los brazos entre si; sin --vs, todos contra todos.
Escribe <out>.jsonl (una fila por episodio) y <out>.meta.json (sha256 de cada fichero).
"""
import argparse, hashlib, itertools, json, math, multiprocessing as mp, os, statistics as st, sys, time, tarfile
from pathlib import Path


def episodio(job):
    a, pa, b, pb, seed, seat = job
    t0 = time.monotonic()
    r = dict(a=a, b=b, seed=seed, seat=seat, valid=False,
             runtime=dict(python_hash_seed=os.environ.get('PYTHONHASHSEED'), wheat_hash=hash('WHEAT')))
    try:
        from kaggle_environments import make
        from kaggle_environments.agent import build_agent
        agents = [None, None]
        paths=[None,None];paths[seat],paths[1-seat]=pa,pb
        hashes=[hashlib.sha256(),hashlib.sha256()];counts=[0,0]
        def traced(path,p):
            loaded,_=build_agent(path,{},"kaggriculture")
            def call(obs,config):
                action=loaded(obs,config)
                hashes[p].update(json.dumps(action,sort_keys=True,separators=(',',':'),allow_nan=False).encode()+b'\n')
                counts[p]+=1
                return action
            return call
        agents=[traced(path,p) for p,path in enumerate(paths)]
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
        if not all(isinstance(v,(int,float)) and math.isfinite(v) for v in rew):
            raise ValueError('Reward no finito')
        mine, theirs = rew[seat], rew[1 - seat]
        try:
            r["shops2"] = list(env.steps[-1][0]["observation"]["town"]["unlocked_shops"][:2])
        except Exception:
            r["shops2"] = None
        r.update(rewards=rew, statuses=stat, n_err=len(errs), errors=errs[:5], steps=len(env.steps),
                 score=1.0 if mine > theirs else 0.0 if mine < theirs else 0.5, margin=mine - theirs,
                 ms=[dict(mean=1000 * st.mean(d), max=1000 * max(d)) if d else None for d in dur])
        r.update(action_hashes=[h.hexdigest() for h in hashes],action_counts=counts)
        r["valid"] = not errs and stat == ["DONE", "DONE"] and len(env.steps) == 720 and counts==[719,719]
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
    ap.add_argument("--lista-semillas", default=None, help="semillas explicitas separadas por comas (ignora --seeds/--seed0)")
    ap.add_argument("--sin-cruces", action="store_true", help="con --vs: no jugar brazo contra brazo")
    ap.add_argument("--fresco", action="store_true", help="un proceso nuevo por partida (agentes multi-fichero con estado en modulos importados)")
    args = ap.parse_args()
    if any(Path(args.out+s).exists() for s in ('.jsonl','.meta.json','.sources.tgz')):
        sys.exit('No sobrescribir un torneo existente')
    Path(args.out).parent.mkdir(parents=True,exist_ok=True)
    ag = dict(x.split("=", 1) for x in args.agentes)
    for n, p in ag.items():
        if not Path(p).exists():
            sys.exit(f"no existe {p}")
    meta = dict(agentes={n: dict(ruta=p, sha256=hashlib.sha256(Path(p).read_bytes()).hexdigest()) for n, p in ag.items()},
                seeds=[int(x) for x in args.lista_semillas.split(',')] if args.lista_semillas else list(range(args.seed0, args.seed0 + args.seeds)), vs=args.vs, inicio=time.strftime("%Y-%m-%d %H:%M:%S"))
    brazos = args.vs.split(",") if args.vs else None
    parejas = [(a, b) for a, b in itertools.combinations(ag, 2) if brazos is None or a in brazos or b in brazos]
    if brazos:
        parejas = [(a, b) if a in brazos else (b, a) for a, b in parejas]
        if args.sin_cruces:
            parejas = [(a, b) for a, b in parejas if b not in brazos]
    jobs = [(a, ag[a], b, ag[b], s, seat) for a, b in parejas for s in meta["seeds"] for seat in (0, 1)]
    import importlib
    from importlib.metadata import version
    engine=Path(importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture').__file__)
    meta.update(state='running',expected_episodes=len(jobs),workers=args.workers,
                runtime=dict(python_version=sys.version, multiprocessing_start_method=mp.get_start_method(),
                             python_hash_seed=os.environ.get('PYTHONHASHSEED'), wheat_hash=hash('WHEAT')),
                engine_sha256=hashlib.sha256(engine.read_bytes()).hexdigest(),
                kaggle_environments=version('kaggle-environments'),
                runner_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    with tarfile.open(args.out+'.sources.tgz','w:gz') as archive:
        archive.add(__file__,arcname='torneo.py')
        for name,path in ag.items():archive.add(path,arcname=f'agents/{name}.py')
    def save():Path(args.out+'.meta.json').write_text(json.dumps(meta,indent=2))
    save()
    print(f"{len(ag)} agentes, {len(parejas)} parejas, {len(jobs)} episodios", flush=True)
    rows = []
    try:
        with mp.Pool(args.workers, maxtasksperchild=1 if args.fresco else None) as pool, open(args.out + ".jsonl", "x") as f:
            for i, r in enumerate(pool.imap_unordered(episodio, jobs), 1):
                rows.append(r)
                f.write(json.dumps(r) + "\n"); f.flush()
                if not r['valid']:raise ValueError(f'Episodio inválido: {r}')
                if i % 50 == 0:
                    meta['completed_episodes']=i;save()
                    print(f"  {i}/{len(jobs)}", flush=True)
        expected={(a,b,s,p) for a,_,b,_,s,p in jobs}
        assert len(rows)==len(expected)==len({(r['a'],r['b'],r['seed'],r['seat']) for r in rows})
        assert {(r['a'],r['b'],r['seed'],r['seat']) for r in rows}==expected
        for n,p in ag.items():
            assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==meta['agentes'][n]['sha256'],f'Cambió {n}'
        assert hashlib.sha256(engine.read_bytes()).hexdigest()==meta['engine_sha256']
        assert hashlib.sha256(Path(__file__).read_bytes()).hexdigest()==meta['runner_sha256']
        meta.update(state='complete',completed_episodes=len(rows),fin=time.strftime('%Y-%m-%d %H:%M:%S'))
        save()
    except BaseException as exc:
        meta.update(state='failed',completed_episodes=len(rows),error=str(exc));save()
        raise
    resumen(rows, list(ag))


if __name__ == "__main__":
    main()
