"""Freeze cap-aware marginal feed values, preserving all other native rules."""
import hashlib
import json
from pathlib import Path

BASE = Path('submission/main_publico_arshs3_vq_top3.py')
OUT = Path('results/bonus_limitado_20260925')
EVIDENCE = Path('docs/evidencia/loop_publicos_20260925')


def main():
    raw=BASE.read_bytes()
    assert hashlib.sha256(raw).hexdigest()=='9668e30ad08f79d485bd230a3c660d4cc420b9382e87f9387b6908e3c94a5145'
    layer=Path('capa_bonus_limitado.py').read_bytes()
    OUT.mkdir(parents=True,exist_ok=True)
    manifest={}
    for name,mode in [('cap_first','first'),('cap_full','full'),('cap_noop','noop')]:
        path=OUT/(name+'.py')
        if path.exists():raise FileExistsError(path)
        data=raw+f'\n_BC_MODE={mode!r}\n'.encode()+layer
        compile(data,str(path),'exec');path.write_bytes(data)
        manifest[name]=dict(path=str(path),sha256=hashlib.sha256(data).hexdigest(),mode=mode,
                            layer_sha256=hashlib.sha256(layer).hexdigest())
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (EVIDENCE/'capped_bonus_variants.json').write_text(json.dumps({n:r for n,r in manifest.items() if n!='cap_noop'},indent=2)+'\n')
    print(json.dumps(manifest,indent=2))


if __name__=='__main__':main()
