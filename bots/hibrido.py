"""Hibrido: cinta del lider hasta `corte` (apertura coordinada que el chasis no
reproduce por piezas) y CAMPEONA_HOZ (adaptativo: precios, tiendas, rival) despues.
Hipotesis (2026-09-22): el valor que separa a Majkel-3075 de su propia cinta esta
en la adaptacion; nuestro planner adapta, la cinta no. warmstart10 (otra cinta,
panel debil) dio +6.25 < cinta pura; nunca se midio vs fuertes ni con 107570947."""
import gzip, json, os
from copy import deepcopy
DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "meta", "tapes")


def make(cinta="top_majkel1337_107570947", corte=240):
    from bots.chassis import make_agent
    from bots.arquetipos import CAMPEONA_HOZ
    T = json.load(gzip.open(os.path.join(DIR, cinta + ".json.gz"), "rt"))
    planner = make_agent(dict(CAMPEONA_HOZ))
    def agent(obs):
        step = int(obs.get("step", obs["day"] * 24 + obs["hour"]))
        if step >= corte:
            return planner(obs)
        return deepcopy(T[min(step, len(T) - 1)])
    return agent
