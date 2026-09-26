# Pre-registro — cha22cc: cha22sfko + PREDICT de top3 con biblioteca contra-cha22

Escrito antes de evaluar. 2026-09-26 ~21:30 UTC.

- **Candidata:** `construir_cha22cc.py` (sha 1a8bf9cc): cha22sfko + capa PREDICT de
  top3 (forecast4, TOP=3) + biblioteca de top3cc. Sonda seed 3499999: +$96 vs cha22,
  3 disparos, 0 errores. (Una primera versión capturaba mal el padre y acababa con
  $3.000: detectado por la sonda, corregido antes de evaluar.)
- **Evaluación:** `torneo.py --out results/torneo_cha22cc --vs cha22sfko,cha22cc`,
  semillas 3500000-3500023 (24 nuevas), dos asientos. Rivales ponderados
  (`pesos_censo_0926_sin_sfko.json`): cha22 0,54; arshs3/vq 0,075; hl74 0,125;
  guru4/tds22/lynni 0,26. Extra informativo: top3cc.
- **Regla:** sustituir cha22sfko por cha22cc si el delta ponderado tiene IC95 por
  semilla > 0 y ningún linaje tiene IC95 entero < −10 pp.

## Resultado (torneo_cha22cc, 816 partidas, 0 errores)

Ponderado **−3,49 pp, IC95 [−11,51; +4,54]** → **REJECTED**. cha22 −6,3; arshs3 −4,2;
harvest −4,2; resto +2,8. cha22cc–cha22 41-7 frente a cha22sfko–cha22 44-4: PREDICT
estorba a las capas de adelanto de ventas propias de cha22. Extra: top3cc gana
37-11 a cha22sfko y 36-12 a cha22cc.
