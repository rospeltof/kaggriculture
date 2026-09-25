"""Identify why the cap valuation fails before any competitive run is launched."""
import gzip
import hashlib
import json
from pathlib import Path

OUT=Path('docs/evidencia/loop_publicos_20260925')


def main():
    rows=json.loads((OUT/'capped_bonus_smoke.json').read_text())
    key={(r['arm'],r['seed'],r['seat']):r for r in rows}
    cases=[]
    for seat in (0,1):
        def events(arm):
            path=OUT/f'capped_bonus_smoke.1039000.{arm}.{seat}.units.jsonl.gz'
            return [json.loads(l) for l in gzip.decompress(path.read_bytes()).decode().splitlines()]
        base,candidate=events('base'),events('cap_full')
        candidate_actions={(e['step'],e['actor'],tuple(e['action'])) for e in candidate}
        omitted=[e for e in base if e['action']==['FEED'] and (e['step'],e['actor'],tuple(e['action'])) not in candidate_actions]
        assert len(omitted)==1 and omitted[0]['step']==682
        feed=omitted[0];xy=feed['xy']
        harvests={arm:[e for e in ev if e['xy']==xy and e['action']==['HARVEST'] and 682<e['step']<=700]
                  for arm,ev in [('base',base),('cap_full',candidate)]}
        assert harvests['base'][0]['step']==harvests['cap_full'][0]['step']==687
        assert harvests['base'][0]['inventory_delta']['EGG']==harvests['cap_full'][0]['inventory_delta']['EGG']==4
        assert harvests['base'][1]['step']==harvests['cap_full'][1]['step']==700
        assert harvests['base'][1]['inventory_delta']['EGG']==2 and harvests['cap_full'][1]['inventory_delta']['EGG']==1
        cases.append(dict(seed=1039000,seat=seat,omitted_feed=feed,later_harvests=harvests,
                          base_harvested=key['base',1039000,seat]['harvested'],
                          candidate_harvested=key['cap_full',1039000,seat]['harvested']))
    summary=[]
    for row in rows:
        if row['arm'] not in ('cap_first','cap_full'):continue
        base=key['base',row['seed'],row['seat']]
        summary.append(dict(seed=row['seed'],seat=row['seat'],arm=row['arm'],
                            value_changes=row['reports'].get('_BC_REPORT',{}).get('value_changes',[]),
                            action_changes=row['changed_action_turns'],
                            accepted_feed_delta={k:row['successful'].get(k,0)-base['successful'].get(k,0)
                                for k in sorted(set(row['successful'])|set(base['successful'])) if k.startswith('FEED:')},
                            harvest_base=base['harvested'],harvest_candidate=row['harvested']))
    report=dict(status='DEVELOPMENT_STOPPED',competitive_ready=False,
                reason='cap_full uses inventory at FEED as if it persisted to production; actual intervening HARVEST invalidates that marginal-value premise. cap_first has no changed actions in the three diagnostic worlds.',
                selection_note='Stopped for a demonstrated valuation/temporal-model error before the pilot, not selected or rejected by development rewards. No population effect estimated.',
                candidate_hashes=json.loads((OUT/'capped_bonus_validation.json').read_text())['candidate_hashes'],
                cases=cases,summary=summary,
                next_action='Do not launch pilot17 or upload these policies. A future version needs inventory projected through harvests, or a provably empty tile plus a feasible next-day feeding plan.')
    (OUT/'capped_bonus_decision.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('status','competitive_ready','reason','next_action')},indent=2))


if __name__=='__main__':main()
