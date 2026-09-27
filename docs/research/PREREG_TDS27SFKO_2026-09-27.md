# Pre-registro — tds27sfko: rompe-espejos sobre la versión nueva de tetsutani

Escrito antes de evaluar. 2026-09-27 ~03:40 UTC.

- **Contexto:** tds27 (tetsutani 27-sep 00:38, "step1009...fixedsell_closure", sha
  55be5d5f) gana 30-2 a top3cc y 24-8 a cha22sfko; 84% global (torneo_tds27). Es
  determinista con la semilla de hash (0 turnos distintos) y no trae recortes de fin.
- **Candidata:** tds27 + `_33_seedfloat` + `_33_knock` (`apilar_fin_partida.py`).
- **Evaluación:** `torneo.py --out results/torneo_tds27sfko --vs tds27,tds27sfko`,
  semillas 3810000-3810015 (16 nuevas), dos asientos. Pool: top3cc, cha22sfko,
  cha22, top3, arshs3, hl74, guru4, tds22.
- **Regla (igual que cha22sfko):** adoptar si (a) directo tds27sfko vs tds27 con IC95
  por semilla > 50%, y (b) pool con punto ≥ 0 y límite inferior dos vías > −5 pp.

## Resultado (torneo_tds27sfko, 544 partidas, 0 errores)

Directo 1-1-30 vs tds27; pool 0/128 celdas cambian. **INERTE → REJECTED.** El cierre
propio de tds27 ("fixedsell_closure") ya evita las compras que recortan SF/KO.
