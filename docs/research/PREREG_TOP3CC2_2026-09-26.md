# Pre-registro — top3cc2: biblioteca PREDICT con los linajes frecuentes

Escrito antes de evaluar. 2026-09-26 ~20:50 UTC.

- **Base:** top3cc (activa 56588419, sha e60ec15c).
- **Candidata top3cc2:** + episodios de top3cc contra hl74, hl59 (Harvest Ledger),
  arshs3, vq, guru4, tds22, lynni: 40 semillas por rival × 2 asientos, semillas de
  construcción 3300000-3300279 (disjuntas de la evaluación).
- **Motivo:** en el bloque 2 de top3cc, arshs3 −5,2 y harvest −4,2 (no
  significativos) y resto +8,3; la biblioteca original no contiene esos agentes.
- **Evaluación:** `torneo.py --out results/torneo_cc2eval --vs top3cc,top3cc2`, semillas 3400000-3400023 (24),
  dos asientos, mismos 8 rivales y pesos que `pesos_censo_0926.json`.
- **Regla:** adoptar top3cc2 si el delta ponderado tiene IC95 por semilla > 0 y
  ningún linaje tiene IC95 entero < −10 pp. Si no, se queda top3cc.

## Resultado (torneo_cc2eval, 816 partidas, 0 errores, semillas 3400000-023)

Ponderado **+0,72 pp, IC95 [−6,35; +7,78]** → **REJECTED** (se queda top3cc).
Linajes: cha22 0,00; arshs3 +4,2; harvest −8,3; resto +5,6. Directo 39,6%.
Nota: en estas semillas top3cc gana ~62% a cha22 (91,7% en el bloque 2 de top3cc):
la varianza entre conjuntos de semillas es grande; estimación combinada ~75%.
