"""Controlled ablation of native opening policies, plus a new public reference."""
import hashlib
import json
from pathlib import Path

BASE = Path('submission/main_publico_arshs3_vq_top3.py')
OUT = Path('results/aperturas_publicas_20260925')


def main():
    raw = BASE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == '9668e30ad08f79d485bd230a3c660d4cc420b9382e87f9387b6908e3c94a5145'
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for name, mode in dict(open_original='Original', open_cycle='EarlyCycle',
                           open_tomato='TomatoInsteadOfCow', open_noop='HybridOpening').items():
        path = OUT/(name+'.py')
        if path.exists():
            raise FileExistsError(path)
        data = raw+f'\n# Native opening ablation; all upstream attribution retained.\n_ALT_MODE={mode!r}\n'.encode()
        compile(data, str(path), 'exec')
        path.write_bytes(data)
        manifest[name] = dict(path=str(path), sha256=hashlib.sha256(data).hexdigest(), mode=mode)
    path = Path('results/publicos_0400_20260925/leoprovorov_a-song-of-ice-and-fire-fixed-flexible/main_entry_fixed.py')
    manifest['marketshock'] = dict(path=str(path), sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                                  source='leoprovorov/a-song-of-ice-and-fire-fixed-flexible',
                                  modification='Only reinsert installed agent last for official Kaggle loader; policy verified identical to named upstream entry.')
    (OUT/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
