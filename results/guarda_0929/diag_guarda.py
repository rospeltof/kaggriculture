"""Diagnostico complementario a torneo.py: juega <agente> contra <rival> y guarda la telemetria de la guarda
(paso de disparo, golpes, gaps) y la del copiador (pasos con ida-y-vuelta, indice de su reventa, cuantas antes de
nuestro 9 con MS activo). Mismo hash de acciones que torneo.py.
Uso: diag_guarda.py <salida.jsonl> <agente.py> <rival.py> <seed,...> [--asientos 0,1]"""
import hashlib, json, sys, time
from multiprocessing import Pool

def jugar(job):
    agente, rival, seed, seat = job
    from kaggle_environments import make
    from kaggle_environments.agent import get_last_callable
    fa = get_last_callable(open(agente).read(), path=agente)
    fr = get_last_callable(open(rival).read(), path=rival)
    hs = [hashlib.sha256(), hashlib.sha256()]
    cpu = [[], []]
    def tr(fn, p):
        def call(obs, cfg):
            c0 = time.process_time(); w0 = time.perf_counter()
            a = fn(obs, cfg)
            cpu[p].append((1000 * (time.process_time() - c0), 1000 * (time.perf_counter() - w0), int(obs.get('step', 0))))
            hs[p].update(json.dumps(a, sort_keys=True, separators=(',', ':'), allow_nan=False).encode() + b'\n')
            return a
        return call
    ag = [None, None]; ag[seat] = tr(fa, seat); ag[1 - seat] = tr(fr, 1 - seat)
    env = make('kaggriculture', configuration={'episodeSteps': 720, 'seed': seed}, debug=False)
    t0 = time.time(); env.run(ag); st = env.steps
    rw = [st[-1][p]['reward'] for p in (0, 1)]
    ms = copia = antes9 = 0; idx_venta = []
    for t in range(len(st) - 1):
        qa = st[t + 1][seat]['action'].get('market') or []
        qr = st[t + 1][1 - seat]['action'].get('market') or []
        ms_on = len(qa) == 10 and qa[9] and qa[9][0] in ('SELL', 'BUY_PRODUCT') and qa[9][1] in ('WHEAT', 'FERTILIZER')
        ms += bool(ms_on)
        for it in ('WHEAT', 'FERTILIZER'):
            b = [i for i, o in enumerate(qr) if o and o[0] == 'BUY_PRODUCT' and o[1] == it]
            s = [i for i, o in enumerate(qr) if o and o[0] == 'SELL' and o[1] == it]
            if b and s:
                copia += 1; idx_venta.append(max(s) if min(b) < max(s) else max(b))
                if ms_on and qa[9][1] == it and max(max(s), max(b)) < 9:
                    antes9 += 1
    durs = [[], []]
    for logs in env.logs:
        for p, lg in enumerate(logs or []):
            if isinstance(lg, dict) and 'duration' in lg:
                durs[p].append(lg['duration'])
    tel = getattr(fa, 'telemetry', None) or {}
    g = (tel.get('jugadores') or {}).get(seat) or {}
    return dict(agente=agente.split('/')[-1], rival=rival.split('/')[-1], seed=seed, seat=seat, rewards=rw,
                margen=rw[seat] - rw[1 - seat], status=[str(st[-1][p]['status']) for p in (0, 1)],
                hash=hs[seat].hexdigest(), off_step=g.get('off_step'), golpes=g.get('golpes'),
                gaps_pos=[x for x in (g.get('log') or []) if x[2] is not None and x[2] > 0][:12],
                evals=tel.get('evals'), abst=tel.get('abstenciones'), errores=tel.get('errores'), gs_max_ms=tel.get('max_ms'),
                pasos_ms=ms, pasos_idayvuelta_rival=copia, antes_de_9_con_ms=antes9,
                idx_venta_hist={str(k): idx_venta.count(k) for k in sorted(set(idx_venta))},
                cp_tel=getattr(fr, 'telemetry', None), ms_max=[1000 * max(d) if d else None for d in durs],
                cpu_max=[max(c)[0] if c else None for c in cpu], cpu_max_paso=[max(c)[2] if c else None for c in cpu],
                cpu_p99=[sorted(x[0] for x in c)[int(.99 * len(c))] if c else None for c in cpu],
                cpu_max_sin_t0=[max(x[0] for x in c if x[2] > 0) if c else None for c in cpu],
                pared_max=[max(x[1] for x in c) if c else None for c in cpu],
                seg=round(time.time() - t0))

if __name__ == '__main__':
    out, agente, rival, seeds = sys.argv[1:5]
    asientos = [int(x) for x in (sys.argv[6] if len(sys.argv) > 6 else '0,1').split(',')]
    jobs = [(agente, rival, int(s), a) for s in seeds.split(',') for a in asientos]
    with Pool(min(4, len(jobs))) as p, open(out, 'a') as f:
        for r in p.imap_unordered(jugar, jobs):
            f.write(json.dumps(r, default=str) + '\n'); f.flush()
            print(json.dumps({k: r[k] for k in ('rival', 'seed', 'seat', 'margen', 'status', 'off_step', 'golpes', 'pasos_ms', 'antes_de_9_con_ms', 'idx_venta_hist', 'ms_max', 'cpu_max', 'cpu_max_paso', 'cpu_max_sin_t0', 'seg')}), flush=True)
