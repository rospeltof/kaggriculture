"""Extiende cobertura de productos sobre el top3 confirmado, sin cambiar su padre."""
import hashlib
import json
from pathlib import Path

BASE=Path('submission/main_publico_arshs3_vq_top3.py')
OUT=Path('results/forecast_productos_20260925')
VARIANTS={
    'top3_egg':{'_V92_P_USE':('MILK','WOOL','STRAWBERRY','EGG')},
    'top3_melon':{'_V92_P_USE':('MILK','WOOL','STRAWBERRY','MELON')},
    'top3_egg_melon':{'_V92_P_USE':('MILK','WOOL','STRAWBERRY','EGG','MELON')},
    'top3_fast2':{'_V92_P_K':2,'_V92_P_EVERY':1},
}


def build():
    raw=BASE.read_bytes()
    assert hashlib.sha256(raw).hexdigest()=='9668e30ad08f79d485bd230a3c660d4cc420b9382e87f9387b6908e3c94a5145'
    OUT.mkdir(parents=True,exist_ok=True);manifest={}
    for name,config in VARIANTS.items():
        p=OUT/(name+'.py')
        if p.exists():raise FileExistsError(p)
        extra='\n# Local forecast-coverage research. Apache-2.0 upstream notices retained.\n'
        extra+='_FP_PARENT=[v for v in list(globals().values()) if callable(v)][-1]\n'
        for k,v in config.items():extra+=f'{k}={v!r}\n'
        extra+='\ndef forecast_products_agent(observation,configuration=None):\n    return _FP_PARENT(observation,configuration)\n'
        data=raw+extra.encode();compile(data,str(p),'exec');p.write_bytes(data)
        manifest[name]=dict(path=str(p),sha256=hashlib.sha256(data).hexdigest(),config=config)
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(manifest,indent=2))


if __name__=='__main__':build()
