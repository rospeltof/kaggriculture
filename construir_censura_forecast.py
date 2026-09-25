"""Freeze native/floor negative-evidence masks over both submitted policies."""
import hashlib
import json
from pathlib import Path

OUT=Path('results/censura_forecast_20260925')
EVIDENCE=Path('docs/evidencia/loop_publicos_20260925')


def main():
    panel=json.loads((EVIDENCE/'close_panel_manifest.json').read_text())
    parents={'vq':panel['controls']['base'],'top3':panel['controls']['top3']}
    layer=Path('capa_censura_forecast.py').read_bytes();OUT.mkdir(parents=True,exist_ok=True)
    manifest={}
    for parent,spec in parents.items():
        raw=Path(spec['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==spec['sha256']
        for mode,enabled in [('native',True),('floor',True),('native',False)]:
            name=f'censor_{mode if enabled else "noop"}_{parent}'
            path=OUT/(name+'.py');assert not path.exists()
            data=raw+b'\n'+layer+f'\n_CF_MODE={mode!r}\n_CF_ENABLED={enabled!r}\n'.encode()
            compile(data,str(path),'exec');path.write_bytes(data)
            manifest[name]=dict(path=str(path),sha256=hashlib.sha256(data).hexdigest(),
                                config=dict(parent=parent,mode=mode,enabled=enabled),
                                behavior_reference='base' if parent=='vq' else 'top3')
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (EVIDENCE/'forecast_censor_variants.json').write_text(json.dumps(
        {n:r for n,r in manifest.items() if r['config']['enabled']},indent=2)+'\n')
    print(json.dumps(manifest,indent=2))


if __name__=='__main__':main()
