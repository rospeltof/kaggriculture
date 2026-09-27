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

## Resultado (torneo_tds27cc, 816 partidas, 0 errores)

Ponderado **−4,79 pp, IC95 [−14,35; +4,76]** → **REJECTED**. tds27 −2,1; cha22 −6,3;
arshs3 −12,5; harvest 0; resto −5,2; directo 41,7%. tds27 ya integra PREDICT afinado
por su autor: añadir episodios no ayuda. Referencia del mismo bloque: tds27top3 gana
42-6 a cha22, 42-6 a top3cc y 24-16-8 a tds27.
