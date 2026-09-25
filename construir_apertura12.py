"""Freeze one opening quantity on both references and exact quantity8 noops."""
import hashlib
import json
from pathlib import Path

OUT=Path('results/apertura12_20260925')
EVIDENCE=Path('docs/evidencia/loop_publicos_20260925')


def main():
    panel=json.loads((EVIDENCE/'close_panel_manifest.json').read_text());layer=Path('capa_apertura12.py').read_bytes()
    OUT.mkdir(parents=True,exist_ok=True);manifest={}
    for parent,label in [('base','vq'),('top3','top3')]:
        spec=panel['controls'][parent];raw=Path(spec['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==spec['sha256']
        for enabled,q in [(True,12),(False,8)]:
            name=('open12_' if enabled else 'open_noop_')+label;path=OUT/(name+'.py');assert not path.exists()
            tail=f'\n_OPN_Q={q}\nV9_OPENING_STEP0=(("BUY_PRODUCT","WHEAT",{q}),("SELL","WHEAT",{q-5}))\n'.encode()
            data=raw+b'\n'+layer+tail;compile(data,str(path),'exec');path.write_bytes(data)
            manifest[name]=dict(path=str(path),sha256=hashlib.sha256(data).hexdigest(),config=dict(quantity=q,enabled=enabled),behavior_reference=parent)
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (EVIDENCE/'opening12_variants.json').write_text(json.dumps({n:r for n,r in manifest.items() if r['config']['enabled']},indent=2)+'\n')
    print(json.dumps(manifest,indent=2))


if __name__=='__main__':main()
