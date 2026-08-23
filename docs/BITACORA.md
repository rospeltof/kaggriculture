# Bitácora de experimentos

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
