"""Verify buy edits and accepted transactions; development rewards do not select arms."""
from collections import Counter
import contextlib
import gzip
import io
import json
from pathlib import Path

from verificar_alimentacion_economica import main as verify_execution

OUT = Path('docs/evidencia/loop_publicos_20260925')
TAG = 'wheat_trade_smoke'


def main():
    with contextlib.redirect_stdout(io.StringIO()):
        report = verify_execution(tag=TAG, manifest_file='wheat_trade_variants.json',
                                  output_file='wheat_trade_execution.json', expected_games=30, noop_name='wheat_noop')
    manifest = json.loads((OUT/'wheat_trade_variants.json').read_text())
    rows = json.loads((OUT/(TAG+'.json')).read_text())
    validation = []
    for row in rows:
        if row['arm'] not in manifest: continue
        config = manifest[row['arm']]['config']
        events = row['layer_events']['_WT_EVENTS']; stats = row['reports']['_WT_REPORT']
        assert stats['errors'] == 0 and stats['changed'] == len(events)
        assert stats['cut_units'] == sum(e['original_quantity']-e['new_quantity'] for e in events)
        assert stats['moved'] == sum(e['new_index'] != e['original_index'] for e in events)
        ledger = [json.loads(l) for l in gzip.decompress((OUT/f"{TAG}.{row['seed']}.{row['arm']}.{row['seat']}.ledger.jsonl.gz").read_bytes()).decode().splitlines()]
        matches = []
        for event in events:
            step = event['step']; old = event['original']; index = event['original_index']
            assert 288 <= step <= 695 and step % 24 != 23
            assert old[index][:2] == ['BUY_PRODUCT', 'WHEAT'] and old[index][2] >= 20
            assert sum(o[:2] == ['BUY_PRODUCT', 'WHEAT'] for o in old) == 1
            assert all(o[0] == 'BUY_SEED' for i, o in enumerate(old) if i != index)
            quantity = (old[index][2]+1)//2 if config['half'] else old[index][2]
            assert quantity == event['new_quantity'] and event['next_native_sale'] >= (old[index][2]+1)//2
            expected = [list(o) for o in old]; expected[index][2] = quantity
            if config['front']: expected.insert(0, expected.pop(index))
            assert event['modified'] == expected
            actual = [e for e in ledger if e['player'] == row['seat'] and e['step'] == step and e['op'] == 'BUY_PRODUCT' and e['item'] == 'WHEAT']
            assert len(actual) <= quantity
            next_sale = [e for e in ledger if e['player'] == row['seat'] and e['step'] == step+1 and e['op'] == 'SELL' and e['item'] == 'WHEAT']
            matches.append(dict(step=step, original_slot=index, new_slot=event['new_index'],
                                original_request=old[index][2], new_request=quantity,
                                accepted_buy=len(actual), buy_cash=sum(e['value'] for e in actual),
                                planned_next_sale=event['next_native_sale'], accepted_next_sale=len(next_sale),
                                next_sale_cash=sum(e['value'] for e in next_sale)))
        validation.append(dict(arm=row['arm'], seed=row['seed'], seat=row['seat'],
                               stats=stats, matches=matches, escapes=row['escapes'],
                               changed_action_turns=row['changed_action_turns'],
                               actual_wheat_buys=row['flows'].get('BUY_PRODUCT:WHEAT'),
                               actual_wheat_sales=row['flows'].get('SELL:WHEAT')))
    report['buy_events'] = validation
    report['note'] = 'Execution, exact declared edits, cash and actual transactions verified. Harvest/feed differences and escapes are recorded; no guarantee of economic improvement or preserved production.'
    (OUT/'wheat_trade_validation.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('summary', 'buy_events')}, indent=2))
    for r in validation:
        print(json.dumps({k: v for k, v in r.items() if k != 'matches'}))
    return report


if __name__ == '__main__': main()
