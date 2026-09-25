"""Audita predicciones sobre observaciones reales; no estima victorias contrafactuales."""
import contextlib
from copy import deepcopy
import io
import json
from pathlib import Path

OUT=Path('docs/evidencia/research_20260925')
SRC=Path('submission/main_publico_arshs3_arsgorynich.py')


def profile(meta):
    d=json.loads(Path(meta['path']).read_text());me=d['info']['TeamNames'].index('Rospel')
    ns={};exec(compile(SRC.read_bytes(),str(SRC),'exec'),ns)
    entry=[v for v in ns.values() if callable(v)][-1]
    parent=ns['_v92_predict'];events=[];diff=0;diff_examples=[]
    def traced(obs,action,state):
        before=deepcopy(action);out=parent(obs,action,state)
        if out!=before:
            step=int(obs['step']);best=state.get('best') or []
            for order in out.get('market',[]):
                if order not in before.get('market',[]) and order[0]=='SELL':
                    item=order[1];idx=ns['_V92_P_ITEMS'].index(item)
                    ev=best[0] if best else {}
                    prior=[k for k,q in ev.items() if step-240<=k[0]<step-1 and k[1]==idx and q>=2]
                    seen=state['obs'];hits=sum(any((t+dt,i) in seen for dt in (-1,0,1)) for t,i in prior)
                    events.append(dict(step=step,item=item,qty=order[2],prior_count=len(prior),prior_hits=hits))
        return out
    ns['_v92_predict']=traced
    with contextlib.redirect_stdout(io.StringIO()):
        for t in range(719):
            obs=deepcopy(d['steps'][t][me]['observation']);obs['step']=t;obs['player']=me
            action=entry(obs,d['configuration'])
            if action!=d['steps'][t+1][me]['action']:
                diff+=1
                if len(diff_examples)<3:diff_examples.append(dict(step=t,generated=action,recorded=d['steps'][t+1][me]['action']))
    seen=ns['_V92_P'][me]['obs']
    for e in events:
        i=ns['_V92_P_ITEMS'].index(e['item'])
        e['future_net_sale_4']=any((e['step']+dt,i) in seen for dt in range(1,5))
    result=dict(id=meta['id'],source=meta['source'],reconstructed_action_differences=diff,
                events=events,forecast_stats=ns['_V92_P_REPORT'],hp_stats=ns['_HP_STATS'],diff_examples=diff_examples)
    return result


if __name__=='__main__':
    selection=json.loads((OUT/'replay_selection.json').read_text())['files']
    rows=[]
    for meta in [m for m in selection if m['source']=='arshs3'][:4]:
        r=profile(meta);rows.append(r)
        e=r['events'];print(r['id'],'action differences',r['reconstructed_action_differences'],
            'events',len(e),'future hits',sum(x['future_net_sale_4'] for x in e),'stats',r['forecast_stats'],flush=True)
    (OUT/'forecast_probe.json').write_text(json.dumps(rows,indent=2)+'\n')
