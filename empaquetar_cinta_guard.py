"""Empaqueta una cinta + guardia de caja (bots/guardia_cinta.py) como main.py.
Escribe a --out; no envia. El unico cambio frente a la cinta desplegada es la
guardia del d0: aisla su efecto en el ladder."""
import argparse, base64, gzip, hashlib, json
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parent

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("name"); ap.add_argument("--out", default="submission/main_guard.py")
    ap.add_argument("--reserve", type=int, default=12)
    a = ap.parse_args()
    payload = (ROOT / "bots/meta/tapes" / f"{a.name}.json.gz").read_bytes()
    trace = json.loads(gzip.decompress(payload)); assert len(trace) == 720
    guard_src = (ROOT / "bots/guardia_cinta.py").read_text()
    source = f'''"""Kaggriculture: {a.name} + guardia de caja del d0 (reserve={a.reserve}).
Autocontenido; generado por empaquetar_cinta_guard.py. No consulta red ni archivos.
"""
import base64
import gzip
import json

# ---- bots/guardia_cinta.py (copia literal) ----
{guard_src}
# ---- fin guardia ----

_TRACE = json.loads(gzip.decompress(base64.b64decode({base64.b64encode(payload).decode("ascii")!r})))


def agent(obs, config=None):
    step = int(obs.get("step", 0) or 0)
    if step >= len(_TRACE):
        return {{"farmer": ["PASS"], "hands": [], "market": []}}
    return guard_cash(obs, json.loads(json.dumps(_TRACE[step])), reserve={a.reserve})
'''
    out = ROOT / a.out; out.write_text(source)
    rec = dict(candidate=f"{a.name}+guard{a.reserve}", prepared_at=datetime.now(timezone.utc).isoformat(),
               sha256=hashlib.sha256(out.read_bytes()).hexdigest(), bytes=out.stat().st_size)
    (ROOT / f"docs/research/paquete_{a.name}_guard.json").write_text(json.dumps(rec, indent=2) + "\n")
    print(f"escrito {out} ({out.stat().st_size:,} bytes)")

if __name__ == "__main__":
    main()
