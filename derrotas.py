"""Clasifica los replays de UNA submission en victorias/derrotas y perfila al rival.

Nace del pedido del usuario (2026-08-31): reconstruir rivales reales de nuestra
banda para tener un panel con resolución. El panel actual está saturado (base,
_noop y candidato leen idéntico 0/0/100/100) y por eso es ciego a las mejoras.

Guard anti-mezcla: sólo lee replays/<BOT>/ y verifica que 'Rospel' esté en
TeamNames. Nunca cruza generaciones.

Uso:
    ./.venv/bin/python derrotas.py                 # tabla de resultados
    ./.venv/bin/python derrotas.py --perfil        # + composición del rival al final
"""
import argparse
import glob
import json
import os
from collections import Counter

YO = "Rospel"
PROD = {"GOOSE": "EGG", "COW": "MILK", "SHEEP": "WOOL"}


def cargar(path):
    d = json.load(open(path))
    names = d["info"]["TeamNames"]
    if YO not in names:
        return None
    me = names.index(YO)
    rew = d["steps"][-1]
    return {
        "ep": d["info"]["EpisodeId"],
        "rival": names[1 - me],
        "me": me,
        "mio": rew[me].get("reward") or 0,
        "suyo": rew[1 - me].get("reward") or 0,
        "steps": d["steps"],
    }


def composicion(steps, idx):
    """Cuenta tiles del jugador idx en el último step observable."""
    obs = steps[-1][0]["observation"]
    farm = obs["farms"][idx]
    c = Counter()
    for row in farm["tiles"]:
        for t in row:
            if not isinstance(t, dict):
                continue
            if t.get("animal"):
                c[t["animal"]] += 1
            elif t.get("kind") == "PLANT":
                c[t["crop"]] += 1
            elif t.get("kind") == "WEED":
                c["WEED"] += 1
    c["quadrants"] = len(farm.get("unlocked_quadrants", []))
    c["hands"] = len(farm.get("hands", []))
    return c


def main(perfil=False, bot="CAMPEONA_FB"):
    files = sorted(glob.glob(f"replays/{bot}/*.json"))
    rows = [r for r in (cargar(f) for f in files) if r]
    rows.sort(key=lambda r: r["mio"] - r["suyo"])
    w = sum(1 for r in rows if r["mio"] > r["suyo"])
    l = sum(1 for r in rows if r["mio"] < r["suyo"])
    t = len(rows) - w - l
    print(f"{bot}: {len(rows)} partidas -> {w}V {l}D {t}E "
          f"({100.0*(w+0.5*t)/max(1,len(rows)):.1f}%)")
    print(f"\n{'episodio':>10} {'rival':22s} {'nuestro':>9} {'suyo':>9} {'margen':>9}")
    for r in rows:
        marca = "  DERROTA" if r["mio"] < r["suyo"] else ""
        print(f"{r['ep']:>10} {r['rival'][:22]:22s} {r['mio']:>9,.0f} {r['suyo']:>9,.0f} "
              f"{r['mio']-r['suyo']:>+9,.0f}{marca}")
    if perfil:
        print(f"\n--- composición final del RIVAL en las derrotas ---")
        for r in rows:
            if r["mio"] >= r["suyo"]:
                continue
            c = composicion(r["steps"], 1 - r["me"])
            top = {k: v for k, v in c.most_common() if k not in ("quadrants", "hands")}
            print(f"  {r['ep']} {r['rival'][:18]:18s} q{c['quadrants']} h{c['hands']:>2} "
                  f"{dict(list(top.items())[:8])}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--perfil", action="store_true")
    ap.add_argument("--bot", default="CAMPEONA_FB")
    main(**vars(ap.parse_args()))
