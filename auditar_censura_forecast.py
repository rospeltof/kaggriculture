"""Offline negative-evidence audit on preregistered exact-source trajectories."""
from collections import Counter
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path

from auditar_feedback_real import OUT, SOURCES


def main():
    prefix=OUT/'forecast_censor_audit'
    target=Path(str(prefix)+'.json');plan_path=Path(str(prefix)+'.plan.json')
    assert not target.exists() and not plan_path.exists()
    audit_path=OUT/'feedback_0914.attribution.json'
    audit=json.loads(audit_path.read_text())
    receipts={r['id']:r for r in json.loads((OUT/'feedback_0914.fetch.json').read_text())}
    plan=dict(created_at=datetime.now(timezone.utc).isoformat(),episodes=[r['episode'] for r in audit['results']],
              rule='Every exact-source control from recency0914, no outcome filter. Reconstruct native PREDICT rankings from archived live snapshots; compare two prospectively specified masks for negative evidence. No games, no policy choice by prediction accuracy or reward.',
              masks=['native_eligibility','no_floor_reached'],
              scoring='Keep every observed positive event and native matching/miss rules. Penalize an absent library event only if all three time points in its matching neighborhood were observable under the selected mask. Stable original-library tie order.',
              source_audit_sha256=hashlib.sha256(audit_path.read_bytes()).hexdigest(),
              script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              sources={name:dict(path=path,sha256=hashlib.sha256(Path(path).read_bytes()).hexdigest()) for name,path in SOURCES.items()})
    plan_path.write_text(json.dumps(plan,indent=2)+'\n')
    results=[]
    for control in audit['results']:
        episode=control['episode'];policy=control['policy'];receipt=receipts[episode]
        raw=Path(receipt['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==receipt['sha256']
        replay=json.loads(raw)
        path=OUT/f'feedback_0914.attribution.{episode}.snapshots.jsonl.gz'
        snapshots=[json.loads(line) for line in gzip.decompress(path.read_bytes()).decode().splitlines()]
        ns={};source=Path(SOURCES[policy]);assert hashlib.sha256(source.read_bytes()).hexdigest()==control['source_sha256']
        exec(compile(source.read_bytes(),str(source),'exec'),ns)
        seen={};observable={};rows=[];counters=Counter()
        for step,snapshot in enumerate(snapshots):
            assert snapshot['step']==step
            if step:
                prev=snapshots[step-1]['race_prev'];current=replay['steps'][step][0]['observation']
                draw=ns['_v9_town_draw'](prev['shops'],step-1)
                params=ns['_v44y_params'](current)
                for i,item in enumerate(ns['_V92_P_ITEMS']):
                    q=snapshot['inference_previous'][item]
                    if q is not None:seen[step-1,i]=q
                    native=prev['prices'].get(item,0)>3
                    ending_inventory=current['market']['inventory'][item]+draw.get(item,0)
                    floor=ns['_r37_market_price'](item,ending_inventory,params)>1
                    observable[step-1,i]=(native,native and floor)
                    counters['item_turns']+=1;counters['native_excluded']+=not native
                    counters['additional_floor_excluded']+=native and not floor
            if not (150<=step<700 and step%ns['_V92_P_EVERY']==0):continue
            obs=dict(replay['steps'][step][control.get('seat',0)]['observation'])
            # Only step/town/market are used by the forecaster; player is immaterial here.
            obs['step']=step
            expected=ns['_v92_p_forecast'](obs,dict(obs=seen))
            items=ns['_V92_P_ITEMS']
            expected_next={item:[sum(ev.get((step+dt,i),0) for dt in (1,2)) for ev in expected]
                           for i,item in enumerate(items)}
            assert expected_next==snapshot['next_predictions'],(episode,step)
            shops=tuple(obs['town']['unlocked_shops'][:2]);candidates=ns['_v92_p_pair'](shops)
            assert ns['_V92_EP'] is None
            lo=step-240;recent=[(tt,i) for tt,i in seen if tt>=lo]
            ranked=[[],[],[]];removed=[0,0]
            for index,(_,ev) in enumerate(candidates):
                matches=0;false=[0,0,0]
                for tt,i in ev:
                    if not lo<=tt<step-1:continue
                    if any((tt+delta,i) in seen for delta in (-1,0,1)):
                        matches+=1;continue
                    false[0]+=1
                    for mask in (0,1):
                        penalty=all(observable.get((tt+delta,i),(False,False))[mask] for delta in (-1,0,1))
                        false[mask+1]+=penalty;removed[mask]+=not penalty
                miss=sum(1 for tt,i in recent if not any((tt+delta,i) in ev for delta in (-1,0,1)))
                for mask in range(3):ranked[mask].append((matches-.5*false[mask]-.5*miss,index))
            chosen=[[index for _,index in sorted(scores,key=lambda x:-x[0])[:ns['_V92_P_TOP']]] for scores in ranked]
            assert [candidates[i][1] for i in chosen[0]]==expected
            counters['exact_native_forecasts']+=1
            record=dict(step=step,selected=chosen[0],masks={})
            for mask,name in enumerate(plan['masks']):
                before=[candidates[i][1] for i in chosen[0]];after=[candidates[i][1] for i in chosen[mask+1]]
                changed=before!=after
                signals=[[any(ns['_hp_quantity'](ev,i,step,seen)>=ns['_V92_P_K'] for ev in group) for i in range(len(items))]
                         for group in (before,after)]
                counters[name+'_changed_rankings']+=changed
                counters[name+'_changed_signals']+=signals[0]!=signals[1]
                counters[name+'_removed_penalties']+=removed[mask]
                record['masks'][name]=dict(selected=chosen[mask+1],changed_rankings=changed,
                                         signals_before=signals[0],signals_after=signals[1],removed_library_penalties=removed[mask])
            rows.append(record)
        results.append(dict(episode=episode,policy=policy,snapshot_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),summary=dict(counters),forecasts=rows))
        print(json.dumps(dict(episode=episode,policy=policy,summary=dict(counters))),flush=True)
    target.write_text(json.dumps(dict(plan=plan,results=results,note='Repeated overlapping history windows are not independent evidence. Changed offline signals do not establish emitted action changes, accepted trades or competitive benefit.'),indent=2)+'\n')


if __name__=='__main__':main()
