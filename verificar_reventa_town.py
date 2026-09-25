"""Verify observed buys against engine receipts and following liquidation."""
import contextlib
import gzip
import io
import json
from pathlib import Path

from verificar_alimentacion_economica import main as verify_execution

OUT = Path('docs/evidencia/loop_publicos_20260925')
TAG = 'town_trade_smoke'


def main():
    with contextlib.redirect_stdout(io.StringIO()):
        report = verify_execution(tag=TAG, manifest_file='town_trade_variants.json',
                                  output_file='town_trade_execution.json', expected_games=30, noop_name='town_noop')
    manifest = json.loads((OUT/'town_trade_variants.json').read_text())
    rows = json.loads((OUT/(TAG+'.json')).read_text())
    checks = []; activation = {n: 0 for n in manifest}
    for row in rows:
        if row['arm'] not in manifest: continue
        events = row['layer_events']['_TR_EVENTS']; stats = row['reports']['_TR_REPORT']
        buys = {e['step']: e for e in events if e['kind'] == 'buy'}
        closes = {e['buy_step']: e for e in events if e['kind'] == 'close'}
        assert set(buys) == set(closes)
        assert stats['buys'] == stats['closes'] == len(buys) and stats['errors'] == 0
        assert stats['requested'] == sum(e['quantity'] for e in buys.values())
        assert stats['observed_bought'] == sum(e['bought'] for e in closes.values())
        ledger = [json.loads(l) for l in gzip.decompress((OUT/f"{TAG}.{row['seed']}.{row['arm']}.{row['seat']}.ledger.jsonl.gz").read_bytes()).decode().splitlines()]
        owned = [e for e in ledger if e['player'] == row['seat'] and e['item'] == 'WHEAT']
        pairs = []
        for step, buy in buys.items():
            close = closes[step]; quantity = buy['quantity']
            assert close['step'] == step+1 and step % 24 in (4, 8, 12, 16, 20) and 288 <= step <= 695
            assert 0 < quantity <= min(manifest[row['arm']]['config']['max_quantity'], buy['capacity'])
            assert buy['money']-buy['estimated_cost'] >= 5000 and buy['naive_profit'] > 0 and buy['drain'] > 0
            for action in (buy['original'], buy['native_next']):
                assert not action.get('market')
                assert not any(c and c[0] in ('PICKUP', 'DROP', 'PLACE') for c in [action.get('farmer')] + list(action.get('hands') or []))
            accepted_buy = [e for e in owned if e['step'] == step and e['op'] == 'BUY_PRODUCT']
            accepted_sale = [e for e in owned if e['step'] == step+1 and e['op'] == 'SELL']
            assert len(accepted_buy) == close['bought'] <= quantity
            # This is an upper bound on possible diversion, not proof of a pickup fill.
            pickup_requested = sum(int(c[2]) for c in close['units'] if c and len(c) >= 3 and c[:2] == ['PICKUP', 'WHEAT'])
            missing_sale = max(0, close['bought']-len(accepted_sale))
            assert missing_sale <= pickup_requested
            if close['bought']:
                assert close['modified'][0][:2] == ['SELL', 'WHEAT']
                assert close['modified'][0][2] == max(close['bought'], close['inherited_sale'])
                assert len(close['modified']) <= 10
            pairs.append(dict(step=step, requested=quantity, accepted_buy=len(accepted_buy),
                              next_sale=len(accepted_sale), inherited_sale=close['inherited_sale'],
                              missing_sale=missing_sale, pickup_requested=pickup_requested,
                              buy_cash=sum(e['value'] for e in accepted_buy),
                              next_sale_cash=sum(e['value'] for e in accepted_sale), naive_profit=buy['naive_profit']))
        activation[row['arm']] += len(buys)
        checks.append(dict(seed=row['seed'], arm=row['arm'], seat=row['seat'],
                           roundtrips=pairs, escapes=row['escapes'], changed_action_turns=row['changed_action_turns']))
    assert all(activation.values()), activation
    report.update(competitive_ready=True, activation=activation, roundtrip_checks=checks,
                  note='Sources, noop, cash, actual wheat buys and next sales validated. Positive no-rival forecast is not guaranteed profit; no reward-based development selection.')
    (OUT/'town_trade_validation.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('summary', 'roundtrip_checks')}, indent=2))
    for row in checks:
        print(json.dumps(dict(seed=row['seed'], arm=row['arm'], seat=row['seat'], pairs=len(row['roundtrips']),
                             bought=sum(r['accepted_buy'] for r in row['roundtrips']),
                             missing_sales=sum(r['missing_sale'] for r in row['roundtrips']), escapes=row['escapes'])))
    return report


if __name__ == '__main__': main()
