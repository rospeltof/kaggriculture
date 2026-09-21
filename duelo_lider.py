"""Diagnóstico registrado frente a HOZ vivo. No selecciona ni promueve agentes."""
from datetime import datetime, timezone
import gzip
import json
from multiprocessing import Pool
import statistics as st

from evaluar_lider import ROOT, OUT, encoded, episode, sha


def main():
    register = json.loads((OUT / "confirmacion_registro.json").read_text())
    candidate = register["candidate"]
    confirmation = json.loads((OUT / f"confirm_{candidate}.meta.json").read_text())
    assert confirmation["state"] == "complete", "Esperar confirmación completa"
    target = OUT / "duelo_hoz.json"
    assert not target.exists(), "No sobrescribir diagnóstico"
    seeds = list(range(217000, 217008))
    paths = [ROOT / name for name in confirmation["file_hashes"]]
    paths.append(ROOT / "duelo_lider.py")
    hashes = {str(p.relative_to(ROOT)): sha(p.read_bytes()) for p in paths}
    meta = dict(state="registered", candidate=candidate, opponent="base", seeds=seeds,
                seats=[0, 1], expected_episodes=16, workers=2,
                role="Diagnóstico, sin selección ni promoción; ocho semillas y ambos asientos",
                started_at=datetime.now(timezone.utc).isoformat(), file_hashes=hashes)
    with target.open("x") as handle:
        json.dump(meta, handle, indent=2, ensure_ascii=False)
    jobs = [(candidate, "base", seed, seat) for seed in seeds for seat in (0, 1)]
    rows = []
    raw = OUT / "duelo_hoz.episodes.jsonl"
    try:
        with raw.open("x") as handle, Pool(2) as pool:
            for row in pool.imap_unordered(episode, jobs):
                handle.write(json.dumps(row, ensure_ascii=False, allow_nan=False) + "\n")
                handle.flush()
                assert row["valid"], row
                rows.append(row)
        assert len(rows) == 16
        assert hashes == {str(p.relative_to(ROOT)): sha(p.read_bytes()) for p in paths}
        assert {(r["seed"], r["seat"]) for r in rows} == {(s, p) for s in seeds for p in (0, 1)}
        means = [st.mean(r["score"] for r in rows if r["seed"] == s) for s in seeds]
        from scipy.stats import t
        margin = float(t.ppf(.975, 7)) * st.stdev(means) / 8**.5
        compressed = raw.with_suffix(raw.suffix + ".gz")
        compressed.write_bytes(gzip.compress(raw.read_bytes(), mtime=0))
        meta.update(state="complete", completed_episodes=16, score=st.mean(means),
                    seed_scores=means, seed_ci95=[st.mean(means)-margin, st.mean(means)+margin],
                    wins=sum(r["score"] == 1 for r in rows),
                    ties=sum(r["score"] == .5 for r in rows),
                    losses=sum(r["score"] == 0 for r in rows),
                    episodes_file=compressed.name, episodes_sha256=sha(compressed.read_bytes()),
                    finished_at=datetime.now(timezone.utc).isoformat())
    except BaseException as exc:
        meta.update(state="failed", error=str(exc), completed_episodes=len(rows))
        raise
    finally:
        target.write_text(json.dumps(meta, indent=2, ensure_ascii=False, allow_nan=False) + "\n")
    print(json.dumps({k: meta[k] for k in ("candidate", "score", "wins", "ties", "losses", "seed_ci95")}, indent=2))


if __name__ == "__main__":
    main()
