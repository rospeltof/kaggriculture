"""Extract the exact grain-funding and failed-feed chain from frozen causal replays."""
import gzip
import json
from pathlib import Path

OUT = Path('docs/evidencia/loop_publicos_20260925')
TAG = 'pilot10.cow_d3_y1_m100.harm'


def main():
    records = []
    for arm in ('base', 'cow_d3_y1_m100'):
        replay = json.loads(gzip.decompress((OUT/(TAG+'.'+arm+'.replay.json.gz')).read_bytes()))
        ledger = [json.loads(l) for l in gzip.decompress((OUT/(TAG+'.'+arm+'.ledger.jsonl.gz')).read_bytes()).decode().splitlines()]
        events = []
        for step in range(173, 240):
            obs = replay['steps'][step][0]['observation']
            farm, private = obs['farms'][0], obs['private']
            action = replay['steps'][step+1][0]['action']
            buys = [o for o in action.get('market', []) if o[:2] == ['BUY_PRODUCT', 'WHEAT']]
            if buys:
                accepted = [e for e in ledger if e['player'] == 0 and e['step'] == step and e['op'] == 'BUY_PRODUCT' and e['item'] == 'WHEAT']
                events.append(dict(step=step, kind='BUY_WHEAT', money_before=farm['money'],
                                   wheat_price_before=obs['market']['prices']['WHEAT'], shed_wheat_before=private['shed'].get('WHEAT', 0),
                                   requested=sum(o[2] for o in buys), accepted=len(accepted), cash=sum(e['value'] for e in accepted)))
            commands = [action.get('farmer') or ['PASS'], *(action.get('hands') or [])]
            for actor, (pos, command, inv) in enumerate(zip([farm['farmer'], *farm['hands']], commands, private['inventories'])):
                if command == ['FEED'] and tuple(pos) in ((4,2), (4,3), (4,4)):
                    tile = farm['tiles'][pos[1]][pos[0]]
                    events.append(dict(step=step, kind='FEED', actor=actor, xy=pos,
                                       wheat_before=inv.get('WHEAT', 0), fed_before=tile.get('fed_today')))
        records.append(dict(arm=arm, events=events))
    (OUT/'pilot10.funding_failure.json').write_text(json.dumps(dict(
        note='Observed legal-policy chain in the preselected harm cell; no money or state injected. Original 720-step rewards and ledger were reproduced.',
        seed=1018001, opponent='ars40', seat=0, records=records), indent=2)+'\n')
    for row in records:
        print(row['arm'], [e for e in row['events'] if e['step'] == 191 or e['kind'] == 'FEED'])


if __name__ == '__main__':
    main()
