"""Pasa la deteccion EMBEBIDA en f29g (funciones _gs_antes/_gs_despues del modulo) por los 133 replays reales de
final_29 y la compara con la implementacion de referencia (guarda_f29.jsonl). Solo lee NUESTRA observacion y
nuestra accion emitida. Uso: validar_replays.py <f29g.py> <carpeta_replays> <ref.jsonl> <salida.jsonl>"""
import glob, json, sys
from multiprocessing import Pool

NS = None
def init(path):
    global NS
    NS = {}
    exec(compile(open(path).read(), path, 'exec'), NS)

def job(path):
    d = json.load(open(path)); n = d['info']['TeamNames']
    if n.count('Rospel') != 1:
        return None
    me = n.index('Rospel'); st = d['steps']
    NS['_GS_STATE'].clear()
    det = None
    for s in range(len(st) - 1):
        obs = dict(st[s][me]['observation']); obs['step'] = s; obs['player'] = me
        NS['_gs_antes'](obs, None)
        g = NS['_GS_STATE'][me]
        if det is None and g['off']:
            det = s
        NS['_gs_despues'](obs, None, st[s + 1][me].get('action') or {})
    g = NS['_GS_STATE'][me]
    return dict(ep=d['info']['EpisodeId'], rival=n[1 - me], det=det, log=[list(x) for x in g['log']])

if __name__ == '__main__':
    agente, carpeta, ref, out = sys.argv[1:5]
    files = sorted(glob.glob(carpeta + '/*.json'))
    R = {json.loads(l)['ep']: json.loads(l) for l in open(ref)}
    rows = []
    with Pool(4, initializer=init, initargs=(agente,)) as p:
        for r in p.imap_unordered(job, files):
            if r:
                rows.append(r)
    with open(out, 'w') as f:
        for r in rows:
            f.write(json.dumps(r) + '\n')
    dif_det = dif_gap = dif_n = n_ev = 0; ms = []
    for r in rows:
        rr = R[r['ep']]
        if r['det'] != rr['det']:
            dif_det += 1; print('DET distinto', r['ep'], r['rival'], r['det'], rr['det'])
        a = {x[0]: x for x in r['log']}; b = {x[0]: x for x in rr['log']}
        if set(a) != set(b):
            dif_n += 1; print('pasos evaluados distintos', r['ep'], sorted(set(a) ^ set(b))[:10])
        for t in set(a) & set(b):
            ga, gb = a[t][2], b[t][2]
            n_ev += 1; ms.append(a[t][3])
            if (ga is None) != (gb is None) or (ga is not None and abs(ga - gb) > 1e-3):
                dif_gap += 1; print('gap distinto', r['ep'], t, a[t], b[t])
    ms.sort()
    dets = sorted((r['det'], r['ep'], r['rival']) for r in rows if r['det'] is not None)
    print(f'partidas {len(rows)}; evaluaciones comparadas {n_ev}; det distintos {dif_det}; pasos distintos {dif_n}; gaps distintos {dif_gap}')
    print('ms p50 %.2f p99 %.2f max %.2f' % (ms[len(ms)//2], ms[int(.99*len(ms))], ms[-1]))
    print('disparos:', dets)
