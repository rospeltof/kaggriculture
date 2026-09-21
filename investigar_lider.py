"""Extrae y audita los ocho replays aportados el 2026-09-14.

Acciones grabadas en estado t+1 se ejecutan desde t. La validación reproduce
AMBAS cintas con la semilla original y compara estados relevantes en cada turno.
El ledger observa commits efectivos del motor; nunca estima ventas desde órdenes.
"""
import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import importlib
import json
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(__file__).resolve().parent
IDS = (107673304, 107674284, 107674293, 107675268, 107685970, 107692988, 107696961, 107710951)
OUT = ROOT / "docs/evidencia/lider_20260914"
TAPES = ROOT / "bots/meta/tapes"
LEADER = "Majkel1337"


def packed(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()


def digest(obj):
    return hashlib.sha256(packed(obj)).hexdigest()


def compact_state(step):
    obs = step[0]["observation"]
    return {"day": obs["day"], "hour": obs["hour"], "farms": obs["farms"],
            "inventory": obs["market"]["inventory"], "prices": obs["market"]["prices"],
            "town": obs["town"], "private": [s["observation"]["private"] for s in step]}


def composition(farm):
    counts = Counter()
    for row in farm["tiles"]:
        for tile in row:
            if isinstance(tile, dict):
                counts[tile.get("crop") or tile.get("animal") or tile["kind"]] += 1
    return dict(counts)


def extract(source_dir):
    OUT.mkdir(parents=True, exist_ok=True)
    rows, trajectories = [], {}
    for episode in IDS:
        path = source_dir / f"{episode}.json"
        data = path.read_bytes()
        replay = json.loads(data)
        assert replay["module_version"] == "1.32.7" and len(replay["steps"]) == 720
        assert replay["statuses"] == ["DONE", "DONE"]
        names = replay["info"]["TeamNames"]
        seat = names.index(LEADER)
        row = dict(episode=episode, source=str(path), source_sha256=hashlib.sha256(data).hexdigest(),
                   seed=replay["info"]["seed"], teams=names, leader_seat=seat,
                   rewards=replay["rewards"], module_version=replay["module_version"],
                   opponent_elo=None, tapes=[], player_summaries=[])
        for player in (0, 1):
            trace = []
            for state in replay["steps"][1:]:
                a = state[player].get("action") or {}
                trace.append(dict(farmer=a.get("farmer") or ["PASS"],
                                  hands=a.get("hands") or [], market=a.get("market") or []))
            trace.append(dict(farmer=["PASS"], hands=[], market=[]))
            name = f"maj_{episode}" if player == seat else f"sepopp_{episode}"
            tape_path = TAPES / f"{name}.json.gz"
            tape_bytes = gzip.compress(packed(trace), mtime=0)
            if tape_path.exists():
                assert tape_path.read_bytes() == tape_bytes, f"No sobrescribir {name}"
            else:
                tape_path.write_bytes(tape_bytes)
            row["tapes"].append(dict(name=name, sha256=hashlib.sha256(tape_bytes).hexdigest()))
            ops, hires, plants, land = Counter(), [], [], []
            for t, action in enumerate(trace[:-1]):
                before = replay["steps"][t][0]["observation"]["farms"][player]
                after = replay["steps"][t+1][0]["observation"]["farms"][player]
                ops.update(a[0] for a in [action["farmer"]] + action["hands"] if a)
                if len(after["unlocked_quadrants"]) > len(before["unlocked_quadrants"]):
                    land.append(dict(step=t, quadrants=len(after["unlocked_quadrants"])))
                # Count hire commits from public hire count; h23 refresh resets it.
                if t % 24 != 23 and after["hires_today"] > before["hires_today"]:
                    hires.append(dict(step=t, count=after["hires_today"]-before["hires_today"]))
                for y in range(10):
                    for x in range(10):
                        a,b = before["tiles"][y][x], after["tiles"][y][x]
                        if isinstance(b, dict) and b.get("kind") == "PLANT":
                            old = (a.get("crop"), a.get("planted_day")) if isinstance(a, dict) else None
                            if old != (b["crop"], b["planted_day"]):
                                plants.append(dict(step=t, x=x, y=y, crop=b["crop"], day=b["planted_day"]))
            snapshots = {}
            for day in (0,1,2,3,5,8,10,12,15,20,25,29):
                obs = replay["steps"][day*24][player]["observation"]
                farm = obs["farms"][player]
                snapshots[str(day)] = dict(money=farm["money"], composition=composition(farm),
                                          prices=obs["market"]["prices"], town=obs["town"])
            row["player_summaries"].append(dict(ops=dict(ops), land=land, hires=hires,
                plants_visible=plants, snapshots=snapshots, action_hash=digest(trace), opening_hash=digest(trace[:120])))
            if player == seat:
                trajectories[episode] = trace
        rows.append(row)
    comparison = []
    for i,a in enumerate(IDS):
        for b in IDS[i+1:]:
            ta,tb = trajectories[a],trajectories[b]
            diff = [t for t in range(719) if ta[t] != tb[t]]
            units = sum((x["farmer"],x["hands"]) != (y["farmer"],y["hands"]) for x,y in zip(ta,tb))
            market = sum(x["market"] != y["market"] for x,y in zip(ta,tb))
            comparison.append(dict(a=a,b=b,first_divergence=diff[0] if diff else None,
                                   different_turns=len(diff), different_unit_turns=units, different_market_turns=market))
    report = dict(schema=1, date="2026-09-14", leader_identity=LEADER,
                  caveats=["Elo y ranking no figuran en estos archivos.",
                           "Ocho victorias seleccionadas por el usuario, no muestra aleatoria del ladder.",
                           "PLANT contado por transición visible: puede omitir muerte en el mismo turno."],
                  episodes=rows, pairwise= comparison)
    (OUT/"replays.json").write_text(json.dumps(report, indent=2, ensure_ascii=False)+"\n")
    return report


def validate_one(row):
    from kaggle_environments import make
    from bots.meta.tape import make as make_tape
    engine = importlib.import_module("kaggle_environments.envs.kaggriculture.kaggriculture")
    replay = json.loads(Path(row["source"]).read_text())
    ctx, ledger = {}, []
    originals = {n:getattr(engine,n) for n in ("_process_market","_commit_unit","_do_hire","_do_buy_land")}

    def market(state, env):
        obs = state[0].observation
        ctx.update(step=obs.day*24+obs.hour, farms=obs.farms)
        return originals["_process_market"](state,env)

    def record(op,item,value,farm):
        player = next(i for i,f in enumerate(ctx["farms"]) if f is farm)
        ledger.append(dict(step=ctx["step"],player=player,op=op,item=item,value=value))

    def commit(op,item,price,farm,private,market,shed_capacity=100):
        ok = originals["_commit_unit"](op,item,price,farm,private,market,shed_capacity)
        if ok:
            record(op,item,price if op=="SELL" else -price,farm)
        return ok

    def atomic(name, op):
        def call(farm,*args,**kwargs):
            before=farm["money"]
            result=originals[name](farm,*args,**kwargs)
            if farm["money"]!=before:
                record(op,None,farm["money"]-before,farm)
            return result
        return call

    engine._process_market=market
    engine._commit_unit=commit
    engine._do_hire=atomic("_do_hire","HIRE")
    engine._do_buy_land=atomic("_do_buy_land","BUY_LAND")
    try:
        config=dict(replay["configuration"],seed=row["seed"])
        env=make("kaggriculture",configuration=config,debug=False)
        env.run([make_tape(t["name"]) for t in row["tapes"]])
    finally:
        for name,func in originals.items():
            setattr(engine,name,func)
    differences=[t for t,(a,b) in enumerate(zip(replay["steps"],env.steps)) if compact_state(a)!=compact_state(b)]
    assert len(env.steps)==720 and not differences, (row["episode"], differences[:5])
    assert [s.reward for s in env.steps[-1]]==row["rewards"]
    assert [s.status for s in env.steps[-1]]==["DONE","DONE"]
    cashflows=[]
    for p in (0,1):
        totals=defaultdict(lambda:dict(units=0,cash=0))
        for e in ledger:
            if e["player"]==p:
                r=totals[f"{e['op']}:{e['item'] or ''}"]
                r["units"]+=1;r["cash"]+=e["value"]
        assert sum(r["cash"] for r in totals.values())+3000==row["rewards"][p]
        cashflows.append(dict(totals))
    path=OUT/f"ledger_{row['episode']}.jsonl.gz"
    path.write_bytes(gzip.compress(b"\n".join(packed(e) for e in ledger)+b"\n",mtime=0))
    return dict(episode=row["episode"],exact_states=720, rewards=row["rewards"],cashflows=cashflows,
                ledger=path.name,ledger_sha256=hashlib.sha256(path.read_bytes()).hexdigest())


if __name__=="__main__":
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source-dir",type=Path,default=Path("/Users/rospel/Downloads"))
    ap.add_argument("--validate",action="store_true")
    ap.add_argument("--workers",type=int,default=4)
    args=ap.parse_args()
    data=extract(args.source_dir)
    for row in data["episodes"]:
        p=row["leader_seat"];s=row["player_summaries"][p]
        print(row["episode"], row["teams"][1-p], row["rewards"], "opening", s["opening_hash"][:12],
              "land",s["land"], "d15",s["snapshots"]["15"]["composition"],flush=True)
    if args.validate:
        with Pool(args.workers) as pool:
            validation=list(pool.imap(validate_one,data["episodes"]))
        (OUT/"validacion.json").write_text(json.dumps(validation,indent=2,ensure_ascii=False)+"\n")
        print("Exactitud: ocho episodios × 720 estados; cashflows conciliados con dinero final.",flush=True)
