# Pre-registro — tds27top3: _V92_P_TOP 1 → 3 sobre tds27

Escrito antes de evaluar. 2026-09-27 ~03:50 UTC.

- **Precedente:** top3 (TOP=3) ganó 20-0 a VQ (mismo agente, TOP=1) en torneo_0926a.
- **Candidata:** tds27 (sha 55be5d5f) + `_V92_P_TOP = 3` al final (sha fb31fb24).
  Sonda seed 3899998: +$79 vs tds27, 13 disparos, 0 errores. tds27sfko fue inerte
  en la misma sonda (empate exacto).
- **Evaluación:** `torneo.py --out results/torneo_tds27top3 --vs tds27,tds27top3`,
  semillas 3820000-3820015 (16 nuevas), dos asientos, pool: top3cc, cha22sfko,
  cha22, top3, arshs3, hl74, guru4, tds22.
- **Regla:** adoptar si (a) directo tds27top3 vs tds27 con IC95 por semilla > 50%,
  y (b) pool con punto ≥ 0 y límite inferior dos vías > −5 pp.

## Resultado (torneo_tds27top3, 544 partidas, 0 errores)

- (a) Directo tds27top3 vs tds27: 18-4-10 (71,9%), **IC95 por semilla [52,5; 91,3]**. Cumple.
- (b) Pool: **+3,12 pp**, IC95 semilla [−1,43; +7,68], dos vías [−2,84; +9,09];
  4/128 celdas cambian, las 4 a favor (guru4 +12,5, tds22 +12,5). Cumple.
- Tiempo: 2,9 ms medio por turno, máximo 336 ms (11 procesos en paralelo).
- **Veredicto: ADOPTAR tds27top3** (sha fb31fb24).
