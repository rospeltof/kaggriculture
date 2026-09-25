"""Build independent, source-frozen wheat buy ablations for loop19."""
import hashlib
import json
from pathlib import Path

BASE = Path('submission/main_publico_arshs3_vq_top3.py')
OUT = Path('results/trigo_reventa_20260925')
EVIDENCE = Path('docs/evidencia/loop_publicos_20260925')


def main():
    raw = BASE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == '9668e30ad08f79d485bd230a3c660d4cc420b9382e87f9387b6908e3c94a5145'
    layer = Path('capa_trigo_reventa.py').read_bytes()
    configs = dict(wheat_front=dict(half=False, front=True, enabled=True),
                   wheat_half=dict(half=True, front=False, enabled=True),
                   wheat_both=dict(half=True, front=True, enabled=True),
                   wheat_noop=dict(half=False, front=False, enabled=False))
    OUT.mkdir(parents=True, exist_ok=True); manifest = {}
    for name, cfg in configs.items():
        path = OUT/(name+'.py')
        if path.exists(): raise FileExistsError(path)
        tail = f"\n_WT_HALF={cfg['half']!r}\n_WT_FRONT={cfg['front']!r}\n_WT_ENABLED={cfg['enabled']!r}\n"
        data = raw+b'\n'+layer+tail.encode(); compile(data, str(path), 'exec'); path.write_bytes(data)
        manifest[name] = dict(path=str(path), sha256=hashlib.sha256(data).hexdigest(), config=cfg)
    (OUT/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    (EVIDENCE/'wheat_trade_variants.json').write_text(json.dumps({n: r for n, r in manifest.items() if n != 'wheat_noop'}, indent=2)+'\n')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__': main()
