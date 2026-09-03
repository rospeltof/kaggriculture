"""Los 40 rivales REALES del ladder como panel. ¿Ordena igual que el Elo?"""
import glob, json, math, os, statistics as st, sys
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BOTS = ["campeona_grano", "grano_noop", "grano_siega"]
ELO = {}


def _una(a):
    bot, tape, seed, seat = a
    from kaggle_environments import make
    from harness import materialize
    yo = materialize(f"bots.arquetipos:{bot}")
    riv = materialize(f"bots.meta.tape:{tape}")
    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=False)
    env.run([yo, riv] if seat == 0 else [riv, yo])
    f = env.steps[-1]
    mio = f[seat].reward or 0; suyo = f[1 - seat].reward or 0
    return (bot, tape, seed), (1.0 if mio > suyo else (0.5 if mio == suyo else 0.0))


def main():                                     # GUARD OBLIGATORIO
    tapes = [os.path.basename(f)[:-8] for f in glob.glob("bots/meta/tapes/lad_*.json.gz")]
    seeds = list(range(91300, 91308))
    trabajos = [(b, t, s, seat) for b in BOTS for t in tapes for s in seeds for seat in (0, 1)]
    print(f"{len(tapes)} cintas x {len(seeds)} seeds x 2 asientos x {len(BOTS)} bots "
          f"= {len(trabajos)} episodios", flush=True)
    with Pool(max(1, (os.cpu_count() or 2) - 1)) as pool:
        res = pool.map(_una, trabajos)
    por_bot = {}
    for (bot, tape, seed), v in res:
        por_bot.setdefault(bot, {}).setdefault((tape, seed), []).append(v)
    pares = {b: {k: sum(v) / len(v) for k, v in d.items()} for b, d in por_bot.items()}
    print(f"\n{'bot':18s} {'Elo':>7} {'panel 40':>9}")
    for b in BOTS:
        e = f"{ELO[b]:.1f}" if b in ELO else "-"
        print(f"{b:18s} {e:>7} {100*st.mean(list(pares[b].values())):>8.1f}%")
    json.dump({b: {f"{k[0]}|{k[1]}": v for k, v in d.items()} for b, d in pares.items()},
              open("results/panel40.json", "w"))
    base = pares[BOTS[0]]
    print(f"\n{'contra base':18s} {'delta':>8} {'sd':>7} {'t':>7}")
    for b in BOTS[1:]:
        k = sorted(set(base) & set(pares[b]))
        d = [pares[b][x] - base[x] for x in k]
        m = st.mean(d); sd = st.stdev(d)
        t = m/(sd/math.sqrt(len(d))) if sd else float("nan")
        print(f"{b:18s} {100*m:>+7.1f} {100*sd:>7.1f} {t:>+7.2f}")


if __name__ == "__main__":
    main()
