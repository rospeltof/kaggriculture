"""Repara PLANT bloqueado por maleza insertando riego sin perder tareas útiles.

Sólo desplaza un turno el sufijo de movimiento/riego de esa unidad; requiere
un último turno redundante que absorba la inserción antes del reset nocturno.
"""
import hashlib
import json
from pathlib import Path

BASE=Path('submission/main_publico_arshs3_vq.py')
OUT=Path('results/recuperacion_turno_20260925')
LAYER='''
_RT_PARENT=[v for v in list(globals().values()) if callable(v)][-1]
_RT_STATE={}
_RT_REPORT=dict(intents=0,planted=0,shifted=0,expired=0,unsafe_suffix=0)

def _rt_command(seat,t,i):
    a=_ca_tape(seat,t)
    commands=[a.get('farmer') or ['PASS']]+list(a.get('hands') or [])
    return list(commands[i]) if i<len(commands) else ['PASS']

def recuperacion_turno_agent(observation,configuration=None):
    action=_RT_PARENT(observation,configuration)
    step=int(observation['step']);seat=int(observation['player']);day=step//24
    if step==0:
        _RT_STATE.clear()
        for k in _RT_REPORT:_RT_REPORT[k]=0
    st=_RT_STATE.setdefault(seat,dict(pending={},delayed={},day=day))
    if st['day']!=day:st['delayed'].clear();st['day']=day
    f=observation['farms'][seat];tiles=f['tiles'];seeds=observation['private']['seeds']
    pos=[tuple(f['farmer'])]+[tuple(p) for p in f['hands']]
    units=[list(action.get('farmer') or ['PASS'])]+[list(c) for c in action.get('hands',[])]
    changed=False
    for i in list(st['delayed']):
        if i<len(units):
            units[i]=_rt_command(seat,step-1,i);changed=True;_RT_REPORT['shifted']+=1
    for i,xy in enumerate(pos):
        if i>=len(units) or i in st['delayed']:continue
        cmd=_rt_command(seat,step,i);tile=tiles[xy[1]][xy[0]]
        if (len(cmd)>1 and cmd[0]=='PLANT' and cmd[1] in _RT_CROPS
            and isinstance(tile,dict) and tile.get('kind')=='WEED' and units[i]==['DIG']):
            st['pending'][xy]=(cmd[1],day);_RT_REPORT['intents']+=1
    reserved={c:sum(u[:2]==['PLANT',c] for u in units) for c in _RT_CROPS}
    for xy,(crop,original_day) in list(st['pending'].items()):
        tile=tiles[xy[1]][xy[0]]
        if isinstance(tile,dict) and tile.get('crop'):
            st['pending'].pop(xy,None);continue
        if day-original_day>_RT_DELAY or day+_RT_FIRST[crop]>=30:
            st['pending'].pop(xy,None);_RT_REPORT['expired']+=1;continue
        if tile is not None or step%24>21:continue
        for i,p in enumerate(pos):
            if p!=xy or i>=len(units) or i in st['delayed'] or units[i]!=['WATER']:continue
            if seeds.get(crop,0)<=reserved[crop]:break
            suffix=[_rt_command(seat,t,i) for t in range(step,day*24+24)]
            permitted=set(_CA_MOVES)|{'WATER','PASS'}
            redundant=(suffix[-1]==['PASS'] or suffix[-2:]==[['WATER'],['WATER']])
            if not redundant or not all(c[0] in permitted for c in suffix) or suffix[0]!=['WATER']:
                _RT_REPORT['unsafe_suffix']+=1;break
            units[i]=['PLANT',crop];reserved[crop]+=1;st['delayed'][i]=True
            st['pending'].pop(xy,None);_RT_REPORT['planted']+=1;changed=True;break
    if changed:
        action=dict(action,farmer=units[0],hands=units[1:])
        race=_RACE_STATE.get(seat)
        if race is not None and race.get('step')==step and race.get('prev_action') is not None:race['prev_action']=action
    return action
recuperacion_turno_agent.telemetry=_RT_REPORT
'''


if __name__=='__main__':
    raw=BASE.read_bytes();assert hashlib.sha256(raw).hexdigest()=='9b463dfb8076b4c63946e1ae4249cd1cfc3cc58b63115cf2bd5b00f96f188976'
    OUT.mkdir(parents=True,exist_ok=True);manifest={}
    for name,crops,delay in [('recover_now',['STRAWBERRY','TOMATO'],0),
                             ('recover_later',['STRAWBERRY','TOMATO','WHEAT','CARROT','MELON'],2)]:
        p=OUT/(name+'.py')
        if p.exists():raise FileExistsError(p)
        constants=f'\n_RT_CROPS={crops!r}\n_RT_DELAY={delay}\n_RT_FIRST={{"STRAWBERRY":10,"TOMATO":8,"WHEAT":2,"CARROT":2,"MELON":10}}\n'
        data=raw+constants.encode()+LAYER.encode();compile(data,str(p),'exec');p.write_bytes(data)
        manifest[name]={'path':str(p),'sha256':hashlib.sha256(data).hexdigest(),'config':{'crops':crops,'max_delay_days':delay}}
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(manifest,indent=2))
