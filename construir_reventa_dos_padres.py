"""Loop29: unchanged town layer on VQ; reuse exact top3 submissions from loop20."""
import hashlib
import json
from pathlib import Path

OUT=Path('results/reventa_dos_padres_20260925')
EVIDENCE=Path('docs/evidencia/loop_publicos_20260925')


def main():
    panel=json.loads((EVIDENCE/'close_panel_manifest.json').read_text())
    old=json.loads(Path('results/reventa_town_20260925/manifest.json').read_text())
    layer=Path('capa_reventa_town.py').read_bytes()
    top3=Path(panel['controls']['top3']['path']).read_bytes()
    raw=Path(panel['controls']['base']['path']).read_bytes()
    assert hashlib.sha256(raw).hexdigest()==panel['controls']['base']['sha256']
    assert hashlib.sha256(top3).hexdigest()==panel['controls']['top3']['sha256']
    OUT.mkdir(parents=True,exist_ok=True);manifest={}
    for name,q,enabled,parent in [('town20_vq',20,True,'base'),('town50_vq',50,True,'base'),('town_noop_vq',20,False,'base'),('town20_top3',20,True,'top3'),('town50_top3',50,True,'top3'),('town_noop_top3',20,False,'top3')]:
        tail=f'\n_TR_MAX_Q={q!r}\n_TR_ENABLED={enabled!r}\n'.encode()
        data=(raw if parent=='base' else top3)+b'\n'+layer+tail
        if parent=='base':
            path=OUT/(name+'.py');assert not path.exists()
            compile(data,str(path),'exec');path.write_bytes(data)
        else:
            spec=old[f'town{q}' if enabled else 'town_noop'];path=Path(spec['path'])
            assert path.read_bytes()==data and hashlib.sha256(data).hexdigest()==spec['sha256']
        manifest[name]=dict(path=str(path),sha256=hashlib.sha256(data).hexdigest(),config=dict(max_quantity=q,enabled=enabled),behavior_reference=parent)
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (EVIDENCE/'town_factorial_variants.json').write_text(json.dumps({n:r for n,r in manifest.items() if r['config']['enabled']},indent=2)+'\n')
    print(json.dumps(manifest,indent=2))


if __name__=='__main__':main()
