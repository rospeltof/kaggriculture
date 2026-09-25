"""Check the declared support/quantity changes and final market receipts."""
from collections import Counter
import contextlib
import gzip
import hashlib
import io
import json
from pathlib import Path

from verificar_alimentacion_economica import main as verify_execution

OUT = Path('docs/evidencia/loop_publicos_20260925')
TAG = 'extra_forecast_smoke'


def main():
    with contextlib.redirect_stdout(io.StringIO()):
        report = verify_execution(tag=TAG, manifest_file='extra_forecast_variants.json',
                                  output_file='extra_forecast_execution.json', expected_games=42, noop_name='extra_noop')
    manifest = json.loads((OUT/'extra_forecast_variants.json').read_text())
    rows = json.loads((OUT/(TAG+'.json')).read_text()); checked = []
    for row in rows:
        if row['arm'] not in manifest: continue
        policy = manifest[row['arm']]['config']['policy']
        events = row['layer_events']['_XF_EVENTS']; stats = row['reports']['_XF_REPORT']
        assert stats['fires'] == len(events)
        ledger = [json.loads(l) for l in gzip.decompress((OUT/f"{TAG}.{row['seed']}.{row['arm']}.{row['seat']}.ledger.jsonl.gz").read_bytes()).decode().splitlines()]
        actual = Counter((e['step'], e['item']) for e in ledger if e['player'] == row['seat'] and e['op'] == 'SELL')
        for e in events:
            assert any(e['signals']) and e['weak'] == (not e['signals'][0])
            if policy == 'rank2': assert any(e['signals'][:2])
            if policy == 'quorum': assert e['signals'][0] or sum(e['signals']) >= 2
            assert e['horizon'] == (12 if e['weak'] and policy == 'short12' else 48)
            assert e['original_quantity'] == min(e['stock'], e['planned'])
            assert e['quantity'] == ((e['original_quantity']+1)//2 if e['weak'] and policy == 'half' else e['original_quantity'])
            final = sum(int(o[2]) for o in e['final_market'] if len(o) >= 3 and o[:2] == ['SELL', e['item']])
            assert actual[e['step'], e['item']] <= final
        checked.append(dict(seed=row['seed'], arm=row['arm'], seat=row['seat'], stats=stats,
                            changed_action_turns=row['changed_action_turns'], weak_emissions=sum(e['weak'] for e in events),
                            main_emissions=sum(not e['weak'] for e in events), escapes=row['escapes']))
    for name in manifest:
        assert any(r['changed_action_turns'] for r in checked if r['arm'] == name), name
    vq = Path('submission/main_publico_arshs3_vq.py')
    report.update(competitive_ready=True, control_hash=hashlib.sha256(vq.read_bytes()).hexdigest(), checks=checked,
                  note='Noop, hashes, cash, declared forecast support/quantity/horizon and accepted sales bounded by final orders checked. No development reward selection or claim that opponent predictions are correct.')
    (OUT/'extra_forecast_validation.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('summary', 'checks')}, indent=2))
    for row in checked: print(json.dumps(row))
    return report


if __name__ == '__main__': main()
