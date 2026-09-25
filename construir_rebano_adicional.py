"""Extra sheep without speculative shops or land purchase; separate from loop3."""
import hashlib
import json
from pathlib import Path

BASE = Path('submission/main_publico_arshs3_vq_top3.py')
LAYER = Path('capa_rebano_adicional.py')
OUT = Path('results/rebano_adicional_v3_20260925')


def main():
    raw = BASE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == '9668e30ad08f79d485bd230a3c660d4cc420b9382e87f9387b6908e3c94a5145'
    layer = LAYER.read_bytes()
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for day in (12, 14):
        for size in (2, 3, 6):
            name = f'sheep{size}_d{day}'
            path = OUT / (name+'.py')
            if path.exists():
                raise FileExistsError(path)
            data = raw+f'\n_SG_START={day}\n_SG_SIZE={size}\n_SG_MARGIN=600\n'.encode()+layer
            compile(data, str(path), 'exec')
            path.write_bytes(data)
            manifest[name] = dict(path=str(path), sha256=hashlib.sha256(data).hexdigest(),
                                  day=day, size=size, margin=600,
                                  layer_sha256=hashlib.sha256(layer).hexdigest())
    (OUT / 'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
