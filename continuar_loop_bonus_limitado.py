"""Round17: cap-aware food valuation after the registered initial-herd block."""
import hashlib
import json
from pathlib import Path
import time

import continuar_loop_publicos as loop


def main():
    decision=json.loads((loop.OUT/'capped_bonus_decision.json').read_text())
    if not decision['competitive_ready']:
        raise RuntimeError('Loop17 stopped in development; do not launch the registered pilot.')
    while True:
        try:state=json.loads(loop.STATE.read_text())
        except (FileNotFoundError,json.JSONDecodeError):state={}
        if state.get('state')=='failed':raise RuntimeError(state)
        if state.get('phase')=='sixteen_rounds_complete':break
        time.sleep(5)
    validation=json.loads((loop.OUT/'capped_bonus_validation.json').read_text())
    manifest=json.loads((loop.OUT/'capped_bonus_variants.json').read_text())
    assert validation['passed']
    assert validation['candidate_hashes']=={n:r['sha256'] for n,r in manifest.items()}
    for name,spec in manifest.items():
        assert hashlib.sha256(Path(spec['path']).read_bytes()).hexdigest()==spec['sha256'],name
    loop.BASE='submission/main_publico_arshs3_vq_top3.py'
    variants={n:r['path'] for n,r in manifest.items()}
    pool={n:p for n,p in {**loop.POOL,**loop.EXTRA}.items() if n in ('arshs3','tds','hybu','ars40')}
    prefix=loop.run('pilot17',variants,1040000,16,pool)
    report=loop.analyze(prefix,variants,2,lambda n:'capped',2)
    result=loop.confirmation('confirm17',report['selected_for_confirmation'],variants,1041000)
    loop.save('seventeen_rounds_complete',state='complete',pilot17=report,confirm17=result,
              next_action='Review marginal food value, physical consumption, W/L/T and real feedback; continue research. Goal remains active.')


if __name__=='__main__':
    try:main()
    except BaseException as exc:
        # A deliberately stopped prototype must not overwrite a different
        # active tournament's pipeline state.
        print(repr(exc),flush=True);raise
