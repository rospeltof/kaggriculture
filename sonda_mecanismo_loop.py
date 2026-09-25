"""Reproduce una celda de cambio W/L/T o acciones y concilia transacciones."""
import argparse
from collections import defaultdict
import gzip
import json
from pathlib import Path

from sonda_fallo_forecast import run


def main(prefix,candidate,direction,tag='mechanism'):
    prefix=Path(prefix);meta=json.loads(Path(str(prefix)+'.meta.json').read_text())
    assert meta['state']=='complete'
    rows=[json.loads(l) for l in Path(str(prefix)+'.jsonl').read_text().splitlines()]
    arms=meta['vs'].split(',');keyed={(r['a'],r['b'],r['seed'],r['seat']):r for r in rows}
    selected=[]
    for r in rows:
        if r['a']!='base' or r['b'] in arms:continue
        c=keyed[candidate,r['b'],r['seed'],r['seat']]
        changed=r['action_hashes'][r['seat']]!=c['action_hashes'][c['seat']]
        if (direction==0 and changed) or (c['score']-r['score'])*direction>0:
            selected.append((r['b'],r['seed'],r['seat']))
    opponent,seed,seat=sorted(selected)[0];envs=[];ledgers=[];telemetry=[]
    for arm in ('base',candidate):
        path=Path(meta['agentes'][arm]['ruta']);ns={}
        exec(compile(path.read_bytes(),str(path),'exec'),ns)
        entry=[v for v in ns.values() if callable(v)][-1]
        env,ledger=run(entry,meta['agentes'][opponent]['ruta'],seed,seat)
        assert [s.reward for s in env.steps[-1]]==keyed[arm,opponent,seed,seat]['rewards']
        envs.append(env);ledgers.append(ledger)
        telemetry.append({k:ns[k] for k in ('_V92_P_REPORT','_HP_STATS','_CA_REPORT','_RP_REPORT','_RT_REPORT','_HE_REPORT','_HD2_REPORT','_CXTB_REPORT','_V219_REPORT','_V233_REPORT','_IF_REPORT','_PM_REPORT','_EC_REPORT','_Y_REPORT','_R85_REPORT','_NF_REPORT','_LB_REPORT') if k in ns})
        dest=Path(str(prefix)+f'.{candidate}.{tag}.{arm}.ledger.jsonl.gz')
        if dest.exists():raise FileExistsError(dest)
        dest.write_bytes(gzip.compress(('\n'.join(json.dumps(r) for r in ledger)+'\n').encode(),mtime=0))
    b,c=envs;different=[t for t in range(719) if b.steps[t+1][seat].action!=c.steps[t+1][seat].action]
    first=different[0];sales=[]
    for ledger in ledgers:
        products=defaultdict(lambda:[0,0])
        for r in ledger:
            if r['player']==seat and r['op']=='SELL':products[r['item']][0]+=1;products[r['item']][1]+=r['value']
        sales.append(dict(products))
    rule=('First sorted opponent/seed/seat with a changed own action hash; no outcome filter, mechanism only'
          if direction==0 else 'First sorted opponent/seed/seat with WLT improvement or regression; mechanism only')
    report=dict(candidate=candidate,direction=direction,rule=rule,
        opponent=opponent,seed=seed,seat=seat,first_difference=first,changed_action_turns=len(different),
        first_actions=[e.steps[first+1][seat].action for e in envs],first_market=b.steps[first][0].observation.market,
        final_rewards=[[s.reward for s in e.steps[-1]] for e in envs],own_sale_units_cash=sales,
        telemetry=telemetry,shops_preserved=all(x[0].observation.town==y[0].observation.town for x,y in zip(*[e.steps for e in envs])))
    Path(str(prefix)+f'.{candidate}.{tag}.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('prefix');ap.add_argument('candidate');ap.add_argument('--direction',type=int,choices=(-1,0,1),default=1)
    ap.add_argument('--tag',default='mechanism')
    a=ap.parse_args();main(a.prefix,a.candidate,a.direction,a.tag)
