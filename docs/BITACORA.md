# Bitácora de experimentos

## 2026-09-05 (2) — Dos réplicas con potencia: la compra parcial y `harvest_76`, ambas a cero

Ambos bloques pre-registrados antes de correr, 16 semillas, 5.120 episodios cada
uno, con `noop` exacto y `_peor` (CAMPEONA_FB exacta) claramente negativo.

### Compra parcial (`seed_partial_batch`) — REFUTADA

| bloque | semillas | delta |
|---|---|---|
| descubrimiento | 4 | +5,00 |
| confirmación | 8 | +4,84 |
| **réplica** | **16** | **+0,23** |

Criterio pre-registrado (ambos análisis deben excluir cero): por semilla
IC95 [−6,20; +6,67], dos vías IC95 [−6,01; +6,48]. **Ambos incluyen cero.**

La bandera **dispara** (cambia acciones en 1.280/1.280 episodios) y el panel
**discrimina** (`_peor` a −26,95, t=−12,43). Resultado nulo real, no test nulo.

### `harvest_76` (adopción del 2026-09-03) — REFUTADA

Ablación leave-one-out: `sin_h76` = CAMPEONA_HOZ con `prio_harvest=62`.

| | delta | t | IC95 |
|---|---|---|---|
| `sin_h76` por semilla (n=16) | −0,08 | −0,29 | **[−0,65; +0,49]** |
| `sin_h76` dos vías (df=15) | −0,08 | −0,30 | [−0,63; +0,47] |

**No es inconcluso: el intervalo es ±0,5 y EXCLUYE el +2,5 atribuido.** Quitar el
mecanismo no cuesta nada. `sin_h76` cambia acciones en sólo **102/1.280
episodios** (8%): huella minúscula con poca varianza, que yo leí como efecto real
porque el t por celda daba 2,96.

### La lección de método, en dos partes

**1. La unidad de análisis.** El panel es un diseño **cruzado** (40 cintas × N
semillas, ambas dimensiones aleatorias). Tratar las celdas como independientes
infla el t. El estimador correcto es el de dos vías `V_cinta + V_semilla −
V_celda` con los gl del clúster menor. Recalculado: `harvest_76` pasa de +2,96
por celda a **+1,76** a dos vías, y la réplica confirma que no había nada.

**2. Ante un resultado fronterizo, la respuesta no es un estimador mejor: son
más datos.** El veredicto conservador del otro LLM sobre la compra parcial
("inconcluso, no adoptar", t=2,08) era el correcto. Yo apliqué el estimador a
dos vías —más apropiado para el diseño— obtuve t=2,52 y dije que pasaba. La
réplica dice +0,23. El estimador sigue siendo el bueno; usarlo **después de ver
el resultado** para cruzar la línea fue el error.

### CALIBRACIÓN DE LA ESCALERA (colateral, y muy útil)

`CAMPEONA_HOZ` = `CAMPEONA_GRANO` + `harvest_76`, y acabamos de medir que son
**idénticas en el 92% de los episodios** y separadas por −0,08 puntos de panel.
En la escalera: **`hoz` 818,1 contra `grano` 774,8**.

**43 puntos de Elo entre dos bots prácticamente iguales.** Diferencias de menos
de ~50 puntos entre nuestras propias submissions **no contienen información**.
Todas las lecturas comparando generaciones caben dentro de ese ruido.

### Estado del linaje

Con `harvest_76` a cero, **la única mejora que sostiene al campeón de septiembre
es `seed_stock_aware`** (+6,4 reportado). ⚠️ Sus datos crudos de confirmación
**se perdieron**: `results/panel40.json` fue sobrescrito por una corrida
posterior. No es verificable sin volver a medirlo. El `barrido.py` actual ya
impide sobrescribir, pero llega tarde para ese archivo.

---

## 2026-09-05 — Traspaso para revisión externa; envíos suspendidos

El usuario pidió reservar la única corrida que indica tener en Kaggle y
organizar hallazgos, errores e ideas para otro LLM. **No se envió ninguna
submission.** Se había preparado HOZ_LOTES y realizado un smoke de dos episodios
contra su propio módulo; no era el veto contra HOZ ni una confirmación de fuerza.
`submission/main.py` quedó restaurado byte por byte a su versión anterior.
La copia experimental permanece local e ignorada en `results/`.

**Error de nuestra verificación de empaquetado:** comparar directamente las
tuplas de la config Python con las listas del JSON produjo un falso desacuerdo.
Normalizar ambas mediante JSON, conservando el orden, confirmó igualdad. No era
un fallo del candidato y tampoco aporta evidencia de mejora.

Se prepararon `ESTADO_ACTUAL.md`, `AUDITORIA_LLM.md`, `IDEAS_Y_PRUEBAS.md`, un
método vigente único y un prompt de revisión. El método anterior se conserva en
`archivo/` como histórico. Los resultados de lotes se copiaron fuera de `results/`
a `evidencia/lotes_semillas/`, con hashes y fuentes congeladas. El generador
`preparar_contexto_llm.py` verifica registros existentes y reúne el contexto sin
red ni simulaciones. Este traspaso no autoriza nuevos barridos ni envíos y no
crea un commit. Ver [ESTADO_ACTUAL.md](ESTADO_ACTUAL.md).

---

## 2026-09-05 — Compra parcial de semillas y verificación de conducta

**Corrección del instrumento:** `sd=0` en W/L/T no demuestra que una bandera
no dispare. El `muerde.py` anterior comparaba dinero, no decisiones. Ambos
medidores guardan ahora huellas de acciones emitidas antes de entregarlas al
motor. El barrido además guarda episodios, configs y hashes; exige noop exacto
y rechaza errores. Los reclamos históricos de no ejecución basados sólo en
sd o dinero quedan limitados a esas métricas, salvo evidencia adicional de código.

**Incertidumbre:** reportamos también SE/t agrupados por semilla, ya que las
40 cintas comparten escenarios. Reanalizar `harvest_76` así conserva +2,5 puntos
pero cambia el t de confirmación de 2,96 a 1,60; no prueba regresión, sí menor
solidez que la atribuida. No se revierte el campeón por esta observación.

**Hipótesis aislada:** `seed_partial_batch=True` permite comprar parte del lote
adaptativo cuando la caja no alcanza para las seis semillas. Mantiene scorer,
piso de trigo, reserva y orden de compras. Apagado por defecto.

**Sonda 99000, primera cinta lad_, asiento 0:** primer melón d6 h16 → d1 h18,
primera fresa d8 h3 → d7 h19. La tile (2,1) que recibe melón temprano se ocupaba
con trigo en la base. 599 decisiones distintas; noop y chasis anterior exactos.
Ambos brazos ganan: prueba directa de conducta distinta con W/L/T idéntico.

**Descubrimiento, 101000–101003:** 1.280 episodios; base 62,1875%, candidato
67,1875%, delta +5,0 puntos, t por semilla 1,68, IC95 [−4,47; +14,47]. Noop
exacto; CAMPEONA_FB como control anterior −25,9375 puntos, t por semilla −15,07.
Pasa el cribado positivo predefinido, no constituye confirmación.

**Confirmación, 102000–102007:** 2.560 episodios válidos; base 60,0000%,
candidato 64,8438%, delta +4,8438 puntos. t por celda 2,45; t por semilla 2,08;
IC95 por semilla [−0,67; +10,36]. Noop exacto en 640/640 comparaciones; control
anterior −23,2813 puntos (IC95 [−31,45; −15,11]). El candidato mejora 62
resultados y empeora 31; cambia acciones en los 640 episodios.

**INCONCLUSO, NO ADOPTADO.** Se repite la señal, pero no supera el criterio
registrado (IC95 por semilla por encima de cero). No se rescata combinando
descubrimiento y confirmación ni cambiando al t por celda. El veto head-to-head
no correspondía sin confirmación. La bandera queda apagada. Coste: 3.840
episodios de panel, unos 25 minutos de pared con diez workers.

Protocolo, comandos y evidencia:
[EXPERIMENTO_LOTES_SEMILLAS.md](EXPERIMENTO_LOTES_SEMILLAS.md).

---

## 2026-09-04 (2) — La ventana d12-d16, localizada al detalle. Tres arreglos, tres fallos

### El sintoma, con precision

Deltas de banco diarios (24 partidas nuestras contra sus cintas | 12 replays suyos):

| dia | nuestro delta | tetsuya |
|---|---|---|
| 13 | **+4.918** | +2.952 |
| **14** | **+459** | **+10.204** |
| **15** | **+472** | **+7.350** |
| **16** | **−289** | **+5.948** |
| 17 | +12.296 | +5.904 |

**Zona muerta de tres dias.** Vendemos CERO melon hasta el dia 17 y entonces 48
de golpe; ellos venden 19/18/12 los dias 14/15/16.

### La causa: llegamos tarde a los cultivos de lead time largo

| cultivo | nosotros (total, dia medio) | tetsuya |
|---|---|---|
| **MELON** | 20.8 · **dia 7.8** | 13.1 · **dia 5.2** |
| **STRAWBERRY** | 41.2 · **dia 11.7** | 37.8 · **dia 7.5** |
| WHEAT | 77.6 · dia 12.4 | **148.3** · dia 19.2 |
| CARROT | 43.4 · dia 19.3 | 21.8 · dia 22.9 |

Melon 2.6 dias tarde, fresa 4.2. Ambos tienen `first=10`: cada dia de retraso al
plantar es un dia de retraso al cobrar, y **no se recupera** — de ahi que el
ratio se congele en 0.67 despues del dia 16.

### DESCARTADO 1: atasco logistico (shed / manos)

El shed NO se desborda (carga maxima 28 de 100). Y el melon en manos es **cero
hasta el dia 16**: no es que cosechemos y se atasque, es que **no cosechamos**.

### DESCARTADO 2: el scorer elige mal (`premium_first`)

Filtrar los candidatos a los cultivos con `first>=10` en los dias tempranos:
**sd = 0.0 en pf4, pf6 y pf6_l8**. NO DISPARA -> el scorer **ya elegia** melon y
fresa el dia 0-6. El tapon no venia de la eleccion.
(Cuarta vez esta semana con la firma sd=0.0: parchear el camino que se LEE en vez
del que EJECUTA.)

### DESCARTADO 3: el piso de forraje era un fantasma (`wheat_floor_live`)

Hipotesis: `wheat_floor` usa `herd = sum(cfg["animals"]) = 8` desde el dia 0,
cuando aun no hay ningun animal, y esas 8 tiles se plantan ANTES que el cultivo
elegido (bucle L819: `(("WHEAT", wheat_gap), (best, resto))`).

| brazo | delta | t |
|---|---|---|
| `wl0` (sin adelanto) | **−45.6** | −11.93 |
| `wl2` | −23.4 | −6.51 |
| `wf4` (piso fijo 4) | −26.2 | −6.89 |
| `wl4` | −30.6 | −8.85 |

**El chasis tenia razon.** Motor L817-819: `if consecutive_unfed >= 2: # Animal
escapes`. Un animal sin comer DOS DIAS se escapa, y el trigo tarda 4 dias en dar:
plantar 8 trigos el dia 0 para animales que llegan el dia 4-8 es **la
anticipacion exacta que exige el ciclo del trigo**, no forraje fantasma.

### El dato que no encaja con ninguna hipotesis mia

| dia | nuestro banco | tetsuya |
|---|---|---|
| 9 | **332** | **5.237** |
| 10 | 1.042 | 1.158 (−4.080) |

**Ellos ACUMULAN y sueltan $4.080 de golpe el dia 10; nosotros vamos a cero
constantemente.** No gastamos menos: goteamos. La diferencia puede no estar en
QUE plantamos ni en CUANDO lo elegimos, sino en la SECUENCIA DE COMPRAS.
**Pista viva, sin probar.**

### Estado: 9 barridos hoy, 9 negativos

Superficie, cuarto cuadrante, rebano, fertilizar un corte, gansos, ventas,
contra-meta, lead time y forraje. **La busqueda por parametros esta agotada** y
tres hipotesis mecanicas sobre la ventana d12-d16 han caido con evidencia dura.
Lo que queda con horizonte real es el planificador (rollout determinista de
nuestra propia granja) o la secuencia de compras.

---

## 2026-09-04 — Seis barridos, seis negativos: estamos en un óptimo local afilado

**Escalera (resuelve la vigilancia de ayer):** `campeona_hoz` 769.5 -> **831.3**
(48 ep) y `campeona_grano` 828.9 -> **786.6** (56 ep). Se cruzaron: era ruido de
arranque. **Con ~50 episodios el rating tiene un error de ±40**, así que la
escalera no arbitra diferencias de 10 puntos; sólo el panel puede.

### Análisis de los 12 replays del TOP1 (tetsuya): DOS hipótesis mías, falsas

`tetsuya` gana 11/12 con $115.822 (nosotros ~$94k). Composición por fases:
melón d6 -> fresa 35 tiles d12 -> trigo 22 d18 -> **trigo 34 d24** -> vacío d29.
Banco de $2.500 el día 12 y $115k al cierre: reinvierten todo.

**FALSO que cultiven el doble.** Medido: nuestra base planta **66.4 tiles en el
pico** (media 44.9), más que sus ~58. `crop_tiles=30` NO limita la superficie —
sólo acota al scorer adaptativo; `idle_plant` planta por encima. Por eso subirlo
no hizo nada.

**FALSO que la mano de obra nos limite.** Regamos el **94% de las plantas vivas**
y **no muere ninguna de sed** (0.0 con 2 días sin regar). No hay superficie
bloqueada que un planificador pudiera desbloquear.

### Los seis barridos (2.880 episodios cada uno)

| frente | mejor brazo | peor brazo |
|---|---|---|
| superficie | `ct_58` −4.1 | `ct50_q4` −16.1 |
| cuarto cuadrante | — | `q4` −13.8 (t=−4.63) |
| rebaño | `r6` −7.8 | **`r15_top1` −29.1 (t=−7.45)** |
| fertilizar un corte | `fm` −5.3 | `fwcm` −37.8 (t=−10.07) |

**Séptimo intento fallido de copiar al meta**, y el más concluyente: su
composición EXACTA de animales es el peor brazo de su barrido.

### El óptimo local, medido en todas las direcciones

| dimensión | óptimo | al moverse |
|---|---|---|
| manos | 12 | 9→−6.9 · 11→−2.8 · 14→−24 · 15→−33 |
| animales | 8 | 6→−7.8 · 10→−8.4 · 13→−15 · 16→−22.5 |
| cuadrantes | 3 | 4→−13.8 |
| superficie | actual | +10→−7.5 · +28→−8.8 |
| ventas | tirar todo | cualquier retención → negativo |
| fertilizante | fresa/tomate, reserva 20 | cualquier cambio → negativo |

**Cada dimensión empeora en AMBOS sentidos. La búsqueda por parámetros está
agotada; lo que quede debe venir de mecanismos nuevos.**

### EL NÚMERO QUE IMPORTA: 12.5% contra el TOP1

Extraídas las 12 cintas de tetsuya (`extraer_top1.py`, prefijo `top_` para NO
mezclarlas con el panel `lad_`: son poblaciones distintas). Contra ellas nuestro
campeón gana el **12.5%**, frente al 58-65% contra la escalera de ~800.

Probada la hipótesis "nuestro óptimo lo es sólo contra esta población":
**NO se confirma.** `r13` sale +4.2 con t=0.81 (ruido); el resto de sus
decisiones también pierden contra ellos.

**Dónde se abre la brecha** (banco mediano por día):

| día | nosotros | tetsuya | ratio |
|---|---|---|---|
| 12 | 3.886 | 2.500 | **1.55** |
| 14 | 12.532 | 15.656 | 0.80 |
| **16** | **14.782** | **28.954** | **0.51** |
| 28 | 70.976 | 106.270 | 0.67 |

**Vamos por delante el día 12 y nos sacan el doble para el 16.** Después el
ratio se congela en 0.67: no perdemos más terreno, pero tampoco lo recuperamos.
**Todo el partido se decide entre los días 12 y 16.**

### MECANISMO DEL MOTOR QUE NO USÁBAMOS (y por qué no sirve)

Motor L431-443: en los cultivos de UN CORTE el rendimiento **no madura con la
edad, lo añade el RIEGO**, sólo dentro de `[(max_yield_day+1)//2 .. max_yield_day]`
— que coincide exactamente con nuestro `c["win"]` (el chasis estaba bien
ingeniado). Y ahí `bonus = 2 if fertilized else 1`:

| cultivo | ventana | sin fert | fertilizado |
|---|---|---|---|
| WHEAT | 2..4 | 4 | **6** (tope) |
| CARROT | 2..3 | 3 | **4** (tope) |
| MELON | 6..12 | tope 6 en edad 10 | tope 6 en edad **8** |

Nunca los fertilizábamos. Añadirlos: **−29.4 (t=−7.84)**. Dos razones:

1. **El fertilizante ya está óptimamente asignado.** Fresa: +4 uds x $199 =
   **+$796**. Trigo: +2 x $46 = **+$92**. La fresa rinde **8.6x más por unidad de
   fertilizante**. Por eso `fert_reserve=40` empeora aún más (−36.2).
2. **`FERTILIZE` roba una acción al RIEGO, y en los de un corte el riego ES el
   rendimiento.** Con el 94% ya regado no hay holgura para el riego futuro que
   cobraría el x2.

Esto reconcilia el `sin_fert = −50` de ayer: recoger fertilizante es vital
**porque alimenta a la fresa**, no porque el fertilizante sea bueno en abstracto.

### Monte Carlo: qué es viable

Medido: el agente usa **0.30 ms/turno de media** (p95 0.57, max 39.4) de un
presupuesto de **1.000 ms**, más 60 s de banco de overage. El episodio entero nos
cuesta **0.22 s de ~780 s disponibles**. Holgura ~3.300x.

- **MCTS sobre la partida completa: DESCARTADO.** Un rollout del motor cuesta
  5.6 s (7.8 ms/turno simulado) y, peor, **el estado del rival es privado**
  (shed, semillas, inventarios): no se puede reconstruir el estado del motor.
- **Rollout determinista de NUESTRA granja: viable.** El crecimiento depende sólo
  de edad/riego/fertilizante y la producción animal de first/interval/cap. Nada
  de eso depende del rival; sólo el precio. Convierte las prioridades cocinadas a
  mano en valores calculables.
- **Búsqueda offline sobre las perillas vivas: automatizable**, con el riesgo
  conocido del winner's curse que envenenó `buscar_apertura.py`.

**Fuentes en internet: nada aprovechable.** El foro está tras login y los
writeups de Lux AI/Halite son de arquitecturas que no transfieren.

---

## 2026-09-03 (7) — El motor leído de primera mano + ventas y contra-meta rechazados

### ¿Lee bien los precios el agente? SÍ

Comparada `_price_at` del chasis contra `market_price` del motor en **5.148
puntos** de los 9 productos: **cero errores por encima de 0.5** (el máximo, 0.50,
es el redondeo a entero del motor). La tabla `MKT` coincide con `MARKET_PARAMS`
parámetro a parámetro. **Ahí no hay nada roto.**

### TRES REGLAS DEL MOTOR QUE NO ESTABAN EN RULES.md

1. **La venta se cotiza UNIDAD A UNIDAD.** `_process_market` recalcula
   `market_price` con el inventario ya incrementado tras cada unidad, así que una
   orden de 40 recorre la curva 40 veces **dentro del mismo turno**.
2. **`if price > 1: inventory += 1`** — *"Sales at \$1 do not increase market
   supply"*. El suelo es absorbente: a \$1 la oferta deja de subir.
3. **El shed tiene capacidad 100 y, si se llena, `BUY_ANIMAL` y `BUY_PRODUCT`
   fallan EN SILENCIO.** Y `BUY_PRODUCT` sólo existe para WHEAT y FERTILIZER.

Medido sobre `campeona_hoz` (16 partidas): **5% de pérdida por ráfaga
(\$5.897/partida)** y ~60 unidades/partida vendidas a \$1 — WOOL 29.6 (25% de la
lana), MILK 18.1 (13%), MELON 11.3.

### `sell_marginal` RECHAZADO — gradiente monótona (2.880 ep, seeds 95500-95503)

| piso marginal | delta | t |
|---|---|---|
| `sm_05` | −3.1 | −2.54 |
| `sm_20` | −4.4 | −3.22 |
| `sm_30` | −5.6 | −3.83 |
| `sm_50` | −8.1 | −4.60 |
| `sm_70` | −10.0 | −4.53 |
| `hinge_hold` | −1.6 | −1.51 |

**Cuanto más aguantas, peor.** La dosis-respuesta monótona es evidencia más
fuerte que cualquier t individual: no hace falta confirmación para rechazar.
**Las 60 unidades a \$1 NO son una fuga; tirarlas es lo correcto.** Tres razones,
todas visibles en el motor: el shed tope 100 se llena; el dinero de hoy compone
25 días; y el mercado es **compartido en lockstep**, así que aguantar le regala
al rival los turnos de precio alto. Confirma `sell_floor=0` desde el otro lado:
`sell_floor` decide SI vender, `sell_marginal` CUÁNTAS, y **las dos formas de
aguantar pierden**.

### CONTRA-META: no hay hueco porque YA somos el contra-meta

Medido contra los 40 rivales reales (80 episodios):

**Composición media del rival al cierre:** COW 7.67, SHEEP 4.42, STRAWBERRY 3.18,
WHEAT 1.11, GOOSE 0.69. **La escalera es pesada en animales y ligera en
cultivos; nosotros al revés.**

**Inventario de mercado al cierre** (10.000 = neutro): de 9 mercados, **8 acaban
en ESCASEZ** — el town drena más de lo que aporta el conjunto. WHEAT cierra a
−448, EGG a −176, CARROT a −189. Sólo dos quedan saturados, **y los saturamos
nosotros**: FERTILIZER +368 (vendemos 157.9) y MELON +148 (vendemos 113.9).

### Y aun así, redirigir esos dos mercados PIERDE (2.880 ep, seeds 96500-96503)

| brazo | delta | t |
|---|---|---|
| `melon_5` | +1.6 | +0.49 (ruido) |
| `fr_40` (reservar fertilizante) | −13.1 | −5.04 |
| `fr_60` = `fr_100` | −14.4 | −5.30 |
| `melon_11` | −16.9 | −4.01 |
| **`sin_fert`** | **−50.0** | **−12.45** |

Que un mercado esté saturado NO implica dejar de venderle: venderlo a \$26-65
bate a guardarlo, porque guardarlo llena el shed y el uso alternativo está
acotado por el número de tiles de fresa/tomate, que `fert_reserve=20` ya cubre.
(`fr_60` == `fr_100` porque la reserva satura contra ese recuento — el mismo
patrón de redundancia que las prioridades.)

**`sin_fert` −50.0 es el efecto más grande medido en todo el día.** Recoger
fertilizante vale la mitad de nuestra tasa de victoria: `collect_fert` +
`fert_dawn_load` + `fert_phase_lock` son el núcleo real de la ventaja.

### ⚠️ VIGILAR: primer desacuerdo serio panel vs escalera

```
campeona_grano   828.9   (38 ep)   panel decia +6.4 sobre fase -> CONFIRMA
campeona_fase    819.4   (66 ep, fuera)
campeona_hoz     769.5   (27 ep)   panel decia +2.5 sobre grano -> CONTRADICE
```

`hoz` está ~60 puntos por debajo de `grano`. Con 27 episodios es pronto (los
ratings arrancan bajos), pero `prio_harvest=76` fue la adopción de **huella más
pequeña** (4 celdas de 160). Si a los ~60 episodios sigue debajo, hay que
revisar si el panel resuelve cambios de huella minúscula.

---

## 2026-09-03 (6) — Gansos: RECHAZADO. Y mi modelo del mercado estaba mal

### El veredicto (2.880 episodios, seeds 94000-94003)

| brazo | composición | panel 40 | delta | t |
|---|---|---|---|---|
| base | COW 4 + SHEEP 4 | 59.1% | — | — |
| `suma_g4` | + GOOSE 4 | 42.5% | −16.6 | −4.61 |
| `mixto` | COW 2 + GOOSE 6 | 30.3% | −28.7 | −7.72 |
| `vaca_g` | COW 4 + GOOSE 4 | 29.1% | −30.0 | −8.79 |
| `g8` | GOOSE 8 | 19.1% | −40.0 | −9.74 |
| `g6` | GOOSE 6 | 15.0% | −44.1 | −10.95 |
| `g10` | GOOSE 10 | 9.7% | **−49.4** | **−13.31** |

### EL ERROR DE MODELO (lo importante de esta entrada)

Leí la tabla `_price_at(producto, 10000 + d)` como si `d` fueran las **ventas
acumuladas de la partida**. NO LO ES: es el exceso de inventario **instantáneo**.
Las ventas se reparten en 25 días y el town drena continuamente, así que el
exceso nunca se acerca a las 100 unidades de golpe.

**Prueba:** WOOL termina la partida a **$247**, por encima de su base de $200.
Tras vender 119 lanas el inventario está POR DEBAJO del inicial.

Mi afirmación de que "regalamos el 30% de la producción animal a $1" era FALSA:

| | base (COW 4 + SHEEP 4) | g8 (8 gansos) |
|---|---|---|
| ingreso animal | MILK $25.354 + WOOL $13.940 = **$39.294** | EGG **$18.324** |
| unidades vendidas | 259 | ~409 |
| **$/unidad** | **$152** | **$45** |
| ingreso de cultivos | $45.349 | $37.153 (también cae) |
| dinero medio | **93.884** | 70.821 |

El ganso pierde por lo más simple: **precio base $50 frente a $160 y $200**. Ser
más barato ($300), más rápido (día 4) y diario (iv=1) no compensa valer 3-4 veces
menos por unidad. Y la mezcla de acciones es IDÉNTICA (53% MOVER, 19% WATER en
ambos): tampoco libera mano de obra.

### ⚠️ REVISAR: la tesis del suelo de $1 del briefing

*"Fresa, lana y leche tocan el suelo de $1 a las ~100 unidades, y eso explica la
lista de experimentos fallidos de escalado"* se apoya en la MISMA lectura
equivocada. Puede seguir siendo cierta para **ráfagas concentradas** (vender 100
fresas el mismo día sí hunde el precio) pero NO para la producción repartida,
que es como vendemos. **Pendiente de re-examen.**

### Y me dejé llevar por UNA partida

Mi sonda de un episodio dio $100.261 para `g8` contra $82.167 de la base, y lo
reporté como señal fuerte. La distribución real de `g8` es mediana $63.668 con
máximo $119.364: pegué en la cola alta. Es el error contra el que advierto en
`METODO.md`, cometido media hora después de escribirlo. **Una sonda de un
episodio sirve para comprobar que una bandera MUERDE, nunca para estimar
su efecto.**

---

## 2026-09-03 (5) — Plantilla: frente CERRADO. 12 manos es el óptimo

**El bug metodológico que invalidaba los intentos previos.** El chasis calcula
`n_h = min(hands_per_quadrant * cuadrantes, hands_cap)`. Con `hpq=4` y 3
cuadrantes eso es `min(12, 12)`:

- `hands_cap=14` → `min(12, 14)` = 12. **No muerde.**
- `hands_per_quadrant=5` → `min(15, 12)` = 12. **No muerde.**

**Los dos experimentos de plantilla del pasado eran estructuralmente incapaces
de probar la hipótesis.** Aquellos "resultados nulos" nunca fueron una prueba.
Para mover la plantilla hay que mover LAS DOS perillas a la vez.

**La economía: S6.1, el HIRE n-ésimo del día cuesta `fib(n)`** — 1, 1, 2, 3, 5,
8, 13, 21, 34, 55, 89, **144** — y los peones desaparecen cada noche (S6.3).
Coste determinista por partida (~21 días de plantilla completa):

| plantilla | $/día en el pico | $ total en HIRE |
|---|---|---|
| 9 | $88 | $1.958 |
| 11 | $232 | $4.982 |
| **12 (base)** | **$376** | **$8.006** |
| 14 | $986 | $19.128 |

**Las manos 11 y 12 se llevan el 61% de todo el presupuesto de contratación.**

### Descubrimiento (2.880 episodios, seeds 93000-93003)

| brazo | manos | delta | t |
|---|---|---|---|
| `h11` | 11 | +5.3 | +1.81 |
| `h10` | 10 | +0.0 | 0.00 |
| `h9` | 9 | −6.9 | −2.44 |
| `hpq5_solo` | 12 (5 temprano) | −12.8 | −3.27 |
| `por_trabajo` (`hire_by_work`) | variable | −17.8 | −4.37 |
| `h14` | 14 | **−24.1** | **−6.07** |
| `h15` | 15 | **−33.4** | **−7.96** |

### Confirmación en semillas disjuntas (2.560 episodios, seeds 93500-93507)

| brazo | descubrimiento | confirmación | veredicto |
|---|---|---|---|
| `h11` | +5.3 (t=+1.81) | **−2.8 (t=−1.43)** | **CAMBIA DE SIGNO** — falso positivo |
| `h10` | +0.0 (t=0.00) | **−7.0 (t=−3.27)** | negativo |

**Nada se adopta. La plantilla de 12 es el óptimo.** `h11` habría entrado con la
tabla del descubrimiento sola: es la demostración más limpia hasta ahora de por
qué el protocolo de confirmación en semillas disjuntas no es opcional. Con 8
brazos contra una base, el mejor de todos a t=1.81 es justo lo que produce el
azar.

**`hire_by_work` rechazado con instrumento bueno.** El comentario del chasis
argumentaba que la cinta del meta corre 8.3 manos de media frente a nuestras ~11
y que ahí estaba el exceso de ~950 pasos. Razonamiento plausible, medida
demoledora (−17.8). **Quinto intento fallido de copiarle algo al meta.**

**Y ampliar temprano también es malo** (`hpq5_solo`, −12.8): gastar en peones el
día 5 retrasa la compra del cuadrante. Las perillas de plantilla no son
independientes del resto de la economía — compiten por la misma caja.

### Lo que esto le hace a la fuga que originó el frente

El 8.2% de `PASS` **no era dinero recuperable ni ampliando ni recortando**. Y el
53.5% de movimiento tampoco es obviamente desperdicio: son 3.897 pasos para
2.789 servicios, o sea **1.4 pasos por acción útil**, cerca del suelo teórico de
1.0 en una malla donde las tiles contiguas están a un paso. La mano de obra no
es el cuello de botella que parecía.

---

## 2026-09-03 (4) — Las prioridades son un RANKING, no magnitudes

**Por qué este barrido:** `muerde.py` dejó 6 perillas de prioridad vivas
(`prio_water`, `prio_feed`, `prio_care`, `prio_harvest`, `prio_plant`,
`fert_prio`) y ninguna se había tuneado con el panel de 40 — todas las búsquedas
previas usaron paneles rotos o saturados.

**El hallazgo estructural.** Tres pares de brazos salieron **idénticos celda a
celda** en las 160 celdas. No es azar: cada par produce **la misma reordenación**
por caminos distintos.

| par idéntico | la reordenación que ambos consiguen |
|---|---|
| `water_30` == `feed_85` | FEED siempre por encima de WATER |
| `harvest_50` == `fert_60` | FERTILIZE por encima del HARVEST de baja |
| `plant_55` == `fert_30` | PLANT por encima de FERTILIZE |
| `plant_28` == base | bajar la que YA es última no reordena nada |

**Consecuencia sobre el pasado:** `evolucion9` y `evolucion10` trataron estos
números como continuos. El espacio real es el de **órdenes** — pocas
permutaciones alcanzables — y buscar sobre magnitudes explora una redundancia
enorme donde la mayoría de los movimientos son no-ops. Sumado a las 11 perillas
muertas, buena parte de aquella CPU se fue en no moverse.

### Resultados (4.480 episodios, seeds 92000-92003)

| brazo | delta | t | reordenación |
|---|---|---|---|
| **`harvest_76`** | **+2.5** | **+2.02** | HARVEST sobre FEED y CARE |
| `care_80` | +2.8 | +0.89 | CARE sobre FEED |
| `harvest_50`=`fert_60` | +0.0 | 0.00 | |
| `water_30`=`feed_85` | −6.2 | −2.33 | FEED siempre sobre WATER |
| `care_55` | −10.3 | −3.46 | CARE bajo HARVEST |
| `plant_55`=`fert_30` | −13.4 | −4.43 | PLANT sobre FERTILIZE |

Las tres reordenaciones malas confirman que el orden actual **no es arbitrario**:
el riego debe poder ganarle a la comida cuando está en ventana o urgente.

### CONFIRMACIÓN en semillas disjuntas (2.560 episodios, seeds 92500-92507)

| brazo | descubrimiento | confirmación | veredicto |
|---|---|---|---|
| `harvest_76` | +2.5 (t=2.02) | **+2.5 (t=2.96)** | **ADOPTADO** — delta idéntico |
| `care_80` | +2.8 (t=0.89) | +1.1 (t=0.50) | rechazado, ruido |

`harvest_76` difiere de la base en sólo **4 de 160 celdas** y aun así replica el
delta exacto: el reorden importa en pocas situaciones, y en esas voltea la
partida. **Campeón: `CAMPEONA_HOZ`** (= `CAMPEONA_GRANO` + `prio_harvest=76`).

### Dónde se va la mano de obra (instrumento nuevo)

Una partida completa, 13 unidades, 7.285 turnos:

| acción | % |
|---|---|
| **`_MOVER`** | **53.5%** |
| WATER | 19.1% |
| **`PASS`** | **8.2%** |
| HARVEST | 3.9% |
| FEED+CARE+COLLECT | 8.6% |
| PLANT+FERTILIZE+DIG | 4.1% |

**El 62% del presupuesto no produce nada.** El `PASS` no está repartido: se
acumula al final del día (h21 25%, h22 35%, **h23 40%**) y en los días 27-29
(27%, 20%, 23%). Las cuadrillas terminan el circuito hacia las 20:00.

**Hipótesis descartada:** pre-posicionar durante esas horas muertas para la ruta
de mañana. Al alba TODAS las unidades están en (4,4) — S1.1 aplica a la
cuadrilla entera, no sólo al granjero. La posición de fin de día es irrelevante.

**Pista abierta:** a la hora 0 sólo existe el granjero; las 12 manos aparecen
durante el día. Si la plantilla se contrata a diario, una mano que pasa 4 horas
en `PASS` es dinero pagado por turnos vacíos. ¿Paga la mano marginal del día 27
en adelante?

---

## 2026-09-03 (3) — INSPECCIÓN DURA: el chasis tiene DOS cerebros y 11 perillas muertas

**El hallazgo estructural.** El chasis implementa **dos veces** la misma
pregunta ("¿qué hago en esta tile?"):

1. la lista `tasks` con prioridades (`prio_harvest`, `prio_water`…)
2. **`_service_ops`**, que es la que MANDA cuando `router=True` — y el campeón
   lleva `router=True`

Ya divergieron. Reglas que no coinciden entre las dos:

| regla | `_service_ops` (manda) | lista `tasks` |
|---|---|---|
| cosechar fresa/tomate | `yu >= 2` o día ≥ 28 | `yu >= 3` (alta) / `yu >= 2` (baja) |
| cosechar un corte en el pico | **exige estar regada** | no lo exige |
| regar continuas el día final | permitido | prohibido |
| cosechar animal | `yu >= min(h_at, cap-1)` | `yu >= cap-1` / `yu >= h_at` |

**Herramienta nueva: `muerde.py`.** Quita (o perturba) cada clave del config y
comprueba si el resultado cambia. 306 episodios, ~4 min.

**Trampa que casi me come:** si el valor del config COINCIDE con el default del
chasis, quitar la clave es un no-op **por construcción** y el test no dice nada.
`sell_floor=0` salió "inerte" en la v1 — y es un mecanismo ADOPTADO (+3.1).
Para esas claves hay que PERTURBAR. Segunda trampa: perturbar restando una
constante (2000 → 1970) tampoco prueba nada; la perturbación debe ser
proporcional. Ambas corregidas dentro de la herramienta.

### Las 11 perillas MUERTAS (18% del config es decoración)

| clave | valor | por qué no muerde |
|---|---|---|
| `plants` | `{CARROT:1, MELON:11, STRAWBERRY:5, WHEAT:8}` | **`adaptive=True` ignora el plan fijo entero** |
| `hands` | 8 | lo pisa `hands_per_quadrant 4 × 3 cuadrantes = 12` |
| `mkt_opp_factor` | 1 | lo pisa `opp_read=True` |
| `tiles_per_unit` | 5 | sólo se lee bajo `phased=True` (apagado) |
| `zone_fallback_prio` | 70 | sólo bajo `zoning=True` (apagado) |
| `prio_dig`, `prio_urgency`, `prio_win_bonus` | 8/25/12 | esas tiles las resuelve el router |
| `premium_hold_day` | 8 | — |
| `multi_feeder`, `smart_overflow` | False | apagadas |

**`plants` es la peor: quien lea el config creerá que plantamos 11 melones y 8
trigos. No plantamos nada de eso — decide el scorer adaptativo.** Y `hands=8`
es el mismo cuento que `hands_cap=14`: una perilla que no llega a morder.

**Lo que SÍ vive:** `prio_harvest`, `prio_water`, `prio_feed`, `prio_care`,
`prio_plant`, `fert_prio`, `wave_min_value`. La lista de prioridades NO está
muerta del todo — gobierna a las unidades fuera de ruta.

**Consecuencia sobre el pasado:** toda búsqueda sobre el config (`evolucion9`,
`evolucion10`, `buscar_apertura`) estuvo explorando 11 dimensiones muertas.

### `endgame_reap` RECHAZADO — pero por fin con un resultado de verdad

v1 y v2 sobre la lista `tasks`: **sd = 0.0**, código muerto para el router.
v3 sobre `_service_ops` sí muerde: el día 29, `WATER` se evalúa ANTES que
`HARVEST` y retorna de inmediato, así que una planta con rendimiento y sin regar
se REGABA (bonus que ya no hay mañana para cobrar) en vez de cosecharse; y la de
un corte con `age < peak` no entraba nunca en la rama de `HARVEST`.

Producto en pie al cerrar: **$1.994 → $1.485/partida (−26%)**.
Panel de 40 (320 pares, seeds 91300-91307): **−0.2, sd 2.8, t = −1.00.**

**Recuperar $509 no compra ni un punto de rating** — y encaja con que el Elo es
W/L/T: $509 sobre $73.000 es 0,7% del margen, casi nunca voltea un resultado.
Bandera apagada, arreglo conservado detrás del flag.

> **La regla que separa las dos fugas de hoy:** la de semillas pagó (+6.4) porque
> liberaba caja TEMPRANO para componer 25 días; la del día 29 no pagó porque
> devolvía monedas cuando ya no quedaba nada que hacer con ellas.
> **No importa cuánto dinero recuperas, importa cuándo.**

---

## 2026-09-03 (2) — `seed_stock_aware`: ADOPTADO (+6.4, t=+2.62 confirmado)

**Cambio de instrumento:** en vez de leer replays, inspeccionar el **estado
terminal** de la partida y preguntar *"¿qué compramos y nunca usamos?"*.
48 episodios de `campeona_fase`, dos fugas duras:

| fuga | medida |
|---|---|
| semillas compradas y jamás sembradas | **40.3 uds = $2.005/partida** |
| plantas cosechables en pie al cerrar | 10.9 |

**Causa raíz de la fuga de semillas — desajuste de unidades en el chasis.**
`deficit` cuenta **tiles** (global, cualquier cultivo), pero la compra sólo
descontaba el stock del cultivo `best` de HOY:

```python
adaptive_need = max(0, deficit - seeds.get(best, 0))   # <- solo `best`
```

Cada vez que `best` rota, el lote anterior deja de contar y se compra uno nuevo
**para las mismas tiles**. Por eso el melón era el peor ($867): es la semilla
cara que más rota como `best`. El mismo defecto estaba duplicado en `idle_plant`.

**Arreglo (`seed_stock_aware`):** descontar el stock TOTAL de semillas aún
plantables hoy, en los dos sitios que compran.

| | base | con el arreglo |
|---|---|---|
| semillas sobrantes | 40.3 | **20.6** |
| $ muertos | $2.005 | **$551** |
| melón / fresa | $867 / $665 | $90 / $133 |

**Panel de 40 — descubrimiento y confirmación en semillas DISJUNTAS:**

| corrida | seeds | pares | delta | sd | t |
|---|---|---|---|---|---|
| descubrimiento | 91000–91003 | 160 | +6.6 | 44.6 | +1.86 |
| **confirmación** | **91100–91107** | **320** | **+6.4** | **43.7** | **+2.62** |

El efecto replicó casi exacto en semillas que no participaron en su
descubrimiento → no era winner's curse. **Campeón: `CAMPEONA_GRANO`**
(= `CAMPEONA_FASE` + `seed_stock_aware`). Segundo efecto más grande jamás
medido, sólo por detrás de `fert_dawn_load` (+12.8).

**Van 8 de 8: todas las ganancias han salido de incoherencias internas del
chasis, ninguna de ideas estratégicas ni de copiar al meta.**

### `endgame_reap` RECHAZADO — y el diagnóstico era malo

delta +0.0 con **sd = 0.0**: la bandera nunca llega a morder. La puse en la rama
`if ready:` de los cultivos de un solo corte, donde el riego pre-cosecha exige
`not overdue`, o sea `age == peak` EXACTO — casi ninguna planta cumple eso el
día 29. Y sobre todo: las 10.9 plantas en pie **no son de un solo corte** (a
esas el código ya les da `HARVEST` a prio 85 cuando se pasan), son **continuas**
(fresa/tomate), que viven en la rama `else` que el parche ni toca. Esa fuga es
de **capacidad de mano de obra el último día**, no de prioridades. Sigue abierta.

### ⚠️ REGLA NUEVA: `sd = 0.0` significa "no se ejecutó", no "no sirve"

Tercera vez con esta firma (`hands_cap 14`, `fase_noop2`, `endgame_reap`). Un
arm que sale **idéntico** al base en las 160 celdas no es un resultado nulo, es
un **test nulo**: el mecanismo no cambió ni una decisión. Antes de leer un
"+0.0" como rechazo, comprobar que la bandera dispara.

---

## 2026-09-03 — Cuarentena cerrada: no había nada que rescatar

**El motivo:** varios mecanismos se rechazaron con paneles que después
resultaron rotos o saturados. El bug de `medicion.py` sólo producía FALSOS
NEGATIVOS, así que en principio podía haber ideas buenas enterradas por error.
Re-medidos los cinco contra el panel de 40 rivales reales (2.560 episodios):

| mecanismo | panel 40 | delta | t | veredicto |
|---|---|---|---|---|
| `_noop` | 56.9% | +0.0 | — | control ✅ |
| `work_steal` | 29.7% | **−27.2** | **−7.67** | veneno confirmado |
| `fert_pickup` | 57.5% | +0.6 | +1.00 | nulo |
| `season_aware` | 55.3% | −1.6 | −0.50 | nulo |
| `sheep6` | 49.4% | −7.5 | −1.91 | negativo |
| `hands_cap 14` | 56.9% | +0.0 | — | **NO DISPARA** |
| `campeona_fb` (ref. externa) | 38.1% | −18.8 | −6.06 | coherente ✅ |

**Los cinco rechazos originales eran correctos.** La asimetría del bug era real
como propiedad del bug, pero en la práctica no había nada bueno enterrado.

**`hands_cap=14` es un test nulo, no un resultado nulo.** Lee +0.0 con sd = 0.0,
es decir no cambia ni una sola decisión: el tope efectivo lo pone
`hands_per_quadrant × 3 = 12`, así que la bandera nunca llega a morder.
Cuidado con leer "sd = 0" como "sin efecto": significa "sin ejecución".

**`fert_pickup` pasó de dañino a nulo** — ahora tiene sentido: `fert_dawn_load`
ya resuelve la logística que `fert_pickup` intentaba resolver caminando al shed.
**`season_aware` sigue siendo redundante** tras `fallback_fix`, como decía la
entrada original.

Con esto queda cerrada la cola entera de ideas pendientes de la bitácora.

---

## 2026-09-02 (2) — El panel de 40 rivales REALES: el instrumento que sí ordena como el Elo

**El problema que lo motiva:** el ladder no reproducía nuestro orden local.
`ruta` ganaba 90-10 a `alba` en el panel de 5 cintas y en el ladder estaban
empatadas (844.9 vs 846.6).

**Diagnóstico: el panel de 5 estaba SOBREAJUSTADO por construcción.** Se eligieron
por tener resolución (celdas 25-75%), y eso es seleccionar los rivales donde
nuestras diferencias se amplifican — selección sobre el estadístico que se mide.

| bot | Elo real | panel 5 (seleccionado) | **panel 40 (completo)** |
|---|---|---|---|
| campeona_ruta | 844.9 | **61.6%** | 51.6% |
| campeona_alba | 846.6 | 46.0% | 54.7% |
| campeona_fase | 826.4 | — | 56.9% |

El panel de 40 (todos los rivales de una submission, sin seleccionar) reproduce el
empate del ladder; el de 5 no. Herramientas: `extraer_todos.py`, `panel40.py`.
`METODO.md` §5 corregido.

**RE-MEDICIÓN DE LAS 4 ADOPCIONES (ablación leave-one-out, 160 pares):**

| apagar | delta | sd | t | el mecanismo vale |
|---|---|---|---|---|
| `_noop` | +0.0 | 0.0 | — | control ✅ |
| `sell_floor 0` | −3.1 | 15.5 | **−2.54** | **+3.1** ✅ |
| `fert_dawn_load` | −12.8 | 34.2 | **−4.74** | **+12.8** ✅ |
| `fert_phase_lock` | −2.5 | 18.4 | −1.72 | +2.5 marginal |
| **paquete `ruta`** | **+5.3** | 45.8 | +1.47 | **−5.3, NO significativo** |
| `campeona_fb` (Elo 787.3) | −13.4 | 48.1 | −3.53 | referencia externa ✅ |

**Convergencia:** los dos únicos que pasan t>2 (`sell_floor 0` y `fert_dawn_load`)
son exactamente los que lleva `CAMPEONA_ALBA`, la submission con más Elo (846.6).
El instrumento local y el externo por fin coinciden.

**El paquete `ruta` no está probado como dañino (t=+1.47) pero NUNCA demostró
ayudar con instrumento válido.** Por nuestra propia regla (t>2) no debió adoptarse.
Predicción escrita antes de ver el número: fallé en las dos direcciones — esperaba
que el paquete sobreviviera "porque arregla bugs verificados" y sospechaba de
`fert_phase_lock`. *Lección: arreglar un bug verificado NO garantiza mejorar.*

**`buy_feed` (la #1 de la cola pendiente) — DESCARTADO, −34.4 pts (t=−8.61).**
El mayor negativo de la sesión, peor que retroceder tres generaciones. El mecanismo
funciona como se diseñó (trigo plantado 64 -> 2, fresa 11 -> 69) pero mete los 290
tile-días liberados en FRESA, que toca el piso de $1 a las ~100 unidades: valen los
~$25 del margen, no los $93.6 del precio base. Y encima perdemos el trigo como
producto vendible, **el único sumidero sin fondo del juego** (a +450 sigue a $19.9).
*La aritmética de la cola valoraba al margen equivocado — mismo error que `crop_max`.*
`herd_scale` decae con él (la bitácora lo condicionaba a que buy_feed funcionara).

**ERROR PROPIO GRAVE — parche mal indentado.** El primer `buy_feed` dejó huérfano
un `_commit` dentro del bloque nuevo y, peor, su `if` a indentación 4 CERRÓ el
bloque contenedor, cambiando la condición de la compra de tierra. La base se
desplomó de 56.9% a 15.6% y por un momento pareció que `campeona_fb` superaba a
`campeona_fase`. **Lo detectó el brazo `_noop`, que leía 15.6% igual que la base:
si el control se mueve, lo roto es el instrumento, no el candidato.** Corregido y
verificado (la base vuelve a 56.9% exacto). Es la segunda vez en el día que un
control de este tipo evita una conclusión falsa.

## 2026-09-02 — El plan de apertura: FRENTE CERRADO, y dos errores de método propios

**Contexto:** con el ladder asentándose a ~1 episodio/2h y 28 días de plazo, se
decidió no esperar la validación externa y atacar la **optimización offline de la
trayectoria** (la "Opción A" que la bitácora identificó hace semanas).

**La descomposición que la hace viable:** medido sobre las 12 partidas del top-1,
**el 83% de las acciones de unidad no miran al rival** (MOVE 43.9% + campo 39.5%).
El campo es casi un problema de UN jugador y admite optimización offline; sólo el
mercado interactúa (máx 10 órdenes/turno). Por eso funcionan las cintas.

**Mecanismo `opening_plan`** (gateado): para los días <= `plan_until` las órdenes
de COMPRA las dicta un calendario; ventas, HIRE, rutas y reparación siguen siendo
del chasis. Barrido del horizonte (10 seeds, vs cinta ahmad_ali):

| plan_until | dinero medio | delta |
|---|---|---|
| base (sin plan) | $85,105 | — |
| día 0 | $85,105 | **+0** (control exacto: el mecanismo no mete ruido) |
| día 2 | $86,960 | +1,855 |
| día 4 | $87,971 | +2,866 |
| día 12 | $79,882 | **−5,223** |

Congelar de más DESTRUYE adaptación que sí vale. El horizonte útil es 0-4.

**LA COMPROBACIÓN PREVIA QUE CANCELÓ LA BÚSQUEDA.** Antes de gastar horas se midió
cuánto puede moverse la palanca: 6 aperturas aleatorias razonables (3-6 animales,
4-10 lotes de semillas en d0-d4, todas dentro de presupuesto) contra la nuestra,
panel de 5 cintas:

| plan | win-rate |
|---|---|
| **BASE (nuestro scorer)** | **50.0%** |
| rnd0 / rnd3 | 6.0% / 4.0% |
| rnd1, rnd2, rnd4, rnd5 | **0.0%** |

**Amplitud 50 puntos, y las seis aleatorias se hunden.** La apertura es una palanca
enorme pero de UN SOLO SENTIDO: se puede destrozar la partida, pero nuestro scorer
ya está en la meseta buena. La superficie no es una colina que subir sino una
meseta estrecha rodeada de acantilados — por eso el hill-climbing rechazó 248 de
250 mutaciones. **Frente cerrado**, y con él el punto ciego (a) del BRIEFING
("la secuencia de apertura de los días 0-2").

**Error de método 1 — winner's curse en el hill-climber.** El buscador guardaba la
puntuación del titular como estimación ÚNICA sin re-evaluarla. Cuando it018 sacó
+10.8 con t=1.46 (por debajo del listón), ese 67.5% quedó congelado como referencia
y las 232 iteraciones siguientes competían contra un número inflado por suerte. Al
re-medir en seeds frescos, la ganancia real era **+$1,360, dentro del ruido**, no
+17 puntos. *Lección: con evaluación ruidosa hay que re-evaluar al titular cada
iteración, o el primer golpe de suerte congela la búsqueda.*

**Error de método 2 — se repitió el incidente del 2026-08-26.** Se lanzó
multiprocessing SIN `if __name__ == "__main__"` y se provocó una tormenta de spawns
en macOS: **384 MB de tracebacks**. La bitácora ya decía "Guard SIEMPRE" y aun así
ocurrió. Corregido y verificado en `buscar_apertura.py` y en los scripts auxiliares.

**Riesgo evitado por poco — cintas sobrescritas.** Al minar las derrotas de
CAMPEONA_ALBA, `reconstruir.py` reescribió `axel_ahmer`, que es una cinta ACTIVA
del panel v2 extraída de CAMPEONA_FB. Detectado y restaurado (el panel vuelve a
leer 50.0% exacto); la nueva quedó como `axel_ahmer_b`. *El extractor nombra por
slug del rival: dos episodios del mismo rival colisionan silenciosamente.*

**Panel ampliado** con 6 cintas nuevas de las derrotas de ALBA (todas validadas
EXACTAS): demon_ji, umkaaa, caminolsy, tatsuhito_yoshikawa, patwid, axel_ahmer_b.

**Estado del ladder:** campeona_ruta 844.9 (41 eps), campeona_alba 846.6 (48),
campeona_fase 826.4 (48). **El ladder NO reproduce el orden local** (ruta gana
90-10 a alba y 78-22 a fase en el panel). Causas posibles sin distinguir: pocos
episodios, cintas ciegas, o ruido de Elo (±30-40). Sigue abierto.

## 2026-09-01 — CAMPEONA_FASE + el diagnóstico de "acciones por parada" FALSADO

**Nueva campeona: `CAMPEONA_FASE` = ALBA + `fert_phase_lock`.** `_fert_due` aceptaba
NUEVE edades seguidas en la fresa (8..16) cuando solo DOS pagan: el motor
(kaggriculture.py L777-800) tickea con `next_day`, así que el riego que cobra el x2
es el de la VÍSPERA del tick (edades 9,11,13,15). Fertilizar en 9 y en 13 cubre los
cuatro ticks con dos aplicaciones. Verificado: fresa 9 edades -> [9,13]; tomate -> [7,10].

| medición | resultado |
|---|---|
| panel de 5 cintas | **+8.0 pts, t=+2.75** (200 eps), positivo en las 5 celdas |
| head-to-head vs ALBA | **94-6 = 94.0%** (IC95 [88%,97%], 100 eps) |
| controles | `_noop` +0.0 · `_peor` −38.5 |
| efecto | FERTILIZE 95 -> **68** y fresa 254u sobre 54 plantas (4.70/planta) |

**Acumulado del ciclo: `CAMPEONA_FASE` 80-0 (100.0%) contra `campeona_fb`**
($93,282 vs $79,804). Cadena: fb -> `sell_floor 0` -> `fert_dawn_load` -> `fert_phase_lock`.

Descartado en la misma tanda: `idle_best_only` (−2.5, t=−0.44).

---

**FALSADO: "acciones productivas por parada" NO es el objetivo.**

| bot | prod/parada | paradas de 4 | prod/move | WR panel |
|---|---|---|---|---|
| cinta C95 | 1.85 | 203 | 1.03 | — |
| campeona_fb | 1.45 | 60 | 0.81 | — |
| campeona_alba | 1.53 | 55 | 0.85 | 73.0% |
| **campeona_fase** | **1.49** | **46** | 0.84 | **81.0%** |

**La campeona nueva es la MEJOR en win-rate y la PEOR en paradas de 4.** Causa:
`fert_phase_lock` QUITA fertilizaciones (95 -> 68); las 27 eliminadas no cubrían
ningún tick pagador. **La métrica cuenta acciones, no valor**: optimizarla empuja a
hacer más trabajo inútil por visita. El 1.85 de la cinta es CONSECUENCIA de su
granja, no causa de su éxito — copiar el estadístico habría sido cargo-culting.
Coherente con que `harvest_at=1`, que SÍ sube la métrica, midiera +0.0 exacto.

Queda como correlato de diagnóstico, nunca como objetivo. **Cuarta explicación del
foso caída en dos días** (riego, bundling, tamaño de rebaño, acciones por parada).

**Nota de proceso (feedback del usuario):** de los 13 agentes del primer workflow
salió UNA mejora (`fert_dawn_load`, la mayor del día); el segundo se cortó en 3/6
lentes. `fert_phase_lock` costó CERO agentes — salió de una lente cacheada,
implementada y medida con el harness. El cuello ya no es generar ideas (la cola
está llena: `melon_head`, `shed_access_reservado`, gate de `herd_demand`) sino
MEDIRLAS: `herd_demand` necesita ~420 pares y tiene 225.

## 2026-08-31 (4) — Teardown del notebook "from zero to top meta": la cinta C95 decodificada

**Hallazgo de material.** El notebook de Rayk Kretzschmar
(`kaggriculture-findings-from-zero-to-top-meta`) no es solo prosa: las celdas 46/51/54
llevan **el fuente completo de tres agentes del top meta** (C92, C94, C95) en
base64+zlib, y dentro de C95 va `_TRACE`, **la cinta exacta de 720 turnos** de
Lev Neganov episodio 91587143 player 1. Todo decodificado en `bots/meta/`.

**Rival de panel nuevo y real.** `bots/meta/c95_main.py` corre limpio en 1.32.7:
$175,142 vs starter. Contra `campeona_fb`: **0-24, $76.7k vs $113.1k** (24 eps).
Es la pieza que le faltaba al panel: fuerte, discriminante y no endogámico.
`campeona_noop` leyó **idéntico** a la base ($79,400, misma sd) — el brazo de
control sigue sano tras todos los parches de hoy.

**La cinta, medida (determinista, de `trace_c95.json`):** 10 vacas + 4 ovejas,
0 gansos; 3 cuadrantes (NE día 6 step 160, SW día 10 step 240, nunca SE);
peones en RAMPA 4/1/2/3/3/3/4/7/6/7 y luego 8-14 (media 8.3, no plano);
apertura step 0 = HIRE x4 + COW 1 + **SHEEP 4** + 5 semillas wheat + 5 melón +
5 wheat de producto (~$2,900 de $3,000); siembra 138 WHEAT (13-15/día desde el
día 19), 37 STRAWBERRY, 18 MELON, **cero carrot y cero tomate**; 301
COLLECT_FERTILIZER, 72 FERTILIZE (≈2 por fresa) y 242 fertilizer vendidos;
CARE se corta el día 27 y FEED el 28 (abandono deliberado del rebaño).
Fresa: 299 unidades sobre 37 plantas = **7.87/planta** (el máximo teórico con
los 4 ticks duplicados es 8). Nosotros: 220 sobre 65 = **3.38/planta**.

**Mezcla de acciones, misma seed, mismo formato:**

| | cinta C95 | campeona_fb |
|---|---|---|
| unit-turns | 6,716 | 7,286 |
| MOVE | 42.8% | 52.5% |
| WATER | 15.1% | **19.4%** (el 51% del briefing es de una versión vieja) |
| PASS | 15.4% | 10.5% |
| **productivas / movimiento** | **0.98** | **0.70** |

**El hecho económico que reordena la lista de fallidos.** Precio tras vender N
unidades a mercado fresco (`_price_at`): WHEAT 25 -> 19.9 a +450 (¡80% del base!);
FERTILIZER 100 -> 60 a +200; MELON 250 -> 1 a +200; **STRAWBERRY, WOOL y MILK
tocan el piso de $1 a las ~100 unidades**. Integrando las curvas sobre lo que
vendió cada uno, la descomposición del gap: WHEAT **+$7,409**, MELON **+$5,379**,
FERTILIZER **+$4,568**, y MILK/WOOL/STRAWBERRY **+$127/+$128/+$115**.
Sus 6 vacas de más valen $127; sus 79 fresas de más valen $115.
*Esto no contradice la lista de fallidos: la explica.* Escalar el rebaño falló
tres veces porque la leche marginal vale $1, no por falta de ejecución.

**Siete hipótesis estructurales sacadas de la cinta.** *(Corrección de instrumento: la
primera lectura fue por MEDIAS CRUDAS, con sd $18k y ±$6-8k de banda — no resolvía
nada. El test correcto es el PAREADO por seed espejado, que es lo que prescribe el
propio aparato: la sd cae a $0.5-2.2k y ahí sí hay veredicto. `_noop` leyó delta
exactamente 0 con sd 0.)*

| mecanismo | delta pareado | sd(par) | t | veredicto |
|---|---|---|---|---|
| `water_cadence` | −$20,566 | — | — | **negativo duro** |
| `crop_max` fresa 8 | −$1,220 | 11,714 | −0.29 | **INCONCLUSO** (no negativo) |
| `sell_marginal` 0.4 | −$591 | 1,341 | −1.25 | negativo débil |
| `sell_marginal` 0.5 | −$965 | 1,522 | −1.79 | negativo |
| `sell_marginal` 0.6 | −$3,430 | 2,230 | **−4.35** | **negativo duro y monótono** |
| `sell_floor` 0 | **+$506** | 829 | **+1.72** | **positivo débil** |
| `sell_floor` 0.2 | −$6 | 547 | −0.03 | nulo |
| `drop_deposit` v2000 | −$18 | 173 | −0.29 | no dispara nunca |
| `drop_deposit` v1000 | −$5,973 | 7,564 | −2.23 | negativo |

La monotonía de `sell_marginal` (t=−4.35 en el piso más alto) confirma
"correr, no aguantar". `crop_max` NO quedó refutado: su sd pareada es $11.7k
porque cambia la granja entera; necesita n real.

**Detalle antiguo (medias crudas, conservado para trazabilidad):**
(8 seeds espejados = 16 eps c/u, dinero vs C95; base $79,400):

| mecanismo | resultado | nota |
|---|---|---|
| `water_cadence` (regar sólo si paga: ventana de one-time, víspera de tick fertilizado, o cu>=1) | **$58,834** | mató las muertes (46.5->10.0) y los riegos perdidos (14.5->2.5) y AUN ASÍ perdió: productivas 2,724->2,310, movimiento 3,780->4,736 |
| `crop_max` fresa 8 / 12 | $78,180 | **reprodujo la mezcla exacta de la cinta** (137 wheat / 36 fresa vs sus 138/37) y el dinero no se movió |
| `hire_by_work` (plantilla al ritmo del trabajo) | $48,439 (1 seed) | la curva salió 1/1/2/4/5/5/5/5/6/8/12, parecida a la cinta, pero el proxy de trabajo no ve el setup del día 0 |
| `sell_marginal` 0.4 / 0.5 / 0.6 | $78,809 / $78,434 / $75,970 | acotar cada orden para que la unidad marginal supere el piso |
| `sell_floor` 0 / 0.2 | $79,905 / $79,394 | quitar el piso |

**Las dos lecciones metodológicas del día:**

1. **El riego no era un impuesto sobre el presupuesto de acciones: era la carga
   útil que amortizaba las caminatas.** Quitar los riegos que el motor no paga
   subió el movimiento a 66% y bajó las productivas. El cuello no es cuántas
   acciones gastamos sino **cuánto trabajo hay por visita**.
2. **En un mercado compartido en lockstep, aguantar inventario se lo regala al
   rival.** La columna de C95 sube monótona con nuestro pacing:
   $114.6k (base) -> $116.3k (floor 0.5) -> $118.4k (floor 0.6). Por eso el autor
   del notebook dejó `_RESERVE = {}` y `_RACE_WEIGHT = 0.0`: toda su maquinaria de
   reserve-price con forecast de drenaje del town está **en el código y apagada**.
   Lo que sí deja encendido es `_SORT_KEY='impact'` — correr, no aguantar.

**Conclusión.** La composición y la política de mercado **no transfieren**: es el
hallazgo de LN_CLONE otra vez, ahora con el agente meta real y a grano mucho más
fino. El foso es la capa de ejecución, cuantificado como **0.70 vs 0.98
productivas por paso**. Todos los mecanismos de hoy quedan gateados y apagados en
`CAMPEONA_FB`, que sigue leyendo idéntico.

**SUBMISSION 55924018 — `campeona_alba` al ladder.**

Empaquetada con `empaquetar.py CAMPEONA_ALBA` y verificada con las tres pruebas
que exige la historia del repo (el bug del orden de dict de 2026-08-19):

1. **Espejo** `submission/main.py` vs el módulo: 8-8-4 con **dinero idéntico y
   misma sd** ($74,561 en ambos lados). Es la firma correcta de agentes iguales
   —cada seed se juega dos veces con lados invertidos— y no el 8-0 imposible que
   delató el bug antiguo.
2. **Fidelidad byte a byte**: **0 de 2,157 decisiones distintas** entre
   `submission/main.py` y `bots.arquetipos:campeona_alba`.
3. Self-play DONE/DONE y humo vs starter $129,036.

Descripción con `campeona_alba` como PRIMER TOKEN, que es lo que `bajar_replays.py`
usa para separar carpetas: sin eso los replays caerían en `CAMPEONA_FB/` — justo la
mezcla de generaciones que ese guard existe para evitar.

**Par activo ahora: `campeona_alba` (55924018) + `campeona_fb` (55876067, 805.7).**
`campeona_season` sale del matchmaking. El incumbente queda vivo como control: el
ladder arbitra el A/B directamente.

**Cómo leerlo (y cómo NO).** Toda submission arranca en 600 y necesita ~50-90
episodios para asentarse. El notebook del meta documenta el caso extremo: dos
copias con el MISMO SHA-256 acabaron en 2182.2 y 1210.1 por puro camino de
oponentes y asientos, y la segunda subió a 1865.6 sin tocar código. **No leer las
primeras 24 h.** El criterio es el rating asentado contra los 805.7 de campeona_fb,
no el número de mañana temprano.

**Predicción falsable, para no engañarnos después:** si `fert_dawn_load` y
`sell_floor=0` transfieren al meta real, `campeona_alba` debería asentarse
CLARAMENTE por encima de 805.7. Si se asienta en la banda 780-830 el resultado es
nulo y la ganancia local era específica de las cintas del panel (rivales CIEGOS,
que no reaccionan a que vendamos antes) — una hipótesis muy viva, porque el
mecanismo `sell_floor=0` explota exactamente eso. Si baja de 780, revertir.

**CAMPEONA FINAL DEL DÍA: `CAMPEONA_ALBA` = CARRERA + `fert_dawn_load`.**

Re-medición de los tres mecanismos mal juzgados, sobre CARRERA y el panel válido
(200 eps por brazo):

| variante | takahirohon | ahmad_ali | artfix | masih_pemula | uman_n3l | MEDIA | delta | t | veredicto |
|---|---|---|---|---|---|---|---|---|---|
| CARRERA (base) | 37.5% | 55.0% | 47.5% | 72.5% | 75.0% | 57.5% | — | — | — |
| +`crop_max` fresa 8 | 32.5% | 42.5% | 32.5% | 70.0% | 52.5% | 46.0% | −11.5 | −2.82 | descartar |
| +`hinge_forecast` | 30.0% | 52.5% | 32.5% | 70.0% | 65.0% | 50.0% | −7.5 | −2.89 | descartar |
| **+`fert_dawn_load`** | **57.5%** | **85.0%** | **77.5%** | 65.0% | **80.0%** | **73.0%** | **+15.5** | **+3.70** | **ADOPTAR** |

Confirmación head-to-head (100 eps, seeds 41000): **90-10 = 90.0%** (IC95 [83%,94%])
contra CAMPEONA_CARRERA, con `_noop` en **33-33-34 = 50.0%** exacto y dinero idéntico.
Aquí el dinero TAMBIÉN sube ($87,198 vs $80,541): contra un rival que no es C95 el
intercambio fertilizante->fresa sí paga.

**El mecanismo.** Ejecutábamos los ONE-TIME al 100% (melón 6.00 u/planta de 6) y los
ONGOING al 42% (fresa 3.38 de 8). `_service_ops` gatea FERTILIZE en `has_fert` y la
unidad llegaba a la fresa con las manos vacías. No es el `fert_pickup` que falló:
aquel caminaba al shed A MEDIA RUTA y rompía la localidad de la serpentina. Aquí no
hay viaje — por S1.1/S6.2 el motor GARANTIZA que al amanecer toda unidad está en una
tile de acceso al shed, así que un solo PICKUP carga la cuota del día.
Efecto medido: FERTILIZE 25 -> 95, fresa **3.38 -> 4.63 u/planta**, melón 90 -> 114
unidades (el mismo 114 de la cinta del meta).

**Cadena del día:** CAMPEONA_FB -> +`sell_floor 0` (CARRERA) -> +`fert_dawn_load` (ALBA).
**ALBA vs CAMPEONA_FB: 96-4 = 96.0%** (IC95 [90%,98%]), $89,996 vs $81,493, 100 eps.

**Lo que NO cambió, y hay que decirlo.** Contra C95 seguimos **0-16** y con el mismo
dinero que esta mañana ($78,258 contra $79,400 de la base — dentro del ruido). La
ganancia del día es real contra rivales de NUESTRA banda y no acorta la distancia
con el top del meta. El foso de ejecución (0.70 productivas por paso contra 0.98)
sigue intacto.

**Y el aviso metodológico repetido dos veces en un día:** `fert_dawn_load` leía
−$3,879 en la lente de dinero contra C95 y yo lo reporté como negativo con una
explicación aritmética correcta al dólar (convierte fertilizante de $85 en fresa de
$25). La aritmética era cierta y la conclusión falsa: la caja baja y los DUELOS
suben. Dos mecanismos adoptados hoy, los dos rescatados de un descarte por lente
equivocada.

**NUEVA CAMPEONA: `CAMPEONA_CARRERA` = CAMPEONA_FB con `sell_floor = 0`.**

Primer mecanismo del proyecto validado sobre un panel que pasa sus propios
controles. Resultados sobre las 5 cintas reconstruidas (20 seeds espejados por
celda = 200 episodios por brazo, seeds 31000):

| brazo | takahirohon | ahmad_ali | artfix | masih_pemula | uman_n3l | MEDIA | delta | t |
|---|---|---|---|---|---|---|---|---|
| base | 32.5% | 52.5% | 40.0% | 65.0% | 75.0% | **53.0%** | — | — |
| `_noop` | 32.5% | 52.5% | 40.0% | 65.0% | 75.0% | **53.0%** | **+0.0** | — |
| **`sell_floor 0`** | 37.5% | 55.0% | 47.5% | 72.5% | 75.0% | **57.5%** | **+4.5** | **+2.23** |
| `_peor` | 22.5% | 40.0% | 7.5% | 30.0% | 72.5% | **34.5%** | −18.5 | −3.32 |

`_noop` +0.0 en las CINCO celdas; `_peor` negativo en las CINCO. El candidato sube
en 4/5 y no baja en ninguna. Más el head-to-head: **77-21-2 = 78.0%** contra
CAMPEONA_FB (IC95 [69%,85%], 100 eps) con `_noop` en 50.0% exacto.

**El mecanismo, en una frase:** en un mercado compartido en lockstep aguantar
inventario se lo regala al rival. `sell_floor` decidía NO vender con el precio bajo
y el rival vendía dentro del precio que nosotros sosteníamos. Evidencia directa: al
subir nuestro pacing el dinero de C95 subía monótono ($114.6k -> $116.3k -> $118.4k)
mientras el nuestro bajaba. Es la misma conclusión del autor del notebook: su
reserve-price con forecast de drenaje está escrito y **enviado apagado**
(`_RESERVE = {}`, `_RACE_WEIGHT = 0.0`); lo único encendido es `_SORT_KEY='impact'`.

**Lección de método (la más cara del día).** Este mecanismo leía **+$506 (t=1.72)**
en la lente de dinero contra C95 y estuvo a punto de descartarse. En win-rate contra
panel diverso son +4.5 pts (t=2.23) y +28 pts cara a cara. El Elo paga W/L/T, no
margen. Los otros once mecanismos del día se juzgaron con la lente de dinero: los
negativos duros se sostienen, pero `crop_max`, `hinge_forecast` y `fert_dawn_load`
quedaron descartados por un instrumento ciego y se re-miden sobre la campeona nueva.

**PANEL NUEVO: rivales reales del ladder reconstruidos como cintas.**

Bajados los **54 replays de campeona_fb (submission 55876067) y de ninguna otra**
(`bajar_replays.py --activas 2` habría mezclado campeona_season; se fue directo al
ID). Marcador real: **27V 26D 1E = 50.9%**. El episodio 102802012 es contra
"Rospel" — espejo contra nosotros mismos, empatado al centavo: buen control de que
el clasificador acierta el lado.

**Bug del extractor (costaba el experimento entero).** En el replay DESCARGADO la
acción del índice t es la que YA se aplicó para llegar a ese estado, no la que se
toma desde él. Sin corregirlo la simulación va un turno por detrás y la granja
colapsa: $12,470 contra los $85,804 reales — el mismo síntoma que el handicap
sintético, y se habría leído como "las cintas no sirven". La firma que lo delata es
que la curva de dinero cumple `sim[t] == real[t-1]`. Con `shift=1`:

| episodio | rival | real (yo/rival) | extracción | vs bot vivo |
|---|---|---|---|---|
| 104210270 | Uman_n3l | 82,068/85,804 | **EXACTA** | 82,068/85,804 |
| 102861914 | Zihao Zeng | 62,672/70,020 | **EXACTA** | 62,672/70,020 |
| 102819471 | ArtFix | 105,116/113,804 | **EXACTA** | 105,116/113,804 |
| (8 de 8) | | | **EXACTA** | idéntico |

Cero turnos divergentes en los 720. **Validación extra no buscada: nuestro
campeona_fb LOCAL reproduce el marcador del ladder al centavo -> el bot local es
idéntico al subido.**

**Perfil del panel en seeds frescos (n=20 espejados, seeds 21000):**

| cinta | nuestro WR | nuestro $ | su $ |
|---|---|---|---|
| zihao_zeng | 0.0% | 73,716 | 98,172 |
| axel_ahmer | 5.0% | 81,238 | 93,796 |
| **takahirohon** | **52.5%** | 78,042 | 81,731 |
| **ahmad_ali** | **52.5%** | 86,408 | 86,383 |
| **artfix** | **55.0%** | 78,547 | 82,491 |
| **masih_pemula_beneran** | **72.5%** | 82,496 | 78,986 |
| **uman_n3l** | **75.0%** | 77,294 | 67,716 |
| sgsuh | 80.0% | 88,246 | 76,272 |

Cinco caen en la banda de resolución 25-75% (media 61.5%, cerca del 65.2% del panel
viejo) y a diferencia del handicap sintético **no colapsan** en seeds ajenos.

**Limitaciones honestas.** Una cinta es CIEGA: no reacciona a nosotros, así que es
algo más débil que el rival original y su varianza sube en seeds ajenos
(zihao_zeng hace $116.9k en seeds frescos contra los $70.0k de su partida real).
El propio notebook del meta marca el límite: las cintas fijas son un diagnóstico
correlacionado, no una puerta de promoción; los seeds vírgenes siguen mandando.

Herramientas: `derrotas.py` (clasificación con guard de TeamNames),
`reconstruir.py` (extracción + doble validación), `bots/meta/tape.py`,
`bots/meta/tapes/*.json.gz`.

**EL HALLAZGO PRINCIPAL DEL DÍA: el panel oficial es CIEGO A LAS MEJORAS.**

100 episodios head-to-head contra el campeón, con control:

| brazo | vs `campeona_fb` | dinero |
|---|---|---|
| `_noop` | **34-34-32 -> 50.0%** exacto | $84,606 vs $84,606, idéntico al centavo |
| `sell_floor 0` | **77-21-2 -> 78.0%**, IC95 [69%, 85%] | $84,960 vs $83,660 |

+28 puntos de win-rate con el dinero casi igual. **Lección de método: la lente de
dinero contra C95 daba +$506 (t=1.72) y casi lo descarto.** Los otros once
mecanismos del día fueron juzgados con esa misma lente equivocada; los negativos
duros se sostienen, pero los "planos" (`crop_max`, `hinge_forecast`,
`fert_dawn_load`) quedaron descartados con un instrumento que no ve lo que paga Elo.

Pero al llevarlo al panel (25 seeds x 4 rivales, seeds 11000):

| brazo | vs C95 | vs cinta v16 | vs campeona | vs rutera |
|---|---|---|---|---|
| base | 0% | 0% | 100% | 100% |
| `_noop` | 0% | 0% | 100% | 100% |
| `sell_floor 0` | **0%** | **0%** | **100%** | **100%** |
| `_peor` | 4% | 2% | 16% | 100% |

**Todas las celdas saturadas.** El candidato es INDISTINGUIBLE de la base en las
cuatro. Sólo `_peor` se mueve -> el panel detecta regresiones y es ciego a las
mejoras: modo de fallo #3 del BRIEFING, ahora confirmado con datos. Causa raíz:
**no hay ningún rival entre nuestro nivel y el del meta.** Contra todo el linaje
C90-C95 vamos 0% (los tres comparten la misma cinta de campo); contra nuestras
generaciones viejas, 100%.

**Intento de instrumento (FALLIDO, `bots/meta/c95_handicap.py`).** Idea: degradar
la cinta de forma determinista para fabricar rivales de fuerza graduable.
(a) Anular una fracción de acciones de peón: **colapsa a $0** — la cinta no tiene
holgura, desincronizar PICKUP/PLACE/FEED destruye la granja. (b) Topar unidades
vendidas por turno: sí produce un dial (s2 100%, s8 91.7%, s11 58.3%, s16 0%),
pero **falla sus dos controles**: el brazo `_peor` lee +12.7 pts POR ENCIMA de la
base (debía leer claramente peor), y el punto de calibración oscila
**66% / 90% / 74%** en tres bloques de seeds de n=25 con IC que no se solapan.
Throttlear las ventas del rival no produce una versión más débil del mismo juego:
produce OTRO juego. Instrumento descartado.

**Conclusión operativa.** El cuello del proyecto no es la falta de ideas: es que
**no existe un instrumento capaz de decir que sí.** Un panel válido necesita
rivales (a) de fuerza intermedia real, (b) diversos en estrategia, (c) NO derivados
de nuestro propio bot, y (d) estables entre bloques de seeds. La única fuente que
cumple las cuatro es el ladder: reconstruir 3-5 rivales reales de nuestra banda
como agentes-cinta. Es exactamente el método del autor del notebook ("download the
current leaders, work out which moves repeat, turn the repeatable part into a local
agent") y ya tenemos la herramienta (`bajar_replays.py`, `perfilar_rivales.py`).

Estado de `sell_floor 0`: 78% contra su padre con control limpio, indistinguible
contra todo lo demás. **No se enciende hasta tener panel válido.**

**Segunda tanda (tomate/hinge y fertilizante) — el eje queda cerrado por SIMETRÍA:**

| mecanismo | delta pareado | sd(par) | t |
|---|---|---|---|
| `hinge_forecast` (horizonte hasta el cierre para curvas hinge) | +$7 | 4,405 | +0.00 |
| `hinge_forecast` + `hinge_hold` | −$2,253 | 3,408 | −1.87 |
| `fert_dawn_load` + `fert_tick_aligned` | −$3,879 | 6,090 | −1.80 |
| `fert_dawn_load` solo | −$4,088 | 6,028 | −1.92 |
| `fert_crops=[]` (no fertilizar nada) | −$1,812 | 3,107 | −1.65 |
| rebaño 6+6 | −$10,272 | 19,983 | −1.45 |

**`fert_dawn_load` funciona como mecanismo y aun así pierde — y la aritmética cuadra
al dólar.** FERTILIZE 25 -> 101, fresa vendida 220 -> 288 (5.05 u/planta, era 3.38).
Pero FERTILIZER vendido 184 -> 110: **−74 unidades a ~$85 = −$6,290**, contra +68
fresas que al margen valen ~$25-40 = **+$2,000**. Neto teórico −$4,300; medido
−$3,879. *Estamos convirtiendo fertilizante de $85 en fresa de $25.*
Y como no fertilizar nada TAMBIÉN pierde (−$1,812), el nivel actual es un óptimo
local: el eje del fertilizante está cerrado por ambos lados.

**El rendimiento por planta es EL número del proyecto:**

| cultivo | cinta | nosotros | máximo |
|---|---|---|---|
| MELÓN (one-time) | 6.33 | **6.00** | 6 (100%) |
| FRESA (ongoing) | 8.08 | **3.38** | 8 (42%) |
| TOMATE (ongoing) | — | **3.5** (71u de 20 plantas) | 8 (44%) |

Los one-time los ejecutamos al 100%; los ongoing al 42%. Por eso ningún cambio de
composición mueve la caja: multiplicamos otro cultivo por el mismo 0.44. El tomate
NO falla por el mercado (el hinge es real: $102-144/u con 2-3 tiendas, verificado
con `_price_at`); falla por lo mismo que la fresa.

**Sobre el tomate, para no perderlo:** demanda de temporada ~250u contra oferta
combinada de 6u; déficit final medido 220-283 según sorteo de tiendas
(PIZZA_SHOP y FARMERS_MARKET son las únicas que lo piden). Vender 120u el día 29
con 2 tiendas = $12,614 ($105/u). La oportunidad existe y es NUESTRA sola — la
tabla `_MP` de C95 es anterior al parche 1.32.7 — pero requiere primero saber
cosechar un ongoing.

**Corrección de una lectura mía:** dije que la cinta "pacea el melón de 6 en 6".
**Falso.** Verificado sobre `trace_c95.json`: casi todos los `SELL MELON 6` van
inmediatamente después de cosechas — el 6 es el `max_yield` de UNA planta. La cinta
no pacea el melón: **vende en cuanto cosecha**. Refuerza la misma conclusión.

**Latencia DROP->SELL (medida, y remedio fallido):** el único `DROP` del chasis
estaba en el endgame (día>=28); todo lo cosechado antes espera al auto-drop nocturno
(S6.3) y sólo es vendible a h0 del día siguiente. Medido: **87% de nuestras ventas a
h0 contra 52% de C95**; primera venta de melón step 288 contra su step 252. Pero
`drop_deposit` (DROP oportunista en tile de acceso, forma C72: 1 paso / valor 2000)
**casi nunca dispara** (delta −18, sd 173): nuestras rutas no pasan por el shed a
media jornada. La latencia es real; el remedio exige cambiar las RUTAS, no la
política de venta.

**Nota de ventaja:** la tabla `_MP` de C95 es **anterior a 1.32.7** — no tiene la
forma `hinge` y lleva CARROT `below_target` 0.20. Nuestro `MKT` sí tiene el modelo
correcto (RULES S5.1). El meta está valorando mal carrot/tomate/huevo.

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

## 2026-09-02 (3) — Evolución 9: primera selección por WIN-RATE → nace `campeona`, al ladder

**Cambio de fitness:** win_rate x 1e6 + dinero (victorias primero). Justificación: los mecanismos ganadores del día eran neutros en dinero — el proxy viejo los habría descartado. 4,740 episodios, 8 generaciones, panel coevolutivo [gemela + barnyard + cinta], registro de 2,534 firmas previas respetado.

**Ganadora `t5e_3` → `CAMPEONA`:** final 60.0% WR (lector_ref 48.3%); **confirmación head-to-head en seeds vírgenes 46-4 ($90.9k vs $81.6k)**; verificación de transcripción 16-0 en seeds nuevos ($92.3k vs $83.4k); autopsia **$118.0k absoluto, 8% ocio**.

**Lo que la evolución adoptó (y que solas eran neutras):** `beat_wave=True` (ya corregida, umbral $2,000) y **`melon_max=8`** — la disciplina de melón que el usuario pidió, rechazada en ablación aislada y validada aquí dentro de la combinación correcta; tercera vez que se repite el patrón (hands_per_quadrant, ahora estas dos): *el valor de un mecanismo depende de sus compañeros*. También: 3er cuadrante y prio_feed 75.

**Subida al ladder** con autorización explícita del usuario ("sube solo la mejor"): submission de `CAMPEONA`. Fugas restantes para la próxima ronda: 36.5 plantas muertas ($3.7k, la sobre-expansión de idle_plant+land_early sigue sin regarse a tiempo) y 18.5 riegos de ventana ($1.5k) — objetivos de la fase 3 del router (rutas ordenadas por deadline, no solo por espacio).

## 2026-09-03 — Forense de la derrota vs Akshay V → `season_aware`: el scorer aprende el calendario

**La partida (102138884, -$41,723):** íbamos GANANDO +$11,102 el día 18 y terminamos -$40,791 — tiramos $52k en nueve días. Ventas reales reconstruidas (ventas_reales.py, desde el inventario de mercado): **el 85% del gap son FRESAS — 130u/$31.5k nuestras vs 265u/$64.1k suyas**; en wheat/melón/carrot/tomate le ganamos. Con ~50 tiles de fresa desde el día 18 vendimos la mitad de unidades que él: las plantamos TARDE (d9: 6 tiles, d12: 8, d15: 25, d18: 50) y una fresa es ongoing con 4 tandas (edades 10,12,14,16) — plantada el d18 alcanza una sola.

**Doble miopía del scorer** (responde también la pregunta del usuario sobre carrot vs fresa): (1) valoraba la fresa en 4 unidades ignorando que fertilizada rinde 8; (2) trataba una fresa del día 18 igual que una del día 5. A precios REALIZADOS medidos en nuestras partidas: fresa 8u x $231 / 18d = **$103/tile-día**, melón 6u x $141 / 11d = $77, carrot 3u x $57 / 4d = $43. El carrot es la peor tile del juego SALVO al cierre, cuando es lo único que completa ciclo (4 días) — plantarlo el d24 es correcto, el d9 (9 tiles contra Akshay) es el error.

**`season_aware` (gateado):** unidades esperadas = las que el cultivo alcanza a rendir antes del día 30. Fresa 8 (d0-12) → 6 (d15) → 2 (d18) → 0 (d21); melón 0 desde el d21. Es la idea del usuario del VALOR COMPUESTO aplicada al scorer.

**Evidencia (dos mediciones independientes, seeds distintos):** ablación 72 eps/variante 29.2% vs 13.9%; confirmación 176 eps/variante en seeds vírgenes 46.0% vs 35.2%. **Combinado: 248 eps/variante, +12.1 puntos de win-rate (2.9 sigma), +$4k de economía.** `scorer_v2` rechazado por TERCERA vez (-1.4%) — enterrado.

Candidata `CAMPEONA_SEASON` registrada. **Pendiente de autorización explícita del usuario para subir.**

## 2026-09-03 (2) — Forense exhaustivo: la fertilización es LA fuga; la veta de duelos cerrados está agotada

Enjambre forense sobre 17 replays de la era CAMPEONA (9W-8L, 52.9% WR, $80.2k vs $90.2k). Cinco analistas cayeron cuando la Mac se durmió; el sintetizador reconstruyó el análisis completo.

**1. La veta de duelos cerrados está AGOTADA.** Margen <$8k: **5 victorias, 0 derrotas**. La derrota más cercana necesita +$9,720. `sell_rank`/`opp_read`/`beat_wave` ya cobraron todo lo convertible — más ingeniería de lockstep tiene retorno ~cero. El siguiente punto de rating se compra con ECONOMÍA.

**2. Nuestro techo es plano:** ingreso bruto $110,325 en victorias vs $109,861 en derrotas (0.4%). El resultado lo determina el rival: $70.1k cuando ganamos, $112.9k cuando perdemos. No perdemos partidas — nos superan en producción.

**3. Autocorrección de `ventas_reales.py`:** atribuía las COMPRAS del rival como ventas suyas (el residuo del balance de inventario). El rival compra ~390 wheat/partida; neto, NOSOTROS le ganamos en wheat (+$4,148). "Plantar más wheat" iba a ser la recomendación #1 y era falsa. Corregido.

**4. Gap neto real en derrotas ($31,701):** STRAWBERRY +$18,930 (60%), MILK +$9,335, WOOL +$5,513 = **107% del gap**; en wheat y carrot ganamos.

**5. LA FUGA: recolectamos 208.4 fertilizantes/partida y ejecutamos 21.8 FERTILIZE.** Solo el 24.7% de nuestras fresas se fertiliza; el rival 62.4% (75.8% en derrotas). Rendimiento: 3.32 u/tile nuestro vs 5.34 suyo — **plantamos 37% más tiles de fresa y cosechamos 15% menos unidades**. Causa raíz: el FERTILIZE era puramente oportunista (solo la unidad que casualmente cargaba fertilizante); nunca iba al shed a buscarlo, y de noche todo se volcaba y se vendía a $65 (65% del base). Existía el patrón exacto que faltaba: el desvío WHEAT→FEED.
→ Implementado `fert_pickup` (desvío de adquisición al shed, espejo del de FEED) + `fert_tick_aligned` (aplicar en edad tick-2..tick: 2 aplicaciones cubren los 4 ticks de la fresa) + `fert_reserve` (no vender lo que se va a usar). Estimación con la curva: **+$13,100/partida neto**. Presupuesto de acciones verificado: ~102 turnos-unidad necesarios contra 215 en PASS en esa ventana.

**6. Interacción que obliga a shipear junto con `season_aware`:** el scorer hace `ticks *= 2` para fert_crops — **ya asume que fertilizamos**. Con 24.7% real, sobrevalúa la fresa sobre una promesa que el ejecutor no cumple; `fert_pickup` la vuelve verdad. Ablación 2x2 en curso (panel DIVERSO, 120 eps/variante).

**7. Respuestas a las observaciones del usuario:**
- *Farmhand quieto*: NO es bug. Las unidades quietas están en tiles del shed los días 2-3 (granja de 1 cuadrante saturada: 0.0-0.1 tiles vacías, no hay trabajo que dar) y en el cierre d27-29 (ocio real pero inconvertible: nada plantado en d28-29 completa ciclo). 8 peones cuestan $54/día (fib) — el ocio temprano es casi gratis.
- *Movimiento*: 53.3% nuestro vs **54.6% del rival** — estamos a la par; ya no es la frontera (la zonificación fue rechazada por unanimidad evolutiva).
- *Tercer cuadrante*: ocupación 67-72 de 75 tiles (90-96%) — las vacías que se ven son 3-8, no un cuadrante ocioso.
- *Carrot vs fresa*: a precios realizados, fresa $103/tile-día > melón $77 > carrot $43. El carrot solo es correcto al cierre (ciclo de 4 días); `season_aware` ya lo mueve ahí.

**8. Veredicto sobre las ideas del usuario:** VALOR COMPUESTO confirmado con tres evidencias independientes (fresa d9-12 rinde 5.39 u/tile vs 1.02 en d18+; nuestras tiles de wheat cuestan 365 tile-días de fresa; $29-48k de banco parado desde el d10). FASES confirmadas como estructura, pero NO como flag de política (`phased=False` en 9/9 finalistas evolutivos): la fase correcta vive como **horizonte dentro del scorer** — que es exactamente lo que son `season_aware` y `fert_tick_aligned`.

**Cola pendiente:** `buy_feed` (comprar forraje libera 365 tile-días: $28.4/tile-día pagados vs $93.6 que rinde una fresa fertilizada) y `herd_scale` (8 animales fijos desde el d10 vs 13.5 del rival, con $29-48k de banco parado) — este último SOLO detrás de buy_feed, porque escalar rebaño sin resolver la logística de forraje ya falló dos veces (sheep8, MIMADA_XL).

## 2026-09-03 (3) — El panel degenerado, y el veredicto: `season_aware` sí, `fert_pickup` no

**Incidente metodológico:** la ablación 2x2 en panel "diverso" [clon + control + barnyard] devolvió **66.7% para las CUATRO variantes** — idéntico al decimal. Panel DEGENERADO: 40/40 contra los débiles, 0/40 contra el fuerte; el resultado lo fijaba el rival, no la variante. Cero poder de discriminación. Lección: un panel puede fallar por endogamia (todos iguales a nosotros) O por saturación (todos decididos de antemano); hay que exigirle **zona de decisión**. Panel corregido con nuestra propia escalera histórica [CAMPEONA + RUTERA + INTEGRAL], donde cada partida se puede ganar o perder.

**Verificación del mecanismo (antes de juzgar el resultado):** FERTILIZE ejecutados 18 (base) → 59 (fert_pickup) → 73 (+season); PASS 866 → 588. El mecanismo hace lo que promete.

**Ablación en panel discriminante (120 eps/variante):**

| variante | win-rate | dinero |
|---|---|---|
| **season_aware** | **89.2% (+18.3 pts, 3.6σ)** | $89,625 |
| season + fert | 88.3% (+17.5, 3.4σ) | $90,983 |
| fert solo | 81.7% (+10.8, 2.0σ) | $88,597 |
| base (CAMPEONA) | 70.8% | — |

**Desempate head-to-head (80 eps espejados): season 48-32 sobre season_fert (60.0%, +1.8σ).**

**Veredicto:** `season_aware` es el ganador — **tercera confirmación independiente** (2.3σ, 2.1σ, 3.6σ; 616 episodios acumulados). `fert_pickup` ayuda en solitario (+10.8 pts) pero **no aporta sobre season_aware y pierde el head-to-head**: la superaditividad que predijo el forense NO se cumplió. Hipótesis del porqué: season_aware ya redirige las tiles al cultivo correcto en el momento correcto, y encima de eso las ~55 acciones extra de fertilización compran menos de lo que cuestan en el margen. Queda gateado y apagado, disponible si el meta cambia (los rivales fuertes SÍ fertilizan el 62-75%, así que puede pagar contra ellos aunque no contra nuestra escalera).

**Candidata final: `CAMPEONA_SEASON`** (CAMPEONA + season_aware). Pendiente de autorización del usuario.

## 2026-09-03 (4) — CAMPEONA_SEASON al ladder + higiene de replays por generación

**Submission enviada** (autorización explícita del usuario): `campeona_season` — CAMPEONA + `season_aware`. Validación self-play OK ($98.0k / $97.1k); config verificada en el paquete (`'season_aware': True`, línea 952). *Nota: el chequeo automático dio un falso negativo porque buscaba comillas dobles y pprint escribe simples — verificado a mano.*

**Higiene de datos (riesgo señalado por el usuario):** los replays mezclaban 7 generaciones de bots. Auditoría episodio→submission de los 171 replays locales:
- Los dos análisis que motivaron los hallazgos grandes SÍ eran del campeón: **Akshay V (102138884) → CAMPEONA** y **ShiviWhivi (102203713) → CAMPEONA** ✓. Eric Han Wang y meryol eran de integral_v2 (generación inmediata anterior); Tarun de rutera y "ln" de v1 (análisis viejos, ya archivados).
- **Limpieza:** borrados 70 replays de generaciones retiradas (1.7 GB); los 101 restantes reorganizados en `replays/CAMPEONA/` (41) y `replays/integral_v2/` (60) — las dos activas en el ladder.
- **Prevención estructural:** `bajar_replays.py` descarga SOLO de las submissions activas y las deja separadas por bot; imprime cuáles son las activas. Nunca más se mezclan generaciones en un análisis.

Ratings al momento: CAMPEONA 770.1, integral v2 765.8 (mejor histórico; arrancamos en 600).

## 2026-09-04 — Las tres observaciones del usuario, resueltas (y el bug de las zanahorias)

Replay 102786320 (`campeona_season` vs Omkar Kadam, -$24.8k), archivado en `replays/CAMPEONA_SEASON/`.

**1. "Hay tiles sin plantar" — CIERTO, pero plantarlas es VENENO.** Día 0: 11 tiles vacías con 18 semillas en mano; día 12: 16 vacías con 42 semillas. Implementé `idle_plant_walkers` (que una unidad de camino plante una tile vacía contigua): **-55.8 pts de win-rate (-10.5σ)** y **727 plantas muertas ($53,140)** contra 24 de la base. Las tiles vacías no son negligencia: son el límite real de la capacidad de RIEGO. Mismo error que el `grow` ingenuo de agosto. Descartado, gateado y apagado.

**2. "Farmhand 4 se queda muchos turnos en la misma tile" — CIERTO y medido**: 16 episodios de ≥8 turnos sin moverse; el peor, unidad 4 con **20 turnos en (4,4) y 17 PASS** (días 2 y 3). Causa: el router le da una ruta de 1 tile, la termina y nadie le reasigna trabajo. Implementé `work_steal` (la unidad ociosa roba la mitad de la cola del compañero más cargado): **-24.2 pts (-4.3σ)** y -$13,225. Robar tiles rompe la localidad de la serpentina — más movimiento (4,281 vs 3,978) y menos acciones productivas (2,554 vs 2,858). *El sanity de UN seed daba $111k (parecía bueno) y la autopsia ya delataba la verdad; leer el dinero de un seed en vez de la autopsia casi me engaña otra vez.* Descartado, gateado y apagado.

**3. "¿Por qué zanahorias con la fresa a 6x?" — ERA UN BUG, y es el hallazgo grande.** Día 11 del replay: 44 CARROTS plantados a $42 con la fresa a $186 y cero tiles nuestras de fresa. Instrumenté el scorer en ese turno exacto: el scorer PRINCIPAL sí prefería fresa (score 70.2 vs 25.1 del carrot). El culpable era el **fallback de `melon_max`**: al cortar el melón, elegía el segundo cultivo con un modelo distinto — unidades crudas, sin `season_aware` ni el ×2 del fertilizante — y sumándole la oferta rival estimada (144u de fresa) la fresa colapsaba al floor y ganaba el carrot. **Dos caminos de decisión con dos modelos de valor distintos.**

**`fallback_fix`** (ambos caminos puntúan con el mismo modelo): **+14.2 pts de win-rate (3.2σ), +$2,708**; head-to-head **62-28 (68.9%, 3.9σ)** sobre `fallback+season_aware`. `season_aware` queda **redundante** una vez arreglado el fallback (sus 3 confirmaciones previas se midieron con el bug presente: compensaba parcialmente lo que el fallback rompía). Candidata: **`CAMPEONA_FB`**, pendiente de autorización.

## 2026-09-04 (2) — CAMPEONA_FB al ladder

**Submission 55876067** enviada con autorización del usuario ("Subela con ese fix"). Validación self-play OK ($75.2k/$73.9k); `'fallback_fix': True` verificado en la línea 1018 del paquete. Decisión del usuario: dejarla acumular partidas antes de la siguiente iteración.

Estado del ladder al enviar: **campeona_season 782.3** (nuevo máximo histórico, +12 en su primer día), campeona 772.3, integral v2 retirada de facto por el cupo de 2 activas. Con 3 submissions en cola de reemplazo, las dos que compiten pasarán a ser season y fb — exactamente las dos candidatas validadas.

## 2026-09-05 — El instrumento estaba roto: el empate contaba como derrota

**El bug.** `evolucion9.py` agregaba `a["w"] += my > their`. El motor es DETERMINISTA, así que un cambio inocuo produce empates EXACTOS — y un empate no es `>`, así que iba a la columna de derrotas. Un brazo `noop` (cash_buffer 200→201) leía **33.3%** en vez de 50%: **28 de 80 episodios eran empates contados como derrotas**. Con ese medidor se probaron 19 variantes en un día y las 19 salieron negativas. Esa uniformidad era la firma del medidor, no de 19 malas ideas.

**El segundo hallazgo, peor que el bug.** El duelo espejo contra la gemela tiene SUELO: `a66` (rebaño 6+6) y `_peor` (`fallback_fix=False`, literalmente la generación anterior del ladder, peor por 31 puntos de rating real) leen **ambos 5.0%**. No distingue "malo" de "distinto". Razón de teoría de juegos: en el espejo ambos bots compiten por el mismo mercado con la misma estrategia en un equilibrio delicado; cualquier desviación rompe la simetría y la gemela la explota. Medíamos **distancia a nuestro propio óptimo local**, no calidad. El panel escalera [CAMPEONA+RUTERA+INTEGRAL] sí discrimina: separa `_peor` de la base a −3.8σ.

**`medicion.py` (nuevo, obligatorio para toda ablación):** (1) empates a 0.5 y reportados aparte; (2) sigma agrupada por par (seed, rival) — los episodios espejados comparten semilla y contarlos como 2 muestras la infla ~40%; (3) brazos de control automáticos: `_noop` (debe leer igual que la BASE — no igual a 50%: contra panel externo la base puede estar en 97% legítimamente) y `_peor` (la generación anterior, que además **prueba si el panel discrimina**; si no ve una diferencia conocida, no tiene autoridad para juzgar ninguna otra). El reporte se autodiagnostica en pantalla. *Mi primera versión del validador comparaba contra 50% y declaró "¡SESGADO!" a un panel que funcionaba: el control atrapó un error en el control.*

**Asimetría del daño:** el bug solo producía FALSOS NEGATIVOS. Nunca nos hizo adoptar algo malo; nos hizo descartar cosas que quizá servían. En cuarentena (medidos solo en espejo): `work_steal`, `fert_pickup`, los recortes/ampliaciones de plantilla, sheep6/sheep8 y el desempate que descartó `season_aware`. Siguen rechazados los que tenían evidencia MECÁNICA independiente del panel: `idle_plant_walkers` (727 plantas muertas contra 24) y `a66` (revalidado en escalera, muy por debajo del suelo).

### Mecanismos nuevos medidos con el instrumento corregido

- **`order_funding` + `animal_first`**: el chasis comprobaba la caja en cada compra sin descontar lo ya encolado ese turno, así que las semillas se comían el dinero del animal y el `BUY_ANIMAL` se rechazaba en silencio (**47% de rechazos**, medido). Con el fix bajan a 25%. Pero los animales COMPRADOS no cambian (18 en ambos casos): el techo era el target fijo de 8, no la caja. Al arreglar la secuencia, **el orden de armado de órdenes se revela como la política de asignación de capital** — y estaba invertido (animales $191/tile-día contra fresa $46). `animal_first` mueve el bloque del animal delante de las semillas. Primera lectura: **100.0% (108-0) contra 97.2% de la base**, +1.4σ — prometedor, en confirmación.
- **`herd_demand` (rebaño derivado de la demanda del town): RECHAZADO.** 41.7-50.0% contra 97.2% de la base, muy por debajo del suelo `_peor` (81.5%) — daño real, no artefacto. El scorer sí logra el comportamiento buscado (en un town con dos YARN_STORE elige oveja y rechaza vaca), pero el rebaño grande no paga con nuestra ejecución: 12 peones ya saturados de riego. Queda gateado y apagado. Dos bugs propios corregidos en el camino: un `NameError` (`me` en vez de `obs["player"]`) que paralizaba al bot desde el día 6, y un modelo de precio que restaba el drenaje del town de TODA la temporada, fingiendo escasez y comprando 14 vacas en monocultivo (corregido con `herd_drain_days`, horizonte de 8 días como el scorer de cultivos).

## 2026-09-05 (2) — El panel también estaba roto, y de dos formas opuestas

Con el medidor arreglado, los dos paneles que usábamos fallan **simétricamente**:

| panel | base | diagnóstico |
|---|---|---|
| escalera [camp+rut+int+xl] | **97.1%** | SATURADO por arriba: 2.9 pts de margen para detectar mejoras |
| duro [barnyard+v16+int] | **30.6%** | CIEGO por abajo: `_peor` a −0.6σ, no ve una diferencia conocida |

El panel duro fue rechazado **por el control automático**, no por mi criterio: el reporte imprimió `[¡CIEGO!]` y `NO interpretar los deltas`. Sin él habría concluido "funding es neutro contra rivales fuertes" a partir de un panel sin autoridad para decir nada.

**Un panel sirve solo si (a) la base está en zona media y (b) VE una diferencia que sabemos real.** Probé 4 composiciones y las que mezclan un rival DURO + uno PAR + uno FÁCIL quedaron en la zona correcta a −1.7/−1.8σ (les faltaba n, no calidad).

**PANEL OFICIAL validado** (`medicion.panel_oficial()`): **[barnyard + CAMPEONA + RUTERA]**, 45 seeds — base **65.2%** (34.8 pts de margen), `_noop` 65.2% (+0.0σ ✓), `_peor` **50.0% (−2.8σ ✓ discrimina)**. De aquí en adelante el panel se valida ANTES de medir con él.

**Consecuencia sobre las mediciones de hoy:** `funding` (+1.0σ) y `season_aware` (−1.0σ) se midieron en el panel escalera saturado, donde solo había 2.9 puntos de rango — ninguna de las dos lecturas tenía potencia real. Re-medidas con el panel oficial junto al resto de la cuarentena (`work_steal`, `fert_pickup`).

**Lección de método, la más cara de la semana:** durante días optimizamos contra un espejo (que solo mide distancia a nuestro propio óptimo local) o contra bots que ya vencíamos (sin margen). El bot no se estancó por falta de ideas: **el termómetro no distinguía**. Elegir el panel a ojo y descubrir su sesgo después de concluir es el error de fondo; ahora el panel se somete a sus controles primero y el reporte se autodiagnostica.
