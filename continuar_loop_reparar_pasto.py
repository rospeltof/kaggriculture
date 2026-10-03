"""Loop33: repair missing animal structures on both submitted policies."""
import hashlib
import json
from pathlib import Path
import time

import continuar_loop_publicos as loop
from continuar_loop_adelanto_trigo import changed_seeds
from continuar_loop_panel_cercano import analyze, verify_sources


def main():
    validation=json.loads((loop.OUT/'animal_build_validation.json').read_text())
    candidates=json.loads((loop.OUT/'animal_build_variants.json').read_text())
    panel=json.loads((loop.OUT/'close_panel_manifest.json').read_text())
    assert validation['passed'] and validation['competitive_ready']
    assert validation['candidate_hashes']=={n:r['sha256'] for n,r in candidates.items()}
    verify_sources(panel)
    for spec in candidates.values():
        assert hashlib.sha256(Path(spec['path']).read_bytes()).hexdigest()==spec['sha256']
    print('Loop33 mechanics and frozen sources verified; waiting for loop32.',flush=True)
    while True:
        try:state=json.loads(loop.STATE.read_text())
        except (FileNotFoundError,json.JSONDecodeError):state={}
        if state.get('state')=='failed':raise RuntimeError(state)
        if state.get('phase')=='thirty_two_rounds_complete':break
        time.sleep(5)
    verify_sources(panel)
    for spec in candidates.values():
        assert hashlib.sha256(Path(spec['path']).read_bytes()).hexdigest()==spec['sha256']
    loop.BASE=panel['controls']['base']['path'];control=panel['controls']['top3']['path']
    assert panel['controls']['base']['sha256']==validation['base_hash']
    assert panel['controls']['top3']['sha256']==validation['control_hash']
    variants={n:r['path'] for n,r in candidates.items()}
    pool={n:r['path'] for n,r in panel['pilot_pool'].items()}
    prefix=loop.run('pilot33',dict(variants,top3=control),1087000,16,pool)
    report=analyze(prefix,variants,control,2)
    (loop.OUT/'pilot33.results.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    selected=report['selected_for_confirmation'];result=None
    if selected:
        chosen={n:variants[n] for n in selected}
        expanded=dict(pool,**{n:r['path'] for n,r in panel['confirm_extra'].items()})
        prefix=loop.run('confirm33',dict(chosen,top3=control),1088000,32,expanded)
        result=analyze(prefix,chosen,control,0)
        for name in chosen:
            row=result['results'][name]
            row['changed_seeds_vs_parent']=changed_seeds(prefix,name,candidates[name]['behavior_reference'],chosen)
            eligible=(row['delta_points']>=3 and row['versus_top3']['delta_points']>=0
                      and min(row['opponent_breakdown'].values())>=-20
                      and min(row['versus_top3']['opponent_breakdown'].values())>=-20
                      and len(row['changed_seeds_vs_parent'])>=2)
            row['registered_submission_gate']=eligible
            if eligible:row['status']='REAL_WORLD_CANDIDATE_REVIEW_REQUIRED'
        (loop.OUT/'confirm33.results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    loop.save('thirty_three_rounds_complete',state='complete',pilot33=report,confirm33=result,
              next_action='Review constructed structures, executed animal placement and care, production and shop changes, both references and alternate hash sensitivity. No automatic upload; continue research.')


if __name__=='__main__':
    try:main()
    except BaseException as exc:
        loop.save('loop33_failed',state='failed',error=repr(exc));raise
