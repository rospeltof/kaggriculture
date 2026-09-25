"""Freeze general compact-worker provision variants and a disabled control."""
import hashlib
import json
from pathlib import Path

BASE = Path('submission/main_publico_arshs3_vq_top3.py')
OUT = Path('results/suministro_ovino_20260925')
EVIDENCE = Path('docs/evidencia/loop_publicos_20260925')


def main():
    raw = BASE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == '9668e30ad08f79d485bd230a3c660d4cc420b9382e87f9387b6908e3c94a5145'
    layer = Path('capa_suministro_ovino.py').read_bytes()
    configs = {'sheep_supply_buy':dict(hold=False,enabled=True),
               'sheep_supply_hold':dict(hold=True,enabled=True),
               'sheep_supply_noop':dict(hold=False,enabled=False)}
    OUT.mkdir(parents=True, exist_ok=True); manifest = {}
    for name, cfg in configs.items():
        path = OUT/(name+'.py'); assert not path.exists(), path
        tail = f"\n_SS_HOLD={cfg['hold']!r}\n_SS_ENABLED={cfg['enabled']!r}\n"
        data = raw+b'\n'+layer+tail.encode(); compile(data, str(path), 'exec'); path.write_bytes(data)
        manifest[name] = dict(path=str(path),sha256=hashlib.sha256(data).hexdigest(),config=cfg)
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (EVIDENCE/'sheep_supply_variants.json').write_text(json.dumps({n:r for n,r in manifest.items() if n!='sheep_supply_noop'},indent=2)+'\n')
    print(json.dumps(manifest,indent=2))


if __name__ == '__main__': main()
