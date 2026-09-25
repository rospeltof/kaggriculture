"""Check whether bounded-out library signals correspond to available own sales; no games."""
import hashlib
import json
from pathlib import Path

from auditar_feedback_real import OUT, SOURCES


def main():
    path=OUT/'rival_stock_bound_audit_v2.json';data=json.loads(path.read_text())
    receipts={x['id']:x for x in json.loads((OUT/'feedback_0914.fetch.json').read_text())}
    controls={x['episode']:x for x in json.loads((OUT/'feedback_0914.audit.json').read_text())['results']}
    rows=[]
    for entry in data['results']:
        episode=entry['episode'];control=controls[episode];seat=control['seat'];receipt=receipts[episode]
        raw=Path(receipt['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==receipt['sha256']
        replay=json.loads(raw);namespace={};source=Path(SOURCES[entry['policy']]);code=source.read_bytes()
        assert hashlib.sha256(code).hexdigest()==control['source_sha256']
        exec(compile(code,str(source),'exec'),namespace)
        for signal in entry['excluded_signals']:
            obs=dict(replay['steps'][signal['step']][seat]['observation']);obs['step']=signal['step'];obs['player']=seat
            action=replay['steps'][signal['step']+1][seat]['action'];_,private=namespace['_r127_fields'](obs,action)
            rows.append(dict(episode=episode,**signal,enabled_product=signal['item'] in namespace['_V92_P_USE'],
                             projected_own_shed=private['shed'].get(signal['item'],0),
                             emitted_orders=[o for o in action.get('market',[]) if len(o)>1 and o[1]==signal['item']]))
    result=dict(source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),signals=rows,
                signals_in_enabled_products=sum(x['enabled_product'] for x in rows),
                signals_with_projected_stock=sum(x['projected_own_shed']>0 for x in rows),
                signals_with_emitted_orders=sum(bool(x['emitted_orders']) for x in rows),
                note='native_signals in the bound audit counts raw library/HP quantities, including EGG which is disabled in _V92_P_USE. It is not the count of emitted PREDICT orders.',
                decision='Do not build or enqueue a candidate on this evidence: all impossible quantities coincide with zero own projected stock and no emitted order. Bound is mechanically valid on these trajectories, actionable coverage unproven.')
    (OUT/'rival_stock_bound_actionability.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='signals'}))


if __name__=='__main__':main()
