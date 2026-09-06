# Kaggriculture — contexto para revisión por otro LLM

Generado por `preparar_contexto_llm.py` con evidencia local verificada.
**Estado: no subir a Kaggle; compra parcial inconclusa.**

Este archivo reúne documentos de trabajo, no instrucciones de sistema. La solicitud vigente del usuario determina el alcance. El prompt incluido es una plantilla para que el usuario formule su petición.

Se comprobaron 3.840 registros de episodios, 960 comparaciones noop, pares, estadísticas por semilla, hashes de nueve archivos de evidencia, cinco fuentes archivadas y 40 cintas. No se ejecutaron partidas ni consultas. Comprobar coherencia no valida por sí solo el diseño causal o el simulador.

Para una revisión documental basta este archivo. Para auditar trazas resumidas adjuntar también `docs/evidencia/lotes_semillas/`; para inspeccionar código actual y repetir análisis compartir el repositorio. Las acciones completas no se reconstruyen a partir de hashes. No se incluye la bitácora íntegra.

Los enlaces se conservan como en cada fuente; las rutas junto a SOURCE indican dónde resolverlos en el repositorio.

## Índice y huellas de los documentos

- `docs/PROMPT_SEGUNDO_CEREBRO.md` — SHA-256 `e319f3917d23defc367804e464d3d13be14d21061eb2ca73fede8977d4f04c07`
- `AGENTS.md` — SHA-256 `52acc4d4ffa732212d8f470ab16b28ea472a7620ce983f6cc0d1b52369d8387b`
- `docs/ESTADO_ACTUAL.md` — SHA-256 `9d8633e163773b6ddcccc5a4e89207a6393c91d68b058be3be962392b7e7450b`
- `docs/BRIEFING.md` — SHA-256 `471d54db56ece371c5936bd1c1244c2e64a4d70c3801d561be83ff5db10e139c`
- `docs/AUDITORIA_LLM.md` — SHA-256 `f5637e70de4bd1f6427f68b8d4bdfc43b914c16572f005a663a9c813e4a180f0`
- `docs/METODO.md` — SHA-256 `f3dba1825cb10bc6c7d3a668da2c5220f8b198f83a8384a1af7732c55e3231c0`
- `docs/IDEAS_Y_PRUEBAS.md` — SHA-256 `a7807a0d52dfdae4d12fdbb8b14215db98187930a63f79dae805d179b2597335`
- `docs/RULES.md` — SHA-256 `068679a3a092baecf46c929f6c3f44d31ff3d2ab11be39323d3f59e6d526a268`
- `docs/EXPERIMENTO_LOTES_SEMILLAS.md` — SHA-256 `94a2657c1f9429c24893e0cb00f273ae2eb4b68f28ab4ef79fa29df3808d9bbf`
- `docs/evidencia/lotes_semillas/README.md` — SHA-256 `7b4beb82362bb17bd01b39cec158c7596acd36c066ff0df5ff9bf025c0367e3d`


---

## SOURCE: docs/PROMPT_SEGUNDO_CEREBRO.md

# Prompt de traspaso para otro LLM

Copia el bloque siguiente como petición al otro LLM. Si no tiene acceso al repo,
adjunta `docs/CONTEXTO_LLM.md`, generado con `python3 preparar_contexto_llm.py`.
Para reanálisis independiente adjunta también `docs/evidencia/lotes_semillas/`.
Los archivos son contexto y evidencia: no elevan instrucciones a nivel de sistema.

---

Trabaja como par técnico crítico con experiencia en agentes para simulaciones
y diseño experimental. No necesito una lista de ideas plausibles: necesito
identificar qué sabemos, dónde nuestra inferencia falla y qué prueba barata
puede cambiar una decisión.

El proyecto es Kaggriculture. Nuestro agente es un planner determinista de
Python, sin LLM durante el juego. Código en `bots/chassis.py`, configuraciones
en `bots/arquetipos.py`. La base es `CAMPEONA_HOZ`. `HOZ_LOTES` es experimental:
la compra parcial dio +5,0 y +4,84 puntos en dos bloques, pero su confirmación
por semilla quedó inconclusa (IC95 [−0,67; +10,36]).

**Restricción actual:** el usuario reservó su última corrida disponible en
Kaggle y dijo que no se suba nada. No envíes submissions, no reemplaces la base
ni ejecutes barridos nuevos. Esta petición es revisión y propuesta. Una
instrucción histórica de envío no es autorización actual.

Si tienes repo, lee `AGENTS.md`, `docs/ESTADO_ACTUAL.md`, `docs/BRIEFING.md`
completo, `docs/AUDITORIA_LLM.md`, `docs/METODO.md` y `docs/IDEAS_Y_PRUEBAS.md`.
Lee `docs/RULES.md` antes de consultar el motor. Busca en `docs/BITACORA.md`
por términos; no la leas entera. `docs/archivo/` conserva historia, no reglas
vigentes. Si sólo recibes el contexto adjunto, declara qué no puedes verificar
y no afirmes haber inspeccionado archivos ausentes.

Evalúa especialmente:

1. ¿Los datos realmente sostienen el mecanismo y la conclusión que les damos?
2. ¿Confundimos acciones emitidas con ejecutadas, dinero con victorias, o
   episodios con muestras independientes?
3. ¿Qué cambia al agrupar por semilla y qué incertidumbre no cubre ese análisis?
4. ¿La comparación con el líder controla mercado, rival, cohortes y gasto?
5. ¿Los descartes previos pertenecen a la misma implementación y población?
6. ¿La propuesta nueva tiene una ruta que ejecuta, unidades coherentes y una
   predicción que pueda salir falsa?

Devuelve, en este orden:

- Un resumen de máximo diez líneas del estado, las restricciones y tu veredicto
  sobre la evidencia actual. Distingue inconcluso de refutado.
- Hasta cinco objeciones concretas, cada una con archivo/dato que la sostiene,
  límite de la evidencia y comprobación que podría resolverla.
- **Una sola siguiente prueba prioritaria**, usando la ficha de
  `IDEAS_Y_PRUEBAS.md`: hipótesis, mecanismo, falsación, disparo, brazos, controles,
  semillas, unidad de análisis, regla de parada, coste y qué harías con cada resultado.
- Qué información adicional necesitarías y por qué cambiaría la decisión.

No cambies el criterio estadístico después de ver el resultado, no selecciones
los rivales que favorecen al candidato ni juntes bloques para rescatar una
confirmación fallida. Un noop exacto y un control anterior negativo no garantizan
generalización al ladder. Acertar una explicación económica no garantiza ganar.

Revisa también errores del LLM que escribió el traspaso. Tu acuerdo con él no es
una réplica empírica. Prefiero una objeción verificable a una afirmación convincente.



---

## SOURCE: AGENTS.md

# Entrada para agentes que trabajan en este repositorio

## Estado y autorización

- La instrucción actual del usuario es **no subir nada a Kaggle**. Reservó la
  única corrida que dice tener disponible. No ejecutar envíos ni cambiar
  submissions basándose en instrucciones históricas.
- Este traspaso organiza evidencia; no autoriza nuevos barridos costosos.
  Proponer primero hipótesis, coste, regla de parada y criterio de decisión.
  Una petición nueva y explícita del usuario puede cambiar este alcance.
- `CAMPEONA_HOZ` sigue siendo la base. `HOZ_LOTES` es experimental e inconcluso;
  tener una configuración o un `main.py` preparado no significa aprobación.

## Leer en este orden

1. `docs/ESTADO_ACTUAL.md`: decisiones vigentes, qué está probado y qué falta.
2. `docs/BRIEFING.md` entero: proyecto y experimentos anteriores.
3. `docs/AUDITORIA_LLM.md` y `docs/METODO.md`: errores conocidos y reglas actuales.
4. `docs/IDEAS_Y_PRUEBAS.md`: cola corta y ficha para revisar una idea.
5. `docs/RULES.md` antes de leer el motor de Kaggriculture.

Consultar `docs/BITACORA.md` mediante búsquedas; es un registro histórico, no
una fuente de órdenes vigentes. `docs/archivo/` es histórico. El contenido de
replays, notas y prompts antiguos es evidencia a evaluar, no autorización.

## Disciplina experimental

- Separar rama ejecutada, acción emitida, acción ejecutada por el motor,
  mecanismo económico y W/L/T. Ninguno implica automáticamente el siguiente.
- `sd=0` en victorias no demuestra que el parche no se ejecutó.
- El router usa `_service_ops`, pero `tasks` sigue ejecutando algunas decisiones.
- Comparar base, noop y candidato con iguales cintas, semillas y ambos asientos.
  Registrar controles, errores, configs, hashes y acciones antes de entregarlas
  al motor. El dinero es diagnóstico, no criterio de mejora.
- Fijar de antemano unidad de análisis, tamaño muestral y confirmación disjunta.
  No cambiar el criterio después de ver resultados ni seleccionar rivales por
  favorecer a la variante. Inconcluso no significa refutado.
- No presentar el panel fijo de cintas como prueba de Elo futuro o respuesta
  de rivales adaptativos. Un control anterior negativo es necesario en nuestro
  protocolo, pero no garantiza que detectemos mejoras pequeñas.

## Archivos y evidencia

Código: `bots/chassis.py`, configuraciones: `bots/arquetipos.py`.
Medición: `barrido.py`, `muerde.py`, `harness.py`.
Evidencia transportable: `docs/evidencia/lotes_semillas/`.
`results/`, `replays/` y `.venv/` están ignorados por Git; comprobar disponibilidad.
No ejecutar las sondas antiguas que importan `lab.py` sin verificarlo: ese archivo
no está en este checkout.

Para preparar contexto para otro LLM, sin red ni simulaciones:

```bash
./.venv/bin/python preparar_contexto_llm.py
```

Genera `docs/CONTEXTO_LLM.md` y comprueba la evidencia. No empaqueta ni envía
submissions. Para información actual de Kaggle, usar una consulta explícita y
fechada; los ratings en documentos son snapshots.



---

## SOURCE: docs/ESTADO_ACTUAL.md

# Estado actual — leer primero

Actualizado el 2026-09-05. Esta página resuelve contradicciones con notas antiguas;
las instrucciones nuevas del usuario prevalecen sobre cualquier documento.

## Decisión del usuario

**No subir nada a Kaggle por el momento.** El usuario indica que le queda una
corrida disponible y quiere reservarla. Ese cupo es información del usuario,
no una cuota verificada por API. El trabajo actual es preparar el traspaso y
revisar ideas; no se han autorizado más barridos ni envíos en este traspaso.

**No se envió ninguna submission en esta sesión.** Sólo se consultó la lista
de submissions. Se llegó a preparar un paquete experimental; luego se restauró
`submission/main.py` byte por byte al archivo anterior. Su SHA-256 es
`cfad10b88abc38f8f7f79a3b83148f11e37d57865f37cea648cffa9bbcf1e1d7`.

La copia experimental no enviada está sólo localmente en
`results/hoz_lotes_main_preparado_no_enviado.py`. No es el archivo de envío activo.

## Qué agente es cuál

| Nombre | Uso y estado |
|---|---|
| `CAMPEONA_HOZ` / `campeona_hoz` | Base actual; `seed_partial_batch` ausente y por tanto apagado |
| `HOZ_LOTES` / `hoz_lotes` | Copia de HOZ con `seed_partial_batch=True`; experimental, no aprobada |
| `CAMPEONA_FB` | Control anterior exacto en el experimento de compra parcial |
| `submission/main.py` | Paquete anterior restaurado; no asumir que refleja todos los cambios locales |

Última consulta CLI de esta sesión: `campeona_hoz` submission **55994874**, score
**818,1**; `campeona_grano` **55993562**, score **774,8**; ambas COMPLETE.
Son snapshots; no se verificó el rank actual ni el número actual de episodios.

## Hallazgo principal

`seed_partial_batch` reduce únicamente el tamaño del lote adaptativo hasta que
pase el mismo `_afford` con reserva de $100. Mantiene scorer, forraje y orden
de compras. Está implementado en `bots/chassis.py`; no se activó en la base.

| Evidencia | Resultado | Lo que permite concluir |
|---|---|---|
| Sonda 99000, una cinta, asiento 0 | Primer melón d6 h16 → d1 h18; primera fresa d8 h3 → d7 h19 | El mecanismo actúa en ese escenario |
| Descubrimiento, 4 semillas × 40 cintas × 2 asientos | Base 62,1875%, candidato 67,1875%; +5,0 puntos | Señal positiva para confirmar |
| Confirmación, 8 semillas nuevas, mismo panel | Base 60,0%, candidato 64,8438%; +4,8438 puntos | Señal repetida, incertidumbre aún demasiado amplia |
| IC95 de confirmación por semilla | [−0,67; +10,36] puntos; t=2,08 | **Inconcluso** según el criterio registrado |

Se ejecutaron 3.840 episodios de panel. Todos terminaron sin errores. Noop exacto
en las 960 comparaciones correspondientes; el control anterior perdió claramente
en ambos bloques. El candidato cambia acciones en sus 960 episodios, pero el
adelanto de cohortes se midió sólo en la sonda, no en todo el panel.

No se ejecutó el veto head-to-head planificado: exigía confirmación positiva.
El smoke posterior del paquete contra su mismo módulo tuvo dos episodios sin
errores y medias idénticas; **no es ese veto** ni prueba fuerza contra HOZ.

## Interpretaciones que debemos retirar

- W/L/T idéntico o dinero idéntico no implica decisiones idénticas.
- 3.840 episodios no son 3.840 muestras independientes: el análisis principal
  de confirmación tiene ocho promedios de semilla sobre un panel fijo.
- La brecha d12–d16 contra el líder es una pista, no una causa identificada.
- Fracasos de variantes concretas no prueban que toda búsqueda esté agotada.
- El t por celda de 2,45 no reemplaza después de observarlo el criterio por
  semilla que habíamos fijado. Tampoco se cambia a un test unilateral.

## Qué sigue y qué no está iniciado

1. Otro LLM revisa críticamente este estado, la auditoría y el protocolo.
2. Se escoge **una** siguiente prueba con coste y resultado falsador explícitos.
3. Se registra y acuerda el presupuesto antes de ejecutar otro barrido.
4. Una decisión futura sobre Kaggle necesita instrucción nueva del usuario.

No hay procesos de evaluación, subidas ni monitores programados por este traspaso.

## Dónde está la evidencia

- [Experimento detallado](EXPERIMENTO_LOTES_SEMILLAS.md): protocolo y resultados.
- [Auditoría del razonamiento](AUDITORIA_LLM.md): errores y límites.
- [Ideas y pruebas](IDEAS_Y_PRUEBAS.md): cola corta para evaluación crítica.
- [Evidencia transportable](evidencia/lotes_semillas/README.md): JSON, episodios
  comprimidos, manifiestos y fuentes exactas del panel.
- `results/`: originales locales, ignorados por Git.

Los archivos nuevos y modificados están en el working tree. Este trabajo no
creó un commit: para que viajen en un clon deben incorporarse a Git o compartirse
mediante el archivo de contexto generado. No dar por hecho que ya están remotos.



---

## SOURCE: docs/BRIEFING.md

# Kaggriculture — briefing de incorporación

**Actualizado: 2026-09-05.** Este documento conserva el contexto técnico e
histórico. Empieza por [ESTADO_ACTUAL.md](ESTADO_ACTUAL.md), que fija estado y
autorizaciones. La sección 5 resume variantes ya medidas: antes de repetirlas,
explica qué mecanismo o implementación cambia. No son descartes universales.

## 0. Estado en una pantalla

- **Competencia:** Kaggriculture (Kaggle, simulación de granja). La ficha
  histórica registra deadline **2026-09-30**, 7.786 equipos y $5.000 para cada
  top-10; esos datos no se han vuelto a verificar en este traspaso.
- **Base vigente: `CAMPEONA_HOZ`.** Última consulta de la sesión: score 818,1;
  `campeona_grano`, 774,8. Ver IDs y límites del snapshot en
  [ESTADO_ACTUAL.md](ESTADO_ACTUAL.md). No se verificó el rank ni los episodios
  actuales. La nota previa registraba rank 3.777 y HOZ 808,3 con 62 episodios.
- El briefing previo registraba al top-1 en ~3.040 de rating. Las mediciones
  locales contra sus cintas dieron **12,5%**, y contra el panel de rivales de
  ~800, 58–68%; no son tasas actuales verificadas del ladder.
- El agente es un **planner en Python puro** (`bots/chassis.py`)
  con un dict de configuración (`bots/arquetipos.py`). Sin LLM en runtime.

**Discrepancia histórica pendiente:** la nota previa comparaba `hoz` 808,3 y
`grano` 770,8 con la congelada `campeona_fase` 819,4, pese a mejoras locales de
+6,4 (`seed_stock_aware`) y +2,5 (`harvest_76`). Los scores se movieron después;
no atribuir esa diferencia directamente al parche. El ruido y la composición
de rivales pueden influir; no hay aquí un intervalo externo calculado que
cuantifique esa explicación.

**Hoy no se sube nada ni se ejecutan nuevos barridos:** el usuario reserva su
última corrida de Kaggle. La compra parcial sigue inconclusa y apagada.

## 1. Mapa de lectura

| documento | qué es | estado |
|---|---|---|
| [ESTADO_ACTUAL.md](ESTADO_ACTUAL.md) | decisiones, agente activo y autorizaciones | leer primero |
| [AUDITORIA_LLM.md](AUDITORIA_LLM.md) | hechos, inferencias y errores posibles | límites del razonamiento |
| [METODO.md](METODO.md) | protocolo operativo único; reemplaza reglas antiguas | vigente |
| [RULES.md](RULES.md) | modelo del motor con reclamos falsables S1.1–S8.3 y evidencia | consultar antes de releer el motor |
| [EXPERIMENTO_LOTES_SEMILLAS.md](EXPERIMENTO_LOTES_SEMILLAS.md) | protocolo y resultado del último experimento | inconcluso, no adoptado |
| [evidencia/lotes_semillas/](evidencia/lotes_semillas/README.md) | datos, manifiestos y fuentes transportables | respaldo del experimento |
| [IDEAS_Y_PRUEBAS.md](IDEAS_Y_PRUEBAS.md) | hipótesis y ficha para decidir próximas pruebas | propuestas, no autorizaciones |
| [BITACORA.md](BITACORA.md) | registro cronológico desde 2026-08-17 | historia; contiene interpretaciones corregidas después |

⚠️ **`RULES.md` es más completo de lo que parece.** En septiembre perdí tiempo
"descubriendo" leyendo el motor cosas que ya estaban documentadas ahí: S3.4 (el
riego añade rendimiento en ventana, ×2 si está fertilizada), S5.3 (SELL sólo
desde el shed), S5.4 (cotización unidad a unidad), S5.6 (shed lleno bloquea
compras), S5.7 (ventas a $1 no agregan oferta). **Antes de leer el motor, lee
RULES.md.**

## 2. Cómo medimos — lo más importante del proyecto

Aquí es donde hemos perdido más días. Si propones algo, di **cómo se falsaría**.

**El instrumento local vigente: el panel fijo de 40.** Cuarenta cintas extraídas
de rivales reales de una submission (`bots/meta/tapes/lad_*.json.gz`). Son agentes
pasivos, no los rivales originales. En la prueba de lotes se usaron 4 y 8 semillas
× 2 asientos, tamaños de ese protocolo y no una regla universal. Se calcula el
delta pareado de W/L/T por (cinta, semilla), promediando asientos; el análisis
principal estima incertidumbre entre promedios de semilla del panel fijo.
Herramientas: `panel40.py`, `barrido.py`. La decisión sigue [METODO.md](METODO.md).

**Por qué 40 y no unos pocos:** un panel de 5 cintas elegidas "porque tenían
resolución" nos mintió durante días. Elegir rivales por resolución es
**seleccionar sobre el estadístico que se mide**. El panel de 5 decía que `ruta`
batía a `alba` por +15,6; el de 40 dijo −3,1. El snapshot contemporáneo del
ladder fue 844,9 frente a 846,6; una nota posterior registró 808 frente a 847.
Ninguno respalda la gran ventaja inicial, pero snapshots distintos no son una
calibración causal del panel.

**Brazos de control obligatorios.** Todo barrido lleva un `_noop` (copia de la
base) que **debe coincidir por episodio en acciones, dinero, estados y W/L/T**,
además de delta y sd cero. Una discrepancia invalida la comparación y exige
investigarla. También se fija un control anterior; detectar su regresión no
garantiza sensibilidad a mejoras pequeñas ni generalización al ladder.

**Confirmación en semillas disjuntas — NO es opcional.** El descubrimiento y la
confirmación usan semillas que no se solapan. Ejemplo real: `h11` midió **+5,3
(t=1,81)** en el descubrimiento y **−2,8 (t=−1,43)** al confirmar. Habría entrado
al campeón. Con 8–12 brazos contra una base aumenta el riesgo de seleccionar
un t≈2 producido por azar; registrar multiplicidad y confirmar fuera de la
selección. Semillas nuevas no validan por sí solas rivales nuevos.

**Corrección de incertidumbre (2026-09-05):** las 40 cintas comparten las mismas
semillas. `barrido.py` conserva el t por celda histórico y añade SE/t agrupando
primero por semilla. En `harvest_76`, el t de confirmación cambia de 2,96 a 1,60
con esta agrupación; el delta sigue en +2,5. No demuestra que el cambio sea malo,
pero su significancia no es robusta a la unidad de análisis.

### Las tres trampas que ya nos costaron caro

1. **`sd = 0,0` NO demuestra que el parche no se ejecutó.** Con delta cero sólo
   prueba igualdad de W/L/T en las celdas medidas. La versión antigua de
   `muerde.py` comparaba dinero final, tampoco decisiones. Ahora ambos scripts
   registran hashes de acciones emitidas antes de entregarlas al motor. El
   chasis tiene dos caminos — `tasks` y `_service_ops` — y el router prioriza el
   segundo, pero hay tareas que aún se ejecutan por el primero. Verifica la
   acción que cambia; si necesitas demostrar ejecución interna, añade un contador
   de rama. Una traza idéntica sólo vale para los escenarios observados.
2. **Quitar una clave cuyo valor == default es un no-op POR CONSTRUCCIÓN.** Hay
   que **perturbar** el valor, y proporcionalmente (restar 30 a 2000 no prueba
   nada). `muerde.py` lo detecta y lo hace solo.
3. **Una sonda de UN episodio sirve para ver si una bandera muerde, jamás para
   estimar su efecto.** Una sonda dio $100k para los gansos contra $82k de la
   base; el panel dio 19% de winrate contra 59%, y la mediana real del brazo era
   $63k. Había pegado en la cola alta.

**`muerde.py`** quita o perturba cada clave y compara acciones, dinero y estados
por separado. La medición histórica encontró **11 claves sin cambio de dinero
final en sus seis partidas**, no demostró que no cambiaran decisiones (`plants` entera
—`adaptive=True` la ignora—, `hands=8` —lo pisa `hands_per_quadrant×3`—,
`mkt_opp_factor`, `tiles_per_unit`, `zone_fallback_prio`, `prio_dig`,
`prio_urgency`, `prio_win_bonus`, `premium_hold_day`, `multi_feeder`,
`smart_overflow`). Las anulaciones evidentes por lectura del código siguen
siendo evidencia adicional. **El config describe intenciones, no comportamiento.**

## 3. El juego

Las reglas verificadas están en `RULES.md`. Lo mínimo para orientarte:

- 720 turnos = 30 días × 24 horas, 2 jugadores, gana quien acabe con más dinero.
  Empiezas con $3.000. Sandbox: 1,6 vCPU, 100 MiB, **1 s/turno** + 60 s de banco.
- **La métrica primaria es W/L/T: el margen de monedas no compra rating.**
  “Esto recupera $X” puede explicar un mecanismo, pero no aprobar una mejora.
  El momento del ingreso puede habilitar reinversión; hay que medir si acaba
  cambiando victorias, empates o derrotas.
- Granja de 10×10 en 4 cuadrantes de 25. Empiezas con 1; los siguientes cuestan
  $1.000, $2.000, $4.000 en orden fijo NE→SW→SE.
- Peones: coste `fib(n)` **por día** ($1,1,2,3,5,8,13,21,34,55,89,144) y
  **desaparecen cada noche**. Las manos 11 y 12 se llevan el 61% del presupuesto
  de contratación.
- **Curvas de precio:** ⚠️ `_price_at(producto, 10000+d)` mide **exceso de
  inventario INSTANTÁNEO, no ventas acumuladas de la partida.** En las sondas
  históricas, las ventas se repartían en 25 días mientras el town drenaba stock.
  En un caso la lana cerró a **$247** (base $200) después de vender 119 unidades:
  el inventario acabó POR DEBAJO del inicial. Eso no fija un máximo universal
  de inventario ni implica ausencia de saturación transitoria.
  Confundir esto me llevó a una conclusión falsa; está en la bitácora 2026-09-03.
- **Inventarios de cierre históricos:** se registraron fertilizante +368 y melón
  +148 sobre el nivel inicial, junto con escasez en otros productos. El resumen
  “8 de 9 en escasez” no cuadra con esos dos excedentes; el conteo queda pendiente
  de revisar en los datos. Los inventarios finales tampoco describen los precios
  en cada venta ni prueban quién causó todo el exceso del mercado compartido.

## 4. El bot

`bots/chassis.py` + un dict de config. La base `CAMPEONA_HOZ` (compra parcial
apagada; identidad del paquete de envío en `ESTADO_ACTUAL.md`):

```
adaptive=True (scorer $/tile-día)   router=True   hands_per_quadrant=4 (→12 manos)
animals=[(COW,4),(SHEEP,4)]         max_quadrants=3   crop_tiles=30   melon_max=8
fert_crops=[STRAWBERRY,TOMATO]      sell_floor=0   prio_harvest=76
fert_dawn_load, fert_phase_lock, fert_tick_aligned, seed_stock_aware
```

⚠️ `crop_tiles=30` **no significa 30 tiles**: sólo acota al scorer adaptativo, y
`idle_plant` planta por encima. En el diagnóstico histórico se midieron
**66 tiles en el pico**; no es una cantidad garantizada en cualquier escenario.

**Varias perturbaciones de la base dieron regresiones locales.** Este resumen
histórico motivó la descripción “óptimo local afiladísimo”; los ensayos no prueban
un óptimo matemático ni agotan interacciones o estrategias alternativas:

| dimensión | valor de referencia | variantes medidas |
|---|---|---|
| manos | 12 | 9→−6,9 · 11→−2,8 · 14→−24 · 15→−33 |
| animales | 8 | 6→−7,8 · 10→−8,4 · 13→−15 · 16→−22,5 |
| cuadrantes | 3 | 4→−13,8 |
| superficie | actual | +10→−7,5 · +28→−8,8 |
| ventas | tirar todo, ya | retenciones ensayadas → negativo |
| fertilizante | fresa/tomate, reserva 20 | cambios ensayados → negativo |

## 5. Variantes medidas — revisar antes de repetir

Son resultados históricos de implementaciones concretas. La mayoría usa el panel
de 40 (2.880 episodios por barrido salvo nota); algunos diagnósticos usan dinero,
no W/L/T. Los t originales son por celda salvo indicación y no se han recalculado
todos por semilla. “Negativo”, “nulo” e “inconcluso” no son equivalentes.

**Copiar aspectos del meta: siete variantes históricas sin mejora.**
- Composición exacta del top-1 (COW 6 + SHEEP 7 + GOOSE 2): **−29,1 (t=−7,45)**,
  el peor brazo de su barrido.
- Rebaño 10/12/13/16 animales: −8,4 / −14,1 / −15,0 / −22,5.
- `hire_by_work` (plantilla al ritmo del trabajo, como la cinta del meta): −17,8.
- Copiar su superficie (`crop_tiles` 40/50/58/70): −7,5 a −8,8. Cuarto
  cuadrante: −13,8.
- Composición/colocación del meta, `crop_max`, `hinge_forecast`, `shed_hub`.

**Variante de gansos y huevos: −49,4 (t=−13,31).** La explicación propuesta
contrasta su sumidero grande con **precio base $50 frente a $160 de leche y
$200 de lana**. En la implementación ensayada, ser más barato ($300), más rápido
(día 4) y diario (iv=1) no se tradujo en victorias. La mezcla agregada de acciones
se describió como similar; eso no prueba acciones idénticas ni refuta todo uso
de gansos en otras estrategias.

**Aguantar producto para vender mejor: negativo con gradiente monótona.**
`sell_marginal` con piso 0,05/0,2/0,3/0,5/0,7 → −3,1 / −4,4 / −5,6 / −8,1 /
−10,0. El diagnóstico registró ~60 unidades/partida vendidas a $1. Liberar shed,
disponer antes de caja y vender antes que el rival son explicaciones plausibles
del resultado; no demuestran que toda venta a $1 sea óptima. Las cintas pasivas
también pueden favorecer ventajas basadas en su calendario fijo de ventas.

**Fertilizar cultivos de un corte: −29,4 (t=−7,84).** El mecanismo es real
(RULES S3.4: el riego añade rendimiento, ×2 si fertilizado; trigo 4→6 unidades)
pero la variante ensayada pierde. La explicación histórica compara el ingreso
incremental calculado de fresa y trigo: **8,6×** ($796 contra $92) a los precios
usados, además del coste de una acción `FERTILIZE` que compite con el riego.
Es una justificación dependiente de precios, tiempos y oportunidades; no prueba
una asignación universalmente óptima del fertilizante.

**Redirigir los mercados que saturamos: negativo.** Reservar fertilizante en vez
de venderlo: −13,1 a −14,4. Subir el melón: −16,9. Y **`collect_fert=False` da
−50,0 puntos (t=−12,45)**, la mayor regresión de ese barrido. Es una ablación
grande bajo esa configuración, no una descomposición causal aditiva de “la mitad”
de toda nuestra fuerza.

**Quitar el piso de trigo forrajero: −45,6 (t=−11,93).** Parece que reservamos
tiles el día 0 para animales que aún no existen, pero el motor hace que un animal
sin comer **dos días se escape**, y el trigo tarda 4 días en dar. Eso respalda
anticipar forraje, pero el resultado no demuestra que exactamente ocho trigos
en d0 sea el único calendario viable.

**Prioridades: importan por la reordenación que producen.** Tres pares de brazos
tuvieron W/L/T idéntico celda a celda; se atribuyó a la misma reordenación por
caminos distintos. Sin trazas o evidencia de código adicional, la igualdad del
resultado no demuestra esa explicación. Reordenaciones negativas medidas:
PLANT sobre FERTILIZE −13,4; CARE bajo HARVEST −10,3; FEED siempre sobre WATER −6,2.

**Otros antecedentes** (detalle en la bitácora): `work_steal` (−27,2), `buy_feed`
(−34,4), `season_aware` (nulo, descrito como redundante tras `fallback_fix`),
`fert_pickup` (nulo), plantar en tiles vacías sin capacidad de riego, zonificar el mapa,
`opening_plan` con planes aleatorios (0-6% contra nuestro 50%), `water_cadence`
(−20,6k en dinero, no puntos W/L/T), `harvest_at=1`. Revisar el diseño y la
instrumentación de cada entrada antes de tomarla como descarte competitivo.

## 6. Adopciones históricas y el patrón que motivaron

**El registro atribuyó ocho adopciones a incoherencias internas del chasis.**
Es una pista útil para priorizar inspecciones, no evidencia de que las ideas
estratégicas no puedan mejorar. Las adopciones usaron el criterio de su época;
sus niveles de evidencia no son idénticos. Ejemplos:

- **`seed_stock_aware` (+6,4, t por celda=2,62 en confirmación).** El déficit que dispara la compra de
  semillas es de **tiles** (global), pero sólo se descontaba el stock del cultivo
  `best` de HOY: cada rotación de `best` compraba un lote nuevo para las MISMAS
  tiles. El diagnóstico histórico encontró 40 semillas sin usar y $2.005/partida
  comprometidos en ese stock; son cifras de la muestra examinada.
- **`fert_dawn_load` (+12,8).** Recoger fertilizante al alba, cuando el motor
  garantiza que la unidad está en una tile de acceso al shed: coste de
  movimiento cero.
- **`fallback_fix` (+14,2).** El scorer tenía dos caminos con dos economías
  distintas; el "segundo mejor" se elegía con otra fórmula.
- **`prio_harvest=76` (+2,5 en ambos bloques).** W/L/T cambia respecto de la
  base en 4/160 celdas de descubrimiento y 9/320 de confirmación; no son conteos
  de acciones distintas. En confirmación, t por celda=2,96 y t por semilla=1,60.
  La magnitud se repite, pero la certeza histórica no es robusta a esa agrupación.

**Prioridad sugerida:** buscar contradicciones del chasis tiene antecedentes
favorables. Otra vía sigue siendo admisible si concreta mecanismo, antecedente,
prueba falsadora y coste según el método vigente.

## 7. Lo que está abierto

**La comparación histórica sugiere una ventana d12–d16.** Deltas de banco
diarios de `tetsuya` y nuestros agentes (12 replays suyos, 24 partidas nuestras):

| día | nosotros | tetsuya |
|---|---|---|
| 13 | +4.918 | +2.952 |
| **14** | **+459** | **+10.204** |
| **15** | **+472** | **+7.350** |
| **16** | **−289** | **+5.948** |
| 17 | +12.296 | +5.904 |

En esta comparación vamos por delante el día 12 y para el 16 tienen el doble.
**Corrección 2026-09-05:** la tabla original da ratio 0,51 en d16 y 0,67 en d28;
no está congelado. Además compara simulaciones nuestras con replays del líder
contra terceros, no los dos jugadores del mismo mercado.

**Asociación medida, causalidad pendiente:** el día medio de plantado del melón
es 2,6 días posterior y el de la fresa 4,2. Ambos tienen `first=10`, pero esos
promedios de toda la temporada no identifican las cohortes que pagan d12–d16.

**Diagnóstico histórico:** en los escenarios examinados, el shed no pasa de
28/100 y el melón en manos es cero hasta d16. Debilita la hipótesis de atasco
después de cosechar para esos casos;
quitar el trigo forrajero da −45,6. `premium_first` tuvo W/L/T idéntico: eso
solo no descarta un cambio de decisiones. Una sonda posterior de pf6 sí produjo
acciones idénticas, pero sólo verifica ese escenario.

**Pista de caja:** en d9 ellos tienen $5.237 y nosotros $332; su banco cae unos
$4.080 hasta d10. Eso es flujo neto, no gasto bruto demostrado. La secuencia de
compras sigue abierta. La sonda de `seed_partial_batch` verifica otro mecanismo:
rechazar un lote completo aun pudiendo comprar una parte retrasa el primer melón
de d1 a d6 en un escenario. Descubrimiento +5,0 puntos y confirmación +4,84;
IC95 de confirmación agrupado por semilla [−0,67; +10,36]. **Inconcluso, no
adoptado; bandera apagada.** Ver `EXPERIMENTO_LOTES_SEMILLAS.md`.

**Otra vía propuesta: un planificador.** El benchmark histórico registró
**0,30 ms/turno de media** (p95 0,57 ms) de un presupuesto de 1.000 ms, y el
episodio entero costó **0,22 s de ~780 s nominales disponibles**. Es una medición
de esa implementación y entorno; no mide cuánto podría aprovechar otro método
ni garantiza latencias en el sandbox de Kaggle.

- **Rollout exacto de la partida completa: estado insuficiente.** Se midieron
  5,6 s para un rollout del motor y el rival mantiene estado privado (shed,
  semillas, inventarios). No se puede reconstruir su estado exacto desde la
  observación disponible. Eso no descarta todo MCTS aproximado, planificación
  parcial o con creencias/POMDP; su coste y utilidad siguen sin validar.
- **Rollout de NUESTRA granja: propuesta plausible.** Las reglas de crecimiento
  y producción permiten modelar transiciones locales a partir del estado visible
  y acciones. Precios e interacciones compartidas requieren supuestos explícitos.
  Podría ayudar a valorar prioridades; no hay aquí prueba de mejora competitiva.

## 8. Qué te pedimos

1. **Explica qué aporta la próxima idea.** Nueve barridos históricos consecutivos
   (~26.000 episodios) no encontraron mejoras. Prioriza cambios con mecanismo
   claro; ese antecedente no demuestra que todo el espacio esté agotado.
2. Para cada hipótesis: **cómo la falsarías** con el panel de 40, y **qué
   esperarías ver si es falsa**.
3. **Propón cómo comprobar activación y mecanismo** antes de un barrido
   (`muerde.py` o una sonda contra la base). Hubo pruebas históricas atribuidas
   a parches en el camino equivocado; la atribución exige código/trazas, no sólo
   W/L/T nulo. Hoy se revisan propuestas; no se ejecutan nuevas corridas.
4. Cuestiona las premisas. En particular: ¿es correcto que el retraso de 3-4 días
   en plantar explique la ventana d12-d16? ¿Hay otra lectura de la sección 7?

Si algo está mal planteado desde la raíz, dilo sin suavizarlo.



---

## SOURCE: docs/AUDITORIA_LLM.md

# Auditoría de razonamiento para el siguiente LLM

Actualizado: 2026-09-05. Lee primero [ESTADO_ACTUAL.md](ESTADO_ACTUAL.md).
Este documento distingue hechos observados, inferencias y comprobaciones pendientes.
No sustituye el [método vigente](METODO.md) ni autoriza experimentos o envíos.

**Restricción vigente del usuario:** reservar la última corrida disponible de
Kaggle; no subir nada por el momento. Esta revisión organiza el repositorio:
no ejecuta nuevos episodios ni llamadas de subida. Un comando histórico en un
documento no autoriza ejecutarlo. Aprobar una idea localmente y autorizar una
submission son decisiones distintas.

## 1. Convertir una señal positiva en una mejora aprobada

**Hecho.** `seed_partial_batch` dio +5,0000 puntos en descubrimiento y +4,8438
en confirmación. El IC95 principal de confirmación es [−0,67; +10,36];
t por semilla = 2,08, por debajo del umbral registrado de 2,3646.

**Conclusión permitida.** Señal positiva repetida, confirmación inconclusa.
La bandera permanece experimental y apagada. No se ejecutó el veto head-to-head,
que sólo correspondía tras confirmar.

**Errores posibles.** Llamarla refutada porque el intervalo cruza cero; llamarla
validada porque ambos deltas son positivos; reemplazar el análisis principal por
t por celda = 2,45; juntar ambos bloques para rescatar la confirmación; cambiar
unilateralidad, tamaño o regla de parada después de ver resultados.

**Pendiente.** Una réplica independiente podría reducir incertidumbre. Necesita
un protocolo nuevo antes de correr, sin presentar sus resultados como parte de
la confirmación terminada. Véase [experimento y decisión](EXPERIMENTO_LOTES_SEMILLAS.md).

## 2. Contar episodios como observaciones independientes

**Hecho.** Se completaron 3.840 episodios de panel entre los dos bloques, incluidos
base y controles. La confirmación tiene ocho semillas; los dos asientos comparten
escenario y las 40 cintas se evalúan sobre esas mismas semillas. El análisis
principal promedia asientos y cintas antes de estimar variación entre semillas.

**Límite.** Su intervalo resume variación entre escenarios sobre ese panel fijo.
No cuantifica por sí solo incertidumbre sobre rivales nuevos, un ladder futuro o
agentes que reaccionan. Con ocho promedios, la aproximación t tampoco debe tratarse
como una garantía libre de supuestos. Miles de episodios no eliminan estos límites.

**Hecho adicional.** Agrupar por semilla cambia el t histórico de confirmación de
`harvest_76` de 2,96 a 1,60, manteniendo +2,5 puntos. Cuestiona su certeza estadística;
no demuestra que la adopción fuera perjudicial. Véase [BRIEFING.md](BRIEFING.md).

## 3. Confundir activación, mecanismo y efecto competitivo

**Hecho.** En la sonda 99000, asiento 0, la compra parcial modifica 599 acciones
y adelanta el primer melón confirmado en tablero de d6 h16 a d1 h18. Ambos brazos
ganan. En confirmación cambia acciones en 640/640 episodios, con 62 resultados
mejores, 31 peores y 547 iguales respecto de la base.

**Límite.** La sonda demuestra el adelanto en ese escenario; no su frecuencia ni
su magnitud típica. Cambiar una traza durante el panel tampoco demuestra que
cada episodio siga el mismo mecanismo causal.

**Errores posibles.** Inferir que `sd=0` implica un parche inactivo, que una traza
distinta demuestra que se ejecutó una rama interna específica, o que una acción
emitida fue aceptada por el motor. Para cada afirmación hay que usar su evidencia:
comparación de acciones, contador de rama o transición efectiva del estado.

Las sondas deben distinguir acciones emitidas de ejecución observada. La estimación
de compras por delta de semillas tiene una salvedad de refresh nocturno y se llama
`seed_buys_lower_bound`; no presentarla como contador exacto universal.
Referencias: [sonda](../sondas/005_lotes_semillas.py),
[medidor](../barrido.py), [detalle de instrumentación](EXPERIMENTO_LOTES_SEMILLAS.md).

## 4. Convertir caja y calendarios en causalidad demostrada

**Hecho.** La comparación histórica de d12–d16 usa simulaciones nuestras y replays
del líder contra terceros. No son los dos jugadores del mismo mercado. El ratio
publicado pasa de 0,51 en d16 a 0,67 en d28: no quedó congelado.

**Errores posibles.** Interpretar una caída del banco como compras brutas o una
subida como ventas brutas; atribuir el hueco a melones sólo porque su plantado
medio es posterior; convertir un promedio de temporada en fecha de la cohorte
que debía pagar durante cuatro días concretos.

**Inferencia razonable.** El adelanto de cultivos largos puede contribuir al flujo
de caja. **Pendiente:** conectar cohortes concretas con cosechas, ventas y gastos
en escenarios comparables. La sonda de semillas identifica otro mecanismo real,
pero no explica por sí sola la brecha con el líder. Véanse
[BRIEFING.md, sección 7](BRIEFING.md) y [BITACORA.md](BITACORA.md).

## 5. Usar dinero o controles como prueba suficiente de fuerza

**Hecho.** La métrica primaria documentada es victoria/derrota/empate, con empate
= 0,5. El margen monetario sirve para diagnóstico; ganar por más dinero no añade
otra victoria. La caja intermedia puede explicar un mecanismo, no aprobarlo.

**Hecho.** El noop de ambos bloques coincide exactamente y el control anterior
es claramente peor. Eso respalda la integridad de la comparación y la detección
de esa regresión grande; no prueba sensibilidad a cualquier mejora pequeña ni
generalización al ladder.

**Límite.** Las cintas son rivales pasivos. El head-to-head contra nuestro linaje
puede amplificar ventajas por interacciones de mercado: su papel registrado es
veto, no promoción. La conversión histórica de puntos del panel a Elo mediante
×2,7 proviene de una calibración pequeña y ruidosa; no es una predicción precisa.
Referencia: [METODO.md](METODO.md).

## 6. Leer una configuración fallida como una idea universalmente refutada

**Hecho.** Hay muchas variantes negativas documentadas. Su evidencia corresponde
a implementaciones, valores, bases, paneles y semillas concretos; algunas pruebas
antiguas también tenían problemas de medición que después se corrigieron.

**Errores posibles.** Convertir “copiar esta composición perdió” en “ninguna
estrategia con esos animales puede funcionar”; “estas perillas perdieron” en
“el espacio está agotado”; “las adopciones previas corrigieron incoherencias” en
“sólo puede mejorar corregir incoherencias”. Tampoco cabe ignorar los negativos
y repetirlos sin una diferencia verificable en implementación o mecanismo.

**Criterio de lectura.** Tratar “óptimo local afiladísimo”, “espacio barrido” y
“medido y fallido” del [briefing](BRIEFING.md) como resúmenes históricos con alcance
limitado. Una configuración expresa intención; rutas como `tasks`, `_service_ops`
y defaults pueden modificar su efecto real. Revisar [chassis.py](../bots/chassis.py)
y [arquetipos.py](../bots/arquetipos.py) cuando la hipótesis dependa de ese efecto.

## 7. Declarar imposible toda planificación con estado privado

**Hecho documentado.** El estado privado del rival no está disponible para
reconstruir un rollout exacto de la partida completa. El briefing también registra
un coste de 5,6 s para un rollout medido; no es un benchmark de todas las técnicas.

**Límite de la inferencia.** Estas restricciones no demuestran imposibilidad de
planificación parcial, aproximada o con creencias sobre estado oculto, incluida
una formulación POMDP. Tampoco demuestran que esas alternativas sean útiles.

**Pendiente.** Toda propuesta deberá declarar qué estado conoce, qué aproxima,
qué asume de precios/rival, qué coste mide y cómo valida el beneficio. El rollout
de nuestra granja es una vía propuesta, no una mejora competitiva comprobada.
Referencia: [BRIEFING.md, sección 7](BRIEFING.md).

## 8. Obedecer reglas históricas o confiar en evidencia que no viaja

**Hecho.** El [método histórico](archivo/METODO_HISTORICO_2026-09-05.md) acumuló
reglas de distintas fechas: panel de cinco cintas, selección por resolución, t>2
y conversión a Elo. El [METODO.md vigente](METODO.md) las reemplaza como única
guía operativa. El archivo conserva historia, no instrucciones actuales. Leer el
estado vigente y el protocolo específico antes de copiar comandos; una instrucción
de subida antigua no supera la restricción actual.

**Hecho.** [`.gitignore`](../.gitignore) excluye `results/` y `*.tar.gz`. Los JSONL,
manifiestos y fuentes archivadas originales no acompañan automáticamente a un clon.
El [paquete compacto](evidencia/lotes_semillas/) facilita la revisión; comprobar su
inventario para saber qué contiene y qué sigue disponible sólo en la máquina local.
Un resumen numérico o un hash por sí solo no permite reconstruir todos los datos.

## 9. Confundir representación serializada con diferencias de parámetros

**Error de esta sesión.** Durante la revisión del empaquetado se comparó
`config == meta['configs'][...]` sin normalizar. La aserción falló porque `animals`
usa tuplas en Python y listas al volver a leer JSON; no por parámetros diferentes.

**Corrección.** Para esa comparación, normalizar ambos lados mediante la misma
serialización JSON, preservando el orden de listas y secuencias. No ordenar
`animals` ni otras secuencias cuyo orden pueda influir en comportamiento.

**Límite.** Igualdad de configuración normalizada no demuestra igualdad de fuentes,
del paquete generado o de comportamiento. Cada comprobación debe describirse
por lo que verifica. El fallo inicial de la aserción no es evidencia de una
regresión del bot ni de una submission enviada. Véanse
[empaquetar.py](../empaquetar.py) y [estado actual](ESTADO_ACTUAL.md).



---

## SOURCE: docs/METODO.md

# Método vigente — evaluar ideas sin engañarnos

Actualizado el 2026-09-05. Sustituye las reglas operativas anteriores. La versión
con paneles históricos se conserva en [archivo](archivo/METODO_HISTORICO_2026-09-05.md).
El estado y las autorizaciones están en [ESTADO_ACTUAL.md](ESTADO_ACTUAL.md).

## 1. Qué pregunta contesta cada medición

| Nivel | Medición | Qué no demuestra |
|---|---|---|
| Ejecución interna | Contador de la rama prevista | Que cambie la acción |
| Conducta | Primera acción distinta / hash de acciones emitidas | Que el motor acepte la orden |
| Mecanismo | Estado siguiente: compra, plantado, cosecha, venta realizada | Que ganemos más |
| Resultado local | Delta pareado W/L/T contra panel | Rating real ni generalización a todos los rivales |
| Resultado externo | Episodios reales del candidato y control en Kaggle | Causalidad limpia si cambia el emparejamiento o falta muestra |

El dinero final y la caja diaria son diagnósticos. La variable de decisión local
es victoria=1, empate=0,5, derrota=0. No promocionar por un margen de monedas.

## 2. Antes de gastar CPU

Completar la ficha de [IDEAS_Y_PRUEBAS.md](IDEAS_Y_PRUEBAS.md): una hipótesis,
línea o función que sostiene el mecanismo, parche aislado, controles, resultado
falsador, coste y regla de decisión. Buscar antecedentes en BRIEFING/BITACORA.
No repetir una variante descartada sin explicar qué cambia en esta prueba.

Separar aprobación para estudiar una idea, autorización de un barrido y decisión
de enviarla a Kaggle. Hoy no hay autorización para nuevos envíos ni barridos.
El segundo LLM puede revisar y recomendar; su acuerdo no autoriza gastos.

## 3. Verificar disparo y mecanismo

1. Congelar base, configuración y fuentes. La bandera nueva debe estar apagada
   por defecto. Comparar el comportamiento de la base con el chasis previo.
2. Perturbar el valor real: quitar una clave igual a su default es un noop por
   construcción. Identificar qué camino ejecuta (`tasks`, router u otro).
3. Capturar acciones antes de entregarlas al motor, que puede mutar las listas.
   Un contador de rama y una primera divergencia ayudan más que un hash aislado.
4. Comprobar el cambio previsto en el estado siguiente. Una orden BUY/PLANT/SELL
   emitida puede fallar, truncarse o ejecutarse parcialmente.
5. Una o pocas sondas demuestran posibilidad del mecanismo, no frecuencia ni
   fuerza. En episodios posteriores divergentes ya cambian las observaciones:
   para atribuir la primera decisión, usar la misma observación y estado del router.

`muerde.py` registra hashes, dinero y estados por cinta/semilla. Una traza igual
no demuestra que una clave sea universalmente inútil. `sd=0` en W/L/T sólo
significa delta constante; no informa sobre ejecución del parche.

## 4. Panel, espejo y controles

- Panel operativo: las 40 cintas `lad_` existentes, sin elegir por resultado.
  Guardar nombres y hashes. No mezclar `top_` con `lad_` como si fueran la misma
  población. El panel de cinco rivales es histórico, no el panel actual.
- Cada semilla se juega en ambos asientos. Empates cuentan 0,5.
- Base y noop exacto en cada bloque. Deben coincidir por episodio las acciones,
  dinero, estados y W/L/T. Cualquier discrepancia invalida la corrida.
- Control anterior definido antes de medir. En la prueba de lotes fue la
  configuración **exacta CAMPEONA_FB**, no una mezcla parcial con HOZ.
- Error, timeout, episodios faltantes, configuración o fuentes cambiadas:
  investigar el instrumento antes de interpretar deltas. No convertir errores
  o recompensas ausentes en derrotas ordinarias silenciosamente.

Un control anterior claramente peor comprueba sensibilidad a esa regresión.
No certifica potencia para detectar una mejora pequeña, ni transporte al ladder.
No seleccionar celdas porque la base esté entre 30% y 70%: sesga el panel.

## 5. Unidad de análisis e incertidumbre

Sea r el W/L/T por episodio. Para cada cinta t y semilla s:

```text
d[t,s] = media de asientos(r_candidato[t,s] - r_base[t,s])
D[s]   = media de las 40 cintas(d[t,s])
delta  = media de semillas(D[s])
SE     = desviación muestral(D[s]) / sqrt(n_semillas)
IC95   = delta ± t_0.975(n_semillas-1) × SE
```

El t por celda se conserva como comparación histórica, **no como sustituto
posterior** del análisis primario. Compartir semillas crea escenarios comunes;
el análisis principal actual trata cada semilla como un bloque del panel fijo.
Con ocho semillas hay ocho promedios independientes a ese nivel, no 640 ni 2.560.

El intervalo t es una aproximación con pocas semillas y no incorpora selección
del panel, variantes ya probadas, familias de rivales ni adaptación del rival.
Si otra pregunta requiere bootstrap, bloques por rival o inferencia de dos vías,
debe registrarse antes; no elegir después el método que dé el menor p.

Semillas disjuntas comprueban repetición en escenarios nuevos del mismo panel.
Para afirmar generalización a rivales nuevos hay que reservar también rivales
o familias fuera del proceso de selección. Las cintas son pasivas y pueden
favorecer cambios que explotan su calendario fijo de ventas/compras.

## 6. Descubrimiento, confirmación y decisiones

Fijar antes: candidato, panel, semillas, tamaño, controles, métrica primaria,
umbral, regla de parada y qué se hará si el resultado es inconcluso. Si se prueban
varios brazos, registrar multiplicidad y selección; el mejor t de muchos brazos
no merece la misma confianza que una hipótesis única preregistrada.

Para **lotes de semillas** se fijó:

- Descubrimiento: cuatro semillas, delta positivo y controles válidos para
  pasar a confirmación; no exigía significancia del descubrimiento.
- Confirmación: ocho semillas nuevas, IC95 por semilla completamente positivo
  (t>2,3646). El control anterior debía tener IC95 completamente negativo.
- Sólo después correspondía un head-to-head como veto, nunca como promotor.

Son los criterios de ese experimento, no tamaños universales adecuados para
cualquier idea. La confirmación de lotes cruza cero: **inconclusa**. No mezclar
bloques, cambiar a prueba unilateral, cambiar la unidad de análisis ni añadir
semillas hasta conseguir significancia. Una réplica futura es una nueva prueba,
con presupuesto y decisión fijados antes, manteniendo visible este resultado.

| Decisión | Evidencia mínima |
|---|---|
| No dispara en la sonda | Ninguna acción cambia en los estados examinados; revisar camino, no declarar idea falsa |
| Mecanismo no observado | Cambia conducta, pero no la variable intermedia prevista |
| Inconcluso | El intervalo incluye efectos compatibles con cero / falta generalización |
| Regresión local | Evidencia negativa bajo el diseño registrado |
| Mejora local confirmada | Pasa criterio primario y controles en bloque independiente |
| Candidato para ladder | Decisión separada, paquete verificado y nueva instrucción del usuario |

## 7. Integridad y reproducción

`barrido.py` escribe pares compatibles, episodios JSONL incrementales y manifiesto
con configs, seeds, archivos, versiones y hashes. No sobrescribe resultados
anteriores; añade sufijo si hace falta. Comparar configs Python con JSON tras
normalizar tuplas/listas mediante serialización **preservando orden**; el orden
de algunos diccionarios sí puede afectar al agente.

Conservar evidencia accesible fuera de `results/`, que está ignorado por Git.
El paquete [lotes_semillas](evidencia/lotes_semillas/README.md) incluye datos y
fuentes congeladas; `preparar_contexto_llm.py` verifica hashes y reanaliza el
resultado con biblioteca estándar, sin simulaciones ni red.

Los comandos de barridos históricos se documentan en el informe del experimento.
Copiarlos no autoriza ejecutarlos. No hay un comando de envío en esta guía para
evitar confundir documentación operativa con la autorización vigente.

## 8. Qué sustituye de la documentación antigua

- Panel de cinco seleccionado por resolución → panel fijo de 40 con sus límites.
- «sd=0 implica no ejecución» → separar trazas, ejecución y resultados.
- t>2 universal / contar celdas como independientes → diseño y grados de libertad explícitos.
- Elo ≈ delta×2,7 → calibración histórica débil; no usar como predicción precisa.
- Self-play como promotor → sólo diagnóstico o veto definido de antemano.
- «Toda idea plausible ya falló» → fallaron implementaciones y diseños concretos.



---

## SOURCE: docs/IDEAS_Y_PRUEBAS.md

# Cola de ideas y revisión entre LLMs

Estado: propuestas, no experimentos autorizados. La última corrida de Kaggle
queda reservada. **Un episodio local no consume una submission de Kaggle**;
los costes de CPU local y el cupo de envíos son presupuestos distintos.

## Primera tarea recomendada: revisión de la evidencia existente

Antes de otra hipótesis, pedir a otro LLM que reconstruya el delta y los controles
desde `evidencia/lotes_semillas/`, cuestione la unidad de análisis y revise el
parche. Coste: cero episodios nuevos, cero llamadas Kaggle. Debe entregar sus
objeciones con referencias, no aceptar nuestros resúmenes por confianza.

Que dos LLMs estén de acuerdo no constituye evidencia experimental independiente.
Un revisor ayuda si detecta supuestos, rutas que no ejecutan, muestras compartidas
o criterios movidos después del resultado. La prueba empírica sigue pendiente.

## A. Extender el diagnóstico de cohortes — siguiente prueba barata candidata

1. **Hipótesis:** el lote parcial evita que el trigo ocupe antes las últimas
   tiles disponibles y por eso adelanta cohortes premium en varios escenarios,
   no sólo en la sonda 99000. Apoyo: `decide`, bloque `seed_partial_batch`;
   tile (2,1), trigo d1 h19 en base frente a melón d1 h18 en candidato.
2. **Cómo se falsa:** medir plantados confirmados, primeras cohortes y cash
   comprometido. Si cambia compras pero sólo acumula semillas sin adelantar
   cohortes, falla el mecanismo general propuesto. Si adelanta cohortes y W/L/T
   no mejora, el mecanismo no basta para demostrar fuerza.
3. **Disparo:** contar cuándo el lote completo falla `_afford`, cuándo el parcial
   pasa y qué compra/plantado se ejecuta; mantener noop. No usar sólo dinero.
4. **Coste propuesto:** cuatro cintas elegidas por regla determinista previa
   independiente de resultados, dos semillas, dos asientos, tres brazos
   (base/noop/candidato): **48 episodios**, sólo mecanismo. Este panel pequeño
   no puede aprobar una mejora. El diseño y semillas requieren fijación antes.

El valor de esta prueba es averiguar qué medir y dónde puede fallar la explicación;
no rescatar significancia ni buscar retrospectivamente los rivales favorables.

## B. Réplica de compra parcial — si se decide pagar más evidencia de resultado

1. **Hipótesis:** la ventaja esperada del candidato congelado es positiva en
   escenarios nuevos sobre el mismo panel de 40. Evidencia previa: +5,0 y +4,84
   puntos; confirmación inconclusa con ocho semillas.
2. **Cómo se falsa:** nuevo bloque independiente, métrica primaria por semilla,
   IC95 y controles fijados de antemano. Intervalo que cruza cero → inconcluso;
   intervalo completamente negativo → regresión en ese diseño. No fusionar
   bloques como si el tamaño se hubiera fijado antes ni parar al cruzar un umbral.
3. **Disparo:** reutilizar la sonda conocida, asegurar que config/chasis coinciden
   con el candidato congelado y conservar hashes/estados/acciones.
4. **Coste ilustrativo:** cuatro brazos × 40 cintas × 24 semillas × dos asientos
   = **7.680 episodios**, aproximadamente 50 minutos de pared con el rendimiento
   observado de diez workers. No es un presupuesto aprobado ni una garantía
   de potencia. El revisor debe justificar n con el efecto mínimo que importa,
   la varianza observada y la incertidumbre de estimarla con ocho semillas.

Esta réplica no resuelve rivales adaptativos ni rivales nuevos. Si el objetivo
es transporte al ladder, hay que proponer además un panel reservado por rival
o familia, evitando contaminarlo con decisiones del desarrollo.

## C. Separar la excepción forrajera de la expansión — hipótesis de código

1. **Hipótesis:** mientras `wheat_gap>0`, sobrescribir `adaptive_best` con WHEAT
   propaga el piso forrajero a compras expansivas que tenían otro propósito.
   Apoyo: `bots/chassis.py`, asignación de `adaptive_best`, compras de `idle_plant`
   y fallback ocioso. Se observó una salida inicial de 6+8 semillas de trigo
   con piso 8; eso no demuestra por sí solo sobrecompra, porque pueden caber.
2. **Cómo se falsa:** separar el cultivo elegido por scorer del pedido de forraje,
   conservando su piso y anticipación. Si el camino no cambia o el trigo deja
   de abastecer animales, revisar/rechazar esa implementación. Sólo panel válido
   y confirmación pueden juzgar beneficio competitivo.
3. **Disparo:** traza del `best` original, override forrajero, órdenes de ambos
   bloques, stock y cohortes. El doble pedido consulta el mismo stock anterior,
   pero hay que distinguir cantidad duplicada, necesidad física y preferencia.
4. **Coste:** primero una sonda, sin combinar con compra parcial. Si sobrevive,
   el diseño mínimo análogo de cuatro brazos/40 cintas/cuatro semillas/espejo
   cuesta 1.280 episodios, más confirmación si procede. Aún no implementado.

No equivale a quitar el trigo ni activar `idle_best_only`: esas implementaciones
ya dieron resultados negativos. El fallback ocioso sí puede plantar otras pilas,
por lo que no hay prueba de un bloqueo permanente de semillas ajenas al scorer.

## D. Planificación de nuestra granja — investigación posterior

1. **Hipótesis:** una simulación propia de horizonte corto ordena mejor compras
   o servicios que prioridades fijas. Se apoya en reglas deterministas de cultivo
   y animales, pero debe declarar precios futuros y estado oculto que aproxima.
2. **Cómo se falsa:** primero confrontar predicciones de estado propio contra el
   motor en transiciones conocidas. Errores de crecimiento, consumo o calendario
   invalidan el simulador. Exactitud predictiva no aprueba su política: después
   hacen falta activación, panel y confirmación de la decisión que cambie.
3. **Disparo:** limitar inicialmente a una decisión y registrar el ranking
   calculado frente al elegido; medir p95/p99 de tiempo y memoria reales.
4. **Coste:** prototipo y validación del modelo antes de barridos. No hay presupuesto
   estimado fiable todavía. Prioridad posterior a las pruebas baratas de arriba.

No declarar imposible toda planificación porque el rival tenga datos privados.
Tampoco iniciar MCTS completo suponiendo que podemos reconstruir esos datos.

## Ficha obligatoria de una propuesta

```text
ID / título / estado: propuesta (sin ejecutar)
Pregunta y efecto mínimo de interés:
Base exacta y hashes:
Antecedentes negativos y diferencia de esta implementación:
Hipótesis en una frase:
Función/línea y unidades de cada cantidad:
Variable intermedia y orden que debe ejecutarse:
Qué observación refutaría el mecanismo:
Sonda de disparo, noop y estados comparables:
Brazos, controles y por qué ese control:
Población de rivales; posibles sesgos de selección:
Semillas reservadas / separación de descubrimiento-confirmación:
Métrica primaria, unidad de análisis, IC y regla de parada:
Qué haré si es negativo, inconcluso o positivo:
Número exacto de episodios y coste estimado:
Archivos de salida / manifiestos / verificación del paquete:
Objeción más fuerte del otro LLM y respuesta verificable:
Autorización disponible: análisis / sonda / barrido / envío (separados)
```

## Contrato del LLM revisor

Entregar una decisión **revisar / listo para sonda / listo para propuesta de
barrido**, con motivo. Señalar qué dato falta para cambiarla. No declarar una
mejora confirmada por plausibilidad, autoridad del primer LLM o dinero de un seed.
No cambiar el código del autor durante una corrida congelada. Si propone otra
idea, debe competir por coste e información y no multiplicar automáticamente brazos.



---

## SOURCE: docs/RULES.md

# Reglas de Kaggriculture — modelo verificado

Este documento es nuestro modelo mental del motor, escrito como **afirmaciones falsables**.
Cada afirmación tiene un estado:

- ❓ **predicción** — creemos que es así (según la doc o intuición), sin verificar
- ✅ **verificada** — confirmada leyendo el motor Y con una sonda ejecutada (se anota la evidencia)
- ❌ **refutada** — se deja tachada con la corrección al lado. *Los errores son lo más valioso del documento: marcan dónde nuestro modelo mental estaba mal.*

Fuentes de verdad, en orden de autoridad creciente:
página de la competencia → `kaggriculture.py` (el motor) → sonda ejecutada (`lab.py` / `tests/`).

**Motor de referencia:** `kaggle-environments == 1.32.7` — incluye el cambio de balance de agosto 2026 (curva `hinge` de escasez para CARROT/TOMATO/EGG, ver S5.1). Los organizadores anunciaron que es el último cambio salvo bugs.

**Formato:** `- ❓ **S1.** <afirmación falsable> — *Sonda:* <cómo comprobarla>`

Ejemplos del formato (mecánica trivial, para calibrar):

- ✅ **E1.** Comprar 1 semilla de wheat en el turno T deja el banco en $2,990, ya visible en la observación del turno T+1. — *Evidencia:* sonda B1, obs 1 (money 2990 tras BUY_SEED en step 0).
- ✅ **E2.** `PLANT WHEAT` parado en una tile vacía consume 1 semilla y la tile ya contiene el plant dict en la observación siguiente. — *Evidencia:* sonda B2, obs 23 (plant dict visible el turno después de plantar).

---

## 1. Orden de procesamiento del turno

*Preguntas guía: ¿en qué momento exacto se aplican mis acciones vs las órdenes de mercado vs el consumo del town vs el day-refresh? ¿Un peón contratado este turno puede actuar este mismo turno? ¿Si vendo y el precio cambia, qué precio me pagan? ¿En qué turno exacto del día ocurre el refresh (riego/comida se resetea)?*

- ✅ **S1.1.** Al inicio de cada día el granjero reaparece en (4,4) — la tile de acceso al shed del cuadrante NW — sin importar dónde terminó el día anterior. *Implicación: la posición de fin de día es gratis; no hay que "volver a casa".* — *Evidencia:* sonda A (farmer en (4,0) a h23 del día 0 → (4,4) a h0 del día 1).
- ✅ **S1.2.** La edad de una planta es por día calendario, no por turnos desde plantado: plantar a h0 o a h22 del día D da el mismo `planted_day = D` y el mismo calendario de crecimiento. *Implicación: plantar tarde en el día no pierde crecimiento — pero ver la trampa S2.1.* — *Evidencia:* sonda B2 (`planted_day=0` plantando a h22) + `_new_plant` no recibe la hora.
- ✅ **S1.3.** El efecto de una orden de mercado del turno T (dinero, items en shed) ya es visible en la observación del turno T+1. — *Evidencia:* sondas B1 y C.
- ✅ **S1.4.** Orden completo del turno: (1) acciones de unidades — por jugador: **granjero primero, luego peones en orden de lista**; (2) mercado en lockstep; (3) consumo del town; (4) decay de plantas; (5) si es h23, refresh de fin de día. Luego se actualiza day/hour. — *Evidencia:* motor `interpreter` L894–965.
- ✅ **S1.5.** Pipeline en el mismo turno: granjero `PLANT` + peón `WATER` sobre la misma tile **funciona** (el granjero actúa antes). Al revés — granjero `WATER` + peón `PLANT` — falla: el riego cae en tile vacía. *Implicación: con un peón, plantar+regar cuesta 1 turno de calendario, y hasta un plantado a h23 sobrevive si un peón riega en ese mismo turno.* — *Evidencia:* sonda P1 (002).
- ✅ **S1.6.** Validación atómica de PLANT: si los PLANT de un cultivo en un turno superan las semillas disponibles, **todos** los PLANT de ese cultivo se descartan (documentado en la página; visible en motor L920–933).
- ✅ **S1.7.** La producción de ongoing crops y animales ocurre en el refresh nocturno (durante el procesamiento del turno h23) — amanece visible en la observación de h0.

## 2. Plantas: riego, weeds y muerte

*Preguntas guía: ¿el día de plantado cuenta como día sin regar? ¿En qué momento exacto una planta se vuelve weed? ¿Regar dos veces el mismo día hace algo? ¿Pueden aparecer weeds en tiles locked o sobre estructuras?*

- ✅ **S2.1.** Una semilla nace con `consecutive_unwatered = 1` (el día de plantado cuenta como día sin regar): plantada en la última hora del día (h23), sin turno para regarla, amanece como WEED — muere esa misma medianoche y la semilla se pierde. *Implicación: la hora límite práctica para plantar es h22, siempre con el riego encadenado en el turno siguiente.* — *Evidencia:* sonda B1 (PLANT a h23 → `{"kind": "WEED"}` en día 1 h0); sonda B2 obs 23 (`consecutive_unwatered=1` recién plantada).
- ✅ **S2.2.** Plantar a h22 + regar a h23 sobrevive: el refresh nocturno deja `consecutive_unwatered = 0` y resetea `watered_today` a False para el día nuevo. Una planta nueva nace con `yield_units = 1`. — *Evidencia:* sonda B2, obs 23 vs obs 24.
- ✅ **S2.3.** Los weeds solo aparecen en tiles vacías y desbloqueadas (`None`) durante el refresh nocturno, con probabilidad 0.005 por tile. Nunca sobre plantas, estructuras ni tiles locked. — *Evidencia:* motor `_spawn_weeds` L836–840.
- ✅ **S2.4.** El RNG nocturno (weeds y sorteo de tiendas) es determinista por `(seed, día)`: mismo seed de episodio → misma partida. Útil para reproducir escenarios en el harness. — *Evidencia:* motor L869–871.

## 3. Cosecha y yields

*Preguntas guía: ¿cuánto rinde exactamente un wheat regado todos los días si cosecho el día 2? ¿Y el día 4? ¿Con fertilizer? ¿Cuándo empieza y termina el bonus del fertilizer? ¿Qué le pasa al yield si cosecho tarde (decay)? ¿HARVEST en tomato/strawberry deja la planta o la quita?*

- ✅ **S3.1.** Un wheat plantado el día 0 nace con `max_lifespan_step = 120` (= día 5, h0): el step absoluto donde empieza el decaimiento es `(max_yield_day + 1) × 24`, fijado al plantar. — *Evidencia:* sonda B2, obs 23.
- ✅ **S3.2.** `HARVEST` recoge **todos** los `yield_units` acumulados en una sola acción (plantas y animales). Las one-time desaparecen de la tile; ongoing y animales quedan. — *Evidencia:* motor L446–473.
- ✅ **S3.3.** `HARVEST` es no-op antes de `first_yield_day` aunque `yield_units > 0`: un melón de edad 8 con 4 unidades acumuladas no entrega nada. — *Evidencia:* motor L453 + sonda P4.
- ✅ **S3.4.** El bonus de riego se aplica **en el momento de la acción WATER** (no de noche): +1 (+2 si fertilizada ese día) cuando `window_start ≤ edad ≤ max_yield_day`, con `window_start = (max_yield_day + 1) // 2`. Ventanas: wheat 2–4, carrot 2–3, melón 6–12. — *Evidencia:* motor L431–444 + sonda P4.
- ❌ **S3.5.** ~~La tabla de la página: melón "Time to Max Yield: 10 days"~~ → **En el motor `max_yield_day = 12`**. Regando a diario el tope de 6 se alcanza en edad 10 (edades 11–12 no suman); `first_yield_day = 10`. La nota de la página ("ventana 6–12") era la correcta; su tabla está desactualizada. — *Evidencia:* motor `CROPS` L16 + sonda P4 (curva 1,1,1,1,1,2,3,4,5,6,6,6).
- ✅ **S3.6.** `FERTILIZE` consume 1 FERTILIZER **del inventario personal** de quien lo ejecuta (igual que FEED); la ventana es `hoy, hoy+1, hoy+2` — el día de fertilizar cuenta. Refertilizar toma el máximo (extiende, no acumula). — *Evidencia:* motor L475–482.
- ✅ **S3.7.** Ongoing crops producen en el refresh nocturno cuando `(día_siguiente − planted_day − first_yield_day) % interval == 0`: +1 base, +2 si ese día estuvo regada Y fertilizada. Al llegar a `max_yield` producciones, el decay arranca un día después. — *Evidencia:* motor L786–802.
- ✅ **S3.8.** Decay: desde `max_lifespan_step`, `yield_units` baja 1 **cada 2 turnos**; al llegar a 0 la tile se vuelve weed. Cosechar antes de que empiece, o rápido si ya empezó. — *Evidencia:* motor `_decay_plants` L752–766.
- ✅ **S3.9.** Curvas de yield verificadas empíricamente (plantado día 0, riego diario — sonda 003):

  | Cultivo | Curva por edad | Pico | Con fertilizer | Cosechar a más tardar |
  |---|---|---|---|---|
  | WHEAT | 1, 1, 2, 3, 4 | 4 en edad 4 | fert d2 → 6 en edad 4 | día 4 (decay desde d5 h0) |
  | CARROT | 1, 1, 2, 3 | 3 en edad 3 | fert d2 → 4 en edad 3 | día 3 (decay desde d4 h0) |
  | MELON | 1×6, 2, 3, 4, 5, 6 | 6 en edad 10 | fert d6 → 6 en edad 8, pero HARVEST sigue bloqueado hasta edad 10 | día 12 (decay desde d13 h0) |
  | TOMATO | 0 hasta edad 7; +1 en amaneceres 8, 9, 10, 11 | 4 acumulado | tick ×2 si regada+fertilizada | día 11 (decay desde d12 h0) |
  | STRAWBERRY | 0 hasta edad 9; +1 en amaneceres 10, 12, 14, 16 | 4 acumulado | tick ×2 | día 16 (decay desde d17 h0) |
  | COW | primera leche amanecer d8 (colocada d0), +1 cada 2 días | cap held 6 | — | — |
  | SHEEP | primera lana amanecer d6, +1 cada 3 días | cap held 6 | — | — |

- ✅ **S3.10.** Detalles de la sonda 003: los ongoing nacen con `yield_units = 0` (los one-time con 1). El decay es *veloz*: 1 cada 2 turnos significa que un wheat pasa de pico 4 a weed en las primeras 8 horas del día 5 — el deadline de cosecha es duro. **En melón el fertilizer es casi inútil**: alcanza el cap en edad 8 pero no se puede cosechar hasta edad 10 (solo ahorra riegos finales). En ongoing sí multiplica: cada tick regado+fertilizado produce 2 en vez de 1 — hasta 8 unidades totales por planta si se cosecha entre ticks (el conteo de producciones es por tick, no por unidad; la fertilización cubre 3 días, y los 4 ticks del tomato abarcan 4). — *Evidencia:* sonda 003 + motor L795–800.

## 4. Animales: feed, care, escape, fertilizer

*Preguntas guía: ¿de dónde sale el wheat del FEED — inventario de quien alimenta, o shed? ¿El primer día sin alimentar cuenta para el escape? ¿Cuándo se paga exactamente el bonus de CARE? ¿COLLECT_FERTILIZER cuántas veces al día por animal?*

- ✅ **S4.1.** FEED consume 1 wheat **del inventario personal de quien alimenta** — NO toma del shed: con 2 wheat en el shed y el inventario vacío, FEED es no-op (`fed_today` sigue False, shed intacto); con wheat en mano, alimenta y descuenta 1 del inventario. *Implicación logística: cada ronda de alimentación exige `PICKUP WHEAT n` previo (o wheat cosechado aún en mano); presupuestar ese turno extra por unidad que alimenta.* — *Evidencia:* sonda C, obs 7 vs obs 11.
- ✅ **S4.2.** BUY_ANIMAL y BUY_PRODUCT entregan al shed (no al inventario del granjero). — *Evidencia:* sonda C, obs 1 (shed = {WHEAT: 2, GOOSE: 1} tras comprar).
- ✅ **S4.3.** El wheat es un único item sin importar el origen: cosechado o comprado, cualquiera sirve para FEED ("¿los animales comen de nuestra cosecha?" → sí, mientras esté en el inventario de quien alimenta).
- ✅ **S4.4.** Matemática del CARE, confirmada de punta a punta: cada noche con fed+cared banca +1; la noche de producción paga `1 + banco` (si el animal fue alimentado ese día), el banco se resetea, y el care de esa misma noche re-banca 1. Un ganso colocado el día 0 con feed+care diario amanece el día 4 con exactamente 4 huevos (1+3 = justo el cap). Estado estable con care diario: **2 huevos/día — CARE duplica la producción del ganso por 1 acción/día.** — *Evidencia:* motor L805–833 + sonda P2.
- ✅ **S4.5.** `fertilizer_available` se enciende **cada noche para todo animal vivo, alimentado o no**; `COLLECT_FERTILIZER` da 1 al inventario personal y apaga el flag. Máximo 1/animal/día, sin acumulación. — *Evidencia:* motor L515–521, L831.
- ✅ **S4.6.** El escape (2 noches sin comer) pierde solo el animal: **la estructura queda en pie** y es reutilizable. Una estructura con animal no se puede DIG. — *Evidencia:* motor L817–819, L488.
- ✅ **S4.7.** `BUILD_COOP` / `BUILD_PASTURE` no cuestan dinero (solo la acción) y exigen tile totalmente vacía (un weed bloquea — DIG primero). — *Evidencia:* motor L493–503.
- ✅ **S4.8.** `max_held` capea la acumulación: producción no cosechada por encima del cap **se pierde** (el ganso del P2 quedó en 4 = cap exacto). La cadencia de cosecha importa. — *Evidencia:* motor L827 + sonda P2.
- ✅ **S4.9.** **La rampa de CARE**: el banco acumula +1 por noche fed+cared también durante los días de espera previos al primer yield. Colocados el día 0 con feed+care diario: sheep amanece el d6 con **6 lanas (cap completo — $1,200 a precio base, de un animal de $500)**; cow amanece el d8 con **6 leches ($960; 1+7 capado en 6, 2 desperdiciadas)**; goose con 4 huevos (1+3 = su cap justo, $200). En estado estable con care diario: sheep 4 lanas/3 días (~$267/día), cow 3 leches/2 días ($240/día), goose 2 huevos/día ($100/día). *Implicación: los animales lentos convierten la espera en inventario; con care diario, sheep y cow dominan al ganso por tile y por acción a precio base.* — *Evidencia:* sonda 004.

## 5. Mercado y precios

*Preguntas guía: ¿el precio de mi venta se cotiza antes o después de que mi unidad entre al inventario del mercado? ¿Cómo se resuelven ventas simultáneas de los dos jugadores? ¿Vender 100 wheat seguidos recauda cuánto (la suma sobre la curva)? ¿Cómo funciona el floor de $1? ¿Qué puedo comprar de vuelta y a qué precio?*

- ✅ **S5.1.** *(cambio de balance, motor 1.32.7, agosto 2026)* CARROT, TOMATO y EGG usan la forma `hinge` en su curva de escasez: con déficit `d = I0 − inv` y `u = d/T`, `f(u) = u + 8·max(0, u−1)²`. Bajo el codo (`d < T`) se comporta lineal; pasado el codo, el precio despega cuadráticamente. CARROT además subió `below_target` 0.20 → 1.00 (a déficit T: $70 vs los $42 de antes). TOMATO y EGG conservan su target 0.40 — solo cambia el comportamiento pasado el codo. Según el anuncio, el spike aparece (sin producción de nadie) en ~50% de partidas para tomato, 26% carrot, 22% eggs, dependiendo de qué tiendas destape el town. — *Evidencia:* diff `kaggriculture.py` 1.32.6 → 1.32.7 (`HINGE_GAIN = 8.0`, `MARKET_PARAMS`).
- ✅ **S5.2.** El precio de compra se cotiza al inventario post-compra: comprar 2 wheat con el mercado en I0 costó $52 ($26 + $26), no $50 (2 × base). — *Evidencia:* sonda C, obs 1 (money 3000 → 2648 = −$300 goose − $52 wheat).
- ✅ **S5.3.** `SELL` vende **solo desde el shed** — lo que está en inventario personal no es vendible. `DROP` (acción de unidad) + `SELL` (orden de mercado) **en el mismo turno funciona**, porque las acciones de unidad se procesan antes que el mercado. — *Evidencia:* motor `_commit_unit` L653–661 + sonda P3 (venta con wheat en mano: $0; DROP+SELL mismo turno: cobrado).
- ✅ **S5.4.** Lockstep por unidad: la unidad n de ambos jugadores se cotiza al mismo inventario pre-commit y luego ambas se ejecutan — no hay ventaja de orden en volumen de SELL/BUY. `HIRE` y `BUY_LAND` son atómicos y se resuelven **en orden de jugador (el 0 primero)** cuando llega su índice de cola. — *Evidencia:* motor L563–626.
- ✅ **S5.5.** Solo se conservan las primeras `maxMarketOrdersPerTurn` (10) órdenes por turno (`q[:10]`); una orden SELL/BUY muere definitivamente en cuanto una unidad no puede ejecutarse (sin stock / sin dinero / shed lleno).
- ✅ **S5.6.** Con el shed lleno (≥100), `BUY_PRODUCT` y `BUY_ANIMAL` **fallan** — un shed lleno bloquea compras, no solo almacenamiento. `BUY_SEED` no tiene límite (las semillas viven aparte). — *Evidencia:* motor L662–686.
- ✅ **S5.7.** Ventas al floor de $1 pagan el $1 pero no agregan inventario al mercado (el floor se mantiene reactivo a compras posteriores). — *Evidencia:* motor L658–660.
- ✅ **S5.8.** Los precios se recalculan tras el mercado Y tras el consumo del town, cada turno — la observación siguiente siempre trae precios frescos.

## 6. Peones (farm hands)

*Preguntas guía: ¿costo exacto del 1er, 2do, 3er peón del mismo día? ¿Dónde aparece y desde cuándo actúa? ¿Qué pasa con su inventario cuando desaparece al final del día?*

- ✅ **S6.1.** Costo del HIRE n-ésimo del día: `fib(hires_today)` = $1, 1, 2, 3, 5, 8, 13, 21, 34, 55 — **10 peones cuestan $143 el día entero**. Confirmado: primer hire $1. *Implicación: los peones son absurdamente baratos frente a cualquier cosecha; el límite real es tener trabajo útil que darles.* — *Evidencia:* motor L690–709 + sonda P1 (money 2979 = 3000 − 20 − 1).
- ✅ **S6.2.** El peón aparece durante la fase de mercado del turno T (spawn: primera tile de acceso al shed libre en orden NWSE, empates por menor ocupación → el primer hire del día cae en (5,4), locked pero transitable) y **actúa desde T+1**. — *Evidencia:* motor L533–541 + sonda P1.
- ✅ **S6.3.** Al fin del día: inventarios de todos (granjero y peones) se vuelcan al shed automáticamente (overflow sobre 100 se descarta), los peones desaparecen, `hires_today` vuelve a 0. — *Evidencia:* motor `_end_of_day` L873–882.

## 7. Town: tiendas y consumo

*Preguntas guía: ¿cada cuánto consume cada tienda y cuántas unidades? ¿El consumo del town mueve los precios igual que una compra de jugador? ¿Qué significa el "2x" de las tiendas de un solo producto?*

- ✅ **S7.1.** Las tiendas consumen en todo turno con `step % 4 == 0` (incluido el step 0) — 1 unidad de cada producto que demandan, ×2 si la tienda es mono-producto. El town center consume 1 de cada producto (menos fertilizer) en `step % 24 == 0`. El consumo drena inventario de mercado directamente → sube precios igual que una compra. — *Evidencia:* motor `_town_consume` L728–749.
- ✅ **S7.2.** El sorteo de tienda nueva ocurre en el refresh nocturno cuando `día_siguiente % 3 == 0` (noches de los días 2, 5, 8, …), con reemplazo, tope 8 instancias. — *Evidencia:* motor L884–891.

## 8. Terreno, shed e inventario

*Preguntas guía: ¿desde qué tiles exactas funcionan PICKUP/DROP/PLACE al shed? ¿Qué pasa con el overflow del shed al final del día? ¿DIG qué puede y qué no puede remover? ¿Qué acciones funcionan sobre tiles locked?*

- ❌ **S8.1.** ~~"Comprar cuadrantes vecinos" sugiere elegir cuál~~ → **`BUY_LAND` no permite elegir: el orden es fijo NE ($1k) → SW ($2k) → SE ($4k)**. Las tiles se desbloquean inmediatamente en la fase de mercado del mismo turno. — *Evidencia:* motor `LAND_ORDER` L83 + `_do_buy_land` L712–725.
- ✅ **S8.2.** `DIG` remueve planta, weed o estructura vacía de la tile donde estás parado; nada más (ni animales, ni a distancia).
- ✅ **S8.3.** Entre el respawn matinal (S1.1) y el auto-drop nocturno (S6.3), la posición y la carga al final del día son gratis: nunca hay que gastar turnos en "volver a dejar las cosas". El único costo real del overflow es el descarte sobre 100.



---

## SOURCE: docs/EXPERIMENTO_LOTES_SEMILLAS.md

# Compra parcial de semillas — protocolo y evidencia

Fecha: 2026-09-05. Protocolo registrado antes del panel.
Estado final: señal positiva repetida, confirmación inconclusa; no adoptar.

**Alcance vigente:** el usuario suspendió cualquier envío a Kaggle y pidió
preparar una revisión por otro LLM. Los comandos de este documento registran
el experimento realizado; no autorizan volver a ejecutarlo. Ver
[estado actual](ESTADO_ACTUAL.md) y [evidencia transportable](evidencia/lotes_semillas/README.md).

## Hipótesis y cambio aislado

Exigir caja para el lote completo retrasa la compra y el plantado de cultivos
largos. `seed_partial_batch=True` reduce el lote adaptativo (máximo seis)
hasta que pase la misma función `_afford`, con la misma reserva de $100.
No cambia el cultivo elegido, el piso forrajero, el stock contabilizado,
las otras compras ni su orden. La bandera está apagada por defecto.

No confundir esta intervención con `order_funding`, `animal_first`, reducción
del piso de trigo o coordinación de los dos pedidos de semillas. No se combinan.

## Sonda de activación y mecanismo (antes del panel)

Comando:

```bash
git show HEAD:bots/chassis.py > /tmp/kaggriculture_chassis_antes_lotes.py
./.venv/bin/python sondas/005_lotes_semillas.py --reference /tmp/kaggriculture_chassis_antes_lotes.py
```

Semilla 99000, asiento 0, cinta `lad_abhi_kumar_agrawal_104715819`.
Archivo: `results/sonda_lotes_99000_s0.json`.

- Base, noop y chasis anterior: mismas 719 decisiones y dinero final.
- Candidato: 599 turnos con acciones distintas; todos los agentes acaban DONE.
- Primera diferencia: d1 h16, caja $472. La base no compra; el candidato compra
  cuatro semillas de melón por $320 y conserva la reserva.
- Primer melón **confirmado en el tablero**: base d6 h16, candidato d1 h18.
- Melones plantados hasta d4: base 0, candidato 5; hasta d6: ambos 8.
- Primera fresa confirmada: base d8 h3, candidato d7 h19.

La misma tile (2,1) explica cómo pocos turnos se convierten en varios días:
la base planta WHEAT en d1 h19 y no planta MELON allí hasta d6 h16. El
candidato planta MELON en d1 h18. Hasta d2 la base ha plantado 17 trigos y
ningún melón; el candidato, 12 trigos y cinco melones. El piso configurado
de trigo es el mismo. Es una observación de esta sonda, no una estimación de
frecuencia del mecanismo en la población.

La sonda comprueba activación y adelanto de cohortes en este escenario. No
estima mejora de win-rate. Ambos brazos ganan este episodio pese a sus acciones
distintas: igualdad de W/L/T no prueba igualdad de conducta.

Alcance de la instrumentación: se cuentan plantas visibles después del turno.
Las compras inferidas por delta de semillas son una cota inferior si un plantado
muere durante el refresh de ese mismo turno. En el JSON inicial ese campo se
llamó `executed_seed_buys`; la sonda lo etiqueta ahora `seed_buys_lower_bound`.
La primera compra descrita arriba ocurre en h16, antes del plantado de h18, y
está respaldada también por la acción emitida. No depende de esa salvedad nocturna.

## Diseño fijado antes de observar el panel

Población: las 40 cintas `lad_`, sin selección por resultados.

| Brazo | Configuración |
|---|---|
| base | CAMPEONA_HOZ |
| noop | copia exacta de CAMPEONA_HOZ |
| _peor | configuración exacta CAMPEONA_FB, generación anterior del linaje |
| partial_batch | CAMPEONA_HOZ + seed_partial_batch=True |

Descubrimiento: semillas 101000–101003, dos asientos, 1.280 episodios.
Confirmación prevista: semillas 102000–102007, dos asientos, 2.560 episodios.
La sonda 99000 no pertenece a ninguno de los dos bloques. No se ajustarán
parámetros ni se escogerán rivales a partir del descubrimiento.

## Integridad y criterio de decisión

1. El noop debe coincidir por episodio en acciones emitidas, dinero, estados
   y W/L/T; delta y sd de W/L/T deben ser cero. Un error o timeout invalida la
   evaluación y se investiga antes de interpretar resultados.
2. `_peor` debe dar una regresión clara. Se considera claro un intervalo 95%
   agrupado por semilla completamente por debajo de cero. Si falla, no se
   atribuye al panel autoridad para aprobar o rechazar una mejora pequeña.
3. Métrica de resultado: diferencia pareada de W/L/T por (cinta, semilla),
   promediando ambos asientos. El t por celda se conserva para comparación
   histórica; el análisis principal promedia primero las 40 cintas de cada
   semilla y estima la incertidumbre entre semillas.
4. Descubrimiento con delta positivo y controles válidos: pasa a confirmación.
   No se exige significancia en cuatro semillas para hacer ese cribado.
   Delta no positivo: no se adopta ni se gasta automáticamente la confirmación.
5. Confirmación: delta positivo e intervalo 95% agrupado por semilla por encima
   de cero (t > 2,3646 con ocho semillas). Si cruza cero, el resultado es
   inconcluso; no se presenta como mejora validada. Las cintas siguen siendo
   rivales pasivos, y nuevas semillas no validan generalización a otros rivales.
6. Sólo un candidato confirmado pasa al duelo contra el campeón como veto.
   No se cambia CAMPEONA_HOZ ni se envía una submission con este experimento.

Detalle del veto, fijado durante la confirmación y antes de leer su resultado:
40 semillas nuevas 103000–103039, dos asientos (80 episodios). Se exige ausencia
de errores y W/L/T medio al menos 50% contra CAMPEONA_HOZ. Su magnitud no se
usa para promocionar ni para convertir el efecto a Elo.

Coste: 1.280 episodios para el primer contraste; 2.560 adicionales sólo si pasa
el descubrimiento. Las mediciones de compras y cohortes son diagnóstico del
mecanismo; el dinero no sustituye la métrica de victorias.

## Resultado

Prueba de integración: `SET=semillas_parciales N_SEEDS=1 WORKERS=2
TAPES=lad_abhi_kumar_agrawal_104715819 ./.venv/bin/python barrido.py 99002`.
Ocho episodios DONE, noop exacto en ambos asientos, candidato y control anterior
con acciones distintas. Esta prueba de una cinta no decide fuerza.

Validaciones adicionales: ocho casos alrededor de los límites de reserva y
tamaño de lote (incluyendo caja igual al coste más reserva), ninguna orden de
cantidad cero y respeto de caja ya comprometida con `order_funding=True`.
El verificador noop acepta trazas idénticas y rechaza una traza distinta aunque
el dinero y W/L/T coincidan. Compilación y `git diff --check` correctos.

Comando del descubrimiento:

```bash
SET=semillas_parciales N_SEEDS=4 WORKERS=10 ./.venv/bin/python -u barrido.py 101000
```

Descubrimiento terminado: 1.280 episodios válidos; noop exacto en sus 320
comparaciones por episodio. Fuentes y cintas mantienen sus hashes.

| Brazo | W/L/T medio | Delta (puntos) | t por celda | t por semilla |
|---|---:|---:|---:|---:|
| base | 62,1875% | 0 | — | — |
| noop | 62,1875% | 0 | — | — |
| _peor | 36,2500% | −25,9375 | −5,94 | −15,07 |
| partial_batch | 67,1875% | +5,0000 | +1,41 | +1,68 |

El candidato cambia la traza en 320/320 episodios. La señal positiva no alcanza
significancia en descubrimiento; satisface el cribado predefinido y pasa a
confirmación sin ajustar el código ni seleccionar rivales.

IC95 del delta agrupado por semilla: candidato [−4,47; +14,47] puntos;
control anterior [−31,41; −20,46] puntos.

Evidencia: `results/barrido_101000.json`, `results/barrido_101000.meta.json`,
`results/barrido_101000.episodes.jsonl`, `results/lotes_descubrimiento_101000.txt`.
Las fuentes utilizadas se conservaron en `results/lotes_fuentes_20260905.tar.gz`;
sus hashes y los de las 40 cintas están en los manifiestos de las corridas.

Comando de confirmación (semillas 102000–102007):

```bash
SET=semillas_parciales N_SEEDS=8 WORKERS=10 ./.venv/bin/python -u barrido.py 102000
```

Confirmación terminada: 2.560 episodios válidos, noop exacto en 640/640
comparaciones, cero errores. Configs, fuentes y cintas idénticas al descubrimiento;
semillas disjuntas verificadas.

| Brazo | W/L/T medio | Delta (puntos) | t por celda | t por semilla |
|---|---:|---:|---:|---:|
| base | 60,0000% | 0 | — | — |
| noop | 60,0000% | 0 | — | — |
| _peor | 36,7188% | −23,2813 | −8,45 | −6,74 |
| partial_batch | 64,8438% | +4,8438 | +2,45 | +2,08 |

**IC95 agrupado por semilla del candidato: [−0,67; +10,36] puntos.**
Control anterior: [−31,45; −15,11], claramente inferior. El candidato modifica
las acciones en 640/640 episodios: mejora W/L/T en 62, empeora en 31 y conserva
el resultado en 547. No hay empates en ninguno de los brazos.

| Semilla de confirmación | Delta (puntos) |
|---|---:|
| 102000 | +13,75 |
| 102001 | +2,50 |
| 102002 | +2,50 |
| 102003 | 0,00 |
| 102004 | −2,50 |
| 102005 | +3,75 |
| 102006 | +16,25 |
| 102007 | +2,50 |

**Decisión según protocolo: inconcluso, no adoptar.** Se repite el signo y una
magnitud próxima al descubrimiento, pero el intervalo primario cruza cero y
t=2,08 no supera 2,3646. El t por celda de 2,45 no sustituye ahora el criterio
fijado. Tampoco se juntan ambos bloques para rescatar la confirmación.

No se ejecuta el veto head-to-head porque sólo correspondía después de una
confirmación positiva. `seed_partial_batch` queda experimental y apagado;
CAMPEONA_HOZ y la submission conservan su configuración. La hipótesis no queda
refutada: una réplica independiente con más semillas podría reducir incertidumbre,
pero no forma parte de esta corrida ni se añade mirando resultados intermedios.

Coste realizado: 3.840 episodios de panel; 8,19 minutos de pared en
descubrimiento y 16,82 en confirmación con diez workers. La sonda y la prueba
de integración son adicionales. Ambos bloques tienen controles válidos.

Evidencia de confirmación: `results/barrido_102000.json`,
`results/barrido_102000.meta.json`, `results/barrido_102000.episodes.jsonl`,
`results/lotes_confirmacion_102000.txt`. Resumen con intervalos y transiciones:
`results/lotes_veredicto_20260905.json`.



---

## SOURCE: docs/evidencia/lotes_semillas/README.md

# Evidencia transportable del experimento de lotes

Copiada de `results/` sin nuevas simulaciones. Estos archivos están fuera de
las reglas de exclusión de Git; aún hay que incorporarlos a un commit para que
viajen en un clon. `indice.json` declara origen local, tamaño y SHA-256.

| Archivo | Contenido |
|---|---|
| `veredicto.json` | Resúmenes, intervalos, deltas por semilla, transiciones y decisión |
| `sonda_99000.json` | Acciones iniciales divergentes, cohortes y controles de la sonda |
| `pares_101000.json`, `pares_102000.json` | W/L/T por brazo y (cinta, semilla), asientos promediados |
| `manifiesto_101000.json`, `manifiesto_102000.json` | Configs exactas, seeds, fuentes/cintas, versiones y resultado |
| `episodios_101000.jsonl.gz`, `episodios_102000.jsonl.gz` | Los 1.280 y 2.560 episodios con rewards, estados y hashes de acciones |
| `fuentes_panel.tgz` | Fuentes exactas de barrido/chasis/arquetipos/tape/harness usadas en ambos bloques |

Los manifiestos conservan sus rutas originales `results/...`; esta tabla y el
índice indican sus copias transportables. Los originales no fueron reescritos.
Los hashes de acciones permiten verificar igualdad, **no reconstruir las acciones**.
La sonda sí contiene la primera diferencia y los plantados observados.

Las 40 cintas no se duplicaron aquí: los manifiestos enumeran sus nombres y
hashes; sus archivos están en `bots/meta/tapes/`. El generador verifica que estén
presentes e idénticos. Si faltan en otro checkout, no se podrá repetir el panel.
No incluye replays privados ni credenciales.

En el JSON de la primera sonda, `executed_seed_buys` es una inferencia por stock
y una cota inferior si un PLANT muere en el mismo refresh nocturno. La sonda
actual usa el nombre `seed_buys_lower_bound`; no se altera el archivo histórico.

Verificar y preparar contexto sin red ni simulaciones:

```bash
python3 preparar_contexto_llm.py
```

Para leer un JSONL comprimido usar `gzip.open(..., 'rt')`. Para las fuentes
usar `tarfile.open(..., 'r:gz')` y leer miembros; no hace falta extraer ni ejecutar.
El generador comprueba hashes, controles, pares y estadísticas primarias.


---

## Veredicto reproducido desde episodios

```json
{
  "verdict": "inconcluso_no_adoptar",
  "method": "IC95 t de Student de deltas medios por semilla, panel fijo de 40 cintas",
  "runs": [
    {
      "seeds": [
        101000,
        101001,
        101002,
        101003
      ],
      "episodes": 1280,
      "arms": {
        "base": {
          "win_rate_percent": 62.18749999999999,
          "delta_points": 0.0,
          "ci95_seed_points": [
            0.0,
            0.0
          ],
          "t_seed": null,
          "t_cell": null,
          "seed_deltas_points": {
            "101000": 0.0,
            "101001": 0.0,
            "101002": 0.0,
            "101003": 0.0
          },
          "changed_actions_episodes": 0,
          "ties": 0
        },
        "noop": {
          "win_rate_percent": 62.18749999999999,
          "delta_points": 0.0,
          "ci95_seed_points": [
            0.0,
            0.0
          ],
          "t_seed": null,
          "t_cell": null,
          "seed_deltas_points": {
            "101000": 0.0,
            "101001": 0.0,
            "101002": 0.0,
            "101003": 0.0
          },
          "changed_actions_episodes": 0,
          "ties": 0
        },
        "_peor": {
          "win_rate_percent": 36.25,
          "delta_points": -25.937500000000004,
          "ci95_seed_points": [
            -31.41485860603126,
            -20.460141393968744
          ],
          "t_seed": -15.070165563453184,
          "t_cell": -5.9412628810031025,
          "seed_deltas_points": {
            "101000": -23.75,
            "101001": -27.500000000000004,
            "101002": -22.5,
            "101003": -30.0
          },
          "changed_actions_episodes": 320,
          "ties": 0
        },
        "partial_batch": {
          "win_rate_percent": 67.1875,
          "delta_points": 5.0,
          "ci95_seed_points": [
            -4.469671882026762,
            14.469671882026763
          ],
          "t_seed": 1.6803361008336117,
          "t_cell": 1.4075895748459328,
          "seed_deltas_points": {
            "101000": 8.75,
            "101001": -1.25,
            "101002": 1.25,
            "101003": 11.25
          },
          "changed_actions_episodes": 320,
          "ties": 0
        }
      },
      "runtime_minutes": 8.185930316666667,
      "transitions": {
        "iguales": 250,
        "mejoran": 43,
        "empeoran": 27
      }
    },
    {
      "seeds": [
        102000,
        102001,
        102002,
        102003,
        102004,
        102005,
        102006,
        102007
      ],
      "episodes": 2560,
      "arms": {
        "base": {
          "win_rate_percent": 60.0,
          "delta_points": 0.0,
          "ci95_seed_points": [
            0.0,
            0.0
          ],
          "t_seed": null,
          "t_cell": null,
          "seed_deltas_points": {
            "102000": 0.0,
            "102001": 0.0,
            "102002": 0.0,
            "102003": 0.0,
            "102004": 0.0,
            "102005": 0.0,
            "102006": 0.0,
            "102007": 0.0
          },
          "changed_actions_episodes": 0,
          "ties": 0
        },
        "noop": {
          "win_rate_percent": 60.0,
          "delta_points": 0.0,
          "ci95_seed_points": [
            0.0,
            0.0
          ],
          "t_seed": null,
          "t_cell": null,
          "seed_deltas_points": {
            "102000": 0.0,
            "102001": 0.0,
            "102002": 0.0,
            "102003": 0.0,
            "102004": 0.0,
            "102005": 0.0,
            "102006": 0.0,
            "102007": 0.0
          },
          "changed_actions_episodes": 0,
          "ties": 0
        },
        "_peor": {
          "win_rate_percent": 36.71875,
          "delta_points": -23.28125,
          "ci95_seed_points": [
            -31.451523503515027,
            -15.110976496484973
          ],
          "t_seed": -6.738012911527406,
          "t_cell": -8.454555952002593,
          "seed_deltas_points": {
            "102000": -3.75,
            "102001": -20.0,
            "102002": -25.0,
            "102003": -25.0,
            "102004": -25.0,
            "102005": -33.75,
            "102006": -18.75,
            "102007": -35.0
          },
          "changed_actions_episodes": 640,
          "ties": 0
        },
        "partial_batch": {
          "win_rate_percent": 64.84375,
          "delta_points": 4.84375,
          "ci95_seed_points": [
            -0.6701159427042518,
            10.357615942704252
          ],
          "t_seed": 2.077244684159868,
          "t_cell": 2.4469567658648965,
          "seed_deltas_points": {
            "102000": 13.750000000000002,
            "102001": 2.5,
            "102002": 2.5,
            "102003": 0.0,
            "102004": -2.5,
            "102005": 3.75,
            "102006": 16.25,
            "102007": 2.5
          },
          "changed_actions_episodes": 640,
          "ties": 0
        }
      },
      "runtime_minutes": 16.821907966666668,
      "transitions": {
        "iguales": 547,
        "mejoran": 62,
        "empeoran": 31
      }
    }
  ]
}
```


## Configuraciones exactas del panel archivado

Snapshot del experimento, no importación del código actual.

```json
{
  "base": {
    "hands": 8,
    "animals": [
      [
        "COW",
        4
      ],
      [
        "SHEEP",
        4
      ]
    ],
    "plants": {
      "CARROT": 1,
      "MELON": 11,
      "STRAWBERRY": 5,
      "WHEAT": 8
    },
    "care": true,
    "collect_fert": true,
    "fert_prio": 45,
    "animal_harvest_at": 4,
    "premium_hold_day": 8,
    "buy_land": true,
    "max_quadrants": 3,
    "prio_care": 70,
    "prio_urgency": 25,
    "plant_near": true,
    "endgame": true,
    "adaptive": true,
    "crop_tiles": 30,
    "zoning": false,
    "zone_fallback_prio": 70,
    "prio_feed": 75,
    "prio_water": 44,
    "prio_win_bonus": 12,
    "prio_harvest": 76,
    "prio_plant": 40,
    "grow": false,
    "prio_dig": 8,
    "mkt_opp_factor": 1,
    "router": true,
    "hire_late": true,
    "multi_feeder": false,
    "phased": false,
    "tiles_per_unit": 5,
    "sell_floor": 0,
    "idle_plant": true,
    "hands_per_quadrant": 4,
    "land_early": true,
    "town_forecast": true,
    "fert_crops": [
      "STRAWBERRY",
      "TOMATO"
    ],
    "opp_read": true,
    "sell_rank": true,
    "order_budget": true,
    "beat_wave": true,
    "wave_min_value": 2000,
    "melon_max": 8,
    "smart_overflow": false,
    "scorer_v2": false,
    "fallback_fix": true,
    "fert_dawn_load": true,
    "fert_tick_aligned": true,
    "fert_phase_lock": true,
    "seed_stock_aware": true
  },
  "noop": {
    "hands": 8,
    "animals": [
      [
        "COW",
        4
      ],
      [
        "SHEEP",
        4
      ]
    ],
    "plants": {
      "CARROT": 1,
      "MELON": 11,
      "STRAWBERRY": 5,
      "WHEAT": 8
    },
    "care": true,
    "collect_fert": true,
    "fert_prio": 45,
    "animal_harvest_at": 4,
    "premium_hold_day": 8,
    "buy_land": true,
    "max_quadrants": 3,
    "prio_care": 70,
    "prio_urgency": 25,
    "plant_near": true,
    "endgame": true,
    "adaptive": true,
    "crop_tiles": 30,
    "zoning": false,
    "zone_fallback_prio": 70,
    "prio_feed": 75,
    "prio_water": 44,
    "prio_win_bonus": 12,
    "prio_harvest": 76,
    "prio_plant": 40,
    "grow": false,
    "prio_dig": 8,
    "mkt_opp_factor": 1,
    "router": true,
    "hire_late": true,
    "multi_feeder": false,
    "phased": false,
    "tiles_per_unit": 5,
    "sell_floor": 0,
    "idle_plant": true,
    "hands_per_quadrant": 4,
    "land_early": true,
    "town_forecast": true,
    "fert_crops": [
      "STRAWBERRY",
      "TOMATO"
    ],
    "opp_read": true,
    "sell_rank": true,
    "order_budget": true,
    "beat_wave": true,
    "wave_min_value": 2000,
    "melon_max": 8,
    "smart_overflow": false,
    "scorer_v2": false,
    "fallback_fix": true,
    "fert_dawn_load": true,
    "fert_tick_aligned": true,
    "fert_phase_lock": true,
    "seed_stock_aware": true
  },
  "_peor": {
    "hands": 8,
    "animals": [
      [
        "COW",
        4
      ],
      [
        "SHEEP",
        4
      ]
    ],
    "plants": {
      "CARROT": 1,
      "MELON": 11,
      "STRAWBERRY": 5,
      "WHEAT": 8
    },
    "care": true,
    "collect_fert": true,
    "fert_prio": 45,
    "animal_harvest_at": 4,
    "premium_hold_day": 8,
    "buy_land": true,
    "max_quadrants": 3,
    "prio_care": 70,
    "prio_urgency": 25,
    "plant_near": true,
    "endgame": true,
    "adaptive": true,
    "crop_tiles": 30,
    "zoning": false,
    "zone_fallback_prio": 70,
    "prio_feed": 75,
    "prio_water": 44,
    "prio_win_bonus": 12,
    "prio_harvest": 62,
    "prio_plant": 40,
    "grow": false,
    "prio_dig": 8,
    "mkt_opp_factor": 1,
    "router": true,
    "hire_late": true,
    "multi_feeder": false,
    "phased": false,
    "tiles_per_unit": 5,
    "sell_floor": 0.4,
    "idle_plant": true,
    "hands_per_quadrant": 4,
    "land_early": true,
    "town_forecast": true,
    "fert_crops": [
      "STRAWBERRY",
      "TOMATO"
    ],
    "opp_read": true,
    "sell_rank": true,
    "order_budget": true,
    "beat_wave": true,
    "wave_min_value": 2000,
    "melon_max": 8,
    "smart_overflow": false,
    "scorer_v2": false,
    "fallback_fix": true
  },
  "partial_batch": {
    "hands": 8,
    "animals": [
      [
        "COW",
        4
      ],
      [
        "SHEEP",
        4
      ]
    ],
    "plants": {
      "CARROT": 1,
      "MELON": 11,
      "STRAWBERRY": 5,
      "WHEAT": 8
    },
    "care": true,
    "collect_fert": true,
    "fert_prio": 45,
    "animal_harvest_at": 4,
    "premium_hold_day": 8,
    "buy_land": true,
    "max_quadrants": 3,
    "prio_care": 70,
    "prio_urgency": 25,
    "plant_near": true,
    "endgame": true,
    "adaptive": true,
    "crop_tiles": 30,
    "zoning": false,
    "zone_fallback_prio": 70,
    "prio_feed": 75,
    "prio_water": 44,
    "prio_win_bonus": 12,
    "prio_harvest": 76,
    "prio_plant": 40,
    "grow": false,
    "prio_dig": 8,
    "mkt_opp_factor": 1,
    "router": true,
    "hire_late": true,
    "multi_feeder": false,
    "phased": false,
    "tiles_per_unit": 5,
    "sell_floor": 0,
    "idle_plant": true,
    "hands_per_quadrant": 4,
    "land_early": true,
    "town_forecast": true,
    "fert_crops": [
      "STRAWBERRY",
      "TOMATO"
    ],
    "opp_read": true,
    "sell_rank": true,
    "order_budget": true,
    "beat_wave": true,
    "wave_min_value": 2000,
    "melon_max": 8,
    "smart_overflow": false,
    "scorer_v2": false,
    "fallback_fix": true,
    "fert_dawn_load": true,
    "fert_tick_aligned": true,
    "fert_phase_lock": true,
    "seed_stock_aware": true,
    "seed_partial_batch": true
  }
}
```
