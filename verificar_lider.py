"""Reanálisis de registros ya completos, sin motor, red ni nuevas partidas.

Verifica cobertura, score desde rewards, noop, fuentes archivadas, hashes de
cintas y reproduce medias e intervalos desde episodios. Requiere scipy sólo
para el cuantil t del resumen, no kaggle-environments en ejecución.
"""
import argparse
import gzip
import hashlib
import itertools
import json
import math
from pathlib import Path
import statistics as st
import tarfile

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"docs/evidencia/lider_20260914"


def require(condition,message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def compare(actual,expected,path="summary"):
    if isinstance(actual,dict):
        require(set(actual)==set(expected),f"Claves distintas: {path}")
        for key in actual:
            compare(actual[key],expected[key],f"{path}/{key}")
    elif isinstance(actual,list):
        require(len(actual)==len(expected),f"Longitudes distintas: {path}")
        for i,(a,b) in enumerate(zip(actual,expected)):
            compare(a,b,f"{path}/{i}")
    elif isinstance(actual,(int,float)) and not isinstance(actual,bool):
        require(math.isclose(actual,expected,rel_tol=1e-10,abs_tol=1e-12),f"Número distinto: {path}")
    else:
        require(actual==expected,f"Valor distinto: {path}")


def verify(path):
    # Importar el módulo no carga el motor: sólo summarize necesita scipy.
    from evaluar_lider import summarize
    meta=json.loads(path.read_text())
    require(meta["state"]=="complete",f"No interpretar corrida {meta['state']}")
    payload=(path.parent/meta["episodes_file"]).read_bytes()
    require(sha(payload)==meta["episodes_sha256"],"Hash de episodios distinto")
    decoded=gzip.decompress(payload)
    rows=[json.loads(line) for line in decoded.splitlines()]
    plain=path.with_name(path.name.replace(".meta.json",".episodes.jsonl"))
    if plain.exists():
        require(plain.read_bytes()==decoded,"JSONL y gzip difieren")
    arms,opponents,seeds=meta["arms"],meta["opponents"],meta["seeds"]
    expected=set(itertools.product(arms,opponents,seeds,(0,1)))
    keyed={(r["arm"],r["opponent"],r["seed"],r["seat"]):r for r in rows}
    require(set(keyed)==expected and len(rows)==len(expected)==meta["expected_episodes"]==meta["completed_episodes"],
            "Cobertura incompleta o duplicada")
    for row in rows:
        require(row["valid"] and not row["errors"] and row["statuses"]==["DONE","DONE"],"Episodio inválido")
        require(row["steps"]==720 and row["action_counts"]==[719,719],"Pasos incompletos")
        a,b=row["rewards"][row["seat"]],row["rewards"][1-row["seat"]]
        require(math.isfinite(a) and math.isfinite(b),"Reward no finito")
        require(row["score"]==(1 if a>b else 0 if a<b else .5),"W/L/T mal calculado")
    count=0
    for o,s,p in itertools.product(opponents,seeds,(0,1)):
        a,b=keyed["base",o,s,p],keyed["noop",o,s,p]
        require(all(a[k]==b[k] for k in ("rewards","statuses","steps","action_hashes","action_counts","score")),"Noop distinto")
        count+=1
    with tarfile.open(path.with_name(path.name.replace(".meta.json",".sources.tgz")),"r:gz") as archive:
        members=archive.getmembers()
        source_names={name for name in meta["file_hashes"] if not name.startswith("bots/meta/tapes/")}
        require(len(members)==len(source_names) and {m.name for m in members}==source_names,"Archivo de fuentes incompleto")
        for member in members:
            require(member.isfile(),"Fuente no regular")
            require(sha(archive.extractfile(member).read())==meta["file_hashes"][member.name],"Fuente archivada distinta")
    for name,expected_hash in meta["file_hashes"].items():
        if name.startswith("bots/meta/tapes/"):
            require(sha((ROOT/name).read_bytes())==expected_hash,f"Cinta distinta: {name}")
    compare(summarize(rows,arms,opponents,seeds),meta["summary"])
    if "liquid_vs_tree" in meta:
        compare(summarize(rows,arms,opponents,seeds,reference="tree")["tree_liquid"],meta["liquid_vs_tree"])
    print(f"OK {path.name}: {len(rows)} episodios, {count} noop exactos, fuentes/cintas verificadas, resumen reproducido.")
    return meta


def verify_design(metas):
    by_phase={m["phase"]:m for m in metas}
    if not {"pilot","confirm","stress"} <= set(by_phase):
        return
    pilot,confirm,stress=(by_phase[k] for k in ("pilot","confirm","stress"))
    register=json.loads((OUT/"confirmacion_registro.json").read_text())
    require(sha((OUT/"pilot.meta.json").read_bytes())==register["pilot_sha256"],"Piloto registrado cambió")
    best=min((a for a in pilot["arms"] if a not in ("base","noop","_peor")),
             key=lambda a:(-pilot["summary"][a]["score"],a))
    require(best==register["candidate"],"Selección distinta al desempate registrado")
    n=math.ceil(((1.96+.84)*max(pilot["summary"][best]["delta"]["seed_sd"],.10)/.15)**2)
    require(register["raw_sample_size"]==n and register["n_seeds"]==min(32,max(16,n)),"Tamaño incorrecto")
    require(confirm["seeds"]==list(range(215000,215000+register["n_seeds"])),"Semillas de confirmación")
    require(stress["seeds"]==list(range(216000,216008)),"Semillas de diagnóstico")
    require(confirm["arms"]==stress["arms"]==["base","noop","_peor",best],"Candidato cambió")
    require(set(pilot["seeds"]).isdisjoint(confirm["seeds"]) and
            set(confirm["seeds"]).isdisjoint(stress["seeds"]),"Semillas solapadas")
    for other in (confirm,stress):
        for key in ("configs","engine_sha256","kaggle_environments"):
            compare(pilot[key],other[key],key)
        for name in set(pilot["file_hashes"]) & set(other["file_hashes"]):
            require(pilot["file_hashes"][name]==other["file_hashes"][name],f"Fuente cambió entre bloques: {name}")
    print("OK diseño: selección, tamaño previo, semillas disjuntas, controles y fuentes estables.")


def verify_duel():
    path=OUT/"duelo_hoz.json"
    if not path.exists():
        return
    meta=json.loads(path.read_text())
    require(meta["state"]=="complete","Duelo incompleto")
    raw=(OUT/meta["episodes_file"]).read_bytes()
    require(sha(raw)==meta["episodes_sha256"],"Hash de duelo")
    rows=[json.loads(line) for line in gzip.decompress(raw).splitlines()]
    expected=set(itertools.product(range(217000,217008),(0,1)))
    require(len(rows)==16 and {(r["seed"],r["seat"]) for r in rows}==expected,"Cobertura del duelo")
    for r in rows:
        require(r["arm"]==meta["candidate"] and r["opponent"]=="base","Identidad de duelo")
        require(r["valid"] and not r["errors"] and r["statuses"]==["DONE","DONE"] and
                r["steps"]==720 and r["action_counts"]==[719,719],"Duelo inválido")
        own,other=(r["rewards"][r["seat"]],r["rewards"][1-r["seat"]])
        require(math.isfinite(own) and math.isfinite(other),"Reward de duelo")
        require(r["score"]==(1 if own>other else 0 if own<other else .5),"Score de duelo")
    means=[st.mean(r["score"] for r in rows if r["seed"]==s) for s in meta["seeds"]]
    compare(means,meta["seed_scores"])
    compare(st.mean(means),meta["score"])
    from scipy.stats import t
    margin=float(t.ppf(.975,7))*st.stdev(means)/8**.5
    compare([st.mean(means)-margin,st.mean(means)+margin],meta["seed_ci95"])
    for label,value in (("wins",1),("ties",.5),("losses",0)):
        compare(sum(r["score"]==value for r in rows),meta[label])
    for name,value in meta["file_hashes"].items():
        require(sha((ROOT/name).read_bytes())==value,f"Fuente del duelo cambió: {name}")
    print("OK duelo: 16 episodios, scores, intervalo y fuentes verificadas.")


if __name__=="__main__":
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("manifests",nargs="*",type=Path)
    args=ap.parse_args()
    metas=[verify(path) for path in args.manifests or sorted(OUT.glob("*.meta.json"))]
    if not args.manifests:
        verify_design(metas)
        verify_duel()
