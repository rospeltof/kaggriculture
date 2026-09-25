"""Freeze already validated sources for the prospectively registered loop25."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import tarfile

OUT = Path('docs/evidencia/loop_publicos_20260925')
PREREG = Path('docs/research/PREREG_LOOP25_PANEL_CERCANO_2026-09-25.md')


def read(name):
    return json.loads((OUT / name).read_text())


def spec(path):
    return dict(path=path, sha256=hashlib.sha256(Path(path).read_bytes()).hexdigest())


def main():
    target = OUT / 'close_panel_manifest.json'
    archive_path = OUT / 'close_panel_sources.tgz'
    assert PREREG.exists() and not target.exists() and not archive_path.exists()
    choices = {
        'history360': ('patterns_variants.json', 'top3'),
        'wheat_front': ('wheat_trade_variants.json', 'top3'),
        'advance_vq': ('advance_wheat_variants.json', 'base'),
        'sheep_supply_buy': ('sheep_supply_variants.json', 'top3'),
        'harvest68': ('public_0712_variants.json', 'top3'),
    }
    candidates = {name: dict(read(source)[name], behavior_reference=parent)
                  for name, (source, parent) in choices.items()}
    controls = {
        'base': spec('submission/main_publico_arshs3_vq.py'),
        'top3': spec('submission/main_publico_arshs3_vq_top3.py'),
    }
    assert controls['base']['sha256'] == '9b463dfb8076b4c63946e1ae4249cd1cfc3cc58b63115cf2bd5b00f96f188976'
    assert controls['top3']['sha256'] == '9668e30ad08f79d485bd230a3c660d4cc420b9382e87f9387b6908e3c94a5145'
    prior_validation = {}
    for name, file in (
        ('wheat_front', 'wheat_trade_validation.json'),
        ('advance_vq', 'advance_wheat_validation.json'),
        ('sheep_supply_buy', 'sheep_supply_validation.json'),
        ('harvest68', 'public_0712_validation.json'),
    ):
        validated = read(file)
        assert validated['passed'] and validated.get('competitive_ready', True)
        assert validated['candidate_hashes'][name] == candidates[name]['sha256']
        prior_validation[name] = spec(str(OUT / file))
    previous = read('confirm8.meta.json')
    checked = read('confirm8.validation.json')
    assert previous['state'] == 'complete' and checked['complete_coverage']
    assert previous['agentes']['history360']['sha256'] == candidates['history360']['sha256']
    prior_validation['history360'] = spec(str(OUT / 'confirm8.validation.json'))
    fresh = read('public_0548_variants.json')
    pool = dict(mirror_vq=controls['base'], mirror_top3=controls['top3'], **fresh)
    extra = dict(recent_harvest68=candidates['harvest68'],
                 arshs3=spec('submission/main_publico_arshs3_arsgorynich.py'))
    all_sources = dict(controls, **candidates, **pool, **extra)
    for name, item in all_sources.items():
        assert spec(item['path'])['sha256'] == item['sha256'], name
    with tarfile.open(archive_path, 'w:gz') as archive:
        for name, item in all_sources.items():
            archive.add(item['path'], arcname=f'agents/{name}.py')
        archive.add(PREREG, arcname=PREREG.name)
    manifest = dict(
        created_at=datetime.now(timezone.utc).isoformat(),
        prereg=spec(str(PREREG)), candidates=candidates, controls=controls,
        pilot_pool=pool, confirm_extra=extra, prior_validation=prior_validation,
        pilot_seeds=list(range(1063000, 1063016)),
        confirm_seeds=list(range(1064000, 1064032)),
        pilot_expected=1920, confirm_expected={1: 1920, 2: 2560},
        source_archive=spec(str(archive_path)),
        interpretation='New conditional population; does not replace prior decisions or identify private opponent code.',
    )
    target.write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps(dict(candidates=list(candidates), pilot_pool=list(pool),
                         confirm_pool=list(dict(pool, **extra)), pilot_expected=1920)))


if __name__ == '__main__':
    main()
