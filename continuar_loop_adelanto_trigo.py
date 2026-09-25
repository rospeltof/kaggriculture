"""Loop24: earlier native purchases with VQ primary and top3 control."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import time

import continuar_loop_publicos as loop

CONTROL='submission/main_publico_arshs3_vq_top3.py'


def analyze(prefix,candidates,limit):
    report=loop.analyze(prefix,dict(candidates,top3=CONTROL),0,lambda n:n,0)
    report['results']['top3']['status']='DIAGNOSTIC_CONTROL_ONLY'
    report['selected_for_confirmation']=sorted((n for n in candidates if report['results'][n]['delta_points']>0),
        key=lambda n:(-report['results'][n]['delta_points'],n))[:limit]
    for name in candidates:
        captured=io.StringIO()
        with contextlib.redirect_stdout(captured):
            row=loop.paired(str(prefix)+'.jsonl','top3',name,','.join(['base','noop',*(n for n in candidates if n!=name)]))
        report['results'][name]['versus_top3']=row
        Path(str(prefix)+f'.{name}.versus_top3.txt').write_text(captured.getvalue())
    return report


def changed_seeds(prefix,name,parent,candidates):
    rows=[json.loads(l) for l in Path(str(prefix)+'.jsonl').read_text().splitlines()]
    indexed={(r['a'],r['b'],r['seed'],r['seat']):r for r in rows}
    excluded={'base','noop','top3',*candidates}
    changed=set()
    for row in rows:
        if row['a']!=name or row['b'] in excluded:continue
        ref=indexed[parent,row['b'],row['seed'],row['seat']]
        if row['action_hashes'][row['seat']]!=ref['action_hashes'][ref['seat']]:changed.add(row['seed'])
    return sorted(changed)


def main():
    while True:
        try:state=json.loads(loop.STATE.read_text())
        except (FileNotFoundError,json.JSONDecodeError):state={}
        if state.get('state')=='failed':raise RuntimeError(state)
        if state.get('phase')=='twenty_three_rounds_complete':break
        time.sleep(5)
    validation=json.loads((loop.OUT/'advance_wheat_validation.json').read_text())
    manifest=json.loads((loop.OUT/'advance_wheat_variants.json').read_text())
    fresh=json.loads((loop.OUT/'public_0548_variants.json').read_text())
    assert validation['passed'] and validation['competitive_ready']
    assert validation['candidate_hashes']=={n:r['sha256'] for n,r in manifest.items()}
    for name,spec in {**manifest,**fresh}.items():
        assert hashlib.sha256(Path(spec['path']).read_bytes()).hexdigest()==spec['sha256'],name
    assert hashlib.sha256(Path(CONTROL).read_bytes()).hexdigest()==validation['control_hash']
    loop.BASE='submission/main_publico_arshs3_vq.py'
    assert hashlib.sha256(Path(loop.BASE).read_bytes()).hexdigest()=='9b463dfb8076b4c63946e1ae4249cd1cfc3cc58b63115cf2bd5b00f96f188976'
    variants={n:r['path'] for n,r in manifest.items()}
    pool={n:p for n,p in {**loop.POOL,**loop.EXTRA}.items() if n in ('arshs3','tds','hybu','ars40')}
    pool.update({n:r['path'] for n,r in fresh.items()})
    prefix=loop.run('pilot24',dict(variants,top3=CONTROL),1061000,32,pool)
    report=analyze(prefix,variants,2)
    (loop.OUT/'pilot24.results.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    selected=report['selected_for_confirmation'];result=None
    if selected:
        chosen={n:variants[n] for n in selected};expanded={**loop.POOL,**loop.EXTRA,**{n:r['path'] for n,r in fresh.items()}}
        prefix=loop.run('confirm24',dict(chosen,top3=CONTROL),1062000,32,expanded)
        result=analyze(prefix,chosen,0)
        for name in chosen:
            row=result['results'][name];parent='base' if manifest[name]['config']['parent']=='vq' else 'top3'
            row['changed_seeds_vs_parent']=changed_seeds(prefix,name,parent,chosen)
            improves_parent=parent=='base' or row['versus_top3']['delta_points']>0
            eligible=(row['delta_points']>=3 and min(row['opponent_breakdown'].values())>=-20
                      and row['versus_top3']['delta_points']>=0 and improves_parent
                      and len(row['changed_seeds_vs_parent'])>=2)
            row['registered_submission_gate']=eligible
            if eligible:row['status']='REAL_WORLD_CANDIDATE'
        (loop.OUT/'confirm24.results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    loop.save('twenty_four_rounds_complete',state='complete',pilot24=report,confirm24=result,
        next_action='Review actual prebuys/native repayment, induced earlier sales, physical changes and both submitted parents; continue autonomous research. No automatic submission.')


if __name__=='__main__':
    try:main()
    except BaseException as exc:
        loop.save('loop24_failed',state='failed',error=repr(exc));raise
