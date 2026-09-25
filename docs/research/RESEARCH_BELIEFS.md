# Research beliefs — Kaggriculture

Actualizado: 2026-09-25 UTC. Cada entrada lleva su evidencia; cada evidencia nueva sube o baja la creencia.

## HIGH CONFIDENCE

- **[2026-09-25, confirm13] Mejorar pérdidas/caja no garantiza cambiar W/L/T.**
  1.600episodios, noop416/416: inputs1/2delta0. Cambian107/86acciones y el
  margen sube103/82veces, baja4cada una. Mecanismo activo pero gate incumplido;
  no cambiar después el criterio a dinero ni llamarlas inertes. Piloto+4,6875pp
  no se confirmó; evidencia confirm13y diagnóstico físico del piloto.


- **[2026-09-25, error temporal en loop17] Stock lleno ahora no implica
  bonus inútil esta noche.** En1039000, cap_full omite FEED682 por ver4huevos;
  HARVEST687 retira esos4 antes de producir. Resultado: cosecha700de2→1,
  total91→90. Modelo temporal incorrecto, aunque ejecución/noop pasan24juegos.
  Detenido antes del piloto; no es estimación W/L/T ni refutación de todo cap.
  Evidencia `capped_bonus_decision.json` y ledgers/unidades de desarrollo.

- **[2026-09-25, aperturas loop12] TomatoInsteadOfCow y MarketShock completo
  perjudican a top3 en este panel:** −80,46875/−64,0625pp,1.008episodios,
  noop192/192, ICdos vías completamente negativos. No confirmar/enviar estas
  fuentes. Tomate aumenta propio dinero en un caso adverso, pero cambia tiendas
  y aumenta más el dinero rival. Dinero bruto no equivale a mejora competitiva.
  EarlyCycle cambia128/128acciones pese a delta0: no llamarlo inerte.

- **[2026-09-25, pérdida en campo] No todo cap se arregla cosechando más.**
  Doce replays top3 reproducidos exactamente:33MILK truncados al primer yield
  de vacas tardías con inventario previo0; es exceso de banco de cuidado.
  Sólo14EGG se truncan con inventario acumulado; su rescate necesita ruta y
  entrega.3CARROTperdidas por decay,1por sequía y4MILKmaduras en campo al final.
  No es ingreso marginal realizable ni cobertura universal. Ver
  `AUDITORIA_PERDIDAS_CAMPO_2026-09-25.md` y `field_loss_audit.json`.

- **[2026-09-25, PASS auditado] Ocio emitido no equivale a trabajo marginal
  perdido.** Ocho replays top3 ya seleccionados,720estados exactos cada uno:
  al cerrar el día no queda CARE omitido en un animal alimentado con futuro
  útil entre las oportunidades de la misma tile.60casos sin WATER no añaden
  producción inmediata/al siguiente amanecer ni evitan muerte esa noche.
  No prueba ausencia de mejoras de rutas o efectos posteriores. Evidencia
  `pass_opportunities_v2.json`, `pass_marginal_water.json`. No añadir trabajo
  indiscriminado ni repetir el viejo work_steal que rompía recorridos.

- **[2026-09-25, liquidez diferida] Una sustitución asequible ahora puede
  quitar alimento a otros animales.** Piloto10,ars40/1018001/asiento0:
  dos COW→SHEEP cuestan200más; compra WHEAT8en191 pasa7aceptadas→0,
  tres vacas quedan sin alimentar dos noches y escapan239. Margen+1.037→−22.858,
  mismas tiendas, recompensas/ledger reproducidos. No atribuir todo a precio
  de lana ni llamar irrelevante el coste adicional porque la compra se aceptó.
  Gate monetario por acción no garantiza financiación de inputs próximos.
  Ver `pilot10.physical_audit.json` y `pilot10.funding_failure.json`.

- **[2026-09-25, oferta comprometida] Mirar sólo animales/plantas colocados
  puede sobreestimar una inversión adicional.** En el desarrollo ovino había
  seis ovejas pagadas aún en transporte y8 lanas privadas. Incorporarlas cambia
  ingreso proyectado9.637→4.157 frente a coste8.615. El filtro anterior admitía
  una inversión que el modelo completo rechaza. En infill4_d18 también hay
  un proyecto V219 comprometido aún sin plantar; no cambiar su confirmación
  en curso, pero revisar ese supuesto antes de interpretar la cotización.
- **[2026-09-25, transporte] Una orden de regreso tardía no evita el depósito
  automático nocturno.** Hay que comprobar antes de HARVEST si alcanza viaje,
  cosecha y entrega. Rebaño v2 entrega36/53/83 lanas, confirmado por instrumentar
  `_apply_unit_action` real, incluido PLACEh23. Fuente de v3 sólo cambia filtro
  económico y conserva exactamente las acciones forzadas en ambos asientos.

- **[2026-09-25, confirm5] La relajación late18_6k perjudica a VQ:** −21,591pp,
  IC95 dos vías[−36,90;−6,28],1.152 episodios, noop384/384,16 semillas nuevas.
  Piloto+3,125 dependía de una semilla; confirmación cambia156/352 partidas,
  cero celdas mejores y38 peores. Caso negativo ejecuta80 tomates sin errores,
  pero margen+190→−1.416. Refuta este criterio de inversión, no todo tomate.
- **[2026-09-25, infill] Agregar peones puede desactivar módulos del padre:**
  R51 acepta contratación sólo si todos los peones presentes pertenecen a módulos
  conocidos. Contratar después de hora3 conserva su fertilizador en el caso
  auditado. Correcta ejecución del módulo nuevo no asegura preservar al padre.
  Asimismo cosechar+regar juntos dejó4 tomates sin entregar y hubo overflow;
  alternar días de madurez entregó32/32. Evidencia dirigida, no mejora W/L.

- **[2026-09-25, loop3] El modelo HD2 con tiendas futuras a peso1 causa daño:**
  −84,375 pp, IC dos vías [−114,33;−54,42], noop96/96, 504 episodios.
  Diagnóstico reproducido: cambia dos gansos por vacas, EV estimado674→6371;
  leche261→301 unidades pero ingreso28.950→26.820, huevos93→0 y margen
  +1.808→−2.020. Tiendas iguales y cero errores. Refuta esta extrapolación
  e implementación, no toda planificación con demanda futura.

- **[2026-09-25 UTC] PREDICT aporta fuerza en el panel de públicos:** ablarlo
  sobre VQ pierde **68,75 puntos** (IC dos vías [−89,57; −47,93]); exigir
  confianza adicional pierde **51,56** ([−78,92; −24,20]). 608 episodios, ocho
  rivales y ocho semillas, noop exacto 160 veces. No podar una capa rentable
  sólo porque una métrica de precisión parcial parezca baja.
- **[2026-09-25 UTC] Corrección de nuestra sonda:** «12/67 aciertos» omitía ventas
  simultáneas y usaba flujo neto inferido. Reproducción exacta de 720 estados de
  cada uno de cuatro replays + ledger: **50/67** con venta aceptada rival en
  t..t+4, **42/67 en t**. Esto no prueba causalidad de cada adelanto, pero invalida
  la motivación observacional inicial de baja coincidencia. En una celda controlada,
  mismas cantidades totales vendidas y peor timing convierten +89 monedas en −78.

- **[2026-09-25 UTC] El orden local arshs3 > v13 transfiere en esta lectura real:**
  2292,5 @148 episodios frente a 1857,9 @136. No convierte 20-0 local en un
  delta Elo calibrado ni garantiza 2900. VQ ya enviada (56535264); el original
  continúa activo. Fuente: snapshots API en `docs/evidencia/research_20260925/`.
- **[2026-09-25 UTC] La cola histórica no es el estado actual.** «Todas las vías
  cerradas», «subir públicos pendiente» y los viejos procesos en curso quedaron
  superados por nuevas autorizaciones y datos. No repetir experimentos por notas
  antiguas, ni convertir un descarte de implementación en imposibilidad general.

- **[2026-09-24] Entre agentes públicos top las partidas se deciden por cientos de dólares, no por decenas**: derrotas de arshs3 mediana $521; una capa que suma +$20/partida (VQ) no voltea ninguna contra el pool, pero decide los espejos (prioridad de slot en lockstep): 17-3, 40-0, 95%.
- **[2026-09-24] Una capa puede ser un intercambio entre linajes rivales, no una mejora**: ADV sobre arshs3 +25..+30 contra el linaje tds y −20..−30 contra herd-safe/order-book; neto ≈ 0 en confirmación. Evaluar siempre contra un pool con varios linajes, nunca contra el rival que motivó la capa.

- **[2026-09-24] Nuestro nivel absoluto era el problema, no el relativo.** Torneo en bucle cerrado (720 partidas, motor oficial): nuestras dos activas (seek/decem + guardias, "confirmadas" a +22..+28 vs nuestras referencias) pierden 0-20 contra CADA uno de 7 agentes públicos Apache-2.0, por −$12..16k de media. El ladder coincide: públicos 2500-2950, nosotros ~1160. **Lección de método: medirse contra la mejor referencia EXTERNA disponible pronto y de forma continua; un harness que sólo compara variantes propias puede validar mejoras reales dentro de una familia débil.** Última comparación con notebooks públicos: 2026-09-02.
- **[2026-09-24] Dentro del ecosistema público, la familia Herd-Safe (Dmitrii Gluzdov / arsgorynich) domina en bucle cerrado a la familia cinta+reflejos de Thomas Tschinkel.** arshs3 98,8% (20-0 vs v13 y v94); v94, con 2944,7 documentado en ladder, 25%. Bucle cerrado intra-familia ≠ ladder: queda por ver qué transfiere.

- **[2026-09-23] Calibrar la guardia a la cinta vale +14 puntos vs fuertes** (107570947: reserve 6 -> 39.1%, reserve 8 -> 53.1% en cal1). Todas las comparaciones previas entre cintas con guardias se hicieron con la guardia a medias.
- **[2026-09-23] Un piloto de ~100 candidatas con 64 celdas por brazo NO ordena.** El 1o de cal1 (umg_111191811, 87.5%, parejo contra 4 fuentes) cae a 31.0% (-11.7) en una poblacion fresca; el 4o (110304538) queda 1o. La unica defensa es confirmar en rivales Y semillas que la seleccion no toco.

- **[2026-09-22] Nuestro chasis adaptativo es peor que la cinta fija de Majkel EN TODAS LAS FASES.** Hibrido (cinta 107570947 hasta d10/d15/d20 + CAMPEONA_HOZ, con guardias) vs 71 fuertes: cinta pura 43.0%, traspaso d20 17.4%, d15 10.6%, d10 10.5%, HOZ solo 9.9%. La ventaja de la cinta se acumula toda la partida. "El valor esta en la adaptacion" es cierto para la adaptacion de MAJKEL, no para la nuestra. **Ultima hipotesis de mejora sobre la cinta, cerrada. Consolidar.**

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

- **[2026-09-25, DSM actual] La siguiente frontera incluye inversión productiva:**
  cuatro replays recientes, 720 estados exactos cada uno, cuarta tierra día10
  y 116–231 tomates vendidos. No demuestra que tomate cause su rating.
  Nuestra base puede ocupar SE con seis ovejas al día12; el módulo tardío de
  tomates no actúa allí. Adelantarlo cambia la asignación de tierra, no sólo
  fechas. Diagnóstico temprano ejecuta diez plantas/60 unidades sin errores,
  pero pierde en ambos asientos del mundo de desarrollo. Loop5 con semillas
  nuevas debe medir el coste de oportunidad y W/L/T, no el ingreso bruto.

- **[2026-09-25, loop1] Diversificar patrones de rival es REAL_WORLD_CANDIDATE:** top3
  frente a top1 da +9,375 pp (IC dos vías [−7,86; +26,61]) en cuatro semillas,
  ocho rivales. La señal aparece en dos semillas y tres rivales. Reproducción
  causal de una celda: −1.062 → +292, 15→24 activaciones, shops iguales.
  Confirmación disjunta: +10,795 pp, IC95 semilla [1,23;20,36], dos vías
  [−0,12;21,71], once rivales/16 semillas. 20 celdas mejores y una peor;
  arshs3 −6,25 pp. Cumple el gate registrado de envío, sin garantía de ladder.
  Daño reproducido: +216→−425, tiendas iguales, sin errores. Fast2 +2,841 pp
  no supera gate; no redondearlo ni cambiar al subpanel favorable.
- **[2026-09-25] Recuperar siembra exige reservar el riego del mismo día:**
  persistir el intento entre peones no basta si sólo hay una visita diaria.
  Insertar PLANT y desplazar un sufijo hasta un turno final redundante sí
  recuperó una fresa perdida por maleza. El RNG posterior cambió: W/L de esa
  sonda contra replay no estima mejora frente a la política rival.

- **[2026-09-25 UTC] Fecha nueva de notebook no implica mejora:** tds25/hl25
  dieron −7,81/−9,38 pp vs VQ, con IC dos vías que cruzan cero. Ninguna pasó
  el umbral exploratorio; no se confirmaron ni enviaron. 608 episodios, ocho
  rivales, ocho semillas nuevas, controles exactos. El 10/16 directo de tds25
  no rescata un criterio global incumplido. No se refutan universalmente sus
  mecanismos por este resultado. Ver `RESULTADOS_2026-09-25.md`.

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

- **[2026-09-25 UTC, hipótesis inicial corregida] PREDICT sin filtro inmediato
  era una posible fuga.** Prueba ejecutada y rechazada: añadir el filtro causa
  regresión clara. La sonda original omitía competencia simultánea; ver corrección
  arriba y `forecast_signals_validated.json`. No repetir gate/off con los mismos
  parámetros ni presentar «12/67» como precisión válida.

- **[2026-09-23] La robustez de una cinta fuera de contexto es sobre todo propiedad de la FUENTE.** Media de las cintas de cada fuente vs 32 fuertes (cal2): DECEM 64.3% (11 de 13 > 55%), seek 46.1%, Boey 39.7%, Majkel-nuevo 31.6%, Vadim-nuevo 15.6%, M&M&P&Q 6.8% (n2 del ladder). El valor de un agente y el de su cinta son cosas distintas.
- **[2026-09-23] REFUTADA: "las ordenes saturantes (SELL X 50) hacen robusta una cinta".** DECEM 3% saturantes = M&M&P&Q 3%; Vadim-nuevo es la mas saturante (21%) y de las peores. Correlacion debil observada en su lugar: las fuentes robustas emiten mas PASS (DECEM 7.0%, seek 8.0% vs 1-3% el resto) y menos animales (17-19). M&M&P&Q emite 932 ordenes BUY_ANIMAL/partida: insistencia reactiva que la cinta repite a ciegas.

- Mas cintas (30 victorias, tree_v2) > 4 cintas (tree_v1). Se mide ahora.
- ~~Las cintas de DSM/UMG/Vadim pueden ser mejores materia prima que las de Majkel.~~ **Bajada:** DSM pierde 3-6 contra Majkel en directo; misma liga. Y mezclar politicas rompe la coherencia de prefijos del arbol. Se descarta salvo hueco de cobertura.
- Matching por mas contexto que la tienda (acciones tempranas del rival, malas hierbas) podria reducir mas el desajuste.

## DISPROVEN

- Gansos/huevos (-49.4). Aguantar producto para vender mejor (gradiente monotona hasta -10). Fertilizar cultivos de un corte (-29.4). Mas superficie / cuarto cuadrante (-8/-14). Rebano 6..16 (todo negativo, optimo 8). Plantilla 9..15 (optimo 12). Copiar composicion del lider por piezas (7 de 7). `hire_by_work` (-17.8). Quitar forraje temprano (-45.6). Cadencia de riego con o sin poda de ruta (-21.8). Reordenar prioridades (mejor +2.5 = ruido). Compra parcial (+0.23 al replicar). harvest_76 (-0.08). compete_aware (-12.8). Asimetria de asiento (0). Optimizar la apertura DENTRO de nuestro planner (techo ~0.6% del dinero final).
- "Nuestro mejor intento es un replay" NO es una anomalia: el meta de esta escalera (C90-C95) ya eran cintas.
