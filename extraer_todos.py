"""Extrae TODOS los rivales de una carpeta de replays como cintas de panel.

Nace de la pregunta bloqueante (2026-09-02): el ladder no reproduce el orden de
nuestro panel de 5 cintas. Con los 40 rivales REALES de campeona_ruta como panel,
podemos ver cual de los dos ordenamientos miente.

Nombres con sufijo de episodio: dos partidas del mismo rival NO deben colisionar
(casi contaminamos el panel sobrescribiendo axel_ahmer).
"""
import glob, gzip, json, os, re, sys, unicodedata

YO = "Rospel"
DIR = os.path.join("bots", "meta", "tapes")


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return (re.sub(r"[^a-zA-Z0-9]+", "_", s).strip("_").lower() or "rival")[:18]


def main(carpeta):
    os.makedirs(DIR, exist_ok=True)
    hechos = []
    for f in sorted(glob.glob(f"replays/{carpeta}/*.json")):
        d = json.load(open(f))
        nm = d["info"]["TeamNames"]
        if YO not in nm:
            continue
        me = nm.index(YO); opp = 1 - me
        S = d["steps"]
        ep = d["info"]["EpisodeId"]
        nombre = f"lad_{slug(nm[opp])}_{ep}"
        tr = []
        for t in range(len(S)):
            a = (S[t + 1][opp].get("action") or {}) if t + 1 < len(S) else {}
            tr.append({"farmer": a.get("farmer") or ["PASS"],
                       "hands": a.get("hands") or [],
                       "market": a.get("market") or []})
        with gzip.open(os.path.join(DIR, nombre + ".json.gz"), "wt") as fh:
            json.dump(tr, fh, separators=(",", ":"))
        hechos.append((nombre, nm[opp], S[-1][me].get("reward") or 0,
                       S[-1][opp].get("reward") or 0, d["info"].get("seed")))
    json.dump([{"cinta": h[0], "rival": h[1], "nuestro": h[2], "suyo": h[3], "seed": h[4]}
               for h in hechos], open(f"results/panel_{carpeta}.json", "w"), indent=1)
    v = sum(1 for h in hechos if h[2] > h[3])
    print(f"{len(hechos)} cintas de {carpeta}: marcador real {v}V {len(hechos)-v}D "
          f"({100*v/len(hechos):.1f}%)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "CAMPEONA_RUTA")
