"""Empaqueta tree_v3 (familia de cintas con prefijo identico + ramificacion
consistente) como main.py autonomo, con guardia de caja opcional. No envia.
Escribe a --out para verificar antes de promover a submission/main.py."""
import argparse, base64, gzip, hashlib, json, sys
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default="submission/main_tree_v3.py")
    ap.add_argument("--guard", type=int, default=0, help="reserve de la guardia d0; 0 = sin guardia")
    a = ap.parse_args()
    from bots.arbol_lider_v3 import cargar, BRANCH_STEPS
    cintas, lcp = cargar(); n = len(cintas)
    fam = [sum(1 for j in range(n) if j != i and lcp[i][j] >= 72) for i in range(n)]
    start = max(range(n), key=lambda i: (fam[i], cintas[i]["money"]))
    # solo viajan las cintas alcanzables desde start (LCP >= 72) + start
    idx = [i for i in range(n) if i == start or lcp[start][i] >= 72]
    pack = []
    for i in idx:
        raw = gzip.compress(json.dumps(cintas[i]["acts"], separators=(",", ":")).encode())
        pack.append(dict(ep=cintas[i]["ep"], money=cintas[i]["money"], seq=[list(s) for s in cintas[i]["seq"]],
                         b64=base64.b64encode(raw).decode("ascii")))
    sub_lcp = [[lcp[i][j] if i != j else 720 for j in idx] for i in idx]
    start_k = idx.index(start)
    guard_src = (ROOT / "bots/guardia_cinta.py").read_text() if a.guard else ""
    source = f'''"""Kaggriculture: tree_v3 — {len(idx)} cintas de Majkel1337 con prefijo identico (72 pasos),
ramificacion consistente por tienda en pasos {BRANCH_STEPS}{', guardia de caja d0 reserve=%d' % a.guard if a.guard else ''}.
Autocontenido; generado por empaquetar_arbol_v3.py. No consulta red ni archivos.
"""
import base64
import gzip
import json

{guard_src}
_BRANCH_STEPS = {BRANCH_STEPS!r}
_RAW = json.loads({json.dumps(pack, separators=(",", ":"))!r})
_CINTAS = [(c["ep"], c["money"], [tuple(s) for s in c["seq"]],
            json.loads(gzip.decompress(base64.b64decode(c["b64"])))) for c in _RAW]
_LCP = {sub_lcp!r}
_START = {start_k}
_STATE = {{}}
_COMMIT = {{}}


def agent(obs, config=None):
    step = int(obs.get("step", 0) or 0)
    if step == 0 or "cur" not in _STATE:
        _STATE["cur"] = _START
        _COMMIT.clear()
    shops = tuple((obs.get("town") or {{}}).get("unlocked_shops") or [])
    if step in _BRANCH_STEPS:
        k = _BRANCH_STEPS.index(step); cur = _STATE["cur"]
        cand = [j for j in range(len(_CINTAS))
                if (j == cur or _LCP[cur][j] >= step)
                and len(_CINTAS[j][2]) > k and _CINTAS[j][2][k] == shops]
        if cand:
            _STATE["cur"] = max(cand, key=lambda j: _CINTAS[j][1])
    acts = _CINTAS[_STATE["cur"]][3]
    action = json.loads(json.dumps(acts[min(step, len(acts) - 1)]))
    {"return guard_commitments(obs, guard_cash(obs, action, reserve=%d), _COMMIT)" % a.guard if a.guard else "return action"}
'''
    out = ROOT / a.out; out.write_text(source)
    rec = dict(candidate=f"tree_v3{'+guard%d' % a.guard if a.guard else ''}", n_cintas=len(idx), start=cintas[start]["ep"],
               eps=[cintas[i]["ep"] for i in idx], prepared_at=datetime.now(timezone.utc).isoformat(),
               sha256=hashlib.sha256(out.read_bytes()).hexdigest(), bytes=out.stat().st_size)
    (ROOT / f"docs/research/paquete_{rec['candidate']}.json").write_text(json.dumps(rec, indent=2) + "\n")
    print(f"escrito {out} ({out.stat().st_size:,} bytes, {len(idx)} cintas, inicio {cintas[start]['ep']})")


if __name__ == "__main__":
    main()
