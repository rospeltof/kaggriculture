"""Muestra en qué pasos un rival real (asiento de un replay) se aparta de un agente conocido.

Alimenta al agente candidato con las observaciones de ese asiento (como censo_linajes.py) y
compara su acción con la registrada. Imprime los primeros N pasos distintos.

Uso: diff_fork.py <replay.json> <asiento> <candidato.py> [N]
"""
import json, sys
from kaggle_environments import make
from kaggle_environments.agent import get_last_callable
from kaggle_environments.utils import structify


def norm(a):
    if not isinstance(a, dict):
        return a
    return {"farmer": a.get("farmer") or ["PASS"], "hands": [list(h) for h in (a.get("hands") or [])],
            "market": [list(m) for m in (a.get("market") or []) if m]}


def main(replay, seat, ruta, n=10):
    seat = int(seat); n = int(n)
    d = json.load(open(replay)); steps = d["steps"]
    cfg = structify(make("kaggriculture").configuration)
    fn = get_last_callable(open(ruta).read(), path=ruta)
    vistos = 0
    for t in range(len(steps) - 1):
        obs = dict(steps[t][seat]["observation"]); obs["step"] = steps[t][0]["observation"].get("step", t)
        real = steps[t + 1][seat].get("action")
        if real is None:
            continue
        a = fn(structify(obs), cfg)
        if norm(a) != norm(real):
            ra, ca = norm(real), norm(a)
            partes = [k for k in ("farmer", "hands", "market") if ra[k] != ca[k]]
            print(f"t={t} h{t % 24:02d} difiere en {partes}")
            for k in partes:
                print(f"   real {k}: {json.dumps(ra[k])[:230]}")
                print(f"   cand {k}: {json.dumps(ca[k])[:230]}")
            vistos += 1
            if vistos >= n:
                break


if __name__ == "__main__":
    main(*sys.argv[1:])
