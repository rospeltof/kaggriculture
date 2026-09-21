"""Descarga replays de UNA submission ajena (el lider) en replays/<carpeta>/.

A diferencia de bajar_replays.py (que baja NUESTRAS submissions), aqui el
objetivo es un submission_id concreto de otro equipo. La CLI lo permite.
Carpeta propia por submission: nunca se mezclan generaciones ni equipos.

Uso: ./.venv/bin/python bajar_lider.py <submission_id> <carpeta> [max]
"""
import os, subprocess, sys

KAGGLE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".venv", "bin", "kaggle")


def main(sub_id, carpeta, maxn):
    d = os.path.join("replays", carpeta); os.makedirs(d, exist_ok=True)
    out = subprocess.run([KAGGLE, "competitions", "episodes", sub_id, "--format", "csv"],
                         capture_output=True, text=True).stdout
    eps = [l.split(",")[0] for l in out.splitlines()[1:] if l[:1].isdigit()]
    print(f"submission {sub_id}: {len(eps)} episodios; bajando hasta {maxn} en {d}", flush=True)
    ok = 0
    for e in eps[:maxn]:
        if os.path.exists(os.path.join(d, f"{e}.json")):
            ok += 1; continue
        r = subprocess.run([KAGGLE, "competitions", "replay", e, "-p", d], capture_output=True, text=True)
        good = "downloaded" in r.stdout or os.path.exists(os.path.join(d, f"{e}.json"))
        ok += good
        print(("  OK   " if good else "  FALLO ") + e, flush=True)
    print(f"listo: {ok}/{min(maxn, len(eps))}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 40)
