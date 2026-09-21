# Research beliefs — Kaggriculture

Actualizado: 2026-09-21. Cada entrada lleva su evidencia; cada evidencia nueva sube o baja la creencia.

## HIGH CONFIDENCE

- **Las cintas del lider transfieren al ladder.** Panel +14.36 -> ladder 852.6 vs 677.5 de HOZ (56245770, 126 ep). Primera vez que panel y ladder coinciden en un salto grande.
- **Nuestro chasis esta en un optimo local afilado y la busqueda por perillas esta agotada.** 13 barridos (2026-09-03..06), todos negativos salvo `seed_stock_aware` (+6.4, replicado -6.25 en ablacion). Manos 12, animales 8, cuadrantes 3, ventas "tirar todo": cada dimension empeora en AMBOS sentidos.
- **El Elo es W/L/T; el margen de monedas no compra rating.** `endgame_reap` recupero \$509/partida y midio -0.2. Solo importa CUANDO entra el dinero (compone) y si voltea partidas.
- **Con 16 semillas el MDE es ~7 puntos; con 8, ~10.** Efectos de +2..+5 son invisibles para el harness aunque sean reales. `harvest_76` (+2.5) y compra parcial (+4.84) se adoptaron/casi con estadistico inflado y dieron 0 al replicar.
- **El panel es un diseno CRUZADO (40 cintas x N semillas); el estimador correcto es dos vias.** Tratar celdas como independientes infla t (2.96 -> 1.76 en harvest_76).
- **El rival nos cuesta ~38% de produccion (140.5k aislados vs 87.5k compitiendo).** Es competencia de PRECIO pura (mismas unidades, precios hundidos), concentrada en lana (-65%), melon (-35%), fresa (-19%). Pero los productos fragiles siguen valiendo 4x mas: mover la cesta hacia lo robusto pierde monotonicamente (`compete_aware` -2.5/-8.4/-12.8).
- **La escalera tiene +-40 de ruido a ~60 episodios.** hoz y grano son identicas en el 92% de episodios y la escalera las separa 30-43 puntos. Diferencias <50 entre submissions propias no informan.
- **No hay asimetria de asiento** (-0.2 sobre 19.208 episodios). Los paneles estan balanceados.
- **El 68% de nuestro riego no compra rendimiento, pero cortarlo es catastrofico** (-21.8): el agua es la carga util que amortiza el caminar; sin ella el circuito se dispersa.

## MEDIUM CONFIDENCE

- **Ramificar la cinta por tiendas (arbol) generaliza mejor que una cinta fija.** Piloto: tree = cinta (64.06%). Confirmacion con 16 seeds en curso (compare). Ladder: 56444202 pendiente.
- **La unica rama estrategica VISIBLE de la politica del lider es la tienda (step 72, 144, ...).** El `town` esta vacio antes; las divergencias en pasos 20-36 son reacciones a la caja (BUY_SEED MELON 2 o no), no ramas.
- **Una cinta fija de un agente de 3075 rinde ~850 en el ladder.** El valor del agente esta en la adaptacion al contexto (rival, campo, mercado), no en la secuencia. Reducir el desajuste de contexto (mas cintas, mejor matching) deberia acercar el arbol al agente original.
- **La economia del lider es un PAQUETE coordinado** (2 vacas + 3 ovejas turno 1-2, 12 melones, tierra d6, compra forraje, 13-22 animales) que nuestro chasis no reproduce por piezas: cada pieza probada por separado pierde.
- **La brecha con el top se abre en d12-d16** (vamos por delante en d12; ratio 0.51 en d16, 0.67 despues). Causa inmediata: plantamos melon 2.6 dias y fresa 4.2 dias tarde. Tres arreglos mecanicos (scorer, forraje, lotes) fallaron; el arbol del lider lo resuelve de raiz.

## LOW CONFIDENCE

- Mas cintas (30 victorias, tree_v2) > 4 cintas (tree_v1). Se mide ahora.
- Las cintas de DSM/UMG/Vadim (top-3 actual, 2850-2880) pueden ser mejores que las de Majkel (sub 56142830 a 2652). Replays bajandose.
- Matching por mas contexto que la tienda (acciones tempranas del rival, malas hierbas) podria reducir mas el desajuste.

## DISPROVEN

- Gansos/huevos (-49.4). Aguantar producto para vender mejor (gradiente monotona hasta -10). Fertilizar cultivos de un corte (-29.4). Mas superficie / cuarto cuadrante (-8/-14). Rebano 6..16 (todo negativo, optimo 8). Plantilla 9..15 (optimo 12). Copiar composicion del lider por piezas (7 de 7). `hire_by_work` (-17.8). Quitar forraje temprano (-45.6). Cadencia de riego con o sin poda de ruta (-21.8). Reordenar prioridades (mejor +2.5 = ruido). Compra parcial (+0.23 al replicar). harvest_76 (-0.08). compete_aware (-12.8). Asimetria de asiento (0). Optimizar la apertura DENTRO de nuestro planner (techo ~0.6% del dinero final).
- "Nuestro mejor intento es un replay" NO es una anomalia: el meta de esta escalera (C90-C95) ya eran cintas.
