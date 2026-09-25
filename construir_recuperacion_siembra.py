"""Recuperación por casilla de siembras perdidas al cavar maleza."""
import hashlib
import json
from pathlib import Path

BASE=Path('submission/main_publico_arshs3_vq.py')
OUT=Path('results/recuperacion_20260925')
LAYER='''
# Own research: remember weed-blocked plant intent by tile, across worker changes.
_RP_PARENT=[v for v in list(globals().values()) if callable(v)][-1]
_RP_STATE={}
_RP_REPORT=dict(intents=0,attempts=0,observed_plants=0,expired=0,no_water=0,no_seed=0)

def recuperacion_agent(observation,configuration=None):
    action=_RP_PARENT(observation,configuration)
    step=int(observation['step']);seat=int(observation['player']);day=step//24
    if step==0:
        _RP_STATE.clear()
        for k in _RP_REPORT:_RP_REPORT[k]=0
    st=_RP_STATE.setdefault(seat,{})
    farm=observation['farms'][seat];tiles=farm['tiles'];priv=observation['private']
    positions=[tuple(farm['farmer'])]+[tuple(p) for p in farm['hands']]
    units=[list(action.get('farmer') or ['PASS'])]+[list(c) for c in action.get('hands',[])]
    raw=_ca_tape(seat,step)
    planned=[raw.get('farmer') or ['PASS']]+list(raw.get('hands') or [])
    for i,(pos,cmd) in enumerate(zip(positions,planned)):
        tile=tiles[pos[1]][pos[0]]
        if (len(cmd)>1 and cmd[0]=='PLANT' and cmd[1] in _RP_CROPS
            and isinstance(tile,dict) and tile.get('kind')=='WEED'
            and i<len(units) and units[i]==['DIG']):
            st[pos]=(cmd[1],day)
            _RP_REPORT['intents']+=1
    reserved={crop:sum(c[:2]==['PLANT',crop] for c in units) for crop in _RP_CROPS}
    changed=False
    for pos,(crop,original_day) in list(st.items()):
        tile=tiles[pos[1]][pos[0]]
        if isinstance(tile,dict) and tile.get('crop'):
            _RP_REPORT['observed_plants']+=int(tile.get('crop')==crop)
            st.pop(pos,None);continue
        if day-original_day>_RP_DELAY or day+_RP_FIRST[crop]>=30:
            _RP_REPORT['expired']+=1;st.pop(pos,None);continue
        if tile is not None:continue
        for i,here in enumerate(positions):
            if here!=pos or i>=len(units) or units[i][0] not in ('WATER','PASS','FERTILIZE'):continue
            if int(priv['seeds'].get(crop,0))<=reserved[crop]:
                _RP_REPORT['no_seed']+=1;break
            # Find another planned WATER before midnight. The planting action
            # preserves this unit's location; routes and movement stay unchanged.
            later_same_turn=any(j>i and p==pos and j<len(units) and units[j]==['WATER'] for j,p in enumerate(positions))
            visits=_ca_visits(observation,action,pos,day*24+23,start=step+1)
            if not later_same_turn and not any(op=='WATER' for t,j,op in visits):
                _RP_REPORT['no_water']+=1;break
            units[i]=['PLANT',crop];reserved[crop]+=1
            _RP_REPORT['attempts']+=1;changed=True;break
    if changed:
        action=dict(action,farmer=units[0],hands=units[1:])
        race=_RACE_STATE.get(seat)
        if race is not None and race.get('step')==step and race.get('prev_action') is not None:
            race['prev_action']=action
    return action
recuperacion_agent.telemetry=_RP_REPORT
'''


if __name__=='__main__':
    raw=BASE.read_bytes()
    assert hashlib.sha256(raw).hexdigest()=='9b463dfb8076b4c63946e1ae4249cd1cfc3cc58b63115cf2bd5b00f96f188976'
    OUT.mkdir(parents=True,exist_ok=True)
    configs={'recover_ongoing':{'crops':['STRAWBERRY','TOMATO'],'delay':2},
             'recover_all':{'crops':['STRAWBERRY','TOMATO','WHEAT','CARROT','MELON'],'delay':2}}
    manifest={}
    for name,c in configs.items():
        p=OUT/(name+'.py')
        if p.exists():raise FileExistsError(p)
        constants=f'\n_RP_CROPS={c["crops"]!r}\n_RP_DELAY={c["delay"]!r}\n_RP_FIRST={{"STRAWBERRY":10,"TOMATO":8,"WHEAT":2,"CARROT":2,"MELON":10}}\n'
        data=raw+constants.encode()+LAYER.encode();compile(data,str(p),'exec');p.write_bytes(data)
        manifest[name]={'path':str(p),'sha256':hashlib.sha256(data).hexdigest(),'config':c}
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(manifest,indent=2))
