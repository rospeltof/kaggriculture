"""Empaqueta el ARBOL de rutas del lider como main.py autonomo; no envia a Kaggle.

El arbol (bots/experimentos_lider.py, kind="tree") ramifica entre 4 cintas de
Majkel1337 usando SOLO informacion visible: la primera tienda desbloqueada en
d3 (step 72) y la presencia de YARN_STORE en d6 (step 144). Empato con la cinta
maj_107674293 en el piloto del 2026-09-14 (64.06%) y perdio el desempate por
orden alfabetico; deberia generalizar mejor a rivales nuevos porque ramifica.
"""
import argparse, base64, gzip, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BRANCH_IDS = (107685970, 107692988, 107696961, 107710951)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--guard", type=int, default=0, help="reserve de la guardia d0 (+reintento de compromisos); 0 = sin guardias")
    ap.add_argument("--out", default="submission/main.py")
    a = ap.parse_args()
    guard_src = (ROOT / "bots/guardia_cinta.py").read_text() if a.guard else ""
    tapes = {}
    for i in BRANCH_IDS:
        payload = (ROOT / "bots/meta/tapes" / f"maj_{i}.json.gz").read_bytes()
        trace = json.loads(gzip.decompress(payload))
        assert len(trace) == 720 and all(isinstance(a, dict) for a in trace), i
        tapes[i] = base64.b64encode(payload).decode("ascii")
    encoded = json.dumps({str(k): v for k, v in tapes.items()})
    source = f'''"""Kaggriculture: arbol de rutas de Majkel1337 (4 cintas){', guardias de caja d0 (reserve=%d) y reintento de compromisos' % a.guard if a.guard else ''}.
Autocontenido; generado por empaquetar_arbol.py. No consulta red ni archivos.
Ramifica solo con informacion visible: primera tienda en d3, YARN_STORE en d6.
"""
import base64
import gzip
import json

{guard_src}
_RAW = json.loads({encoded!r})
_TAPES = {{int(k): json.loads(gzip.decompress(base64.b64decode(v))) for k, v in _RAW.items()}}
_STATE = {{"route": 107685970}}
_COMMIT = {{}}


def agent(obs, config=None):
    step = int(obs.get("step", 0) or 0)
    if step == 0:
        _STATE["route"] = 107685970
        _COMMIT.clear()
    shops = (obs.get("town") or {{}}).get("unlocked_shops") or []
    if step == 72:
        first = shops[0] if shops else None
        if first == "PET_CAFE":
            _STATE["route"] = 107685970
        elif first in ("BAKERY", "BRUNCH_SPOT"):
            _STATE["route"] = 107692988
        else:
            _STATE["route"] = 107696961 if first == "YARN_STORE" else 107710951
    if step == 144 and _STATE["route"] in (107696961, 107710951):
        _STATE["route"] = 107696961 if "YARN_STORE" in shops else 107710951
    trace = _TAPES[_STATE["route"]]
    if step >= len(trace):
        return {{"farmer": ["PASS"], "hands": [], "market": []}}
    action = json.loads(json.dumps(trace[min(step, 719)]))
    {"return guard_commitments(obs, guard_cash(obs, action, reserve=%d), _COMMIT)" % a.guard if a.guard else "return action"}
'''
    output = ROOT / a.out
    previous_sha = None; archive = None
    if output.exists():
        previous = output.read_bytes()
        previous_sha = hashlib.sha256(previous).hexdigest()
        archive = ROOT / "submission/archivo" / f"main_{previous_sha}.py"
        archive.parent.mkdir(exist_ok=True)
        if archive.exists():
            assert archive.read_bytes() == previous
        else:
            archive.write_bytes(previous)
    output.write_text(source)
    record = dict(candidate=f"tree{'+guard%d' % a.guard if a.guard else ''}", branch_ids=list(BRANCH_IDS),
                  prepared_at=datetime.now(timezone.utc).isoformat(),
                  main_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
                  main_bytes=output.stat().st_size, previous_main_sha256=previous_sha,
                  previous_main_archive=str(archive.relative_to(ROOT)) if archive else None,
                  state="prepared", authorization="Usuario 2026-09-21: 'si hazlo' (subir el tree)")
    evidence = ROOT / f"docs/evidencia/envio_tree{'_guard' if a.guard else ''}_{datetime.now().strftime('%Y%m%d')}"
    evidence.mkdir(exist_ok=True)
    with (evidence / "paquete.json").open("w") as handle:
        json.dump(record, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    print(f"escrito {output} ({output.stat().st_size:,} bytes); anterior archivado en {archive.name if archive else None}")


if __name__ == "__main__":
    main()
