"""Extrae de una carpeta de replays de UNA submission ajena:
  - las VICTORIAS del duenyo como cintas candidatas `<prefijo>_<ep>`
  - todos sus RIVALES como cintas de panel fuerte `fuerte_<slug>_<ep>`
El duenyo se detecta como el TeamName presente en todas las partidas (las
submissions pueden renombrar el equipo: se usa el nombre de cada replay).
shift=1: la accion en el indice t+1 del replay es la aplicada en t.
Uso: ./.venv/bin/python extraer_fuente.py <CARPETA> <prefijo>
"""
import collections, glob, gzip, json, os, re, sys, unicodedata

DIR = os.path.join("bots", "meta", "tapes")


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return (re.sub(r"[^a-zA-Z0-9]+", "_", s).strip("_").lower() or "rival")[:18]


def cinta(S, p):
    tr = []
    for t in range(len(S)):
        a = (S[t + 1][p].get("action") or {}) if t + 1 < len(S) else {}
        tr.append({"farmer": a.get("farmer") or ["PASS"], "hands": a.get("hands") or [],
                   "market": a.get("market") or []})
    return tr


def main(carpeta, prefijo):
    files = sorted(glob.glob(f"replays/{carpeta}/*.json"))
    cnt = collections.Counter()
    for f in files:
        cnt.update(set(json.load(open(f))["info"]["TeamNames"]))
    dueno = cnt.most_common(1)[0][0]
    v = n = r = 0
    for f in files:
        d = json.load(open(f)); nm = d["info"]["TeamNames"]
        if dueno not in nm:
            continue
        p = nm.index(dueno); rw = d["rewards"]; S = d["steps"]; ep = d["info"]["EpisodeId"]
        if rw[p] is None or rw[1 - p] is None or len(S) < 720:
            continue
        n += 1
        with gzip.open(os.path.join(DIR, f"fuerte_{slug(nm[1 - p])}_{ep}.json.gz"), "wt") as fh:
            json.dump(cinta(S, 1 - p), fh, separators=(",", ":")); r += 1
        if rw[p] > rw[1 - p]:
            with gzip.open(os.path.join(DIR, f"{prefijo}_{ep}.json.gz"), "wt") as fh:
                json.dump(cinta(S, p), fh, separators=(",", ":")); v += 1
    print(f"{carpeta}: duenyo '{dueno}' ({cnt[dueno]}/{len(files)}), {n} partidas, "
          f"{v} victorias -> {prefijo}_*, {r} rivales -> fuerte_*")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
