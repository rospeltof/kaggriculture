"""Bookkeeping of accepted sales; ordinal matching is descriptive, never causal."""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path

OUT = Path('docs/evidencia/loop_publicos_20260925')


def main(suffix):
    audit_path = OUT / f'feedback_{suffix}.audit.json'
    audit = json.loads(audit_path.read_text())
    receipts = {r['id']: r for r in json.loads((OUT / f'feedback_{suffix}.fetch.json').read_text())}
    target = OUT / f'feedback_{suffix}.sale_timing.json'
    assert not target.exists()
    result = dict(created_at=datetime.now(timezone.utc).isoformat(),
                  rule='All accepted SELL flows in every exact-source recency control. Pair nth chronological unit with nth rival unit only for accounting; not identical production units or a causal price effect.',
                  audit_sha256=hashlib.sha256(audit_path.read_bytes()).hexdigest(), results=[])
    for control in audit['results']:
        episode = control['episode']; seat = control['seat']
        receipt = receipts[episode]; replay_path = Path(receipt['path'])
        assert hashlib.sha256(replay_path.read_bytes()).hexdigest() == receipt['sha256'] == control['replay_sha256']
        replay = json.loads(replay_path.read_text())
        path = OUT / f'feedback_{suffix}.{episode}.ledger.jsonl.gz'
        ledger = [json.loads(line) for line in gzip.decompress(path.read_bytes()).decode().splitlines()]
        for player in (0, 1):
            assert 3000 + sum(e['value'] for e in ledger if e['player'] == player) == control['rewards'][player]
        flows = defaultdict(lambda: [[], []])
        for e in ledger:
            if e['op'] == 'SELL':
                flows[e['item']][0 if e['player'] == seat else 1].append(e)
        products = {}
        for item, (own, other) in sorted(flows.items()):
            n = min(len(own), len(other)); pairs = []
            for index, (a, b) in enumerate(zip(own, other)):
                pairs.append(dict(index=index, own_step=a['step'], rival_step=b['step'],
                                  own_price=a['value'], rival_price=b['value'],
                                  cash_difference=a['value']-b['value']))
            matched_gap = sum(p['cash_difference'] for p in pairs)
            unmatched_own = sum(e['value'] for e in own[n:])
            unmatched_other = sum(e['value'] for e in other[n:])
            gap = sum(e['value'] for e in own) - sum(e['value'] for e in other)
            assert gap == matched_gap + unmatched_own - unmatched_other
            daily = []
            for day in range(30):
                parts = [[e for e in es if e['step']//24 == day] for es in (own, other)]
                if not any(parts):
                    continue
                daily.append(dict(day=day, quantity=[len(es) for es in parts],
                                  cash=[sum(e['value'] for e in es) for es in parts]))
            # Preserve emitted order slots, without pretending to infer which duplicate
            # SELL command produced each fill in the ledger.
            turns = []
            grouped = defaultdict(lambda: [[], []])
            for which, es in enumerate((own, other)):
                for e in es:
                    grouped[e['step']][which].append(e['value'])
            for step, prices in sorted(grouped.items()):
                observation = replay['steps'][step][0]['observation']
                orders = []
                for player in (seat, 1-seat):
                    market = (replay['steps'][step+1][player]['action'] or {}).get('market') or []
                    orders.append([dict(slot=i, order=o) for i, o in enumerate(market)
                                   if len(o) >= 2 and o[1] == item])
                turns.append(dict(step=step, market_stock=observation['market']['inventory'][item],
                                  shops=observation['town']['unlocked_shops'],
                                  quantity=[len(ps) for ps in prices], cash=[sum(ps) for ps in prices],
                                  requested_orders=orders))
            products[item] = dict(quantity=[len(own), len(other)],
                                  cash=[sum(e['value'] for e in es) for es in (own, other)],
                                  cash_gap=gap, matched_units=n, matched_ordinal_cash_gap=matched_gap,
                                  unmatched_cash=[unmatched_own, unmatched_other],
                                  ordinal_timing=dict(earlier=sum(a['step'] < b['step'] for a, b in zip(own, other)),
                                                      same=sum(a['step'] == b['step'] for a, b in zip(own, other)),
                                                      later=sum(a['step'] > b['step'] for a, b in zip(own, other))),
                                  daily=daily, turns=turns, pairs=pairs)
        result['results'].append(dict(episode=episode, policy=control['policy'], opponent=control['opponent'],
                                     seat=seat, replay_sha256=receipt['sha256'],
                                     ledger_sha256=hashlib.sha256(path.read_bytes()).hexdigest(), products=products))
    target.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(episodes=len(result['results']), products=sum(len(r['products']) for r in result['results']), output=str(target))))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('suffix'); main(ap.parse_args().suffix)
