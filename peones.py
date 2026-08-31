"""Economia del peon: turnos-unidad por indice, trabajo efectivo, marginal por rango.

WORK = accion no-movimiento que el motor ACEPTA (usa el clasificador de ocio.py).
MOVE = movimiento valido.  PASS = ocio explicito.  NOOP = accion ignorada.
"""
import json, sys, os
from collections import defaultdict, Counter
sys.path.insert(0, "/Users/rospel/Desktop/kaggriculture")
from ocio import classify, MOVES

FIB = [1,1,2,3,5,8,13,21,34,55,89,144,233,377]
def salario(n):  # costo de tener n peones un dia entero
    return sum(FIB[:n])

def load(path):
    d = json.load(open(path))
    n = d["info"]["TeamNames"]
    me = 0 if n[0].startswith("Rospel") else 1
    return d, me, n[1-me]

def scan(d, p):
    """Devuelve rows: (day,hour,unit_idx,label) label in WORK/MOVE/PASS/NOOP:*"""
    S = d["steps"]; rows=[]
    for t in range(1, len(S)):
        o = S[t-1][p]["observation"]
        if "farms" not in o: o = S[t-1][0]["observation"]
        act = S[t][p].get("action") or {}
        farm = o["farms"][p]; priv = o.get("private", {})
        tiles = farm["tiles"]; shed = dict(priv.get("shed",{}) or {}); seeds=dict(priv.get("seeds",{}) or {})
        invs = list(priv.get("inventories",[{}]))
        pos_list = [tuple(farm["farmer"])] + [tuple(h) for h in farm["hands"]]
        ops = [act.get("farmer")] + list(act.get("hands") or [])
        day, hour = o["day"], o["hour"]
        for i,pos in enumerate(pos_list):
            op = ops[i] if i < len(ops) else None
            inv = dict(invs[i]) if i < len(invs) else {}
            lab = classify(op, pos, tiles, inv, shed, seeds, day)
            if lab is None:
                lab = "MOVE" if (op and op[0] in MOVES) else "WORK"
            rows.append((day, hour, i, lab, op[0] if op else None))
    return rows

def main(paths, player="me"):
    per_idx = defaultdict(Counter)          # idx -> Counter(labels)
    rank_work = defaultdict(list)           # rango (1=mejor peon del dia) -> lista work/dia
    hands_by_day = defaultdict(list)
    day_hands_work = defaultdict(list)      # (nhands) -> [work total equipo]
    farmer_work = []
    tot_games=0; salario_total=[]
    marg_rank_pass = defaultdict(list)
    for path in paths:
        d, me, opp = load(path)
        p = me if player=="me" else 1-me
        rows = scan(d, p)
        tot_games+=1
        # por dia: hands presentes y trabajo por hand
        work = defaultdict(lambda: defaultdict(Counter))
        for day,hour,i,lab,op in rows:
            work[day][i][lab]+=1
            per_idx[i][lab]+=1
        sal=0
        for day, units in sorted(work.items()):
            nh = max(units.keys())    # indice maximo = numero de peones
            hands_by_day[day].append(nh)
            sal += salario(nh)
            tw = sum(c["WORK"] for c in units.values())
            day_hands_work[nh].append(tw)
            farmer_work.append(units[0]["WORK"])
            hs = sorted(((c["WORK"], c["PASS"], c["MOVE"]) for k,c in units.items() if k>0), reverse=True)
            for r,(w,ps,mv) in enumerate(hs, start=1):
                rank_work[r].append(w)
                marg_rank_pass[r].append(ps)
        salario_total.append(sal)
    print(f"### {player}  ({tot_games} partidas)")
    print(f"salario total medio por partida: ${sum(salario_total)/max(1,len(salario_total)):,.0f}")
    print("\n-- por INDICE de unidad (0=granjero) --")
    print(f"{'idx':>4} {'turnos':>8} {'WORK':>7} {'MOVE':>7} {'PASS':>7} {'%PASS':>7} {'%WORK':>7}")
    for i in sorted(per_idx):
        c=per_idx[i]; tot=sum(c.values())
        if tot<50: continue
        print(f"{i:>4} {tot:>8} {c['WORK']:>7} {c['MOVE']:>7} {c['PASS']:>7} {100*c['PASS']/tot:>6.1f}% {100*c['WORK']/tot:>6.1f}%")
    print("\n-- MARGINAL: peones ordenados por trabajo DENTRO de cada dia --")
    print(f"{'rango':>6} {'dias-peon':>10} {'WORK/dia':>9} {'PASS/dia':>9}")
    for r in sorted(rank_work):
        v=rank_work[r]
        if len(v)<20: continue
        print(f"{r:>6} {len(v):>10} {sum(v)/len(v):>9.1f} {sum(marg_rank_pass[r])/len(marg_rank_pass[r]):>9.1f}")
    print(f"\n granjero WORK/dia: {sum(farmer_work)/len(farmer_work):.1f}")
    print("\n-- trabajo total del equipo por numero de peones ese dia --")
    for nh in sorted(day_hands_work):
        v=day_hands_work[nh]
        if len(v)<10: continue
        print(f"  {nh:>2} peones: {len(v):>4} dias-partida, WORK equipo/dia = {sum(v)/len(v):>6.1f}  ({sum(v)/len(v)/(nh+1):.1f} por unidad)")
    print("\n-- peones por dia (media) --")
    print("  " + " ".join(f"d{k}:{sum(v)/len(v):.1f}" for k,v in sorted(hands_by_day.items())))

if __name__ == "__main__":
    who = sys.argv[1]
    main(sys.argv[2:], who)
