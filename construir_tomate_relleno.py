"""Cuatro variantes aisladas de ocupación productiva en tierra ya comprada."""
import hashlib
import json
from pathlib import Path

BASE=Path('submission/main_publico_arshs3_vq_top3.py')
LAYER=Path('capa_tomate_relleno.py')
OUT=Path('results/tomate_relleno_v4_20260925')


def build():
    raw=BASE.read_bytes();layer=LAYER.read_bytes()
    assert hashlib.sha256(raw).hexdigest()=='9668e30ad08f79d485bd230a3c660d4cc420b9382e87f9387b6908e3c94a5145'
    OUT.mkdir(parents=True,exist_ok=True);manifest={}
    for day,size in ((16,4),(16,8),(18,4),(18,8)):
        name=f'infill{size}_d{day}';p=OUT/(name+'.py')
        if p.exists():raise FileExistsError(p)
        data=raw+f'\n_IF_START={day}\n_IF_SIZE={size}\n_IF_MARGIN=600\n'.encode()+layer
        compile(data,str(p),'exec');p.write_bytes(data)
        manifest[name]=dict(path=str(p),sha256=hashlib.sha256(data).hexdigest(),start=day,plots=size,margin=600,layer_sha256=hashlib.sha256(layer).hexdigest())
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(manifest,indent=2))


if __name__=='__main__':build()
