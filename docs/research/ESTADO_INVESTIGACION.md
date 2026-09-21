# Estado de investigación — leer primero para continuar

Actualizado: 2026-09-21 22:10 (America/Bogota). Deadline 2026-09-30. Rank ~4589/9776.
Loop autónomo autorizado por el usuario (mensaje del 2026-09-21): harness + ladder
como evidencia complementaria, submissions como instrumento (5/día).

## BEST_CURRENT_CHAMPION

**`maj_107674293`** — submission 56245770, **852,6** (126 ep, convergida). Cinta fija
de Majkel1337 (episodio 107674293). Código: `submission/archivo/main_7894c0...py`.
Referencia local: `CAMPEONA_HOZ` (677,5 en ladder, cayendo).

## RESEARCH_FRONTIER (estados)

| id | qué | estado | evidencia |
|---|---|---|---|
| `tree_v1` | árbol 4 cintas Majkel, ramas por tienda d3/d6 | **REAL_WORLD_CANDIDATE** — sub **56444202** (2026-09-21 21:53) | piloto: 64,06% = cinta; confirmación en curso |
| `tree_v2` | árbol 30 victorias Majkel (sub 56142830), NN sobre secuencia de tiendas | **PROMISING** — panel `compare` corriendo (9.216 ep) | dispara y ramifica (6 semillas → 5 cintas finales) |
| `tree_v3` | árbol con cintas de DSM/UMG/Vadim (top-3, 2850-2880) | **PENDIENTE** — replays bajando | — |
| `tree_liquid` | árbol + ventas reactivas | PROMISING (empató con tree en piloto, 0 cambios de W/L/T) | no confirmar solo |
| `warmstart10` | cinta hasta d10 + HOZ | PROMISING débil (+6,25 piloto, < cinta pura) | baja prioridad |
| matching por contexto (rival/hierbas) | elegir cinta por más que la tienda | idea, no implementada | LOW confidence |

## REJECTED (resumen; detalle en RESEARCH_BELIEFS.md y BITACORA.md)

Todo el espacio de perillas del chasis (13 barridos), gansos, ventas retenidas,
fertilizar un corte, superficie, rebaño, plantilla, copiar por piezas, cadencia,
compete_aware, compra parcial, harvest_76, apertura dentro del planner.

## PROCESOS EN CURSO (al escribir esto)

- `evaluar_lider.py --phase compare --seeds 16` → `results/compare_arboles.txt`,
  evidencia en `docs/evidencia/lider_20260914/compare.*`. **No tocar fuentes hasta que termine.**
- `bajar_lider.py` para DSM_56307459 (40), UMG_56376259 (30), VADIM_56374127 (30)
  → `replays/<CARPETA>/`, log `results/bajar_top3.txt`.
- `bajar_lider.py 56245770 MAJTAPE_LADDER 60` → partidas reales de nuestra cinta,
  log `results/bajar_majtape.txt`.

## NEXT_EXPERIMENTS (orden)

1. Leer `compare`: si `tree_v2` > `tree` con IC dos vías > 0 → subir `tree_v2`
   (`empaquetar_arbol.py` necesita generalizarse a N cintas). Si empatan, subir
   igualmente por criterio #7 (distinguir en ladder).
2. Failure analysis REAL: clasificar las 60 partidas de MAJTAPE_LADDER (V/D,
   rival, tiendas, dónde se abre la brecha). Buscar qué explota a una cinta fija.
3. Clasificar replays de DSM/UMG/Vadim (`clasificar_lider.py` con OBJ = nombre),
   extraer cintas (`extraer_top1.py <Team> <CARPETA>`), construir `tree_v3`.
4. Cuando 56444202 pase de ~60 ep: comparar con 852,6 y actualizar
   HARNESS_VS_LEADERBOARD.

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
