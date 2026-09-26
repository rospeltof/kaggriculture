# Pre-registro — top3cc3: doble cobertura de cha22 en la biblioteca

Escrito antes de construir y evaluar. 2026-09-26 ~21:50 UTC.

- **Base:** top3cc (activa 56588419). **Candidata:** + 330 episodios más de top3cc vs
  cha22 (semillas de construcción 3600000-3600164; disjuntas de toda evaluación).
- **Motivo:** ~5 episodios de cha22 por par de tiendas; el pronóstico usa los 3 que
  mejor encajan. Su ventaja contra cha22 varía mucho entre conjuntos de semillas
  (91,7% en 3200000-023; ~62% en 3400000-023).
- **Evaluación:** `torneo.py --out results/torneo_cc3eval --vs top3cc,top3cc3`,
  semillas 3700000-3700023 (24), dos asientos, rivales y pesos de `pesos_censo_0926.json`.
- **Regla:** adoptar si delta ponderado con IC95 por semilla > 0 y ningún linaje con
  IC95 entero < −10 pp.
