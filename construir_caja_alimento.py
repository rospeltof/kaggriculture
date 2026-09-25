"""Freeze food-funding policies without changing the running early-cow block."""
import hashlib
import json
from pathlib import Path

BASE = Path('submission/main_publico_arshs3_vq_top3.py')
OUT = Path('results/caja_alimento_20260925')
EVIDENCE = Path('docs/evidencia/loop_publicos_20260925')


def main():
    raw = BASE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == '9668e30ad08f79d485bd230a3c660d4cc420b9382e87f9387b6908e3c94a5145'
    early = Path('capa_vacas_tempranas.py').read_text()
    assert early.count('margin=_EC_MARGIN)') == 1
    early = early.replace('margin=_EC_MARGIN)', 'margin=_cf_margin(obs, action))')
    layer = Path('capa_caja_alimento.py').read_text()
    configs = dict(cash_food_night=('night', False, 3), cash_food_24=(24, False, 3),
                   cash_food_48=(48, False, 3), cash_all_24=(24, True, 3),
                   cash_noop=(24, False, 8))
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for name, (horizon, all_costs, start) in configs.items():
        path = OUT/(name+'.py')
        if path.exists():
            raise FileExistsError(path)
        config = dict(horizon=horizon, all_costs=all_costs, start=start)
        constants = f'\n_EC_START={start}\n_EC_MIN_YARN=1\n_CF_HORIZON={horizon!r}\n_CF_ALL={all_costs!r}\n'
        data = raw+constants.encode()+early.encode()+b'\n'+layer.encode()
        compile(data, str(path), 'exec')
        path.write_bytes(data)
        manifest[name] = dict(path=str(path), sha256=hashlib.sha256(data).hexdigest(), config=config)
    (OUT/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    (EVIDENCE/'cash_variants.json').write_text(json.dumps({n: r for n, r in manifest.items() if n != 'cash_noop'}, indent=2)+'\n')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
