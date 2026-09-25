"""Prueba registrada de cobertura de reparación, después de las rondas anteriores."""
import json
from pathlib import Path
import statistics
import time

from scipy.stats import t as tdist
from continuar_loop_publicos import OUT, STATE, EXTRA, run, save
from validar_torneo import validate


def main():
    while True:
        try:s=json.loads(STATE.read_text())
        except (FileNotFoundError,json.JSONDecodeError):s={}
        if s.get('state')=='failed':raise RuntimeError(s)
        if s.get('phase')=='three_rounds_complete':break
        time.sleep(5)
    path=json.loads((OUT/'recovery_variants.json').read_text())['recover_now']['path']
    prefix=run('recovery_coverage',{'recover_now':path},1003000,32,{'arshs3':EXTRA['arshs3']})
    validate(str(prefix));meta=json.loads(Path(str(prefix)+'.meta.json').read_text())
    rows=[json.loads(l) for l in Path(str(prefix)+'.jsonl').read_text().splitlines()]
    keyed={(r['a'],r['b'],r['seed'],r['seat']):r for r in rows}
    differences=[];changed=0;own_actions=0;by_seat={}
    for seed in meta['seeds']:
        ds=[]
        for seat in (0,1):
            a=keyed['base','arshs3',seed,seat];b=keyed['recover_now','arshs3',seed,seat]
            ds.append(100*(b['score']-a['score']))
            own_actions+=int(a['action_hashes'][seat]!=b['action_hashes'][seat])
        differences.append(statistics.mean(ds))
    for seat in (0,1):
        by_seat[seat]=statistics.mean(100*(keyed['recover_now','arshs3',seed,seat]['score']-keyed['base','arshs3',seed,seat]['score']) for seed in meta['seeds'])
    mean=statistics.mean(differences)
    error=float(tdist.ppf(.975,len(differences)-1))*statistics.stdev(differences)/len(differences)**.5
    base=statistics.mean(r['score'] for r in rows if r['a']=='base' and r['b']=='arshs3')
    status='INCONCLUSIVE'
    if mean>0 and sum(d>0 for d in differences)>=2:status='PROMISING'
    if mean+error<0:status='REJECTED'
    direct=[r for r in rows if {r['a'],r['b']}=={'base','recover_now'}]
    result=dict(reference='base',candidate='recover_now',opponent='arshs3',seeds=meta['seeds'],
        base_wr=100*base,candidate_wr=100*base+mean,delta_points=mean,ci95_seed=[mean-error,mean+error],
        ci95_2way=None,ci95_2way_reason='One opponent, not estimable',status=status,
        positive_seeds=sum(d>0 for d in differences),negative_seeds=sum(d<0 for d in differences),
        own_actions_changed=own_actions,matched_pool_episodes=64,by_seat=by_seat,
        direct_vs_vq_wr=100*statistics.mean(r['score'] if r['a']=='recover_now' else 1-r['score'] for r in direct))
    Path(str(prefix)+'.results.json').write_text(json.dumps(result,indent=2)+'\n')
    save('four_rounds_complete',state='complete',recovery_coverage=result,
         next_action='Inspect all confirmations and mechanisms, make justified submission or next experiment; research goal stays active.')


if __name__=='__main__':
    try:main()
    except BaseException as exc:
        save('loop4_failed',state='failed',error=repr(exc));raise
