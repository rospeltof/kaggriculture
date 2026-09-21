"""Selecciona desde piloto terminado y registra tamaño ANTES de confirmar."""
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"docs/evidencia/lider_20260914"


def main():
    path=OUT/"pilot.meta.json"
    pilot=json.loads(path.read_text())
    assert pilot["state"]=="complete" and pilot["completed_episodes"]==1792
    summary=pilot["summary"]
    assert summary["noop"]["changed_actions"]==0 and summary["noop"]["delta"]["mean"]==0
    candidates=[a for a in pilot["arms"] if a not in ("base","noop","_peor")]
    best=sorted(candidates,key=lambda a:(-summary[a]["score"],a))[0]
    result=dict(pilot_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidate=best,
                pilot_score=summary[best]["score"],pilot_delta=summary[best]["delta"]["mean"],
                seed_sd=summary[best]["delta"]["seed_sd"],
                prior_control_delta=summary["_peor"]["delta"]["mean"],
                selection_rule="Máximo W/L/T; empate por nombre; excluidos controles")
    gate=result["pilot_delta"]>=.15 and result["prior_control_delta"]<0
    sd=max(result["seed_sd"],.10)
    calculated=math.ceil(((1.96+.84)*sd/.15)**2)
    n=min(32,max(16,calculated))
    result.update(proceed=gate,raw_sample_size=calculated,n_seeds=n if gate else 0,
                  sample_size_capped=calculated>32,seed_start=215000,seed_end=215000+n-1 if gate else None,
                  expected_episodes=48*n*4*2 if gate else 0,
                  effect_of_interest=.15,approximate_mde80=2.8*sd/math.sqrt(n) if gate else None,
                  promotion_rule="Delta >=15 puntos, IC95 semilla y dos vías >0, control anterior ambos IC95 <0, noop exacto y cero errores")
    target=OUT/"confirmacion_registro.json"
    with target.open("x") as handle:
        handle.write(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps(result,indent=2,ensure_ascii=False))


if __name__=="__main__":
    main()
