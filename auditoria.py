"""Qué se nos está pasando: auditoría de los replays de UNA submission.

Complementa a derrotas.py (que clasifica) mirando DENTRO de las partidas:
  A) trayectoria del margen por día -> ¿dónde se decide la partida?
  B) qué producto explica el margen final (unidades vendidas nuestras vs suyas)
  C) composición del rival en victorias vs derrotas
  D) fugas propias: plantas muertas, weeds, sobrante sin vender, producción capada

Guard anti-mezcla: solo lee replays/<BOT>/ y exige 'Rospel' en TeamNames.

Uso: ./.venv/bin/python auditoria.py --bot CAMPEONA_ALBA
"""
import argparse
import glob
import json
from collections import Counter, defaultdict

YO = "Rospel"
BASE = {"WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120, "MELON": 250,
        "EGG": 50, "MILK": 160, "WOOL": 200, "FERTILIZER": 100}


def cargar(path):
    d = json.load(open(path))
    names = d["info"]["TeamNames"]
    if YO not in names:
        return None
    me = names.index(YO)
    S = d["steps"]
    return dict(ep=d["info"]["EpisodeId"], rival=names[1 - me], me=me, S=S,
                mio=S[-1][me].get("reward") or 0, suyo=S[-1][1 - me].get("reward") or 0)


def vendido(S, idx):
    """Unidades vendidas por el jugador idx (offset +1: la accion del indice t ya se aplico)."""
    c = Counter()
    for t in range(len(S)):
        if t + 1 >= len(S):
            break
        for o in (S[t + 1][idx].get("action") or {}).get("market") or []:
            if isinstance(o, list) and len(o) >= 3 and o[0] == "SELL":
                c[o[1]] += o[2]
    return c


def composicion(S, idx):
    farm = S[-1][0]["observation"]["farms"][idx]
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
    c["quads"] = len(farm.get("unlocked_quadrants", []))
    return c


def main(bot="CAMPEONA_ALBA", top=6):
    rows = [r for r in (cargar(f) for f in sorted(glob.glob(f"replays/{bot}/*.json"))) if r]
    W = [r for r in rows if r["mio"] > r["suyo"]]
    L = [r for r in rows if r["mio"] < r["suyo"]]
    print(f"{bot}: {len(rows)} partidas -> {len(W)}V {len(L)}D "
          f"({100.0*len(W)/max(1,len(rows)):.1f}%)  "
          f"dinero medio: nuestro ${sum(r['mio'] for r in rows)/len(rows):,.0f} | "
          f"rival ${sum(r['suyo'] for r in rows)/len(rows):,.0f}")

    print("\n--- A) ¿en qué día se decide? margen medio por día ---")
    for grupo, nom in ((W, "victorias"), (L, "derrotas")):
        if not grupo:
            continue
        marg = []
        for dia in range(0, 30, 3):
            s = dia * 24
            vals = [r["S"][s][0]["observation"]["farms"][r["me"]]["money"]
                    - r["S"][s][0]["observation"]["farms"][1 - r["me"]]["money"]
                    for r in grupo if s < len(r["S"])]
            marg.append(f"d{dia:02d} {sum(vals)/len(vals):>+8,.0f}")
        print(f"  {nom:10s} " + "  ".join(marg))

    print("\n--- B) unidades vendidas: nosotros vs rival (media) ---")
    print(f"  {'producto':12s} {'V:nuestro':>10} {'V:rival':>9} {'D:nuestro':>10} {'D:rival':>9} {'gap en D':>9}")
    for it in ("WHEAT", "STRAWBERRY", "MELON", "MILK", "WOOL", "FERTILIZER", "EGG", "TOMATO", "CARROT"):
        f = lambda g, i: (sum(vendido(r["S"], i(r))[it] for r in g) / len(g)) if g else 0
        vn, vr = f(W, lambda r: r["me"]), f(W, lambda r: 1 - r["me"])
        dn, dr = f(L, lambda r: r["me"]), f(L, lambda r: 1 - r["me"])
        print(f"  {it:12s} {vn:>10.0f} {vr:>9.0f} {dn:>10.0f} {dr:>9.0f} {dn-dr:>+9.0f}")

    print("\n--- C) composición del rival (media) ---")
    for grupo, nom in ((W, "cuando ganamos"), (L, "cuando perdemos")):
        if not grupo:
            continue
        acc = Counter()
        for r in grupo:
            acc.update(composicion(r["S"], 1 - r["me"]))
        print(f"  {nom:16s} " + "  ".join(f"{k} {acc[k]/len(grupo):.1f}"
              for k in ("COW", "SHEEP", "GOOSE", "STRAWBERRY", "WHEAT", "MELON", "TOMATO", "CARROT", "quads")))
    print("  nuestra          " + "  ".join(f"{k} {sum(composicion(r['S'], r['me'])[k] for r in rows)/len(rows):.1f}"
          for k in ("COW", "SHEEP", "GOOSE", "STRAWBERRY", "WHEAT", "MELON", "TOMATO", "CARROT", "quads")))

    print(f"\n--- D) las {top} derrotas más ajustadas (donde está el Elo) ---")
    for r in sorted(L, key=lambda r: r["suyo"] - r["mio"])[:top]:
        c = composicion(r["S"], 1 - r["me"])
        print(f"  {r['ep']} {r['rival'][:18]:18s} {r['mio']:>8,.0f} vs {r['suyo']:>8,.0f} "
              f"({r['mio']-r['suyo']:>+8,.0f})  rival: " +
              " ".join(f"{k}{c[k]}" for k in ("COW", "SHEEP", "GOOSE", "STRAWBERRY", "WHEAT", "MELON") if c[k]))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--bot", default="CAMPEONA_ALBA")
    ap.add_argument("--top", type=int, default=6)
    main(**vars(ap.parse_args()))
