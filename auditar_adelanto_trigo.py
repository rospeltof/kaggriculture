"""Chronology only: matching large wheat buy requests one step apart in a replay."""
from collections import defaultdict
import gzip
import json
from pathlib import Path

OUT=Path('docs/evidencia/loop_publicos_20260925')


def main():
    replay=json.loads(Path('replays/vq_feedback_0742/episode-113198597-replay.json').read_text())
    seat=replay['info']['TeamNames'].index('Rospel');assert seat==0
    ledger=[json.loads(l) for l in gzip.decompress((OUT/'feedback_0742.113198597.ledger.jsonl.gz').read_bytes()).decode().splitlines()]
    by=defaultdict(list)
    for e in ledger:
        if e['op']=='BUY_PRODUCT' and e['item']=='WHEAT':by[e['player'],e['step']].append(e)
    rows=[]
    for step in range(1,719):
        own=replay['steps'][step+1][seat]['action'];prev=replay['steps'][step][1-seat]['action']
        buys=[(i,o) for i,o in enumerate(own['market']) if len(o)>=3 and o[:2]==['BUY_PRODUCT','WHEAT'] and o[2]>=20]
        for slot,order in buys:
            matches=[(i,o) for i,o in enumerate(prev['market']) if o==order]
            fills=[by[seat,step],by[1-seat,step-1]]
            rows.append(dict(own_step=step,opponent_step=step-1,own_slot=slot,quantity=order[2],
                equal_requested_order_previous_turn=bool(matches),opponent_slots=[i for i,_ in matches],
                actual_units=[len(x) for x in fills],actual_cash=[sum(e['value'] for e in x) for x in fills],
                own_previous_action=replay['steps'][step][seat]['action'],own_action=own,
                opponent_previous_action=prev,
                own_next_action=replay['steps'][step+2][seat]['action'] if step<718 else None))
    report=dict(episode=113198597,policy='vq',seed=replay['info']['seed'],seat=seat,
        scope='Timeline of accepted trades, not recovered opponent policy or causal profit of moving orders. Source replay control verified separately in feedback_0742.audit.json.',
        large_own_buys=len(rows),equal_request_one_step_early=sum(r['equal_requested_order_previous_turn'] for r in rows),
        matched_actual_cash=[sum(r['actual_cash'][p] for r in rows if r['equal_requested_order_previous_turn']) for p in (0,1)],
        matched_actual_units=[sum(r['actual_units'][p] for r in rows if r['equal_requested_order_previous_turn']) for p in (0,1)],
        rows=rows)
    path=OUT/'grim_wheat_timing_audit.json';assert not path.exists();path.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='rows'},indent=2))


if __name__=='__main__':main()
