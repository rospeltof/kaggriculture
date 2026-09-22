# Research beliefs — Kaggriculture

Actualizado: 2026-09-21. Cada entrada lleva su evidencia; cada evidencia nueva sube o baja la creencia.

## HIGH CONFIDENCE

- **[2026-09-22, 24 partidas REALES de 56449108] La cinta + guardias es una maquina de produccion FIJA (~100-107k) y gana sii el rival produce menos.** Banco identico en V y D en cada dia (d12 9.7k, d16 33k, d29 100-107k). En las derrotas hacemos MAS dinero (107k) que en las victorias (100k); el rival hace 113k vs 73k. Los que nos ganan van al doble en d12 (19k vs 9.7k), los alcanzamos en d18 y nos pasan en d21-25 con ~5-7% mas de produccion tardia. **El techo de una cinta es el plan que copia.** Ya no hay fragilidad mecanica: 24/24 con 4 manos y 3 cuadrantes, derrotas ajustadas.

- **[2026-09-22, 40 partidas REALES] El arbol por tiendas transfiere y CORRIGE el desajuste de tienda.** tree_v1 (56444202): 31-9 (78%), 1082 @40 ep. Gana justo donde la cinta fija perdia: PIZZA 6-1 (cinta 1-6), BRUNCH 5-1 (1-3), SMOOTHIE 4-1 (4-7). Sus 9 derrotas: 8 son fallos de manos del d1 (1-3 manos: 1V-8D; con 4 manos: 30-1).
- **[2026-09-22, 32 partidas REALES] La guardia de caja funciona mecanicamente (32/32 con 4 manos) y mejora el WR: 53% vs 40% del campeon reciente, margen de dinero en positivo.** Coherente con la aritmetica (+16 esperado, +13 observado). La correlacion manos->resultado era causal al menos en parte.
- **[2026-09-22] NO leer el rating de una submission joven; leer su W/L y la fuerza de sus rivales.** La guardia estaba en 714 @32 ep con 53% de WR porque una submission nueva juega contra rivales flojos hasta subir; tree_v1 en 1082 @40 con 78%. Casi descarte la guardia por el rating. El rating converge con ~100+ episodios; el W/L es legible desde ~30.

- **[2026-09-21, 60 partidas REALES] Las manos del d1 predicen el resultado de una cinta.** 0-2 manos: 0% WR (12 partidas); 3: 23% (13); 4: 60% (35). Causa: cuatro `BUY_SEED WHEAT 1` en los pasos 18-21 dejan la caja en \$0..\$9 al alba y fib(n) necesita \$7 para 4 manos. Tres catastrofes (\$8k-23k) con trayectoria identica: \$0, 8 HIRE fallidos, 1 mano. **Arreglo: `bots/guardia_cinta.py` reserve=6** (sub 56444505).
- **[2026-09-21] DIVERGENCIA HARNESS/LADDER identificada: 71.5% local vs 40% real para la misma cinta.** Mecanismo: las cintas pasivas del panel no mueven el mercado del d0; los rivales reales si, y eso decide si hay \$7 en el paso 25. Localmente solo el 15% de partidas cae a <4 manos; en el ladder el 42%. **El panel subestima sistematicamente la fragilidad de las cintas al contexto de mercado temprano.**
- **[2026-09-21] La tienda del d3 explica las derrotas de una cinta fija.** maj_107674293 (original con YARN_STORE): 56-60% WR con YARN/BAKERY, 14% con PIZZA, 25% BRUNCH, 33% ICE_CREAM. Es desajuste de contexto puro; el arbol por tiendas ataca exactamente esto.
- **[2026-09-21] En la cima (DSM/Majkel/UMG, ~2850-3075) las partidas se deciden por 1-5%.** DSM vs Majkel 3-6 con margenes de \$300-5.000 sobre ~\$100k. Una cinta que pierde 10-30% por contexto cae a ~850 aunque venga de un agente de 3075.

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

- **[2026-09-22] Ninguna de las 27 victorias de DSM (n1, 3174) supera a 107570947 como cinta fija** — ni en piloto (75.5% vs 67.4%), con 27 candidatas contra 1 referencia. Con 30 Majkel-2652 + 12 Majkel-3075 + 27 DSM: **107570947 es la mejor cinta fija de ~70 candidatas de los 3 mejores jugadores. El enfoque de cinta fija ha tocado techo (~1200 Elo).**
- **[2026-09-22] Lo que Majkel cambio entre 2652 y 3075 (diff de cintas):** 3er cuadrante en d6 en vez de d9; menos animales (14 vs 20 a d12) con menos ovejas (3 vs 9) y mas gansos (4 vs 2); mas zanahoria (72 vs 41) y tomate (10 vs 0); vende huevo (162 vs 0) y casi nada de lana. **Va exactamente hacia los productos que SUBEN con rival (hinge/log) y lejos de la lana (-65%)** — lo que nuestro `compete_aware` intento y el chasis no supo ejecutar. Como cinta fija no supera a 2652: el beneficio esta en ejecutar ese plan REACCIONANDO.
- **[2026-09-22] La cinta+guardias no deja nada en la mesa que una capa barata recupere:** cierre limpio (\$82 sin vender, \$466 en pie = 0.6%); acciones fallidas por desajuste de campo 0.1-1.0%; unico recurso libre: 4.7% de mano-turnos sin orden (5o peon), +2-4% como mucho y con riesgo de interferir.

- **[2026-09-22] Las cintas de Majkel ACTUAL (3075) NO son mejores cintas fijas que las de Majkel-2652.** Confirmacion pareada (71 fuertes x 8 seeds): mejor +1.85 [-26; +30] vs 107570947. Y sin embargo Majkel actual como AGENTE gana 85% a nuestra cinta por \$30k. Inferencia: **el valor anadido entre versiones esta en la adaptacion al contexto, no en la secuencia.** La siguiente palanca es reactiva (precios/ventas), no mas cintas del mismo autor.
- **[2026-09-22] Un piloto de 4 semillas sobre N candidatos siempre infla al mejor.** majkel2: +10.7 -> +1.85 al confirmar; tapes: +18.0 -> -3.1. El successive halving con confirmacion pareada en el mismo bloque es obligatorio.

- **[2026-09-22] Segunda clase de filo de navaja: compromisos de capital a paso fijo (BUY_LAND/BUY_ANIMAL) sin recuperacion.** La cinta 107606658 falla el 2o cuadrante por \$193 y toda la expansion muere (\$26-49k). `guard_commitments` (reintento hasta 48 pasos) la lleva a \$61-81k con 3 cuadrantes. En el campeon rara vez actua (57/60 compras reales entraron; cuando actua, +23k neto en 4 partidas locales). Importa mas para las cintas de caja apretada del arbol.

- **Ramificar la cinta por tiendas (arbol) generaliza mejor que una cinta fija.** Piloto: tree = cinta (64.06%). Confirmacion con 16 seeds en curso (compare). Ladder: 56444202 pendiente.
- **La unica rama estrategica VISIBLE de la politica del lider es la tienda (step 72, 144, ...).** El `town` esta vacio antes; las divergencias en pasos 20-36 son reacciones a la caja (BUY_SEED MELON 2 o no), no ramas.
- **Una cinta fija de un agente de 3075 rinde ~850 en el ladder.** El valor del agente esta en la adaptacion al contexto (rival, campo, mercado), no en la secuencia. Reducir el desajuste de contexto (mas cintas, mejor matching) deberia acercar el arbol al agente original.
- **La economia del lider es un PAQUETE coordinado** (2 vacas + 3 ovejas turno 1-2, 12 melones, tierra d6, compra forraje, 13-22 animales) que nuestro chasis no reproduce por piezas: cada pieza probada por separado pierde.
- **La brecha con el top se abre en d12-d16** (vamos por delante en d12; ratio 0.51 en d16, 0.67 despues). Causa inmediata: plantamos melon 2.6 dias y fresa 4.2 dias tarde. Tres arreglos mecanicos (scorer, forraje, lotes) fallaron; el arbol del lider lo resuelve de raiz.

## LOW CONFIDENCE

- Mas cintas (30 victorias, tree_v2) > 4 cintas (tree_v1). Se mide ahora.
- ~~Las cintas de DSM/UMG/Vadim pueden ser mejores materia prima que las de Majkel.~~ **Bajada:** DSM pierde 3-6 contra Majkel en directo; misma liga. Y mezclar politicas rompe la coherencia de prefijos del arbol. Se descarta salvo hueco de cobertura.
- Matching por mas contexto que la tienda (acciones tempranas del rival, malas hierbas) podria reducir mas el desajuste.

## DISPROVEN

- Gansos/huevos (-49.4). Aguantar producto para vender mejor (gradiente monotona hasta -10). Fertilizar cultivos de un corte (-29.4). Mas superficie / cuarto cuadrante (-8/-14). Rebano 6..16 (todo negativo, optimo 8). Plantilla 9..15 (optimo 12). Copiar composicion del lider por piezas (7 de 7). `hire_by_work` (-17.8). Quitar forraje temprano (-45.6). Cadencia de riego con o sin poda de ruta (-21.8). Reordenar prioridades (mejor +2.5 = ruido). Compra parcial (+0.23 al replicar). harvest_76 (-0.08). compete_aware (-12.8). Asimetria de asiento (0). Optimizar la apertura DENTRO de nuestro planner (techo ~0.6% del dinero final).
- "Nuestro mejor intento es un replay" NO es una anomalia: el meta de esta escalera (C90-C95) ya eran cintas.
