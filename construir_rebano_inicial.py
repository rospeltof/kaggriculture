"""Build the four preregistered initial herd compositions and an exact noop."""
import hashlib
import json
from pathlib import Path

BASE = Path('submission/main_publico_arshs3_vq_top3.py')
OUT = Path('results/rebano_inicial_20260925')
EVIDENCE = Path('docs/evidencia/loop_publicos_20260925')


def main():
    raw = BASE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == '9668e30ad08f79d485bd230a3c660d4cc420b9382e87f9387b6908e3c94a5145'
    layer = Path('capa_rebano_inicial.py').read_bytes()
    configs = dict(initial_sheep1=('COW', 'SHEEP', 1), initial_sheep2=('COW', 'SHEEP', 2),
                   initial_cow1=('SHEEP', 'COW', 1), initial_cow2=('SHEEP', 'COW', 2),
                   initial_noop=('COW', 'SHEEP', 0))
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for name, (source, target, qty) in configs.items():
        path = OUT/(name+'.py')
        if path.exists():
            raise FileExistsError(path)
        config = dict(source=source, target=target, qty=qty)
        constants = f'\n_IH_FROM={source!r}\n_IH_TO={target!r}\n_IH_QTY={qty}\n'
        data = raw+constants.encode()+layer
        compile(data, str(path), 'exec')
        path.write_bytes(data)
        manifest[name] = dict(path=str(path), sha256=hashlib.sha256(data).hexdigest(), config=config,
                              layer_sha256=hashlib.sha256(layer).hexdigest())
    (OUT/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    (EVIDENCE/'initial_herd_variants.json').write_text(json.dumps({n: r for n, r in manifest.items() if n != 'initial_noop'}, indent=2)+'\n')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
