# Pre-registro — capa FR (adelantarse a las compras de trigo de la cinta)

Escrito antes de evaluar. 2026-09-28 ~02:40 UTC.

- **Hechos:** en replays reales, Jun_value y David Goldrajch compran en t−1 lo que nuestra
  cinta compra en t y lo venden en t en el índice 9 (+$8-11k por partida). Las compras
  grandes vienen de la cinta (rutas 103, 104, 112, 124: 7 de 64 pares, ~11% de partidas).
- **Brazos:** ref = combo (activa 56625348); fr = combo + FR con ataque; frdef = combo + FR
  solo defensa (pre-compra propia, sin especulación). `apilar_frontrun.py`.
- **Semillas:** las 43 de 4200000-4200299 cuyo par usa esas rutas (seleccionadas por par, no
  por resultado; `results/exp_0928/semillas_trigo.json`), dos asientos. Rivales: tds27,
  cha22, hl836 (seguidores de cinta).
- **Regla:** adoptar fr (o frdef) si el delta pareado en estas partidas tiene IC95 por semilla
  > 0 contra el conjunto de rivales. Fuera de estas rutas la capa no actúa (sin compras ≥ 20
  en la cinta), así que el efecto global = efecto aquí × ~11%.
