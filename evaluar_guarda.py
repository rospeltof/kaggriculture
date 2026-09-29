"""Evalúa las cuatro condiciones de docs/research/PREREG_GUARDA_2026-09-29.md.

Uso: evaluar_guarda.py <confirm_guarda_cp.jsonl> <confirm_guarda_panel.jsonl>
"""
import json
import random
import statistics as st
import sys


def cargar(ruta):
    filas = [json.loads(l) for l in open(ruta) if l.strip()]
    idx = {(r['a'], r['b'], r['seed'], r['seat']): r for r in filas}
    return filas, idx


def pares(idx):
    for (a, b, s, seat), g in sorted(idx.items()):
        if a != 'f29g':
            continue
        f = idx.get(('f29', b, s, seat))
        if f:
            yield b, s, seat, g, f


def main(ruta_cp, ruta_panel):
    ok = {}
    todas = []
    for ruta in (ruta_cp, ruta_panel):
        filas, _ = cargar(ruta)
        todas += filas
    malas = [r for r in todas if not r.get('valid') or r.get('n_err')]
    ok[1] = not malas
    print(f'(1) partidas {len(todas)}, inválidas o con error {len(malas)}: {ok[1]}')

    _, idx = cargar(ruta_panel)
    n = distintas = gan = perd = 0
    por_rival = {}
    for b, s, seat, g, f in pares(idx):
        n += 1
        d = g['action_hashes'][seat] != f['action_hashes'][seat]
        pr = por_rival.setdefault(b, [0, 0, []])
        pr[0] += 1
        pr[2].append(g['margin'] - f['margin'])
        if d:
            distintas += 1
            pr[1] += 1
            gan += g['score'] > f['score']
            perd += g['score'] < f['score']
    frac = distintas / n if n else 1
    ok[2] = frac <= 0.02 and perd <= gan
    print(f'(2) panel: celdas {n}, hash propio distinto {distintas} ({100 * frac:.2f} %), '
          f'W/L ganadas {gan} perdidas {perd}: {ok[2]}')
    for b, (m, dd, dm) in sorted(por_rival.items()):
        print(f'     {b:>7s}: {dd}/{m} distintas, Δmargen medio {st.mean(dm):+.1f}')

    _, idx = cargar(ruta_cp)
    por_sem = {}
    por_cp = {}
    for b, s, seat, g, f in pares(idx):
        por_sem.setdefault(s, []).append(g['score'] - f['score'])
        c = por_cp.setdefault(b, dict(n=0, wg=0.0, wf=0.0, dm=[], disp=0))
        c['n'] += 1
        c['wg'] += g['score']
        c['wf'] += f['score']
        c['dm'].append(g['margin'] - f['margin'])
        c['disp'] += g['action_hashes'][seat] != f['action_hashes'][seat]
    sem = sorted(por_sem)
    celdas = sum(len(v) for v in por_sem.values())
    punto = sum(sum(v) for v in por_sem.values()) / celdas
    rng = random.Random(20260929)
    boot = []
    for _ in range(4000):
        muestra = [rng.choice(sem) for _ in sem]
        tot = sum(sum(por_sem[s]) for s in muestra)
        cnt = sum(len(por_sem[s]) for s in muestra)
        boot.append(tot / cnt)
    boot.sort()
    lo, hi = boot[int(0.025 * len(boot))], boot[int(0.975 * len(boot)) - 1]
    margen_ok = all(st.mean(c['dm']) > 0 for c in por_cp.values())
    ok[3] = lo > 0 and margen_ok
    print(f'(3) copiadores: celdas {celdas}, ΔW/L {100 * punto:+.2f} pp IC95 [{100 * lo:+.2f}; {100 * hi:+.2f}], '
          f'margen mayor contra los 4: {margen_ok}: {ok[3]}')
    for b, c in sorted(por_cp.items()):
        print(f"     {b:>10s}: n={c['n']} disparo {c['disp']}, puntos f29 {c['wf']:.1f} → f29g {c['wg']:.1f}, "
              f"Δmargen medio {st.mean(c['dm']):+.0f} (mín {min(c['dm']):+.0f})")

    ms = {'f29g': [], 'f29': []}
    for r in todas:
        m = r['ms'][r['seat']]
        if m and r['a'] in ms:
            ms[r['a']].append(m['max'])
    mg, mf = max(ms['f29g']), max(ms['f29'])
    ok[4] = mg <= mf + 100
    print(f'(4) ms máximo por turno: f29g {mg:.0f}, f29 {mf:.0f} (medianas {st.median(ms["f29g"]):.0f} / '
          f'{st.median(ms["f29"]):.0f}): {ok[4]}')
    print('\nCONFIRMADA' if all(ok.values()) else '\nNO CONFIRMADA', ok)


if __name__ == '__main__':
    main(*sys.argv[1:3])
