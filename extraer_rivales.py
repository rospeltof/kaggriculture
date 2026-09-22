"""Extrae los RIVALES de un jugador objetivo en una carpeta de replays, como
cintas `fuerte_<slug>_<episodio>`. Los rivales de un top-5 son top-tier
(2000-3000): forman el PANEL FUERTE, la poblacion que el ladder nos empareja
al subir y la que compare2 mostro que decide (2026-09-22).

Uso: ./.venv/bin/python extraer_rivales.py <Objetivo> <carpeta>
"""
import glob, gzip, json, os, re, sys, unicodedata
DIR = os.path.join("bots", "meta", "tapes")
def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return (re.sub(r"[^a-zA-Z0-9]+", "_", s).strip("_").lower() or "rival")[:18]
def main(obj, carpeta):
    hechos = []
    for f in sorted(glob.glob(f"replays/{carpeta}/*.json")):
        d = json.load(open(f)); nm = d["info"]["TeamNames"]
        if obj not in nm: continue
        me = nm.index(obj); riv = 1 - me; S = d["steps"]; ep = d["info"]["EpisodeId"]
        tr = []
        for t in range(len(S)):
            a = (S[t + 1][riv].get("action") or {}) if t + 1 < len(S) else {}
            tr.append({"farmer": a.get("farmer") or ["PASS"], "hands": a.get("hands") or [], "market": a.get("market") or []})
        nombre = f"fuerte_{slug(nm[riv])}_{ep}"
        with gzip.open(os.path.join(DIR, nombre + ".json.gz"), "wt") as fh:
            json.dump(tr, fh, separators=(",", ":"))
        hechos.append((nombre, nm[riv], S[-1][riv].get("reward") or 0))
    print(f"{len(hechos)} rivales de {obj} en {carpeta} -> fuerte_*")
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
