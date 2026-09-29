# Estado de investigación — leer primero para continuar

## Corte 2026-09-29 18:45 UTC — datos reales: final_29 > final_xc1; regla del par final fijada

- **Activas:** 56655371 final_29 (2215, 105-36 en 141 públicas) + 56628181 final_xc1 (2211,
  100-100 en 200). Envíos restantes hoy: 4. Hoy no se envía nada.
- **Comparación real** (workflow `par-final-datos-reales`, 8 agentes, 3 escépticos): desde las
  12:00 UTC f29 23-15 y xc1 8-26, +37 pp [+14; +55]; modelo logístico con el rating actual de
  cada rival: f29 − xc1 ≈ +92 a +135 puntos. xc1 lleva desde el 28 ~08:00 ganando el 34 %: su
  rating va con retraso. Censo 0929a: f29 64-8 contra la familia tds27 (xc1 31-10).
- **Regla del 30** (CALENDARIO_ENVIOS.md, fijada 18:40 UTC antes de ver datos nuevos): con
  `revisar_par_final.py`, entre 12:00 y 13:00 UTC se propone reenviar la copia exacta de
  final_29 en lugar de final_xc1 si (a1: rating +40, o a2: partidas nuevas xc1 ≤ 40 % y f29
  ≥ 45 %) y (b) y (c). Siempre con aprobación del usuario en ese momento; si falla, par =
  final_29 + final_xc1. Reglas de reintento si la validación falla (no desplazar a f29).
- **Mecanismos en real (132 partidas f29):** sin ERROR/TIMEOUT propios (los 8 ERRORED de
  04:14-06:34 UTC son una caída de la plataforma que afecta a otros equipos); SA 6-0 en
  proyectos de 6 ovejas y YARN 65-17; BP sin fallos; MS/MSS +154 $/partida estático.
- **Problemas nuevos:**
  1. Copiadores de MS (8 rivales en el último tercio: compran X extra en el índice 0 y
     revenden en 2-6, antes de nuestro 9): −383 a −5.914 $/partida; perdimos las 8, MS decide
     2. Guardia f29g construida (workflow `guarda-copiadores-ms`, 6 agentes, 2 revisores
     aptos): bytes de final_29 + capa que simula el mercado contra un rival benigno y apaga
     MS/MSS al detectar compra-reventa delante de nosotros. Resimulación fuera de muestra
     (191 cintas de xc1): 12 disparos, 1 falso positivo (−73), +142 $/partida, 1 L→W, 0 W→L.
     Confirmación local en curso (PREREG_GUARDA_2026-09-29.md). Los copiadores usan código
     privado: ningún notebook público nuevo lo contiene (revisados 13 kernels del 28-29).
  2. Linaje privado A1 con apertura de vaca (6 % del pool, sube desde 1,3 %): f29 y xc1 van
     1-7; segunda tierra en el paso 195-202 (nosotros 266), 10-27 casillas de trigo en el 240,
     más gansos/tomate; 79 % del margen perdido por f29. Es de producción: sin arreglo rápido.
  3. Copias parciales de cha22 3-8 contra f29 (xc1 4-1).
  4. Hueco de MS no descuenta otras compras de la misma lista (t=575): salió a favor; la
     versión estricta ya se descartó (criba n, −$24 a −$88).
  5. Desborde nativo al final del día (t=575, t=623): ~$296/partida en f29, $400 en xc1.

## Corte 2026-09-29 00:05 UTC — final_29 enviada y validada

- **Activas:** **56655371 final_29** (enviada 00:00:49, COMPLETE, empieza en 600) +
  **56628181 final_xc1** (≈2320; 73W-50L en 123 partidas reales). final_frps desplazada.
- Envíos restantes hoy: 4. Regla del usuario (CALENDARIO_ENVIOS.md): al cierre, las dos activas
  deben ser nuestros dos mejores bots; nada de experimentos en los envíos finales.
- Siguiente: bajar partidas reales de final_29 cuando pase de ~40-60 (carpetas nuevas por
  tanda), compararla con final_xc1 en la misma franja y decidir el segundo hueco el 30 antes
  de las ~18:00 UTC.


## Corte 2026-09-28 09:00 UTC — candidata del 29: final_29 (sha cf129189)

- **Envío previsto 29-sep 00:00 UTC:** `submission/main_publico_final_29.py` = final_xc1 + SA +
  BP + MS (X≤90, también con 9 órdenes) + MSS (X≤90). Desplaza a final_frps; par activo:
  final_xc1 (≈2380; 58W-20L en 78 partidas reales) + final_29.
- Evidencia acumulada sobre final_xc1: SA (13/13 celdas a favor), BP (PROMETEDORA), MS
  (ADOPTADA, +3,44 pp [+0,95; +5,92]), extensiones MS (PROMETEDORAS, +$22-52). Pruebas amplias
  contra 26 públicos: sin ningún rival que empeore; margen +$300-775.
- Nuevo público 08:46: Harvest Ledger quita el LOOK 7 de espejo y añade CA −22 solo con
  PET_CAFE (`results/exp_0928b/rival_hlc.py`); no es una amenaza nueva (fork tds27).
- Pendiente 29-sep: vigilar las partidas reales de final_29 (≈15/hora); si rinde como el
  harness, decidir si el segundo hueco pasa de final_xc1 a otra variante fuerte.


## Corte 2026-09-28 08:13 UTC — MS adoptada; candidata del 29: final_xc1_sa_bp_ms90

- **Envío previsto 29-sep 00:00 UTC:** `submission/main_publico_final_xc1_sa_bp_ms90.py`
  (sha a0ffcd24) = final_xc1 + SA + BP + MS(X≤90). Desplaza a final_frps; par activo:
  final_xc1 (≈2380) + final_xc1_sa_bp_ms90.
- **MS** (PREREG_MS): comprar X≤90 de más en nuestra compra de trigo/fertilizante (índice
  temprano gracias a BP) y revender X en el índice 9. Ida y vuelta = $0 exacto contra un
  mercado sin cambios (la compra se cotiza al inventario−1); si el rival compra en medio,
  ganamos nosotros y él paga más. Confirmación **+3,44 pp [+0,95; +5,92]**, 13/13 celdas a
  favor, margen +$388-572 contra todos, 0/672 celdas negativas. Prueba amplia 26 agentes:
  90,1% → 94,7%.
- Cadena de capas al final del módulo: FR → MS → BP → XP(cxd) → step1009 (+ SA en su línea).


## Corte 2026-09-28 07:15 UTC — candidata del 29: final_xc1_sa_bp

- **Plan 29-sep 00:00 UTC:** enviar `submission/main_publico_final_xc1_sa_bp.py` (sha 054c58fd)
  = final_xc1 + SA (peón de ovejas entrega antes de recoger fertilizante) + BP (compras tras
  las ventas, antes de las órdenes fijas). Desplaza a final_frps; par activo: final_xc1
  (2385 a las 07:03, probada en el ladder) + final_xc1_sa_bp.
- Evidencia: SA 13/13 celdas cambiadas a favor y 0/1.120 márgenes negativos (PREREG_SA);
  BP PROMETEDORA, 5/5 a favor, margen +$13-19 con IC>0 contra todos (PREREG_BP); prueba
  amplia contra 26 agentes públicos: 86,8% → 92,1%, ningún rival empeora.
- Ladder: final_xc1 2385; final_frps 1418 (47W-6L; emparejamientos bajos).
- Decisión del par final (30-sep): por defecto final_xc1_sa_bp + final_xc1 (cobertura);
  alternativa: dos copias de la mejor si su resultado real lo respalda.


## Corte 2026-09-28 07:30 UTC — SA lista para el 29; BP en confirmación

- **Ladder:** final_xc1 (56628181) **2360** a las 06:26 (supera ya a tds27top3); final_frps
  1413 (47W-6L en 53 partidas; sube lento por emparejamientos bajos).
- **SA** (peón de ovejas entrega la lana antes de recoger fertilizante): confirmación +2,19
  pp (6/6 celdas a favor), prueba dirigida YARN +2,54 (7/7 a favor); 0 de 1.120 celdas
  pierden margen; inerte fuera de YARN. No cumple el umbral pre-registrado; se envía como
  instrumento a las 00:00 UTC del 29 (`submission/main_publico_final_xc1_sa.py`).
- **BP** (compras de producto tras las ventas y antes de HIRE/BUY_SEED/BUY_ANIMAL/BUY_LAND):
  criba +$18-28 de margen, 80/80 celdas ≥ 0. Confirmación `torneo_bp1` en curso (PREREG_BP).
- Descartados hoy: FG (no vender a precio de suelo: −$1.000 a −$3.400), WF, courier,
  presupuesto de reordenación, compras tardías, BF.
- Tras XC+SA, las derrotas contra la familia tds27 sin YARN son de $6-66 (monedas al aire):
  cualquier ventaja sistemática de ~$30 las voltea.


## Corte 2026-09-28 05:30 UTC — SA (lana antes que fertilizante) en piloto; WF rechazada

- **Activas:** 56628181 final_xc1 (1748 @ ~1 h) + 56626892 final_frps (1280). Cuota del
  28-sep agotada; próximo envío a las 00:00 UTC del 29.
- **WF rechazada** en confirmación (−2,8 pp, 9/10 celdas en contra) pese a margen medio +107:
  vender cantidades extra cuesta en partidas cerradas. El margen medio no sustituye al W/L
  cuando se cambian cantidades.
- **Hallazgo SA:** tds27 añadió COLLECT_FERTILIZER a la lista de tareas del peón de ovejas
  (capa V233, línea `elif tile['fertilizer_available']...`); cha22 y mroute no lo tienen y
  entregan la lana 3 pasos antes (carrera de la lana en pares YARN, −$1.800 a −$6.300).
  Criba g (10 semillas YARN): con lana en las manos entregar primero = +$1.800-2.450 de
  margen, 30 → 80% contra cha22/mroute, sin ninguna celda negativa. Pilotos `torneo_sa1`
  (xc1_sa, xc1_sb vs final_xc1) y `torneo_sc1` (xc1_sa2, xc1_sc vs xc1_sa) en curso
  (PREREG_SA). Panel con fcast2 y pesos `pesos_censo_0928c.json`.


## Corte 2026-09-28 04:30 UTC — XC replicada; WF (vender primero) en piloto

- **Réplica XC con pesos del censo** (`torneo_xcr`, 768 partidas): final_xc1 − final_frps
  **+7,30 pp [+1,38; +13,23]**, 17/17 celdas a favor (tds27 71,9→85,9%, hl836 65,6→84,4%,
  hl0928 68,8→81,2%). final_xc1 es la primera candidata del par final.
- **Censo 0928b** (`pesos_censo_0928b.json`): a ~2300 la familia tds27 es el 50% (muchas
  copias EXACTAS de tds27/hl836), linaje top3/arshs3 22,5%, cha22 20%. El panel del harness
  representa bien a la mitad de la población.
- **WF** (`apilar_lana_primero.py`): vender ya el stock libre de lana/leche/fresa mientras
  precio ≥ fracción·base. Criba d: wfa75 +$180 vs tds27/hl0928, W/L 71→100% en 7 semillas.
  Piloto `torneo_wf1` (PREREG_WF) en curso. Las pérdidas grandes contra cha22 en pares YARN
  son de logística (su lana llega antes al cobertizo), no de la decisión de venta.
- Descartado hoy: BF (compras primero), S738 con trigo/fertilizante, mirror-LOOK 8/10,
  quitar compras tardías (fertilizante/contrataciones sí se recuperan).


## Corte 2026-09-28 04:00 UTC — final_xc1 enviada; ladder = campeonato de espejos

**Activas:** **56628181 final_xc1** (03:55, PENDING al enviar) + **56626892 final_frps**.
Cuota del 28-sep agotada (5/5); el 29 y el 30 hay 5 cada día.
- final_xc1 = final_frps + un pase `_cxd_reorder` antes de FR (`apilar_pases.py ... 1 --cxd`).
  PROMETEDORA: margen vs tds27 +80 [+51; +110], W/L +0,31 pp (PREREG_XC).
- Hallazgo: 29/40 partidas reales de tds27top3 se decidieron por < $1.000 (espejos de la
  familia tds27; 9/40 por < $80). Las palancas son la carrera de ventas: vender antes
  (LOOK) y en índice menor (XC). Comprar primero pierde (empuja las ventas atrás).
- Criba_b sin candidatas: S738 con trigo/fertilizante pierde; ml8/ml10 casi inertes; BF pierde.
- Nuevos públicos (0928b): Harvest Ledger 02:23 = tds27 + LOOK 7 si detecta espejo
  (`results/exp_0928b/rival_hl0928.py`, añadido a los paneles); Master Engine V5 (me5)
  de otro linaje; God's mode (manipular la RNG de tiendas, impacto desconocido).
- Censo de partidas reales recientes en cola (`results/cola_0928d.sh` → censo_0928b).


## Corte 2026-09-28 03:15 UTC — candidata final en el ladder

**Activas:** **56626892 final_frps** (02:52) + **56626140 combo_fr** (02:14). Queda 1 envío hoy.
final_frps = tds27top3 + combo (`_S738_LOOK=6`, `_SR_MARGIN=12`) + `_CA_MARGIN=-22` + FR con
pre-venta. Cada pieza confirmada por separado (ver PREREG_BARRIDO_PARAMS, PREREG_COLINA,
PREREG_FRONTRUN); la combinación no muestra interacción negativa (+2,2 pp vs combo_fr).
La app se cerró a mitad de colina2: `torneo.py --reanudar` completó el bloque con los mismos
agentes y semillas; las colas largas se lanzan ahora con `nohup` (`results/cola_*.sh`).


## Corte 2026-09-28 02:35 UTC — dos mejoras confirmadas y enviadas

**Activas:** **56626140 combo_fr** (02:14) + **56625348 combo** (01:36). Quedan 2 envíos hoy.

1. **Combo** (`_S738_LOOK` 4→6 + `_SR_MARGIN` 8→12, sustitución en su línea): +8,4 pp
   [+4,3; +12,5]; **contra la familia tds27 +19,4 pp**. La familia tds27 pasó del 2% al
   ~50% de nuestros rivales reales en un día (censo de 40 partidas del 28-sep).
2. **FR — adelantarse a las compras de trigo de la cinta** (`apilar_frontrun.py`): hallado en
   replays reales. Rivales privados (Jun_value, David Goldrajch) copian la producción de la
   cinta y compran en t−1 el trigo que la cinta compra en t (rutas 103/104/112/124, jugador
   original = comerciante de trigo), vendiéndolo en t en el índice 9: +$8-11k contra nosotros.
   FR pre-compra un paso antes (defensa) y, si el rival es seguidor de cinta, especula.
   **+37,2 pp [+26,3; +48,2] en esas partidas, 51/51 celdas a favor** (~11% de partidas).
   Mecánica del motor: órdenes por índice; en cada índice lockstep por unidad entre los dos
   jugadores; `SELL X 0` ocupa hueco sin efecto; las compras se cotizan a inventario−1.
3. **Rechazados hoy:** router por pares y rutas EXP240 en YARN, zanahoria (dosis), capas
   trasplantadas (inertes), oráculo de ventas con la cinta en PREDICT (inerte), trigo-primero.

**En curso:** colina2 (hp6, cam22, sr10 sobre combo; 48 semillas) → pre-venta FR (`--preventa`,
sonda +$0,7-2,4k más por partida en rutas de trigo).


## Corte 2026-09-28 00:55 UTC — ofensiva de 3 días (usuario: "darle y darle")

**Activas:** tds27top3 **56596228** (2301 @150) + **56624199** tds27top3_cam22 (00:44 UTC,
instrumento en slot 2; sustituye a top3cc, que convergió en ~2090).

**Hecho esta noche (todo pre-registrado):**
- Frontera pública sin cambios: las versiones nuevas son la familia tds27 (arreglo de
  órdenes vacías; `_CA_MARGIN=-22`; step1010 = 41 pasadas → punto fijo, juega idéntico).
- Router (`forzar_ruta.py`, `analizar_rutas.py`): ruta 0 global −26 pp; 4 pares
  seleccionados (~6% de partidas, efecto dependiente del rival) → confirmación aplazada;
  EXP240 en pares YARN −38,8 pp → REJECTED. Las tablas de tds27 están bien afinadas.
- Desempates en espejo tds27 (16% de empates exactos): SF/KO, VQ y ADV inertes en tds27;
  cobertizos vacíos al final; los animales no se venden (el motor solo vende 9 productos).
- Huellas del rival en el paso 2: todas las familias públicas dan (1042|1038, 9989).
- **Barrido de parámetros** (eliminación sucesiva): 24 variantes al final del módulo
  (18 inertes) + criba de inercia en su línea (1b: 3 activas de 18; 2: 9 activas de 40).
  Etapa 2: cam22 +5,0 [−2,3; +12,3] (positivo en todos los linajes), hp6 +1,7, ff12 +0,4,
  hp3 −2,1. **Mecanismo cam22:** más conversión trigo→zanahoria (lo que hacen los privados).
- **En curso:** etapa 1b (12 activas) → dosis-respuesta `_CA_MARGIN` −22/−30/−40
  (`PREREG_ZANAHORIA_2026-09-28.md`), encadenadas.


## Corte 2026-09-27 16:30 UTC — pareja estable; la familia tds27 ocupa lo público

**Ladder 16:04 UTC:** tds27top3 **2293,2** @109 (equipo #~648 a las 09:40 con 2280);
top3cc 2074,9 @144. Censo de 60 partidas de tds27top3: 47-13; linaje cha22 28-7;
tds27 exacto 1-0 (+$19); privados 0-3 (−$8,2k de media; ganan la segunda mitad).

**Frontera pública del día:** todas las versiones nuevas son la familia tds27 en la
práctica: tetsutani 02:50 (= tds27), guru v4 y kunaldesale ttv1 (= tds27 + arreglo de
órdenes vacías), Harvest Ledger 14:23 y haideptry-2965 (+ `_CA_MARGIN=-22`),
lynnsakurai step1010 (41 pasadas → punto fijo; juega idéntico a tds27).
tds27top3: 10-8-2 vs Harvest 14:23, 10-8-2 vs tds27, 18-2 vs haideptry-shepherds.
lucky-boy-2552 (leoprovorov) = arshs3 + parche de router (ruta 0 en 10 pares de
tiendas): base débil frente a tds27, no evaluado.

**Rechazados hoy:** tds27sfko (inerte), tds27cc (−4,8), barrido TOP2/TOP5/K3/EVERY1
(ninguno pasa; TOP5 gana el espejo a TOP3 pero −5,8 en pool).

**Decisión:** no gastar envíos en cambios marginales; seguir la frontera pública
(procedimiento abajo) y reevaluar si aparece una versión que gane a tds27top3.
Herramienta nueva: `extraer_publico.py` (todos los empaquetados vistos).


## Corte 2026-09-27 04:15 UTC — tds27 aparece; pareja tds27top3 + top3cc

**Ladder 02:26 UTC:** top3cc 2059 @84 (60 recientes 46-14), cha22sfko 2178 @88 (34-26).
Censo de sus 120 partidas: rompe-espejos **23-2 contra cha22 exacto** (confirmado en
real); top3cc 10-2 contra el linaje cha22, 8-1 Harvest, 24-9 otras variantes;
cha22sfko 7-12 contra otras variantes y 1-4 contra Harvest.

**tds27** (tetsutani 27-sep 00:38, "step1009...fixedsell_closure"): cha22 + PREDICT
+ más cambios. Gana **30-2 a top3cc y 24-8 a cha22sfko** (84% global). Determinista
con la semilla de hash. tds27sfko inerte (su cierre ya evita esas compras).
**tds27top3** (TOP=3) adoptada por pre-registro: 18-4-10 vs tds27 [52,5; 91,3], pool
+3,1 pp. **Enviada 56596228**, desplazando a cha22sfko. Activas: tds27top3 + top3cc.

**Censo franja 2350-2450 (26-27 sep, 56 partidas):** linaje cha22 ~44%, privados 19%,
Harvest ~15%, tds27 3% (asomando), **arshs3 0%** (52% el día 25).

**tds27cc REJECTED** (−4,8 pp): la contra-biblioteca no ayuda a una base que ya
integra PREDICT. tds27top3 gana 42-6 a cha22 y a top3cc. top3cc se mantiene como
segundo slot (otro linaje; cobertura si tds27top3 falla en el hardware de Kaggle).

### Procedimiento que está funcionando (repetir cuando la frontera pública se mueva)

1. **Rastrear** notebooks nuevos (`kaggle kernels list --competition kaggriculture
   --sort-by dateRun`); extraer sin ejecutar (`extraer2.py`, variantes con
   tar/lzma/b85 por AST) y auditar (`auditar.py`); comprobar la entrada con
   `get_last_callable`.
2. **Torneo** contra nuestras activas y los linajes del censo (`torneo.py`, comprobar
   con `test -e` que la salida no exista).
3. Si un público nuevo nos gana: tomarlo como base y probar **rompe-espejos**
   (determinista con la semilla de hash; `_V92_P_TOP=3` si trae PREDICT;
   `apilar_fin_partida.py` si no tiene cierre propio). Pre-registrar: directo con IC
   por semilla > 50% y pool sin daño (límite dos vías > −5 pp).
4. **Censo** de las partidas reales (`bajar_lider.py` + `censo_linajes.py` +
   `resumir_censo.py`) para ponderar por la población real (`pareado_ponderado.py`).
5. Recordar el orden de activas: el envío nuevo desplaza a la activa MÁS ANTIGUA.


## Corte 2026-09-26 21:15 UTC — censo de linajes y contra-biblioteca

**Censo (`censo_linajes.py`, 80 partidas reales de top3/VQ, franja ~2200):** 42% de
los rivales son cha22 exacto o casi (+10% parcial), 9% Harvest Ledger, 8% arshs3.
top3 perdía 3-10 contra cha22 y sus casi-copias. Las "casi-copias" difieren sobre
todo en el ORDEN de ventas: deriva de `sorted(set())` según la semilla de hash del
proceso (en Kaggle cada agente tiene la suya) → espejos con ruido.
**Franja 2350-2750 (dataset público, 25-sep madrugada, 45 partidas):** 52% arshs3
exacto, 14% cha22 exacto, 4% ars40; el resto disperso.

**Adoptado y enviado:**
- `cha22sfko` (56587842): cha22 + recortes de fin de partida → 29-1-2 vs cha22.
- `top3cc` (56588419): top3 + 330 episodios de cha22 en la biblioteca PREDICT →
  ponderado por población +28,3 pp [+15,4; +41,2]; vs cha22 44-4 (bloque 2) y
  30-18 (otro conjunto de semillas); vs arshs3 83%; gana 37-11 a cha22sfko.
**Rechazados (regla pre-registrada):** top3cc2 (biblioteca con 7 linajes más,
+0,7 [−6,4; +7,8]); cha22cc (cha22sfko + PREDICT, −3,5 [−11,5; +4,5]).
**En curso:** top3cc3 (doble cobertura de cha22), `PREREG_TOP3CC3_2026-09-26.md`.

**Herramientas nuevas:** `censo_linajes.py` + `resumir_censo.py` (linaje de cada
rival por reproducción exacta de acciones), `construir_biblioteca_cc.py`,
`construir_cha22cc.py`, `apilar_fin_partida.py`, `pareado_ponderado.py` (delta
pareado ponderado por la composición real), `torneo.py --fresco`.
**Lección:** con `> fichero` el shell trunca antes de que el script compruebe nada:
verificar `test -e` antes de lanzar con un nombre de salida.

## Corte 2026-09-26 20:15 UTC — cha22 sustituye a VQ; rompe-espejos en prueba

**Contexto.** Desde el 25 a las 11:00 UTC no hubo actividad (sin procesos vivos;
los runners 21–33 del loop anterior quedaron detenidos, no relanzar a ciegas).
Leaderboard 19:37 UTC: #1 Boey 3069,9 · #10 2896 · #100 2637 · #500 2373 ·
**nosotros #965, 2182,7** (top3). Deadline 30-sep 23:59 UTC; el ladder sigue hasta ~15-oct.

**Ladder (40 partidas recientes por activa):** top3 20V-20D (equilibrio ~2185);
VQ 17V-23D (2153). arshs3 se retiró en 2275,7 y v13 en 1853 → el torneo en bucle
cerrado SÍ predijo el orden en el ladder.

**Frontera pública (torneo_0926a, 9 agentes, 720 partidas, 0 errores):** cha22
(tetsutani 26-sep = Abhinav0370 #689 en 2287; también flexonafft, haideptry,
lynnsakurai-wheat) 82,5% · top3 78,8% · VQ 51,2% · guru4 (41 rutas) 51,2% ·
Harvest Ledger V74 31% · idle-seller 30% · god's mode 23% · Fieldcraft 19%.
cha22–top3 10-10; **top3–VQ 20-0; cha22–VQ 16-4**.

**Envío:** 56587658 = cha22 byte-exacto (19:51 UTC), desplaza a VQ. Activas:
**top3 56537205 + cha22 56587658** (dos linajes distintos en el techo público).

**En curso:** `PREREG_CHA22_FIN_2026-09-26.md` — cha22 + recortes de fin de partida
de tds (semillas inútiles desde el día 27, fertilizante desde el paso 696) como
rompe-espejos (copias de cha22 empatan entre sí). Bloque `torneo_cha22fin`.

**Lectura honesta del objetivo "top 1":** los 10 primeros (2896-3070) son agentes
privados adaptativos; los públicos más fuertes rinden ~2200-2300 hoy. Con 4 días,
lo alcanzable es exprimir el techo público (+50..+150) y vigilar publicaciones nuevas.


## Corte operativo 11:01 UTC — confirm21 activa, prioridad31 validada y en cola

Piloto21 cerró 2.016 partidas/noop352 a10:49:39UTC. Sólo `extra_half` pasa a
confirmación: +0,5208pp vs top3, ICdos vías [−8,3859;9,4275], +23,4375vsVQ.
Rank2 −5,2083 inconclusa; quorum −21,875 y short12 −10,4167 rechazadas en este
panel. Todas activas en16semillas. **Confirm21 corre 1.856 partidas**, no mirar
resultados parciales ni reiniciar;22–31 esperan en secuencia. Un torneo principal.

Loop31 validado:48partidas/noop8.628, máximo364ms,162compras/cierres y8.100unidades
exactas. Preserva cola nativa al cerrar town50. Ambas capas activas4/6; caso dirigido
recupera369de margen y dos derrotas pasan a victorias, sin cambio de producción.
Son desarrollos; piloto1.568 con semillas nuevas pendiente tras30. Analizador de
tres referencias validado con fixture1.920/noop448. Fuentes congeladas y runner31
vivo. Total103variantes competitivas más2prototipos17detenidos. Leer PRIORIDAD_CIERRE.

Otra auditoría explica cinco escapes preexistentes en1080001: venta de trigo
antes de recogidas5/2/2, almacén vacío y FEED fallidos. Un control exacto y dos
perturbaciones válidas: conservar trigo evita1escape; conservar y comprar9 evita5,
con cambios de cosechas y margen+120, aún victoria. Un brazo sólo compra fue
inválido por once órdenes; archivado, no usar su resultado. **Preregistro32 escrito;
candidatas NO construidas ni runner32**. Siguiente trabajo: implementar protección
de déficit para recogidas nativas y validar36partidas antes de encolar tras31.

API10:48:09UTC: VQ2291,5/101, top32138,5/91, COMPLETE. Seis nuevos controles
1050 reproducen719acciones/720estados/caja; seis alternativas con rival fijo,
ningún cambioW/L/T. Hallazgo separado: replay113252591 conserva una vaca comprada
sin colocar; DIG33quita maleza pero no reconstruye pasto, PLACE69falla. Auditoría
ofline exacta, reparación todavía no diseñada ni probada. Leer FEEDBACK_1050 y
TRIGO_RUTA_TARDIA. No nuevo envío; cuota antigua no es vigente.

## Corte operativo 10:36 UTC — confirm20 cerrada, 21 activo, nueva prioridad31

Confirm20 terminó10:25:05UTC:3.200episodios/noop832. Town20+0,2841pp,
town50+1,1364pp; ambos ICdos vías cruzan0 y gatefalse. Ambas cambian704/704
acciones propias, no inertes. No envío; contra los cuatro rivales del piloto,
delta0. Seis celdas W/L/Tdistintas auditadas con tres brazos:18partidas exactas,
167compras/cierres y6.280unidades. Leer CIERRE_REVENTAS20.

Daño v13/1050019: cierre de trigo delante de leche661pierde198propias y gana
171al rival. Dos fases idénticas salvo prioridad verifican recuperación369
con leche primero, mismos inventarios. Preregistro31fija dos variantes sobre
los town50 de VQ/top3, con controles originales adicionales. TODAVÍA no se
han construido ni hay runner31; siguiente trabajo: implementar/validar48juegos
sin tocar20–30. V1del capturador falló por wrapper, v2reproducecontrol exacto.

21corre;22–30esperan, no duplicar procesos.30validado48/noop11.504/max314ms,
32aperturas exactas. BUY12/SELL7mantiene stock5 y sólo cambia acción0en8/8
celdas por política. Pierde2de margen contraVQ (cuatro empates→derrotas en brazo
VQ), gana4contraV7sin cambiar derrotas. Mantiene producción en desarrollo,
no garantía global. Piloto960tras29.101variantes más2prototipos17detenidos.

Último ladder consultado10:02UTC:VQ2295,1/98y top32135,7/88; no nuevo envío.
Lectura pública1018archivada con fuentes primarias; no prueba estrategia nueva.

## Nota 10:15 UTC — cota rival auditada; sin nueva variante

`COTA_STOCK_RIVAL_2026-09-25.md` cierra una auditoría offline:12.942checks de
stock y12.942de ventas futuras cumplen cota pública conservadora.31señales
crudas imposibles;25sonEGGdeshabilitado, otras6MILKsin producto propio disponible.
No cambian una orden observada: no construir ni encolar30con esta evidencia.
V1falló clave vacía del auditor, archivada;v2válida. No se agregaron juegos.
Confirm20avanza (2.408/3.200a10:15UTC);21–29siguen vivos en cola. Total99
variantes más2prototipos, sin nuevo envío. No duplicar/reiniciar procesos.

## Corte operativo 10:08 UTC — 29 validado y feedback real actualizado

Confirm20 continúa (3.200episodios previstos);21–29esperan en secuencia.
No duplicar ni reiniciar runners.29:48desarrollos/noop8.628/max331ms, los
cuatro brazos activos6/6,368compras/cierres y13.720unidades exactas. Conservan
trabajo/cosechas/pérdidas/tiendas en esta cuadrícula, cero escapes; sin cambios
W/L/T. Dos fuentesVQ nuevas y dos top3reutilizadas;99variantes más2prototipos.
Ver REVENTA_DOS_PADRES y preregistro29. Piloto1.568después de28, sin autoenvío.

API10:02:07UTC:VQ2295,1/98episodios listados;top32135,7/88, COMPLETE. Siete
replays nuevos reproducidos719acciones/720estados/caja, max214ms, cero errores
observados/escapes/productos terminales propios. Alternativas contra rival
fijo: top3mejora cinco márgenes, empeora dos; Farmerjay851→−340. Esto no mide
respuesta reactiva ni fuerza poblacional. Leer FEEDBACK_1003; ninguna nueva
submission. Las verificaciones de28/29y los diagnósticos están cerrados.

## Corte operativo 10:01 UTC — confirm20 activa, 28 validado, 29 en desarrollo

Pilot20 cerró1.920episodios/noop448: los tres tamaños+3,125pp, intervalos
cruzan0, cuatro celdas mejores en tres semillas. Town20/50 seleccionadas por
regla previa; confirm20 corre3.200juegos. No consultar deltas parciales ni
reiniciar.21–28esperan en secuencia;28ya verificó sus fuentes congeladas.

Auditoría20:12partidas exactas,150compras/cierres y7.722unidades conciliadas.
Town20/50 conservan alimento/cosechas en los tres casos; town80pierde dos
huevos en1049013. Los efectos sobre ventas nativas/rival impiden identificar
todo el margen como beneficio aislado. Leer REVENTA_TOWN.

Loop28: cuatro máscaras de evidencia negativa sobreVQ/top3;48desarrollos,
noop8.628, max407ms,86.160checks y40.306pares floorobservables físicamente
verificados. Todas activas; cero cambiosW/L/T. En mundoNiA, VQproduce una lana
más pero empeora margen. No se combina arreglo27. Piloto1.568tras27; informe
CENSURA_FORECAST y preregistro28.99variantes construidas más2prototipos17:
las dos últimas son reventasVQ del loop29, todavía SIN validación/cola.

Loop29 preinscrito antes de construir: factorial padresVQ/top3 × tamaños20/50,
48desarrollos frente aV7corriendo; reutiliza fuentes top3exactas de20. Panel
cercano y ambas referencias reales, no cambiar confirm20 ni sumar N. Leer
preregistro29. Catálogo público09:49:34UTC:50entradas sin cambios vs09:01.
Último snapshot de ladder sigue09:13UTC; sin nueva consulta ni envío.

## Corte operativo 09:36 UTC —20corriendo,27validado y en cola

Confirm19_fixedhash0terminó09:22:12UTC:3.200episodios,832noops exactos, delta0
ambas políticas. Cambian6/704acciones propias cada una, sólo contraguru6en
tres semillas; ya eran victorias. No inertes, no seleccionadas ni enviadas.
No sumar la medición original inválida. Leer CIERRE_TRIGO19.
Pilot20corre;21–27esperan en secuencia. No duplicar procesos.

Loop27validado72partidas/noop17.256/max404ms,120.792cantidades propias exactas.
Original48falló sólo coberturaVQ, no se relajó: adenda previa+24contraTop3
reactivo demuestra6/8activaciones; contraV7VQ0/8,top32/8. Ambas corrigen datos,
conservan trabajo/cosechas/tiendas/pérdidas, cero escapes/productos terminales.
Los márgenes de desarrollo empeoran donde actúan, ningúnW/L/Tcambia. Registro
más fiel no implica estrategia mejor. Piloto960contra panel cercano tras26.
93variantes construidas más2prototipos17detenidos. Leer ATRIBUCION_VENTAS,
preregistro27y ADENDA_LOOP27_COBERTURA. Verificador final:verificar_cobertura_atribucion_ventas.py.

Consulta09:13:39UTC:VQ2290,3/95y top32119,0/84, COMPLETE. Seis replays nuevos
0914reproducidos719acciones/720estados/caja exactos, sin escapes propios.
Alternativas contra rival grabado favorecen margen top3en5/6, no prueba
reactiva ni explicación causal del rating. Ver FEEDBACK_0914; sin nuevo envío.

## Corte operativo 09:11 UTC — loop26 validado, confirmación principal activa

Confirm19_fixedhash0 continúa con sus3.200celdas registradas; no reiniciar ni
leer deltas parciales para ajustar variantes.20–26esperan en secuencia, un solo
torneo principal.91variantes competitivas construidas más2prototipos detenidos.
Loop26: dos políticas de semillas sobreVQ,40desarrollos/noop5.752/max327ms,
76compras modificadas verificadas. Kind activa2/8celdas, JIT8/8; conserva campo,
siembras/alimento/cosecha/tiendas/escapes y pérdidas en los cuatro mundos.
Ahorra0–20monedas sin cambiarW/L/T. No se ha demostrado ventaja competitiva.
Piloto960contra panel cercano tras25, confirmación disjunta si procede.
Leer `SEMILLAS_TARDIAS_2026-09-25.md` y preregistro26. La consulta pública09:01
no encontró cambios en las50entradas consultadas; sin nueva descarga/envío.

## Corte operativo 08:44 UTC — confirmación repetida por control inválido

Piloto19completo: tres variantes+2,734375pp, señal en2/32semillas; ambas
seleccionadas (both/front). Originalconfirm19cerró3.200pero FALLÓnoop: cuatro
hashes rivales distintos, mismasacciones propias/rewards. Se conserva inválido.
48reproducciones aislaron orden de set dependiente de PYTHONHASHSEED; todos
los720estados económicos comparados coinciden, fuentes externas intactas.
Nueva **confirm19_fixedhash0**corre desde08:43UTC, mismas3.200celdas/gates,
runtime fijo y registrado; no es otra confirmación independiente ni suma N.
Seis partidas técnicas/noop2exacto comprobaron el arreglo. Los seis waiters
20–25anteriores terminaron por cascada y se reiniciaron con logs nuevos; no
hubo partidas20–25antes del fallo. Leer `REPARACION_HASH_RUNTIME_2026-09-25.md`.
20–24validados y
en cola; un solo torneo grande, no duplicar.89variantes construidas más2
prototipos17detenidos. Adelanto24compra antes y permite ventas más tempranas:
36juegos/noop8.628/64llenados,4.480unidades descontadas del compromiso nativo,
max308ms. Nuevo catálogo público08:02UTCno cambia las50entradas anteriores.
Último ladder08:27:46UTC:VQ2292,9/92, top32103,4/81; no nuevo envío.
Tres replays nuevos0828reproducidos719acciones/720estados; máximo181ms,
cero errores observados/escapes propios/productos finales. Dos victorias top3,
derrotaVQpor409; muestras de recencia, no estimación global. Ver informe0828.

Loop25 registrado y en espera tras24: cinco fuentes existentes, panel reactivo
VQ/top3/V7/HS4 y confirmación agregando Harvest68/arshs3. Piloto1.920,
semillas1063000–015; confirmación1064000–031. No depende de quién gane19–24.
Auditoría15replays: mediana99,17%de vector de campo idéntico,71,27%mercado
activo. Descriptivo, no código identificado ni efecto causal. Validación del
analizador con1.920partidas históricas/noop448, sin nuevas simulaciones.
Ver `PREREG_LOOP25_PANEL_CERCANO_2026-09-25.md`; ningún envío automático.

## Loop activo desde 2026-09-25 01:02 UTC

El usuario pidió explícitamente seguir investigando y probando en un **loop
continuo**, sin detenerse al cerrar una ronda. Objetivo persistente activo.

- Loop1: ocho variantes sobre VQ, producción/forecast, 1.000 episodios completos.
  PROMISING: pred_top3 +9,375 pp; pred_fast2 +3,125. Ambas a confirmación.
  Protocolo `PREREG_LOOP1_2026-09-25.md`; semilla 995000–995003.
- Loop2: recuperación de siembras + inversión en tomates, cinco variantes,
  616 episodios completos; ninguna señal agregada positiva. Reparaciones
  y dos variantes de tomate no se activaron en estas cuatro semillas.
  Protocolo `PREREG_LOOP2_2026-09-25.md`; semilla 998000–998003.
- `continuar_loop_publicos.py` encadena esos pilotos, verifica controles,
  selecciona según reglas fijadas y ejecuta confirmaciones disjuntas. Usa
  `torneo.py` y `pareado_torneo.py`; no es otro harness. NO subir automáticamente.
- **Confirm1 completa**, 1.600 episodios, noop416/416, cero errores. Top3
  **+10,795 pp**, IC95 dos vías [−0,115;21,706], cumple gate de prueba real;
  fast2 +2,841 pp, no cumple gate. Top3 máximo757ms, mecanismo de mejora y
  única celda de daño reproducidos. Decisión en `DECISION_ENVIO_TOP3_2026-09-25.md`.
- Loop3 completo: 504 episodios; herd_future −84,375 pp, EV600 −34,375,
  EV1500 0 (inerte), EV_future −40,625. No seleccionadas, sin confirmación.
  Noop96/96, cero errores. Sonda para explicar el gran daño de herd_future.
- Loop4 completo: 384 episodios, noop128/128; recover_now cambia una de64
  partidas, +1,5625pp, IC95 semilla [−1,62;4,75]. Sólo una semilla positiva;
  no pasa gate de dos. INCONCLUSIVE, no envío. No sumar el caso dirigido previo.
- Piloto loop5 completo: 616 episodios, noop104/104, cero errores. Early12_9k
  inerte; early12/14/16_6k −18,75pp, late18_6k +3,125pp. Sólo seed1005002
  activa cambios. **Confirm5 completa**: late18_6k −21,591pp, IC95 dos vías
  [−36,90;−6,28], 1.152 episodios, noop384/384, cero errores. REJECTED.
  Cambió156/352 partidas; ninguna celda mejor y38 peores. No enviar.
- Loop6 completo:736 episodios, noop112/112, cero errores. EGG/MELON/ambos
  delta0; EGG cambia46/64 acciones y MELON es inerte. Top3+fast2 −6,25pp.
  Ninguna seleccionada. Controles factoriales: VQ78,125%, fast2 70,313%,
  top3 96,875%, combinado90,625%. No asumir suma de efectos de rondas previas.
- Loop7 completo: cuatro políticas de tomates en suelo SE libre, 4/8
  plantas d16/d18, sobre top3. V2 podía inhibir R51; v3 corrigió contratación
  pero perdió cuatro tomates por overflow. V4 separa riego/cosecha:16 diagnósticos
  completos, plantas y ventas16/32 confirmadas, R51 y ovejas conservados.
  Piloto1.248 completo, noop256/256. D16 inertes; d18 +1,5625pp cada una,
  IC dos vías[−3,41;6,54], cambia16/128 partidas en dos semillas.
  **Confirm7 completa**:1.600 episodios, noop416/416, cero errores. Ambas
  d18 inertes en352/352 partidas del pool; delta0, IC dos vías indefinido.
  INCONCLUSIVE_NOT_SELECTED: no prueba de beneficio, no envío.
- Loop8: seis variantes de patrones (rank5/7, historia120/360,
  ajuste por producto y desfase temporal). Validación16 juegos completa,
  noop1.438 acciones idénticas, cero errores, máximo271ms. Piloto1.472
  completo:1.472 episodios, noop224/224, cero errores. History360, phase2 y
  rank5 +1,5625pp cada uno (una celda mejor); rank7−3,125, history120−10,9375,
  product3−1,5625. Desempate registrado selecciona history360/phase2.
  **Confirm8 completa**:1.600 episodios, noop416/416, cero errores.
  History360+2,8409pp, IC dos vías[−1,249;6,931], debajo del gate3; PROMISING
  sin envío. Phase2−3,4091pp, IC[−13,23;6,412], inconcluso sin selección.
- Loop9 completo: seis rebaños incrementales (2/3/6 ovejas, día12/14),
  sin comprar tierra y con demanda YARN ya visible. Se validan22 partidas
  dirigidas por versión antes de encolar1.920. V2 corrige cosechas tardías;
  motor confirmó36/53/83 entregas completas en ambos asientos. **V3** incluye
  seis ovejas compradas pero aún sin colocar y lana privada en la proyección.
  Otros22 juegos válidos, forzadas byte de acciones/rewards idéntico a v2;
  seis variantes normales inertes en ese mundo. Manifiesto v3 actualizado
  antes del piloto9. **1.920 completos**, noop320/320, cero errores; las seis
  inertes128/128contra pool, acciones propias/rivales idénticas, delta0 e IC
  dos vías indefinido. Sin selección/confirmación. Total42variantes competitivas.
- Loop10 piloto completo: adelantar conversión COW→SHEEP a días3–7,
  fuera de la regla8–11 ya existente. Seis políticas de fecha/demanda/caja.
 48 juegos dirigidos, noop4.314 turnos exactos, max284ms. En mundo YARN/YARN:
  dos compras/colocaciones aceptadas,49 lanas cosechadas, cero escapes/créditos
  pendientes/inventario final. En dos mundos sin YARN temprano son inertes.
  Piloto1.920 válido, noop320/320, cero errores: y2_m100 +2,34375pp (ambas
  fechas), y1_m100 −8,59375pp, y1_m500 −2,34375pp. D3/D6 tienen acciones y
  rewards idénticos128/128por pareja: no son réplicas independientes.
  **Confirm10 completa**,1.600episodios nuevos1019000–015, noop416/416,
  cero errores. Ambas y2 inertes352/352contra pool; delta0, ICdos vías indefinido.
  INCONCLUSIVE_NOT_SELECTED, sin envío. No refuta beneficio en contextos ausentes.
  Auditoría del daño y1:200monedas extra impiden compra de trigo191 (7→0),
  fallan alimentaciones y escapan tres vacas239; base0. No atribuirlo sólo
  a precios de lana. Próxima hipótesis: reservar insumos futuros antes del swap.
  Y2 sólo actúa en una de16semillas; cobertura rara limita inferencia/gate global.
- Biblioteca auditada:2.398 streams,64/64 pares de tiendas,24–63 por par.
  Doce streams recientes de ventas aceptadas son nuevos por fingerprint; no
  agregan pares de tiendas. Fecha de biblioteca original desconocida (ids−1).
  Loop11 ahora valida tres bibliotecas (DSM4, ladder8, todas12):20juegos,
  noop2.876turnos exactos, max250ms; ladder/all sí seleccionan un stream nuevo.
  Piloto1.920 con32semillas1021000–031, luego confirmación de32semillas;
  **Piloto11 completo**:1.920episodios, noop448/448, cero errores. Tres deltas0,
  ICdos vías indefinido. DSM inerte256/256; ladder/all cambian18/256acciones
  propias y10rivales en tres semillas, sin W/L/T distintos. Ladder/all son
  equivalentes256/256en ambas acciones/rewards. Sin selección/confirmación.
- Loop12 completo: tres aperturas nativas sobre top3 y MarketShock
  público con entrada corregida.12juegos, noop1.438turnos, max229ms; tomate
  inicial produjo4unidades y sustituye una vaca. Trigo temporal de base/cycle
  se cosecha en87, distinto al contador heredado que esperaba53. MarketShock
  tiene un escape tardío de ganso; no se oculta.1.008episodios, semillas1025000–007,
  **1.008 completos**, noop192/192, cero errores. Original−3,125pp, cycle0,
  tomate−80,46875pp, MarketShock−64,0625pp. Los dos últimos REJECTED, ninguna
  seleccionada/confirmada. Cycle cambia128/128acciones: delta0 no implica inercia.
  Seis juegos de mecanismo reproducen caja/rewards; tomate cambia tiendas.
  En su caso adverso sube nuestro dinero pero gana más el rival: no usar dinero
  bruto para adoptar. Total55variantes construidas al registrarlo.
- Loop13 validado/encolado: cuatro ventas preventivas de excedente WHEAT/FERTILIZER
  con reservas1/2días. V1 inválida por omitir VQ al capturar entrada antigua;
  fuente/evidencia conservadas. **V2**36juegos completos, noop4.314turnos,
 22activaciones con vector final/pérdida exactos del motor, max291ms,
  cero errores/escapes/diferencias en animales sin alimentar al cierre.
  Piloto1.248 **completo**, noop256/256, cero errores: wheat1/inputs1/inputs2
  +4,6875pp y wheat2+3,125pp; ICdos vías cruzan0. Tres celdas mejores en dos
  semillas, ninguna peor para inputs1/2. Cambian56/128acciones; ambas fuentes
  son distintas en32/128juegos. Desempate registrado selecciona inputs1/2:
  **Confirm13 completa**,1.600episodios1029000–015, noop416/416, cero errores.
  Ambas delta0/ICdos vías indefinido, ninguna celda mejor/peor; no pasa gate.
  No son inertes: inputs1cambia107/352acciones einputs2cambia86/352.
  Márgenes suben103/82partidas y bajan4cada una, pero ningún W/L/T cambia.
  Dinero diagnóstico no sustituye criterio: inconclusas, sin selección/envío.
  Auditoría12juegos reproduce hashes propios/rewards/caja: pérdidas8→4/6,
  27→9/17 y9→5/6en las tres celdas positivas. Caso neutral6→3, pero omite
  tres FEED posteriores y cosecha3MILK/2EGGmenos; no afirmar alimentación
  universalmente preservada. Mismas tiendas, ningún escape en los12diagnósticos.
  Total59variantes construidas al registrarlo.
  Motivación: c0nrad nos ganó con menos movimiento/jornales y se verificaron
  33unidades propias perdidas en cinco descargas nocturnas; rival0. Guardas ya
  existentes no lo solucionan conservando el vector final. JSON aislado cambia
  orden de bolsas y da predicción falsa en527; reconstrucción viva sí coincide
  con motor en5/5. Ver feedback y `c0nrad_*_audit.json`.
  En mundo dirigido1272457736 contra arshs3 reactivo, reserva1día reduce
  pérdida27→8, reserva2días27→20; quedan pérdidas residuales. En1004000
  brazo2días inerte;1027000 permite diferenciar trigo/fertilizante. No es W/L OOS.
- Loop14 validado/encolado: cuatro reglas de valor del alimento, multiplicador
  0,5/2,5, conservar FEED ovino o conservar todo FEED nativo.36juegos, noop4.314,
  máximo271ms, cero errores/escapes/inventario final; todas cambian acciones
  en tres mundos, consumo de trigo y producción confirmados por motor.
  **Piloto14 completo**:1.248episodios, noop256/256, cero errores. Half−12,5pp
  (ICdos vías[−33,693;8,693], inconcluso no seleccionado); double−26,5625,
  keep_sheep−50,78125, all−64,84375con ICdos vías negativos: REJECTED.
  Todas cambian128/128acciones propias. Sin confirmación ni envío. Ocho
  diagnósticos reproducen rewards/caja y conservan tiendas: producir más
  puede reducir ingresos; producir menos puede beneficiar más al rival.
  Total63variantes competitivas al registrarlo.
  Auditoría previa de8replays top3: PASS no implica trabajo útil pendiente;
  ningún CARE útil omitido entre esas oportunidades y60huecos WATER sin
  efecto inmediato/próximo amanecer ni muerte evitada esa noche.261huecos
  FEED motivan ablar filtro económico, sin asumir que todos fueran errores.
- Loop15 validado/encolado: cuatro reservas de caja antes de sustituir vacas,
  alimento hasta cierre/24/48h o todas las obligaciones24h.42juegos válidos,
  noop4.314, max294ms. En caso adverso:night permite una oveja, compra4trigos
  y evita tres escapes; resto conserva base. En caso solvente:night/24permiten
  dos ovejas,48/all24inertes. No seleccionar por esos rewards. Piloto1.568
  con control antiguo, semillas1034000–015, **completo**:1.568episodios/noop288,
  cero errores. Night/24−12,5pp(ICdos vías[−36,221;11,221]),48/all24inertes128/128,
  legacy−18,75como control. Sin seleccionadas/confirmación. Night/24cambian40/32
  acciones; coinciden entre sí en104/128partidas(ambas acciones/rewards).
  Ocho diagnósticos: reserva evita tres escapes en1034015, pero1034010pierde
  sin escasez de trigo: más lana vendida por menos dinero, menos leche. Caja
  suficiente es necesaria, no criterio de rentabilidad. Total67variantes al registro.
- Loop16 validado/encolado: cuatro mezclas iniciales (1/2vacas→ovejas o viceversa),
  sin más peones/rutas.48juegos/noop5.752turnos, max329ms, compras/colocaciones
  y costes±100/200aceptados, crédito0al día1. Todas cambian acciones en4mundos.
  Cambiar caja inicial altera cultivos y tiendas: es efecto total, no sólo lana
  por leche. Sheep2pierde una vaca215en1272457736;1036000tiene escapes tardíos
  en base/cow1. Se conservan, no ocultarlos. Piloto2.496con32semillas1037000–031,
  confirmación32semillas1038000–031. **Piloto16completo**:2.496episodios,
  noop512/512, cero errores, base92,1875%. Sheep1−86,71875pp, resto−92,1875pp,
  todos REJECTED con ICdos vías negativos. Todos cambian256/256acciones propias.
  Sin seleccionadas/confirmación. Dos celdas adversas reproducidas con caja:
  cambian tiendas; sheep1sube caja831pero rival8.971. No es efecto puro de especies.
  Total71variantes construidas.
- Auditoría de12replays top3:3CARROTpor decay,1por sequía y4MILKen campo final.
  33MILKtruncadas con inventario previo0son exceso de cuidado antes de primer
  yield; no se arreglan cosechando antes.14EGGcon cap sí requerirían ruta/entrega.
  Motivó loop17; ver `AUDITORIA_PERDIDAS_CAMPO_2026-09-25.md`.
- Loop17 detenido en desarrollo:24juegos/noop4.314/max284ms, ejecución válida
  pero cap_full confunde inventario actual con inventario nocturno. Omite FEED682,
  luego HARVEST687 libera espacio y pierde un huevo de producción700. Cap_first
  cambia una valoración pero no acciones en tres mundos. Error de modelo temporal,
  no rechazo por rewards ni estimación poblacional. No lanzar piloto17/subir:
  `capped_bonus_decision.json` marca competitive_ready=false y runner lo exige.
- Loop18 validado/encolado directamente tras16: V7cda529cb yHS48378f73c públicos
  nuevos,24juegos/noop2.876/igualdad oficial-nominal5.752turnos, max431ms.
  Cero estados fatales, cero errores en contadores nuevos observados, cero escapes
  y productos terminales en esos mundos; quedan semillas. Piloto704semillas
  1043000–015 **completo**704episodios/noop192/errores0: V7−21,875pp
  (ICdos vías[−57,741;13,991], inconcluso); HS4−30,46875pp
  (IC[−56,648;−4,290], REJECTED). Ambos activos128/128. Ningún seleccionado
  ni confirmación. **Corre19desde07:33:37UTC**;20/21/22esperan.
  No sobrescribir rivales antiguos del pool.
  Total73variantes competitivas construidas más2prototipos17detenidos.
  Ver `FUENTES_PUBLICAS_0548_2026-09-25.md`; afirmaciones externas no son evidencia.
- Loop19 validado/encolado tras18: prioridad de BUYWHEAT, mitad de cantidad y
  ambas, sólo grandes compras de reventa planificada.30juegos/noop4.314/max305ms,
  ejecución/slots/llenados aceptados verificados. En588616997actúan20/38compras;
  otros dos mundos inertes. Sin escapes en desarrollo, mitad altera alimento
  y añade2MILK. No elegir por rewards. Cobertura estática sólo5/64pares motivó
  ampliar antes del piloto a32semillas por bloque; piloto1.9201046000–031,
  confirmación1047000–031. Runner en espera reiniciado, activos intactos.
  Piloto1.920**completo**, noop448/448, cero errores: las tres+2,734375pp,
  ICdos vías[−3,903;9,372],4celdas mejores/0peores, sólo2/32semillas activas.
  Cambian16/256acciones; compartenW/L/Tpero sólo240/256acciones/rewards.
  Desempate selecciona both/front: **confirmación3.200corriendo desde07:57UTC**.
  Actualización08:44: original completo pero noop inválido por hash del runtime;
  nueva confirm19_fixedhash0corriendo, mismos agentes/muestra/gates. No usar
  el bloque original para promoción ni relajar igualdad literal.
  Ocho mecanismos reproducen hashes/rewards/caja: frontahorra1508/941de trigo
  con igual cantidad y producción; half/bothalteran3WHEAT/3CARROTen un caso.
  Total76variantes competitivas construidas más2prototipos17detenidos.
  Ver `TRIGO_REVENTA_2026-09-25.md`; nuestra fuente reproduce exactamente el
  replay real de origen, pero no conocemos ni copiamos su política rival.
- Loop20 validado/encolado: tres nuevas reventas de trigo alrededor del consumo
  conocido del pueblo, topes20/50/80, sin tocar compras nativas19.30juegos,
  noop4.314turnos, max358ms, cero errores/escapes/stock final.146compras y cierres,
  7.862unidades llenadas/liquidadas;42ventas heredadas integradas sin duplicar.
  Tres brazos activos en tres mundos, alimentación/producción/tiendas/pérdidas
  preservadas allí. Piloto1.9201049000–031tras19, confirmación1050000–031.
  Sonda sintética400escenarios/800piernas exactas demuestra riesgo rival:
  78pérdidas pese a pronóstico positivo sin rival. No seleccionar por caja.
  Total79variantes construidas más2prototipos detenidos.
  Ver `REVENTA_TOWN_2026-09-25.md`; no afirmar beneficio por spread anunciado.
- Loop21validado/encolado: cuatro reglas para señales adicionales del forecast
  (rango2, consenso, mitad, horizonte12), conserva regla del patrón1.42juegos,
  noop4.314turnos, max293ms, cero errores/escapes/producto final. Todas activas
  en tres mundos; cambia comida/cosecha en dos, mismas tiendas. No seleccionar
  por rewards. Piloto2.0161052000–015tras20, controlVQen ambos bloques y dos
  rivales públicos0548añadidos antes de conocer su piloto18; confirmación
 1053000–015contra13rivales, gate adicional≥0vsVQ. Total83variantes construidas
  más2prototipos detenidos. Ver protocolo21.
  Ocho replays reales recientes, cuatro por fuente, reproducidos por código
  enviado:719acciones/720estados exactos;16juegos con contrafactualVQ/top3,
  caja conciliada/max348ms/sin escapes propios. Top3mejora margen7/8pero
  rival grabado no reacciona: no es estimación competitiva. Ver FEEDBACK_PAREADO_0653.
- Loop22validado/encolado: Harvest Ledger V68SHA3b543611y selector-offab4cbb92.
  Master descargado07:12idéntico al V7ya probado, deduplicado.42juegos/noop4.314,
  entradas oficial/nominal8.628turnos exactos, max713ms, cero errores observables,
  escapes/productos finales/créditosYpendientes. Selector activo3mundos, swaps
  1/1/2aceptados; quedan semillas2/0/6y cambian tiendas en1578791335. Piloto1.280
  tras21, controlVQ/gate≥0vsVQ. Total85variantes más2prototipos; ver informe0712.
- Loop23validado/encolado: suministro del peón ovino compacto, buy/hold, dos fuentes
  generales. Replaydavion113174624reproducido exactamente: otro actor consume5
  antes de que peón12retire6; recibe1y queda21turnos PICKUP0. Seis ovejas no
  alimentadas/cuidadas; no FEEDfallido ni problema de caja. Sonda compra6→11
  recupera24lanas vendidas, caja propia+22pero rival−4.137, margen−2.904→+1.255
  contra cinta fija. Regla general lo reproduce sin seed/paso fijos.48desarrollos
  reactivos válidos/noop8.628/max327ms, activo sólo contraV7en mundo dirigido,
  ambos asientos. Retira6trigos completos, restaura6FEEDy24lanas, margen−5090→−1093;
  no convierte esa derrota. Base/arshs3/VQ/HS4inertes. Piloto2.560tras22,
  controlVQy confirmación disjunta.87variantes construidas
  más2prototipos; ver `SUMINISTRO_OVINO_2026-09-25.md`. No es mejora OOS aún.
- Loop24validado/encolado: adelantar compra nativa de trigo sobreVQy top3,
  cancelar sólo llenado observado en origen antes de guardas de alimento.
  36juegos/noop8.628/max308ms,64adelantos/4.480unidades compradas y descontadas
  del plan nativo. Cuatro casos dejan3de89sin adelantar, solicitud posterior
  no llena por capacidad; no duplican lo comprado. Activos sólo en593858505,
  ambos asientos;16eventos por juego, otros dos mundos inertes. Alimento
  preservado, cosecha453de3CARROT→3WHEAT; ventas también se adelantan por stock.
  Sonda contraGrimReapergrabado margen−3070→+313; reactivoarshs3mantieneW.
  Piloto2.560tras23,32semillas, VQbase/top3control; confirmación disjunta.
  89variantes construidas más2prototipos. Ver `ADELANTO_TRIGO_2026-09-25.md`.
  Sonda sintética384casos/1.152piernas exactas: comprar antes sin vender antes
  pierde dinero32/128; adelantar ambas pierde beneficio contra rival pasivo24/32.
  No son tasas poblacionales. Catálogo08:02sin cambios en50entradas; no duplicados.
- Fuentes públicas nuevas: MasterEngine actualizado es tds25 byte exacto,
  excluido. MarketShock12ad317e diferente; loader elegía instalador. Corrección
  de entrada1c94b979 probada idéntica al `module.agent` del autor en8juegos.
  Fuente/adaptación separadas en `FUENTES_PUBLICAS_0400_2026-09-25.md`.
- Auditoría piloto7: cuatro filas TDS con acción propia idéntica y hash rival
  distinto, pero rewards/WLT idénticos. Ocho reproducciones (hashseeds0–3)
  dieron acciones/estados idénticos; origen de la variación neutral no resuelto.
  No afecta selección observada ni justifica afirmar determinismo universal.
- Scorecards actualizadas: `SCORECARDS_LOOP_2026-09-25.md`.
- Estado máquina: `docs/evidencia/loop_publicos_20260925/pipeline_state.json`.
  Logs: `results/loop_publicos_20260925_pipeline.log` y los logs de cada bloque.
  No modificar `torneo.py`, ni agentes de un bloque mientras corre. No lanzar
  otro torneo de ocho workers mientras el pipeline ocupe el equipo.
- Sonda nueva: falta una fresa tras DIG por maleza en replay 113061732. Reparación
  con reintento entre trabajadores no actúa por falta de riego el mismo día;
  inserción en un sufijo con turno final redundante sí recupera planta. Cambia
  tiendas/RNG, así que la sonda frente a replay NO mide ganancia competitiva.

Sonda posterior en bucle cerrado (mismo seed del fallo, ambos asientos, rival
arshs3 reactivo): reparación inerte en asiento 0; recupera planta y −671→+53 en
asiento 1, con tiendas diferentes. Caso dirigido, no estimación poblacional.
La prueba de cobertura quedó registrada y encolada como loop4.

Snapshot vigente07:41:40UTC(sufijo0742):VQ**2296,9/91episodios listados**,
top3**2094,4/79**, ambasCOMPLETE. Incluyen validación. Sin nuevo envío.
Siete replays nuevos por recencia: cada fuente reproduce719acciones/720estados
exactos/caja, máximo187ms; cero escapes propios/productos finales/PICKUPW0.
Top3:2V2D;VQ:2V1D, no WRpoblacional. ContraGrimReaper,19/19compras grandes
rivales ocurren un turno antes con igual cantidad pedida; coste2988menos con
1359unidades vs1361propias. Nueva hipótesis de adelanto de compras, distinta
a prioridad19/nuevos roundtrips20, aún sin construir. Ver `FEEDBACK_0742_2026-09-25.md`.

Snapshot anterior06:52:55UTC (sufijo0653): VQ**2289,1/88episodios listados**,
top3**2094,7/75**, ambasCOMPLETE. Incluyen validación. No nuevo envío. Las
cuatro partidas recientes por fuente se seleccionaron antes de leer rewards.
Diagnóstico8replays/16reproducciones en `FEEDBACK_PAREADO_0653_2026-09-25.md`.

Líder actual consultado 01:36 UTC: DSM 3128,7, submission 56518845. Cuatro replays
recientes reproducidos exactamente; compra cuarta tierra día 10 y cultiva más
tomates, con diferencias grandes de composición por mundo. No inferir causalidad
ni algoritmo del score. Informe: `LIDER_Y_FUENTES_2026-09-25.md`. Dos notebooks
con nombre nuevo eran copias de tds25: se deduplicaron sin repetir torneo.

Snapshot histórico01:52UTC: VQ56535264 **2319,5 /24 episodios listados**, original
56511619 **2275,7**. VQ aún joven, no afirmar superioridad por este rating.
Top3 **56537205 COMPLETE**, enviada 2026-09-25 01:56:34 UTC, commit ba1fda8,
sha9668e30a byte exacto de confirmación. Validación113099118: 720 pasos,
DONE/DONE, cero errores/timeouts. Recibo confirma tres envíos restantes.
Desplaza al original y conserva VQ, su padre, como control. Snapshot02:04UTC:
VQ2364,6 y top3 729,5 inicial. Snapshot02:33UTC: VQ2306,3 y top3 1459,1;
top3 tiene10 episodios listados02:34, incluida validación. Cuatro replays
por recencia:3V/1D, cero escapes propios, inventario terminal0 y cero errores
fatales. Derrota contra c0nrad−23.180: rival32 ovejas frente a17, casi sin tomate.
Cuatro reproducciones exactas y caja conciliada. Lana391/759 unidades,
ingresos69.502/113.264; rival paga menos jornales y tierra. Ver
`FEEDBACK_TOP3_2026-09-25.md`. Muestra pequeña, no WR ni fuerza estable.
Snapshot posterior02:58UTC: top3 1738,5 / VQ2268,6, sin recuento nuevo sincronizado.
Snapshot **03:39:41UTC**: top3 **1941,6 /30 episodios listados**, VQ
**2259,1 /56**, ambos COMPLETE; recuentos incluyen validación. Cuatro nuevas
partidas seleccionadas por endTime antes de leer rewards:4V, márgenes923–2891.
720 estados exactos×4, caja conciliada, cero escapes propios/inventario final.
Producción muy similar a rivales en esa muestra; no es superioridad causal vsVQ.
Archivos con sufijo0333 se consultaron03:39; metadatos `.fetch.json` dan hora real.
Snapshot **04:30:35UTC**:top3 **2022,5 /46episodios listados** y VQ
**2288,2 /69**, ambas COMPLETE. Archivos sufijo0431; hora real en metadatos.
Snapshot **05:13:31UTC**:top3 **2068,8 /58episodios listados** y VQ
**2287,2 /81**, ambas COMPLETE. Archivos sufijo0515; hora real en metadatos.
Recuentos incluyen validación; ninguna submission nueva desde top3.
Cuatro replays nuevos por recencia0515:4V,márgenes240–1.480,720estados exactos
y caja conciliada cada uno; cero escapes propios/stock terminal. Originales
archivados. No estima WR global ni ventaja causal sobre VQ; ver FEEDBACK_TOP3.
Snapshot **05:47:41UTC**:top3 **2093,6 /69episodios listados** y VQ
**2285,8 /83**, ambas COMPLETE. Sufijo0548, recuentos incluyen validación.
Sin otra submission. Después se descargaron cuatro replays fijados por recencia
de esa consulta:3V/1D, márgenes−1.702/+35/+1.230/+459;720estados exactos/caja
conciliada cada uno. Cero escapes propios/stock terminal de productos. Contra
today, flujo neto de WHEAT propio12.308vsrival15.501; diferencia−3.193que se
compensa parcialmente con otras ventas. No demuestra que sobreoperar trigo
sea la causa ni justifica desactivar arbitraje sin auditoría temporal.

Último snapshot **06:26:02UTC**:top3 **2084,7 /73episodios listados**, VQ
**2294,3 /85**, ambas COMPLETE. Sufijo0628; incluyen validación. Sin envío
nuevo ni nuevos replays descargados de esta consulta. La mejora local de top3
no demuestra transferencia superior aVQ; conservar ese control para próximos
candidatos y no elegir padre sólo por el panel histórico.

Lo siguiente es el cierre de la ronda anterior; no significa parar este loop.

## Estado vigente — 2026-09-25 UTC / 2026-09-24 America/Bogota

Esta sección sustituye los planes y estados «en curso» históricos de abajo.
Consulta API archivada en `docs/evidencia/research_20260925/`:

| Agente | Submission | Score observado | Episodios | Estado |
|---|---:|---:|---:|---|
| arshs3 público original | 56511619 | 2292,5 | 148 | Mejor referencia real, activa |
| v13 público | 56511611 | 1857,9 | 136 | Desplazada por VQ |
| arshs3 + VQ | 56535264 | 810 inicial | sin actualizar | REAL_WORLD_CANDIDATE, COMPLETE |

VQ se envió desde `submission/main_publico_arshs3_vq.py`, commit a9f59ee,
sha 9b463dfb, usando la evidencia ya existente (40-0 espejo y otros bloques,
0 cambios W/L/T en el pool). No se repitió el barrido VQ ni ADV. La CLI confirmó
4 envíos restantes tras subirla. Arshs3 original queda activa para comparar;
otro envío desplazaría a esa referencia. `submission/main.py` aún es el original;
el archivo efectivamente enviado está identificado en SUBMISSION_HISTORY.

**Hallazgos nuevos:** muestra fija por recencia, 16 partidas arshs3 y 8 v13,
sin seleccionar por resultado. Arshs3 4V/11D/1E, cero escapes, inventario terminal
propio cero. No es su WR histórico. Cuatro partidas se usan para diagnosticar
el predictor: la primera sonda contó 12/67 coincidencias, pero omitía ventas
simultáneas. **CORRECCIÓN:** cuatro reproducciones exactas con ledger dan 50/67
en t..t+4, 42 en el mismo turno. Una acción reconstruida del agente difiere de
la real (SELL WHEAT en step 623); el ledger se validó contra las acciones reales,
sin esa discrepancia. No atribuir causalidad a cada coincidencia.

**TERMINADO:** `forecast_pilot` (608 episodios), noop exacto 160/160. Gate
**−51,56** puntos (IC dos vías [−78,92; −24,20]); off **−68,75**
([−89,57; −47,93]). REJECTED ambos; no se ejecuta confirmación ni se suben.
Sonda causal de fallo: primeras acciones distintas step 440, mismas cantidades
totales vendidas, peor timing y +89 monedas pasa a −78. Protocolo inalterado:
`PREREG_FORECAST_GATE_2026-09-25.md`; resultados `forecast_results.json`.

**TERMINADO:** `public_refresh` (608 episodios), noop exacto 160/160.
Las versiones nuevas tds25 / hl25 (sha 127ed3e6 / 1dfd4630) obtienen **−7,81**
y **−9,38** puntos vs VQ. IC dos vías [−27,29; +11,67] y [−29,79; +11,04]:
inconcluso, sin señal agregada de mejora; ninguna cumple el criterio registrado.
No se ejecuta confirmación ni otro envío. No rescatar tds25 por su 10/16 en directo.
Protocolo `PREREG_PUBLIC_REFRESH_2026-09-25.md`; `public_refresh_results.json`.

**Cierre de esta ronda:** 1.216 partidas de torneo + ocho diagnósticas; todos
los procesos terminaron. Consulta final: original 2288,6; VQ 1198,5 con apenas
media hora de vida, sin actualizar episodios. No compararlos por ese rating.
El informe completo es [RESULTADOS_2026-09-25.md](RESULTADOS_2026-09-25.md).
Siguiente frontera: aprender de pérdidas actuales y separar producción de precios
realmente ejecutados; preservar el predictor y dejar que VQ reúna evidencia real.
No hay monitoreo automático programado ni candidato nuevo pendiente de envío.

Se endureció el mismo `torneo.py`: no sobrescribir, abortar ante inválidos o
cambios de fuentes, comprobar cobertura, archivar fuentes y capturar acciones
antes del motor. La sonda comparó el wrapper con el loader oficial: 1.438 acciones
y rewards idénticos (dos episodios). No usar `pareado_torneo.py` sin comprobar
antes que el bloque está completo y que cada celda contiene ambos asientos.

La autorización autónoma de investigación y submissions continúa. No hay una
aprobación pendiente para los agentes públicos ya enviados. Las restricciones
anteriores y las listas de procesos de septiembre 21–24 se conservan abajo sólo
como historial; no relanzar sus comandos por leerlos aquí.

## Historial previo a esta revisión

Actualizado: 2026-09-23 20:45 (America/Bogota) = 2026-09-24 01:45 UTC. Deadline 2026-09-30 23:59 UTC.
Loop autónomo autorizado por el usuario (mensaje del 2026-09-21): harness + ladder
como evidencia complementaria, submissions como instrumento (5/día).

## ⚠️ PIVOTE 2026-09-24: el techo real está en los agentes PÚBLICOS

**Leaderboard 2026-09-24 01:02 UTC (9.937 equipos):** #1 3057 · #10 2921 · #100 2715 ·
#500 2499 · #1000 2308 · #2000 1807 · **nosotros ~1160 = puesto ~3.500**.
280 equipos ≥ 2600, 1.635 ≥ 2000.

**Causa:** existe un ecosistema de agentes públicos Apache-2.0 (Code tab) —
cintas de ruta (yhay81) + router por tiendas + capas reactivas (Ahmed Berat Özer
V25-V48, Thomas Tschinkel v9/4 y v13, familia Herd-Safe de Dmitrii Gluzdov /
arsgorynich, haideptry...)— que puntúan 2500-2950 en el ladder. El de Thomas
(v9/4, sub 56269928) documenta **2944,7 con 201 partidas**. Desde el 2026-09-02
no volvimos a medirnos contra ellos: optimizamos dentro de una familia débil.

**Torneo en bucle cerrado** (`torneo.py`, motor oficial 1.32.7, cargados como Kaggle
= último callable, 10 semillas 910000-009 × 2 asientos, 720 partidas, 0 errores,
máx 215 ms/turno). Evidencia: `docs/evidencia/torneo_publicos/torneo_rr1.*`.

| agente | origen | % vs resto | nota |
|---|---|---|---|
| **arshs3** | arsgorynich, Herd-Safe v3 forecast4 | **98,8%** | gana a TODOS (ars40 18-2, resto 20-0) |
| ars40 | arsgorynich, More Wheat v11 | 81,2% | |
| hsov | haideptry, Shepherds Ledger herd-safe | 76,2% | |
| h2965 | haideptry, 2965 Master Hybrid (V59) | 67,5% | |
| guru6 | guruprasaathas111, Master Engine V6 | 47,5% | |
| v13 | Thomas Tschinkel, Metav4 v13 | 41,2% | gana a v94 20-0 |
| v94 | Thomas Tschinkel, 2945 Farm (ladder 2944,7) | 25,0% | pierde con toda la familia Herd-Safe |
| seek+gcal | nuestra activa 56507746 | 8,8% | pierde 0-20 con CADA público, −$12..16k |
| decem+gcal | nuestra activa 56507747 | 3,8% | idem |

**Rondas 2 y 3** (`torneo_rr2`, `torneo_rr3`; seeds 920000-009 y 930000-009;
560+560 partidas, 0 errores, máx 291 ms/turno; límite de Kaggle 1 s + reserva):

| agente | rr2 % | rr3 % | directo vs arshs3 |
|---|---|---|---|
| arshs3 | 82,9 | 77,1 | — (**invicto: 22/22 cruces en las 3 rondas**) |
| tds (tetsutani, demand-preserving, 22-sep) | 72,9 | 78,6 | 8-12 / 7-13 (margen −$10..−$14) |
| hl59 (haodou092, Harvest Ledger V59) | — | 78,6 | 7-13 (≈ tds: 14 empates de 20) |
| hybu (wzhengbiao) | — | 53,6 | 8-12 |
| ars40 ≈ dmw (More Wheat) | 50,7 | — | 6-14 |
| wz15, lp16, obr, ob3, hsov≈hs2700≈st25, bv48 | 26-44 | 5-44 | 1-19 .. 7-13 |

Entre los públicos top los márgenes medios son de decenas de dólares sobre ~$115k:
las partidas se deciden en el margen.

**Activas desde 2026-09-24 04:28 UTC:** 56511611 (v13) y **56511619 (arshs3)**.
v13 se mantiene a propósito como segunda familia: su rating frente al de arshs3
mide si el bucle cerrado intra-público transfiere al ladder.

**Experimentos de capas sobre arshs3 (2026-09-24):**
- **VQ** (compactación de cola, tetsutani): contra el pool 0/120 celdas cambian
  (+$20/partida, mínimo −$6) → inerte en W/L; en ESPEJO gana 17-3, 40-0 (20
  semillas nuevas) y 95% (tercer bloque). `hsov2` (haideptry, 24-sep) ya es copia
  de arshs3: las copias circulan. **REAL_WORLD_CANDIDATE: arshs3vq** (sha 9b463dfb,
  `results/exp_publicos/arshs3_vq.py`, construido con `apilar_capa_vq.py` @e43ce1d).
- **ADV** (adelanto de ventas, Ahmed EXP293): descubrimiento +10 [−10; +30],
  confirmación −2,1 [−20; +16] → **REJECTED**. Intercambia partidas entre linajes.
- Derrotas de arshs3: mediana $521 (p25 $257, p75 $1.147); sólo 7/95 < $100.
  Micro-capas de final de partida no las voltean.

**Plan de envíos (día UTC 2026-09-25; hoy queda 1 envío sin usar a propósito):**
v13 y arshs3 juntan ~18 h de ladder = prueba de transferencia bucle cerrado →
ladder (predicción: arshs3 ≫ v13; 20-0 local). Luego: (1) subir arshs3vq, (2)
subir la segunda según esa lectura (v13 si transfiere mal; si no, tds o hl59,
el otro linaje top). El envío nuevo siempre desplaza al activo MÁS ANTIGUO.

Ficheros auditados estáticamente (sólo stdlib; `exec` de cadenas constantes sin
imports peligrosos; `open` sólo tras una variable de entorno de desarrollo o
`path=None`). Código en `results/publicos/` (gitignored; hashes en el meta).

**Decisión pendiente del usuario:** subir agentes públicos (código de terceros,
Apache-2.0). Propuesta: arshs3 (campeón en bucle cerrado) + v13 (rama distinta,
autor con el mejor registro de ladder documentado). Las cintas propias quedan
superadas por ~+1.500 Elo esperados.

**Limitaciones:** el torneo es intra-familia (forks emparentados); no mide contra
los top-10 adaptativos (mtmr_s1, feel the agi, DeeperNet), que según Thomas
abandonan la cinta en d12-18 y le ganaron 36-0 a v9/4. Ranking en ladder entre
públicos: incierto (±100 de ruido por submission según Thomas).

## BEST_CURRENT_CHAMPION (hasta el 2026-09-23; historia)

**CHAMPION_CANDIDATE: `107570947 + guardias`** — 56449108, commit 6527d3a,
**1.180 @24 ep, 15-9 (62%)**, 24/24 con 4 manos y 3 cuadrantes, derrotas ajustadas.
Paquete: `submission/main_107570947_guard.py` (= `submission/main.py`).
Segunda: `tree_v1+guardias` 56447472, 1.136 @40 (23-17). Ambas activas.
Champion formal anterior: `maj_107674293` (56245770, 857, 126 ep) — superada.

**Escalera de ratings a episodios comparables:** cinta 857 (126) · tree_v1 1082 (40) ·
tree_v1+g 1136 (40) · **107570947+g 1180 (24)**.

**Panel FUERTE (80 rivales de Majkel/DSM), la métrica que predice el ladder:**
guard:107570947 54,8% · 107570947 36,3% · guard:tree_v3 29,5% · tree 20,2% ·
cinta campeona 17,4% · HOZ 9,5%. **Las guardias valen +15-18 vs fuertes.**

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

## REGLA REFORZADA (violada dos veces hoy)

**`evaluar_lider.py` hashea sus fuentes (evaluar_lider.py, chassis, arquetipos,
tape.py, arbol_lider*.py, guardia_cinta.py, clasif json) al inicio y al final.
NO editar NINGUNO mientras una fase corre.** Preparar ediciones en el scratchpad
y aplicarlas al terminar. Si se edita por error: `git checkout <fichero>` antes de
que termine (funcionó el 2026-09-22 05:05).

## PROCESOS EN CURSO (al escribir esto)

- `evaluar_lider.py --phase majkel2 --seeds 4` → `results/majkel2.txt`: 12 cintas de
  Majkel ACTUAL (vs top-3) + guardias, vs 71 fuertes sin Majkel. Referencia
  guard:107570947.
- **Pendiente de lanzar al terminar:** fase `dsm` (27 victorias de DSM, nº1 actual)
  — la edición está en `scratchpad/evaluar_lider_con_dsm.py`; copiar sobre
  `evaluar_lider.py` cuando `majkel2` termine.
- Terminados: compare, compare2, tapes, fuerte; descargas (DSM 40, UMG 30, VADIM 30,
  MAJTAPE_LADDER 60, TREE1_LADDER 40, GUARD_LADDER 32).

## HALLAZGOS DE HOY (resumen; detalle en RESEARCH_BELIEFS.md)

1. **Manos d1 → resultado** (60 reales): 0-2 manos 0%, 3: 23%, 4: 60%. Guardia
   `bots/guardia_cinta.py` reserve=6. Sólo d1 (d2 residual 3/60; d3+ ninguno).
2. **Divergencia harness/ladder**: 71,5% local vs 40% real. Cintas pasivas no
   mueven el mercado d0.
3. **Tienda d3 explica derrotas** de la cinta fija: 60% BAKERY … 14% PIZZA.
4. **DSM vs Majkel 3-6**; cima decidida por 1-5%. Cintas de DSM no son mejor materia.
5. **compare**: cinta +12,1 > tree +9,0 > tree_v2 +4,8 (vs HOZ). Más cintas mezcladas, peor.

## SESION 2026-09-23 — en curso

**Ladder @13:11:** 56449108 (107570947+g) **1.163,7** @78 ep; 56447472 (tree_v1+g)
1.131,6 @81 ep. Rank equipo **3.510 / 9.919**. Nuevo nº1: Boey (3.112).

**Fallo de método encontrado:** el evaluador aplicaba las guardias con
`reserve=6` fijo; 72 de 79 cintas necesitan \$7+ (5 HIRE al alba, usan 4).
Todas las comparaciones previas entre cintas con guardias se hicieron con la
guardia a medias. Nuevo prefijo `gcal:` con `reserve_auto` (da 8 para
107570947 = exactamente la submission). `guard:` se conserva para reproducir.

**En curso:**
- Piloto `cal1` (`results/cal1.txt`): 111 cintas (Majkel-2652 ×30, Majkel-3075
  ×12, DSM ×27, UMG ×21, Vadim ×21) con `gcal:`, vs 32 fuertes balanceados
  (8 por fuente) × 2 seeds × 2 asientos = 14.592 ep.
- Descargas (`results/bajar_ronda2.txt`): 25 replays de Boey (56309208),
  M&M&P&Q (56378284), DECEM (56446088), Majkel-nuevo (56407295), Vadim-nuevo
  (56427964), seek inspiration (56407833).

**Hecho:** `cal1` (111 cintas) → `confirm_cal1` vs 148 rivales NUEVOS (rivales
del top-13 actual). Ganadora confirmada: **`110304538` (Majkel-3075) + gcal:
+18,9 [−0,5; +38,4] vs 107570947+gcal, positiva vs las 6 fuentes → subida como
56504082** (17:30). La #1 del piloto (umg_111191811) se desplomó a −11,7.

**Activas en ladder:** 56449108 (107570947+g, 1.164) y 56504082 (110304538+gcal).
⚠️ La próxima submission desplaza a **56449108**: sólo subir si 56504082 ≥ 56449108
o si la candidata nueva supera a ambas.

**En curso:** piloto `cal2` (`results/cal2.txt`, centinela `results/cal2.done`):
93 cintas de Boey/MMPQ/DECEM/Majkel-nuevo/Vadim-nuevo/seek + anclas, vs 32
rivales de fuentes viejas no usados en cal1, 2 seeds. Filtro grueso → etapa 2
(~20 brazos, más celdas) → confirmación vs `results/rivales_reserva_confirm2.json`
(76 rivales nunca usados), siempre con `gcal:110304538` y `gcal:107570947` en el
mismo bloque.

**Herramientas nuevas:** `comparar_pareado.py` (delta pareado, IC semilla y dos
vías, desglose por fuente), `extraer_fuente.py` (victorias + rivales de una
carpeta), fase `spec` del evaluador (brazos/rivales/semillas desde JSON).
**Lección de infraestructura:** esperar por fichero centinela, nunca por
`pgrep -f` con un patrón que aparece en el propio comando del bucle.

## CIERRE DE SESION 2026-09-22 — decision: CONSOLIDAR (revisada el 23)

Todas las vias de mejora sobre la cinta estan medidas y cerradas:
- Mejor cinta fija: 107570947, de ~70 candidatas de Majkel-2652/Majkel-3075/DSM.
- Guardias (caja d0 + compromisos): +15-18 vs fuertes; 100% mecanicas en real.
- Arboles: peores que la cinta sola vs fuertes (tree_v3+g 29.5% vs 54.8%).
- Hibrido cinta+chasis: colapsa al nivel del chasis (10-17% vs 43%).
- Cierre limpio (0.6%), acciones fallidas ~1%, ocio 4.7% (+2-4% maximo).

**Champion: `107570947 + guardias` (56449108).** Dejar converger. Segundo billete:
`tree_v1 + guardias` (56447472). El score de equipo es el mejor submission.

## NEXT_EXPERIMENTS (si se retoma; orden)

1. Leer 56449108 y 56447472 a ~100 ep (rating convergido, W/L por rival).
2. Unica capa barata no probada: dar trabajo a los peones sin orden (4.7% de
   mano-turnos), p.ej. barrido de riego a partir de h18 y DIG de maleza. +2-4%
   estimado, riesgo de interferir con la cinta. Medir vs fuertes antes de subir.
3. Si el ladder converge por debajo de 1150: subir 107570947+g de nuevo como
   billete adicional NO es investigacion (misma esperanza, mas varianza del max).
   Solo si el usuario lo pide.

### (historial de la cola)

0. **Leer piloto `dsm`** (`results/dsm.txt`, 27 victorias de DSM nº1 + guardias vs
   62 fuertes, 4 seeds). Top-3 → `--phase` de confirmación pareada con 8 seeds
   contra guard:107570947 (añadir fase análoga a `majkel2_confirm`). Si alguna
   supera con IC dos vías > 0 → subir con guardias (reserve calibrada a sus
   HIRE del alba: ver `empaquetar_cinta_guard.py --reserve`).
1. Si DSM no supera: **el enfoque de cinta fija ha llegado a su techo** (~el plan
   de Majkel-2652). Opciones: (a) consolidar 107570947+g y dejarlo converger;
   (b) subir 2-3 cintas top en paralelo (5/día) y dejar que el ladder elija;
   (c) capa reactiva — pero la evidencia dice que el gap con los fuertes es
   produccion tardía (+5-7% d21-25), no ventas.
2. `tree_v1+guardias` tiene 3/40 con 3 manos: sus cintas necesitan reserve=8.
   Sólo relevante si se vuelve a subir un árbol.
3. Leído majkel2 (hecho): ninguna cinta de Majkel-3075 > 107570947 (+1,85
   [−26; +30]). El valor de Majkel actual está en la adaptación, no la secuencia.

### (anteriores)

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
