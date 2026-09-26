"""Biblioteca de pronostico 'contra-cha22' para la capa PREDICT (_V92_P) de top3.

top3 (arshs3 + VQ + _V92_P_TOP=3) adelanta sus ventas cuando las partidas de su
biblioteca que mejor encajan con lo que el rival ya vendio anuncian una venta
grande del rival en 1-2 turnos. La biblioteca publica son partidas del top-30 del
19-sep; cha22, que hoy es ~la mitad de nuestros rivales, no esta en ella.

1. Juega top3 contra cha22 (ambos asientos) en semillas de construccion.
2. Al final de cada partida lee de top3 el mismo estado que usa en vivo
   (_V92_P[jugador]['obs'] = {(turno, item): unidades}) y el par de tiendas.
3. Anade esos episodios a la biblioteca original por par de tiendas, con el
   mismo formato binario (uint16 n; por episodio uint16 m; eventos delta/255+abs,
   item, cantidad), y escribe top3 con _V92_P_BLOB/_V92_P_INDEX sustituidos.

Uso: construir_biblioteca_cc.py <top3.py> <rivales> <salida.py> <seed0> <nseeds>
     <rivales> = una ruta, o varias separadas por comas (cada rival juega nseeds semillas
     distintas y consecutivas a partir de seed0, en ambos asientos).
"""
import base64, hashlib, json, multiprocessing as mp, sys, zlib
from pathlib import Path

NAMES = ['BAKERY', 'BRUNCH_SPOT', 'FARMERS_MARKET', 'ICE_CREAM_SHOP', 'PET_CAFE', 'PIZZA_SHOP', 'SMOOTHIE_SHOP', 'YARN_STORE']


def jugar(job):
    top3, cha22, seed, seat = job
    from kaggle_environments import make
    from kaggle_environments.agent import get_last_callable
    fn = get_last_callable(open(top3).read(), path=top3)
    agents = [None, None]
    agents[seat], agents[1 - seat] = fn, cha22
    env = make("kaggriculture", configuration={"seed": seed, "episodeSteps": 720})
    env.run(agents)
    st = [str(s.status) for s in env.steps[-1]]
    shops = tuple(env.steps[-1][0]["observation"]["town"]["unlocked_shops"][:2])
    g = fn.__globals__
    ev = dict((g.get("_V92_P") or {}).get(seat, {}).get("obs", {}))
    return dict(seed=seed, seat=seat, status=st, shops=list(shops),
                ev=[[t, i, int(q)] for (t, i), q in sorted(ev.items())])


def decodificar(g):
    raw = zlib.decompress(base64.b85decode(g["_V92_P_BLOB"]))
    lib = {}
    for a in range(8):
        for b in range(8):
            start, _ = g["_V92_P_INDEX"][a * 8 + b]
            pos = start; n = raw[pos] | raw[pos + 1] << 8; pos += 2; eps = []
            for _ in range(n):
                m = raw[pos] | raw[pos + 1] << 8; pos += 2; ev = {}; last = 0
                for _ in range(m):
                    d = raw[pos]; pos += 1
                    if d == 255:
                        t = raw[pos] | raw[pos + 1] << 8; pos += 2
                    else:
                        t = last + d
                    ev[(t, raw[pos])] = raw[pos + 1]; pos += 2; last = t
                eps.append(ev)
            lib[(a, b)] = eps
    return lib


def codificar(lib):
    out = bytearray(); index = []
    for a in range(8):
        for b in range(8):
            start = len(out); eps = lib[(a, b)]
            out += len(eps).to_bytes(2, "little")
            for ev in eps:
                items = sorted(ev.items())
                out += len(items).to_bytes(2, "little"); last = 0
                for (t, i), q in items:
                    d = t - last
                    if 0 <= d < 255:
                        out.append(d)
                    else:
                        out.append(255); out += int(t).to_bytes(2, "little")
                    out.append(i); out.append(min(255, int(q))); last = t
            index.append((start, len(out) - start))
    return base64.b85encode(zlib.compress(bytes(out), 9)).decode(), index


def main(top3, cha22, salida, seed0, nseeds):
    seed0, nseeds = int(seed0), int(nseeds)
    from kaggle_environments.agent import get_last_callable
    g = get_last_callable(open(top3).read(), path=top3).__globals__
    lib = decodificar(g)
    # comprobacion de ida y vuelta del formato
    blob, index = codificar(lib)
    assert decodificar({"_V92_P_BLOB": blob, "_V92_P_INDEX": index}) == lib, "codec no reproduce la biblioteca"
    antes = sum(len(v) for v in lib.values())
    rivales = cha22.split(",")
    jobs = [(top3, riv, seed0 + k * nseeds + s, seat) for k, riv in enumerate(rivales)
            for s in range(nseeds) for seat in (0, 1)]
    with mp.Pool(11) as pool:
        res = pool.map(jugar, jobs)
    Path(salida + ".episodios.json").write_text(json.dumps(res))
    malos = [r for r in res if r["status"] != ["DONE", "DONE"]]
    nuevos = 0
    for r in res:
        if r["status"] != ["DONE", "DONE"] or len(r["shops"]) < 2 or not r["ev"]:
            continue
        a, b = NAMES.index(r["shops"][0]), NAMES.index(r["shops"][1])
        lib[(a, b)].append({(t, i): q for t, i, q in r["ev"]}); nuevos += 1
    blob, index = codificar(lib)
    extra = (f"\n\n# ==== Biblioteca PREDICT contra-cha22 (kaggriculture local, 2026-09-26) ====\n"
             f"# {antes} episodios previos + {nuevos} nuevos vs {[Path(r).parent.name for r in rivales]} (semillas desde {seed0}).\n"
             f"_V92_P_BLOB = {blob!r}\n_V92_P_INDEX = {index!r}\n_V92_P_RAW = None\n_V92_P_LIB = None\n")
    Path(salida).write_bytes(Path(top3).read_bytes() + extra.encode())
    cubiertos = sum(1 for k, v in lib.items() if v)
    print(f"episodios: {antes} originales + {nuevos} nuevos; partidas invalidas {len(malos)}; pares con datos {cubiertos}/64")
    print(salida, hashlib.sha256(Path(salida).read_bytes()).hexdigest()[:12])


if __name__ == "__main__":
    main(*sys.argv[1:6])
