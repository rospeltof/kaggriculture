"""Laboratorio de reglas de Kaggriculture.

Corre escenarios guionizados (una mecánica a la vez) contra un oponente pasivo
y deja inspeccionar el estado paso a paso. Pensado para verificar las
predicciones de docs/RULES.md.

Uso típico (desde `python -i lab.py`, un notebook, o un test):

    env = run_scenario({
        0: {"farmer": ["PASS"], "market": [["BUY_SEED", "WHEAT", 1]]},
        1: {"farmer": ["PLANT", "WHEAT"]},
        25: {"farmer": ["WATER"]},
    }, n_steps=60)

    o = obs_at(env, step=2)   # observación del jugador 0 tras el paso 2
    print_farm(o)             # resumen legible del farm
    tile_at(o, 4, 4)          # dict crudo del tile donde arranca el granjero
    print_market(o)           # precios e inventario del mercado
"""

from kaggle_environments import make

DEFAULT_ACTION = {"farmer": ["PASS"], "hands": [], "market": []}

CROP_CHARS = {"WHEAT": "w", "CARROT": "c", "TOMATO": "t", "STRAWBERRY": "s", "MELON": "m"}
ANIMAL_CHARS = {"GOOSE": "G", "COW": "C", "SHEEP": "S"}


def scripted(script):
    """Agente que ejecuta script[step] y PASS en los pasos no listados.

    script: {step: {"farmer": [...], "hands": [...], "market": [...]}}
    Las claves ausentes de un paso se completan con la acción por defecto.
    """

    def agent(obs):
        step = obs.get("step", obs["day"] * 24 + obs["hour"])
        action = dict(DEFAULT_ACTION)
        action.update(script.get(step, {}))
        return action

    return agent


def run_scenario(script, n_steps=48, seed=42, opponent="pass", config=None):
    """Corre un episodio con el script como jugador 0. Devuelve el env."""
    cfg = {"episodeSteps": n_steps, "seed": seed}
    if config:
        cfg.update(config)
    env = make("kaggriculture", configuration=cfg, debug=True)
    agent = scripted(script) if isinstance(script, dict) else script
    env.run([agent, opponent])
    return env


def obs_at(env, step, player=0):
    """Observación del jugador tras procesarse el paso `step`.

    Las claves compartidas (farms, market, town) viven en el agente 0;
    para el jugador 1 se mezclan con sus claves privadas.
    """
    base = dict(env.steps[step][0].observation)
    if player != 0:
        base.update(env.steps[step][player].observation)
    return base


def tile_at(obs, x, y, player=None):
    """Dict crudo del tile (x, y) — tiles se indexa [y][x]."""
    p = obs["player"] if player is None else player
    return obs["farms"][p]["tiles"][y][x]


def _tile_char(tile):
    if tile is None:
        return "."
    if tile == "LOCKED":
        return "#"
    kind = tile.get("kind")
    if kind == "WEED":
        return "x"
    if kind == "PLANT":
        ch = CROP_CHARS.get(tile.get("crop"), "?")
        return ch.upper() if tile.get("watered_today") else ch
    if kind in ("COOP", "PASTURE"):
        animal = tile.get("animal")
        if animal:
            return ANIMAL_CHARS.get(animal, "?")
        return "o" if kind == "COOP" else "u"
    return "?"


def print_farm(obs, player=None):
    """Resumen legible: mayúscula = planta regada hoy, # = locked, x = weed,
    o/u = coop/pasture vacíos, G/C/S = animales, [..] = posición del granjero."""
    p = obs["player"] if player is None else player
    farm = obs["farms"][p]
    print(
        f"día {obs['day']} hora {obs['hour']} | player {p} | "
        f"money ${farm['money']:.0f} | quadrants {list(farm['unlocked_quadrants'])}"
    )
    print(f"farmer en {list(farm['farmer'])} | hands: {[list(h) for h in farm['hands']]}")
    fx, fy = farm["farmer"]
    for y, row in enumerate(farm["tiles"]):
        cells = []
        for x, tile in enumerate(row):
            ch = _tile_char(tile)
            cells.append(f"[{ch}]" if (x, y) == (fx, fy) else f" {ch} ")
        print("".join(cells))
    priv = obs.get("private") or {}
    print("seeds:", {k: v for k, v in (priv.get("seeds") or {}).items() if v})
    print("shed:", {k: v for k, v in (priv.get("shed") or {}).items() if v})
    invs = priv.get("inventories") or [{}]
    print("inv farmer:", dict(invs[0]))


def print_market(obs):
    """Precio e inventario por producto, con el delta respecto al I0 = 10,000."""
    market = obs["market"]
    for item, price in market["prices"].items():
        inv = market["inventory"][item]
        delta = inv - 10000
        print(f"{item:11s} ${price:>4} | inv {inv:>6} ({delta:+d})")


if __name__ == "__main__":
    env = run_scenario(
        {
            0: {"farmer": ["PASS"], "market": [["BUY_SEED", "WHEAT", 1]]},
            1: {"farmer": ["PLANT", "WHEAT"]},
        },
        n_steps=6,
    )
    print_farm(obs_at(env, 3))
