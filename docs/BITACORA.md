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
