"""Extrae mecanismos actuales del líder; ninguna cinta se usa como rival adaptativo."""
from collections import Counter,defaultdict
from copy import deepcopy
import gzip
import hashlib
import json
from pathlib import Path

from analizar_publicos_reales import analyze
from investigar_lider import compact_state
from sonda_fallo_forecast import run

OUT=Path('docs/evidencia/loop_publicos_20260925')


def main():
    selection=json.loads((OUT/'dsm_replay_selection.json').read_text());report=[];traces={}
    for meta in selection['episodes']:
        eid=meta['id'];path=Path(f'replays/DSM_56518845/episode-{eid}-replay.json')
        replay=json.loads(path.read_text());assert replay['module_version']=='1.32.7'
        summary=analyze({'id':eid,'source':'dsm','team':'DSM','path':str(path)})
        me=summary['me'];opp=1-me
        def tape(player):
            def agent(obs):return deepcopy(replay['steps'][int(obs['step'])+1][player]['action'])
            return agent
        env,ledger=run(tape(me),tape(opp),replay['info']['seed'],me)
        assert all(compact_state(a)==compact_state(b) for a,b in zip(replay['steps'],env.steps))
        outfile=OUT/f'dsm_{eid}.ledger.jsonl.gz'
        if outfile.exists():raise FileExistsError(outfile)
        outfile.write_bytes(gzip.compress(('\n'.join(json.dumps(r) for r in ledger)+'\n').encode(),mtime=0))
        summary['states_exact']=720;summary['cashflow']=[]
        for player in (me,opp):
            by=defaultdict(lambda:[0,0]);phases=defaultdict(lambda:[0,0])
            for r in ledger:
                if r['player']!=player:continue
                by[r['op'],r['item']][0]+=1;by[r['op'],r['item']][1]+=r['value']
                phases[r['step']//240,r['op'],r['item']][0]+=1
                phases[r['step']//240,r['op'],r['item']][1]+=r['value']
            summary['cashflow'].append({'total':[{'op':op,'item':item,'units':n,'cash':cash} for (op,item),(n,cash) in by.items()],
                'phases':[{'phase':phase,'op':op,'item':item,'units':n,'cash':cash} for (phase,op,item),(n,cash) in phases.items()]})
        actions=[s[me]['action'] or {} for s in replay['steps'][1:]]
        traces[eid]=actions
        summary['first_land_changes']=[];summary['max_hands']=0
        for t in range(719):
            f0=replay['steps'][t][0]['observation']['farms'][me]
            f1=replay['steps'][t+1][0]['observation']['farms'][me]
            if len(f1['unlocked_quadrants'])>len(f0['unlocked_quadrants']):
                summary['first_land_changes'].append([t,len(f1['unlocked_quadrants'])])
            summary['max_hands']=max(summary['max_hands'],len(f0['hands']))
        report.append(summary)
        print(eid,summary['opponent'],summary['margin'],'states exact 720','hands',summary['max_hands'],'land',summary['first_land_changes'],flush=True)
    pairs=[]
    import itertools
    for a,b in itertools.combinations(traces,2):
        units=[t for t,(x,y) in enumerate(zip(traces[a],traces[b])) if (x.get('farmer'),x.get('hands'))!=(y.get('farmer'),y.get('hands'))]
        pairs.append({'a':a,'b':b,'first_unit_divergence':units[0] if units else None,'different_unit_turns':len(units)})
    (OUT/'dsm_current_analysis.json').write_text(json.dumps({'selection':selection,'episodes':report,'pairwise':pairs},indent=2,ensure_ascii=False)+'\n')


if __name__=='__main__':main()
