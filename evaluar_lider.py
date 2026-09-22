"""Panel reproducible para candidatos de arquitecturas distintas; nunca envía.

Uso: ./.venv/bin/python evaluar_lider.py --phase pilot
     ./.venv/bin/python evaluar_lider.py --phase confirm --candidate tree --seeds 16
"""
import argparse
from collections import defaultdict
from datetime import datetime, timezone
import gzip
import hashlib
from importlib.metadata import version
import itertools
import json
import math
from multiprocessing import Pool
from pathlib import Path
import statistics as st
import tarfile
import time

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"docs/evidencia/lider_20260914"
IDS=(107673304,107674284,107674293,107675268,107685970,107692988,107696961,107710951)


def encoded(obj):
    return json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def materialize(name):
    if name.startswith("guard:"):
        from bots.guardia_cinta import guard_cash, guard_commitments
        inner = materialize(name[6:]); st = {}
        def g(obs):
            return guard_commitments(obs, guard_cash(obs, inner(obs), reserve=6), st)
        return g
    from bots.chassis import make_agent
    from bots.arquetipos import CAMPEONA_HOZ,CAMPEONA_FB
    from bots.meta.tape import make as tape
    if name in ("base","noop"):
        return make_agent(dict(CAMPEONA_HOZ))
    if name=="_peor":
        return make_agent(dict(CAMPEONA_FB))
    if name.startswith(("maj_","sepopp_","lad_","top_","fuerte_","top2_","top3_")):
        return tape(name)
    if name.startswith("hib"):
        from bots.hibrido import make as mk_h
        corte={"hib10":240,"hib15":360,"hib20":480}[name]
        return mk_h("top_majkel1337_107570947", corte)
    if name=="tree_v2":
        from bots.arbol_lider import make as make_v2
        return make_v2()
    if name=="tree_v3":
        from bots.arbol_lider_v3 import make as make_v3
        return make_v3()
    from bots.experimentos_lider import make
    if name not in ("tree","tree_liquid","warmstart10"):
        raise ValueError(f"Candidato desconocido: {name}")
    return make(name)


def episode(job):
    arm,opp,seed,seat=job
    start=time.monotonic()
    result=dict(arm=arm,opponent=opp,seed=seed,seat=seat,valid=False)
    try:
        from kaggle_environments import make
        hashes=[hashlib.sha256(),hashlib.sha256()];counts=[0,0];timings=[[],[]]
        def traced(agent,p):
            def call(obs):
                tick=time.perf_counter()
                a=agent(obs)
                timings[p].append(time.perf_counter()-tick)
                hashes[p].update(encoded(dict(step=obs.get("step"),action=a))+b"\n")
                counts[p]+=1
                return a
            return call
        agents=[None,None]
        agents[seat]=traced(materialize(arm),seat)
        agents[1-seat]=traced(materialize(opp),1-seat)
        env=make("kaggriculture",configuration={"seed":seed,"episodeSteps":720},debug=False)
        env.run(agents)
        final=env.steps[-1]
        rewards=[s.reward for s in final];statuses=[str(s.status) for s in final]
        errors=[(t,p,str(s.status)) for t,step in enumerate(env.steps) for p,s in enumerate(step)
                if str(s.status) in ("ERROR","TIMEOUT","INVALID")]
        result.update(rewards=rewards,statuses=statuses,steps=len(env.steps),errors=errors,
                      action_hashes=[h.hexdigest() for h in hashes],action_counts=counts,
                      agent_ms=dict(mean=st.mean(timings[seat])*1000,max=max(timings[seat])*1000))
        if errors or statuses!=["DONE","DONE"] or len(env.steps)!=720 or counts!=[719,719]:
            raise ValueError("Episodio incompleto/inválido")
        if any(not isinstance(v,(int,float)) or not math.isfinite(v) for v in rewards):
            raise ValueError("Reward inválido")
        mine,theirs=rewards[seat],rewards[1-seat]
        result.update(valid=True,score=1.0 if mine>theirs else 0.0 if mine<theirs else 0.5)
    except Exception as exc:
        result["error"]=f"{type(exc).__name__}: {exc}"
    result["seconds"]=time.monotonic()-start
    return result


def uncertainty(matrix):
    """Filas=rival, columnas=semilla; asientos ya promediados."""
    from scipy.stats import t
    nr,ns=len(matrix),len(matrix[0]);n=nr*ns
    flat=[v for row in matrix for v in row];mean=st.mean(flat)
    by_seed=[st.mean(row[s] for row in matrix) for s in range(ns)]
    by_rival=[st.mean(row) for row in matrix]
    sd=st.stdev(by_seed) if ns>1 else 0
    se=sd/math.sqrt(ns)
    seed_margin=float(t.ppf(.975,ns-1))*se if ns>1 else None
    vr=nr/(nr-1)*sum((sum(row)-ns*mean)**2 for row in matrix)/(n*n) if nr>1 else 0
    vs=ns/(ns-1)*sum((sum(row[s] for row in matrix)-nr*mean)**2 for s in range(ns))/(n*n) if ns>1 else 0
    vc=n/(n-1)*sum((v-mean)**2 for v in flat)/(n*n) if n>1 else 0
    variance=vr+vs-vc
    df=min(nr,ns)-1
    twoway_margin=float(t.ppf(.975,df))*math.sqrt(variance) if variance>=0 and df>0 else None
    return dict(mean=mean,seed_sd=sd,seed_se=se,seed_deltas=by_seed,rival_deltas=by_rival,
                seed_ci95=[mean-seed_margin,mean+seed_margin] if seed_margin is not None else None,
                twoway_variance=variance,twoway_df=df,
                twoway_ci95=[mean-twoway_margin,mean+twoway_margin] if twoway_margin is not None else None)


def summarize(rows,arms,opponents,seeds,reference="base"):
    keyed={(r["arm"],r["opponent"],r["seed"],r["seat"]):r for r in rows}
    pairs={a:{(o,s):st.mean(keyed[a,o,s,p]["score"] for p in (0,1))
              for o,s in itertools.product(opponents,seeds)} for a in arms}
    result={}
    for a in arms:
        selected=[r for r in rows if r["arm"]==a]
        matrix=[[pairs[a][o,s]-pairs[reference][o,s] for s in seeds] for o in opponents]
        changed=sum(r["action_hashes"][r["seat"]]!=keyed[reference,r["opponent"],r["seed"],r["seat"]]["action_hashes"][r["seat"]] for r in selected)
        result[a]=dict(score=st.mean(pairs[a].values()),delta=uncertainty(matrix),
            wins=sum(r["score"]==1 for r in selected),ties=sum(r["score"]==.5 for r in selected),
            losses=sum(r["score"]==0 for r in selected),changed_actions=changed,episodes=len(selected),
            mean_money=st.mean(r["rewards"][r["seat"]] for r in selected),
            mean_agent_ms=st.mean(r["agent_ms"]["mean"] for r in selected),
            max_agent_ms=max(r["agent_ms"]["max"] for r in selected))
        result[a]["strata"]={prefix:st.mean(v for (o,s),v in pairs[a].items() if o.startswith(prefix))
                             for prefix in ("lad_","sepopp_","maj_") if any(o.startswith(prefix) for o in opponents)}
    return result


def run(args):
    from bots.arquetipos import CAMPEONA_HOZ,CAMPEONA_FB
    lad=sorted(p.name[:-8] for p in (ROOT/"bots/meta/tapes").glob("lad_*.json.gz"))
    recent=[f"sepopp_{i}" for i in IDS]
    if args.phase=="pilot":
        arms=["base","noop","_peor"]+[f"maj_{i}" for i in IDS]+["tree","tree_liquid","warmstart10"]
        opponents=lad[::5]+recent;seeds=list(range(214000,214004))
        assert len(opponents)==16
    elif args.phase=="confirm":
        assert args.candidate and args.seeds in range(16,33)
        arms=["base","noop","_peor",args.candidate]
        opponents=lad+recent;seeds=list(range(215000,215000+args.seeds))
    elif args.phase=="tapes":
        # 2026-09-21: successive halving sobre las 30 victorias de Majkel (sub
        # 56142830) como cintas SOLAS. Piloto barato; las mejores van a confirm.
        import glob as _g
        tops=sorted(Path(x).name[:-8] for x in _g.glob(str(ROOT/"bots/meta/tapes/top_majkel1337_*.json.gz")))
        clas={r["ep"]:r for r in json.load(open(ROOT/"results/clasif_MAJKEL_56142830.json"))}
        tops=[t for t in tops if clas.get(int(t.split("_")[-1]),{}).get("gana")]
        arms=["base","noop","maj_107674293"]+tops
        opponents=lad[::5]+recent;seeds=list(range(221000,221000+args.seeds))
    elif args.phase=="fuerte":
        # 2026-09-22: PANEL FUERTE. compare2 mostro que los brazos se ordenan al
        # reves segun la fuerza del rival y que el ladder sigue al subconjunto
        # fuerte. 80 rivales de Majkel y DSM (2000-3000), 8 seeds, 2 asientos.
        import glob as _g
        fuertes=sorted(Path(x).name[:-8] for x in _g.glob(str(ROOT/"bots/meta/tapes/fuerte_*.json.gz")))
        arms=["base","noop","maj_107674293","top_majkel1337_107570947","guard:top_majkel1337_107570947",
              "tree_v3","guard:tree_v3","tree"]
        opponents=fuertes;seeds=list(range(227000,227000+args.seeds))
    elif args.phase=="majkel2":
        # 2026-09-22: las 12 partidas de Majkel ACTUAL (3075) contra el top-3,
        # como candidatas con guardias, vs el panel fuerte SIN las cintas de
        # Majkel (71 rivales). Referencia: guard:107570947 (la candidata en ladder).
        import glob as _g
        c2=sorted(Path(x).name[:-8] for x in _g.glob(str(ROOT/"bots/meta/tapes/top2_majkel1337_*.json.gz")))
        fuertes=sorted(Path(x).name[:-8] for x in _g.glob(str(ROOT/"bots/meta/tapes/fuerte_*.json.gz")) if "majkel" not in Path(x).name)
        arms=["base","noop","guard:top_majkel1337_107570947"]+[f"guard:{t}" for t in c2]
        opponents=fuertes;seeds=list(range(230000,230000+args.seeds))
    elif args.phase=="majkel2_confirm":
        # 2026-09-22: confirmacion (successive halving) de las 3 mejores del
        # piloto majkel2 contra la candidata en ladder, 8 seeds, mismo bloque.
        import glob as _g
        fuertes=sorted(Path(x).name[:-8] for x in _g.glob(str(ROOT/"bots/meta/tapes/fuerte_*.json.gz")) if "majkel" not in Path(x).name)
        arms=["base","noop","guard:top_majkel1337_107570947",
              "guard:top2_majkel1337_110344288","guard:top2_majkel1337_110304538","guard:top2_majkel1337_110360751"]
        opponents=fuertes;seeds=list(range(232000,232000+args.seeds))
    elif args.phase=="hibrido":
        # 2026-09-22: cinta 107570947 hasta d10/d15/d20 + CAMPEONA_HOZ despues,
        # con guardias, vs panel fuerte sin Majkel/DSM. Referencia: guard:107570947.
        import glob as _g
        fuertes=sorted(Path(x).name[:-8] for x in _g.glob(str(ROOT/"bots/meta/tapes/fuerte_*.json.gz"))
                       if "majkel" not in Path(x).name and "dsm" not in Path(x).name)
        arms=["base","noop","guard:top_majkel1337_107570947","guard:hib10","guard:hib15","guard:hib20"]
        opponents=fuertes;seeds=list(range(233000,233000+args.seeds))
    elif args.phase=="dsm":
        # 2026-09-22: las 27 victorias de DSM (n1 actual, 3174) como candidatas
        # con guardias, vs panel fuerte SIN Majkel ni DSM (62 rivales).
        import glob as _g
        c3=sorted(Path(x).name[:-8] for x in _g.glob(str(ROOT/"bots/meta/tapes/top3_dsm_*.json.gz")))
        fuertes=sorted(Path(x).name[:-8] for x in _g.glob(str(ROOT/"bots/meta/tapes/fuerte_*.json.gz"))
                       if "majkel" not in Path(x).name and "dsm" not in Path(x).name)
        arms=["base","noop","guard:top_majkel1337_107570947"]+[f"guard:{t}" for t in c3]
        opponents=fuertes;seeds=list(range(231000,231000+args.seeds))
    elif args.phase=="compare2":
        # 2026-09-22: successive halving. Top-5 cintas solas del piloto `tapes`
        # (4 seeds) + arboles v1/v3 + cinta campeona, 16 seeds, mismo bloque.
        TOP5=["top_majkel1337_107649304","top_majkel1337_107603287","top_majkel1337_107570947",
              "top_majkel1337_107604888","top_majkel1337_107658008"]
        arms=["base","noop","_peor","maj_107674293","tree","tree_v3"]+TOP5
        opponents=lad+recent;seeds=list(range(223000,223000+args.seeds))
    elif args.phase=="compare":
        # 2026-09-21: arbol v1 (4 cintas) contra arbol v2 (30 victorias de la
        # sub 56142830) y la cinta desplegada, en el MISMO bloque.
        arms=["base","noop","_peor","tree","tree_v2","maj_107674293"]
        opponents=lad+recent;seeds=list(range(219000,219000+args.seeds))
    else:
        assert args.candidate
        arms=["base","noop","_peor",args.candidate]
        opponents=[f"maj_{i}" for i in IDS];seeds=list(range(216000,216008))
    tag=args.phase+("_"+args.candidate if args.candidate else "")
    manifest=OUT/f"{tag}.meta.json";raw=OUT/f"{tag}.episodes.jsonl"
    if manifest.exists() or raw.exists() or raw.with_suffix(raw.suffix+".gz").exists():
        raise FileExistsError(f"No sobrescribir corrida: {tag}")
    source_names=["evaluar_lider.py","bots/experimentos_lider.py","bots/chassis.py","bots/arquetipos.py","bots/meta/tape.py",
                  "docs/EXPERIMENTOS_ATREVIDOS_2026-09-14.md","bots/arbol_lider.py","results/clasif_MAJKEL_56142830.json","bots/arbol_lider_v3.py","bots/guardia_cinta.py","bots/hibrido.py"]
    tape_names=sorted(set(o for o in opponents if not o.startswith("guard:"))|{f"maj_{i}" for i in IDS})
    paths=[ROOT/n for n in source_names]+[ROOT/f"bots/meta/tapes/{n}.json.gz" for n in tape_names]
    hashes={str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in paths}
    import importlib
    engine=Path(importlib.import_module("kaggle_environments.envs.kaggriculture.kaggriculture").__file__)
    meta=dict(schema=1,state="running",phase=args.phase,arms=arms,opponents=opponents,seeds=seeds,
              started_at=datetime.now(timezone.utc).isoformat(),workers=args.workers,
              configs={"base":CAMPEONA_HOZ,"noop":CAMPEONA_HOZ,"_peor":CAMPEONA_FB},
              file_hashes=hashes,engine_sha256=sha(engine.read_bytes()),
              kaggle_environments=version("kaggle-environments"),expected_episodes=len(arms)*len(opponents)*len(seeds)*2)
    with tarfile.open(OUT/f"{tag}.sources.tgz","w:gz") as archive:
        for name in source_names:
            archive.add(ROOT/name,arcname=name)
    def save():
        manifest.write_text(json.dumps(meta,indent=2,ensure_ascii=False,allow_nan=False)+"\n")
    save();rows=[];keyed={};start=time.monotonic();last=start
    jobs=[(a,o,s,p) for o,s,p,a in itertools.product(opponents,seeds,(0,1),arms)]
    print(f"{tag}: {len(jobs)} episodios, {len(arms)} brazos, {len(opponents)} rivales, {len(seeds)} seeds",flush=True)
    try:
        with raw.open("x") as handle,Pool(args.workers) as pool:
            for row in pool.imap_unordered(episode,jobs,chunksize=1):
                handle.write(json.dumps(row,ensure_ascii=False,allow_nan=False)+"\n");handle.flush()
                if not row["valid"]:
                    raise ValueError(row)
                key=(row["arm"],row["opponent"],row["seed"],row["seat"])
                assert key not in keyed
                keyed[key]=row;rows.append(row)
                suffix=key[1:]
                if ("base",*suffix) in keyed and ("noop",*suffix) in keyed:
                    b,n=keyed["base",*suffix],keyed["noop",*suffix]
                    assert all(b[f]==n[f] for f in ("rewards","statuses","steps","action_hashes","action_counts","score")), "Noop distinto"
                if len(rows)%64==0 or time.monotonic()-last>=30:
                    meta["completed_episodes"]=len(rows);save();last=time.monotonic()
                    print(f"{len(rows)}/{len(jobs)}; {time.monotonic()-start:.0f}s",flush=True)
        assert len(rows)==len(jobs)
        assert hashes=={str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in paths}, "Fuentes cambiadas"
        assert meta["engine_sha256"]==sha(engine.read_bytes()), "Motor cambiado"
        meta.update(state="complete",completed_episodes=len(rows),summary=summarize(rows,arms,opponents,seeds),
                    finished_at=datetime.now(timezone.utc).isoformat(),runtime_seconds=time.monotonic()-start)
        # Conservar también comparación directa de la capa de ventas con su árbol.
        if "tree" in arms and "tree_liquid" in arms:
            meta["liquid_vs_tree"]=summarize(rows,arms,opponents,seeds,reference="tree")["tree_liquid"]
        save()
        compressed=raw.with_suffix(raw.suffix+".gz")
        compressed.write_bytes(gzip.compress(raw.read_bytes(),mtime=0))
        meta["episodes_file"]=compressed.name;meta["episodes_sha256"]=sha(compressed.read_bytes());save()
        for arm,r in sorted(meta["summary"].items(),key=lambda x:(-x[1]["score"],x[0])):
            print(arm, f"{r['score']:.2%}",f"delta {r['delta']['mean']:+.2%}",
                  "CIseed",r["delta"]["seed_ci95"],"CI2way",r["delta"]["twoway_ci95"],flush=True)
    except BaseException as exc:
        meta.update(state="failed",error=f"{type(exc).__name__}: {exc}",completed_episodes=len(rows));save()
        raise


if __name__=="__main__":
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--phase",choices=("pilot","confirm","stress","compare","tapes","compare2","fuerte","majkel2","dsm","majkel2_confirm","hibrido"),required=True)
    ap.add_argument("--candidate")
    ap.add_argument("--seeds",type=int,default=16)
    ap.add_argument("--workers",type=int,default=8)
    run(ap.parse_args())
