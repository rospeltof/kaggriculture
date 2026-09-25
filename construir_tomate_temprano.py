"""Mueve coherentemente la campaña V219 sin tocar las rutas del padre.

Las fechas biológicas se desplazan; las fechas del resto de la explotación
siguen absolutas. Conserva avisos y atribuciones Apache-2.0 del archivo público.
"""
import ast
import hashlib
import json
from pathlib import Path

from construir_tomato_loop import FINITE

BASE=Path('submission/main_publico_arshs3_vq.py')
OUT=Path('results/tomate_temprano_20260925')
VARIANTS={
    'early12_9k':(12,9000),
    'early12_6k':(12,6000),
    'early14_6k':(14,6000),
    'early16_6k':(16,6000),
    'late18_6k':(18,6000),
}


def patch_function(src,name,predicate,changes):
    nodes=[n for n in ast.parse(src).body if isinstance(n,ast.FunctionDef) and n.name==name]
    nodes=[n for n in nodes if predicate(ast.get_source_segment(src,n))]
    assert len(nodes)==1,(name,len(nodes))
    node=nodes[0];old=ast.get_source_segment(src,node);new=old
    for before,after in changes:
        assert new.count(before)==1,(name,before,new.count(before))
        new=new.replace(before,after)
    lines=src.splitlines(keepends=True)
    return ''.join(lines[:node.lineno-1])+new+'\n'+''.join(lines[node.end_lineno:])


def transformed(src):
    src=patch_function(src,'_v219_request',lambda s:'parent_hires=' in s,[
        ('day!=18','day!=_ET_START'),
        ("if state.get('requested_day')==day:return action",
         "if day>_ET_START+11:return action\n    if state.get('requested_day')==day:return action"),
        ('day in (24,27)','day in (_ET_START+6,_ET_START+9)'),
        ('day in (19,20,21,22,23,25)','day-_ET_START in (1,2,3,4,5,7)'),
        ('26<=day<=28','_ET_START+8<=day<=_ET_START+10'),
        ('fertilizer and day==27','fertilizer and day==_ET_START+9'),
    ])
    src=patch_function(src,'_v219_worker',lambda s:True,[
        ('day==18','day==_ET_START'),('day<29','day<_ET_START+11'),
    ])
    src=patch_function(src,'agent',lambda s:'if step==432:' in s,[
        ('if step==432:','if step==_ET_START*24:'),
        ('or day<18','or day<_ET_START'),
        ('day==24 or fertilizer_worker','day==_ET_START+6 or fertilizer_worker'),
    ])
    src=patch_function(src,'_r53_labor_assignment',lambda s:True,[
        ('day not in (26,27,28)','day-_ET_START not in (8,9,10)'),
        ('day==27','day==_ET_START+9'),
    ])
    src=patch_function(src,'_cxtb_qualifies',lambda s:True,[
        ("farm['money'] < 12000","farm['money'] < _ET_LIQUIDITY"),
        ('tape[432:719]','tape[_ET_START*24:719]'),
    ])
    return src


def build():
    raw=BASE.read_bytes()
    assert hashlib.sha256(raw).hexdigest()=='9b463dfb8076b4c63946e1ae4249cd1cfc3cc58b63115cf2bd5b00f96f188976'
    src=transformed(raw.decode());OUT.mkdir(parents=True,exist_ok=True);manifest={}
    for name,(day,threshold) in VARIANTS.items():
        path=OUT/(name+'.py')
        if path.exists():raise FileExistsError(path)
        extra='\n# Local early-tomato experiment, 2026-09-25.\n'
        extra+='_ET_PARENT=[v for v in list(globals().values()) if callable(v)][-1]\n'
        extra+=f'_ET_START={day}\n_ET_LIQUIDITY=6000\n_CXTB_MIN_REVENUE={threshold}\n'
        extra+='_CXTB_HARVEST_DAYS=tuple(range(_ET_START+8,_ET_START+12))\n'
        extra+='V13V_SKIP_DAYS=tuple(_ET_START+d for d in (1,3,5))\n'
        extra+='for _et_day in range(_ET_START+8,_ET_START+11):_R53_LABOR_REPORT["labor_day"+str(_et_day)]=0\n'
        extra+=FINITE
        extra+='\ndef early_tomato_agent(observation,configuration=None):\n    return _ET_PARENT(observation,configuration)\n'
        data=(src+extra).encode();compile(data,str(path),'exec');path.write_bytes(data)
        manifest[name]=dict(path=str(path),sha256=hashlib.sha256(data).hexdigest(),
                            start_day=day,min_revenue=threshold,liquidity=6000,
                            finite_supply=True,harvest_days=list(range(day+8,day+12)))
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(manifest,indent=2))


if __name__=='__main__':build()
