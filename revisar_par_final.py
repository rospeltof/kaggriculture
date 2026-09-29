"""Comprobación de solo lectura para decidir el par final (regla fijada 2026-09-29 18:40 UTC).

Uso:  ./.venv/bin/python revisar_par_final.py [--desde 2026-09-29T18:40]

No envía nada. Lee de Kaggle las submissions (rating y estado) y los episodios de
final_29 y final_xc1, y evalúa la regla de docs/research/CALENDARIO_ENVIOS.md:
  (a1) rating f29 - rating xc1 >= +40, o
  (a2) partidas públicas creadas después de --desde (no vistas al fijar la regla),
       >= 30 por bot: xc1 gana <= 40 % y f29 gana >= 45 %;
  (b)  f29 gana >= 45 % de sus últimas 30 y, desde --desde, no tiene 3 o más episodios
       ERRORED que xc1 (las caídas de la plataforma afectan a todos por igual);
  (c)  rating f29 >= rating xc1 - 25.
Se reenvía la copia exacta de final_29 solo si (a1 o a2) y (b) y (c), y el usuario
lo aprueba en el chat en ese momento.
"""
import argparse
import json
import math
import os
import sys
from datetime import datetime, timezone

from kaggle.api.kaggle_api_extended import KaggleApi

COMP = 'kaggriculture'
SUBS = {'f29': 56655371, 'xc1': 56628181}
EQUIPO = 'Rospel'


def wilson(w, n, z=1.96):
    if n == 0:
        return float('nan'), float('nan')
    p = w / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c - h) / d, (c + h) / d


def partidas(api, sub):
    filas, raras = [], []
    for e in api.competition_list_episodes(sub):
        r = json.loads(e.to_json())
        ag = r.get('agents') or []
        yo = [a for a in ag if a.get('submissionId') == sub]
        otro = [a for a in ag if a.get('submissionId') != sub]
        if r.get('state') != 'COMPLETED' or len(yo) != 1 or any(a.get('reward') is None for a in ag):
            raras.append(dict(id=r.get('id'), t=r.get('createTime'), estado=r.get('state'),
                              tipo=r.get('type'), agentes=ag))
            continue
        if r.get('type') != 'EPISODE_TYPE_PUBLIC' or len(otro) != 1 or otro[0].get('teamName') == EQUIPO:
            continue
        m, o = yo[0]['reward'], otro[0]['reward']
        filas.append(dict(id=r['id'], t=r['createTime'], m=m, o=o, rival=otro[0].get('teamName'),
                          res='W' if m > o else ('L' if m < o else 'T')))
    filas.sort(key=lambda x: x['t'])
    return filas, raras


def wl(lista):
    w = sum(x['res'] == 'W' for x in lista)
    l = sum(x['res'] == 'L' for x in lista)
    return w, l


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--desde', default='2026-09-29T18:40')
    ap.add_argument('--guardar', default='results/par_final')
    a = ap.parse_args()

    api = KaggleApi()
    api.authenticate()
    ahora = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    subs = {int(s.ref): s for s in api.competition_submissions(COMP)}
    rating, estado = {}, {}
    for k, sid in SUBS.items():
        s = subs.get(sid)
        estado[k] = str(getattr(s, 'status', None))
        try:
            rating[k] = float(getattr(s, 'public_score', None) or getattr(s, 'publicScore'))
        except (TypeError, ValueError):
            rating[k] = float('nan')
    print(f'consulta {ahora}')
    recientes = sorted(subs.values(), key=lambda s: str(s.date), reverse=True)[:4]
    print('submissions más recientes:')
    for s in recientes:
        print(f'  {s.ref} {s.date} {s.status} {getattr(s, "public_score", "")}')

    datos = {}
    for k, sid in SUBS.items():
        filas, raras = partidas(api, sid)
        datos[k] = dict(filas=filas, raras=raras)
        w, l = wl(filas)
        print(f'{k} {sid}: rating {rating[k]:.1f} estado {estado[k]} | públicas {w}-{l} '
              f'| última partida {filas[-1]["t"] if filas else "-"} | episodios raros {len(raras)}')
        for r in raras[-5:]:
            print('   raro:', json.dumps(r, ensure_ascii=False)[:300])

    f, x = datos['f29']['filas'], datos['xc1']['filas']
    dif = rating['f29'] - rating['xc1']
    a1 = dif >= 40
    nf = [p for p in f if p['t'] >= a.desde]
    nx = [p for p in x if p['t'] >= a.desde]
    wf, lf = wl(nf)
    wx, lx = wl(nx)
    pf = wf / (wf + lf) if wf + lf else float('nan')
    px = wx / (wx + lx) if wx + lx else float('nan')
    a2 = (wf + lf >= 30 and wx + lx >= 30 and px <= 0.40 and pf >= 0.45)
    u30 = f[-30:]
    w30, l30 = wl(u30)
    # Los ERRORED sin replay descargable son caídas de la plataforma cuando afectan igual a
    # otros equipos (29-sep 04:14-06:34 UTC). Cuentan contra (b) solo los posteriores a --desde
    # y solo si f29 tiene al menos 3 más que xc1 en ese mismo tramo.
    def errores(k):
        return [r for r in datos[k]['raras'] if r.get('estado') == 'ERRORED' and (r.get('t') or '') >= a.desde]
    ef, ex = errores('f29'), errores('xc1')
    b = (w30 + l30 > 0 and w30 / (w30 + l30) >= 0.45 and len(ef) < len(ex) + 3)
    c = rating['f29'] >= rating['xc1'] - 25

    lo, hi = wilson(wf, wf + lf)
    print(f'\n(a1) rating f29 - xc1 = {dif:+.1f} (>= +40): {a1}')
    print(f'(a2) desde {a.desde}: f29 {wf}-{lf} ({100 * pf:.1f} % [{100 * lo:.1f}; {100 * hi:.1f}]), '
          f'xc1 {wx}-{lx} ({100 * px:.1f} %); >= 30 por bot, xc1 <= 40 %, f29 >= 45 %: {a2}')
    print(f'(b)  últimas 30 de f29 {w30}-{l30}, ERRORED desde --desde f29 {len(ef)} / xc1 {len(ex)}: {b}')
    print(f'(c)  rating f29 >= xc1 - 25: {c}')
    ok = (a1 or a2) and b and c
    print('\nREGLA:', 'se cumple -> proponer al usuario reenviar la copia exacta de final_29 (sha cf129189)'
          if ok else 'no se cumple -> el par se queda final_29 + final_xc1')
    os.makedirs(os.path.dirname(a.guardar) or '.', exist_ok=True)
    salida = f'{a.guardar}_{ahora[:16].replace(":", "")}.json'
    json.dump(dict(consulta=ahora, rating=rating, estado=estado, desde=a.desde, a1=a1, a2=a2, b=b, c=c,
                   cumple=ok, datos=datos), open(salida, 'w'))
    print('guardado', salida)
    return 0


if __name__ == '__main__':
    sys.exit(main())
