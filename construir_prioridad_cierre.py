"""Loop31: queue-only wrappers around frozen town50 parents, plus disabled noops."""
import hashlib
import json
from pathlib import Path

OUT = Path('results/prioridad_cierre_20260925')
EVIDENCE = Path('docs/evidencia/loop_publicos_20260925')


def main():
    previous = json.loads((EVIDENCE / 'town_factorial_variants.json').read_text())
    layer = Path('capa_prioridad_cierre.py').read_bytes()
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for label in ('vq', 'top3'):
        parent = 'town50_' + label
        spec = previous[parent]
        raw = Path(spec['path']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == spec['sha256']
        for enabled in (True, False):
            name = ('close_queue_' if enabled else 'close_noop_') + label
            path = OUT / (name + '.py')
            assert not path.exists()
            data = raw + b'\n' + layer + f'\n_CQ_ENABLED={enabled!r}\n'.encode()
            compile(data, str(path), 'exec')
            path.write_bytes(data)
            manifest[name] = dict(path=str(path), sha256=hashlib.sha256(data).hexdigest(),
                                  config=dict(enabled=enabled, max_quantity=50),
                                  behavior_reference=parent, source_parent=spec)
    (OUT / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    candidates = {name: spec for name, spec in manifest.items() if spec['config']['enabled']}
    (EVIDENCE / 'close_queue_variants.json').write_text(json.dumps(candidates, indent=2) + '\n')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
