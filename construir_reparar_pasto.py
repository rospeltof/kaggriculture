"""Loop33: freeze animal construction recovery on both actual sources."""
import hashlib
import json
from pathlib import Path

OUT = Path('results/reparar_pasto_20260925')
EVIDENCE = Path('docs/evidencia/loop_publicos_20260925')


def main():
    panel = json.loads((EVIDENCE / 'close_panel_manifest.json').read_text())
    layer = Path('capa_reparar_pasto.py').read_bytes()
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for parent, label in [('base', 'vq'), ('top3', 'top3')]:
        spec = panel['controls'][parent]
        raw = Path(spec['path']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == spec['sha256']
        for enabled in (True, False):
            name = ('animal_build_' if enabled else 'animal_noop_') + label
            path = OUT / (name + '.py')
            assert not path.exists()
            data = raw + b'\n' + layer + f'\n_AB_ENABLED={enabled!r}\n'.encode()
            compile(data, str(path), 'exec')
            path.write_bytes(data)
            manifest[name] = dict(path=str(path), sha256=hashlib.sha256(data).hexdigest(),
                                  config=dict(enabled=enabled), behavior_reference=parent)
    (OUT / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    (EVIDENCE / 'animal_build_variants.json').write_text(json.dumps(
        {name: spec for name, spec in manifest.items() if spec['config']['enabled']}, indent=2) + '\n')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
