# Estado de investigación — leer primero para continuar

Actualizado: 2026-09-22 03:20 (America/Bogota). Deadline 2026-09-30. Rank ~4589/9776.
Loop autónomo autorizado por el usuario (mensaje del 2026-09-21): harness + ladder
como evidencia complementaria, submissions como instrumento (5/día).

## BEST_CURRENT_CHAMPION

**CHAMPION_CANDIDATE: `tree_v1`** — 56444202, **1.082 @40 ep, 31-9 (78%)** en ladder.
Desactivada al subir su sucesora. Champion formal aún `maj_107674293` (56245770,
857, 126 ep) hasta que 56447472 confirme.

**En ladder ahora:** `tree_v1+guardias` (56447472, commit 98f9ea6, predicción ≥1.082)
y `maj+guard6` (56444505, 53% @32 ep).

## RESEARCH_FRONTIER (estados)

| id | qué | estado | evidencia |
|---|---|---|---|
| `maj+guard6` | cinta campeona + guardia de caja d0 | **VALIDADO en ladder** — 56444505: 32/32 con 4 manos, 17-15 (53%) vs 40% | rating 714 @32 es dinámica de arranque, no rendimiento |
| `tree_v1` | árbol 4 cintas Majkel, ramas por tienda d3/d6 | **CHAMPION_CANDIDATE** — 56444202: 31-9 (78%), 1082 @40 | local +6..+9 global pero **+10 vs fuertes**; ladder confirma |
| `tree_v1+guardias` | lo anterior + guard_cash + guard_commitments | **REAL_WORLD_CANDIDATE** — sub **56447472** (2026-09-22 03:10) | combinación de validados (#6); 8/9 derrotas del tree eran manos d1 |
| `107570947` (cinta sola) | mejor cinta del successive halving | **PROMISING** | compare2: +13,1 global; **+21,5 vs fuertes [5,7; 37,3]**, −0,6 vs débiles. Panel fuerte en curso |
| `tree_v2` | árbol 30 victorias Majkel, NN sobre tiendas | **PROMISING→REJECTED como está**: +4,8 [−5,0; +14,7], < v1 < cinta | defecto: cambia entre cintas con prefijos distintos (12 prefijos) → estado inconsistente al ramificar. Arreglable: ramificar sólo entre cintas con prefijo idéntico |
| `mejor cinta sola` | successive halving sobre 30 victorias como cintas fijas | **EN CURSO** — piloto `tapes` 4 seeds (4.096 ep) | compare dice cinta sola > árboles localmente |
| `tree_v3` | árbol con cintas de DSM/UMG/Vadim (top-3, 2850-2880) | **PENDIENTE** — replays bajando | — |
| `tree_liquid` | árbol + ventas reactivas | PROMISING (empató con tree en piloto, 0 cambios de W/L/T) | no confirmar solo |
| `warmstart10` | cinta hasta d10 + HOZ | PROMISING débil (+6,25 piloto, < cinta pura) | baja prioridad |
| matching por contexto (rival/hierbas) | elegir cinta por más que la tienda | idea, no implementada | LOW confidence |

## REJECTED (resumen; detalle en RESEARCH_BELIEFS.md y BITACORA.md)

Todo el espacio de perillas del chasis (13 barridos), gansos, ventas retenidas,
fertilizar un corte, superficie, rebaño, plantilla, copiar por piezas, cadencia,
compete_aware, compra parcial, harvest_76, apertura dentro del planner.

## PROCESOS EN CURSO (al escribir esto)

- `evaluar_lider.py --phase tapes --seeds 4` → `results/tapes_piloto.txt`, evidencia
  `docs/evidencia/lider_20260914/tapes.*`. **No tocar fuentes hasta que termine.**
- Terminados: compare (resultados arriba), descargas (DSM 40, UMG 30, VADIM 30,
  MAJTAPE_LADDER 60 en `replays/`).

## HALLAZGOS DE HOY (resumen; detalle en RESEARCH_BELIEFS.md)

1. **Manos d1 → resultado** (60 reales): 0-2 manos 0%, 3: 23%, 4: 60%. Guardia
   `bots/guardia_cinta.py` reserve=6. Sólo d1 (d2 residual 3/60; d3+ ninguno).
2. **Divergencia harness/ladder**: 71,5% local vs 40% real. Cintas pasivas no
   mueven el mercado d0.
3. **Tienda d3 explica derrotas** de la cinta fija: 60% BAKERY … 14% PIZZA.
4. **DSM vs Majkel 3-6**; cima decidida por 1-5%. Cintas de DSM no son mejor materia.
5. **compare**: cinta +12,1 > tree +9,0 > tree_v2 +4,8 (vs HOZ). Más cintas mezcladas, peor.

## NEXT_EXPERIMENTS (orden)

1. Leer piloto `tapes` → top-3 cintas a `--phase confirm` (16 seeds). Si alguna
   supera a 107674293 con IC dos vías > 0 → nueva cinta base (+guardia) al ladder.
2. Leer 56444505 (guardia) y 56444202 (tree v1) a ~60 ep → HARNESS_VS_LEADERBOARD.
   Predicción guardia: claramente > 852,6 si las manos d1 eran la causa dominante.
3. Si guardia transfiere Y tree v1 ≥ cinta en ladder → `tree_v1 + guard` (combinación
   de validados, criterio #6).
4. Arreglar `tree_v2`: ramificar sólo entre cintas con prefijo IDÉNTICO hasta el
   paso de ramificación (agrupar por hash de prefijo). Medir vs tree v1.
5. `tree_liquid` (ventas reactivas) al ladder si hay slot: 0 efecto local por
   rivales pasivos — mismo patrón de divergencia que la guardia.
6. Ampliar guardia al d1 (until_step=48) si 56444505 muestra déficit residual en d2.

## HARNESS_VS_LEADERBOARD (dataset acumulado)

| exp | local delta (vs HOZ) | ladder | transferencia |
|---|---|---|---|
| campeona_grano (seed_stock_aware) | +6,4 | 772 vs hoz 677 | ruido de ladder ±40; no concluyente |
| campeona_hoz (+harvest_76) | +2,5 (falso: −0,08) | 677–831 según fecha | ruido |
| **maj_107674293** | **+14,36** | **852,6** | **SÍ: salto grande transfiere** |
| tree_v1 | +17,97 (piloto) | pendiente | — |

Lección provisional: el ladder sólo resuelve saltos ≥ ~100 Elo; el harness sólo
efectos ≥ ~7 puntos. Buscar cambios GRANDES, no micro.

## HIGH_UPSIDE_HYPOTHESES

- **H1 (VERY HIGH / MEDIUM):** una cinta fija de un agente de 3075 rinde 852 → el
  valor está en la adaptación. Cuantas más cintas y mejor matching de contexto,
  más cerca del agente original. `tree_v2`/`tree_v3` prueban esto.
- **H2 (HIGH / LOW):** las cintas de los top-3 actuales (≈2870) son mejores
  materia prima que las de Majkel (sub a 2652).
- **H3 (HIGH / LOW):** el rival explota a la cinta de forma identificable en los
  replays reales (p. ej. inunda el producto que la cinta vende tarde). Si es así,
  una capa reactiva mínima (ventas) sobre la cinta lo corrige.
