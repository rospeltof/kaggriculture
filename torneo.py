"""Torneo round-robin entre arquetipos + autopsias de desperdicio.

Cada par se enfrenta n_seeds seeds con espejo (2n episodios por par).
Al final: tabla de liga (suma de scores) y autopsia de cada arquetipo
contra un rival fijo (starter) para comparar desperdicio interno.

Uso:
    ./.venv/bin/python torneo.py -n 12
"""
import argparse

from autopsia import autopsy, print_report
from harness import evaluate

SPECS = {
    "control":      "bots.arquetipos:control",
    "gansos":       "bots.arquetipos:gansos",
    "ovejas_vacas": "bots.arquetipos:ovejas_vacas",
    "writeup":      "bots.arquetipos:writeup",
    "starter":      "starter",
}


def main(n_seeds=12, seed0=1000, do_autopsy=True):
    names = list(SPECS)
    points = {n: 0.0 for n in names}
    money = {n: [] for n in names}

    print("=== TORNEO ROUND-ROBIN ===\n")
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            r = evaluate(SPECS[a], SPECS[b], n_seeds=n_seeds, seed0=seed0)
            points[a] += r["score"]
            points[b] += 1 - r["score"]
            money[a].append(r["money_a"])
            money[b].append(r["money_b"])
            print()

    print("=== TABLA DE LIGA (máx 4.0 puntos) ===")
    for n in sorted(names, key=lambda k: -points[k]):
        avg_money = sum(money[n]) / len(money[n]) if money[n] else 0
        print(f"  {n:14s} {points[n]:4.2f} pts | dinero final medio ${avg_money:,.0f}")

    if do_autopsy:
        print("\n=== AUTOPSIAS (3 seeds vs starter) ===")
        for n in names:
            if n == "starter":
                continue
            agg = autopsy(SPECS[n], "starter", n_seeds=3, seed0=6000)
            print_report(n, agg)
            print()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", "--seeds", type=int, default=12)
    ap.add_argument("--seed0", type=int, default=1000)
    ap.add_argument("--sin-autopsia", action="store_true")
    args = ap.parse_args()
    main(n_seeds=args.seeds, seed0=args.seed0, do_autopsy=not args.sin_autopsia)
