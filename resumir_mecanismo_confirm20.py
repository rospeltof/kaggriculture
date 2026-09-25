"""Reconcile the completed confirm20 mechanism audit, without new games."""
from collections import Counter
import gzip
import json
from pathlib import Path

OUT = Path('docs/evidencia/loop_publicos_20260925')


def main():
    rows = json.loads((OUT/'confirm20.physical.json').read_text())
    result = []
    for row in rows:
        ledger = [json.loads(line) for line in gzip.decompress(
            (OUT/f"confirm20.physical.{row['case']}.{row['arm']}.ledger.jsonl.gz").read_bytes()).splitlines()]
        own = [event for event in ledger if event['player'] == row['seat']]
        assert 3000 + sum(e['value'] for e in own) == row['rewards'][row['seat']]
        if row['arm'] == 'base':
            continue
        base = next(b for b in rows if b['case'] == row['case'] and b['arm'] == 'base')
        buys = {e['step']: e for e in row['edits'] if e['kind'] == 'buy'}
        closes = [e for e in row['edits'] if e['kind'] == 'close']
        assert len(buys) == len(closes) == row['reports']['_TR_REPORT']['buys']
        reconciled = []
        for close in closes:
            buy = buys[close['buy_step']]
            paid = [e for e in own if e['step'] == buy['step'] and e['op'] == 'BUY_PRODUCT' and e['item'] == 'WHEAT']
            sold = [e for e in own if e['step'] == close['step'] and e['op'] == 'SELL' and e['item'] == 'WHEAT']
            assert close['step'] == buy['step'] + 1
            assert len(paid) == close['bought'] == buy['quantity']
            assert len(sold) == close['quantity'] >= close['bought']
            reconciled.append(dict(buy_step=buy['step'], close_step=close['step'],
                                   bought=len(paid), sold=len(sold), inherited=close['inherited_sale'],
                                   paid=sum(e['value'] for e in paid), received=sum(e['value'] for e in sold)))
        flow_delta = {}
        for key in sorted(set(base['flows']) | set(row['flows'])):
            before, after = base['flows'].get(key, [0, 0]), row['flows'].get(key, [0, 0])
            if before != after:
                flow_delta[key] = [after[0]-before[0], after[1]-before[1]]
        own_delta = row['rewards'][row['seat']] - base['rewards'][row['seat']]
        rival_delta = row['rewards'][1-row['seat']] - base['rewards'][1-row['seat']]
        assert sum(delta[1] for delta in flow_delta.values()) == own_delta
        assert own_delta - rival_delta == row['margin'] - base['margin']
        result.append(dict(case=row['case'], arm=row['arm'], seed=row['seed'], opponent=row['opponent'],
                           margin_before=base['margin'], margin_after=row['margin'], own_cash_delta=own_delta,
                           rival_cash_delta=rival_delta, flow_delta=flow_delta, operations=reconciled,
                           same_accepted_work=row['accepted'] == base['accepted'],
                           same_harvest=row['harvested'] == base['harvested'],
                           harvest_delta={k: row['harvested'].get(k, 0)-base['harvested'].get(k, 0)
                                          for k in set(row['harvested']) | set(base['harvested'])
                                          if row['harvested'].get(k, 0) != base['harvested'].get(k, 0)},
                           same_shops=row['shops'] == base['shops'], same_additions=row['additions'] == base['additions'],
                           escapes=row['escapes']))
    output = dict(games=len(rows), candidate_games=len(result),
                  operations=sum(len(r['operations']) for r in result),
                  units_bought=sum(e['bought'] for r in result for e in r['operations']),
                  units_sold=sum(e['sold'] for r in result for e in r['operations']), results=result,
                  note='All changed-WLT rival/seed cells, seat0, explain mechanism only. Cash deltas include all downstream effects; they are not isolated roundtrip profits or an independent WLT estimate.')
    (OUT/'confirm20.physical.summary.json').write_text(json.dumps(output, indent=2)+'\n')
    print(json.dumps({k: v for k, v in output.items() if k != 'results'}))


if __name__ == '__main__':
    main()
