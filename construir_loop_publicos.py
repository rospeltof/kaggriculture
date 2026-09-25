"""Construye variantes aisladas sobre VQ, sin sobrescribir evidencia existente."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = ROOT / 'submission/main_publico_arshs3_vq.py'
EXPECTED = '9b463dfb8076b4c63946e1ae4249cd1cfc3cc58b63115cf2bd5b00f96f188976'
OUT = ROOT / 'results/loop_publicos_20260925'
VARIANTS = {
    'crop40': {'crop_blend': .4},
    'crop80': {'crop_blend': .8},
    'crop_end26': {'_CA_TO': 26, '_CA_BUFFER': 6},
    'crop_edge0': {'_CA_MARGIN': 0.0},
    'pred_top3': {'_V92_P_TOP': 3},
    'pred_h96': {'_V92_P_H': 96},
    'pred_fast2': {'_V92_P_K': 2, '_V92_P_EVERY': 1},
    'pred_window6': {'_HP_WINDOW': 6},
}

# Adapted from haodou092/kaggriculture-harvest-ledger, Apache-2.0,
# raw source SHA 1dfd463070024f85879d642fc294e1848ccfab00aad3f3980a04b0a8eca37fdd.
# Only the valuation of short crops changes. Existing herd safeguards remain.
PRICES = '''
def _loop_crop_prices(obs):
    step=int(obs['step']);day=step//24
    prices=obs['market']['prices']
    if day<6 or day>26:return int(prices['CARROT']),int(prices['WHEAT'])
    out={};shops=obs['town']['unlocked_shops']
    for item in ('CARROT','WHEAT'):
        demand=1+_hd2_daily_shop_demand(item,shops)
        incoming=0.0
        for farm in obs['farms']:
            for row in farm['tiles']:
                for tile in row:
                    if isinstance(tile,dict) and tile.get('crop')==item:
                        age=day-int(tile['planted_day'])
                        if age>=0 and age+3>=2:
                            incoming+=max(float(tile.get('yield_units',0)),3.0)
        inv=float(obs['market']['inventory'][item])+incoming+6-3*demand
        future=float(_r37_market_price(item,int(round(inv)),obs['market'].get('params')))
        now=float(prices[item]);future=min(future,now*1.5)
        out[item]=int(round((1-_LOOP_BLEND)*now+_LOOP_BLEND*future))
    return out['CARROT'],out['WHEAT']
'''


def build():
    raw=BASE.read_bytes()
    assert hashlib.sha256(raw).hexdigest()==EXPECTED
    OUT.mkdir(parents=True,exist_ok=True)
    manifest={}
    for name,config in VARIANTS.items():
        dest=OUT/(name+'.py')
        if dest.exists():raise FileExistsError(dest)
        src=raw.decode()
        extra='\n# Local research 2026-09-25; inherited Apache-2.0 notices retained.\n'
        extra+='_LOOP_PARENT = [v for v in list(globals().values()) if callable(v)][-1]\n'
        if 'crop_blend' in config:
            old='p_c, p_w = int(prices.get("CARROT", 0)), int(prices.get("WHEAT", 0))'
            assert src.count(old)==1
            src=src.replace(old,'p_c, p_w = _loop_crop_prices(observation)')
            extra+='# Crop quote adapted from haodou092/Harvest Ledger, Apache-2.0.\n'
            extra+=f'_LOOP_BLEND = {config["crop_blend"]!r}\n'+PRICES
        else:
            for key,value in config.items():extra+=f'{key} = {value!r}\n'
        extra+='''
def loop_research_agent(observation,configuration=None):
    return _LOOP_PARENT(observation,configuration)
'''
        data=(src+extra).encode()
        compile(data,str(dest),'exec')
        dest.write_bytes(data)
        manifest[name]={'path':str(dest.relative_to(ROOT)), 'sha256':hashlib.sha256(data).hexdigest(), 'config':config}
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(manifest,indent=2))


if __name__=='__main__':build()
