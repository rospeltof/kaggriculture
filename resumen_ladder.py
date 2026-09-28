"""Resumen de partidas reales de una carpeta de replays (una submission nuestra).

Por partida: rival, dinero final de ambos, margen, primer paso con accion distinta
(copias de la familia tds27 divergen tarde) y el paso de mayor perdida de margen.
Al final: W/L/T, cuantas son espejos (|margen| < 1.000) y cuantas copias tardias
(primera diferencia >= paso 100).

Uso: resumen_ladder.py replays/<carpeta> [...]
"""
import glob, json, sys


def main(*carpetas):
    res = []
    for c in carpetas:
        for f in sorted(glob.glob(f"{c}/*.json")):
            d = json.load(open(f))
            names = d["info"]["TeamNames"]
            if "Rospel" not in names:
                continue
            me = names.index("Rospel"); op = 1 - me
            rw = d["rewards"]
            if rw[0] is None or rw[1] is None:
                continue
            steps = d["steps"]
            first = next((t - 1 for t in range(1, len(steps)) if steps[t][0].get("action") != steps[t][1].get("action")), None)
            mon = [[s[0]["observation"]["farms"][p]["money"] for p in (0, 1)] for s in steps]
            mg = [m[me] - m[op] for m in mon]
            peor = min(range(len(mg) - 1), key=lambda t: mg[t + 1] - mg[t])
            res.append((names[op], rw[me], rw[op], rw[me] - rw[op], first, peor, mg[peor + 1] - mg[peor], d["info"]["EpisodeId"]))
    res.sort(key=lambda r: r[3])
    for r in res:
        print("%-26s nos %7.0f riv %7.0f margen %+7.0f  1a dif %4s  peor paso %3d (%+6.0f)  ep %d" % (r[0][:26], *r[1:4], r[4], r[5], r[6], r[7]))
    w = sum(r[3] > 0 for r in res); l = sum(r[3] < 0 for r in res); t = len(res) - w - l
    esp = [r for r in res if abs(r[3]) < 1000]
    tard = [r for r in res if r[4] is None or r[4] >= 100]
    print(f"\npartidas {len(res)}: W {w} L {l} T {t} ({100 * (w + t / 2) / max(1, len(res)):.1f}%)")
    print(f"espejos |margen|<1000: {len(esp)} (W {sum(r[3] > 0 for r in esp)} L {sum(r[3] < 0 for r in esp)}); "
          f"copias tardias (1a dif >= 100): {len(tard)} (W {sum(r[3] > 0 for r in tard)} L {sum(r[3] < 0 for r in tard)})")


if __name__ == "__main__":
    main(*sys.argv[1:])
