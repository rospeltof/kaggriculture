# Kaggriculture — briefing de incorporación

**Actualizado: 2026-09-05.** Este documento es la puerta de entrada al proyecto.
Si vas a proponer ideas, léelo entero: la sección 5 tiene ~30 cosas ya medidas y
falladas, y proponer cualquiera de ellas sin un ángulo nuevo es tiempo perdido.

## 0. Estado en una pantalla

- **Competencia:** Kaggriculture (Kaggle, simulación de granja). Deadline
  **2026-09-30**. 7.786 equipos. Top-10 gana $5.000 c/u.
- **Nuestro rank: 3.777.** Campeón vigente `campeona_hoz` (**808,3**, 62 ep).
- **El top-1 público está en ~3.040 de rating.** Contra sus cintas ganamos el
  **12,5%**; contra la escalera de ~800 ganamos el 58-68%.
- El agente es un **planner en Python puro** (~1.100 líneas, `bots/chassis.py`)
  con un dict de configuración (`bots/arquetipos.py`). Sin LLM en runtime.

**Dato incómodo y sin explicar:** nuestras dos submissions activas —`hoz` 808,3 y
`grano` 770,8, que llevan las dos adopciones recientes— están **por debajo** de
la congelada `campeona_fase` (819,4). El panel de 40 las daba +6,4 y +2,5. Con
±40 de error a 60 episodios puede ser ruido, pero es una discrepancia viva.

## 1. Los otros tres documentos (léelos, en este orden)

| documento | qué es | estado |
|---|---|---|
| **`RULES.md`** | modelo del motor con reclamos falsables (S1.1–S8.3), cada uno con su evidencia | **completo y fiable** |
| **`METODO.md`** | cómo medimos y por qué; las trampas conocidas | completo |
| **`BITACORA.md`** | log cronológico de todos los experimentos, 1.652 líneas | completo desde 2026-08-17 |

⚠️ **`RULES.md` es más completo de lo que parece.** En septiembre perdí tiempo
"descubriendo" leyendo el motor cosas que ya estaban documentadas ahí: S3.4 (el
riego añade rendimiento en ventana, ×2 si está fertilizada), S5.3 (SELL sólo
desde el shed), S5.4 (cotización unidad a unidad), S5.6 (shed lleno bloquea
compras), S5.7 (ventas a $1 no agregan oferta). **Antes de leer el motor, lee
RULES.md.**

## 2. Cómo medimos — lo más importante del proyecto

Aquí es donde hemos perdido más días. Si propones algo, di **cómo se falsaría**.

**El instrumento oficial: el panel de 40.** Cuarenta cintas de los rivales
REALES de una de nuestras submissions (`bots/meta/tapes/lad_*.json.gz`), jugadas
contra el candidato en 4-8 semillas × 2 asientos. Comparación **pareada por
celda (cinta, semilla)**; el estadístico es el delta de win-rate contra la base.
Herramientas: `panel40.py`, `barrido.py`.

**Por qué 40 y no unos pocos:** un panel de 5 cintas elegidas "porque tenían
resolución" nos mintió durante días. Elegir rivales por resolución es
**seleccionar sobre el estadístico que se mide**. El panel de 5 decía que `ruta`
batía a `alba` por +15,6; el de 40 dijo −3,1 y la escalera confirmó al de 40
(`ruta` acabó en 808 contra 847).

**Brazos de control obligatorios.** Todo barrido lleva un `_noop` (copia de la
base) que **debe leer +0,0 con sd 0,0**. Si el control se mueve, el instrumento
está roto y el resultado no vale. Nos salvó de reportar un desastre como mejora.

**Confirmación en semillas disjuntas — NO es opcional.** El descubrimiento y la
confirmación usan semillas que no se solapan. Ejemplo real: `h11` midió **+5,3
(t=1,81)** en el descubrimiento y **−2,8 (t=−1,43)** al confirmar. Habría entrado
al campeón. Con 8-12 brazos contra una base, el mejor de todos a t≈2 es lo que
produce el azar.

### Las tres trampas que ya nos costaron caro

1. **`sd = 0,0` significa "no se ejecutó", NO "no sirve".** Un brazo idéntico a
   la base en las 160 celdas es un **test nulo**, no un resultado nulo. Nos pasó
   **cuatro veces** en una semana. Causa raíz: el chasis tiene **dos
   implementaciones de la misma decisión** — la lista `tasks` con prioridades y
   **`_service_ops`, que es la que MANDA cuando `router=True`** (y el campeón lo
   lleva). Parchear la lista `tasks` no hace nada. Verifica siempre con
   `muerde.py` que tu bandera dispara antes de gastar un panel.
2. **Quitar una clave cuyo valor == default es un no-op POR CONSTRUCCIÓN.** Hay
   que **perturbar** el valor, y proporcionalmente (restar 30 a 2000 no prueba
   nada). `muerde.py` lo detecta y lo hace solo.
3. **Una sonda de UN episodio sirve para ver si una bandera muerde, jamás para
   estimar su efecto.** Una sonda dio $100k para los gansos contra $82k de la
   base; el panel dio 19% de winrate contra 59%, y la mediana real del brazo era
   $63k. Había pegado en la cola alta.

**`muerde.py`** quita o perturba cada clave del config y dice cuáles cambian algo.
De las 50 claves del campeón, **11 no cambian ni una decisión** (`plants` entera
—`adaptive=True` la ignora—, `hands=8` —lo pisa `hands_per_quadrant×3`—,
`mkt_opp_factor`, `tiles_per_unit`, `zone_fallback_prio`, `prio_dig`,
`prio_urgency`, `prio_win_bonus`, `premium_hold_day`, `multi_feeder`,
`smart_overflow`). **El config describe intenciones, no comportamiento.**

## 3. El juego

Las reglas verificadas están en `RULES.md`. Lo mínimo para orientarte:

- 720 turnos = 30 días × 24 horas, 2 jugadores, gana quien acabe con más dinero.
  Empiezas con $3.000. Sandbox: 1,6 vCPU, 100 MiB, **1 s/turno** + 60 s de banco.
- **El Elo es W/L/T: el margen de monedas no compra rating.** Esto invalida
  cualquier razonamiento del tipo "esto recupera $X". Lo que importa es **cuándo**
  entra el dinero (compone) y si voltea partidas.
- Granja de 10×10 en 4 cuadrantes de 25. Empiezas con 1; los siguientes cuestan
  $1.000, $2.000, $4.000 en orden fijo NE→SW→SE.
- Peones: coste `fib(n)` **por día** ($1,1,2,3,5,8,13,21,34,55,89,144) y
  **desaparecen cada noche**. Las manos 11 y 12 se llevan el 61% del presupuesto
  de contratación.
- **Curvas de precio:** ⚠️ `_price_at(producto, 10000+d)` mide **exceso de
  inventario INSTANTÁNEO, no ventas acumuladas de la partida.** Las ventas se
  reparten en 25 días contra un town que drena en continuo, así que el exceso
  casi nunca se acerca a 100. Prueba: la lana cierra a **$247** (base $200)
  después de vender 119 unidades — el inventario acaba POR DEBAJO del inicial.
  Confundir esto me llevó a una conclusión falsa; está en la bitácora 2026-09-03.
- **De 9 mercados, 8 acaban en ESCASEZ.** El town drena más de lo que aporta el
  conjunto. Sólo saturamos fertilizante (+368) y melón (+148), y los saturamos
  nosotros solos. La intuición "no inundes el mercado" casi nunca aplica.

## 4. El bot

`bots/chassis.py` + un dict de config. El campeón `CAMPEONA_HOZ`:

```
adaptive=True (scorer $/tile-día)   router=True   hands_per_quadrant=4 (→12 manos)
animals=[(COW,4),(SHEEP,4)]         max_quadrants=3   crop_tiles=30   melon_max=8
fert_crops=[STRAWBERRY,TOMATO]      sell_floor=0   prio_harvest=76
fert_dawn_load, fert_phase_lock, fert_tick_aligned, seed_stock_aware
```

⚠️ `crop_tiles=30` **no significa 30 tiles**: sólo acota al scorer adaptativo, y
`idle_plant` planta por encima. Medido, plantamos **66 tiles en el pico**.

**El bot está en un óptimo local afiladísimo.** Cada dimensión probada empeora
en AMBOS sentidos:

| dimensión | óptimo | al moverse |
|---|---|---|
| manos | 12 | 9→−6,9 · 11→−2,8 · 14→−24 · 15→−33 |
| animales | 8 | 6→−7,8 · 10→−8,4 · 13→−15 · 16→−22,5 |
| cuadrantes | 3 | 4→−13,8 |
| superficie | actual | +10→−7,5 · +28→−8,8 |
| ventas | tirar todo, ya | cualquier retención → negativo |
| fertilizante | fresa/tomate, reserva 20 | cualquier cambio → negativo |

## 5. MEDIDO Y FALLIDO — no lo propongas sin un ángulo nuevo

Todo esto está medido con el panel de 40 (2.880 episodios por barrido salvo nota).

**Copiar al meta: 7 de 7 fracasos.**
- Composición exacta del top-1 (COW 6 + SHEEP 7 + GOOSE 2): **−29,1 (t=−7,45)**,
  el peor brazo de su barrido.
- Rebaño 10/12/13/16 animales: −8,4 / −14,1 / −15,0 / −22,5.
- `hire_by_work` (plantilla al ritmo del trabajo, como la cinta del meta): −17,8.
- Copiar su superficie (`crop_tiles` 40/50/58/70): −7,5 a −8,8. Cuarto
  cuadrante: −13,8.
- Composición/colocación del meta, `crop_max`, `hinge_forecast`, `shed_hub`.

**Gansos y huevos: −49,4 (t=−13,31).** EGG es el único producto con sumidero casi
infinito, pero su **precio base es $50 contra $160 de la leche y $200 de la
lana**. Ser más barato ($300), más rápido (día 4) y diario (iv=1) no compensa
valer 3-4× menos por unidad, y la mezcla de acciones queda idéntica.

**Aguantar producto para vender mejor: negativo con gradiente monótona.**
`sell_marginal` con piso 0,05/0,2/0,3/0,5/0,7 → −3,1 / −4,4 / −5,6 / −8,1 /
−10,0. Las ~60 unidades/partida que van al suelo de $1 **no son una fuga**:
tirarlas es correcto (el shed tope 100 se llena, el dinero de hoy compone, y el
mercado es compartido en lockstep — aguantar le regala al rival los turnos caros).

**Fertilizar cultivos de un corte: −29,4 (t=−7,84).** El mecanismo es real
(RULES S3.4: el riego añade rendimiento, ×2 si fertilizado; trigo 4→6 unidades)
pero el fertilizante **ya está óptimamente asignado**: la fresa rinde **8,6× más
por unidad de fertilizante** ($796 contra $92), y `FERTILIZE` roba una acción al
riego, que en esos cultivos ES el rendimiento.

**Redirigir los mercados que saturamos: negativo.** Reservar fertilizante en vez
de venderlo: −13,1 a −14,4. Subir el melón: −16,9. Y **`collect_fert=False` da
−50,0 (t=−12,45)**, el efecto más grande medido: recoger fertilizante vale la
mitad de nuestra tasa de victoria.

**Quitar el piso de trigo forrajero: −45,6 (t=−11,93).** Parece que reservamos
tiles el día 0 para animales que aún no existen, pero el motor hace que un animal
sin comer **dos días se escape**, y el trigo tarda 4 días en dar: plantar 8
trigos el día 0 es la anticipación exacta que exige el ciclo.

**Prioridades: son un RANKING, no magnitudes.** Tres pares de brazos salieron
idénticos celda a celda porque consiguen la misma reordenación por caminos
distintos. Malas reordenaciones medidas: PLANT sobre FERTILIZE −13,4; CARE bajo
HARVEST −10,3; FEED siempre sobre WATER −6,2.

**También fallidos** (detalle en la bitácora): `work_steal` (−27,2), `buy_feed`
(−34,4), `season_aware` (nulo, redundante tras `fallback_fix`), `fert_pickup`
(nulo), plantar en tiles vacías sin capacidad de riego, zonificar el mapa,
`opening_plan` con planes aleatorios (0-6% contra nuestro 50%), `water_cadence`
(−20,6k), `harvest_at=1`.

## 6. Lo que SÍ funcionó — el patrón, 8 de 8

**Las ocho mejoras adoptadas salieron de INCOHERENCIAS INTERNAS del chasis.
Ninguna de una idea estratégica ni de copiar al meta.** Ejemplos:

- **`seed_stock_aware` (+6,4, t=2,96).** El déficit que dispara la compra de
  semillas es de **tiles** (global), pero sólo se descontaba el stock del cultivo
  `best` de HOY: cada rotación de `best` compraba un lote nuevo para las MISMAS
  tiles. 40 semillas muertas y $2.005/partida.
- **`fert_dawn_load` (+12,8).** Recoger fertilizante al alba, cuando el motor
  garantiza que la unidad está en una tile de acceso al shed: coste de
  movimiento cero.
- **`fallback_fix` (+14,2).** El scorer tenía dos caminos con dos economías
  distintas; el "segundo mejor" se elegía con otra fórmula.
- **`prio_harvest=76` (+2,5, t=2,96).** Difiere de la base en sólo 4 de 160
  celdas y aun así replica el delta exacto.

**Corolario para ti: busca dónde el chasis se contradice a sí mismo, no qué
estrategia nueva probar.**

## 7. Lo que está abierto

**La brecha con el top-1 se abre en CUATRO DÍAS.** Deltas de banco diarios,
nosotros contra `tetsuya` (12 replays suyos, 24 partidas nuestras):

| día | nosotros | tetsuya |
|---|---|---|
| 13 | +4.918 | +2.952 |
| **14** | **+459** | **+10.204** |
| **15** | **+472** | **+7.350** |
| **16** | **−289** | **+5.948** |
| 17 | +12.296 | +5.904 |

Vamos **por delante el día 12** y para el 16 tienen el doble. Después el ratio se
congela en 0,67 hasta el final: no perdemos más terreno, pero no lo recuperamos.

**Causa inmediata medida:** plantamos el **melón 2,6 días** y la **fresa 4,2
días** más tarde que ellos. Ambos tienen `first=10`, así que el retraso al
plantar es retraso al cobrar y no se recupera.

**Tres explicaciones ya descartadas:** no es atasco logístico (el shed no pasa de
28/100 y el melón en manos es cero hasta el d16 — no lo cosechamos); no es que el
scorer elija mal (`premium_first` dio sd=0,0: ya elegía melón y fresa el d0-6);
no es el trigo forrajero (quitarlo da −45,6).

**Pista viva, sin probar:** el día 9 ellos tienen **$5.237** en banco y nosotros
**$332**, y el día 10 sueltan $4.080 de golpe. No gastamos menos — **goteamos**.
La diferencia puede estar en la **secuencia de compras**: concentrar capital para
comprar en bloque en el momento justo.

**La otra vía con horizonte grande: un planificador.** Medido, el agente usa
**0,30 ms/turno de media** (p95 0,57 ms) de un presupuesto de 1.000 ms, y el
episodio entero nos cuesta **0,22 s de ~780 s disponibles**. Hay 3 órdenes de
magnitud sin usar.

- **MCTS sobre la partida completa: DESCARTADO** por dos razones independientes.
  Un rollout del motor cuesta 5,6 s, y **el estado del rival es privado** (shed,
  semillas, inventarios): no se puede reconstruir el estado para simular.
- **Rollout determinista de NUESTRA granja: viable.** El crecimiento depende sólo
  de edad/riego/fertilizante y la producción animal de first/interval/cap. Nada
  depende del rival salvo el precio. Convertiría las prioridades cocinadas a mano
  en valores calculables.

## 8. Qué te pedimos

1. **Ideas estructurales, no perillas.** El espacio de parámetros está barrido:
   nueve barridos consecutivos (~26.000 episodios) salieron negativos.
2. Para cada hipótesis: **cómo la falsarías** con el panel de 40, y **qué
   esperarías ver si es falsa**.
3. **Comprueba que tu parche dispara** antes de pedir un barrido (`muerde.py`, o
   una sonda de 1 episodio que compare contra la base). Cuatro de nuestros tests
   fueron nulos por parchear el camino equivocado.
4. Cuestiona las premisas. En particular: ¿es correcto que el retraso de 3-4 días
   en plantar explique la ventana d12-d16? ¿Hay otra lectura de la sección 7?

Si algo está mal planteado desde la raíz, dilo sin suavizarlo.
