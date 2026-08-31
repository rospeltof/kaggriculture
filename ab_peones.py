"""A/B del NUMERO DE PEONES sobre CAMPEONA_FB.
(1) head-to-head espejado contra la gemela base  -> zona de decision real (nulo 50%)
(2) dinero contra panel fuerte [barnyard, v16]   -> la economia, que es donde perdemos
"""
import argparse, copy, math, os, sys
from multiprocessing import Pool
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import run_episode
from bots.arquetipos import CAMPEONA_FB

def var(name, **kw):
    c = copy.deepcopy(CAMPEONA_FB); c.update(kw); return ("cfg", name, c)

def h2h(variants, base, n, seed0, procs=None):
    jobs, meta = [], []
    for v in variants:
        for s in range(seed0, seed0+n):
            jobs.append((v, base, s, 720)); meta.append((v[1], 0))
            jobs.append((base, v, s, 720)); meta.append((v[1], 1))
    with Pool(procs or 11) as p: res = p.map(run_episode, jobs)
    agg={}
    for (name, side), r in zip(meta, res):
        mine, th = r["money"][side], r["money"][1-side]
        a=agg.setdefault(name, {"w":0,"n":0,"m":[],"o":[]})
        a["n"]+=1; a["w"]+= 1 if mine>th else (0.5 if mine==th else 0)
        a["m"].append(mine); a["o"].append(th)
    return agg

def panel(variants, opps, n, seed0, procs=None):
    jobs, meta = [], []
    for v in variants:
        for o in opps:
            for s in range(seed0, seed0+n):
                jobs.append((v, o, s, 720)); meta.append((v[1], o if isinstance(o,str) else o[1], 0))
                jobs.append((o, v, s, 720)); meta.append((v[1], o if isinstance(o,str) else o[1], 1))
    with Pool(procs or 11) as p: res = p.map(run_episode, jobs)
    agg={}
    for (name, oname, side), r in zip(meta, res):
        mine, th = r["money"][side], r["money"][1-side]
        a=agg.setdefault(name, {"w":0,"n":0,"m":[],"by":{}})
        a["n"]+=1; a["w"]+= 1 if mine>th else (0.5 if mine==th else 0); a["m"].append(mine)
        b=a["by"].setdefault(oname,[0,0,[]]); b[0]+= 1 if mine>th else 0; b[1]+=1; b[2].append(mine)
    return agg

if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("-n",type=int,default=60)
    ap.add_argument("--seed0",type=int,default=4100000); ap.add_argument("--np",type=int,default=30)
    a=ap.parse_args()
    V=[var("cap12_BASE"), var("cap11",hands_cap=11), var("cap10",hands_cap=10),
       var("cap9",hands_cap=9), var("cap8",hands_cap=8), var("cap6",hands_cap=6),
       var("hpq3",hands_per_quadrant=3)]
    BASE=("cfg","gemela",copy.deepcopy(CAMPEONA_FB))
    print(f"=== (1) HEAD-TO-HEAD vs gemela CAMPEONA_FB — {a.n} seeds x2 espejo por variante ===")
    A=h2h(V,BASE,a.n,a.seed0)
    print(f"{'variante':14s} {'win-rate':>9s} {'sigma':>7s} {'dinero':>10s} {'rival':>10s} {'delta$':>9s}")
    for name,d in sorted(A.items(), key=lambda kv:-kv[1]['w']/kv[1]['n']):
        wr=d['w']/d['n']; se=math.sqrt(0.25/d['n']); z=(wr-0.5)/se
        mm=sum(d['m'])/len(d['m']); oo=sum(d['o'])/len(d['o'])
        print(f"{name:14s} {wr:8.1%} {z:+7.2f} {mm:10,.0f} {oo:10,.0f} {mm-oo:+9,.0f}")
    print(f"\n=== (2) PANEL FUERTE (dinero) — {a.np} seeds x2 por par ===")
    OP=[("bots/sparring_barnyard.py",),("bots/sparring_v16.py",)]
    OP=[(o[0],) for o in OP]
    P=panel(V,[o[0] for o in OP],a.np,a.seed0+500000)
    print(f"{'variante':14s} {'dinero medio':>13s} {'win-rate':>9s}   por-oponente")
    for name,d in sorted(P.items(), key=lambda kv:-sum(kv[1]['m'])/len(kv[1]['m'])):
        mm=sum(d['m'])/len(d['m']); sd=math.sqrt(sum((x-mm)**2 for x in d['m'])/len(d['m']))
        bo=" ".join(f"{o.split('/')[-1][:12]}:{v[0]}/{v[1]} ${sum(v[2])/len(v[2]):,.0f}" for o,v in sorted(d['by'].items()))
        print(f"{name:14s} {mm:13,.0f} +-{sd/math.sqrt(d['n']):,.0f} {d['w']/d['n']:8.1%}   {bo}")
