"""Compara hashes de acciones propias/rivales en las mismas celdas del pool."""
import argparse
import json
from pathlib import Path

from validar_torneo import validate


def main(prefix):
    prefix=Path(prefix);validate(str(prefix))
    meta=json.loads(Path(str(prefix)+'.meta.json').read_text())
    rows=[json.loads(line) for line in Path(str(prefix)+'.jsonl').read_text().splitlines()]
    keyed={(r['a'],r['b'],r['seed'],r['seat']):r for r in rows}
    arms=meta['vs'].split(',');report={}
    for arm in arms:
        if arm in ('base','noop'):continue
        pairs=[(r,keyed[arm,r['b'],r['seed'],r['seat']]) for r in rows if r['a']=='base' and r['b'] not in arms]
        changed=[(a,b) for a,b in pairs if a['action_hashes'][a['seat']]!=b['action_hashes'][b['seat']]]
        report[arm]=dict(pool_episodes=len(pairs),own_action_hash_changed=len(changed),
            opponent_action_hash_changed=sum(a['action_hashes'][1-a['seat']]!=b['action_hashes'][1-b['seat']] for a,b in pairs),
            changed_seeds=sorted({a['seed'] for a,b in changed}),
            changed_cells=[dict(opponent=a['b'],seed=a['seed'],seat=a['seat'],base_score=a['score'],candidate_score=b['score']) for a,b in changed])
    Path(str(prefix)+'.behavior.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:{a:b for a,b in v.items() if a!='changed_cells'} for k,v in report.items()},indent=2))
    return report


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('prefix');args=ap.parse_args();main(args.prefix)
