"""Public-only upper bound on rival animal products; private state used only as audit truth."""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from auditar_feedback_real import OUT, SOURCES

PRODUCTS={'COW':'MILK','SHEEP':'WOOL','GOOSE':'EGG'}
CAP={'COW':6,'SHEEP':6,'GOOSE':4}


def public_update(upper, previous, current, own_action, seat, step, draw):
    """Inputs are public observations plus our own last emitted action, never rival private/actions."""
    rival=1-seat;before=previous['farms'][rival];after=current['farms'][rival]
    positions={tuple(x) for x in [before['farmer'],*before['hands']]}
    possible=Counter()
    for x,y in positions:
        tile=before['tiles'][y][x];new=after['tiles'][y][x]
        if not isinstance(tile,dict) or tile.get('animal') not in PRODUCTS:continue
        q=max(0,int(tile.get('yield_units',0)))
        if not q:continue
        # At night harvest can be hidden by new production; keep all possible harvests.
        changed=(not isinstance(new,dict) or new.get('animal')!=tile['animal'] or int(new.get('yield_units',0))<q)
        if step%24==23 or changed:possible[PRODUCTS[tile['animal']]]+=q
    requested=Counter()
    for order in (own_action.get('market') or [])[:10]:
        if len(order)>=3 and order[0]=='SELL' and order[1] in PRODUCTS.values():
            requested[order[1]]+=max(0,int(order[2]))
    lows={}
    for item in PRODUCTS.values():
        inv=int(current['market']['inventory'][item]);old=int(previous['market']['inventory'][item])
        # If the market is empty, consumption may have been truncated. Zero remains a valid lower bound.
        added=max(0,inv+int(draw.get(item,0))-old) if inv>0 else 0
        lows[item]=max(0,added-requested[item])
        upper[item]=max(0,upper[item]+possible[item]-lows[item])
    return dict(harvest_upper=dict(possible),rival_sales_lower=lows)


def future_upper(upper,public,seat,step,horizon=4):
    result=Counter(upper);night=(step+horizon)//24>step//24
    for row in public['farms'][1-seat]['tiles']:
        for tile in row:
            if not isinstance(tile,dict) or tile.get('animal') not in PRODUCTS:continue
            kind=tile['animal'];result[PRODUCTS[kind]]+=max(0,int(tile.get('yield_units',0)))
            if night:result[PRODUCTS[kind]]+=CAP[kind]
    return dict(result)


def main():
    dest=OUT/'rival_stock_bound_audit.json';plan_path=OUT/'rival_stock_bound_audit.plan.json'
    assert not dest.exists() and not plan_path.exists()
    source=OUT/'forecast_censor_audit.json';ranking=json.loads(source.read_text())
    receipts={r['id']:r for r in json.loads((OUT/'feedback_0914.fetch.json').read_text())}
    controls={r['episode']:r for r in json.loads((OUT/'feedback_0914.audit.json').read_text())['results']}
    plan=dict(created_at=datetime.now(timezone.utc).isoformat(),episodes=[r['episode'] for r in ranking['results']],
              rule='All six exact-source0914 trajectories, no outcome filter. Upper bound from public animal yield decreases/actor positions, conservative night ambiguity, and lower bound on rival visible sales after subtracting our requested final sales. No candidate policy, games, thresholds fitted or private data used by estimator.',
              future_bound='Current off-field upper + every visible animal yield + maximum held per animal if next four steps cross a night. New animals cannot first produce within four steps.',
              checks='At every observation upper >= actual rival shed+bags for MILK/WOOL/EGG; forward bound >= actual rival sales in next four forecast steps. Private inventory/ledger only audit assertions.',
              source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    plan_path.write_text(json.dumps(plan,indent=2)+'\n');results=[]
    for rr in ranking['results']:
        episode=rr['episode'];policy=rr['policy'];control=controls[episode];seat=control['seat'];raw=Path(receipts[episode]['path']).read_bytes()
        assert hashlib.sha256(raw).hexdigest()==receipts[episode]['sha256']
        replay=json.loads(raw);ns={};code=Path(SOURCES[policy]).read_bytes();assert hashlib.sha256(code).hexdigest()==control['source_sha256'];exec(compile(code,SOURCES[policy],'exec'),ns)
        import gzip
        snaps=[json.loads(l) for l in gzip.decompress((OUT/f'feedback_0914.attribution.{episode}.snapshots.jsonl.gz').read_bytes()).splitlines()]
        ledger=[json.loads(l) for l in gzip.decompress((OUT/f'feedback_0914.{episode}.ledger.jsonl.gz').read_bytes()).splitlines()]
        rival_sales=Counter((e['step'],e['item']) for e in ledger if e['player']==1-seat and e['op']=='SELL')
        forecasts={r['step']:r for r in rr['forecasts']};seen={};upper=Counter();stats=Counter();signals=[];bounds=[]
        for step in range(719):
            obs=replay['steps'][step][seat]['observation'];public={k:obs[k] for k in ('farms','market','town')}
            if step:
                prior=replay['steps'][step-1][seat]['observation'];prev={k:prior[k] for k in ('farms','market','town')}
                details=public_update(upper,prev,public,replay['steps'][step][seat]['action'],seat,step-1,ns['_v9_town_draw'](prev['town']['unlocked_shops'],step-1))
                for i,item in enumerate(ns['_V92_P_ITEMS']):
                    q=snaps[step]['inference_previous'][item]
                    if q is not None:seen[step-1,i]=q
            actual_private=replay['steps'][step][1-seat]['observation']['private']
            actual=Counter(actual_private['shed'])
            for bag in actual_private['inventories']:actual.update(bag)
            supply=future_upper(upper,public,seat,step)
            for item in PRODUCTS.values():
                stats['inventory_checks']+=1
                assert upper[item]>=actual[item],(episode,step,item,upper[item],actual[item])
                stats['exact_inventory_bounds']+=upper[item]==actual[item]
                sold=sum(rival_sales[step+dt,item] for dt in range(1,5))
                assert supply[item]>=sold,(episode,step,item,supply[item],sold)
                stats['forward_checks']+=1
            bounds.append(dict(step=step,off_field_upper=dict(upper),actual_rival_stock={p:actual[p] for p in PRODUCTS.values()},four_step_upper=supply))
            if step not in forecasts:continue
            forecast=forecasts[step];candidates=ns['_v92_p_pair'](tuple(obs['town']['unlocked_shops'][:2]));best=[candidates[i][1] for i in forecast['selected']]
            for item in PRODUCTS.values():
                i=ns['_V92_P_ITEMS'].index(item);pred=max((ns['_hp_quantity'](ev,i,step,seen) for ev in best),default=0)
                if pred<ns['_V92_P_K']:continue
                stats['native_signals']+=1
                constrained=supply[item]<ns['_V92_P_K'];stats['impossible_threshold_signals']+=constrained
                if constrained:signals.append(dict(step=step,item=item,predicted=pred,supply_upper=supply[item],actual_next_four_sales=sum(rival_sales[step+dt,item] for dt in range(1,5))))
        row=dict(episode=episode,policy=policy,summary=dict(stats),excluded_signals=signals,bounds=bounds)
        results.append(row);print(json.dumps(dict(episode=episode,policy=policy,summary=dict(stats))),flush=True)
    dest.write_text(json.dumps(dict(plan=plan,results=results,note='A proven upper bound only identifies impossible signal quantities in these observations. It does not prove changed actions or benefit from gating them.'),indent=2)+'\n')


if __name__=='__main__':main()
