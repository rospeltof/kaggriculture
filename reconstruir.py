"""Extrae la cinta de 720 turnos de un rival desde un replay NUESTRO y la valida.

Guard anti-mezcla: sólo lee replays/CAMPEONA_FB/ y exige 'Rospel' en TeamNames.

Validación: el replay guarda el seed. Si la cinta es fiel y nuestro bot es el
mismo, correrla contra campeona_fb con ese seed debe reproducir el marcador
original. La desviación se reporta como fidelidad.

Uso:
    ./.venv/bin/python reconstruir.py --ep 104210270 --nombre uman_n3l
    ./.venv/bin/python reconstruir.py --derrotas 8      # las N derrotas más ajustadas
"""
import argparse
import glob
import gzip
import json
import os
import re
import unicodedata

YO = "Rospel"
DIR = os.path.join("bots", "meta", "tapes")


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "_", s).strip("_").lower()
    return s or "rival"


BOT = "CAMPEONA_FB"          # carpeta activa; la fija main() con --bot


def leer(ep):
    path = f"replays/{BOT}/episode-{ep}-replay.json"
    d = json.load(open(path))
    names = d["info"]["TeamNames"]
    assert YO in names, f"{ep}: replay ajeno (TeamNames={names})"
    me = names.index(YO)
    return d, me, names[1 - me]


def extraer(ep, nombre=None):
    d, me, rival = leer(ep)
    opp = 1 - me
    # OFFSET (verificado 2026-08-31): en el replay descargado la acción del índice
    # t es la que YA se aplicó para llegar a ese estado, no la que se toma desde él.
    # Sin el shift la simulación va un turno por detrás y la granja colapsa
    # (medido: $12,470 contra los $85,804 reales). Con shift=1 la reproducción es
    # EXACTA en los 720 turnos, dinero al centavo.
    S = d["steps"]
    trace = []
    for t in range(len(S)):
        a = (S[t + 1][opp].get("action") or {}) if t + 1 < len(S) else {}
        trace.append({"farmer": a.get("farmer") or ["PASS"],
                      "hands": a.get("hands") or [],
                      "market": a.get("market") or []})
    nombre = nombre or slug(rival)
    os.makedirs(DIR, exist_ok=True)
    with gzip.open(os.path.join(DIR, nombre + ".json.gz"), "wt") as fh:
        json.dump(trace, fh, separators=(",", ":"))
    real_mio = d["steps"][-1][me].get("reward") or 0
    real_suyo = d["steps"][-1][opp].get("reward") or 0
    return nombre, rival, d["info"].get("seed"), real_mio, real_suyo, me


def _tape_nuestra(ep, me):
    """Nuestra propia cinta del mismo episodio: sirve para validar la extracción."""
    d, _, _ = leer(ep)
    S = d["steps"]
    tr = []
    for t in range(len(S)):
        a = (S[t + 1][me].get("action") or {}) if t + 1 < len(S) else {}
        tr.append({"farmer": a.get("farmer") or ["PASS"],
                   "hands": a.get("hands") or [],
                   "market": a.get("market") or []})
    os.makedirs(DIR, exist_ok=True)
    with gzip.open(os.path.join(DIR, "_self.json.gz"), "wt") as fh:
        json.dump(tr, fh, separators=(",", ":"))
    import bots.meta.tape as T
    T._CACHE.pop("_self", None)
    return "bots.meta.tape:_self"


def validar(ep, nombre, seed, me):
    """(a) cinta-vs-cinta debe reproducir el marcador EXACTO; (b) cinta vs bot vivo."""
    from kaggle_environments import make as mk
    from harness import materialize
    import bots.meta.tape as T
    T._CACHE.pop(nombre, None)
    cinta = materialize(f"bots.meta.tape:{nombre}")

    env = mk("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=False)
    self_spec = _tape_nuestra(ep, me)
    par = [None, None]
    par[me] = materialize(self_spec)
    par[1 - me] = cinta
    env.run(par)
    fin = env.steps[-1]
    fiel = (fin[me].reward or 0, fin[1 - me].reward or 0)

    env2 = mk("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=False)
    par2 = [None, None]
    par2[me] = materialize("bots.arquetipos:campeona_fb")
    par2[1 - me] = materialize(f"bots.meta.tape:{nombre}")
    env2.run(par2)
    f2 = env2.steps[-1]
    vivo = (f2[me].reward or 0, f2[1 - me].reward or 0)
    return fiel, vivo


def main(ep=None, nombre=None, derrotas=0, bot=None):
    global BOT
    if bot:
        BOT = bot
    eps = []
    if ep:
        eps = [(ep, nombre)]
    elif derrotas:
        rows = []
        for f in glob.glob(f"replays/{BOT}/*.json"):
            d = json.load(open(f))
            names = d["info"]["TeamNames"]
            if YO not in names:
                continue
            me = names.index(YO)
            mio = d["steps"][-1][me].get("reward") or 0
            suyo = d["steps"][-1][1 - me].get("reward") or 0
            if mio < suyo:
                rows.append((suyo - mio, d["info"]["EpisodeId"]))
        rows.sort()
        eps = [(e, None) for _, e in rows[:derrotas]]
    print(f"{'episodio':>10} {'rival':18s} {'real (yo/rival)':>19} {'extraccion':>10} "
          f"{'vs bot vivo':>19} {'agente':>28}")
    for e, n in eps:
        nom, rival, seed, rm, rs, me = extraer(e, n)
        fiel, vivo = validar(e, nom, seed, me)
        ok = "EXACTA" if fiel == (rm, rs) else "FALLA"
        print(f"{e:>10} {rival[:18]:18s} {rm:>8,.0f}/{rs:<10,.0f} {ok:>10} "
              f"{vivo[0]:>8,.0f}/{vivo[1]:<10,.0f} {'bots.meta.tape:' + nom:>28}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ep", type=int)
    ap.add_argument("--nombre")
    ap.add_argument("--derrotas", type=int, default=0)
    ap.add_argument("--bot", default=None, help="carpeta de replays/ (default CAMPEONA_FB)")
    main(**vars(ap.parse_args()))
