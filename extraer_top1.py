"""Extrae las cintas del TOP1 (tetsuya) de replays donde NO jugamos nosotros.

`extraer_todos.py` filtra por YO="Rospel" y saca al rival; aqui el objetivo es un
jugador concreto en partidas de terceros. Prefijo `top_` para NO colisionar con
el panel `lad_*` de 40 rivales reales (panel40.py hace glob de lad_*): son dos
poblaciones distintas y mezclarlas seria justo el error que el panel de 5 nos
enseno a no cometer.

Uso:  ./.venv/bin/python extraer_top1.py [TeamName] [carpeta]
"""
import glob, gzip, json, os, sys

OBJETIVO = sys.argv[1] if len(sys.argv) > 1 else "tetsuya"
CARPETA = sys.argv[2] if len(sys.argv) > 2 else "TOP1"
DIR = os.path.join("bots", "meta", "tapes")


def main():
    os.makedirs(DIR, exist_ok=True)
    hechos = []
    for f in sorted(glob.glob(f"replays/{CARPETA}/*.json")):
        d = json.load(open(f))
        nm = d["info"]["TeamNames"]
        if OBJETIVO not in nm:
            continue
        yo = nm.index(OBJETIVO); riv = 1 - yo
        S = d["steps"]
        ep = d["info"]["EpisodeId"]
        nombre = f"top_{OBJETIVO.lower()}_{ep}"
        tr = []
        for t in range(len(S)):
            # shift=1: la accion en el indice t del replay es la YA aplicada
            a = (S[t + 1][yo].get("action") or {}) if t + 1 < len(S) else {}
            tr.append({"farmer": a.get("farmer") or ["PASS"],
                       "hands": a.get("hands") or [],
                       "market": a.get("market") or []})
        with gzip.open(os.path.join(DIR, nombre + ".json.gz"), "wt") as fh:
            json.dump(tr, fh, separators=(",", ":"))
        hechos.append((nombre, nm[riv], S[-1][yo].get("reward") or 0,
                       S[-1][riv].get("reward") or 0))
    v = sum(1 for h in hechos if h[2] > h[3])
    print(f"{len(hechos)} cintas de {OBJETIVO}: marcador real {v}V {len(hechos)-v}D")
    for h in hechos:
        print(f"  {h[0]:32s} vs {h[1][:18]:18s} {h[2]:>9,.0f} - {h[3]:>9,.0f}")


if __name__ == "__main__":
    main()
