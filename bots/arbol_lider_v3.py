"""Arbol de rutas v3: ramificacion CONSISTENTE con el prefijo ejecutado.

Defecto de v2 (compare 2026-09-21: cinta +12.1 > tree +9.0 > tree_v2 +4.8): al
cambiar de cinta en el paso 72 entre cintas con prefijos distintos, el estado de
la granja no es el que la cinta nueva asume (semillas, posiciones, dinero).

v3: en cada punto de ramificacion s, solo son candidatas las cintas cuyas
acciones coinciden EXACTAMENTE con la cinta actual en todos los pasos < s (LCP
>= s) y cuya tienda observada en s coincide. Si ninguna cumple, se sigue con la
cinta actual: nunca hay un cambio inconsistente. La cinta inicial es la de mayor
dinero dentro de la familia con mas descendientes a 72 pasos.
"""
import glob, gzip, json, os

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "meta", "tapes")
CLASIF = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      "results", "clasif_MAJKEL_56142830.json")
BRANCH_STEPS = (72, 144, 216, 288)


def _lcp(a, b):
    n = 0
    for x, y in zip(a, b):
        if x != y:
            break
        n += 1
    return n


def cargar():
    clas = {r["ep"]: r for r in json.load(open(CLASIF))}
    cintas = []
    for f in sorted(glob.glob(os.path.join(DIR, "top_majkel1337_*.json.gz"))):
        ep = int(os.path.basename(f)[len("top_majkel1337_"):-8])
        r = clas.get(ep)
        if not r or not r["gana"]:
            continue
        acts = json.load(gzip.open(f, "rt"))
        key = [json.dumps(a, sort_keys=True) for a in acts]
        cintas.append(dict(ep=ep, money=r["mio"], seq=[tuple(x) for x in r["shops_seq"]], acts=acts, key=key))
    # LCP entre todas
    n = len(cintas)
    lcp = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            lcp[i][j] = lcp[j][i] = _lcp(cintas[i]["key"], cintas[j]["key"])
    return cintas, lcp


def make(cargado=None):
    cintas, lcp = cargado if cargado else cargar()
    n = len(cintas)
    # cinta inicial: mayor numero de companeras con LCP >= 72; desempate por dinero
    fam = [sum(1 for j in range(n) if j != i and lcp[i][j] >= 72) for i in range(n)]
    start = max(range(n), key=lambda i: (fam[i], cintas[i]["money"]))
    state = {}

    def agent(obs):
        step = int(obs.get("step", obs["day"] * 24 + obs["hour"]))
        if step == 0 or "cur" not in state:
            state["cur"] = start; state["hist"] = []; state["cambios"] = 0
        shops = tuple((obs.get("town") or {}).get("unlocked_shops") or [])
        if step in BRANCH_STEPS:
            k = BRANCH_STEPS.index(step); cur = state["cur"]
            state["hist"].append(shops)
            cand = [j for j in range(n)
                    if (j == cur or lcp[cur][j] >= step)          # prefijo identico hasta aqui
                    and len(cintas[j]["seq"]) > k and cintas[j]["seq"][k] == shops]
            if cand:
                mejor = max(cand, key=lambda j: cintas[j]["money"])
                if mejor != cur:
                    state["cambios"] += 1
                state["cur"] = mejor
        acts = cintas[state["cur"]]["acts"]
        return json.loads(json.dumps(acts[min(step, len(acts) - 1)]))
    agent.state = state
    agent.info = dict(start=cintas[start]["ep"], familia72=fam[start], n=n)
    return agent


tree_v3 = make()
