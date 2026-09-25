"""Variantes del predictor existente: gate por aciertos pasados y ablación PREDICT."""
import argparse
import hashlib
from pathlib import Path

GATE='''
# Research 2026-09-25. Mantener atribuciones Apache-2.0 de la base.
# Aplicar al horizonte inmediato la misma evidencia exigida por forecast4.
_FG_PARENT = [v for v in list(globals().values()) if callable(v)][-1]
_FG_REPORT = dict(considered=0,rejected=0,accepted=0)

def _hp_quantity(ev,item,step,seen):
    immediate=sum(ev.get((step+d,item),0) for d in (1,2))
    extended=sum(ev.get((step+d,item),0) for d in range(1,_HP_WINDOW+1))
    if max(immediate,extended)<_V92_P_K:return immediate
    prior=[(t,i) for (t,i),q in ev.items() if step-240<=t<step-1 and i==item and q>=2]
    hits=sum(any((t+d,i) in seen for d in (-1,0,1)) for t,i in prior)
    _FG_REPORT['considered']+=1
    if hits>=3 and hits>=.7*len(prior):
        _FG_REPORT['accepted']+=1
        return immediate if immediate>=_V92_P_K else extended
    _FG_REPORT['rejected']+=1
    return 0

def forecast_gate_agent(observation,configuration=None):
    if int(observation['step'])==0:
        for k in _FG_REPORT:_FG_REPORT[k]=0
    return _FG_PARENT(observation,configuration)
forecast_gate_agent.telemetry=_FG_REPORT
'''

OFF='''
# Research 2026-09-25: ablación de esta capa; conserva otros predictores y ventas.
_FO_PARENT = [v for v in list(globals().values()) if callable(v)][-1]
def _v92_predict(obs,action,state):
    _v92_p_update(obs,state)
    return action
def forecast_off_agent(observation,configuration=None):
    return _FO_PARENT(observation,configuration)
'''

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('mode',choices=('gate','off'));ap.add_argument('output')
    a=ap.parse_args();out=Path(a.output)
    if out.exists():raise FileExistsError(out)
    base=Path('submission/main_publico_arshs3_vq.py').read_bytes()
    assert hashlib.sha256(base).hexdigest()=='9b463dfb8076b4c63946e1ae4249cd1cfc3cc58b63115cf2bd5b00f96f188976'
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_bytes(base+(GATE if a.mode=='gate' else OFF).encode())
    print(out,hashlib.sha256(out.read_bytes()).hexdigest())
