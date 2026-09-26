# Pre-registro — cha22 + recortes de fin de partida (rompe-espejos)

Escrito antes de ejecutar. 2026-09-26 ~20:10 UTC.

- **Motivo:** cha22 es público y popular (tetsutani, Abhinav0370, flexonafft,
  haideptry, lynnsakurai). En el ladder se cruzará con copias; dos copias empatan
  (lynnw-cha22 0-0-20). Cualquier ventaja determinista ≥ $1 convierte empates en
  victorias.
- **Candidata:** cha22 (sha 127ed3e6) + `_33_seedfloat_agent` + `_33_knock_agent`
  copiados de tds 22-sep (`apilar_fin_partida.py`, sha b887ea03). Sonda seed
  2699999: +$35 frente a cha22, 3 semillas de trigo recortadas, 0 errores.
- **Bloque:** `torneo.py --vs cha22,cha22sfko`, seeds 2610000-2610015 (16 nuevas),
  dos asientos. Pool (8): top3, vq, arshs3, guru4, hl74, lynni, field, tds22.
- **Regla (fijada antes):** adoptar cha22sfko en lugar de cha22 si (a) en el
  directo cha22sfko vs cha22 la tasa por semilla tiene IC95 > 50%, y (b) contra
  el pool el delta pareado tiene punto ≥ 0 y límite inferior dos vías > −5 pp.
  Si (a) sin (b): no adoptar (el rompe-espejos no puede costar partidas normales).

## Resultado (torneo_cha22fin, 544 partidas, 0 errores)

- (a) Directo: **cha22sfko 29-1-2 vs cha22 (93,8%)**, mayoría en 16/16 semillas. Cumple.
- (b) Pool: delta **+0,78 pp**, IC95 semilla [−0,88; +2,45], dos vías [−1,07; +2,63];
  1/128 celdas cambia (a favor, vs vq). Cumple.
- **Veredicto: ADOPTAR cha22sfko** (sha b887ea03) en lugar de cha22.
