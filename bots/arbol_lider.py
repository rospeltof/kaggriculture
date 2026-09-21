"""Arbol de rutas v2 sobre las 30 VICTORIAS de Majkel1337 (sub 56142830).

Generaliza bots/experimentos_lider.py (4 cintas, ramas fijas) a un vecino mas
cercano sobre la SECUENCIA DE TIENDAS observada, que es la unica informacion
estrategica visible: el town esta vacio hasta el paso 72 y las divergencias
anteriores entre cintas son reacciones a la caja (BUY_SEED MELON 2 o no), no
ramas. Nunca consulta semilla ni tiendas futuras.

En cada punto de ramificacion (pasos 72, 144, 216, ...) se queda con las cintas
cuya secuencia de tiendas coincide con la observada hasta ahora; si ninguna
coincide, mantiene la ruta actual. Desempate: mayor dinero final del lider.
"""
import glob, gzip, json, os

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "meta", "tapes")
CLASIF = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      "results", "clasif_MAJKEL_56142830.json")
BRANCH_STEPS = (72, 144, 216, 288)


def cargar_cintas():
    """[(id, dinero, seq_tiendas, acciones)] solo de VICTORIAS."""
    clas = {r["ep"]: r for r in json.load(open(CLASIF))}
    out = []
    for f in sorted(glob.glob(os.path.join(DIR, "top_majkel1337_*.json.gz"))):
        ep = int(os.path.basename(f)[len("top_majkel1337_"):-8])
        r = clas.get(ep)
        if not r or not r["gana"]:
            continue
        seq = [tuple(x) for x in r["shops_seq"]]      # precalculado por el clasificador
        out.append((ep, r["mio"], seq, json.load(gzip.open(f, "rt"))))
    return out


def make(cintas=None):
    cintas = cintas if cintas is not None else cargar_cintas()
    state = {}

    def agent(obs):
        step = int(obs.get("step", obs["day"] * 24 + obs["hour"]))
        if step == 0:
            state["vivas"] = list(cintas)
            state["ruta"] = max(cintas, key=lambda c: c[1])
            state["hist"] = []
        shops = tuple((obs.get("town") or {}).get("unlocked_shops") or [])
        if step in BRANCH_STEPS:
            k = BRANCH_STEPS.index(step)
            state["hist"].append(shops)
            cand = [c for c in state["vivas"] if len(c[2]) > k and c[2][k] == shops]
            if cand:
                state["vivas"] = cand
                state["ruta"] = max(cand, key=lambda c: c[1])
        acts = state["ruta"][3]
        a = acts[min(step, len(acts) - 1)]
        return json.loads(json.dumps(a))
    agent.state = state
    return agent


tree_v2 = make()
