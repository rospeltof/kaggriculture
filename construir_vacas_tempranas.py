"""Extend native COW substitutions into days 3-7 without adding workers."""
import hashlib
import json
from pathlib import Path

BASE = Path('submission/main_publico_arshs3_vq_top3.py')
LAYER = Path('capa_vacas_tempranas.py')
OUT = Path('results/vacas_tempranas_20260925')


def main():
    raw, layer = BASE.read_bytes(), LAYER.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == '9668e30ad08f79d485bd230a3c660d4cc420b9382e87f9387b6908e3c94a5145'
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for day in (3, 6):
        for yarn, margin in ((1, 100), (2, 100), (1, 500)):
            name = f'cow_d{day}_y{yarn}_m{margin}'
            path = OUT / (name+'.py')
            if path.exists():
                raise FileExistsError(path)
            data = raw+f'\n_EC_START={day}\n_EC_MIN_YARN={yarn}\n_EC_MARGIN={margin}\n'.encode()+layer
            compile(data, str(path), 'exec')
            path.write_bytes(data)
            manifest[name] = dict(path=str(path), sha256=hashlib.sha256(data).hexdigest(),
                                  start=day, min_yarn=yarn, margin=margin,
                                  layer_sha256=hashlib.sha256(layer).hexdigest())
    (OUT/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
