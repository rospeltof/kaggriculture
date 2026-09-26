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

## Resultado (torneo_cc3eval, 816 partidas, 0 errores, semillas 3700000-023)

Ponderado **−2,16 pp, IC95 [−12,80; +8,49]** → **REJECTED**. cha22 −4,2; arshs3 −6,3;
harvest −4,2; resto +4,2; directo 37,5%. La contra-biblioteca se satura con los
primeros 330 episodios.

## Nota posterior (sonda de hash, 2026-09-26 21:30 UTC)

cha22 y top3cc producen las mismas 719 acciones con PYTHONHASHSEED 0, 1 y 2: las
"casi-copias" del censo son variantes reales de otros equipos, no deriva de hash.
Las copias exactas de cha22 del ladder juegan igual que el cha22 local.
