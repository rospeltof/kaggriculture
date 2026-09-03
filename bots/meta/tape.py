"""Agentes-cinta reconstruidos de rivales REALES del ladder.

Motivación (2026-08-31): el panel del proyecto está saturado — base, `_noop` y
cualquier candidato leen idéntico 0/0/100/100, así que detecta regresiones y es
CIEGO A LAS MEJORAS. Faltan rivales de fuerza intermedia. Los intentos sintéticos
fallaron (ver bots/meta/c95_handicap.py). La fuente válida es el ladder mismo.

Cada cinta es el schedule de 720 turnos de un rival concreto, extraído de un
replay de NUESTRA submission campeona_fb (55876067) y de ninguna otra.
Es el método del notebook del meta: C95 no es más que la cinta de un episodio.

Limitación honesta: una cinta es CIEGA — no reacciona a nosotros. Reproduce al
rival sólo mientras el mercado se parezca al de la partida original. Por eso
`reconstruir.py` valida cada cinta reproduciendo el marcador real con el seed
original, y se anota la fidelidad.

Uso: bots.meta.tape:uman_n3l
"""
import gzip
import json
import os

_DIR = os.path.join(os.path.dirname(__file__), "tapes")
_CACHE = {}


def _load(name):
    if name not in _CACHE:
        with gzip.open(os.path.join(_DIR, name + ".json.gz"), "rt") as fh:
            _CACHE[name] = json.load(fh)
    return _CACHE[name]


def make(name):
    """Agente que reproduce la cinta `name` turno a turno."""
    def agent(obs, config=None):
        trace = _load(name)
        step = int(obs.get("step", 0) or 0)
        if step >= len(trace):
            return {"farmer": ["PASS"], "hands": [], "market": []}
        return json.loads(json.dumps(trace[step]))   # copia: el motor muta
    return agent


def __getattr__(nombre):
    """bots.meta.tape:uman_n3l -> agente de tapes/uman_n3l.json.gz"""
    if os.path.exists(os.path.join(_DIR, nombre + ".json.gz")):
        return make(nombre)
    raise AttributeError(nombre)
