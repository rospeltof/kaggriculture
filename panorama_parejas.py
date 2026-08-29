"""Censo de partidas del ladder: margen, era del bot, y anatomía de cierre.
Uso: ./.venv/bin/python panorama_parejas.py [replays/*.json]
"""
import json, sys, os, glob
from collections import defaultdict

BASE = {"WHEAT":25,"CARROT":35,"TOMATO":60,"STRAWBERRY":120,"MELON":250,
        "EGG":50,"MILK":160,"WOOL":200,"FERTILIZER":100}
ANIM = {"COW":"MILK","SHEEP":"WOOL","GOOSE":"EGG"}

def load(path):
    d = json.load(open(path))
    n = d["info"]["TeamNames"]
    me = 0 if n[0].startswith("Rospel") else 1
    return d, me, n[1-me]

def sobrante(d, t, pl):
    """(shed_base, tiles_base, manos_base) — dinero dejado en la mesa al step t."""
    obs = d["steps"][t][pl]["observation"]
    priv = obs.get("private") or {}
    shed = priv.get("shed") or {}
    sb = sum(v*BASE.get(k,0) for k,v in shed.items() if k in BASE)
    farm = d["steps"][t][0]["observation"]["farms"][pl]
    tv = 0; tot=defaultdict(int)
    for row in farm["tiles"]:
        for c in row:
            if not isinstance(c, dict): continue
            y = c.get("yield_units",0) or 0
            if c.get("kind")=="PLANT": tot[c["crop"]] += y
            elif c.get("animal") in ANIM: tot[ANIM[c["animal"]]] += y
    tv = sum(v*BASE.get(k,0) for k,v in tot.items())
    mv = 0
    for inv in (priv.get("inventories") or []):
        mv += sum(n*BASE.get(k,0) for k,n in (inv or {}).items())
    return sb, tv, mv

def era(d, me):
    """firma de generación: cuadrantes al d20 + ops de apertura."""
    T=len(d["steps"])-1
    q = len(d["steps"][min(20*24,T)][0]["observation"]["farms"][me]["unlocked_quadrants"])
    npass=0; ntot=0
    for t in range(1, min(48, len(d["steps"]))):
        a = d["steps"][t][me].get("action") or {}
        for o in [a.get("farmer") or ["PASS"]] + list(a.get("hands") or []):
            ntot+=1
            if not o or o[0]=="PASS": npass+=1
    return q, round(100*npass/max(1,ntot))

if __name__ == "__main__":
    paths = sys.argv[1:] or sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)),"replays","*.json")))
    rows=[]
    for p in paths:
        try: d, me, opp = load(p)
        except Exception: continue
        T=len(d["steps"])-1
        r=d["rewards"]
        if r[me] is None or r[1-me] is None: continue
        marg = r[me]-r[1-me]
        ms=[s[0]["observation"]["farms"][me]["money"] for s in d["steps"]]
        mo=[s[0]["observation"]["farms"][1-me]["money"] for s in d["steps"]]
        d28 = ms[min(28*24,T)]-mo[min(28*24,T)]
        d29 = ms[min(29*24,T)]-mo[min(29*24,T)]
        d26 = ms[min(26*24,T)]-mo[min(26*24,T)]
        sb,tv,mv = sobrante(d,T,me)
        sb2,tv2,mv2 = sobrante(d,T,1-me)
        q,pas = era(d,me)
        ep=os.path.basename(p).replace('-replay.json','').replace('episode-','')
        rows.append(dict(ep=ep,opp=opp,marg=marg,mine=r[me],theirs=r[1-me],
                         d26=d26,d28=d28,d29=d29,sob=sb+tv+mv,sob_op=sb2+tv2+mv2,
                         q=q,pas=pas,
                         ult_yo=r[me]-ms[min(29*24,T)], ult_op=r[1-me]-mo[min(29*24,T)],
                         dos_yo=r[me]-ms[min(28*24,T)], dos_op=r[1-me]-mo[min(28*24,T)]))
    rows.sort(key=lambda x:x["marg"])
    print(f"{'ep':<10}{'rival':<20}{'margen':>8}{'yo':>9}{'rival':>9}{'d26':>8}{'d28':>8}{'d29':>8}"
          f"{'ult2d_yo':>9}{'ult2d_op':>9}{'sobra':>7}{'sob_op':>7}{'q':>3}")
    for x in rows:
        print(f"{x['ep']:<10}{x['opp'][:19]:<20}{x['marg']:>+8,.0f}{x['mine']:>9,.0f}{x['theirs']:>9,.0f}"
              f"{x['d26']:>+8,.0f}{x['d28']:>+8,.0f}{x['d29']:>+8,.0f}{x['dos_yo']:>9,.0f}{x['dos_op']:>9,.0f}"
              f"{x['sob']:>7,.0f}{x['sob_op']:>7,.0f}{x['q']:>3}")
