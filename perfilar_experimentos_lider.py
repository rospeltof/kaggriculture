"""Sonda diagnóstica del cambio de arquitectura; no decide fuerza competitiva."""
from collections import Counter
import json
from pathlib import Path
from kaggle_environments import make
from evaluar_lider import materialize
from investigar_lider import composition


def profile(arm):
    actions=[]
    agent=materialize(arm)
    def traced(obs):
        action=agent(obs)
        actions.append(json.loads(json.dumps(action)))
        return action
    env=make("kaggriculture",configuration={"seed":213000,"episodeSteps":720},debug=False)
    env.run([traced,materialize("sepopp_107710951")])
    assert [s.status for s in env.steps[-1]]==["DONE","DONE"]
    days=[]
    for day in range(30):
        obs=env.steps[day*24][0].observation
        ops=Counter(op[0] for a in actions[day*24:(day+1)*24] for op in [a["farmer"]]+a["hands"] if op)
        farm=obs["farms"][0]
        days.append(dict(day=day,money=farm["money"],composition=composition(farm),ops=dict(ops),
                         field=farm["tiles"],shed=obs["private"]["shed"]))
    return dict(arm=arm,seed=213000,seat=0,opponent="sepopp_107710951",
                rewards=[s.reward for s in env.steps[-1]],days=days)


if __name__=="__main__":
    output=Path(__file__).resolve().parent/"docs/evidencia/lider_20260914/perfiles_sonda.json"
    if output.exists():
        raise SystemExit("La sonda ya existe; no repetir ni sobrescribir")
    rows=[profile(a) for a in ("base","tree","tree_liquid","warmstart10")]
    output.write_text(json.dumps(rows,indent=2)+"\n")
    for r in rows:
        print(r["arm"],r["rewards"],"d15",r["days"][15]["composition"],flush=True)
