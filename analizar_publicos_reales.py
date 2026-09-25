"""Diagnóstico por transiciones de la muestra real fija del 2026-09-25."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import statistics as st

OUT=Path('docs/evidencia/research_20260925')


def analyze(meta):
    p=Path(meta['path']);raw=p.read_bytes();d=json.loads(raw)
    names=d['info']['TeamNames']
    target=meta.get('team','Rospel')
    if 'me' in meta:
        me=int(meta['me'])
        if me not in (0,1) or names[me]!=target:raise ValueError('Asiento explícito inconsistente')
    else:
        if names.count(target)!=1:
            raise ValueError('Identidad de asiento ambigua: hace falta metadata de submission o excluir el episodio')
        me=names.index(target)
    opp=1-me
    steps=d['steps'];assert len(steps)==720
    escapes=[[],[]];deaths=[Counter(),Counter()];unfed=[0,0];caremiss=[0,0]
    for t in range(1,len(steps)):
        prev=steps[t-1][0]['observation'];obs=steps[t][0]['observation']
        for player in (0,1):
            for y,row in enumerate(prev['farms'][player]['tiles']):
                for x,a in enumerate(row):
                    if not isinstance(a,dict):continue
                    b=obs['farms'][player]['tiles'][y][x]
                    if a.get('animal') and (not isinstance(b,dict) or not b.get('animal')):
                        escapes[player].append(dict(step=t,xy=[x,y],animal=a['animal']))
                    if a.get('crop') and isinstance(b,dict) and b.get('kind')=='WEED':
                        reason='water' if t%24==0 and a.get('consecutive_unwatered',0)>=1 and not a.get('watered_today') else 'decay_or_other'
                        deaths[player][reason]+=1
            if t%24==0:
                # El primer estado del día conserva consecutive_unfed; evita
                # confundir FEED de h23 (sí pudo ejecutarse) con falta de comida.
                for row in obs['farms'][player]['tiles']:
                    for tile in row:
                        if isinstance(tile,dict) and tile.get('animal'):
                            unfed[player]+=int(tile.get('consecutive_unfed',0)>0)
    daily=[]
    for day in (1,6,10,15,20,25,29):
        obs=steps[day*24][0]['observation'];farms=obs['farms']
        daily.append(dict(day=day,money=[f['money'] for f in farms],
            composition=[dict(Counter(tile.get('animal') or tile.get('crop') or tile.get('kind') for row in f['tiles'] for tile in row if isinstance(tile,dict))) for f in farms]))
    final=steps[-1];rewards=d['rewards'];delta=rewards[me]-rewards[opp]
    residual=[]
    for player in (me,opp):
        priv=final[player]['observation']['private'];obs=final[0]['observation']
        held=Counter(priv['shed'])
        for inv in priv['inventories']:held.update(inv)
        residual.append(dict(units=dict(held),quoted_value=sum(q*obs['market']['prices'].get(i,0) for i,q in held.items())))
    return dict(meta,sha256=hashlib.sha256(raw).hexdigest(),me=me,opponent=names[opp],
        score=1 if delta>0 else 0 if delta<0 else .5,margin=delta,rewards=rewards,
        seed=d['info']['seed'],configuration=d['configuration'],shops=steps[-1][0]['observation']['town']['unlocked_shops'],
        escapes_own=escapes[me],escapes_opp=escapes[opp],unfed_animal_days_own=unfed[me],unfed_animal_days_opp=unfed[opp],
        plant_deaths_own=dict(deaths[me]),plant_deaths_opp=dict(deaths[opp]),daily=daily,terminal_held=residual)


if __name__=='__main__':
    selection=json.loads((OUT/'replay_selection.json').read_text())
    rows=[analyze(m) for m in selection['files']]
    (OUT/'replay_diagnostics.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
    for name in ('arshs3','v13'):
        rr=[r for r in rows if r['source']==name]
        print(name,len(rr),'WLT',st.mean(r['score'] for r in rr),'mean_margin',st.mean(r['margin'] for r in rr))
        for r in rr:
            print(r['id'],r['opponent'],r['margin'],'escapes',len(r['escapes_own']),len(r['escapes_opp']),
                'unfed',r['unfed_animal_days_own'],r['unfed_animal_days_opp'],'deaths',r['plant_deaths_own'],
                'held',r['terminal_held'][0]['quoted_value'])
