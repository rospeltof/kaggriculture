"""Empaqueta la submission: genera submission/main.py autocontenido.

Concatena el código fuente de bots/chassis.py (que no tiene imports — Python
puro) con la config del campeón vigente y la función `agent(obs)` que exige
Kaggle. Única fuente de verdad: el chasis y bots/arquetipos.py.

Uso:
    ./.venv/bin/python empaquetar.py            # usa MIMADA (campeón vigente)
    ./.venv/bin/python empaquetar.py OCHO_MANOS # otra config de arquetipos.py
"""
import os
import pprint
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bots import arquetipos

config_name = sys.argv[1] if len(sys.argv) > 1 else "MIMADA"
cfg = getattr(arquetipos, config_name)

chassis_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bots", "chassis.py")).read()

main_py = f'''"""Kaggriculture submission — generada por empaquetar.py.

Config: {config_name} (campeón vigente de la evolución local; ver docs/BITACORA.md).
Chasis: bots/chassis.py inline (Python puro, sin dependencias).
"""

{chassis_src}

CONFIG = {pprint.pformat(cfg, indent=1, width=100)}


def agent(obs):
    return decide(obs, CONFIG)
'''

os.makedirs("submission", exist_ok=True)
out = os.path.join("submission", "main.py")
with open(out, "w") as f:
    f.write(main_py)
print(f"escrito {out} ({len(main_py):,} bytes) con config {config_name}")
