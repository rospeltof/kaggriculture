# Bitácora de experimentos

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
