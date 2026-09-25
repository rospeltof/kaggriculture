"""Require physical initial compositions, exact noop and reconciled animal costs."""
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import tarfile

OUT=Path('docs/evidencia/loop_publicos_20260925')


def main():
    plan=json.loads((OUT/'initial_herd_smoke.plan.json').read_text())
    rows=json.loads((OUT/'initial_herd_smoke.json').read_text())
    manifest=json.loads((OUT/'initial_herd_variants.json').read_text())
    with tarfile.open(OUT/'initial_herd_smoke.sources.tgz','r:gz') as tar:
        for name,spec in plan['agents'].items():
            assert hashlib.sha256(tar.extractfile(name+'.py').read()).hexdigest()==spec['sha256']
            assert hashlib.sha256(Path(spec['path']).read_bytes()).hexdigest()==spec['sha256']
            if name in manifest:assert manifest[name]['sha256']==spec['sha256']
        assert hashlib.sha256(tar.extractfile('opponent.py').read()).hexdigest()==plan['opponent_sha256']
    keyed={(r['arm'],r['seed'],r['seat']):r for r in rows}
    expected={(a,s,p) for a in plan['agents'] for s in plan['seeds'] for p in plan['seats']}
    assert len(keyed)==len(rows)==48 and set(keyed)==expected
    summary=[]
    for seed in plan['seeds']:
        for seat in plan['seats']:
            base=keyed['base',seed,seat];noop=keyed['initial_noop',seed,seat]
            assert (base['action_hash'],base['rewards'])==(noop['action_hash'],noop['rewards'])
            for arm,spec in manifest.items():
                row=keyed[arm,seed,seat];cfg=spec['config']
                ledger=[json.loads(l) for l in gzip.decompress((OUT/f'initial_herd_smoke.{seed}.{arm}.{seat}.ledger.jsonl.gz').read_bytes()).decode().splitlines()]
                buys=[e for e in ledger if e['player']==seat and e['step']==1 and e['op']=='BUY_ANIMAL']
                composition=Counter(COW=2,SHEEP=2);composition[cfg['source']]-=cfg['qty'];composition[cfg['target']]+=cfg['qty']
                assert Counter(e['item'] for e in buys)==composition
                assert sum(e['value'] for e in buys)==-400*composition['COW']-500*composition['SHEEP']
                assert Counter(e['animal'] for e in row['initial_animals'])==composition
                assert all(e['placed_day']==0 for e in row['initial_animals'])
                assert {(e['x'],e['y']) for e in row['initial_animals']}=={(e['x'],e['y']) for e in base['initial_animals']}
                assert not any(row['checkpoints']['24']['credit'].values()) and not row['checkpoints']['24']['pending']
                assert len(row['reports']['_IH_REPORT']['events'])==1 and not row['reports']['_IH_REPORT']['declined']
                assert not any(v for report in row['reports'].values() for k,v in report.items() if 'error' in k and isinstance(v,(int,float)))
                private=row['terminal_private'];assert sum(private['shed'].values())+sum(sum(b.values()) for b in private['inventories'])==0
                summary.append(dict(seed=seed,seat=seat,arm=arm,composition=dict(composition),
                                    initial_animal_cost=-sum(e['value'] for e in buys),changed_action_turns=row['changed_action_turns'],
                                    same_shops=row['shops']==base['shops'],harvested_base=base['harvested'],harvested_candidate=row['harvested'],
                                    escapes_base=base['escapes'],escapes_candidate=row['escapes']))
    report=dict(passed=True,development_games=48,noop_exact_turns=8*719,max_turn_ms=max(r['max_turn_ms'] for r in rows),
                candidate_hashes={n:r['sha256'] for n,r in manifest.items()},summary=summary,
                note='Correct accepted initial composition and costs do not imply higher W/L; later adaptive routes/shops may change.')
    assert report['max_turn_ms']<1000
    (OUT/'initial_herd_validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
