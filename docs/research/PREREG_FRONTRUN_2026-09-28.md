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

## Resultado (torneo_fr1, 774 partidas, 0 errores)

fr: **+37,21 pp, IC95 por semilla [+26,25; +48,17]**; 51/129 celdas cambian, **51 a favor,
0 en contra**; cha22 +44,2, hl836 +46,5, tds27 +20,9. frdef (solo pre-compra): mismo W/L.
Márgenes medios (ref → frdef → fr): tds27 +110 → +4.314 → +5.135; cha22 −421 → +1.736 →
+1.740; hl836 −16 → +4.187 → +5.001. **Veredicto: ADOPTAR fr.** Efecto global esperado
≈ 11% de partidas × ~65% rivales seguidores de cinta × 37 pp ≈ +2-3 pp, más la defensa
frente a especuladores tipo Jun_value/David Goldrajch.

## Notas del mismo día
- Oráculo de ventas con la cinta propia en PREDICT (`apilar_predict_cinta.py`): inerte; la
  cinta queda entre el 9º y el 32º de 49 candidatos (tds27 se aparta de su cinta al vender).
- "Trigo primero" (orden de mercado): +0,62 pp [−0,65; +1,90], no adoptado.
