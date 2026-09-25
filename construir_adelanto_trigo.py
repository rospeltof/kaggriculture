"""Freeze the same purchase-timing policy over both submitted parents."""
import hashlib
import json
from pathlib import Path

BASE=Path('submission/main_publico_arshs3_vq.py')
TOP3=Path('submission/main_publico_arshs3_vq_top3.py')
OUT=Path('results/adelanto_trigo_20260925')
EVIDENCE=Path('docs/evidencia/loop_publicos_20260925')


def main():
    parents={'vq':BASE,'top3':TOP3}
    hashes={'vq':'9b463dfb8076b4c63946e1ae4249cd1cfc3cc58b63115cf2bd5b00f96f188976',
            'top3':'9668e30ad08f79d485bd230a3c660d4cc420b9382e87f9387b6908e3c94a5145'}
    layer=Path('capa_adelanto_trigo.py').read_bytes();OUT.mkdir(parents=True,exist_ok=True);manifest={}
    for name,parent in parents.items():
        raw=parent.read_bytes();assert hashlib.sha256(raw).hexdigest()==hashes[name]
        for enabled in (True,False):
            arm=('advance_' if enabled else 'advance_noop_')+name
            path=OUT/(arm+'.py');assert not path.exists()
            data=raw+b'\n'+layer+f'\n_BW_ENABLED={enabled!r}\n'.encode();compile(data,str(path),'exec');path.write_bytes(data)
            manifest[arm]=dict(path=str(path),sha256=hashlib.sha256(data).hexdigest(),config=dict(parent=name,enabled=enabled))
    manifest['ref_top3']=dict(path=str(TOP3),sha256=hashes['top3'],config=dict(control=True))
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    candidates={n:r for n,r in manifest.items() if r['config'].get('enabled')}
    (EVIDENCE/'advance_wheat_variants.json').write_text(json.dumps(candidates,indent=2)+'\n')
    print(json.dumps(manifest,indent=2))


if __name__=='__main__':main()
