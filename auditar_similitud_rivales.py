"""Descriptive action similarity in already selected and reproduced real games."""
from collections import Counter
import hashlib
import json
from pathlib import Path

OUT=Path('docs/evidencia/loop_publicos_20260925')


def main():
    target=OUT/'recent_rival_similarity.json';assert not target.exists()
    old=json.loads((OUT/'forecast_pair_replays_0653.json').read_text())['episodes']
    current=json.loads((OUT/'feedback_0742.audit.json').read_text())['results']
    fetched={r['id']:r for r in json.loads((OUT/'feedback_0742.fetch.json').read_text())}
    inputs=[dict(episode=r['episode'],policy=r['real_policy'],path=r['replay'],sha256=r['replay_sha256']) for r in old]
    inputs += [dict(episode=r['episode'],policy=r['policy'],path=fetched[r['episode']]['path'],sha256=r['replay_sha256']) for r in current]
    assert len({r['episode'] for r in inputs})==len(inputs)==15
    plan=dict(rule='All 15 already recency-selected and exactly reproduced games from0653/0742; no outcome selection. Action similarity is descriptive, not code identification, independent policy count or causal explanation.',inputs=inputs)
    (OUT/'recent_rival_similarity.plan.json').write_text(json.dumps(plan,indent=2)+'\n')
    results=[]
    for item in inputs:
        raw=Path(item['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==item['sha256']
        replay=json.loads(raw);seat=replay['info']['TeamNames'].index('Rospel');assert replay['info']['TeamNames'].count('Rospel')==1
        count=Counter();buys=[[],[]]
        for step in range(719):
            commands=[];markets=[]
            for side,player in enumerate((seat,1-seat)):
                action=replay['steps'][step+1][player]['action']
                commands.append([action.get('farmer') or ['PASS'],*(action.get('hands') or [])])
                markets.append(action.get('market') or [])
                for order in markets[-1]:
                    if len(order)>=3 and order[:2]==['BUY_PRODUCT','WHEAT'] and order[2]>=20:
                        buys[side].append((step,int(order[2])))
            n=min(map(len,commands));count['paired_actor_commands']+=n
            count['same_actor_commands']+=sum(a==b for a,b in zip(*commands))
            count['same_actor_count_turns']+=len(commands[0])==len(commands[1])
            count['same_whole_unit_turns']+=commands[0]==commands[1]
            count['same_farmer_turns']+=commands[0][0]==commands[1][0]
            count['same_market_turns']+=markets[0]==markets[1]
            count['either_market_active_turns']+=bool(markets[0] or markets[1])
            count['same_active_market_turns']+=bool(markets[0] or markets[1]) and markets[0]==markets[1]
        other=set(buys[1])
        matches={str(offset):sum((step+offset,q) in other for step,q in buys[0]) for offset in (-1,0,1)}
        row=dict(**item,opponent=replay['info']['TeamNames'][1-seat],seed=replay['info']['seed'],seat=seat,
            margin=replay['rewards'][seat]-replay['rewards'][1-seat],counts=dict(count),
            unit_command_agreement_pct=100*count['same_actor_commands']/count['paired_actor_commands'],
            whole_unit_turn_agreement_pct=100*count['same_whole_unit_turns']/719,
            active_market_agreement_pct=100*count['same_active_market_turns']/max(1,count['either_market_active_turns']),
            large_wheat_orders=[len(x) for x in buys],same_quantity_wheat_buy_offset_matches=matches)
        results.append(row)
        print(json.dumps({k:row[k] for k in ('episode','opponent','margin','unit_command_agreement_pct','whole_unit_turn_agreement_pct','active_market_agreement_pct','large_wheat_orders','same_quantity_wheat_buy_offset_matches')}),flush=True)
    target.write_text(json.dumps(dict(plan=plan,results=results),indent=2)+'\n')


if __name__=='__main__':main()
