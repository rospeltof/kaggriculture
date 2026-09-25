"""Closed confirmation20 actions and WLT contrasts; no new games."""
import json
from pathlib import Path


def main():
    out=Path('docs/evidencia/loop_publicos_20260925');meta=json.loads((out/'confirm20.meta.json').read_text());assert meta['state']=='complete'
    rows=[json.loads(l) for l in (out/'confirm20.jsonl').read_text().splitlines()]
    assert len(rows)==3200
    keyed={(r['a'],r['b'],r['seed'],r['seat']):r for r in rows};arms=('town20','town50');report={}
    for arm in arms:
        contrasts=[];own=rival=better=worse=cells=0;seeds=set()
        for row in rows:
            if row['a']!=arm or row['b'] in ('base','noop',*arms):continue
            base=keyed['base',row['b'],row['seed'],row['seat']];seat=row['seat'];cells+=1
            changed=row['action_hashes'][seat]!=base['action_hashes'][seat];own+=changed
            rival+=row['action_hashes'][1-seat]!=base['action_hashes'][1-seat]
            if changed:seeds.add(row['seed'])
            delta=row['score']-base['score'];better+=delta>0;worse+=delta<0
            if delta:
                contrasts.append(dict(rival=row['b'],seed=row['seed'],seat=seat,score_before=base['score'],score_after=row['score'],
                                      base_margin=base['rewards'][seat]-base['rewards'][1-seat],margin=row['rewards'][seat]-row['rewards'][1-seat]))
        assert cells==704
        report[arm]=dict(panel_cells=cells,changed_own_cells=own,changed_rival_cells=rival,changed_seeds=sorted(seeds),
                         better_seat_cells=better,worse_seat_cells=worse,contrasts=contrasts)
    (out/'confirm20.behavior.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({n:{k:v for k,v in r.items() if k not in ('changed_seeds','contrasts')} for n,r in report.items()}))


if __name__=='__main__':main()
