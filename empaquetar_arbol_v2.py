"""Empaqueta el arbol v2 (N cintas ganadoras + secuencias de tiendas) como main.py
autonomo. No envia. Escribe a --out (por defecto submission/main_tree_v2.py) para
verificar antes de promover a submission/main.py.

La logica del agente es una copia literal de bots/arbol_lider.make(): vecino mas
cercano sobre la secuencia de tiendas en los pasos 72/144/216/288, desempate por
dinero final del lider, y si nada coincide se mantiene la ruta actual.
"""
import argparse, base64, gzip, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--clasif", default="results/clasif_MAJKEL_56142830.json")
    ap.add_argument("--prefix", default="top_majkel1337_")
    ap.add_argument("--out", default="submission/main_tree_v2.py")
    ap.add_argument("--tag", default="tree_v2")
    a = ap.parse_args()
    clas = {r["ep"]: r for r in json.load(open(ROOT / a.clasif))}
    cintas = []
    for ep, r in sorted(clas.items()):
        if not r["gana"]:
            continue
        payload = (ROOT / "bots/meta/tapes" / f"{a.prefix}{ep}.json.gz").read_bytes()
        trace = json.loads(gzip.decompress(payload))
        assert len(trace) == 720 and all(isinstance(x, dict) for x in trace), ep
        cintas.append(dict(ep=ep, money=r["mio"], seq=[list(x) for x in r["shops_seq"]],
                           b64=base64.b64encode(payload).decode("ascii")))
    blob = json.dumps(cintas, separators=(",", ":"))
    source = f'''"""Kaggriculture: {a.tag} — arbol de {len(cintas)} cintas ganadoras del lider.
Autocontenido; generado por empaquetar_arbol_v2.py. No consulta red ni archivos.
Vecino mas cercano sobre la secuencia de tiendas visibles (pasos 72/144/216/288).
"""
import base64
import gzip
import json

_BRANCH_STEPS = (72, 144, 216, 288)
_RAW = json.loads({blob!r})
_CINTAS = [(c["ep"], c["money"], [tuple(s) for s in c["seq"]],
            json.loads(gzip.decompress(base64.b64decode(c["b64"])))) for c in _RAW]
_STATE = {{}}


def agent(obs, config=None):
    step = int(obs.get("step", 0) or 0)
    if step == 0 or "ruta" not in _STATE:
        _STATE["vivas"] = list(_CINTAS)
        _STATE["ruta"] = max(_CINTAS, key=lambda c: c[1])
    shops = tuple((obs.get("town") or {{}}).get("unlocked_shops") or [])
    if step in _BRANCH_STEPS:
        k = _BRANCH_STEPS.index(step)
        cand = [c for c in _STATE["vivas"] if len(c[2]) > k and c[2][k] == shops]
        if cand:
            _STATE["vivas"] = cand
            _STATE["ruta"] = max(cand, key=lambda c: c[1])
    acts = _STATE["ruta"][3]
    return json.loads(json.dumps(acts[min(step, len(acts) - 1)]))
'''
    out = ROOT / a.out
    out.write_text(source)
    rec = dict(candidate=a.tag, n_cintas=len(cintas), eps=[c["ep"] for c in cintas],
               clasif=a.clasif, prepared_at=datetime.now(timezone.utc).isoformat(),
               sha256=hashlib.sha256(out.read_bytes()).hexdigest(), bytes=out.stat().st_size)
    (ROOT / "docs/research").mkdir(exist_ok=True)
    (ROOT / f"docs/research/paquete_{a.tag}.json").write_text(json.dumps(rec, indent=2) + "\n")
    print(f"escrito {out} ({out.stat().st_size:,} bytes, {len(cintas)} cintas)")


if __name__ == "__main__":
    main()
