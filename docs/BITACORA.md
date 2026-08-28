# Bitácora de experimentos

## 2026-08-28 — Evolución 5 (panel del meta): v4 retiene; nace mimada_xl y la tensión dinero-vs-winrate

**Setup:** panel des-endogamizado [mimada_v4 + clon de "ln"], techos altos, mecánicas de ejecución como genes. 4,590 episodios.

**Resultado:** `mimada_v4` retiene el título (53/54 en la final). Pero el subcampeón **`mimada_xl` (m8m_08)** es la v4 escalada — 12 animales (6+6), 3er cuadrante, 9 peones, `multi_feeder` — y fue **el mejor del campo en dinero medio ($64.2k vs $56.6k de v4)** pese a perder el cara-a-cara.

**Hallazgos:**
1. **`multi_feeder` adoptado por 8/9 finalistas evolucionados** — la mecánica desbloqueó rebaños de 12 sin escapes. La frontera de escala se movió.
2. `phased` = False en todos: la fase de capital solo importa en builds extremos (rescató al clon), no a escala moderada.
3. **Tensión dinero-vs-winrate**: contra el gemelo v4, el volumen de XL estrella los mercados compartidos (leche/lana) y pierde por poco; contra oponentes *distintos* produce más. El ladder ES diverso → el dinero medio contra panel variado puede predecir mejor el Elo que el head-to-head contra nuestro propio campeón. Candidata seria a submission junto a v4.
4. El clon sigue débil ($18.7k, 0 pts) — sparring direccional, no benchmark.

**Pendiente decisión del usuario:** subir v4 + xl al ladder (reemplazarían a v1/v2; v2 iba en 641.8).

## 2026-08-27 (2) — Inteligencia del meta: perfil de rivales y el experimento del clon

**Estado del ladder:** mimada v2 = 641.8 (+42, subiendo); v1 = 601.5. Top 1 global: 3,097.

**Método:** el MCP sigue sin auth del lado cliente; ruta alternativa — como toda submission nueva arranca en 600, los bots fuertes pasan por nuestra banda. Bajamos 14 replays propios, perfilamos cada rival (`perfilar_rivales.py`) y cruzamos contra el leaderboard completo.

**Perfil del meta (6 rivales más fuertes, composición día 25):**
- **Fresas a escala en 5 de 6** (19–42 tiles) — el cultivo del meta: 3 tipos de tienda las demandan, el déficit sostiene el precio premium.
- Wheat como columna vertebral (16–41 tiles): alimenta rebaños grandes Y vende a prueba de gluts.
- Rebaños de 11–15 animales; **3 cuadrantes** comprados día 7–13; ocio 2–6% en los mejores.
- El tiburón: **"ln" (rank 862, score 1794) nos ganó con $161.7k** — 41 wheat + 19 fresas + 11 vacas + 4 ovejas, tierra día 7, 5% ocio. 3× nuestro nivel.

**Experimento del clon — el hallazgo central:** LN_CLONE (la build de "ln" sobre NUESTRO chasis) pierde 16–0 contra mimada_v4 con **$13.0k** — la misma composición que al "ln" real le da $161.7k. Conclusión: **el foso del meta no es la receta, es la capacidad de ejecución**. Nuestro chasis se satura ~30 tiles activas + 8 animales (la vieja frontera de movimiento/ocio, ahora cuantificada como EL bloqueador); el de "ln" opera 75 tiles + 15 animales al 5% de ocio.

**Implicación:** más evolución de configs no cierra la brecha. Siguiente frente = mecánica de chasis que escale: logística de wheat para rebaños grandes, rutas de riego para 3 cuadrantes, bundling por tile. Luego evolución 5 con techos altos (crop_tiles 60, rebaños 15+) y clon mejorado en el panel. Nota metodológica: nuestra ecología de fitness es endogámica (evolucionamos contra gemelos); el panel necesita representantes del meta.

## 2026-08-27 — Evolución 4: la planificación adaptativa al mercado GANA (mimada_v4)

**Pregunta:** ¿capa adaptativa (score $/tile-día con espejo de la curva de precios + pipeline propio) o mix fijo evolucionado? 4,590 episodios, 10 generaciones, adaptativo y fijo compitiendo en igualdad (mutación podía encender/apagar `adaptive`).

**Contexto:** la v3 adaptativa a mano perdió 5–25 y luego 10–20 vs v2 (dos fixes: wheat_floor = demanda interna del rebaño; pricing marginal con factor de oponente). El ajuste manual se detuvo ahí y las perillas fueron a evolución.

**Veredicto: `mimada_v4` (k8m_22, adaptativa) — final 52/54, confirmación 50–0 vs mimada_v2 en seeds vírgenes ($59.4k vs $56.0k).** La evolución corrigió mi calibración: `mkt_opp_factor=1` (mi 2 sobre-amortiguaba el melón) y `wheat_floor` auto (= rebaño, 8). La carrera fue reñida (gens 3–7 lideraron configs fijas; la 8 la volteó), pero final y confirmación fueron inapelables. Autopsia v4: la más limpia hasta hoy (1 planta muerta, $50 decay); frontera intacta: 63% movimiento, 13% PASS.

**Sin submission** (decisión del usuario: mejoras locales primero). `mimada_v4` transcrita VERBATIM a arquetipos.py y verificada (10–0 vs v2, mismos números que la confirmación). Lista para subir cuando el usuario dé el go.

## 2026-08-26 (2) — Análisis de replays reales → mimada v2 al ladder

**Diagnóstico del ladder (rating 599 tras ~18 episodios; 3 replays analizados con `analizar_replay.py`):**
1. Ocio confirmado: 32–36 turnos TODO-PASS/partida sin órdenes de mercado (rival top: 1); 8–10% unidades-PASS vs 2–3% de rivales.
2. Weeds tras comprar NE (día 9): 2→6→12–15 al día 20–25; casi todos espontáneos sin DIG (prio 8), no plantas muertas (3–5).
3. Fuga de cierre: **$10–16k sin vender al step 719** (producto en animales + plantas maduras + inventarios de unidades). Rivales: ~$0. Causas: `animal_harvest_at=4` acumula y el auto-drop del día 29 llega sin turnos de venta restantes.
4. Causa raíz: granja ESTÁTICA (plan fijo completo al día 10, banco sin reinvertir) vs meta que escala (9–13 vacas, 20–30 fresas, 3er cuadrante, $78–106k).

**Lección doble de método:**
- Los 5 fixes "obvios" juntos (grow, endgame, dig30, plant_near, land3) perdieron **0–30** vs v1. La ablación individual (16 eps c/u) los separó: `plant_near` 16/16 ($58.8k) y `endgame` 16/16 ($52.6k) ganan; `dig30` neutro (8/16); `land3` 1/16 y `grow` 0/16 **venenos** (el grow melón-primero estrella su propio precio y drena capital animal).
- Incidente ops: la primera ablación se lanzó sin `if __name__ == "__main__"` → tormenta de spawns de multiprocessing en macOS, 4.9 GB de tracebacks. Guard SIEMPRE.

**mimada v2** = mimada + `plant_near` + `endgame`: **30–0 vs v1** ($58.1k vs $49.2k) en seeds frescos; self-play $74k (vs $46k de v1). Enviada como segunda submission (quedan 3 hoy). Pendiente: mecanismo de escalado inteligente (el meta lo exige, el grow ingenuo no sirve) — candidato para evolución 4 con el chasis v2.

## 2026-08-26 — PRIMERA SUBMISSION REAL 🚀

Submission **55782540**: `submission/main.py` (mimada v1, campeón de la evolución 3, ~21k episodios de búsqueda local). Auth por `kaggle auth login` (OAuth); el usuario ya estaba inscrito. Estado inicial: PENDING (episodio de validación self-play en servidores de Kaggle). Quedan 4 submissions del cupo diario. Monitoreo: `kaggle competitions submissions kaggriculture` y `kaggle competitions episodes 55782540`.

## 2026-08-19 — Empaquetado de submission + bug del orden de dict como ADN estratégico

**Verificación del MCP de Kaggle:** endpoints públicos OK (metadatos: 6,367 equipos, 5 subs/día, deadline 2026-09-30; páginas completas). Endpoints autenticados (leaderboard, submit, episodios) devuelven `Unauthenticated`: el usuario debe conectar el connector de Kaggle en el cliente, o generar token de API para el CLI (`kaggle` 2.2.4 ya instalado en el venv). Falta también aceptar las reglas ("Join Competition") en la web.

**Submission empaquetada:** `empaquetar.py` genera `submission/main.py` autocontenido (chasis inline + config campeona). Validación self-play 720 turnos OK.

**Bug descubierto por la disciplina del espejo:** main.py vs módulo `mimada` dio 8–0 — imposible para agentes idénticos (espejo fuerza empate). Causa raíz: **el orden de inserción del dict `plants` es parte de la estrategia** (el chasis compra semillas y planta iterando `plants.items()`), y había dos transformaciones silenciosas: (1) al transcribir h7m_10/g11m_11 a `arquetipos.py` se reordenó el dict, debilitando a los campeones; (2) `pprint` alfabetizaba al empaquetar — deshaciendo por accidente el error (1). Corregido: transcripciones en el orden alfabético original de los mutantes + `sort_dicts=False`. Verificación: 0/719 decisiones distintas, espejo 3–3 con dinero idéntico al centavo.

**Implicaciones:** (a) el orden de plantas es una dimensión de búsqueda NO explorada — y hay un confound conocido: `sample()` genera orden WHEAT-primero y `mutate()` alfabetiza vía normalize; (b) toda transcripción de configs debe ser byte-fiel; el espejo del harness es el detector.

## 2026-08-18 — Evolución 3 (policy search): nuevo campeón `mimada`; la zonificación PIERDE

**Setup:** `evolucion3.py` — el cerebro como perillas: 9 prioridades del scheduler + zonificación + peones hasta 10, buscados junto con la config de granja. 14 generaciones × 40, registro anti-repetición con las 530 firmas de gens 1–2. 6,990 episodios, 27 min.

**Nuevo campeón: `mimada` (h7m_10):** 8 peones, 4 vacas + 4 ovejas, 9 melones + 3 fresas + 9 wheat, `prio_care=70`, `animal_harvest_at=4`, sin zonificación. Final 45/54; **confirmación seeds vírgenes 50–0 vs ocho_manos ($59.4k vs $49.9k)**. Tercer destronamiento consecutivo; el excampeón volvió a sacar 0 pts.

**Hallazgos de política (lo importante):**
1. **La zonificación PIERDE — rechazo unánime**: los 9 finalistas tienen `zoning: false`, pese a semillas dirigidas y 50% de inmigrantes con zoning. La implementación (bloques contiguos estáticos + escalamiento por umbral) no supera al greedy. Resultado negativo valioso: un mecanismo plausible, muerto por evidencia antes de complicar el código.
2. **La urgencia horaria también pierde**: `prio_urgency 0` en 8/9 finalistas — el bump de pánico a las 16h distorsionaba el orden y quitaba valor.
3. **CARE con prioridad alta gana** (70 vs 46 default) y los rebaños mixtos crecen (4+4 a 7+5).
4. `animal_harvest_at`: señal mixta (campeón usa 4 = acumular; otros 1–2).

**Meseta y frontera:** el espacio config+perillas se aplanó (~$55–60k de fitness). El desperdicio restante del campeón: 3,771 acciones de movimiento, 10% PASS, fertilizer sin recoger $5.9k. Próximos avances = mecanismos nuevos en el chasis, p.ej. *bundling por tile* (terminar todas las tareas de la tile donde estás parado antes de moverte; recoger fertilizer en el mismo viaje del FEED).

**Nota:** con 3 rondas de evolución encima, `mimada` es candidata razonable a primera submission real a Kaggle (empaquetar chasis+config en main.py).

## 2026-08-17 — Evolución 2: 14 generaciones, 6,990 episodios, nuevo campeón `ocho_manos`

**Setup:** `evolucion2.py` — 14 generaciones × 40 configs (6 élites + 22 mutantes + 12 inmigrantes), registro de firmas anti-repetición (incluida gen 1), seeds rotativos por generación, panel coevolutivo. Perillas nuevas: `animal_harvest_at`, `premium_hold_day`. 33 minutos de cómputo.

**Nuevo campeón: `ocho_manos` (mutante g11m_11):** 8 peones, 4 vacas + 2 ovejas, 12 melones + 3 fresas + 9 wheat, fert_prio 45, cosecha animal inmediata, NE comprado. Final: 43/54. **Confirmación seeds vírgenes: 50–0 vs vacas_melon ($53.4k vs $34.6k).** El excampeón sacó **0.0 puntos** en la final — una ronda de evolución dirigida lo demolió.

**Convergencias del top 9 (todas las líneas ganadoras comparten):**
1. **7–8 peones** (el máximo muestreado — la evolución chocó contra nuestro propio techo; probar hands>8).
2. **Rebaño mixto vacas+ovejas** — diversifica ventas entre las curvas de leche y lana en vez de estrellar una sola.
3. **Melón pesado (9–12 tiles)** + `fert_prio 45` unánime + `animal_harvest_at 1` (7/9 — no acumular, evita pérdidas por cap).
4. `premium_hold_day 8` frecuente pero señal débil (el hold expira antes de que casi exista producción premium); holds largos (20) rankean peor — **aguantar inventario es veneno**.

**Autopsia del campeón:** limpia en muertes/decay, pero: 63% de acciones siguen siendo movimiento, 12% PASS (9 unidades se quedan sin tareas), 8 producciones capadas ($1,280) — parte inherente a la rampa de CARE (una vaca colocada d0 banca 7 noches pero el cap 6 solo paga 5+1: **cuidar solo 5 de las 7 noches de rampa** es micro-optimización pendiente del planner real).

**Decisiones:** `ocho_manos` promovido a referencia. Fronteras claras para el planner v1: zonificación (movimiento), asignación con 9 unidades (idle), care-ramp exacto, hands>8.

## 2026-08-17 — Evolución gen 1: búsqueda en masa sobre el espacio de estrategias

**Setup:** `evolucion.py` — 48 configs (42 aleatorias + 6 dirigidas), criba de 288 episodios vs campeón (fitness = dinero propio, espejado), final round-robin de 224 episodios (top 6 + campeón + gansos). Luego confirmación del ganador en 50 episodios con seeds vírgenes (4000–4024).

**Nuevo campeón: `vacas_melon` (ex g1_02, config encontrada por muestreo aleatorio):**
5 vacas + 8 melones + 3 fresas + 5 wheat, 4 peones, care, fertilizer prio 45, compra NE.
Final: 49/56 episodios ganados, $46.9k medio. **Confirmación en seeds vírgenes: 50–0 vs ovejas_vacas ($49.4k vs $33.5k, IC95 [93%, 100%]).** sd alta ($12.6k) — sensible al sorteo de tiendas.

**Patrones del top 10:**
1. **Vacas > ovejas al escalar.** Todo el podio es vacas-pesado (5–6 vacas). La lana se estrella en cuadrático pasado T=105; la leche degrada lineal — las vacas soportan rebaños de 5–6, las ovejas saturan en ~3.
2. **`fert_prio` 45–60 en los 10 primeros.** `campeon_fert60` (idéntico al excampeón + disciplina de fertilizer) le ganó 6/6 — el hallazgo de la autopsia valía miles.
3. **Premium crops en dosis** (8 melones + 3 fresas) complementan a los animales.
4. Los gansos colapsan en campo fuerte (1/56 en la final).

**Decisiones:** `vacas_melon` promovido a `bots/arquetipos.py` como referencia a batir. Pendiente: gen 2 mutando ganadores; mejoras de chasis (zonificación — sigue habiendo ~2,450 acciones de movimiento por partida) que ninguna config puede alcanzar.

## 2026-08-17 — Torneo 001: arquetipos

**Setup:** round-robin de 5 agentes, 12 seeds con espejo por par (24 episodios/par, 240 total), motor 1.32.7. Bots sobre el chasis compartido (`bots/chassis.py`). Autopsias de desperdicio con 3 seeds vs starter.

**Tabla de liga** (máx 4.0):

| # | Agente | Pts | Dinero final medio | Nota |
|---|---|---|---|---|
| 1 | ovejas_vacas (3 sheep + 3 cow + care) | 4.00 | $40,594 | ganó los 96 episodios que jugó |
| 2 | gansos (6 geese + care) | 2.88 | $22,321 | |
| 3 | control (solo cultivos) | 1.83 | $11,655 | |
| 4 | writeup (4 sheep + 8 cows + fresas) | 1.29 | $10,230 | sobre-extendido bajo este chasis |
| 5 | starter | 0.00 | $3,538 | |

**Autopsia — desperdicio medio por episodio:**

- **Fertilizer no recogido: 111–128 unidades (~$11–13k nominal) en TODOS los arquetipos animales.** La prioridad 18 nunca gana; casi nadie recolecta. Mayor línea de desperdicio del torneo.
- **Movimiento domina la economía de acciones**: ~65–75% de las acciones de unidad son pasos de traslado (p.ej. control: 1,474 movimientos vs 532 productivas). Zonificar unidades y agrupar tareas es la mayor palanca de eficiencia.
- **Decay por cosecha tardía**: 21–61 unidades/episodio ($545–1,707). El scheduler necesita prioridad de cosecha consciente del deadline.
- **writeup se mata solo**: 7.3 animales escapados/episodio ($3,333) + 24 plantas muertas — 12 animales exceden la logística de wheat y acciones de 5 unidades. *Caveat: esto condena la ejecución de mi chasis, no necesariamente la estrategia del writeup.*
- ovejas_vacas pierde 1 animal/episodio ($500): la logística de feed tiene una fuga menor.
- Inventario sin vender al final: $0 en todos ✓ (la política de venta funciona).

**Decisiones:**
1. El núcleo económico del agente real: ovejas/vacas con care diario. Gansos como candidato secundario.
2. Cambios de estrategia sugeridos por el desperdicio: recolección de fertilizer como línea de ingreso de primera clase; zonificación de unidades para reducir movimiento; cosecha deadline-aware; no plantar más de lo que se puede regar.
3. Pendiente: probar un arquetipo "ovejas_vacas + recolección disciplinada de fertilizer" para medir el delta real (el $11k nominal se degrada con la curva del fertilizer al venderlo).

## 2026-08-28 (2) — v4 y XL al ladder

Submissions **55803139** (mimada v4, adaptativa) y **55803144** (mimada xl, 12 animales + multi_feeder) enviadas y en validación. Pasan a ser las 2 activas (reemplazan a v1/601.5 y v2/618.8 en matchmaking). Experimento en vivo: ¿predice mejor el Elo el head-to-head (v4) o el dinero medio contra campo diverso (XL)? Revisión: mañana — ratings, episodios, y replays de derrotas para la siguiente iteración.

## 2026-08-29 — Evolución 6 vs la cinta: NADIE le gana con configs — el veredicto de 6 evoluciones

**Setup:** cinta de 2913 (sparring_v16) anclada en el panel; 4,392 episodios; registro acumulado 1,642+ firmas.

**Resultado: 0/8 contra la cinta para TODOS los finalistas** (incluida mimada_v4 y todo lo evolucionado). La cinta hace $110–126k contra nosotros; nuestro mejor evolucionado (n9e_4: 3C+5S, wheat 13, fert_prio 75) llega a $59.2k — +$1.8k sobre v4, ruido. **Seis evoluciones y ~1,650 configs únicas prueban que el espacio config/perillas está agotado en ~$55–60k.**

**La brecha es 100% capa de ejecución**: la autopsia del mejor es limpísima en desperdicio ($80 en plantas muertas) pero estructuralmente igual: 3,274 acciones de movimiento + 908 PASS (16%) vs 1,528 productivas. La cinta ejecuta un schedule optimizado offline con rutas ~perfectas.

**Bifurcación estratégica (decisión pendiente):**
- **A. Schedule híbrido**: optimizar offline un plan diario propio (estructura de olas de wheat, fases 8C/4S) y que el chasis lo ejecute con reparación adaptativa — cinta sin fragilidad de cinta.
- **B. Reescritura de ejecución**: rutas diarias por unidad (eliminar el 60% de movimiento y el 16% de ocio). El camino real al top; ingeniería dura.
- **C. Contra-cinta**: conocemos el _ACTIONS exacto de la familia de cintas dominante — pre-inundar sus ventas premium programadas (vender 1 turno antes de sus dumps de MILK/WOOL/STRAWBERRY/MELON) recorta su economía en el mercado lockstep. Exploit específico contra la población real del ladder; neutral vs bots adaptativos.

## 2026-08-30 — Opción B fase 1: el ROUTER — nuevo campeón mimada_v5r

**Implementado en el chasis (gateado `router=True`):** plan de jornada al alba (el día es la unidad natural: reset total + trabajo conocido) — tiles con servicio ordenadas en serpentina espacial, partidas en rutas de costo balanceado (una por unidad, animales primero por cercanía al shed), ejecución con **bundling por tile** (todo lo pendiente en una visita: feed+care+harvest+collect) y reparación en vivo (weeds → DIG y sigue; sin wheat → desvío al shed y retoma). Supresión de tareas ya ruteadas en el greedy (que sigue manejando plantado/build/place). `hire_late`: peones también días 28-29. `_service_ops()` como fuente única de "qué le falta a esta tile".

**Resultados fase 1:**
- Firma estructural (mismo seed vs starter): movimiento **3,355 → 2,156 (−36%)**, productivas 1,567 → 1,698, dinero $98.5k → $104.3k. El ocio SUBIÓ a 35%: el router liberó ~2,000 turnos-unidad que la granja actual no usa — capacidad creada, pendiente de gastar.
- **v5r vs v4: 24–0 ($66.4k vs $61.5k)** — upgrade limpio por pura ejecución. Nuevo campeón.
- Mi expansión a mano (v5rxl) perdió 8–16 — enésima vez: los tamaños los encuentra la búsqueda.
- vs la cinta: 0/16 aún ($48–66k vs $116k) — fase 1 sola no cierra el 2×.

**Lanzada evolución 7**: redimensionar la granja sobre el motor nuevo (router forzado en todos los candidatos, panel = cinta + v5r).

## 2026-08-30 (2) — Evolución 7: la granja redimensionada — rutera vs v5r, la tensión en su forma pura

**Resultado:** el router subió el techo de toda la población (fitness $55-60k → $70-77k). Campeona de fitness: **`rutera`** (r4e_1: crop_tiles 30, fresas 5, 3er cuadrante, 7 peones) — **$80.6k bajo presión de mercado de la cinta** (v5r: $63.2k ahí) y **$100.2k vs oponente débil — primer 6 cifras del proyecto, el nivel absoluto de las finales del título** ($102-103k). Ocio reabsorbido: 35% → 22%; productivas 1,698 → 2,006. Brecha vs la cinta: de 2.2× a **1.5×** (aún 0/8).

**Pero:** rutera pierde **0–20 el cara-a-cara vs v5r** (¡y 12–0 le gana a v4!). La tensión dinero-vs-winrate en su forma más pura: dos criterios de selección, dos campeonas — v5r (duelo) y rutera (economía). El experimento v4/XL del ladder va 657 vs 647 (leve ventaja al criterio duelo, no concluyente).

**Fugas restantes del campeón:** riegos de ventana perdidos $1,252 (timing de ruta vs ventana de bonus) y producción capada $1,040 — objetivos de la fase 2 del router. Propuesta pendiente: subir v5r + rutera al ladder (ambas > v4/XL) y que el Elo real arbitre el criterio.

## 2026-08-30 (3) — v5r y rutera al ladder

Submissions **55807774** (mimada v5r, criterio duelo: 24-0 vs v4, 20-0 vs rutera) y **55807779** (rutera, criterio economía: $80.6k bajo mercado de la cinta, $100k absoluto). Reemplazan a v4 (657.3 final) y XL (657.1 final — cerró empatada con v4: el experimento anterior terminó sin veredicto claro). Ronda 2 del experimento dinero-vs-winrate, con especímenes del motor router. Revisión: mañana.

## 2026-08-31 — Análisis matinal de v5r y rutera en el ladder: el estancamiento explicado

**Ratings:** v5r 683.4, rutera 676.5 (par anterior: 657) — pico de ~800 no sostenido. Ronda 2 del experimento de criterios: de nuevo casi empate, leve ventaja duelo.

**Ejecución en producción (12 replays): LIMPIA.** 0-2 plantas muertas, weeds ~0-4, sobrante final $200-900 (antes $10-16k), 80-104 unidades vendidas en el cierre. El router funciona en el mundo real.

**El estancamiento, cuantificado:** corremos al **34-35% de ocio** (~2,050 turnos-unidad tirados) con granjas de ~30 tiles en 2 cuadrantes, mientras los que nos ganan trabajan 40-50 tiles: perdemos contra el lote de $100-120k (Dhruv 119.8k, Tarun 120.7k, Somasundar 114.3k — descendientes de cinta y titanes de fresa subiendo por nuestra banda) y le ganamos al lote de <$80k. Además 3 derrotas por <$3k de margen (cy zhang -$0.8k, Chris Kang -$0.7k). Nota: rutera vs Dhruv corrió a 20% de ocio y $86.4k — el budget mayor usa más capacidad y gana más; ambas quedaron cortas para el meta real (evolución 7 optimizó contra la cinta en espejo, no contra la diversidad del ladder).

**Fase 2 propuesta:** (a) mecanismo de FERTILIZE en cultivos — no existe en el chasis; en fresas duplica los ticks (4→8 × $120+) y tenemos fertilizer gratis de los animales — sospechoso principal de los $100k+ del meta; (b) granja más grande + trigger de 3er cuadrante por capacidad planeada (no por tiles vacías); (c) evolución 8 para redimensionar con los mecanismos nuevos.

## 2026-08-31 (2) — Auditoría de las observaciones del usuario: las 3 confirmadas; la #3 es la fuga mayor

Sobre 12 replays reales (auditor_puntos.py):
1. **Ocio con trabajo disponible: 1,351 turnos-unidad/partida** (84% del idle total) — unidades quietas con ≥3 tiles vacías Y dinero/semillas. Causa: el budget de crop_tiles capa el plantado; las rutas terminan y no se genera trabajo. Staffing plano (7-8 peones desde el día 1 en 25 tiles) vs elite 4/cuadrante escalando (4→8→12) — sobrecapacidad temprana confirmada.
2. **Tierra: NE día 8** (elite: día 6) y **medio vacía por días**: v5r la usa 9/25 tiles en los días 9-14; rutera 14-16/25. Nadie compra el 3ro. "Días y días sin usar el terreno" — confirmado literal.
3. **VENTAS A MERCADO ESTRELLADO: $14,003/partida en promedio** (86 unidades vendidas a ≤30% del precio base; peor caso $29,862/179u). La política "vender todo, cada turno" desploma los premium (lana/leche a $1-60) y seguimos vendiendo al piso. La fuga de cierre real a precio base es $1,080 (no $900 — el metric anterior valoraba a precio final estrellado, sesgo confirmado). El nuevo leak descubierto es ~13x el de cierre.
4. Pregunta tiendas: el consumo del town SÍ mueve precios (S7.1, drena inventario = compra) y el scorer adaptativo lo ve REACTIVAMENTE (usa inventario actual); NO pronosticamos el drenaje futuro de unlocked_shops (el chasis nunca lee obs["town"]). Gap identificado.

**Plan fase 2 re-priorizado:** (1) guardia de piso en ventas premium (no vender bajo X% del base salvo cierre/shed lleno) + pacing; (2) trabajo infinito: budget dinámico por capacidad + fallback "si ocioso y hay tile+semilla, planta" + staffing por cuadrante + tierra por capacidad planeada; (3) FERTILIZE en cultivos; (4) forecast de demanda del town en el scorer; (5) evolución 8.

## 2026-08-31 (3) — Ablación fase 2: el paquete gana por INTERACCIONES

128 eps, doble lente [duelo v5r + mercado cinta], base rutera ($67.5k):
- **todo_junto: $78,760 (+$11.3k)** — mejor que la suma de sus partes.
- Solos: land_early +$3.5k y town_forecast +$3.5k (héroes); fert +$0.5k, floor -$0.2k, idle_plant -$1.3k (neutros solos); **hpq4 -$7.1k (veneno aislado)** — 4 peones en 1 cuadrante ahoga la apertura… pero CON land_early el 2º cuadrante llega el día ~5 y el staffing escala a tiempo, y idle_plant/fert/forecast llenan la tierra nueva. Lección de libro: los efectos no son aditivos; la ablación da la ciencia, la combinación la da la búsqueda.
- Lanzada evolución 8: flags fase 2 + perillas (piso %, hpq, fert_crops) como genes; panel cinta + todo_junto.

## 2026-08-31 (4) — Evolución 8: el paquete completo corona — nace INTEGRAL

**Resultado:** la evolución (4,400 eps, 2,259 firmas previas respetadas) no encontró nada mejor que el paquete sembrado: **`integral`** = rutera + los 6 mecanismos con floor=0.4, hpq=4, fert=[fresa,tomate], land_early, forecast. Las perillas de la ablación ya eran las correctas (floor 0.4 y hpq 4 en el mejor de TODAS las generaciones).

**Números histórico:** $85.1k bajo mercado de la cinta (v5r: $54.9k, +55%); **$119.4k absoluto — récord del proyecto, por encima del nivel élite de las finales del título ($102-103k)**; ocio 8%; ventas a piso aplastadas: $14k → $450. Confirmación en seeds vírgenes: **20-0 vs v5r ($82.7k vs $66.1k)** — primera vez que un bot gana AMBOS criterios (duelo + economía). Aún 0/8 vs la cinta (1.54×).

**Nueva fuga creada por la expansión:** 32.5 plantas muertas/partida ($4.4k) — el idle_plant+land_early planta más de lo que se riega en los picos; objetivo de la fase 3 junto con riegos de ventana ($2.1k). Pendiente: go del usuario para subir integral al ladder.

## 2026-08-31 (5) — INTEGRAL al ladder 🚀

Submission **55823421** (integral). Activas: rutera (667.0) + integral; v5r sale (670.1 final). Meta inmediata: romper la banda de 800 con los $119k de economía. Fase 3 en el banquillo: plantas muertas por sobre-expansión ($4.4k), riegos de ventana ($2.1k), contra-cinta.

## 2026-09-01 — Análisis de sistema de integral (29 eps, ~700 estable) + apuntes del usuario

10 replays (6G-4P, $84.1k medio vs $73.8k rival), agregado con analizar_integral.py:
1. **Día 0-1 SÍ se planta** (16 wheat + ~1 melón medio) — lo que el usuario vio fue el ramp del melón (semillas de a 6/turno). No sistémico.
2. **Peón 1: BUG REAL encontrado** — PLACE se asignaba al peón más cercano aunque no cargara el animal → 4-7 intentos fallidos en silencio por partida (traza: PLACE COW x4 + x3). Arreglado: elegibilidad como FEED (solo el portador). El vagabundeo W-E-E restante es churn de asignación greedy temprana (menor).
3. **MELÓN — cuello confirmado con matiz:** picos de 24-52 tiles, 162u/partida vendidas a $141 realizado (base $250; en derrotas $101-114). El scorer valoraba al precio MARGINAL una cosecha que se vende en RÁFAGA sobre curva sq. 8.6 semillas de melón muertas al día 25. 3 de 4 derrotas tienen pico ≥44 tiles. Fix: `scorer_v2` — precio medio de ráfaga (integral discreta) + yields fert-aware (fresa/tomate u_eff=7).
4. **Fresa:** 108.5u a $231 realizado (¡vs $120 base!) — no tan poca como parecía, pero varianza 34-173u: cuando el melón come tiles, la fresa paga el pato. scorer_v2 debería resolver.
5. **LANA — el durmiente:** 108u a $210 realizado, precio diario ≥$206 en 8/10 partidas = escasez sostenida NO explotada con solo 4 ovejas. La evolución la mantuvo baja por el panel-espejo con la cinta (que también vende lana) — otro artefacto de endogamia. Variantes sheep6/sheep8 en ablación vs panel diverso.
MILK es el rubro #1 silencioso: $25.4k/partida a $179.
Ablación fase 3 corriendo: fixplace (regresión), scorer_v2, sheep6/8, v2+sheep6.

## 2026-09-01 (2) — Ablación fase 3, doble panel: integral RESISTE; disciplina anti-sobreajuste aplicada a nuestras propias ideas

Panel espejo [integral+cinta]: sheep6 +$0.5k (ruido), scorer_v2 -$0.3k, sheep8 -$12.1k (veneno). Sospecha de ceguera del panel (ambos rivales inundan lana/melón) → re-test en panel diverso [clon_ln + control]: **integral $113.5k > sheep6 $107.6k > scorer_v2 $105.9k > combo $105.3k**. Dos paneles independientes coinciden: rechazar sheep6/8 y scorer_v2 (queda gateado apagado — el sell_floor ya domestica la cola del crash: melón realizado $141, no los $13 de los bots pre-floor que vio el usuario). El fix de PLACE-al-portador (bug puro) se queda. Conclusión de método: las intuiciones "obvias" — incluidas las nuestras — mueren o viven por la evidencia; integral+fixplace es la candidata (la 55823421 desplegada NO trae el fix).

## 2026-09-01 (3) — El usuario tenía razón sobre el melón: mi promedio escondía el dump, y la guardia tiene una válvula traidora

Línea de tiempo de ventas de melón en 5 replays de integral — patrón idéntico en TODOS: d12 ~6u a $221-241, d17-19 ola grande (56-78u a $178-236 que desploma), **d20-21 segunda ola: 48-91u a $4-$73 — bajo el piso de $100**. Contra David Nana: 91u a $16 (la escena exacta del usuario). Causa: la guardia de piso se desactiva cuando shed ≥85 (válvula anti-overflow), y la segunda ola de cosecha (~90 melones en 2 días) llena el shed justo entonces → dump forzado. El promedio $141 que reporté era aritméticamente cierto y analíticamente engañoso — lección: los reclamos distribucionales se verifican con distribuciones, no con medias.

**Física del melón:** sin drenaje del town (ninguna tienda lo compra) el precio no se recupera; el ingreso total ≈ integral de la curva sobre las unidades TOTALES → la palanca es cantidad, no timing. Sobreplantamos ~2x (144-312u vs ~120 óptimas).

**Fixes gateados:** `melon_max` (cap de tiles concurrentes → acota ola y total de temporada; al tope elige el 2º mejor cultivo) + pacing de venta (≤12/orden) + `smart_overflow` (con shed lleno alivia con lo barato; el premium aguanta hasta 95). Ablación doble-panel corriendo.

## 2026-09-01 (4) — Ablación del melón: lo feo no siempre es fuga

Doble panel: espejo — integral base gana ($77.8k), fixes de melón levemente negativos; diverso — todos empatados en ruido ($116.5-119.5k, melon14_ovf +$2.9k dentro del error). **Conclusión: los dumps a $16 son horribles a la vista pero económicamente neutros** — la física del melón (sin drenaje del town, ingreso ≈ integral de la curva sobre cantidad total) significa que el dinero ya se capturó en la bajada; las unidades a $16 son la cola planificada de esa integral, y el scorer ya tenía ~igualados los retornos marginales entre cultivos (eficiencia interna accidental). El bug de la válvula era real; su costo, ~cero. Lección bidireccional: ni mi promedio veía el patrón, ni el patrón era la fuga que parecía. Fixes quedan gateados y apagados. Ship: integral con fix de PLACE (bug real de turnos).

## 2026-09-02 — Notebook "strong-barnyard-economist": doctrina de 4 capas y el anuncio fechado del melón

**Arquitectura del bot** (cinta-más-parches, más evolucionada que V16): A ruta completa de temporada (la economía), B reparación local de weeds, C **ordenamiento de SELLs propios por daño de cotización modelado + demanda viva del town** (la posición en la cola ≤10 importa en el lockstep), D **preempción anti-clon multi-horizonte 3→2→1 turnos con repago exacto de cantidad** (generalización del front-run de V16). Principios: blast radius acotado, cada capa apagable/atribuible ("design for the ablation you will want later" — validación externa de nuestro método), evaluar multi-seed y ambos asientos.

**Benchmark:** barnyard 12-0 vs integral ($95.8k vs $59.7k); 0-8 vs cinta v16 ($82.0k vs $95.4k). Escalera local: integral < barnyard < v16. Segundo sparring de élite en bots/sparring_barnyard.py.

**La joya (conclusiones): "un bloque de melón plantado el día 0 es un ANUNCIO FECHADO de una venta el día 10 — y casi nadie lo lee".** La granja rival es pública con planted_day. Adoptables para nuestro bot cerrado:
1. `opp_pipeline`: reemplazar el mkt_opp_factor ciego por el pipeline OBSERVADO del rival (sus tiles × yields con fechas) en el scorer — encaja exacto en nuestra arquitectura.
2. `beat_wave`: vender el premium retenido ANTES de que madure la ola anunciada del rival.
3. Capa C: ranking de nuestra cola de ventas por fragilidad de curva + demanda del town (hoy es orden estático).

## 2026-09-02 — Revisión adversarial de los tres mecanismos: 5 bugs cazados antes de creerle a la ablación

Enjambre de 4 revisores + verificadores escépticos (34 agentes; 22 cortados por límite de sesión, 12 completos con repro ejecutado). **15 hallazgos, 2 de ellos verificaciones NEGATIVAS valiosas**: la tabla MKT nueva (EGG/MILK/WOOL/FERTILIZER) coincide exactamente con el motor v1.32.7 ✓, y con los 3 flags apagados el comportamiento es idéntico al previo ✓ (confirmado luego con regresión: $114,638 al centavo).

**Bugs confirmados y corregidos (todos con repro):**
1. *(crítico)* **beat_wave expiraba ANTES del dump**: la ventana `0<=to_peak<=2` se apagaba el día del pico, justo cuando el rival cosecha y vende. Fix: sin piso — una tile madura sigue en el tablero hasta que la cosechan.
2. **Detector degenerado**: la ventana cubre el 75% de la vida del carrot y el 60% del wheat → un rival en régimen estacionario encendía `wave_soon` el **46-54% de los turnos**, anulando el sell_floor de forma permanente y re-habilitando el dump de melón sin pacing (deshaciendo el fix de df5c6cc). Fix: agrupar por `planted_day` (bloque sincronizado = anuncio fechado) + umbral por VALOR entrante (≥$2,000), no por número de tiles.
3. **El hold premium hacía sombra a beat_wave**: su `continue` se evaluaba antes de los usos de `wave_soon` → el mecanismo quedaba anulado justo para MELON, el único premium al que aplica (pariente exacto del bug #2 histórico de la válvula). Fix: la ola perfora el hold.
4. **opp_incoming contaba oferta fantasma**: tiles ongoing con ticks ya producidos y cultivos plantados tan tarde que nunca rendirán. Fix: solo ticks restantes y solo lo que madura antes del cierre.
5. **sell_rank ordenaba por fragilidad UNITARIA**: la curva sq del melón es casi plana cerca de I0, así que el rubro más valioso quedaba fuera del cupo de la cola. Fix: daño TOTAL (unitario × volumen).
+ *(preexistente, gateado como `order_budget`)*: en el cierre, `sell_cap=8` + 6 HIRE > 10 órdenes → **4 HIREs descartados en silencio** los días 28-29.

**Ablación previa (con beat_wave roto), panel escalera [gemela+barnyard+cinta]:** opp_read $79.4k (7/18) > los_tres $79.1k > base $74.4k (3/18) > beat_wave $74.1k > sell_rank $74.0k (7/18). Explica el empate de beat_wave: estaba roto de tres formas. `sell_rank` con dinero neutro pero 7/18 victorias es la primera mecánica que sube win-rate sin subir economía (lo que el Elo premia). Re-ablación con todo corregido en curso.

## 2026-09-02 (2) — El experimento decisivo: el win-rate se DUPLICA con dinero constante

**Primero, la autocorrección:** el "+$5.0k de opp_read" de la primera ablación era RUIDO. La misma config base dio $74,410 con unos seeds y $81,609 con otros (±$7.2k sin cambiar una línea); opp_read dio $79,392 y $79,443. Con 18 episodios y sd $15-25k, el error estándar es ~$4-6k: nada por debajo de ~$10k es distinguible. Lección: n insuficiente produce conclusiones invertidas, y solo repetir con otros seeds lo revela.

**Lo que SÍ sobrevivió en ambas corridas fueron las victorias** (base 3/18 en las dos; variantes 4-7/18) → prueba decisiva por win-rate, 360 episodios, seeds vírgenes (2.0M), panel escalera [gemela + barnyard + cinta], 120 eps por variante:

| variante | win-rate | dinero |
|---|---|---|
| **opp_read + sell_rank + order_budget** | **33.3% ± 8.4%** | $71,799 |
| sell_rank solo | 28.3% ± 8.1% (+13.3 pts, 2.5σ) | $68,792 |
| base (INTEGRAL) | 15.0% ± 6.4% | $69,026 |

**+18.3 puntos, 3.4 sigma (p<0.001), con dinero estadísticamente idéntico.** La ganancia no viene de producir más sino de **convertir duelos cerrados**: defender la posición en la cola del lockstep gira los partidos que se deciden por márgenes finos (recordar: 3 derrotas del ladder por <$3k). El Elo paga victorias, no dinero — es la primera vez que optimizamos la métrica correcta directamente.

**Candidata registrada: `INTEGRAL_LECTOR`** (verbatim en arquetipos.py). Pendiente de autorización explícita del usuario para subir.

**Desglose por oponente (30 eps c/u, seeds 2.1M) — dónde vive la mejora:**

| oponente | base | INTEGRAL_LECTOR |
|---|---|---|
| gemela (INTEGRAL) | 43.3% (espejo ≈50%, ruido) | **73.3%** (2.9σ sobre el 50% esperado) |
| barnyard | 0/30 | 0/30 |
| cinta v16 | 0/30 | 2/30 (6.7%) |

**Lectura honesta:** el +18.3 pts global viene casi todo de ganarle a su propio predecesor, no de cerrar la brecha con la élite. Contra barnyard seguimos en cero. PERO eso es exactamente lo que mueve el Elo en NUESTRA banda (~680-700), donde los rivales son pares, no titanes: 73% contra el bot que hoy está en el ladder es subida real de rating. Dato fino: el lector no solo gana más, gana con más margen (18 duelos cerrados vs 30 de la base).
