"""Build four night-stock hypotheses plus an exact disabled wrapper control."""
import hashlib
import json
from pathlib import Path

BASE = Path('submission/main_publico_arshs3_vq_top3.py')
OUT = Path('results/espacio_nocturno_v2_20260925')
EVIDENCE = Path('docs/evidencia/loop_publicos_20260925')


def main():
    raw = BASE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == '9668e30ad08f79d485bd230a3c660d4cc420b9382e87f9387b6908e3c94a5145'
    layer = Path('capa_espacio_nocturno.py').read_bytes()
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {}
    configs = {f'night_{item}{days}': dict(days=days, fertilizer=item == 'inputs', enabled=True)
               for item in ('wheat', 'inputs') for days in (1, 2)}
    configs['night_noop'] = dict(days=1, fertilizer=False, enabled=False)
    for name, cfg in configs.items():
        path = OUT/(name+'.py')
        if path.exists():
            raise FileExistsError(path)
        data = raw+b'\n'+layer+f'\n_NF_DAYS={cfg["days"]}\n_NF_FERTILIZER={cfg["fertilizer"]}\n_NF_ENABLED={cfg["enabled"]}\n'.encode()
        compile(data, str(path), 'exec')
        path.write_bytes(data)
        manifest[name] = dict(path=str(path), sha256=hashlib.sha256(data).hexdigest(), config=cfg)
    (OUT/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    (EVIDENCE/'night_variants.json').write_text(json.dumps({k: v for k, v in manifest.items() if k != 'night_noop'}, indent=2)+'\n')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
