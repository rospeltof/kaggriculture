# Pre-registro — tds27cc: biblioteca PREDICT de tds27top3 ampliada con tds27 y cha22

Escrito antes de evaluar. 2026-09-27 ~04:00 UTC.

- **Base:** tds27top3 (activa 56596228). **Candidata:** + episodios de tds27top3 vs
  tds27 y vs cha22 (120 semillas × 2 asientos cada uno; semillas de construcción
  3900000-3900239, disjuntas).
- **Precedente:** la misma operación dio a top3cc +28 pp ponderado (+50 vs cha22).
- **Evaluación:** `torneo.py --out results/torneo_tds27cc --vs tds27top3,tds27cc`,
  semillas 3950000-3950023 (24 nuevas), dos asientos; rivales y pesos de
  `pesos_anticipados_0927.json`.
- **Regla:** adoptar si el delta ponderado tiene IC95 por semilla > 0 y ningún
  linaje tiene IC95 entero < −10 pp. Uso previsto: segundo slot (en lugar de top3cc).
