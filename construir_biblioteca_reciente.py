"""Freeze three source-set variants over top3, preserving all upstream notices."""
import hashlib
import json
from pathlib import Path

BASE = Path('submission/main_publico_arshs3_vq_top3.py')
LAYER = Path('capa_biblioteca_reciente.py')
STREAMS = Path('docs/evidencia/loop_publicos_20260925/recent_sale_streams.json')
OUT = Path('results/biblioteca_reciente_20260925')


def main():
    raw, layer = BASE.read_bytes(), LAYER.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == '9668e30ad08f79d485bd230a3c660d4cc420b9382e87f9387b6908e3c94a5145'
    records = json.loads(STREAMS.read_text())
    assert len(records) == len({r['episode'] for r in records}) == 12
    configs = dict(library_dsm=[r for r in records if r['source'] == 'DSM'],
                   library_ladder=[r for r in records if r['source'].startswith('top3_opponent')],
                   library_all=records, library_noop=[])
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for name, rows in configs.items():
        path = OUT/(name+'.py')
        if path.exists():
            raise FileExistsError(path)
        packed = [{k: r[k] for k in ('episode', 'shops', 'sales')} for r in rows]
        data = raw+('\n_LB_RECORDS='+repr(packed)+'\n').encode()+layer
        compile(data, str(path), 'exec')
        path.write_bytes(data)
        manifest[name] = dict(path=str(path), sha256=hashlib.sha256(data).hexdigest(),
                              episodes=[r['episode'] for r in rows],
                              source_data_sha256=hashlib.sha256(STREAMS.read_bytes()).hexdigest(),
                              layer_sha256=hashlib.sha256(layer).hexdigest())
    (OUT/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
