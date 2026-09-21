"""Comprueba serialización y equivalencia del archivo enviado en el motor local."""
import hashlib
import importlib.util
import json
from pathlib import Path

from bots.meta.tape import make as tape

ROOT = Path(__file__).resolve().parent


def main():
    path = ROOT / "submission/main.py"
    evidence = ROOT / "docs/evidencia/envio_maj_20260914"
    manifest = json.loads((evidence / "paquete.json").read_text())
    assert hashlib.sha256(path.read_bytes()).hexdigest() == manifest["main_sha256"]
    spec = importlib.util.spec_from_file_location("packed_agent", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    reference = tape(manifest["candidate"])
    for step in range(721):
        obs = {"step": step}
        assert mod.agent(obs) == reference(obs)
        mutated = mod.agent(obs)
        mutated["market"].append(["SELL", "WHEAT", 999])
        assert mod.agent(obs) == reference(obs), "La acción comparte memoria"
    from kaggle_environments import make
    from bots.chassis import make_agent
    from bots.arquetipos import CAMPEONA_HOZ
    rows = []
    for seed in (218000, 218001):
        for seat in (0, 1):
            runs = []
            for candidate in (str(path), reference):
                agents = [None, None]
                agents[seat] = candidate
                agents[1-seat] = make_agent(dict(CAMPEONA_HOZ))
                env = make("kaggriculture", configuration={"seed": seed, "episodeSteps": 720}, debug=False)
                env.run(agents)
                assert len(env.steps) == 720
                assert [s.status for s in env.steps[-1]] == ["DONE", "DONE"]
                assert not any(s.status in ("ERROR", "INVALID", "TIMEOUT") for step in env.steps for s in step)
                # El runtime puede añadir tiempo restante propio; comparar el estado de juego.
                state = [{"actions": [s.action for s in step],
                          "farms": step[0].observation.get("farms"),
                          "private": [s.observation.get("private") for s in step],
                          "market": step[0].observation.get("market"),
                          "town": step[0].observation.get("town"),
                          "rewards": [s.reward for s in step]} for step in env.steps]
                digest = hashlib.sha256(json.dumps(state, sort_keys=True).encode()).hexdigest()
                runs.append(dict(state_sha256=digest, rewards=[s.reward for s in env.steps[-1]]))
            assert runs[0] == runs[1], (seed, seat, runs)
            rows.append(dict(seed=seed, seat=seat, **runs[0]))
            print(f"OK seed={seed} asiento={seat}: 720 estados equivalentes", flush=True)
    result = dict(main_sha256=manifest["main_sha256"], action_cases=721,
                  mutation_isolation=True, simulated_episodes=8, matched_pairs=4, pairs=rows)
    (evidence / "validacion_paquete.json").write_text(json.dumps(result, indent=2) + "\n")
    print("Paquete validado: archivo autónomo y módulo producen el mismo juego.")


if __name__ == "__main__":
    main()
