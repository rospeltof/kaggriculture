# Evidencia de la revisión — 2026-09-25 UTC

- `*_episodes_snapshot.json`: listados API antes de enviar VQ; ratings y edad observada.
- `envio_vq.json`, `submissions_after_vq.json`, `vq_status_check.json`: VQ 56535264, recepción y validación.
- `replay_selection.json`: selección por recencia de 16 arshs3 + 8 v13, sin filtrar resultado.
- `replay_diagnostics.json`: resultados, granjas y escapes por transición; stocks cotizados no son ingresos ejecutados.
- `forecast_probe.json`: sonda original con la métrica incompleta de coincidencias en t+1..t+4; se conserva para auditar el error.
- `forecast_signals_validated.json`: corrección usando ventas aceptadas, incluyendo t. Cuatro replays reproducidos en 720 estados.
- `real_*.ledger.jsonl.gz`: ventas/compras y costes efectivos de esas reproducciones; caja conciliada.
- `forecast_mismatch.json`: única acción de la sonda que difiere de lo grabado (SELL WHEAT en 623). La validación del ledger utiliza acciones grabadas y sí es exacta.
- `forecast_failure*`: sonda causal local en la primera celda ordenada donde base gana y gate pierde; no es selección de candidato.
- `loader_check.json`: instrumentación nueva frente al loader oficial, acciones/rewards idénticos.
- `forecast_pilot.*`, `public_refresh.*`: episodios, manifiestos y fuentes archivadas de los bloques nuevos. Sólo analizar si state=complete.
- `submissions_final_snapshot.json`: lectura posterior al cierre; VQ todavía joven, no inferir fuerza del rating inicial.
- `public_refresh_results.json`: ambas versiones no seleccionadas, intervalos amplios y criterio registrado incumplido.
- `forecast_results.json`: gate y off vs VQ; controles y cobertura en `*.validation.json`.
- `new_public_versions.json`, `public_notebooks.json`: descubrimiento fechado de cambios de versión; las fuentes exactas del torneo se conservan dentro de `.sources.tgz`.

Los replays originales están en `replays/` (ignorado por Git). Los resúmenes,
ledgers y fuentes de los torneos están aquí, fuera de esa exclusión. Para repetir
la sonda original hacen falta sus JSON; para revisar resultados de torneos bastan
los manifiestos, JSONL, archivo de fuentes y versión del motor.

Verificar un bloque sin simular:

```bash
./.venv/bin/python validar_torneo.py docs/evidencia/research_20260925/forecast_pilot
./.venv/bin/python validar_torneo.py docs/evidencia/research_20260925/public_refresh
./.venv/bin/python pareado_torneo.py docs/evidencia/research_20260925/forecast_pilot.jsonl base gate noop,off
```

Las exclusiones de pareado son los otros brazos, no rivales seleccionados por resultado.
Los tests y resúmenes no convierten un pool de forks emparentados en muestra del ladder.
