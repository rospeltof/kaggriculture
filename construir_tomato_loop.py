"""Experimentos del umbral y modelo de la inversión tardía en tomates."""
import hashlib
import json
from pathlib import Path

BASE=Path('submission/main_publico_arshs3_vq.py')
OUT=Path('results/tomato_loop_20260925')
FINITE='''
# Own variant of the inherited shiiin9 tomato projection (Apache-2.0).
# A visible plant produces only during its remaining biological lifespan;
# future rival replanting is not assumed without observing it.
def _cxtb_their_supply(obs,upto):
    supply={};day=int(obs['step'])//24
    for row in obs['farms'][1-int(obs['player'])]['tiles']:
        for tile in row:
            if not isinstance(tile,dict) or tile.get('crop')!='TOMATO':continue
            planted=int(tile['planted_day'])
            held=max(0,int(tile.get('yield_units',0)))
            supply[day]=supply.get(day,0)+held
            for d in range(max(day+1,planted+8),min(upto,planted+11)+1):
                rate=2 if tile.get('fertilized_until_day',-1)>=d else 1
                supply[d]=supply.get(d,0)+rate
    return supply

def _cxtb_expected_revenue(obs):
    inventory=float(obs['market']['inventory']['TOMATO']);day=int(obs['step'])//24
    shops=float(sum(s in ('PIZZA_SHOP','FARMERS_MARKET') for s in obs['town']['unlocked_shops']))
    unlocked=len(obs['town']['unlocked_shops']);pending={}
    for d in range(day+1,30):
        if d%3==0 and unlocked<8:pending[d]=.25;unlocked+=1
    theirs=_cxtb_their_supply(obs,29);revenue=0.0
    for d in range(day,30):
        shops+=pending.get(d,0)
        inventory-=1+6*shops-_CXTB_DRAIN_SLACK
        inventory+=theirs.get(d,0)
        if d in _CXTB_HARVEST_DAYS:
            for _ in range(_CXTB_OUR_UNITS):
                revenue+=_r37_market_price('TOMATO',int(round(inventory)))
                inventory+=1
    return revenue
'''


if __name__=='__main__':
    raw=BASE.read_bytes();assert hashlib.sha256(raw).hexdigest()=='9b463dfb8076b4c63946e1ae4249cd1cfc3cc58b63115cf2bd5b00f96f188976'
    OUT.mkdir(parents=True,exist_ok=True);manifest={}
    for name,threshold,finite in [('tomato6000',6000,False),('tomato12000',12000,False),('tomato_finite',9000,True)]:
        p=OUT/(name+'.py')
        if p.exists():raise FileExistsError(p)
        extra='\n# Local research 2026-09-25; inherited Apache-2.0 attribution retained.\n_TM_PARENT=[v for v in list(globals().values()) if callable(v)][-1]\n'
        extra+=f'_CXTB_MIN_REVENUE={threshold}\n'
        if finite:extra+=FINITE
        extra+='\ndef tomato_loop_agent(observation,configuration=None):\n    return _TM_PARENT(observation,configuration)\n'
        data=raw+extra.encode();compile(data,str(p),'exec');p.write_bytes(data)
        manifest[name]={'path':str(p),'sha256':hashlib.sha256(data).hexdigest(),'config':{'revenue_threshold':threshold,'finite_visible_supply':finite}}
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(manifest,indent=2))
