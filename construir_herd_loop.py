"""Valor económico previsto para compras COW/SHEEP, con logística heredada."""
import hashlib
import json
from pathlib import Path

BASE=Path('submission/main_publico_arshs3_vq.py')
OUT=Path('results/herd_loop_20260925')
EV='''
_HE_OLD_TARGET=_y_target
_HE_OLD_CONTROLLER=_y_controller
_HE_CONTEXT={}
_HE_REPORT=dict(decisions=0,changed=0,evs=[])

def _y_target(kind,shops,cfg):
    if kind not in ('COW','SHEEP') or 'obs' not in _HE_CONTEXT:
        return _HE_OLD_TARGET(kind,shops,cfg)
    obs=_HE_CONTEXT['obs'];step=int(obs['step'])
    if _HE_CONTEXT.get('step')!=step:
        _HE_CONTEXT['step']=step
        _HE_CONTEXT['ev']={a:_hd2_ev(a,2,obs,{})[0] for a in ('COW','SHEEP')}
    values=_HE_CONTEXT['ev'];other='SHEEP' if kind=='COW' else 'COW'
    change=values[other]-values[kind]>=_HE_GAIN
    _HE_REPORT['decisions']+=1;_HE_REPORT['changed']+=int(change)
    if len(_HE_REPORT['evs'])<20:_HE_REPORT['evs'].append([step,kind,values.copy(),change])
    return other if change else None

def _y_controller(obs,action,state,cfg):
    if int(obs['step'])==0:
        _HE_CONTEXT.clear();_HE_REPORT.update(decisions=0,changed=0,evs=[])
    _HE_CONTEXT['obs']=obs
    try:return _HE_OLD_CONTROLLER(obs,action,state,cfg)
    finally:_HE_CONTEXT.pop('obs',None)
'''


if __name__=='__main__':
    raw=BASE.read_bytes();assert hashlib.sha256(raw).hexdigest()=='9b463dfb8076b4c63946e1ae4249cd1cfc3cc58b63115cf2bd5b00f96f188976'
    OUT.mkdir(parents=True,exist_ok=True);manifest={}
    for name,future,gain in [('herd_future',1.0,None),('herd_ev600',0.0,600),('herd_ev1500',0.0,1500),('herd_ev_future',1.0,600)]:
        p=OUT/(name+'.py')
        if p.exists():raise FileExistsError(p)
        extra='\n# Own research; inherited Apache-2.0 notices retained.\n_HE_PARENT=[v for v in list(globals().values()) if callable(v)][-1]\n'
        extra+=f'_HD2_FUTURE={future!r}\n_HE_GAIN={gain!r}\n'
        if gain is not None:extra+=EV
        extra+='\ndef herd_loop_agent(observation,configuration=None):\n    return _HE_PARENT(observation,configuration)\n'
        data=raw+extra.encode();compile(data,str(p),'exec');p.write_bytes(data)
        manifest[name]={'path':str(p),'sha256':hashlib.sha256(data).hexdigest(),'config':{'expected_future_shop_weight':future,'gain_for_two_animals':gain}}
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(manifest,indent=2))
