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
