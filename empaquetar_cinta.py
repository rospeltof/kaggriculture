"""Empaqueta una cinta existente como main.py autónomo; no envía a Kaggle."""
import argparse
import base64
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name")
    args = parser.parse_args()
    if Path(args.name).name != args.name:
        raise ValueError("Usar sólo el nombre de una cinta")
    tape = ROOT / "bots/meta/tapes" / f"{args.name}.json.gz"
    payload = tape.read_bytes()
    trace = json.loads(gzip.decompress(payload))
    assert len(trace) == 720 and all(isinstance(a, dict) for a in trace)
    encoded = base64.b64encode(payload).decode("ascii")
    source = f'''"""Kaggriculture: {args.name}, ruta fija validada localmente.
Autocontenido; generado por empaquetar_cinta.py. No consulta red ni archivos.
"""
import base64
import gzip
import json

_TRACE = json.loads(gzip.decompress(base64.b64decode({encoded!r})))


def agent(obs, config=None):
    step = int(obs.get("step", 0) or 0)
    if step >= len(_TRACE):
        return {{"farmer": ["PASS"], "hands": [], "market": []}}
    return json.loads(json.dumps(_TRACE[step]))
'''
    output = ROOT / "submission/main.py"
    previous = output.read_bytes()
    previous_sha = hashlib.sha256(previous).hexdigest()
    archive = ROOT / "submission/archivo" / f"main_{previous_sha}.py"
    archive.parent.mkdir(exist_ok=True)
    if archive.exists():
        assert archive.read_bytes() == previous
    else:
        archive.write_bytes(previous)
    output.write_text(source)
    record = dict(candidate=args.name, prepared_at=datetime.now(timezone.utc).isoformat(),
                  tape_sha256=hashlib.sha256(payload).hexdigest(),
                  main_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
                  main_bytes=output.stat().st_size, previous_main_sha256=previous_sha,
                  previous_main_archive=str(archive.relative_to(ROOT)),
                  state="prepared", authorization="Usuario: Subela a kaggle pa que coja calle")
    evidence = ROOT / "docs/evidencia/envio_maj_20260914"
    evidence.mkdir(exist_ok=True)
    with (evidence / "paquete.json").open("x") as handle:
        json.dump(record, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    print(json.dumps(record, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
