"""Compara brazo f29g con referencia f29 en un torneo con --vs f29g,f29 --sin-cruces: identidad de hashes
(nuestro asiento y rival), margen y W/L por rival, ms max. Uso: analizar_humo.py <torneo.jsonl>"""
import json, sys, statistics as st
rows = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
bad = [r for r in rows if not r.get('valid')]
print('episodios', len(rows), 'invalidos', len(bad))
idx = {(r['a'], r['b'], r['seed'], r['seat']): r for r in rows}
rivales = sorted({r['b'] for r in rows})
tot_ig = tot = 0
for b in rivales:
    ig = igr = n = 0; dm = []; wg = wf = 0; lines = []; mf = []; mg = []
    for (a, bb, s, seat), r in sorted(idx.items()):
        if a != 'f29g' or bb != b:
            continue
        f = idx.get(('f29', b, s, seat))
        if not f:
            continue
        n += 1
        mine = r['action_hashes'][seat] == f['action_hashes'][seat]
        riv = r['action_hashes'][1 - seat] == f['action_hashes'][1 - seat]
        ig += mine; igr += riv
        dm.append(r['margin'] - f['margin']); wg += r['score']; wf += f['score']; mf.append(f['margin']); mg.append(r['margin'])
        lines.append(f"   s{s} a{seat}: f29 {f['margin']:+8.0f} ({f['score']}) f29g {r['margin']:+8.0f} ({r['score']}) {'=' if mine else 'DISTINTA'}")
    tot += n; tot_ig += ig
    if not n:
        continue
    print(f"{b:>11s}: n={n} hash propio igual {ig}/{n}, rival igual {igr}/{n}; puntos f29 {wf:.1f} f29g {wg:.1f}; "
          f"margen medio f29 {st.mean(mf):+.0f} f29g {st.mean(mg):+.0f}; delta medio {st.mean(dm):+.0f} "
          f"(min {min(dm):+.0f}, max {max(dm):+.0f})")
    for l in lines:
        print(l)
ms = {}
for r in rows:
    for p, m in enumerate(r['ms']):
        if m:
            n = r['a'] if p == r['seat'] else r['b']
            ms.setdefault(n, []).append(m['max'])
print('ms max por turno (peor episodio): ' + ', '.join(f"{n} {max(v):.0f}" for n, v in ms.items()))
print('ms max por turno (mediana de episodios): ' + ', '.join(f"{n} {st.median(v):.0f}" for n, v in ms.items()))
