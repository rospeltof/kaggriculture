"""Measure visible-sale inference errors from completed mechanical development."""
from collections import Counter
import gzip
import json
from pathlib import Path

OUT=Path('docs/evidencia/loop_publicos_20260925')
ITEMS=('MILK','WOOL','STRAWBERRY','EGG','MELON')


def lines(path):
    return [json.loads(s) for s in gzip.decompress(path.read_bytes()).decode().splitlines()]


def main():
    target=OUT/'sale_attribution_inference.json';assert not target.exists()
    result=[]
    for prefix in ('sale_attribution_smoke','sale_attribution_coverage'):
        data=json.loads((OUT/f'{prefix}.json').read_text())
        assert len(data['results'])==data['plan']['expected_games']
        for row in data['results']:
            name=row['arm'];seed=row['seed'];seat=row['seat']
            stem=f'{prefix}.{seed}.{name}.{seat}'
            snapshots=lines(OUT/f'{stem}.snapshots.jsonl.gz')
            ledger=lines(OUT/f'{stem}.ledger.jsonl.gz')
            accepted=Counter((e['step'],e['player'],e['item']) for e in ledger if e['op']=='SELL')
            added=Counter((e['step'],e['player'],e['item']) for e in ledger if e['op']=='SELL' and e['value']>1)
            summary=Counter();errors=[]
            for step,snapshot in enumerate(snapshots[:-1]):
                for item in ITEMS:
                    if snapshot['prices'].get(item,0)<=3:continue
                    estimate=added[step,seat,item]+added[step,1-seat,item]-snapshot['own'].get(item,0)
                    reported=estimate>=2; real=accepted[step,1-seat,item]>=2
                    visible=added[step,1-seat,item]>=2
                    summary['eligible_item_turns']+=1
                    summary['false_events']+=reported and not real
                    summary['missed_real_events']+=not reported and real
                    summary['missed_visible_events']+=not reported and visible
                    summary['exact_quantity_when_reported']+=reported and estimate==accepted[step,1-seat,item]
                    if reported != real or (reported and estimate != accepted[step,1-seat,item]):
                        errors.append(dict(step=step,item=item,inferred=estimate,
                                           own_accepted=accepted[step,seat,item],own_added=added[step,seat,item],
                                           rival_accepted=accepted[step,1-seat,item],rival_added=added[step,1-seat,item]))
            if name.startswith('sales_sync'):
                assert summary['false_events']==0  # own accepted qty >= own visible inventory increment
            result.append(dict(block=prefix,arm=name,seed=seed,seat=seat,summary=dict(summary),errors=errors))
    target.write_text(json.dumps(dict(rule='All completed development cells; infer observations using native price/quantity thresholds. Candidate and parent trajectories may differ. Price-floor omissions remain.',results=result),indent=2)+'\n')
    total={}
    for row in result:
        key=f'{row["block"]}:{row["arm"]}';total.setdefault(key,Counter()).update(row['summary'])
    print(json.dumps(total,indent=2))


if __name__=='__main__':main()
