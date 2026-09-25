# Evidencia del loop continuo

Estado vivo: `pipeline_state.json`. Los manifiestos de cada torneo distinguen
running/complete/failed; no analizar resultados parciales para decidir candidatas.

- `variants.json`: ocho variantes de loop1; `pilot.*`: 1.000 episodios completos.
- `pilot.results.json`: pred_top3 y pred_fast2 seleccionadas según preregistro.
- `pilot.behavior.json`: diferencia de acciones por episodio, separada de W/L/T.
- `pilot.pred_top3.mechanism*`: dos episodios exactos, transacciones conciliadas.
- `recovery_smoke.json`: primer prototipo no recupera la planta.
- `recovery_turn_smoke.json`: segundo la recupera, pero cambia tiendas/RNG;
  prueba de ejecución, no benchmark frente al rival adaptativo.
- `recovery_variants.json`, `tomato_variants.json`: candidatas del piloto2.
- `herd_variants.json`: candidatas del piloto3 encadenado tras pipeline1/2.
- `submissions_snapshot.json`, `vq_episodes_snapshot.json`: consulta de ladder.
- `vq_replay_selection.json`: selección previa por recencia, sin filtrar resultado.
- `vq_replay_diagnostics.json`: tres partidas identificables, un self-match
  excluido por asiento ambiguo; no sustituye el WR histórico.
- `real_loss_cashflow.json`: resumen de ledgers exactos de la ronda anterior;
  ventas brutas de trigo no equivalen a producción (hay compras/reventas).
- `PUBLIC_SOURCES.md`, `atlas_source.json`: fuentes e interpretación fechada.

Para comprobar cualquier bloque completo sin simular:

```bash
./.venv/bin/python validar_torneo.py docs/evidencia/loop_publicos_20260925/pilot
```

Cada `.sources.tgz` conserva el runner y los agentes exactos por hash. Los
JSONL de episodios guardan hashes de acciones antes del motor. Los informes
pareados excluyen otros brazos experimentales, nunca rivales elegidos por resultado.
Los intervalos CGM indefinidos se guardan como null, no como ausencia de incertidumbre.
