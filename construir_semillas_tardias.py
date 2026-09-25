"""Freeze two distinct wheat seed-budget policies over the submitted VQ source."""
import hashlib
import json
from pathlib import Path

BASE = Path('submission/main_publico_arshs3_vq.py')
OUT = Path('results/semillas_tardias_20260925')
EVIDENCE = Path('docs/evidencia/loop_publicos_20260925')


def main():
    raw = BASE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == '9b463dfb8076b4c63946e1ae4249cd1cfc3cc58b63115cf2bd5b00f96f188976'
    layer = Path('capa_semillas_tardias.py').read_bytes(); OUT.mkdir(parents=True, exist_ok=True)
    configs = dict(seed_kind=dict(mode='kind', enabled=True), seed_jit=dict(mode='jit', enabled=True),
                   seed_noop=dict(mode='kind', enabled=False))
    manifest = {}
    for name, config in configs.items():
        path = OUT / (name + '.py'); assert not path.exists()
        data = raw + b'\n' + layer + f"\n_LS_MODE={config['mode']!r}\n_LS_ENABLED={config['enabled']!r}\n".encode()
        compile(data, str(path), 'exec'); path.write_bytes(data)
        manifest[name] = dict(path=str(path), sha256=hashlib.sha256(data).hexdigest(), config=config)
    control = Path('submission/main_publico_arshs3_vq_top3.py')
    manifest['top3'] = dict(path=str(control), sha256=hashlib.sha256(control.read_bytes()).hexdigest(), config=dict(control=True))
    (OUT / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    (EVIDENCE / 'late_seed_variants.json').write_text(json.dumps({n: r for n, r in manifest.items() if r['config'].get('enabled')}, indent=2) + '\n')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
