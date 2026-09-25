"""Audita la evidencia del torneo existente: no ejecuta partidas."""
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
import tarfile


def validate(prefix,ref='base',noop='noop'):
    meta=json.loads(Path(prefix+'.meta.json').read_text())
    assert meta['state']=='complete','No analizar torneo incompleto'
    rows=[json.loads(l) for l in Path(prefix+'.jsonl').read_text().splitlines()]
    agents=meta['agentes'];arms=meta['vs'].split(',') if meta['vs'] else None
    pairs=[(a,b) for a,b in itertools.combinations(agents,2) if arms is None or a in arms or b in arms]
    if arms:pairs=[(a,b) if a in arms else (b,a) for a,b in pairs]
    expected={(a,b,s,p) for a,b in pairs for s in meta['seeds'] for p in (0,1)}
    keyed={(r['a'],r['b'],r['seed'],r['seat']):r for r in rows}
    assert set(keyed)==expected and len(rows)==len(expected)==meta['expected_episodes']==meta['completed_episodes']
    normalized={}
    for r in rows:
        assert r['valid'] and r['n_err']==0 and not r['errors'] and r['statuses']==['DONE','DONE']
        assert r['steps']==720 and r['action_counts']==[719,719]
        assert len(r['action_hashes'])==2 and all(len(h)==64 for h in r['action_hashes'])
        assert all(math.isfinite(v) for v in r['rewards'])
        mine,theirs=r['rewards'][r['seat']],r['rewards'][1-r['seat']]
        assert r['score']==(1 if mine>theirs else 0 if mine<theirs else .5)
        assert r['margin']==mine-theirs
        normalized[r['a'],r['b'],r['seed'],r['seat']]=r
        normalized[r['b'],r['a'],r['seed'],1-r['seat']]=r
    controls=0
    if ref in agents and noop in agents:
        for o in set(agents)-{ref,noop}:
            for s,p in itertools.product(meta['seeds'],(0,1)):
                a,b=normalized[ref,o,s,p],normalized[noop,o,s,p]
                assert all(a[k]==b[k] for k in ('rewards','statuses','steps','action_hashes','action_counts')),(o,s,p)
                controls+=1
    with tarfile.open(prefix+'.sources.tgz') as archive:
        src=archive.extractfile('torneo.py').read()
        assert hashlib.sha256(src).hexdigest()==meta['runner_sha256']
        for name,info in agents.items():
            src=archive.extractfile('agents/'+name+'.py').read()
            assert hashlib.sha256(src).hexdigest()==info['sha256']
    result=dict(complete_coverage=True,episodes=len(rows),noop_exact=controls,archived_hashes_verified=True)
    Path(prefix+'.validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
    return result


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('prefix');a=ap.parse_args()
    validate(a.prefix)
