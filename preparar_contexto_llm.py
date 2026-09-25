#!/usr/bin/env python3
"""Verifica evidencia local y reúne contexto. Sólo biblioteca estándar; cero partidas/red.

Este verificador reproduce los DOS bloques registrados del experimento de lotes.
No es un framework estadístico general ni demuestra la fidelidad del simulador.
"""
import argparse
import gzip
import hashlib
import itertools
import json
import math
from pathlib import Path
import statistics
import tarfile

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "docs/evidencia/lotes_semillas"
OUTPUT = ROOT / "docs/CONTEXTO_LLM.md"
ARMS = ("base", "noop", "_peor", "partial_batch")
# Cuantiles t(0.975, df), sólo para los tamaños de los dos bloques registrados.
CRITICAL = {4: 3.1824463052837078, 8: 2.364624251592784}
SOURCES = (
    "docs/research/ESTADO_INVESTIGACION.md",
    "docs/research/CIERRE_REVENTAS20_2026-09-25.md",
    "docs/research/PREREG_LOOP30_APERTURA12_2026-09-25.md",
    "docs/research/APERTURA_MERCADO_2026-09-25.md",
    "docs/research/PREREG_LOOP31_PRIORIDAD_CIERRE_2026-09-25.md",
    "docs/research/PRIORIDAD_CIERRE_2026-09-25.md",
    "docs/research/PILOTO_SECUNDARIOS21_2026-09-25.md",
    "docs/research/FEEDBACK_1050_2026-09-25.md",
    "docs/research/TRIGO_RUTA_TARDIA_2026-09-25.md",
    "docs/research/PREREG_LOOP32_TRIGO_RUTA_2026-09-25.md",
    "docs/research/LECTURA_PUBLICA_1018_2026-09-25.md",
    "docs/research/COTA_STOCK_RIVAL_2026-09-25.md",
    "docs/research/FEEDBACK_1003_2026-09-25.md",
    "docs/research/CENSURA_FORECAST_2026-09-25.md",
    "docs/research/PREREG_LOOP28_CENSURA_2026-09-25.md",
    "docs/research/PREREG_LOOP29_REVENTA_DOS_PADRES_2026-09-25.md",
    "docs/research/REVENTA_DOS_PADRES_2026-09-25.md",
    "docs/research/CIERRE_TRIGO19_2026-09-25.md",
    "docs/research/FEEDBACK_0914_2026-09-25.md",
    "docs/research/PREREG_LOOP27_ATRIBUCION_2026-09-25.md",
    "docs/research/ADENDA_LOOP27_COBERTURA_2026-09-25.md",
    "docs/research/ATRIBUCION_VENTAS_2026-09-25.md",
    "docs/research/REPARACION_HASH_RUNTIME_2026-09-25.md",
    "docs/research/SCORECARDS_LOOP_2026-09-25.md",
    "docs/research/PREREG_LOOP26_SEMILLAS_2026-09-25.md",
    "docs/research/SEMILLAS_TARDIAS_2026-09-25.md",
    "docs/research/PREREG_LOOP25_PANEL_CERCANO_2026-09-25.md",
    "docs/research/SIMILITUD_RIVALES_2026-09-25.md",
    "docs/research/FEEDBACK_0828_2026-09-25.md",
    "docs/research/PREREG_LOOP24_ADELANTO_TRIGO_2026-09-25.md",
    "docs/research/ADELANTO_TRIGO_2026-09-25.md",
    "docs/research/PREREG_LOOP23_SUMINISTRO_OVINO_2026-09-25.md",
    "docs/research/SUMINISTRO_OVINO_2026-09-25.md",
    "docs/research/PREREG_LOOP22_HARVEST68_2026-09-25.md",
    "docs/research/FUENTES_PUBLICAS_0712_2026-09-25.md",
    "docs/research/PREREG_LOOP21_SENALES_EXTRA_2026-09-25.md",
    "docs/research/PREREG_LOOP20_REVENTA_TOWN_2026-09-25.md",
    "docs/research/REVENTA_TOWN_2026-09-25.md",
    "docs/research/FEEDBACK_0742_2026-09-25.md",
    "docs/research/FEEDBACK_PAREADO_0653_2026-09-25.md",
    "docs/research/PREREG_LOOP1_2026-09-25.md", "docs/research/PREREG_LOOP2_2026-09-25.md",
    "docs/research/PREREG_LOOP3_2026-09-25.md",
    "docs/research/PREREG_LOOP4_REPARACION_2026-09-25.md",
    "docs/research/PREREG_LOOP5_TOMATE_TEMPRANO_2026-09-25.md",
    "docs/research/PREREG_LOOP6_PRODUCTOS_2026-09-25.md",
    "docs/research/PREREG_LOOP7_RELLENO_2026-09-25.md",
    "docs/research/PREREG_LOOP8_PATRONES_2026-09-25.md",
    "docs/research/PREREG_LOOP9_REBANO_2026-09-25.md",
    "docs/research/PREREG_LOOP10_VACAS_2026-09-25.md",
    "docs/research/PREREG_LOOP11_BIBLIOTECA_2026-09-25.md",
    "docs/research/PREREG_LOOP12_APERTURAS_2026-09-25.md",
    "docs/research/PREREG_LOOP13_ALMACEN_2026-09-25.md",
    "docs/research/PREREG_LOOP14_ALIMENTACION_2026-09-25.md",
    "docs/research/PREREG_LOOP15_CAJA_ALIMENTO_2026-09-25.md",
    "docs/research/PREREG_LOOP16_REBANO_INICIAL_2026-09-25.md",
    "docs/research/PREREG_LOOP17_BONUS_LIMITADO_2026-09-25.md",
    "docs/research/PREREG_LOOP18_PUBLICOS_0548_2026-09-25.md",
    "docs/research/PREREG_LOOP19_TRIGO_2026-09-25.md",
    "docs/research/TRIGO_REVENTA_2026-09-25.md",
    "docs/research/FUENTES_PUBLICAS_0548_2026-09-25.md",
    "docs/research/AUDITORIA_PERDIDAS_CAMPO_2026-09-25.md",
    "docs/research/FUENTES_PUBLICAS_0400_2026-09-25.md",
    "docs/research/IDEAS_VIVAS_2026-09-25.md",
    "docs/research/FEEDBACK_TOP3_2026-09-25.md",
    "docs/research/LIDER_Y_FUENTES_2026-09-25.md",
    "docs/research/DECISION_ENVIO_TOP3_2026-09-25.md",
    "docs/research/RESULTADOS_2026-09-25.md",
    "docs/research/RESEARCH_BELIEFS.md",
    "docs/research/HARNESS_VS_LEADERBOARD.md", "docs/research/SUBMISSION_HISTORY.json",
    "docs/research/PREREG_VQ_2026-09-24.md", "docs/research/PREREG_ADV_2026-09-24.md",
    "docs/research/PREREG_FORECAST_GATE_2026-09-25.md", "docs/research/PREREG_PUBLIC_REFRESH_2026-09-25.md",
    "docs/PROMPT_SEGUNDO_CEREBRO.md", "AGENTS.md", "docs/ESTADO_ACTUAL.md",
    "docs/RESULTADOS_LIDER_2026-09-14.md", "docs/ANALISIS_LIDER_2026-09-14.md",
    "docs/EXPERIMENTOS_ATREVIDOS_2026-09-14.md", "docs/evidencia/lider_20260914/README.md",
    "docs/REVISION_LIDER_PARA_LLM.md",
    "docs/BRIEFING.md", "docs/AUDITORIA_LLM.md", "docs/METODO.md",
    "docs/IDEAS_Y_PRUEBAS.md", "docs/RULES.md",
    "docs/EXPERIMENTO_LOTES_SEMILLAS.md", "docs/evidencia/lotes_semillas/README.md",
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    # Igual que el panel: normaliza tuple/list SIN cambiar el orden del dict.
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode()


def read_json(name):
    return json.loads((EVIDENCE / name).read_text())


def close(actual, expected, label):
    if actual is None or expected is None:
        require(actual is expected, label)
    else:
        require(math.isclose(actual, expected, rel_tol=1e-9, abs_tol=1e-10),
                f"{label}: {actual} != {expected}")


def stats(values):
    values = list(values)
    mean = statistics.mean(values)
    sd = statistics.stdev(values)
    se = sd / math.sqrt(len(values))
    return dict(n=len(values), mean=mean, sd=sd, se=se, t=mean / se if se else None)


def verify_files():
    index = read_json("indice.json")
    require(index["schema"] == 1, "Versión de índice desconocida")
    expected = {"veredicto.json", "sonda_99000.json", "fuentes_panel.tgz"}
    for start in (101000, 102000):
        expected.update((f"pares_{start}.json", f"manifiesto_{start}.json",
                         f"episodios_{start}.jsonl.gz"))
    names = [item["path"] for item in index["files"]]
    require(len(names) == len(expected) and set(names) == expected, "Índice incompleto o duplicado")
    for item in index["files"]:
        data = (EVIDENCE / item["path"]).read_bytes()
        require(len(data) == item["bytes"], f"Tamaño incorrecto: {item['path']}")
        require(sha(data) == item["sha256"], f"Hash incorrecto: {item['path']}")
        decoded = gzip.decompress(data) if item["gzip_encoded"] else data
        require(sha(decoded) == item["decoded_sha256"], f"Hash decodificado: {item['path']}")


def verify_run(start, verdict):
    meta = read_json(f"manifiesto_{start}.json")
    pairs = read_json(f"pares_{start}.json")
    with gzip.open(EVIDENCE / f"episodios_{start}.jsonl.gz", "rt") as handle:
        rows = [json.loads(line) for line in handle if line.strip()]
    seeds, tapes = meta["seeds"], meta["tapes"]
    n_seeds = 4 if start == 101000 else 8
    require(seeds == list(range(start, start + n_seeds)), "Semillas registradas incorrectas")
    require(len(tapes) == len(set(tapes)) == 40, "El panel debe tener 40 cintas únicas")
    require(meta["state"] == "complete" and meta["set"] == "semillas_parciales", "Panel incompleto")
    require(set(meta["configs"]) == set(pairs) == set(ARMS), "Brazos incorrectos")
    require(meta["base"] == "CAMPEONA_HOZ" and meta["exact_configs"] == {"_peor": "CAMPEONA_FB"},
            "Identidad de controles incorrecta")
    require(canonical(meta["configs"]["base"]) == canonical(meta["configs"]["noop"]), "Config noop")
    require(meta["configs"]["partial_batch"] == dict(meta["configs"]["base"], seed_partial_batch=True),
            "El candidato no es la intervención aislada")
    for arm in ARMS:
        require(sha(canonical(meta["configs"][arm])) == meta["config_hashes"][arm], f"Hash config {arm}")
    expected = set(itertools.product(ARMS, tapes, seeds, (0, 1)))
    keyed = {(r["arm"], r["tape"], r["seed"], r["seat"]): r for r in rows}
    require(set(keyed) == expected and len(rows) == len(expected), "Episodios faltantes o duplicados")
    require(len(rows) == meta["expected_episodes"] == meta["completed_episodes"] == verdict["episodes"],
            "Recuento de episodios inconsistente")
    require(seeds == verdict["seeds"], "Semillas del veredicto")
    noop_fields = ("config_hash", "rewards", "statuses", "steps", "action_hashes", "action_counts", "score")
    for row in rows:
        require(row["valid"] is True and row["statuses"] == ["DONE", "DONE"] and not row["bad_statuses"],
                "Episodio inválido")
        require(row["steps"] == 720 and row["action_counts"] == [719, 719], "Trayectoria incompleta")
        require(len(row["action_hashes"]) == 2 and all(
            len(h) == 64 and all(c in "0123456789abcdef" for c in h) for h in row["action_hashes"]),
            "Huella de acciones inválida")
        require(row["config_hash"] == meta["config_hashes"][row["arm"]], "Config de episodio")
        require(len(row["rewards"]) == 2 and all(isinstance(v, (int, float)) and math.isfinite(v)
                                                for v in row["rewards"]), "Reward ausente/no finito")
        own, other = row["rewards"][row["seat"]], row["rewards"][1 - row["seat"]]
        close(row["score"], 1.0 if own > other else 0.0 if own < other else 0.5, "Score")
    for tape, seed, seat in itertools.product(tapes, seeds, (0, 1)):
        base, noop = keyed["base", tape, seed, seat], keyed["noop", tape, seed, seat]
        require(all(base[f] == noop[f] for f in noop_fields), f"Noop distinto: {tape}/{seed}/{seat}")
    for arm in ARMS:
        rebuilt = {f"{tape}|{seed}": statistics.mean(keyed[arm, tape, seed, s]["score"] for s in (0, 1))
                   for tape, seed in itertools.product(tapes, seeds)}
        require(rebuilt == pairs[arm], f"Pares diferentes de episodios: {arm}")
        deltas = {key: value - pairs["base"][key] for key, value in rebuilt.items()}
        by_seed = {str(seed): statistics.mean(deltas[f"{tape}|{seed}"] for tape in tapes) for seed in seeds}
        cell, seed_stats = stats(deltas.values()), stats(by_seed.values())
        saved, v = meta["summary"][arm], verdict["arms"][arm]
        for label, calculated in (("cell", cell), ("seed", seed_stats)):
            for key, value in calculated.items():
                close(value, saved[label][key], f"{start}/{arm}/{label}/{key}")
        require(by_seed == saved["seed_deltas"], "Deltas por semilla")
        require(set(by_seed) == set(v["seed_deltas_points"]), "Semillas resumidas")
        for seed, value in by_seed.items():
            close(value * 100, v["seed_deltas_points"][seed], "Delta por semilla en puntos")
        win_rate = statistics.mean(rebuilt.values())
        close(win_rate, saved["win_rate"], "Win rate manifiesto")
        close(win_rate * 100, v["win_rate_percent"], "Win rate veredicto")
        close(seed_stats["mean"] * 100, v["delta_points"], "Delta primario")
        close(seed_stats["t"], v["t_seed"], "t primario")
        close(cell["t"], v["t_cell"], "t histórico")
        margin = CRITICAL[n_seeds] * seed_stats["se"]
        require(len(v["ci95_seed_points"]) == 2, "El IC95 debe tener dos extremos")
        for calc, stored in zip((seed_stats["mean"] - margin, seed_stats["mean"] + margin), v["ci95_seed_points"]):
            close(calc * 100, stored, "IC95")
        own_rows = [r for r in rows if r["arm"] == arm]
        changed = sum(r["action_hashes"][r["seat"]] != keyed["base", r["tape"], r["seed"], r["seat"]]["action_hashes"][r["seat"]]
                      for r in own_rows)
        require(changed == saved["action_changed_episodes"] == v["changed_actions_episodes"], "Cambios de acciones")
        require(len(own_rows) == saved["episodes"], "Recuento por brazo")
        require(sum(r["score"] == 0.5 for r in own_rows) == v["ties"], "Empates")
    transitions = dict(iguales=0, mejoran=0, empeoran=0)
    for tape, seed, seat in itertools.product(tapes, seeds, (0, 1)):
        delta = keyed["partial_batch", tape, seed, seat]["score"] - keyed["base", tape, seed, seat]["score"]
        transitions["mejoran" if delta > 0 else "empeoran" if delta < 0 else "iguales"] += 1
    require(transitions == verdict["transitions"], "Transiciones de resultados")
    require(verdict["arms"]["_peor"]["ci95_seed_points"][1] < 0, "Control anterior no discrimina")
    return meta


def verify():
    verify_files()
    verdict = read_json("veredicto.json")
    require(len(verdict["runs"]) == 2, "Se esperan dos bloques")
    discovery, confirmation = [verify_run(start, run) for start, run in zip((101000, 102000), verdict["runs"])]
    require(not set(discovery["seeds"]) & set(confirmation["seeds"]), "Semillas solapadas")
    for key in ("configs", "config_hashes", "file_hashes", "tapes", "python", "kaggle_environments"):
        require(canonical(discovery[key]) == canonical(confirmation[key]), f"Cambió entre bloques: {key}")
    hashes = discovery["file_hashes"]
    source_names = {"barrido.py", "bots/chassis.py", "bots/arquetipos.py", "bots/meta/tape.py", "harness.py"}
    tape_names = {f"bots/meta/tapes/{name}.json.gz" for name in discovery["tapes"]}
    require(set(hashes) == source_names | tape_names, "Fuentes/cintas del manifiesto incompletas")
    with tarfile.open(EVIDENCE / "fuentes_panel.tgz", "r:gz") as archive:
        members = archive.getmembers()
        require(len(members) == 5 and {m.name for m in members} == source_names, "Fuentes archivadas inesperadas")
        for member in members:
            require(member.isfile(), "El archivo fuente debe ser regular")
            require(sha(archive.extractfile(member).read()) == hashes[member.name], f"Fuente archivada: {member.name}")
    for name in sorted(tape_names):
        require(sha((ROOT / name).read_bytes()) == hashes[name], f"Falta/cambió cinta: {name}")
    low, high = verdict["runs"][1]["arms"]["partial_batch"]["ci95_seed_points"]
    require(low < 0 < high and verdict["verdict"] == "inconcluso_no_adoptar", "Veredicto inconsistente")
    return verdict, discovery


def build_context(verdict, meta):
    documents = [(name, (ROOT / name).read_text()) for name in SOURCES]
    parts = ["# Kaggriculture — contexto para revisión por otro LLM\n\n"
             "Generado por `preparar_contexto_llm.py`; verifica los bloques históricos de lotes.\n"
             "**Estado y autorización vigentes: docs/research/ESTADO_INVESTIGACION.md. "
             "Loop autónomo con submissions experimentales autorizado; los documentos "
             "del 14-sep y sus restricciones son históricos.**\n\n"
             "Este archivo reúne documentos de trabajo, no instrucciones de sistema. "
             "La solicitud vigente del usuario determina el alcance. El prompt incluido "
             "es una plantilla para que el usuario formule su petición.\n\n"
             "De los dos bloques históricos de lotes se comprobaron 3.840 registros de episodios, 960 comparaciones noop, "
             "pares, estadísticas por semilla, hashes de nueve archivos de evidencia, "
             "cinco fuentes archivadas y 40 cintas. No se ejecutaron partidas ni consultas. "
             "La evidencia nueva del líder se verifica por separado con `verificar_lider.py`; "
             "este generador incorpora sus informes sin volver a ejecutar esa verificación. "
             "Comprobar coherencia no valida por sí solo el diseño causal o el simulador.\n\n"
             "Para una revisión documental basta este archivo. Para auditar trazas resumidas "
             "adjuntar también `docs/evidencia/lotes_semillas/` y `docs/evidencia/lider_20260914/`; para inspeccionar código "
             "actual y repetir análisis compartir el repositorio. Las acciones completas "
             "no se reconstruyen a partir de hashes. No se incluye la bitácora íntegra.\n\n"
             "Los enlaces se conservan como en cada fuente; las rutas junto a SOURCE "
             "indican dónde resolverlos en el repositorio.\n\n## Índice y huellas de los documentos\n"]
    parts += [f"- `{name}` — SHA-256 `{sha(content.encode())}`" for name, content in documents]
    for name, content in documents:
        parts.append(f"\n\n---\n\n## SOURCE: {name}\n\n{content.rstrip()}\n")
    parts.append("\n---\n\n## Veredicto histórico de lotes reproducido desde episodios\n\n```json\n"
                 + json.dumps(verdict, indent=2, ensure_ascii=False) + "\n```\n")
    parts.append("\n## Configuraciones exactas del panel archivado\n\n"
                 "Snapshot del experimento, no importación del código actual.\n\n```json\n"
                 + json.dumps(meta["configs"], indent=2, ensure_ascii=False) + "\n```\n")
    return "\n".join(parts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verifica evidencia y vigencia del contexto sin escribir")
    args = parser.parse_args()
    verdict, meta = verify()
    context = build_context(verdict, meta)
    if args.check:
        require(OUTPUT.exists() and OUTPUT.read_text() == context,
                "El contexto falta o está desactualizado: ejecutar sin --check")
    else:
        OUTPUT.write_text(context)
    print(f"OK lotes históricos: 3.840 episodios, noop exacto 960/960, IC95 reproducidos; {verdict['verdict']}.")
    print(f"Contexto {'verificado' if args.check else 'generado'}: {OUTPUT} ({len(context.encode()):,} bytes)")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError, tarfile.TarError) as error:
        raise SystemExit(f"ERROR: {error}") from error
