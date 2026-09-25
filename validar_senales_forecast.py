"""Reconstruye ventas aceptadas reales; incluye competencia en el mismo turno."""
from collections import Counter
from copy import deepcopy
import gzip
import json
from pathlib import Path

from investigar_lider import compact_state
from sonda_fallo_forecast import run

OUT=Path('docs/evidencia/research_20260925')


if __name__=='__main__':
    selection=json.loads((OUT/'replay_selection.json').read_text())['files']
    by_id={r['id']:r for r in selection}
    probes=json.loads((OUT/'forecast_probe.json').read_text());results=[]
    for probe in probes:
        meta=by_id[probe['id']];replay=json.loads(Path(meta['path']).read_text())
        me=replay['info']['TeamNames'].index('Rospel');opp=1-me
        def tape(player):
            def agent(obs):return deepcopy(replay['steps'][int(obs['step'])+1][player]['action'])
            return agent
        env,ledger=run(tape(me),tape(opp),replay['info']['seed'],me)
        assert all(compact_state(a)==compact_state(b) for a,b in zip(replay['steps'],env.steps))
        sales=Counter((r['step'],r['item']) for r in ledger if r['player']==opp and r['op']=='SELL')
        events=[]
        for event in probe['events']:
            t,i=event['step'],event['item']
            events.append(dict(**event,same_turn_accepted=sales[t,i],
                next4_accepted=sum(sales[t+dt,i] for dt in range(1,5)),
                now_or_next4_accepted=sum(sales[t+dt,i] for dt in range(5))))
        summary=dict(id=probe['id'],states_exact=720,events=events,
            same_turn_hits=sum(e['same_turn_accepted']>0 for e in events),
            next4_hits=sum(e['next4_accepted']>0 for e in events),
            now_or_next4_hits=sum(e['now_or_next4_accepted']>0 for e in events))
        results.append(summary)
        (OUT/f"real_{probe['id']}.ledger.jsonl.gz").write_bytes(gzip.compress(('\n'.join(json.dumps(r) for r in ledger)+'\n').encode(),mtime=0))
        print(probe['id'],len(events),'mismo turno',summary['same_turn_hits'],'ahora o próximos 4',summary['now_or_next4_hits'],flush=True)
    (OUT/'forecast_signals_validated.json').write_text(json.dumps(results,indent=2)+'\n')
