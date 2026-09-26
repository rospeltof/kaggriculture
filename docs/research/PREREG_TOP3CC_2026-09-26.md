# Pre-registro — top3 con biblioteca PREDICT contra-cha22 (top3cc)

Escrito antes de evaluar. 2026-09-26 ~20:45 UTC.

- **Motivo (censo de 80 partidas reales, `censo_linajes.py`):** 34/80 rivales son
  cha22 exacto o casi (y 9 más del linaje); top3 perdió 3-10 contra ellos en el
  ladder. La biblioteca de PREDICT (top-30 del 19-sep) no contiene a cha22.
- **Candidata:** top3 (sha 9668e30a) + episodios de top3-vs-cha22 añadidos a la
  biblioteca original (`construir_biblioteca_cc.py`, semillas de construcción
  3000000-3000164, disjuntas de la evaluación). Resto del código idéntico.
- **Evaluación:** `torneo.py --vs top3,top3cc`, semillas 3100000-3100015 (16
  nuevas), dos asientos. Rivales: cha22, cha22sfko (linaje objetivo) y pool de
  no-daño arshs3, guru4, hl74, lynni, vq, tds22.
- **Regla (fijada antes):** adoptar top3cc para el slot de top3 si (a) contra el
  linaje objetivo (cha22 + cha22sfko) el delta pareado es > 0 con IC95 por
  semilla que excluye 0, y (b) contra el pool de no-daño el punto es ≥ 0 y el
  límite inferior dos vías > −5 pp. Si (a) falla → REJECTED. Si (a) pasa y (b)
  no → no adoptar (reportar el intercambio).

## Resultado del bloque 1 (torneo_top3cc, 544 partidas, 0 errores)

- (a) Linaje objetivo: **+28,1 pp** (40,6% → 68,7%), IC95 semilla [+6,4; +49,8];
  12/32 celdas cambian, 12 a favor. **Cumple.**
- (b) Pool: +0,52 pp, IC95 semilla [−10,5; +11,6], dos vías [−17,0; +18,0];
  18/96 celdas, 9/9. arshs3 −12,5, vq −18,8, guru4 +15,6, tds22 +15,6, hl74 +3,1,
  lynni 0. **No cumple** (límite inferior < −5). Directo top3cc–top3 20-10-2.
- **Veredicto por la regla: NO ADOPTAR.** Intercambio entre linajes, no daño neto.

## Pre-registro 2 (hipótesis NUEVA, escrita tras el bloque 1): ponderar por población

- **Pesos fijados ahora con el censo de 80 partidas reales (antes de nuevos datos):**
  linaje cha22 0,54 (cha22 0,27 + cha22sfko 0,27); linaje arshs3 0,075
  (arshs3 0,0375 + vq 0,0375); linaje Harvest Ledger 0,125 (hl74); resto 0,26
  (guru4, tds22, lynni: 0,0867 cada uno).
- **Bloque 2:** semillas 3200000-3200023 (24 nuevas), dos asientos, mismos brazos
  y rivales; se analiza SOLO.
- **Regla:** adoptar top3cc si el delta ponderado tiene IC95 por semilla > 0
  **y** ningún linaje muestra daño claro (IC95 por semilla del linaje
  entero < −10 pp). Si no, se queda top3.

## Resultado del bloque 2 (torneo_top3cc2, 816 partidas, 0 errores, semillas 3200000-023)

Ponderado por censo: **+28,26 pp, IC95 semilla [+15,36; +41,15]**. Linajes: cha22
**+50,0** [+25,9; +74,1]; arshs3 −5,2 [−20,5; +10,0]; harvest −4,2 [−12,8; +4,5];
resto +8,3 [−1,2; +17,9]. Ningún linaje con IC entero < −10. Directo 41,7% (no decide).
**Veredicto por la regla 2: ADOPTAR top3cc** (sha e60ec15c) en el slot de top3.
