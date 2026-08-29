"""Descarga replays SOLO de las submissions activas y los organiza por bot.

Nace del riesgo que señaló el usuario (2026-09-03): analizar partidas de
generaciones viejas creyendo que son del campeón contamina las conclusiones.
Aquí cada replay queda en replays/<NOMBRE_DEL_BOT>/ y nunca se mezcla.

Uso:
    ./.venv/bin/python bajar_replays.py            # lista submissions activas
    ./.venv/bin/python bajar_replays.py --bajar 15 # baja hasta 15 por submission
"""
import argparse
import os
import re
import subprocess

KAGGLE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".venv", "bin", "kaggle")
COMP = "kaggriculture"


def submissions():
    """[(id, descripcion, score)] más recientes primero."""
    out = subprocess.run([KAGGLE, "competitions", "submissions", COMP],
                         capture_output=True, text=True).stdout
    rows = []
    for line in out.splitlines()[2:]:
        m = re.match(r"\s*(\d+)\s+\S+\s+\S+\s+\S+\s+(.*?)\s+SubmissionStatus\.(\w+)\s*([\d.]*)", line)
        if m:
            rows.append((m.group(1), m.group(2).strip()[:60], m.group(4) or "-"))
    return rows


def nombre_bot(desc):
    """Etiqueta corta y estable a partir de la descripción de la submission."""
    d = desc.lower()
    for clave in ("campeona_season", "campeona", "integral v2", "integral", "rutera",
                  "v5r", "xl", "v4", "v2", "v1"):
        if clave in d:
            return clave.replace(" ", "_").upper()
    return "OTRO"


def episodios(sub_id):
    out = subprocess.run([KAGGLE, "competitions", "episodes", sub_id, "--format", "csv"],
                         capture_output=True, text=True).stdout
    return [l.split(",")[0] for l in out.splitlines()[1:] if l[:1].isdigit()]


def main(bajar=0, activas=2):
    subs = submissions()
    print(f"submissions ({len(subs)}); las {activas} primeras son las ACTIVAS en el ladder:")
    for i, (sid, desc, score) in enumerate(subs):
        marca = "  <-- ACTIVA" if i < activas else ""
        print(f"  {sid}  {score:>7s}  {desc}{marca}")
    if not bajar:
        return
    for sid, desc, _ in subs[:activas]:
        bot = nombre_bot(desc)
        d = os.path.join("replays", bot)
        os.makedirs(d, exist_ok=True)
        eps = episodios(sid)
        nuevos = [e for e in eps if not os.path.exists(os.path.join(d, f"episode-{e}-replay.json"))]
        print(f"\n{bot} ({sid}): {len(eps)} episodios, {len(nuevos)} sin descargar")
        for e in nuevos[:bajar]:
            r = subprocess.run([KAGGLE, "competitions", "replay", e, "-p", d],
                               capture_output=True, text=True)
            print(("  OK " if "downloaded" in r.stdout else "  FALLO ") + e)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--bajar", type=int, default=0, help="máximo de replays nuevos por submission")
    ap.add_argument("--activas", type=int, default=2)
    args = ap.parse_args()
    main(bajar=args.bajar, activas=args.activas)
