"""Controlled interventions on the native feed-value rule, preserving its mechanics."""
import ast
import hashlib
import json
from pathlib import Path

BASE = Path('submission/main_publico_arshs3_vq_top3.py')
OUT = Path('results/alimentacion_economica_20260925')
EVIDENCE = Path('docs/evidencia/loop_publicos_20260925')


def main():
    raw = BASE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == '9668e30ad08f79d485bd230a3c660d4cc420b9382e87f9387b6908e3c94a5145'
    text = raw.decode()
    function = next(n for n in ast.parse(text).body if isinstance(n, ast.FunctionDef) and n.name == '_r85_feed')
    original = ast.get_source_segment(text, function)
    assert original.count('*1.25') == 1
    modified = original.replace('*1.25', '*_FF_MULTIPLIER')
    marker = "        item={'GOOSE':'EGG','COW':'MILK','SHEEP':'WOOL'}[tile['animal']]"
    assert modified.count(marker) == 1
    modified = modified.replace(marker, "        if _FF_KEEP_SHEEP and tile['animal']=='SHEEP':continue\n"+marker)
    layer = "\n# Local feed economics experiment; upstream Apache-2.0 attribution retained.\n_FF_PARENT=[v for v in list(globals().values()) if callable(v)][-1]\n"
    layer += modified+'\n\ndef feed_economics_agent(observation, configuration=None):\n    return _FF_PARENT(observation, configuration)\n'
    configs = dict(feed_half=dict(multiplier=0.5, keep_sheep=False, enabled=True),
                   feed_double=dict(multiplier=2.5, keep_sheep=False, enabled=True),
                   feed_keep_sheep=dict(multiplier=1.25, keep_sheep=True, enabled=True),
                   feed_all=dict(multiplier=1.25, keep_sheep=False, enabled=False),
                   feed_noop=dict(multiplier=1.25, keep_sheep=False, enabled=True))
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for name, cfg in configs.items():
        path = OUT/(name+'.py')
        if path.exists():
            raise FileExistsError(path)
        tail = f'\n_FF_MULTIPLIER={cfg["multiplier"]!r}\n_FF_KEEP_SHEEP={cfg["keep_sheep"]!r}\n_R85_FEED={cfg["enabled"]!r}\n'
        data = raw+layer.encode()+tail.encode()
        compile(data, str(path), 'exec')
        path.write_bytes(data)
        manifest[name] = dict(path=str(path), sha256=hashlib.sha256(data).hexdigest(), config=cfg)
    (OUT/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    (EVIDENCE/'feed_variants.json').write_text(json.dumps({k: v for k, v in manifest.items() if k != 'feed_noop'}, indent=2)+'\n')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
