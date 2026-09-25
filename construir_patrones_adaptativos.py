"""Six preregistered forecasting variants, with an exact-transformation control."""
import hashlib
import json
from pathlib import Path

BASE = Path('submission/main_publico_arshs3_vq_top3.py')
LAYER = Path('capa_patrones_adaptativos.py')
OUT = Path('results/patrones_adaptativos_20260925')
CONFIGS = {
    'rank5': ('global', 240, 5),
    'rank7': ('global', 240, 7),
    'history120': ('global', 120, 3),
    'history360': ('global', 360, 3),
    'product3': ('product', 240, 3),
    'phase2': ('phase', 240, 3),
    'transform_noop': ('global', 240, 3),
}


def main():
    raw = BASE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == '9668e30ad08f79d485bd230a3c660d4cc420b9382e87f9387b6908e3c94a5145'
    layer = LAYER.read_bytes()
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for name, (mode, history, top) in CONFIGS.items():
        path = OUT / (name + '.py')
        if path.exists():
            raise FileExistsError(path)
        config = f'\n_PM_MODE={mode!r}\n_PM_HISTORY={history}\n_PM_TOP={top}\n'
        data = raw + config.encode() + layer
        compile(data, str(path), 'exec')
        path.write_bytes(data)
        manifest[name] = dict(path=str(path), sha256=hashlib.sha256(data).hexdigest(),
                              mode=mode, history=history, top=top,
                              layer_sha256=hashlib.sha256(layer).hexdigest())
    (OUT / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
