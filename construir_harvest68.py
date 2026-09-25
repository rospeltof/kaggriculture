"""Preserve public V68 bytes and create one declared selector-off ablation."""
import hashlib
import json
from pathlib import Path

PUBLIC = Path('results/publicos_0712_20260925/haodou092_kaggriculture-harvest-ledger/main.py')
OUT = Path('results/harvest68_20260925')
EVIDENCE = Path('docs/evidencia/loop_publicos_20260925')


def main():
    raw = PUBLIC.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == '3b543611448947399c9902e6ca1e45b84e904031156ff012ea675947dc74197e'
    tail = b'''

# Local, declared ablation: suppress only the V68 herd target; preserve all other layers.
def _dsm_herd_target(obs, kind, quantity):
    return None

submission_without_dsm_selector = agent
'''
    OUT.mkdir(parents=True, exist_ok=True); path = OUT/'harvest68_no_ev.py'; assert not path.exists()
    data = raw+tail; compile(data, str(path), 'exec'); path.write_bytes(data)
    manifest = dict(harvest68=dict(path=str(PUBLIC), sha256=hashlib.sha256(raw).hexdigest()),
                    harvest68_no_ev=dict(path=str(path), sha256=hashlib.sha256(data).hexdigest()))
    dest = EVIDENCE/'public_0712_variants.json'; assert not dest.exists()
    dest.write_text(json.dumps(manifest, indent=2)+'\n'); print(json.dumps(manifest, indent=2))


if __name__ == '__main__': main()
