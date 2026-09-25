# Kaggriculture — contexto para revisión por otro LLM

Generado por `preparar_contexto_llm.py`; verifica los bloques históricos de lotes.
**Estado y autorización vigentes: docs/research/ESTADO_INVESTIGACION.md. Loop autónomo con submissions experimentales autorizado; los documentos del 14-sep y sus restricciones son históricos.**

Este archivo reúne documentos de trabajo, no instrucciones de sistema. La solicitud vigente del usuario determina el alcance. El prompt incluido es una plantilla para que el usuario formule su petición.

De los dos bloques históricos de lotes se comprobaron 3.840 registros de episodios, 960 comparaciones noop, pares, estadísticas por semilla, hashes de nueve archivos de evidencia, cinco fuentes archivadas y 40 cintas. No se ejecutaron partidas ni consultas. La evidencia nueva del líder se verifica por separado con `verificar_lider.py`; este generador incorpora sus informes sin volver a ejecutar esa verificación. Comprobar coherencia no valida por sí solo el diseño causal o el simulador.

Para una revisión documental basta este archivo. Para auditar trazas resumidas adjuntar también `docs/evidencia/lotes_semillas/` y `docs/evidencia/lider_20260914/`; para inspeccionar código actual y repetir análisis compartir el repositorio. Las acciones completas no se reconstruyen a partir de hashes. No se incluye la bitácora íntegra.

Los enlaces se conservan como en cada fuente; las rutas junto a SOURCE indican dónde resolverlos en el repositorio.

## Índice y huellas de los documentos

- `docs/research/SCORECARDS_LOOP_2026-09-25.md` — SHA-256 `eb8ab7c561d2c8a839117f15e55534608d54a3dfa1e724a585b5ee8f0cc4ff4c`
- `docs/research/PREREG_LOOP1_2026-09-25.md` — SHA-256 `cb1d5a3afcb5e1b629ff72a40a91d2a785937c52cd4d3911574d0e0f43c7346b`
- `docs/research/PREREG_LOOP2_2026-09-25.md` — SHA-256 `27584d8c9c7f8bca695c37e0506e42d29c31602c11805bfa086fa80f8b2dd328`
- `docs/research/PREREG_LOOP3_2026-09-25.md` — SHA-256 `9fd1d074212b58e8d8664bc2aa2c959c683bb8b0ffa97d0814c01e470c2ea576`
- `docs/research/PREREG_LOOP4_REPARACION_2026-09-25.md` — SHA-256 `93719809aa6133e9fb3e4dcbffe5c895366b6d93047b25633178bcca7ce508c2`
- `docs/research/PREREG_LOOP5_TOMATE_TEMPRANO_2026-09-25.md` — SHA-256 `6fb66e4527dea8ab81ddb8150d2cb141de51471384ee3245eb04d28c0a871606`
- `docs/research/PREREG_LOOP6_PRODUCTOS_2026-09-25.md` — SHA-256 `7a8a17f2c210a439a9e86a2bcfd0491ee289777011dc94ec53e9cb1306b12c60`
- `docs/research/PREREG_LOOP7_RELLENO_2026-09-25.md` — SHA-256 `ac40ef7f3112c4d8388017b64cc0b7120a8c4186f30b9669fcc5c6fa85f2d2b0`
- `docs/research/PREREG_LOOP8_PATRONES_2026-09-25.md` — SHA-256 `a993c7b152fc3f1b18bca8ba5b244d2825c1ecc67b1839fe9792fc2561b9dba2`
- `docs/research/FEEDBACK_TOP3_2026-09-25.md` — SHA-256 `1be69dc994d85fd92abad16d70163acd31f4cc3b5d26dfe9815b58d90f1ceea2`
- `docs/research/LIDER_Y_FUENTES_2026-09-25.md` — SHA-256 `f940d574bb7e3d43785ee31a100204a8c3a7c7587009f9fcbb02b1ef8df07daf`
- `docs/research/DECISION_ENVIO_TOP3_2026-09-25.md` — SHA-256 `a17b15f6d0db894ec64c3dbd25ce08ac2553f25d2528682b129a1f4a779cbde6`
- `docs/research/RESULTADOS_2026-09-25.md` — SHA-256 `98349e7d3065ae9fb91d396d089c4aa95f1841d5c8b844242add6ba3e8e6965c`
- `docs/research/ESTADO_INVESTIGACION.md` — SHA-256 `836f85ef196caa3ddd19f9533d7dd5b2e5248735c64250ec8c4a0114160eb599`
- `docs/research/RESEARCH_BELIEFS.md` — SHA-256 `289b82abb6b65ea33be71d219ccb8c7024ba3f94ce6cd3fc053d55a1c50b6b8d`
- `docs/research/HARNESS_VS_LEADERBOARD.md` — SHA-256 `bc8c5a4f096242f5d95851275b0e3ba401371edbe85796f447ec2eee94142518`
- `docs/research/SUBMISSION_HISTORY.json` — SHA-256 `abcc963f5888f1598654c17cdcdd9dedf739ded7d17572f5f203717f30c722c0`
- `docs/research/PREREG_VQ_2026-09-24.md` — SHA-256 `7f4b6b42db6dbeeb3981cd0fa56fbf071f4b4f6eec121ceeb292b2b0ca6ebab5`
- `docs/research/PREREG_ADV_2026-09-24.md` — SHA-256 `bed0700878535baaf11409f4dfef3364623943e5e42ecea44fb13b5ebcae4b58`
- `docs/research/PREREG_FORECAST_GATE_2026-09-25.md` — SHA-256 `bf5dd9fbf03de91f1fbf95a557600d969b3c01f143f849271a827abc87cfd2be`
- `docs/research/PREREG_PUBLIC_REFRESH_2026-09-25.md` — SHA-256 `bc60b8ef2b9580510782f1801bcac5e43f4f5c8524f9a39bd9a7c587812a12cc`
- `docs/PROMPT_SEGUNDO_CEREBRO.md` — SHA-256 `e319f3917d23defc367804e464d3d13be14d21061eb2ca73fede8977d4f04c07`
- `AGENTS.md` — SHA-256 `f4ca507f5282b4d01b70c5d3f10fc332c35550eadaeb1d866efcd851eab334dd`
- `docs/ESTADO_ACTUAL.md` — SHA-256 `db1a8944bbb8cf55131e96e009cfb164b38f7f8d72a015135b806a1852ef2e9d`
- `docs/RESULTADOS_LIDER_2026-09-14.md` — SHA-256 `efb3b4c09053f13d648e8019a7ba8363f68a24c234b04b4869754e82877c648b`
- `docs/ANALISIS_LIDER_2026-09-14.md` — SHA-256 `63e3448307868dec34c5c67a697f052f4bc31b4437bc7781b4e702b1d234db53`
- `docs/EXPERIMENTOS_ATREVIDOS_2026-09-14.md` — SHA-256 `da5d98a1afb433c3d2ca6aa11347d212cb8dbcd2a7c43ca8ecfe54bc3ffc544e`
- `docs/evidencia/lider_20260914/README.md` — SHA-256 `d167cefcb9f2cf65dcdabcc8203d99c23e2c9fc1c41df62be78872b8e244e5d0`
- `docs/REVISION_LIDER_PARA_LLM.md` — SHA-256 `9086015c3c33e66ff5362cb4c71b32abcc697d7123715b77184e815dde0b8233`
- `docs/BRIEFING.md` — SHA-256 `450b8b70d8959deedb39a3907ab18ddb5715fa07c92cc24789f07fb4a581ef3d`
- `docs/AUDITORIA_LLM.md` — SHA-256 `f5637e70de4bd1f6427f68b8d4bdfc43b914c16572f005a663a9c813e4a180f0`
- `docs/METODO.md` — SHA-256 `f3dba1825cb10bc6c7d3a668da2c5220f8b198f83a8384a1af7732c55e3231c0`
- `docs/IDEAS_Y_PRUEBAS.md` — SHA-256 `5473112865b0c30da31cf12a8c15b45d02ebf81503df10f35ba1d4d898c6ef9d`
- `docs/RULES.md` — SHA-256 `068679a3a092baecf46c929f6c3f44d31ff3d2ab11be39323d3f59e6d526a268`
- `docs/EXPERIMENTO_LOTES_SEMILLAS.md` — SHA-256 `9aa0937876ed4c4b47f3ae549fba9317af44d46ae478fe2ccdd67e366cb4e01d`
- `docs/evidencia/lotes_semillas/README.md` — SHA-256 `7b4beb82362bb17bd01b39cec158c7596acd36c066ff0df5ff9bf025c0367e3d`


---

## SOURCE: docs/research/SCORECARDS_LOOP_2026-09-25.md

# Scorecards del loop continuo — 2026-09-25 UTC

Estado: loops1–6, confirm1/5 terminados; loop7 corriendo;
loop8 validado y encolado. Objetivo persistente activo.

## Confirmación disjunta terminada

1.600 episodios, noop exacto 416/416, cero errores. Once rivales y 16 semillas.

| Variante | Delta pp | IC95 por semilla | IC95 dos vías | Decisión |
|---|---:|---|---|---|
| pred_top3 | +10,795 | [1,23; 20,36] | [−0,12; 21,71] | REAL_WORLD_CANDIDATE |
| pred_fast2 | +2,841 | [−2,95; 8,63] | [−3,92; 9,60] | PROMISING, gate no cumplido |

Top3: base78,409% →89,205%, 20 celdas mejores y una peor. En ocho rivales
originales +9,375 pp. Peor rival arshs3 −6,25; máximo turno757ms. Mecanismo
favorable y desfavorable reproducidos, dinero conciliado y cero errores.
Ver `DECISION_ENVIO_TOP3_2026-09-25.md`. **Enviada56537205**, commitba1fda8,
01:56UTC, archivo byte exacto; **COMPLETE**, replay de validación720 pasos
DONE/DONE sin errores ni timeouts. Conserva VQ como control activo.
No se mezcla con la investigación productiva en curso.

Snapshot real posterior: VQ2319,5 con24 episodios listados; original2275,7.
No atribuir fuerza relativa al rating aún joven de VQ.

## Piloto loop1

| Variante | Delta pp | IC95 dos vías | Estado |
|---|---:|---|---|
| crop40 | +0.000 | indefinido; no interpretar como cero | INCONCLUSIVE_NOT_SELECTED |
| crop80 | +0.000 | indefinido; no interpretar como cero | INCONCLUSIVE_NOT_SELECTED |
| crop_end26 | -3.125 | [-13.07; +6.82] | INCONCLUSIVE_NOT_SELECTED |
| crop_edge0 | -3.125 | [-13.07; +6.82] | INCONCLUSIVE_NOT_SELECTED |
| pred_top3 | +9.375 | [-7.86; +26.61] | PROMISING |
| pred_h96 | +0.000 | indefinido; no interpretar como cero | INCONCLUSIVE_NOT_SELECTED |
| pred_fast2 | +3.125 | indefinido; no interpretar como cero | PROMISING |
| pred_window6 | -6.250 | [-40.70; +28.20] | INCONCLUSIVE_NOT_SELECTED |

Base: 87,5%; cuatro semillas × ocho rivales × ambos asientos. 1.000 episodios
totales incluyendo directos, noop exacto 128/128, cero errores. Máximo de turno
observado 536 ms: se volverá a mirar en confirmación. Selección fijada en preregistro:
pred_top3 y pred_fast2, ambas PROMISING, no CHAMPION.

Comportamiento: crop40 cambia acciones en 34/64 episodios, crop80 en 50/64,
sin cambiar W/L/T. No son parches inactivos. pred_h96 sí es inerte en estos 64
episodios. pred_top3 y pred_fast2 cambian acciones en 64/64. El intervalo CGM
puede quedar indefinido con este bloque pequeño; no significa ausencia de ruido.

Evidencia: `docs/evidencia/loop_publicos_20260925/pilot.results.json` y
`pilot.behavior.json`. Protocolo: `PREREG_LOOP1_2026-09-25.md`.

Feedback real posterior: VQ 56535264 marca 1967,9 con 14 episodios listados;
original 56511619 marca 2284,3. Lectura joven, aún no ordena las dos políticas.
Snapshots guardados; cuatro replays de VQ seleccionados por extremos de recencia.

La sonda de mecanismo de pred_top3 (ars40, semilla 995002, asiento 0) reproduce
rewards del piloto: margen −1.062 pasa a +292. Primera acción distinta en 559;
predictor pasa de 15 a 24 activaciones y de 112 a 182 unidades anticipadas.
Tiendas idénticas, caja conciliada, sin errores del predictor. Señal compatible
con cobertura de patrones adicionales; no aislar todo el efecto en una sola venta.

De cuatro replays VQ muestreados, tres con asiento identificable son victorias
(+76.819, +4.568, +729). El cuarto tiene ambos jugadores llamados Rospel y seed 0:
se excluye sin asignar submission a un asiento arbitrario. No inferir WR global
ni fuerza rival del margen. El analizador ahora rechaza identidad ambigua.

## Loop2 terminado

616 episodios válidos; noop exacto 104/104; base 90,625% en el pool común.
recover_now, recover_later, tomato12000 y tomato_finite: delta 0 y acciones
idénticas a base en 64/64 episodios. **El panel de cuatro semillas no activó
estas intervenciones**; no es evidencia de que el mecanismo sea inútil.
tomato6000 cambia acciones en 2/64 y pierde 3,125 pp; IC dos vías
[−13,07; +6,82], inconcluso. No hay seleccionada para confirmación de loop2.

El bloque espejo opcional de reparación requería cambios de acción: como no
los hubo, no se lanza automáticamente. La falta de cobertura del mecanismo
raro requiere diagnosticar su activación antes de gastar confirmación ciega.

## Reparación: diagnóstico posterior en bucle cerrado

Cuatro episodios registrados en `recovery_closed_smoke.plan.json`, usando el
seed del fallo observado y arshs3 original como rival **reactivo**, ambos
asientos. En asiento 0 no hay maleza relevante y ambas políticas son idénticas.
En asiento 1 la reparación recupera la planta y el margen pasa de −671 a +53.
Cambian las tiendas posteriores: es efecto total de una intervención en ese
mundo, no el precio aislado de una fresa ni estimación de su efecto medio.
El mecanismo merece evaluar cobertura con más mundos; aún no es candidata
real porque el piloto aleatorio no lo activó y éste es un caso elegido por fallo.

Loop4 registrado posteriormente: 32 semillas aleatorias nuevas, ambos asientos,
base/noop/recover_now/arshs3, 384 episodios. Primero cuantificar cobertura y
efecto por semilla. Su intervalo de dos vías no aplica con un único rival.

## Nuevas fuentes y siguiente familia

Cuatro replays DSM 56518845, elegidos por recencia: 720 estados exactos cada
uno y dinero conciliado. Cuarta tierra día 10, 116–231 tomates vendidos,
composiciones diferentes entre mundos. Ver `LIDER_Y_FUENTES_2026-09-25.md`.
CHA22 y evgendvorkin eran duplicados de tds25; no se repitieron. El notebook
GCN público no mejora en su propio benchmark publicado; prioridad baja.

Loop5: early12_9k, early12_6k, early14_6k, early16_6k y late18_6k. Ventana
completa de siembra/riego/fertilización/cosecha desplazada, oferta rival finita
y criterio de caja explícito. Ocho diagnósticos de desarrollo, seed1004000:
control de transformación de calendario idéntico en 1.438 acciones; temprano
activa diez plantas y vende 60 tomates, sin errores. Noop y base empatan en
comportamiento; la variante temprana pierde ese mundo, no prueba poblacional.
Piloto disjunto 1005000–003 encolado tras loop4, confirmación condicional
1006000–015. Nunca dos torneos grandes simultáneos.

## Loop3: animales terminado

504 episodios, noop exacto 96/96, cero errores. Base 87,5% en pool común.

| Brazo | Delta pp | IC95 dos vías | Episodios con acciones propias distintas /64 |
|---|---:|---|---:|
| herd_future | −84,375 | [−114,33; −54,42] | 62 |
| herd_ev600 | −34,375 | [−95,66; +26,91] | 62 |
| herd_ev1500 | 0 | indefinido | 0 |
| herd_ev_future | −40,625 | [−103,62; +22,37] | 64 |

Ninguna seleccionada; no se gasta confirmación. herd_future REJECTED;
EV600/EV_future son negativos con intervalo amplio, no refutación universal;
EV1500 es inerte en este panel. Intervalos t lineales pueden salir del rango
físico de deltas: se conservan sin presentarlos como probabilidades posibles.
Sonda adicional de herd_future registrada por regla de primera regresión ordenada.

Sonda completada: ars40/1001000/asiento0, primera diferencia step241,
GOOSE2 → COW2. EV de vacas estimado674 →6371 por incorporar tiendas futuras;
observado: leche261 →301 unidades, pero ingreso28.950 →26.820; huevos93 →0.
Margen+1.808 →−2.020, mismas tiendas, caja conciliada, cero errores del módulo.
La variante sí ejecuta su decisión; la evidencia cuestiona la proyección de
valor, no justifica arreglar a ciegas la logística ni presumir que producir más gana.

## Loop6 registrado tras la confirmación top3

Cuatro nuevos brazos sobre top3: extender a EGG, MELON, ambos, y combinar
top3 con fast2. Base/noop top3 y controles VQ/fast2 separados en la misma
muestra, 736 episodios de piloto, confirmación condicional en semillas nuevas.
Primario ahora es mejora frente a top3. Los pilotos productivos ya registrados
mantienen VQ como padre. `continuar_loop_productos.py` espera a loop5.

## Loop4: cobertura de reparación terminada

384 episodios válidos, noop exacto 128/128, cero errores. 32 semillas, ambos
asientos frente a arshs3. Recuperación cambia acciones en **1/64** partidas y
convierte esa derrota en victoria: 93,75% →95,3125%, **+1,5625 pp**,
IC95 por semilla [−1,62;4,75]. No hay intervalo de dos vías con un solo rival.
Una semilla positiva y cero negativas; directo vs VQ50,78125% es diagnóstico.

El preregistro exigía al menos dos semillas positivas para PROMISING: no se
cumple. INCONCLUSIVE; hay mecanismo raro favorable, sin promoción ni envío.
El caso dirigido previo no se suma para superar retrospectivamente ese gate.
La única celda nueva modificada se reprodujo: seed1003008/asiento1, primera
diferencia step186, una planta recuperada y cinco comandos desplazados.
Margen −760 →+42. Cambian las tiendas y la economía de ambos jugadores;
no atribuir su enorme aumento de dinero bruto al valor directo de una planta.

## Loop5: piloto completo, confirma sólo la variante tardía

616 episodios, noop104/104, cero errores. Base90,625%. early12_9k es inerte
en64/64; las otras cuatro cambian acciones en14/64, todas en seed1005002.

| Brazo | Delta pp | IC95 dos vías | Decisión |
|---|---:|---|---|
| early12_9k | 0 | indefinido | Inerte, no seleccionada |
| early12_6k | −18,75 | [−75,60;38,10] | No seleccionada |
| early14_6k | −18,75 | [−75,60;38,10] | No seleccionada |
| early16_6k | −18,75 | [−75,60;38,10] | No seleccionada |
| late18_6k | +3,125 | [−6,82;13,07] | PROMISING, confirmación disjunta |

La señal tardía sólo voltea una celda rival×semilla, frente a tds. Confirm5
seeds1006000–015 y once rivales, 1.152 episodios, ya en curso. Aunque cumpla
el gate frente a VQ, no reemplazar automáticamente al nuevo top3: examinar
comparación y eventual combinación con esa base más fuerte antes de otro envío.

Sonda tds/1005002/asiento0: −220 →+1.521, primera diferencia433, vende80
tomates por10.283. Cambian tiendas y otros productos; efecto total del agente,
no ganancia aislada de tomates. Caja conciliada y rewards exactos del piloto.

## Loop7: relleno SE en desarrollo

Nueva capa conserva filas5–6 del padre y usa4/8 tiles de filas7–8, sembradas
d16/d18, sin fertilizante. Compra sólo semillas/jornales si el modelo cubre
coste+600; no compra otra tierra. Dieciséis diagnósticos v2: noop exacto,
plantas4/8 y cosechas16/32 al forzar la activación, sin errores. Las versiones
normales rechazan invertir en ese mundo por coste. No usar las forzadas como
evidencia de rendimiento ni como candidatas.

Auditoría de jornales detecta interacción no deseada: contratar antes de hora4
bloquea el módulo R51, cuya ventana de HIRE es1–3. V3 espera a hora4 y está
repitiendo validación. V2 y ledgers se conservan. Preregistro de piloto fijado:
16 semillas nuevas×cuatro rivales, 1.248 episodios; no lanzar hasta validar v3.

## Confirm5: el tomate tardío no replica

1.152 episodios, noop384/384, fuentes archivadas verificadas, cero errores.
Late18_6k: base69,886% →48,295%, **−21,591pp**, IC95 semilla[−36,38;−6,80],
dos vías[−36,90;−6,28]. Ninguna celda rival×semilla mejor y38 peores.
Subpanel original−22,656pp; no es daño explicado por añadir tres rivales.
Cambia156/352 partidas repartidas en11 de16 semillas. **REJECTED; no enviar.**

Primer daño por orden fijado: ars40/1006000/asiento0, primera acción distinta433.
Compra tierra y10 semillas, confirma80 tomates cosechados y80 vendidos; caja
conciliada, cero errores. Margen+190→−1.416. Ingreso bruto tomate6.493; tiendas
posteriores cambian, lana y otros ingresos también. No atribuir todo el daño al
coste directo ni rescatar por producir más. Diagnóstico favorable del piloto
predecía ingreso8.288; caso negativo6.010 apenas cruza el umbral6.000.

## Loop7: validación mecánica de inversión en espacio libre

V2 inhibía al fertilizador R51 contratando antes de terminar su ventana; V3
espera a hora4 y conserva un peón/siete aplicaciones, pero un trabajador
lejano perdió cuatro tomates al amanecer por overflow. V4 alterna riego
y cosecha, vende16/16 y32/32 tomates en brazos forzados y conserva ovejas
(108 lanas) y R51.16 juegos completos, noop exacto1.438 acciones.
Cuatro variantes con gate económico son inertes en ese mundo de desarrollo: no
hay evidencia de mejora de rendimiento allí. Versiones forzadas sólo validan
el controlador y están excluidas del piloto/submission. Piloto1.248 encolado,
16 semillas nuevas, cuatro rivales fijados. Manifiesto `infill_variants.json`.

## Loop8: nueva familia en desarrollo

Seis variantes de selección de patrones sobre top3: rank5/7, historia120/360,
patrones por producto y desplazamiento±2 ajustado exclusivamente al pasado.
Piloto1.472 con ocho semillas y ocho rivales; máximo dos a confirmación
disjunta. Protocolo `PREREG_LOOP8_PATRONES_2026-09-25.md`. Validación de
transformación y runtime antes de congelar/encolar.

Desarrollo loop8 completo:16 juegos, noop exacto1.438 acciones, cero errores,
máximo271ms. Todas las variantes cambian acciones; no se selecciona por rewards
en ese mundo dirigido. Piloto encadenado detrás de loop7.

## Loop6: sin selección, base explícita top3

736 episodios, noop112/112, fuentes archivadas, cero errores. Base96,875%.
EGG, MELON y ambos quedan en0pp. EGG y combinado cambian46/64 partidas;
MELON es inerte64/64. No confundir igualdad W/L con ausencia de ejecución.
Top3+fast2:90,625%, −6,25pp, IC95 dos vías[−25,58;13,08], inconcluso sin
selección. No confirm6 ni envío. El techo de este panel reduce sensibilidad
a mejoras pequeñas; no refuta cualquier utilidad de anticipar huevos.

Controles factoriales en el mismo bloque: VQ78,125%, fast2 70,313%, top3
96,875%, top3+fast2 90,625%. Interacción puntual+1,5625pp; fast2 no muestra
ventaja marginal aquí con ninguno de los dos padres. No combinar por sumar
los deltas de confirmaciones distintas. Máximos de los brazos nuevos≤270ms.

## Feedback real top3, muestra fijada02:34UTC

Cuatro completadas recientes, sin filtro por resultado:3V/1D. Márgenes
+26.420 contra Neglected Turtle, −23.180 contra c0nrad, +4.037 contra
StephenNedumpally y +7.776 contra Platycerium.720 pasos cada una, DONE/DONE,
sin estados ERROR/TIMEOUT/INVALID. Cero escapes propios y valor terminal0.
No estima WR global ni compara top3 con VQ; adversarios y edad diferentes.

La derrota tiene cuatro YARN y tres BRUNCH entre las ocho tiendas finales.
Al día15 el rival ya tiene32 ovejas frente a17 nuestras; al día20 posee75.280
frente a56.505. Tiene sólo un tomate tardío: copiar tomate no responde a esta
derrota. Auditoría exacta de transacciones para separar volumen, precio y costes.

Auditoría completada:720 estados exactos×4 y caja conciliada. En la derrota,
lana391/759 unidades y69.502/113.264 de ingreso; rival8.273 de jornales frente
a10.217 propios, tierra3.000 frente a7.000. Hipótesis nueva: especialización
ovina con demanda visible y trabajo marginal viable. Aún no implementada;
ver `FEEDBACK_TOP3_2026-09-25.md`, no repetir herd_future del loop3.



---

## SOURCE: docs/research/PREREG_LOOP1_2026-09-25.md

# Loop continuo 1: producción y extensión de señales útiles

Registrado antes de evaluar. El usuario pidió explícitamente continuar un loop
con muchos experimentos, sin detenerse al cerrar cada ronda. VQ sigue como
referencia local; el original arshs3 y VQ están activos en ladder.

## Hipótesis y riesgos

Base SHA 9b463dfb; constructor `construir_loop_publicos.py`. No se repiten VQ,
ADV, gate/off ni paquetes tds25/hl25. Se aíslan mecanismos dentro de VQ:

| Variante | Cambio | Hipótesis | Potencial / confianza | Riesgo |
|---|---|---|---|---|
| crop40 | Mezcla 40% precio a tres días | Evitar sembrar para un precio que desaparecerá | HIGH / LOW | Oferta futura sobreestimada |
| crop80 | Misma estimación, 80% | Mayor respuesta a la saturación visible | HIGH / LOW | Error de modelo amplificado |
| crop_end26 | Fin de siembra alternativa d26, buffer 6 | Menos capital y semillas que no producen al cierre | MEDIUM / LOW | Perder última cosecha útil |
| crop_edge0 | Margen mínimo 0 en vez de −15 | No sustituir trigo cuando la zanahoria pierde margen previsto | HIGH / LOW | Modelo omite valor de alimento/rutas |
| pred_top3 | Tres patrones rivales en vez de uno | Cobertura de políticas con timing variable | HIGH / MEDIUM | Más falsas alarmas |
| pred_h96 | Venta propia planeada hasta 96 turnos | Aprovechar presión rival aunque la cinta venda más tarde | HIGH / MEDIUM | Renunciar a demanda futura |
| pred_fast2 | Actualizar cada turno, señal mínima dos unidades | Responder a ventas pequeñas y cambios rápidos | HIGH / MEDIUM | Adelantos excesivos y coste CPU |
| pred_window6 | Extensión de 4 a 6 turnos, mismo filtro lejano | Ampliar alcance conservando la protección inmediata | MEDIUM / LOW | Predicción lejana imprecisa |

La idea crop proviene del código público Harvest Ledger (sha 1dfd4630), cuyo
paquete completo no mejoró. Esto aísla valoración, sin adoptar simultáneamente
sus otros cambios. Forecast ablation reveló gran valor de la capa; expandir su
cobertura es una dirección distinta de volver a filtrarla o desactivarla.

## Piloto amplio

Base/noop y ocho variantes; ocho rivales congelados: tds viejo, hybu, ars40,
hsov, v13, obr, h2965, guru6. Semillas **995000–995003**, ambos asientos.
10 brazos y ocho rivales: 80 cruces con pool + 45 entre brazos, **1.000 episodios**.
Métrica primaria delta pareado W/L/T vs VQ en los ocho rivales comunes; otros
brazos excluidos de la estimación. Directos, monedas y hashes son diagnósticos.
No mirar resultados parciales para cambiar la muestra o las variantes.

Seleccionar hasta tres candidatas con delta >0, ordenadas por delta, desempate
alfabético; máximo dos de una familia (crop/pred). Si no hay positiva, continuar
con una nueva hipótesis estructural, sin ampliar este mismo piloto para rescatarlo.
Intervalos amplios no son rechazo automático. Sin cambios W/L/T pero acciones
diferentes = neutral en este panel, no parche inactivo.

## Confirmación

Base/noop más seleccionadas; semillas **996000–996015**, disjuntas. Pool expandido
fijado ahora: los ocho previos + tds25 + hl25 + arshs3 original. Reportar por
separado ocho rivales comunes y tres adicionales; principal = once equiponderados.
Con tres candidatas: (55+10) cruces ×32 = **2.080 episodios**; con dos: 1.600;
con una: 1.152. No cambiar rivales tras ver qué beneficia a cada variante.

Puede justificar REAL_WORLD_CANDIDATE: delta confirmado ≥3 pp y ausencia de
regresión >20 pp por rival, aunque IC cruce cero. Un resultado con daño claro,
bugs o exceso de tiempo se rechaza. Ninguna selección local implica CHAMPION.
Una señal específica grande se documenta para otro experimento, sin cambiar
retrospectivamente esta regla. Si hay varias candidatas positivas, estudiar
combinación en un bloque nuevo que incluya A, B y A+B, con semillas nuevas.

## Integridad

Usar `torneo.py`, `validar_torneo.py`, `pareado_torneo.py`; noop exacto, cero
errores, ambos asientos y fuentes archivadas. No modificar runner/agentes en
ejecución. Controlar máximo de tiempo por turno. Guardar resultados, mecanismos,
estado y siguiente hipótesis antes de pasar al bloque siguiente. Este preregistro
define una ronda del loop, no una razón para detener toda la investigación.



---

## SOURCE: docs/research/PREREG_LOOP2_2026-09-25.md

# Loop 2: siembras fallidas y régimen de inversión en tomates

Registrado mientras corre loop1, antes de evaluar estas candidatas. Reusar
torneo.py; no cambiar el bloque anterior ni sus fuentes. Dos mecanismos nuevos:

## Evidencia y candidatas

Replay 113061732 contra Pand: a paso 185, maleza en (8,1) obliga a DIG en lugar
de PLANT STRAWBERRY. La reparación original abandona el intento al ver un
movimiento después del riego. El agente continúa regando esa casilla vacía.
El rival vende seis fresas adicionales y gana por 718. La atribución causal
exacta debe comprobarse en bucle cerrado, no sólo con este contraste.

Primer prototipo `recover_ongoing` busca otra visita de riego el mismo día;
detecta la intención pero no actúa en este caso: no hay segunda visita ese día.
Se conserva como diagnóstico, no se gasta un torneo en el prototipo inerte.
Nueva reparación inserta PLANT y desplaza un turno un sufijo que contiene sólo
movimientos, WATER y PASS. Exige que el último turno sea PASS o WATER duplicado:
ese turno redundante absorbe el retraso antes del reset nocturno. No añade hires.
Prueba de mecanismo recupera la fresa, pero cambia RNG/tiendas; su W/L contra
acciones grabadas no es evidencia competitiva.

- **recover_now:** fresas/tomates, recuperar el mismo día. Potencial HIGH,
  confianza MEDIUM en mecanismo, LOW en W/L. Riesgo: interacción entre capas y
  posiciones calculadas por la cinta versus acciones finalmente emitidas.
- **recover_later:** todos los cultivos, máximo dos días de retraso. Potencial
  HIGH, confianza LOW; riesgo adicional: cosecha planeada demasiado temprana.

La inversión de tomates ya existe y emplea un umbral de ingresos previstos de
9.000 monedas. Fuente inspeccionada: arshs3, capa shiiin9, Apache-2.0; el
[Meta Atlas público](https://www.kaggle.com/code/leoprovorov/kaggriculture-public-meta-atlas-v2)
señala incertidumbre del supuesto de reposición perpetua del rival. Su snapshot
es 22 septiembre, aunque la ejecución del notebook sea más reciente.

- **tomato6000:** umbral 6.000, estudiar un régimen de inversión más amplio.
  Potencial VERY HIGH / confianza LOW; riesgo de desplazar trabajo rentable.
- **tomato12000:** umbral 12.000, reservar inversión para demanda grande.
  Potencial HIGH / confianza LOW; riesgo de perder oportunidades rentables.
- **tomato_finite:** 9.000, oferta rival sólo hasta el fin biológico de las
  plantas visibles, más producto ya acumulado; corregir el próximo unlock
  esperado de d22 a d21 usando calendario y número de tiendas observado.
  Potencial HIGH / confianza LOW; riesgo: el rival sí puede replantar.

## Diseño y selección

Base/noop VQ + cinco candidatas, ocho rivales congelados iguales al piloto de
loop1; **998000–998003**, ambos asientos. 56+21 cruces, **616 episodios**.
Primario: delta W/L/T en ocho rivales comunes, por celda rival/semilla promediada
sobre asientos; IC95 por semilla y dos vías. Directos y monedas aparte.
Noop exacto, cero errores, fuentes archivadas, tiempos por turno.

Hasta dos candidatas con delta >0, máximo una por familia, orden por delta y
desempate alfabético. Confirmar con **999000–999015**, once rivales fijados: los
ocho del piloto + tds25 + hl25 + arshs3 original. Dos candidatas: 1.600 episodios;
una: 1.152. Candidata real si delta confirmado ≥3 pp sin rival <−20 pp; no exige
que el IC esté completamente sobre cero. No promover CHAMPION automáticamente.

Si una reparación es neutral en W/L/T pero modifica acciones válidas, se permite
un diagnóstico separado de clones por su mecanismo raro: 32 semillas fijadas
**1000000–1000031**, base/noop/una reparación (elegir recover_now por prudencia)
y arshs3 original, todos contra todos, **384 episodios**. Reportar este bloque
por separado; no presentarlo como confirmación del pool ni seleccionar entre
variantes después de mirarlo. Una señal espejo puede justificar estudio real
si conserva W/L/T en el pool y no tiene fallos mecánicos.

Una ronda negativa genera una hipótesis siguiente; no termina el loop solicitado.



---

## SOURCE: docs/research/PREREG_LOOP3_2026-09-25.md

# Loop 3: elegir animales por valor económico y oferta visible

Registrado antes de correr. Revisión de VQ: `_HD2_FUTURE=0` omite demanda
esperada de tiendas futuras en el modelo de elección de gansos/vacas/ovejas.
La capa posterior `_y_target` convierte vacas en ovejas si existe YARN_STORE,
sin valorar el inventario ni la oferta futura del rival. No es el antiguo
barrido de tamaño de rebaño de HOZ; se conserva cantidad y logística del agente
público fuerte y se cambia el criterio de especie en sus compras previstas.

El ledger real 113056789 muestra más leche/lana vendida por nosotros pero
menores ingresos en ambos productos que el rival. No prueba que estas nuevas
reglas lo resuelvan: fundamenta medir oferta y precios conjuntamente.

## Hipótesis

Constructor `construir_herd_loop.py`, base VQ 9b463dfb, atribuciones conservadas.

- `herd_future`: demanda esperada de nuevas tiendas con peso 1 en `_hd2_ev`.
- `herd_ev600`: reemplazar la regla binaria de YARN_STORE por comparación del
  valor previsto de dos vacas versus dos ovejas, incluyendo oferta de ambos,
  precio endógeno y coste. Requiere ganancia modelada de 600. Sólo días 8–11
  y tamaños que la capa heredada ya permitía. Mantiene control de caja y créditos
  de compras efectivas; no convierte estructuras a tipos nuevos.
- `herd_ev1500`: mismo mecanismo con umbral 1.500.
- `herd_ev_future`: EV600 + demanda futura. Factorial parcial permite comparar
  A, B y A+B en vez de asumir aditividad.

Potencial HIGH, confianza LOW. Riesgos: el modelo supone más cuidado del que
ofrece la ruta, usa el mismo calendario de cosecha tras cambiar especie, y
modela imperfectamente reposición/demanda y reacción rival. Diagnosticar cambios
de compras, producción aceptada y precios si aparece señal o daño.

## Diseño

Base/noop + cuatro candidatas, mismos ocho rivales públicos congelados.
**1001000–1001003**, ambos asientos: 48+15 cruces, **504 episodios**.
Primario delta W/L/T pareado; otros brazos excluidos. Noop exacto, cero errores,
fuentes archivadas y máximo por turno. Ejecutar después del pipeline loop1/2,
sin añadir ocho workers a corridas ya activas.

Confirmar hasta dos candidatas con delta >0, orden por delta y nombre, en
**1002000–1002015**, pool fijo expandido a once: ocho originales más tds25,
hl25 y arshs3 original. Dos candidatas 1.600 episodios, una 1.152. REAL_WORLD_CANDIDATE
si delta confirmado ≥3 pp sin rival <−20 pp; IC amplio informado, no veto binario.
Promoción a campeón requiere además evidencia real. Si ninguna mejora, pasar
a otra familia de mecanismos conservando este resultado.



---

## SOURCE: docs/research/PREREG_LOOP4_REPARACION_2026-09-25.md

# Loop 4: cobertura de una reparación rara en mundos nuevos

Pregunta: ¿con qué frecuencia se activa recover_now y qué efecto total tiene
frente a copias reactivas? El piloto de loop2 no activó la reparación en sus
cuatro semillas; no fue una evaluación informativa de ese mecanismo.

Evidencia nueva posterior: en la semilla del fallo real de 113061732, cuatro
episodios frente a arshs3 vivo reprodujeron identidad en asiento 0 y recuperaron
la fresa en asiento 1: margen −671 → +53. Es un caso dirigido y cambia tiendas,
por lo que no estima efecto promedio ni aísla dinero de la planta. Justifica
medir frecuencia/efecto en mundos aleatorios nuevos, no promover el parche.

El espejo opcional original de loop2 exigía activación en su piloto y no se
ejecutará bajo esa regla. Este bloque distinto se registra tras nueva evidencia,
con una pregunta de cobertura y semillas nuevas; no se sumará al piloto como si
fuera confirmación prevista allí. No retocar la variante ni elegir semillas
que contengan maleza después de observarlas.

## Diseño

Base/noop VQ, recover_now congelado de loop2 y arshs3 original. Todos contra
todos, **1003000–1003031**, ambos asientos: 6 cruces ×64 = **384 episodios**.
Usar torneo.py y validar_torneo.py; correr tras pipeline1/2 y loop3, sin otro
torneo grande simultáneo. Primario: delta recover_now vs base contra arshs3,
por semilla promediando asientos. IC95 t por semilla; IC dos vías no aplica
con un único rival. Directo contra VQ es diagnóstico aparte.

Registrar hashes de acciones y proporción de episodios cambiados, errores,
tiempos, número de semillas con mejora/daño y resultados por asiento. Noop exacto.
No cambiar criterio por un directo favorable ni por dinero.

Delta positivo y al menos dos semillas positivas: PROMISING, estudiar mecanismo
de cambios y valorar una prueba real o panel amplio según tamaño/daño. Delta cero
con acciones idénticas: sigue sin cobertura; revisar frecuencia antes de otra
corrida. Daño con intervalo enteramente negativo: REJECTED. Otros resultados:
inconclusos. Este bloque de clones no demuestra mejora universal ni nombra campeón.

La reparación merece conservarse como hipótesis separada aunque las variantes
de predictor mejoren. Cualquier combinación requerirá A, B y A+B en otro bloque.



---

## SOURCE: docs/research/PREREG_LOOP5_TOMATE_TEMPRANO_2026-09-25.md

# Loop 5: invertir antes en una campaña completa de tomates

Motivación: cuatro replays recientes de DSM muestran cuarta tierra al día 10
y producción abundante de tomate. Nuestro piloto de umbrales al día 18 apenas
cambió comportamiento. Probar una fecha productiva distinta, sin copiar las
acciones grabadas como si fueran una política reactiva.

Constructor `construir_tomate_temprano.py`, padre VQ 9b463dfb. Conserva diez
tiles de V219, observación de trabajadores realmente contratados y chequeos
de caja/índices. Cambia campaña completa: siembra, riegos alternos, fertilizante,
calendario de cuadrillas y cuatro amaneceres productivos. Cesa contratación
después de última cosecha; respeta fechas absolutas del resto de la granja.
Modelo de oferta rival finita, futuras tiendas cada tres días, liquidez inicial
6.000 (más chequeo real de presupuesto y reserva 3.000 del request).

| Variante | Siembra | Ingreso mínimo proyectado |
|---|---:|---:|
| early12_9k | 12 | 9.000 |
| early12_6k | 12 | 6.000 |
| early14_6k | 14 | 6.000 |
| early16_6k | 16 | 6.000 |
| late18_6k | 18 | 6.000 |

late18_6k es comparador de calendario: difiere de tomato6000 de loop2 por
liquidez y modelo finito, por eso no es una repetición exacta. El primario sigue
siendo delta W/L/T contra VQ; comparaciones entre brazos son exploratorias.

**Aclaración de desarrollo anterior al piloto:** seed1004000 reveló que otra
capa reactiva de VQ abre SE para seis ovejas al día 12. No figura en futuras
cintas. Early12 puede sustituir esa inversión; las fechas tardías ya encuentran
SE ocupado y no se activan. El experimento mide efecto total de asignación de
tierra/capital más calendario, no una fecha aislada. No ocultar este coste de
oportunidad ni declarar mejor inversión por el ingreso bruto de tomates.

Antes del piloto: ocho episodios de desarrollo, seed **1004000**, ambos
asientos contra arshs3 original, base/noop de transformación de calendario/
early12_6k/late18_6k. Noop conserva fechas, proyección y liquidez originales;
debe emitir exactamente las mismas acciones. Comprobar ramas/plantas/cosechas,
errores y conciliación de caja. Si la intervención no se activa en ese mundo,
diagnosticar elegibilidad; no usar su W/L/T como criterio de selección. Si hay
defecto, versionar corrección y repetir solamente validación necesaria antes
de congelar el piloto, dejando constancia del defecto y los hashes.

Piloto: cinco variantes + base/noop VQ, ocho rivales habituales, **1005000–003**,
ambos asientos, 616 episodios. Ejecutar tras loop4, sin segundo torneo grande
simultáneo. Torneo/validación/pareado existentes, fuentes congeladas antes de
empezar. Reportar activación por hashes y por siembras observadas; no usar
monedas para rescatar delta W/L/T agregado negativo.

Seleccionar hasta dos brazos de mayor delta estrictamente positivo, sin exigir
significación en este piloto pequeño. Confirmación **1006000–015**, once rivales
de confirm1: 1.152 episodios si uno, 1.600 si dos. Semilla como unidad y ambos
asientos; IC95 por semilla y dos vías si estimable. No elegir rivales a posteriori.

Gate de candidata real: delta confirmado ≥3 pp, ningún rival <−20 pp,
acciones válidas, runtime admisible y revisión de mecanismo. IC cruzando cero
se informa como incertidumbre; no convierte una señal útil en CHAMPION ni es
un veto absoluto a experimentar en ladder. Mantener los registros negativos.



---

## SOURCE: docs/research/PREREG_LOOP6_PRODUCTOS_2026-09-25.md

# Loop 6: cobertura de productos y combinación del predictor

Nueva base local de esta ronda: **top3 confirmado**, sha9668e30a, enviado como
56537205. No cambiar los padres de loops3–5, que siguen VQ según su preregistro.
Se pregunta qué mejora a top3, no qué vuelve a superar a un padre más débil.

Constructor `construir_forecast_productos.py`, cuatro brazos:

- top3_egg: incluye EGG en las anticipaciones. Curva hinge y producción frecuente;
  riesgo de vender antes de escasez mayor o contar oferta poco informativa.
- top3_melon: incluye MELON. Cosechas grandes y concentradas pueden hundir precio;
  riesgo de abandonar la ventana prevista de demanda.
- top3_egg_melon: ambas coberturas, para detectar interacción y competencia por
  slots de mercado. No inferir efecto de la suma sin evaluarla.
- top3_fast2: top3 + umbral2/actualización cada turno. Fast2 solo dio +2,841pp
  vs VQ en confirm1, sin pasar gate; ésta es una prueba nueva de interacción,
  no una reinterpretación ni repetición de su confirmación individual.

Piloto: base/noop top3, cuatro brazos nuevos y controles VQ/fast2 solos;
ocho rivales habituales. **1007000–003**, ambos asientos: ocho brazos×ocho
rivales +28 cruces entre brazos, **736 episodios**. VQ, A=top3, B=fast2 y A+B
conviven en la misma muestra; ambos brazos de producto y su combinación también.
Los controles VQ/fast2 no son rivales del estimador principal ni candidatos a
selección. Reportar sus deltas frente a top3 como contraste experimental.

Métrica primaria: delta W/L/T contra top3, ocho rivales equiponderados, unidad
semilla con ambos asientos. Semillas disjuntas de desarrollo y rondas previas.
Seleccionar hasta dos brazos nuevos con delta>0 (orden delta, empate alfabético).
CI por semilla y dos vías si estimable; registrar activación/hash/runtime/errores.
No aumentar muestra ni cambiar productos por resultados parciales.

Confirmación condicional **1008000–015**, once rivales fijados en confirm1,
base/noop top3 más seleccionadas: 1.152 si una, 1.600 si dos. Gate de prueba
real: ≥3pp contra top3, ningún rival<−20pp, ejecución válida, runtime y mecanismo
revisados. No garantizar superioridad de ladder por diferencias de panel.

Runner `continuar_loop_productos.py` espera a loop5. No lanzar segundo torneo
grande. No incluye envíos automáticos: antes de otro envío considerar evidencia
y edad de top3/VQ activos, coste de perder un control y cupo real disponible.



---

## SOURCE: docs/research/PREREG_LOOP7_RELLENO_2026-09-25.md

# Loop7: tomate en tierra ya comprada, sin sustituir al padre

Hipótesis nueva tras inspeccionar la interacción de loop5: utilizar cuatro u
ocho tiles vacíos de las filas7–8 del cuadrante SE, sin comprar tierra ni
ocupar las filas5–6 de ovejas/V219. Padre **top3**, sha9668e30a. Las variantes
del loop5 siguen congeladas y no se modifican por esta idea posterior.

Cuatro brazos: infill4_d16, infill8_d16, infill4_d18, infill8_d18. No usan
fertilizante: cuatro producciones por planta, riego en edades0/2/4/6/8/10
y cosechas de dos unidades en edades9/11. Una cuadrilla adicional por grupo de
cuatro plantas. Contratar sólo cuando finalicen las contrataciones nativas y
los proyectos existentes hayan reservado sus trabajadores; usar índices
observados y confirmar contratación. Comprobar tiempo de siembra+riego y
preservar las acciones de trabajadores anteriores.

Inversión sólo si ingreso modelado ≥ semillas+jornales proyectados+600. Oferta
visible de ambos jugadores con vida finita, expectativas de tiendas futuras,
coste de peones por día y reserva de caja actual4.000. El modelo omite decisiones
futuras no observadas y el efecto sobre otros proyectos/precios, por lo que el
beneficio calculado es criterio experimental, no una garantía de rentabilidad.

Fuente `capa_tomate_relleno.py`, constructor `construir_tomate_relleno.py`.
Antes de simulación, revisión estática corrigió acumulación del coste de HIRE
del padre y venta posterior a la última cosecha. Los cuatro prototipos v1 no
se evaluaron. V2 completó16 diagnósticos, pero la auditoría de jornales detectó
que contratar en horas1–3 inhibía al fertilizador R51 del padre: exige que todos
los trabajadores actuales pertenezcan a módulos que conoce. **V3 contrata sólo
desde hora4**, tras cerrar la ventana R51, y conserva las comprobaciones de
tiempo/índices. Repetir16 diagnósticos por esta corrección antes del piloto.
V3 pasó16 diagnósticos y conservó R51 (un peón/siete aplicaciones), pero el
caso forced8 vendió28 de32 tomates: al amanecer28 perdió cuatro por overflow.
Flujo guardado en `infill_v3_forced8_flow.json`. **V4 separa riego y cosecha**
durante madurez: WATER8, HARVEST9 (dos unidades), WATER10, HARVEST11 (dos).
Mismos ocho días de contratación, más tiempo para entregar; modelo económico
ajustado a ventas agrupadas9/11. Repetir validación de conservación/venta antes
del piloto. No modificar V2/V3 archivados ni sus resultados. Noop con tamaño0 y dos variantes forzadas
sólo para comprobar ejecución; jamás incluirlas en el piloto ni subirlas.

Desarrollo: seed1004000 ya conocida como mundo SE con ovejas; ocho brazos
(base, cuatro normales, noop, dos forzados)×ambos asientos =16 episodios. No
inferir rendimiento de esa elección dirigida. Conciliar caja, confirmar
plantas/cosechas, observar supervivencia del proyecto ovino, cero errores.
Un defecto observado exige corregir/versionar y validar antes de congelar.

Piloto de cobertura: **1010000–1010015**, ambos asientos, cuatro rivales fijados
ahora: arshs3 original, tds, hybu y ars40. Base/noop top3 +cuatro brazos nuevos:
24 cruces con pool +15 entre brazos, ×32 =**1.248 episodios**. Mayor número de
mundos para activar condiciones espaciales/económicas, sin seleccionar semillas
que contengan tiendas concretas. Reportar proporción de acciones cambiadas;
primario delta W/L/T contra top3 en cuatro rivales comunes, unidad semilla.

Seleccionar hasta dos brazos con delta>0, orden delta y empate alfabético.
Confirmación disjunta **1011000–1011015**, once rivales de confirm1 y ambos
asientos; 1.152/1.600 episodios según una/dos seleccionadas. Reportar además
subpanel de los cuatro rivales del piloto. IC95 por semilla y dos vías cuando
estimable. Gate real ≥3pp frente a top3, ningún rival<−20pp, controles y runtime
válidos, revisión de mecanismo. No promover por dinero bruto o por los casos
forzados de desarrollo. Una activación rara sin efecto deja la pregunta abierta.

Runner espera a loop6, nunca dos torneos grandes simultáneos. No incluye envíos
automáticos; considerar edad/evidencia de top3 y VQ antes de desplazar una activa.

Validación V4 completada:16 episodios, noop1.438 acciones idénticas, R51 siete
aplicaciones y108 lanas del proyecto preservadas. Forzados4/8 cosechan/venden
16/32 unidades. Sin errores ni contrataciones faltantes. Cuatro normales
inertes por gate económico en este mundo dirigido; no usarlo como selección.
Manifiesto congelado `infill_variants.json`; fuentes v2/v3/v4 archivadas en
`infill_development.sources.tgz`. Piloto encolado detrás de loop6.



---

## SOURCE: docs/research/PREREG_LOOP8_PATRONES_2026-09-25.md

# Loop8: selección de patrones del rival

Referencia top3 byte exacto sha9668e30a, independiente de resultados aún no
terminados de loops6–7. El beneficio confirmado de top3 frente a top1 sugiere
que reconocer varias rutas de venta merece una segunda ronda. Seis brazos:

- rank5/rank7: ampliar el conjunto de patrones que pueden anticipar una venta.
- history120/history360: adaptar con menos o más historia observada; el H48 de
  ventas propias permanece intacto. No repite pred_h96 del loop1.
- product3: escoger tres patrones por producto, evitando que el ajuste de lana
  determine el de leche. Requiere tres eventos observados de ese producto;
  en caso contrario conserva selección global. Misma tolerancia temporal±1.
- phase2: ajustar cada patrón por −2/−1/+1/+2 turnos sólo si mejora su ajuste
  pasado en más de2 unidades, después de penalización0,25×desplazamiento.

No cambia la oferta productiva, los productos autorizados, el umbral K4, la
ventana extendida ni el ritmo de recomputación. No usa observaciones futuras;
las cintas futuras de referencia son la biblioteca pública ya empaquetada.
El ajuste usa exclusivamente ventas observadas antes del callback actual.

Desarrollo antes del piloto: base, control de transformación global240/top3
y seis brazos, seed1012000, ambos asientos frente a arshs3 reactivo =16 juegos.
El control debe preservar1.438 acciones y ambos rewards. Cero errores, observar
telemetría de ajuste, medir máximo tiempo por callback y conciliación de caja.
Fallo mecánico se corrige/versiona antes de congelar. Rendimiento de este mundo
es diagnóstico, nunca criterio de selección.

Piloto: **1013000–1013007**, ocho rivales fijos de loop1, ambos asientos,
base/noop+seis candidatas:92 cruces×16=**1.472 episodios**. Se amplía de antemano
a ocho mundos para disminuir dependencia de cuatro semillas. No selección
adaptativa de rivales. Primario delta W/L/T frente a top3, unidad semilla;
reportar intervalos por semilla/dos vías y cobertura de cambios de acciones.
Seleccionar hasta dos positivas, orden delta descendente y empate alfabético.

Confirmación disjunta **1014000–1014015**, once rivales de confirm1 y ambos
asientos:1.152/1.600 episodios. Gate≥3pp en once rivales, ninguno<−20pp,
controles y runtime válidos, revisión de un mecanismo favorable y desfavorable
si existe. Lo local no garantiza ladder; examinar feedback real antes de gastar
otro envío. No modificar agentes después de comenzar un bloque.

Encolar detrás de loop7; un único torneo grande a la vez. No hace envíos
automáticos. Nuevas hipótesis, datos y hashes quedan archivados para no repetir.

Validación terminada:16 juegos, control de transformación con1.438 acciones
idénticas y rewards iguales; cero errores, máximo270,8ms entre estos callbacks.
Todas las seis variantes cambian acciones; product3 registra833 ajustes por
producto/asiento, phase2 usa114 patrones desplazados/asiento. Esto confirma
ejecución en el mundo de desarrollo, no mejora. Fuentes completas archivadas
en `patterns_smoke.sources.tgz`, manifiesto `patterns_variants.json`; runner
encolado tras loop7. Runtime se revisará también en los bloques aleatorios.



---

## SOURCE: docs/research/FEEDBACK_TOP3_2026-09-25.md

# Primer feedback real de top3

Snapshot de submissions **2026-09-25 02:33:17 UTC**: top3 56537205 en1459,1;
VQ56535264 en2306,3. Top3 llevaba unos37 minutos. Listado02:34:01UTC devuelve
diez episodios, incluida validación113099118. Estos ratings no ordenan dos
políticas maduras. Fuente API cruda `ladder_snapshot_0233.txt`; el sufijo0236
del archivo de episodios es un nombre, no su hora real.

Selección fijada antes de descargar resultados: las cuatro completadas más
recientes por createTime, excluyendo validación conocida. No se filtró W/L.

| Episodio | Rival | Margen propio | Estado |
|---|---|---:|---|
| 113108628 | Neglected Turtle | +26.420 | DONE/DONE |
| 113107623 | c0nrad | −23.180 | DONE/DONE |
| 113107458 | StephenNedumpally | +4.037 | DONE/DONE |
| 113106269 | Platycerium | +7.776 | DONE/DONE |

Los cuatro se reprodujeron con **720 estados exactos**, motor1.32.7 y acciones
reales de ambos jugadores. Todas las transacciones aceptadas están registradas;
3.000 más flujo de caja coincide con ambos rewards. Cero ERROR/TIMEOUT/INVALID,
escapes propios0 e inventario propio final0. No es una estimación fiable de WR
global ni una comparación causal con VQ. Tampoco prueba ausencia de acciones
inútiles o pérdidas intermedias de inventario.

## La derrota contra c0nrad apunta a asignación productiva

Primeras tiendas YARN/YARN; al final cuatro YARN, tres BRUNCH y una PIZZA.
Al día15 el rival tenía32 ovejas y3 vacas, nosotros17 y6. Al día20 el dinero
era75.280 frente a56.505; terminó132.832 frente a109.652. Sólo tuvo un tomate
tardío. La hipótesis «nos ganan por tomate» no explica esta partida.

| Venta aceptada | Nosotros: unidades / ingreso | Rival: unidades / ingreso |
|---|---:|---:|
| Lana | 391 / 69.502 | 759 / 113.264 |
| Fresa | 244 / 29.825 | 86 / 11.003 |
| Leche | 134 / 4.294 | 83 / 4.370 |
| Melón | 72 / 16.425 | 90 / 14.119 |
| Fertilizante | 373 / 11.154 | 329 / 14.769 |
| Tomate | 0 / 0 | 8 / 536 |

El rival vendió368 lanas adicionales y cobró43.762 más por lana, pese a un
precio medio menor (149,2 frente a177,8). Nuestra ventaja en fresa no compensó.
Gastó menos en jornales:8.273 por274 contrataciones frente a10.217 por307;
y3.000 en tierra frente a7.000. Compró368 unidades de trigo frente a259:
más producción exigió más alimento, pero no más jornales agregados en ese mundo.

Esto sugiere estudiar densidad y calendario ovinos cuando la demanda ya es
visible, junto con el coste marginal de alimentar/cuidar/transportar. No justifica
forzar ovejas en todos los mundos, copiar la cinta rival ni subir una variante
sin comparación reactiva. Loop3 ya mostró daño de extrapolar tiendas futuras;
no repetir ese criterio bajo otro nombre.

La evaluación espacial de tomates loop7 y los seis predictores loop8 continúan
según sus protocolos. Siguiente hipótesis estructural a diseñar: uso de espacio
libre para un rebaño adicional pequeño, o reasignación de trabajo bovino con
demanda observada de lana, contabilizando jornales Fibonacci y capacidad de
alimentación. Aún no hay implementación, protocolo ni prueba de esa hipótesis.

Evidencia: `top3_replay_selection_0236.json`,
`top3_accepted_transactions_0234.json`, `top3_*.ledger.jsonl.gz`, hashes de
replays en cada resumen. Reconstrucción: `auditar_replays_top3.py`; utiliza
el ledger aceptado de `sonda_fallo_forecast.run`. El antiguo `ventas_reales.py`
no se utilizó: su aproximación con precios previos y órdenes emitidas no es
equivalente a transacciones aceptadas por el motor.



---

## SOURCE: docs/research/LIDER_Y_FUENTES_2026-09-25.md

# Líder actual y fuentes públicas — 2026-09-25 UTC

Consulta reproducible ~01:36 UTC, separada de los replays históricos del primer
lugar. DSM figura con **3128,7**, mejor submission **56518845**, 112 episodios
listados. Su submission más reciente es otra; no confundir fecha de equipo con
identidad del agente que sostiene el mejor score.

Se eligieron los **cuatro episodios completados más recientes, sin filtrar
resultado**: 113091953, 113086007, 113079205, 113073385. Dos rivales distintos;
cuatro victorias no constituyen su WR general. Reproducción oficial de ambas
cintas: 720 estados exactos en cada replay y dinero conciliado con transacciones
aceptadas. Hashes, selección y ledgers en
`docs/evidencia/loop_publicos_20260925/dsm_current_analysis.json` y
`dsm_*.ledger.jsonl.gz`. Script: `minar_lider_actual.py`.

| Replay | Rival | Margen DSM | Tomate vendido DSM/rival | Ingreso tomate DSM/rival |
|---|---|---:|---:|---:|
| 113091953 | 吃白饭的大肥鱼 | +10.333 | 211 / 120 | 16.867 / 9.028 |
| 113086007 | DECEM | +8.888 | 116 / 68 | 6.308 / 3.626 |
| 113079205 | 吃白饭的大肥鱼 | +10.096 | 231 / 144 | 15.980 / 9.460 |
| 113073385 | DECEM | +5.348 | 134 / 136 | 7.354 / 7.200 |

Hallazgos observados:

- Cuarto cuadrante en día 10, con sólo 9–319 monedas restantes a esa altura.
  Máximo de 12 peones. La inversión productiva es anterior a nuestro módulo
  opcional de diez tomates del día 18. **Corrección posterior:** nuestra base
  también tiene una ampliación adaptativa de ovejas al día 12; no afirmar que
  siempre espera al 18 para abrir tierra. Véase diagnóstico siguiente.
- Ya tiene 4–10 tomates al día 10; llega a 14–32 según partida y momento.
  Adapta ganado y cultivos: por ejemplo 18 ovejas frente a DECEM en un mundo,
  12 vacas y 5 gansos al día 10 en otro. No copiar una composición universal.
- Los cuatro juegos tienen 5/16/7/8 escapes. Muchos son tardíos; la traza por sí
  sola no distingue abandono deliberado de fallo. «Cero escapes» no es una
  función objetivo válida sin valorar cuidados, producción futura y trabajo.
- Las acciones de unidades difieren en cientos de turnos entre juegos, desde
  los pasos 25/42/78. Hay rutas/comportamiento diferentes según mundo; esto no
  revela su algoritmo ni demuestra aprendizaje automático.

Interpretación: estudiar producción y asignación de capital, además del timing
de ventas. Los tomates explican parte de varias diferencias económicas, pero
**no se ha identificado causalmente el mecanismo que hace ganar a DSM**. El
cuarto replay gana con prácticamente igual cantidad de tomates. Una intervención
local cambia RNG, tiendas, rival reactivo y otros ingresos: medir efecto total.

Primera hipótesis implementable: desplazar coherentemente nuestra campaña
V219 a días 12/14/16, con su riego, fertilización y ventana finita de cosecha.
Se limita inicialmente a diez tiles; no replica la explotación completa de DSM.
Comparar también día 18 con igual modelo económico para separar calendario de
criterio de inversión. Riesgos: precios todavía bajos, peones marginales caros,
agotamiento de caja y conflicto con obligaciones del padre.

Diagnóstico posterior `early_tomato_qualification.json`, seed1004000: al día
12 VQ tiene SE cerrado y 13.089 monedas; al día 14 ya hay seis ovejas allí,
colocadas el día 12. No aparecen como BUY_LAND en las cintas futuras porque
provienen de otra capa adaptativa. El chequeo heredado de futuras cintas no
detecta este coste de oportunidad. El brazo temprano toma ese espacio antes,
siembra diez tomates y vende 60, pero pierde frente al original en ambos
asientos de desarrollo. Por tanto, el loop5 mide también sustitución de una
inversión productiva: no atribuir su efecto sólo a días de cosecha. La versión
tardía no se activa en ese mundo porque SE ya está abierto y ocupado, aunque
su ingreso proyectado supere el umbral. Ésta es una razón de cobertura real,
distinta de una proyección económica demasiado conservadora.

## Fuentes públicas examinadas, sin repetir experimentos

Lista de notebooks recientes y descargas congeladas en el mismo directorio de
evidencia (`public_notebooks_latest.json`, `public_deduplication.json`,
`public_source_review.json`). No se ejecutaron notebooks externos.

- [CHA22](https://www.kaggle.com/code/abhinav0370/cha22-agent): main idéntico byte
  por byte a tds25, ya evaluado. No repetir por el nombre.
- [evgendvorkin](https://www.kaggle.com/code/evgendvorkin/kaggriculture): mismo
  texto normalizado y AST que tds25; diferencia CRLF/LF. No repetir.
- [Graph reinforcement learning](https://www.kaggle.com/code/djamilabenchikh/graph-reinforcement-learning):
  residual GCN/DQN sobre V16 para aplazar ventas, 18 partidas de entrenamiento.
  Su salida pública informa media pareada 0,0 y 0/4 pares positivos frente a
  V16, criterio monetario. Se auditó main sin ejecutarlo: no merece desplazar
  todavía las pruebas de hipótesis con mecanismo concreto. No se afirma que
  todo RL sea inútil ni se lo declara refutado sin torneo propio.



---

## SOURCE: docs/research/DECISION_ENVIO_TOP3_2026-09-25.md

# Decisión de prueba real: VQ + predictor top3

**Enviada 56537205**, 2026-09-25 01:56:34 UTC, commit `ba1fda8`.
**COMPLETE**, verificado ~02:04 UTC. Replay de validación113099118: 720 pasos,
DONE/DONE, sin errores ni timeouts. Recibo confirma tres envíos restantes.

Envío experimental autorizado por el loop autónomo. Archivo exacto de
confirmación: `submission/main_publico_arshs3_vq_top3.py`, SHA-256
`9668e30ad08f79d485bd230a3c660d4cc420b9382e87f9387b6908e3c94a5145`.
Constructor `construir_loop_publicos.py`, cambio `_V92_P_TOP=3` frente a 1.
Se conservan avisos de licencia y atribuciones del padre público Apache-2.0.

Piloto: +9,375 pp, cuatro semillas y ocho rivales. Confirmación disjunta:
16 semillas, once rivales, ambos asientos; base 78,409%, candidato 89,205%,
**+10,795 pp**. IC95 por semilla [1,234; 20,357], dos vías
**[−0,115; 21,706]**. 20 celdas rival×semilla mejoran y una empeora. En los
ocho rivales originales: +9,375 pp, sin regresión por rival. Panel expandido:
peor rival arshs3 −6,25 pp, mejor tds25 +31,25. No se promete ese salto en Elo.

Cumple gate registrado ≥3 pp y ningún rival <−20 pp. Noop exacto 416/416,
1.600 episodios completos, cero errores, fuentes archivadas verificadas.
Máximo local 757 ms por turno con ocho workers; dentro del segundo nominal,
pero el servidor de Kaggle puede tener rendimiento distinto. Copia byte exacta
al archivo de envío, sin incorporar ningún experimento posterior.

Mecanismo favorable ya reproducido en piloto: primera diferencia en step559,
venta de leche anterior a la presión rival; margen −1.062 → +292, tiendas
iguales y caja conciliada. Se revisó también la única celda negativa de
confirmación: arshs3, seed996011, asiento0, +216 → −425. Primera venta adelantada
de leche step392; 24 turnos de acciones distintos, mismas tiendas y cero
errores. Más cobertura de patrones también causa anticipaciones perjudiciales;
no se oculta ese intercambio ni se culpa a un fallo de ejecución inexistente.

pred_fast2 queda PROMISING (+2,841 pp), sin superar el gate principal. No se
redondea a 3 ni se rescata por +4,688 pp en el subpanel original.

Estado real previo al envío: VQ56535264 2319,5 con 24 episodios listados,
arshs3 original56511619 2275,7. VQ es joven y la lista incluye validación;
no prueba aún que VQ supere al original. El próximo envío desplaza al original
y conserva VQ como control activo, que es el padre exacto de top3. Ambas
políticas quedan archivadas para recuperación. La incertidumbre real se
resolverá con emparejamientos de ladder, además de seguir investigando.

Evidencia: `confirm1.results.json`, `confirm1.validation.json`,
`confirm1.pred_top3.mechanism.json`, `pilot.pred_top3.mechanism.json`,
`top3_package.json` y snapshots API en `docs/evidencia/loop_publicos_20260925/`.
ID, fecha, commit y lecturas posteriores se registran en SUBMISSION_HISTORY.



---

## SOURCE: docs/research/RESULTADOS_2026-09-25.md

# Revisión y experimentos — 25 septiembre UTC / 24 septiembre Colombia

**Decisión:** mantener arshs3 original (56511619) y medir en ladder la nueva
arshs3+VQ (56535264). VQ está COMPLETE. Ninguna de las cuatro candidatas medidas
en esta ronda justifica otro envío. El próximo trabajo debe aprender de derrotas
actuales y aislar un mecanismo nuevo, conservando la predicción de ventas.

## Punto de partida y envío

Se revisaron los cambios hasta a9f59ee, el estado de investigación, las creencias,
el historial de submissions, la bitácora y los protocolos VQ/ADV. La bitácora
principal terminaba en septiembre 14, mientras la investigación reciente estaba
en `docs/research/`. Se actualizaron las entradas para evitar seguir planes vencidos.

La primera consulta de esta ronda encontró arshs3 en **2292,5 / 148 episodios**
y v13 en **1857,9 / 136**. Es evidencia favorable al orden local arshs3 > v13,
sin calibrar una conversión de victorias locales a Elo ni demostrar superioridad
contra la cima del ladder.

Se envió el archivo ya guardado y validado
`submission/main_publico_arshs3_vq.py`, commit **a9f59ee**, SHA-256
`9b463dfb8076b4c63946e1ae4249cd1cfc3cc58b63115cf2bd5b00f96f188976`.
Submission **56535264**, 2026-09-25 **00:22:43 UTC**, COMPLETE.
La CLI informó cuatro envíos restantes. Desplazó a v13 y conservó arshs3 como
referencia activa. `submission/main.py` sigue siendo el original.

La evidencia previa de VQ se verificó sin repetir sus partidas: 0/120 celdas
cambian W/L/T en el pool, pero 40-0 en una confirmación espejo y bloques
adicionales favorables. ADV ya había fallado su confirmación; tampoco se repitió.

Última consulta al cerrar la ronda: original **2288,6**, VQ **1198,5**; edades
muy distintas y número de episodios sin actualizar en esa consulta. El rating
inicial de VQ fue 810. No usar estas lecturas tempranas para decidir su fuerza.
No se programó monitoreo automático.

## Experimentos nuevos

Cada bloque contiene 608 episodios: base/noop/dos candidatas, ocho rivales
congelados, ocho semillas y ambos asientos. La tabla usa únicamente el panel
común de ocho rivales, 128 episodios por brazo; los duelos entre brazos se
informan aparte. Puntuación W/L/T = 1/0/0,5. Delta en puntos porcentuales.

| Bloque / candidata | Base VQ | Candidata | Delta | IC95 dos vías | Decisión |
|---|---:|---:|---:|---:|---|
| Forecast / gate | 76,56% | 25,00% | −51,56 | [−78,92; −24,20] | REJECTED |
| Forecast / off | 76,56% | 7,81% | −68,75 | [−89,57; −47,93] | REJECTED |
| Públicos / tds25 | 92,19% | 84,38% | −7,81 | [−27,29; +11,67] | Inconcluso, no seleccionado |
| Públicos / hl25 | 92,19% | 82,81% | −9,38 | [−29,79; +11,04] | Inconcluso, no seleccionado |

Las semillas difieren entre bloques: 990000–990007 y 992000–992007.
La diferencia entre los porcentajes de la base muestra sensibilidad a la semilla;
no comparar porcentajes entre bloques como si fueran efectos de una intervención.
Los intervalos por semilla, desglose por rival y celdas están en los JSON de resultados.

**Forecast:** gate exige un historial mínimo de aciertos también a predicciones
inmediatas; off desactiva `_v92_predict`. Ambas variantes empeoran claramente
en este panel. No se ejecutó el bloque de confirmación ni se enviaron.

**Públicos actualizados:** se descargaron versiones distintas de
[tds](https://www.kaggle.com/code/tetsutani/demand-preserving-turn-sale-timing)
(SHA 127ed3e6) y
[Harvest Ledger](https://www.kaggle.com/code/haodou092/kaggriculture-harvest-ledger)
(SHA 1dfd4630), publicadas el 24 de septiembre. tds cambia sustancialmente su
paquete de política y colas; HL cambia el cálculo de precios futuros para
producción y parámetros de siembra. Se conservaron atribuciones Apache-2.0.
Ninguna supera el umbral registrado de +5 puntos, dos rivales positivos y
ninguno por debajo de −20. No se gastaron los 864 episodios de confirmación.
Los intervalos amplios no demuestran una regresión universal de estas versiones.

En directo tds25 gana 10/16 a VQ, pero pierde globalmente frente al pool;
hl25 gana 6/16. Seleccionar por el directo después de ver el agregado negativo
cambiaría el criterio registrado. No se hizo.

## Qué aprendimos del agente fuerte y de nuestros errores

Se descargaron 24 replays elegidos por recencia: 16 arshs3 y ocho v13.
Arshs3 obtiene 4 victorias, 11 derrotas y un empate en esa ventana, sin escapes
de animales propios y sin stock final propio sin vender. Esta ventana reciente
no estima su WR histórico ni contiene el Elo de los rivales.

**Corrección de medición:** la primera sonda del predictor contó 12/67 señales
con flujo rival inferido en t+1..t+4. Omitía las ventas simultáneas del turno t.
Se reprodujeron cuatro replays con las acciones reales, verificando los **720
estados** de cada uno y conciliando los flujos de caja de ambos jugadores.
El ledger de ventas aceptadas da **50/67 coincidencias en t..t+4**, de las cuales
**42/67 ocurren en t**. La cifra anterior se conserva como evidencia del error,
no como precisión válida. Una coincidencia no prueba por sí sola el beneficio
causal de una venta anticipada. La reconstrucción de la política difirió en una
acción de un replay (SELL WHEAT, paso 623); el ledger usó las acciones grabadas
y sí reprodujo exactamente los estados.

**Mecanismo local:** primera celda ordenada donde base gana y gate pierde:
ars40, semilla 990000, asiento 0. Primera divergencia en paso 440: VQ vende dos
lanas y gate espera; el rival también vende dos lanas ese mismo turno. Se
reproducen los resultados originales: margen **+89 → −78**. Las cantidades
totales vendidas por producto son idénticas; cambia el dinero cobrado por timing,
principalmente después en fresas. No atribuir toda la diferencia a esas primeras
dos lanas: las decisiones posteriores también divergen.

Esto respalda conservar el predictor y estudiar precios ejecutados y ventas
simultáneas. La observación de acciones, el flujo neto de inventario y el dinero
efectivamente recibido responden preguntas diferentes.

## Evidencia, validación y coste

Se reutilizó y reforzó `torneo.py`: captura hashes de acciones antes del motor,
archiva fuentes, rechaza sobrescritura, errores, cobertura incompleta y cambios
de fuentes durante el bloque. El wrapper se comparó con el loader oficial:
1.438 acciones y rewards idénticos en dos episodios. `pareado_torneo.py` ahora
rechaza episodios inválidos, duplicados y celdas incompletas.

Ambos torneos completos: **160 controles noop exactos por bloque**, cobertura
y hashes archivados verificados, cero errores, máximo observado menor de 272 ms
por turno. Coste nuevo: **1.216 episodios de torneo + 8 diagnósticos = 1.224**.
Los diagnósticos son dos del loader, dos del fallo gate y cuatro reproducciones
reales; no se mezclan con las muestras de evaluación.

- [Evidencia y comandos de verificación](../evidencia/research_20260925/README.md).
- [Resultados forecast](../evidencia/research_20260925/forecast_results.json).
- [Resultados públicos nuevos](../evidencia/research_20260925/public_refresh_results.json).
- [Protocolo forecast](PREREG_FORECAST_GATE_2026-09-25.md).
- [Protocolo públicos nuevos](PREREG_PUBLIC_REFRESH_2026-09-25.md).

Los torneos son contra ocho políticas públicas emparentadas, no una muestra
aleatoria del ladder. No evalúan directamente los mejores rivales privados.
Las fuentes exactas están en `.sources.tgz`; los replays originales siguen en
`replays/`, ignorado por Git, con selección, diagnósticos y ledgers conservados.

## Próxima decisión útil

1. Leer partidas de VQ cuando tenga una muestra útil, junto con la referencia
   original y la fuerza observable de sus rivales. Otro envío desplazaría al
   original: debe aportar una hipótesis diferente o evidencia favorable nueva.
2. Investigar pérdidas actuales descomponiendo unidades producidas y precios
   ejecutados por fase. La predicción simultánea ya mostró valor; no volver a
   gate/off con los mismos parámetros ni a ajustes agotados del chasis HOZ.
3. Si aparecen pérdidas por elección de cultivo, aislar sobre VQ una decisión
   de producción basada en oferta futura visible. La versión HL completa no
   mejoró, lo cual no aísla ese mecanismo. Antes de ejecutarla, registrar la
   intervención, los riesgos de alimento/producción y semillas nuevas; todavía
   no es una candidata implementada ni aprobada por evidencia.



---

## SOURCE: docs/research/ESTADO_INVESTIGACION.md

# Estado de investigación — leer primero para continuar

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
- Loop7 en desarrollo: cuatro políticas de tomates en suelo SE libre, 4/8
  plantas d16/d18, sobre top3. V2 podía inhibir R51; v3 corrigió contratación
  pero perdió cuatro tomates por overflow. V4 separa riego/cosecha:16 diagnósticos
  completos, plantas y ventas16/32 confirmadas, R51 y ovejas conservados.
  1.248 episodios corriendo desde02:41UTC, `continuar_loop_relleno.py`.
- Loop8 registrado: seis variantes de patrones (rank5/7, historia120/360,
  ajuste por producto y desfase temporal). Validación16 juegos completa,
  noop1.438 acciones idénticas, cero errores, máximo271ms. Piloto1.472
  encolado detrás de loop7. Total36 variantes competitivas construidas.
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

Líder actual consultado 01:36 UTC: DSM 3128,7, submission 56518845. Cuatro replays
recientes reproducidos exactamente; compra cuarta tierra día 10 y cultiva más
tomates, con diferencias grandes de composición por mundo. No inferir causalidad
ni algoritmo del score. Informe: `LIDER_Y_FUENTES_2026-09-25.md`. Dos notebooks
con nombre nuevo eran copias de tds25: se deduplicaron sin repetir torneo.

Último snapshot real: VQ56535264 **2319,5 /24 episodios listados**, original
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



---

## SOURCE: docs/research/RESEARCH_BELIEFS.md

# Research beliefs — Kaggriculture

Actualizado: 2026-09-25 UTC. Cada entrada lleva su evidencia; cada evidencia nueva sube o baja la creencia.

## HIGH CONFIDENCE

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



---

## SOURCE: docs/research/HARNESS_VS_LEADERBOARD.md

# Harness vs leaderboard — qué métrica local predice el ladder

## Lectura nueva — 2026-09-25 UTC

Arshs3 **2292,5 @148 episodios**, v13 **1857,9 @136**, tras aproximadamente 20 h
activos. Ambos superan las cintas propias (seek 1324,8, decem 1285,9); el orden
arshs3 > v13 coincide con el torneo cerrado (20-0 directo). Evidencia API:
`docs/evidencia/research_20260925/*_episodes_snapshot.json` y
`submissions_after_vq.json`. Ratings observados, no una estimación causal del
delta ni un ranking actual del equipo; no se consultó ese ranking.

VQ (56535264) separará otra pregunta: 0 efecto contra pool histórico, pero
ventaja repetida contra copias, ¿sirve en una población real poblada de forks?
Se conservó arshs3 original como control activo. No comparar el rating de arranque
de VQ con 148 episodios del original para rechazarla. Muestra descriptiva de 16
partidas recientes de arshs3: 4V/11D/1E, no su tasa acumulada.

La frase histórica «sólo ≥100 Elo informa» no debe usarse como umbral universal.
La información depende de episodios, rival, edad y ruido observado. Asimismo,
muchas cintas/forks emparentados no son muchas familias independientes.

## Historial de calibración

Actualizado: 2026-09-23 18:00. Dataset acumulado y conclusiones provisionales.

## Dataset

| submission | candidato | local: delta global vs HOZ | local: vs FUERTES | ladder | episodios |
|---|---|---|---|---|---|
| 55993562 | grano (seed_stock_aware) | +6,4 | — | 772 (vs hoz 677) | 71 |
| 55994874 | hoz (+harvest_76, refutado) | +2,5 → −0,08 | — | 677–831 según fecha | 68 |
| 56245770 | **maj_107674293** (cinta fija) | +14,4 / +10,0 | **43,0%** (peor de todos) | **857** | 126 |
| 56444202 | tree_v1 | +9,0 / +6,1 | 53,1% (+10,2) | **967** @19 ep (TEMPRANO) | 19 |
| 56444505 | maj+guard6 | ≈ cinta (harness no ve el fallo) | — | 714 @32 ep (53% W/L) | 32 |
| 56447472 | tree_v1 + guard(6) | +6,1 global | fuerte: tree 20,2% | **1.132** @81 | 81 |
| 56449108 | **107570947 + guard(8)** | — | fuerte (guard 6): 54,8% · **gcal: 53,1% (cal1)** · 42,7% (rivales r2) | **1.164** @78 | 78 |
| 56504082 | **110304538 + gcal(8)** | — | cal1 62,5% · **rivales r2 61,6% (+18,9 vs 107570947)** | pendiente | 0 |

## Conclusiones (provisionales, se actualizan con cada lectura)

**1. El WR global del panel de 40 NO predice el ladder; el WR contra el subconjunto
FUERTE sí (evidencia: compare2, 2026-09-22).** En el mismo bloque, la cinta
campeona es la mejor vs 40 rivales de ~800 (72,1%) y la PEOR vs 8 rivales reales
de Majkel (43,0%). tree_v1 es −6,7 vs débiles y +10,2 vs fuertes — y en el ladder
va a 967 frente a 857. El ladder nos empareja con rivales de nuestro nivel: al
subir, el subconjunto fuerte es la población relevante.

**2. El harness de cintas pasivas subestima la fragilidad de una secuencia fija
al contexto.** 71,5% local vs 40% real para la misma cinta (56245770). Mecanismo
identificado: los rivales reales mueven el mercado del d0 lo justo para dejar la
caja en \$0 al alba (42% de partidas reales con <4 manos; 15% local).

**3. Los saltos grandes transfieren; los pequeños no se resuelven.** +14 de panel
→ +175 de ladder (cinta vs hoz). +6,4 y +2,5 → indistinguibles del ruido de
±40. Con ~60 episodios el ladder sólo resuelve ≥ ~100 Elo.

**4. Positive surprise pendiente de investigar (punto 13/16):** tree_v1 rinde
mejor en ladder de lo que el panel global predecía. Hipótesis: el ladder ya nos
enfrenta a rivales más fuertes que el panel `lad_` (rating ~800 → ahora 900+).
Comprobación: clasificar los replays de 56444202 por rating del rival y por
tienda d3 cuando pase de 50 episodios.

**5. (2026-09-23) La población de rivales importa más que el tamaño del bloque.**
La misma cinta de referencia rinde 53,1% contra rivales de Majkel/DSM/UMG/Vadim
(sep 11-20) y 42,7% contra los rivales del top-13 de esta semana. El campo se
endurece; confirmar siempre contra la población más reciente disponible.

**6. (2026-09-23) La selección sobre un piloto grande está dominada por ruido.**
111 candidatas × 64 celdas: el 1º (87,5%) cae a 31,0% en población fresca; el 4º
sube a 1º. Successive halving en ≥2 etapas + confirmación en rivales y semillas
disjuntos, siempre.

**7. (2026-09-24) El harness de cintas nunca midió el nivel ABSOLUTO.** Cada
"confirmación" comparaba variantes propias contra rivales-cinta pasivos. Los
agentes públicos (2500-2950 en ladder) nos ganan 20-0 en bucle cerrado. Desde
ahora: toda candidata se mide también en `torneo.py` contra el pool público.

## Regla operativa derivada

- **Métrica primaria local: WR vs panel FUERTE** (80 rivales de Majkel/DSM,
  `fuerte_*`). El panel `lad_` de 40 se conserva como control de no-regresión
  contra rivales débiles.
- Un candidato que gana vs fuertes y pierde poco vs débiles (perfil de
  `107570947`: +21,5 / −0,6) es preferible a uno que gana vs débiles y pierde vs
  fuertes (perfil de la cinta campeona).



---

## SOURCE: docs/research/SUBMISSION_HISTORY.json

[
  {
    "submission_id": 56245770,
    "timestamp": "2026-09-14T23:52:00-05:00",
    "git_commit": "(sin commit: working tree del 14-sep, ver docs/evidencia/envio_maj_20260914)",
    "experiment_id": "maj_107674293",
    "config": "cinta fija de Majkel1337, episodio 107674293 (vs yaki-imo)",
    "local_harness": {
      "panel": "40 lad + 8 sepopp, 19 seeds, 2 asientos",
      "wr": 71.49,
      "base_wr": 57.13,
      "delta": 14.36,
      "ci95_seed": [
        9.02,
        19.71
      ],
      "ci95_2way": [
        6.71,
        22.02
      ],
      "opponent_breakdown": {
        "lad40": "+15.00",
        "sepopp8": "+11.18"
      }
    },
    "reason": "Mejor candidato del piloto de 14 brazos; +14.36 confirmado. Usuario: 'Subela a kaggle pa que coja calle'",
    "leaderboard": {
      "score": 852.6,
      "episodes": 126,
      "rank": "~4589/9776 (2026-09-21)"
    },
    "delta_vs_champion_ladder": "+175 sobre campeona_hoz (677.5), pero hoz esta en caida y ruido de +-40",
    "observed": "Converge en ~852. Es la mejor submission que hemos tenido. Nota: Majkel1337 esta en 3075 y su CINTA fija da 852: el valor del agente esta en la adaptacion, no en la secuencia.",
    "conclusion": "CHAMPION (ladder). Panel +14 -> ladder +175 vs hoz: la direccion transfiere.",
    "next_action": "Arbol de rutas (ramificar por tiendas) para reducir el desajuste de contexto de una cinta fija."
  },
  {
    "submission_id": 56444202,
    "timestamp": "2026-09-21T21:53:35-05:00",
    "git_commit": "f5c2889",
    "experiment_id": "tree_v1",
    "config": "arbol de 4 cintas de Majkel1337 (107685970/107692988/107696961/107710951); rama en step 72 por primera tienda y en 144 por YARN_STORE. Paquete: empaquetar_arbol.py, 51413 bytes",
    "local_harness": {
      "panel": "piloto 14-sep: 16 rivales x 4 seeds x 2 asientos",
      "wr": 64.06,
      "base_wr": 46.09,
      "delta": 17.97,
      "ci95_seed": null,
      "ci95_2way": null,
      "opponent_breakdown": {
        "lad8": "62.50",
        "sepopp8": "65.62"
      },
      "nota": "empato con maj_107674293 (64.06) en el piloto; perdio el desempate alfabetico. Confirmacion con potencia: en curso (compare, 16 seeds)",
      "confirm_compare": {
        "panel": "48 rivales x 16 seeds x 2 asientos (compare 2026-09-21)",
        "wr": 65.76,
        "base_wr": 56.77,
        "delta": 8.98,
        "ci95_seed": [
          4.99,
          12.98
        ],
        "ci95_2way": [
          -6.09,
          24.06
        ],
        "nota": "en el MISMO bloque la cinta sola dio +12.11 [2.81; 21.41] y tree_v2 +4.82. Local: cinta > tree > tree_v2"
      }
    },
    "reason": "REAL_WORLD_CANDIDATE criterio #3 (estructuralmente distinto: ramifica) y #7 (localmente indistinguible de la cinta; solo el ladder los separa). Verificado identico al arbol local en 6 semillas, DONE",
    "leaderboard": {
      "score": 1082.2,
      "episodes": 40,
      "rank": null,
      "lecturas": [
        [
          16,
          914.0
        ],
        [
          19,
          966.9
        ],
        [
          40,
          1082.2
        ]
      ],
      "nota": "+225 sobre el campeon (857) a 40 ep: fuera del ruido de arranque. POSITIVE SURPRISE (punto 16): local +6..+9 global, +10 vs fuertes"
    },
    "delta_vs_champion_ladder": null,
    "observed": "Mucho mejor en ladder de lo que el panel global predecia. Coherente con compare2: el arbol gana vs FUERTES (+10.2) y el ladder empareja con rivales de nuestro nivel",
    "conclusion": "CHAMPION_CANDIDATE (pendiente replay analysis + confirmar a ~60 ep)",
    "next_action": "Comparar contra maj_107674293 (852.6) cuando pase de ~60 episodios. Mientras: compare panel tree vs tree_v2."
  },
  {
    "submission_id": 56444505,
    "timestamp": "2026-09-21T22:40:00-05:00",
    "git_commit": "073fa24",
    "experiment_id": "maj_107674293+guard6",
    "config": "cinta maj_107674293 + bots/guardia_cinta.py reserve=6 until_step=24 (descarta BUY_SEED/BUY_PRODUCT del d0 que dejarian la caja bajo $6)",
    "local_harness": {
      "panel": "sonda 40 partidas vs lad (no es panel completo)",
      "wr": 65,
      "base_wr": 62,
      "delta": 3,
      "ci95_seed": null,
      "ci95_2way": null,
      "nota": "harness NO reproduce el fallo (15% de partidas <4 manos local vs 42% real). Con guardia: 0% <4 manos. Identica a la cinta en 24/40"
    },
    "reason": "REAL_WORLD_CANDIDATE #4: corrige debilidad observada en 60 partidas reales (manos d1 -> WR 0/23/60%). Unico cambio vs champion: la guardia. Aisla su efecto en ladder",
    "leaderboard": {
      "score": 713.7,
      "episodes": 32,
      "rank": null,
      "lecturas": [
        [
          10,
          660.7
        ],
        [
          14,
          709.5
        ],
        [
          32,
          713.7
        ]
      ],
      "nota": "PLANA en ~710 mientras tree_v1 sube a 1082 en la misma ventana. NEGATIVE SURPRISE (punto 12)"
    },
    "delta_vs_champion_ladder": null,
    "observed": "No mejora al campeon; posible que sea peor. Hipotesis: las manos del d1 eran SINTOMA (rival fuerte hunde precios d0 -> caja 0) y no causa. Correlacion tomada por causalidad",
    "conclusion": "PROMISING -> en revision; replays bajando para failure analysis",
    "next_action": "Comparar con 852.6 (56245770) a ~60 ep. Prediccion: si el mecanismo es real, +10..+20 puntos de WR en ladder -> rating claramente > 852. Si queda en ~850, el fallo del d1 no era la causa dominante de las derrotas"
  },
  {
    "submission_id": 56447472,
    "timestamp": "2026-09-22T03:10:00-05:00",
    "git_commit": "98f9ea6",
    "experiment_id": "tree_v1+guards",
    "config": "arbol de 4 cintas (ramas tienda d3 / YARN d6) + guard_cash reserve=6 + guard_commitments max_retry=48. empaquetar_arbol.py --guard 6. 56583 bytes",
    "local_harness": {
      "panel": "tree_v1: compare2 48riv x 16seeds; guardias: sondas",
      "wr": 63.35,
      "base_wr": 57.23,
      "delta": 6.12,
      "ci95_seed": [
        1.9,
        10.34
      ],
      "ci95_2way": [
        -7.13,
        19.37
      ],
      "opponent_breakdown": {
        "lad40": "-6.72 vs cinta",
        "sepopp8 (fuertes)": "+10.16 vs cinta"
      },
      "nota": "las guardias son inertes cuando la caja alcanza; verificado paquete == local en 12 partidas"
    },
    "reason": "Criterio 6: combinacion de dos mejoras validadas POR SEPARADO en ladder. tree_v1 31-9 (78%) con 8/9 derrotas por manos d1 (con 4 manos 30-1); guardia 32/32 con 4 manos, 53% vs 40%",
    "leaderboard": {
      "score": 1131.6,
      "episodes": 81,
      "lecturas": [
        [
          28,
          1118.9
        ],
        [
          40,
          1136.1
        ],
        [
          51,
          1183.5
        ],
        [
          81,
          1131.6
        ]
      ],
      "rank": "3368/9792 (equipo)"
    },
    "delta_vs_champion_ladder": null,
    "observed": "23-17 (58%) a rating mas alto que tree_v1; +54 Elo vs tree_v1 solo a 40 ep. 3/40 con 3 manos (reserve=6 corto para sus cintas; deberia ser 8)",
    "conclusion": "PROMISING; desactivada 2026-09-23 al subir 56504082 (1131.6 @81 ep, congelada)",
    "next_action": "Prediccion: >= tree_v1 (1082 @40ep) y con menos derrotas catastroficas. Si a ~40 ep supera 1082 -> CHAMPION. Desactiva a tree_v1 (56444202, 40 ep, ya leido)"
  },
  {
    "submission_id": 56449108,
    "timestamp": "2026-09-22T04:30:00-05:00",
    "git_commit": "6527d3a",
    "experiment_id": "107570947+guards8",
    "config": "cinta top_majkel1337_107570947 (Majkel vs Q.Ai, PET_CAFE d3) + guard_cash reserve=8 + guard_commitments. empaquetar_cinta_guard.py. 18345 bytes",
    "local_harness": {
      "panel": "FUERTE: 80 rivales de Majkel/DSM x 8 seeds x 2 asientos",
      "wr": 54.84,
      "base_wr": 9.53,
      "delta": 45.31,
      "ci95_seed": [
        32.16,
        58.47
      ],
      "ci95_2way": [
        30.44,
        60.18
      ],
      "opponent_breakdown": {
        "fuertes80": "54.8% (cinta campeona 17.4%, tree_v3+guard 29.5%, tree 20.2%)",
        "compare2 lad40 (sin guardias)": "-0.6 vs cinta",
        "compare2 sepopp8 (sin guardias)": "+21.5 [5.7; 37.3] vs cinta"
      },
      "nota": "reserve=8 (no 6): esta cinta pide 5 HIRE al alba, usa 4, necesita \\$7. Sin guardias: 36.3% vs fuertes"
    },
    "reason": "CHAMPION_CANDIDATE por evidencia local fuerte en la poblacion que predice el ladder. Una variable vs 56447472 (tree_v1+guards): material de cintas",
    "leaderboard": {
      "score": 1156.3,
      "episodes": 90,
      "lecturas": [
        [
          13,
          1182.0
        ],
        [
          24,
          1179.7
        ],
        [
          51,
          1201.3
        ],
        [
          78,
          1163.7
        ],
        [
          90,
          1156.3
        ]
      ],
      "rank": "3368/9792 (equipo)"
    },
    "delta_vs_champion_ladder": null,
    "observed": "15-9 (62%), $100.5k vs $88.1k. 24/24 con 4 manos y 3 cuadrantes. Derrotas ajustadas vs rivales de 93-138k. Banco identico en V y D: produccion fija, gana sii el rival produce menos",
    "conclusion": "CHAMPION hasta 2026-09-24 00:58 UTC; desactivada al subir 56507746/56507747. Congelada ~1156",
    "next_action": "Leer W/L (no rating) a ~30 ep. Prediccion: >= tree_v1+guards. Desactiva a 56444505 (guardia, 32 ep, ya leida)"
  },
  {
    "submission_id": 56504082,
    "timestamp": "2026-09-23T17:30:00-05:00",
    "git_commit": "3cbaca1",
    "experiment_id": "110304538+gcal8",
    "config": "cinta top2_majkel1337_110304538 (Majkel-3075, 2a mitad de sep, vs top-3) + guard_cash reserve_auto=8 + guard_commitments. empaquetar_cinta_guard.py --reserve 8. 19576 bytes",
    "local_harness": {
      "panel": "confirm_cal1: 148 rivales NUEVOS (rivales de Boey/MMPQ/DECEM/Majkel-nuevo/Vadim-nuevo/seek) x 4 seeds x 2 asientos",
      "wr": 61.6,
      "ref_wr": 42.7,
      "delta_vs_ref": 18.92,
      "ci95_seed": [
        -3.5,
        41.3
      ],
      "ci95_2way": [
        -0.5,
        38.4
      ],
      "opponent_breakdown": {
        "boey": "+16.0",
        "decem": "+25.5",
        "majkel3": "+17.9",
        "mmpq": "+21.5",
        "seek": "+11.0",
        "vadim2": "+21.6"
      },
      "historial": "majkel2_confirm (reserve 6 ambos, 71 fuertes): -0.26 [-25;+24]; cal1 piloto (gcal, 32 fuertes): +9.4",
      "nota": "ref = gcal:107570947 = la campeona 56449108 exacta"
    },
    "reason": "REAL_WORLD_CANDIDATE (criterio 1): point estimate claramente interesante en una poblacion FRESCA y relevante (rivales del top-13 de esta semana), positiva contra las 6 fuentes; IC dos vias roza cero por 4 seeds. Desplaza a la mas debil de las dos activas (tree_v1+g)",
    "leaderboard": {
      "score": 1102.3,
      "episodes": 20,
      "rank": null,
      "lecturas": [
        [
          20,
          1096.8
        ],
        [
          "final",
          1102.3
        ]
      ]
    },
    "delta_vs_champion_ladder": null,
    "observed": "20 partidas: 12V 7D 1E (62%), 5-6 manos d1 y 3 cuadrantes en las 20; derrotas ajustadas. = tasa de 107570947+g a igual edad",
    "conclusion": "Localmente empatada con 107570947 en confirm2 (+0.3 [-5.2;+5.9]); desactivada al subir la pareja seek/decem",
    "next_action": "Leer W/L a ~30 ep y rating a ~60. Si supera a 56449108 (1164) -> CHAMPION. OJO: la proxima submission desplazaria a 56449108; solo subir otra si 56504082 no es peor"
  },
  {
    "local_harness_cadena": "cal2 (93 cintas, 32 rivales, filtro) -> etapa2 (148 rivales r2, 2 seeds, 592 ep/brazo) -> confirm2 (76 rivales reservados, 6 seeds)",
    "timestamp": "2026-09-24T00:58:00Z",
    "submission_id": 56507746,
    "git_commit": "2555828",
    "experiment_id": "seek_112344897+gcal8",
    "config": "cinta top11_seek_112344897 (seek inspiration, sub 56407833) + guard_cash reserve_auto=8 + guard_commitments",
    "local_harness": {
      "etapa2": "91.4%, +31.8 vs 110304538 (148 rivales r2)",
      "confirm2_wr": 78.2,
      "confirm2_delta_vs_110304538": 27.74,
      "ci95_seed": [
        9.4,
        46.1
      ],
      "ci95_2way": [
        9.7,
        45.8
      ],
      "delta_vs_107570947": 27.41,
      "ci95_2way_vs_107570947": [
        12.6,
        42.2
      ],
      "opponent_breakdown": {
        "dsm": "+38.9",
        "majkel": "+18.1",
        "umg": "+33.3",
        "vadim": "+19.6"
      },
      "nota": "max de 5 confirmadas: estimacion encogida ~+18..+20"
    },
    "reason": "CHAMPION_CANDIDATE: supera a las dos activas con ambos IC >0 en poblacion fresca. Pareja diversificada (fuente distinta a DECEM)",
    "leaderboard": {
      "score": 1324.8,
      "episodes": 55,
      "rank": null,
      "lecturas": [
        [
          55,
          1324.8
        ]
      ]
    },
    "observed": "1324.8 @55 ep (~3.5 h activa): +160 sobre 107570947+g a igual edad; la mejora relativa del harness SI transfirio",
    "conclusion": "Superada en nivel absoluto por los agentes publicos (0-20 vs cada uno en torneo_rr1). Desactivada al subir 56511611/56511619",
    "next_action": "Leer W/L a ~30 ep; comparar con decem. Si una de las dos flojea claramente en el ladder, sustituirla por decem_112007951 o decem_112034117"
  },
  {
    "local_harness_cadena": "cal2 (93 cintas, 32 rivales, filtro) -> etapa2 (148 rivales r2, 2 seeds, 592 ep/brazo) -> confirm2 (76 rivales reservados, 6 seeds)",
    "timestamp": "2026-09-24T00:58:00Z",
    "submission_id": 56507747,
    "git_commit": "1385825",
    "experiment_id": "decem_112000345+gcal5",
    "config": "cinta top8_decem_112000345 (DECEM, sub 56446088) + guard_cash reserve_auto=5 + guard_commitments",
    "local_harness": {
      "etapa2": "87.8%, +28.2 vs 110304538",
      "confirm2_wr": 73.1,
      "confirm2_delta_vs_110304538": 22.7,
      "ci95_seed": [
        10.3,
        35.1
      ],
      "ci95_2way": [
        8.2,
        37.2
      ],
      "delta_vs_107570947": 22.37,
      "ci95_2way_vs_107570947": [
        7.9,
        36.9
      ],
      "opponent_breakdown": {
        "dsm": "+32.6",
        "majkel": "+13.9",
        "umg": "+25.0",
        "vadim": "+18.5"
      },
      "nota": "senal de fuente: 4 cintas DECEM confirmadas a +20..+23"
    },
    "reason": "CHAMPION_CANDIDATE, pareja de seek; la evidencia de DECEM esta replicada en 4 cintas",
    "leaderboard": {
      "score": 1285.9,
      "episodes": 58,
      "rank": null,
      "lecturas": [
        [
          58,
          1285.9
        ]
      ]
    },
    "observed": "1285.9 @58 ep: +120 sobre 107570947+g; seek > decem, como predijo confirm2 (+27.7 vs +22.7)",
    "conclusion": "Idem; desactivada",
    "next_action": "Idem. Si DECEM transfiere mejor que seek, las otras 3 DECEM confirmadas son el banquillo"
  },
  {
    "local_harness_cadena": "torneo_rr1: bucle cerrado, motor oficial 1.32.7, cargado como Kaggle (ultimo callable), 10 seeds 910000-009 x 2 asientos, 9 agentes, 720 partidas, 0 errores",
    "leaderboard": {
      "score": 1857.9,
      "episodes": 136,
      "rank": null,
      "lecturas": [
        [
          136,
          1857.9
        ]
      ],
      "observed_at": "2026-09-25T00:22:13.462952+00:00"
    },
    "observed": null,
    "conclusion": "Desactivada por VQ; rendimiento inferior a arshs3 en esta lectura",
    "autorizacion": "usuario 2026-09-24 (AskUserQuestion): 'arshs3 + v13 (Recomendado)'",
    "submission_id": 56511611,
    "timestamp": "2026-09-24T04:28:30Z",
    "git_commit": "9e724c3",
    "experiment_id": "publico_v13_thomastschinkel",
    "config": "main.py publico byte-exacto de thomastschinkel/the-metav4-farm-submission-v13 (Apache-2.0), sha256 9d63494603f88219857a3101d7dc19cc750ded04e5886732ee428580326967d9, entrada agent",
    "local_harness": {
      "torneo_rr1_pct_vs_resto": 41.2,
      "vs": {
        "v94": "20-0",
        "arshs3": "0-20",
        "ars40": "0-20",
        "hsov": "0-20",
        "h2965": "0-20",
        "guru6": "6-14",
        "seek": "20-0 (+14.4k)",
        "decem": "20-0 (+15.6k)"
      },
      "nota": "semillas A>B por pareja en torneo_rr1.txt; cambio de asiento casi repite la partida: unidad efectiva = semilla"
    },
    "reason": "Salto de nivel absoluto (publicos 2500-2950 vs nosotros ~1300). Rama cinta+reflejos del autor con mejor registro de ladder documentado (v9/4 2944.7 @201). Diversifica frente a arshs3",
    "next_action": "Conservar como familia de control local"
  },
  {
    "local_harness_cadena": "torneo_rr1: bucle cerrado, motor oficial 1.32.7, cargado como Kaggle (ultimo callable), 10 seeds 910000-009 x 2 asientos, 9 agentes, 720 partidas, 0 errores",
    "leaderboard": {
      "score": 2292.5,
      "episodes": 148,
      "rank": null,
      "lecturas": [
        [
          148,
          2292.5
        ]
      ],
      "observed_at": "2026-09-25T00:22:13.462277+00:00"
    },
    "observed": "Desplazada por top3; score2275.7 en snapshot de retiro. Paquete exacto conservado.",
    "conclusion": "Referencia histórica madura; paquete original conservado",
    "autorizacion": "usuario 2026-09-24 (AskUserQuestion): 'arshs3 + v13 (Recomendado)'",
    "submission_id": 56511619,
    "timestamp": "2026-09-24T04:28:57Z",
    "git_commit": "fd2ce6d",
    "experiment_id": "publico_arshs3_arsgorynich",
    "config": "main.py publico byte-exacto de arsgorynich/herd-safe-v3-experimental-risk-aware-feed (Apache-2.0), sha256 4f8637a3e33348b98f531de246d353f5d2955b2f85480e3fd02bf4a7874f0d01, entrada herdsafe_forecast_agent",
    "local_harness": {
      "torneo_rr1_pct_vs_resto": 98.8,
      "vs": {
        "ars40": "18-2",
        "v13": "20-0",
        "v94": "20-0",
        "h2965": "20-0",
        "hsov": "20-0",
        "guru6": "20-0",
        "seek": "20-0 (+14.6k)",
        "decem": "20-0 (+16.2k)"
      }
    },
    "reason": "Campeon del torneo en bucle cerrado contra el pool publico",
    "next_action": "Control local; no reenviar salvo evidencia nueva"
  },
  {
    "submission_id": 56535264,
    "timestamp": "2026-09-25T00:22:43.633000Z",
    "git_commit": "a9f59ee",
    "experiment_id": "arshs3vq_real",
    "config": {
      "file": "submission/main_publico_arshs3_vq.py",
      "sha256": "9b463dfb8076b4c63946e1ae4249cd1cfc3cc58b63115cf2bd5b00f96f188976",
      "layers": [
        "arshs3",
        "VQ"
      ]
    },
    "local_harness": {
      "pool_delta": 0,
      "ci95_seed": [
        0,
        0
      ],
      "ci95_2way": null,
      "opponent_breakdown": "0 cambios WLT en 120 celdas / 12 rivales",
      "mirror_confirmation": "40-0; bloque posterior 95%",
      "evidence": "docs/research/PREREG_VQ_2026-09-24.md"
    },
    "reason": "VQ validada contra copias; arshs3 transfiere al ladder (2292.5 vs v13 1857.9). Desplaza v13, preserva arshs3 como referencia activa.",
    "leaderboard": {
      "score": 2306.3,
      "rank": null,
      "episodes": null,
      "lecturas": [
        [
          "initial",
          810.0
        ],
        [
          "2026-09-25T00:54:49.768749+00:00",
          1198.5
        ],
        [
          "2026-09-25T01:22:09.418425+00:00",
          1967.9,
          14
        ],
        [
          "2026-09-25T01:52Z",
          2319.5,
          24
        ],
        [
          "2026-09-25T01:57Z",
          2268.9,
          null
        ],
        [
          "2026-09-25T02:05:31.666206+00:00",
          2364.6,
          null
        ],
        [
          "2026-09-25T02:33:17.349601+00:00",
          2306.3,
          null
        ]
      ]
    },
    "delta_vs_champion_ladder": null,
    "observed": "COMPLETE, snapshot02:33UTC. Score2306.3. Sin recuento actualizado de episodios. Control activo de top3.",
    "conclusion": "REAL_WORLD_CANDIDATE; ventaja local específica contra copias, sin promoción automática",
    "next_action": "Recoger feedback real a edad razonable; loops6–8 siguen activos. Rating joven no establece superioridad.",
    "latest_snapshot": "docs/evidencia/loop_publicos_20260925/ladder_snapshot_0233.txt"
  },
  {
    "submission_id": 56537205,
    "timestamp": "2026-09-25T01:56:34.180000Z",
    "git_commit": "ba1fda83c38bd680d00293f81bc6afbbb89d7813",
    "experiment_id": "arshs3vq_top3",
    "config": {
      "file": "submission/main_publico_arshs3_vq_top3.py",
      "sha256": "9668e30ad08f79d485bd230a3c660d4cc420b9382e87f9387b6908e3c94a5145",
      "changes": {
        "_V92_P_TOP": 3
      }
    },
    "local_harness": {
      "reference": "base",
      "candidate": "pred_top3",
      "rivals": [
        "ars40",
        "arshs3",
        "guru6",
        "h2965",
        "hl25",
        "hsov",
        "hybu",
        "obr",
        "tds",
        "tds25",
        "v13"
      ],
      "seeds": [
        996000,
        996001,
        996002,
        996003,
        996004,
        996005,
        996006,
        996007,
        996008,
        996009,
        996010,
        996011,
        996012,
        996013,
        996014,
        996015
      ],
      "base_wr": 78.4090909090909,
      "candidate_wr": 89.20454545454545,
      "delta_points": 10.795454545454545,
      "ci95_seed": [
        1.2340308210197328,
        20.356878269889357
      ],
      "ci95_2way": [
        -0.11529016571724426,
        21.706199256626334
      ],
      "opponent_breakdown": {
        "ars40": 6.25,
        "arshs3": -6.25,
        "guru6": 0.0,
        "h2965": 6.25,
        "hl25": 18.75,
        "hsov": 6.25,
        "hybu": 18.75,
        "obr": 6.25,
        "tds": 12.5,
        "tds25": 31.25,
        "v13": 18.75
      },
      "better_cells": 20,
      "worse_cells": 1,
      "equal_cells": 155,
      "status": "REAL_WORLD_CANDIDATE",
      "registered_submission_gate": true,
      "original_pool_only": {
        "reference": "base",
        "candidate": "pred_top3",
        "rivals": [
          "ars40",
          "guru6",
          "h2965",
          "hsov",
          "hybu",
          "obr",
          "tds",
          "v13"
        ],
        "seeds": [
          996000,
          996001,
          996002,
          996003,
          996004,
          996005,
          996006,
          996007,
          996008,
          996009,
          996010,
          996011,
          996012,
          996013,
          996014,
          996015
        ],
        "base_wr": 85.15625,
        "candidate_wr": 94.53125,
        "delta_points": 9.375,
        "ci95_seed": [
          -0.7995092526113545,
          19.549509252611355
        ],
        "ci95_2way": [
          -1.634345637938253,
          20.384345637938253
        ],
        "opponent_breakdown": {
          "ars40": 6.25,
          "guru6": 0.0,
          "h2965": 6.25,
          "hsov": 6.25,
          "hybu": 18.75,
          "obr": 6.25,
          "tds": 12.5,
          "v13": 18.75
        },
        "better_cells": 12,
        "worse_cells": 0,
        "equal_cells": 116
      }
    },
    "reason": "Cumple gate registrado: delta>=3pp, ningún rival<-20pp, cero errores, revisión de mecanismos y runtime. Prueba real autorizada.",
    "leaderboard": {
      "score": 1459.1,
      "episodes": null,
      "status": "SubmissionStatus.COMPLETE",
      "lecturas": [
        [
          "2026-09-25T02:05:31.666206+00:00",
          729.5,
          null
        ],
        [
          "2026-09-25T02:33:17.349601+00:00",
          1459.1,
          null
        ]
      ]
    },
    "observed": "COMPLETE, snapshot02:33UTC. Score1459.1. Diez episodios listados02:34, incluida validación. Cuatro replays por recencia en revisión.",
    "conclusion": "REAL_WORLD_CANDIDATE; no CHAMPION",
    "next_action": "Recoger feedback real a edad razonable; loops6–8 siguen activos. Rating joven no establece superioridad.",
    "replaces_submission": 56511619,
    "preserves_submission": 56535264,
    "evidence": "docs/research/DECISION_ENVIO_TOP3_2026-09-25.md",
    "latest_snapshot": "docs/evidencia/loop_publicos_20260925/ladder_snapshot_0233.txt"
  }
]



---

## SOURCE: docs/research/PREREG_VQ_2026-09-24.md

# Pre-registro — arshs3 + compactación de cola (VQ)

Escrito antes de ejecutar. 2026-09-24 ~05:20 UTC.

- **Hipótesis:** quitar órdenes de mercado que seguro no ejecutan adelanta las
  ejecutables en la resolución en lockstep y voltea partidas decididas por
  márgenes mínimos (entre agentes públicos top: +$7..+$34 de media).
- **Mecanismo verificado (sonda, seed 939999 vs tds):** 56 turnos cambiados,
  36 órdenes adelantadas, 0 errores.
- **Brazos:** A = arshs3 (sha 4f8637a3); A+VQ = `apilar_capa_vq.py` (sha 9b463dfb).
- **Pool (12):** tds, hl59, hybu, lp16, ars40, hsov, v13, obr, h2965, guru6, wz15, v94.
- **Semillas:** 940000-940009 (nuevas), dos asientos. Más A vs A+VQ directo.
- **Unidad:** celda (rival, semilla) promediando asientos; delta pareado
  A+VQ − A; IC95 por semilla y dos vías.
- **Regla:** ambos IC > 0 → REAL_WORLD_CANDIDATE (sustituye a arshs3 en el
  ladder); punto > 0 con IC que incluye 0 → PROMISING (confirmar con 10 semillas
  nuevas, sin fusionar bloques); punto ≤ 0 → REJECTED. Directo A vs A+VQ se
  reporta aparte, no decide.

## Resultado del bloque (torneo_vq1, 500 partidas, 0 errores)

- Pool: **0/120 celdas cambian** (delta 0,00). Dinero propio: +$20,4 medio,
  225/240 episodios distintos, mínimo −$6. Veredicto por la regla: **no se adopta
  como mejora de W/L contra el pool** (inerte en resultados, no dañino).
- Directo (no decide, según lo fijado): arshs3vq 17-3 contra arshs3.

## Pre-registro 2: espejo (escrito tras ver el directo; hipótesis NUEVA)

- **Hipótesis:** en un espejo arshs3 vs arshs3 la compactación da prioridad de
  slot y gana; en el ladder habrá copias de arshs3 (notebook público del 23-sep).
- **Prueba:** arshs3vq vs arshs3, seeds 950000-950019 (nuevas), dos asientos.
  Unidad: semilla (asientos promediados).
- **Regla:** sustituir arshs3 por arshs3vq en el ladder sólo si el IC95 por
  semilla de la tasa de victoria excluye 50% por arriba **y** ninguna celda del
  pool empeoró (ya observado: 0 peores de 120). Si no, se queda arshs3.



---

## SOURCE: docs/research/PREREG_ADV_2026-09-24.md

# Pre-registro — arshs3vq + ADV (adelanto de ventas, Ahmed Berat Özer EXP293)

Escrito antes de ejecutar. 2026-09-24 ~06:45 UTC.

- **Motivo:** las 95 derrotas de arshs3 en los torneos son por $257 (p25) /
  $521 (mediana) / $1.147 (p75): no se voltean con micro-ajustes. Sus rivales
  más duros (tds 23 derrotas, hl59 15) llevan la capa ADV y arshs3 no.
- **Hipótesis:** vender antes lo que la cinta vendería en ≤4 turnos (si ya está
  en el cobertizo) gana la carrera del libro de precios a rivales que venden lo
  mismo; debería ganar partidas sobre todo contra tds/hl59/hybu/lp16.
- **Brazos:** ref = arshs3vq (sha 9b463dfb, ya confirmado en espejo);
  cand = arshs3_adv_vq (`apilar_capa_vq.py base tds out adv vq`, sha 2abbca9a).
- **Pool (12):** tds, hl59, hybu, lp16, ars40, hsov, v13, obr, h2965, guru6, wz15, v94.
- **Semillas:** 970000-970009 (nuevas), dos asientos, + directo.
- **Unidad y regla:** como PREREG_VQ. Ambos IC > 0 → candidata a sustituir a
  arshs3vq; punto > 0 con IC que incluye 0 → PROMISING (confirmar con 10
  semillas nuevas sin fusionar); punto ≤ 0 → REJECTED. Riesgo específico:
  choque con la capa PREDICT de arshs3 (ambas adelantan ventas) → vigilar
  el delta contra rivales donde arshs3 ya ganaba 20-0.

## Resultado del descubrimiento (torneo_adv1, 500 partidas, 0 errores)

delta +10,0 pts (81,2% → 91,2%); IC95 semilla [−10,2; +30,2]; dos vías
[−10,0; +30,0]; 22 celdas a favor / 10 en contra. Por rival: tds +30, hl59 +30,
wz15 +25, hybu +20, lp16 +20, h2965 +10, hsov +10, v13 0, v94 0, guru6 −5,
ars40 −10, obr −10. Directo 10-10. Veredicto: **PROMISING**.

## Regla de confirmación (fijada antes de correrla)

- Semillas 980000-980009, mismos brazos y mismo pool de 12; el bloque se
  analiza SOLO, sin fusionar con el descubrimiento.
- Ambos IC > 0 → REAL_WORLD_CANDIDATE firme.
- Punto > 0 y delta medio > 0 en el subgrupo fijado de antemano del linaje tds
  (tds, hl59, hybu, lp16, wz15) → REAL_WORLD_CANDIDATE como instrumento (el
  mandato permite subir con IC que incluye 0 si corrige una debilidad observada).
- Punto ≤ 0 → REJECTED.
- Extra (no decide): arshs3 puro y hsov2 (copia de arshs3) como rivales, para
  comprobar que la ventaja en espejo de VQ se conserva con ADV.

## Resultado de la confirmación (torneo_adv2, 580 partidas, 0 errores)

delta **−2,08** pts; IC95 semilla [−20,2; +16,0]; dos vías [−20,4; +16,2];
12 a favor / 16 en contra. Por rival: hybu +25, tds +10, hl59 +10, lp16 +5,
wz15 +5, ars40 0, v13 0, v94 0, guru6 −10, h2965 −20, hsov −20, obr −30.
**Veredicto: REJECTED** (punto ≤ 0). Lectura: ADV intercambia partidas entre
linajes (gana al linaje tds, pierde con herd-safe/order-book); neto ≈ 0.
Extra: arshs3vq y arshs3advvq ganan 95% a arshs3 y a hsov2 (copia de arshs3):
tercera confirmación de la ventaja de VQ en espejo.



---

## SOURCE: docs/research/PREREG_FORECAST_GATE_2026-09-25.md

# Forecast gate: controlar confianza del predictor existente

Registrado antes del piloto. Fecha UTC 2026-09-25 (24-sep en Colombia).

## Evidencia y diferencia con lo ya probado

Arshs3: 2292,5 @148 episodios frente a v13 1857,9 @136. La muestra fijada por
recencia tiene 16 arshs3 y ocho v13; no se eligieron por resultado. Arshs3:
4V/11D/1E, sin escapes y sin inventario propio terminal sin vender. Son episodios
recientes, no una estimación de su WR histórico.

El código exige tres aciertos y precisión histórica ≥70% para señales a 3–4
turnos, pero acepta las señales inmediatas sin ese control. Una sonda en los
primeros cuatro replays reconstruye todas las acciones salvo una en uno de ellos;
67 ventas añadidas por PREDICT, 12 coinciden con venta neta rival inferida a 1–4
turnos. Inferencia de mercado, no ledger causal exacto ni pérdida económica probada.

**Hipótesis:** ese filtro aplicado también a 1–2 turnos evita ventas prematuras
contra oponentes que no siguen la biblioteca histórica. Upside MEDIUM/HIGH,
confianza LOW/MEDIUM. Diferente de ADV, que añadía adelantos generales: aquí se
restringe PREDICT. La ablación compara quitar esta capa, manteniendo las demás.

## Implementaciones y controles

- base y noop: `submission/main_publico_arshs3_vq.py`, sha 9b463dfb.
- gate: `apilar_forecast_gate.py gate`, exige ≥3 aciertos y ≥70% en ventana
  pasada de 240 turnos para el producto antes de aceptar la predicción.
- off: `apilar_forecast_gate.py off`, abla sólo `_v92_predict`; conserva el
  registro de señales y las demás capas de ventas y producción.
- No cambiar producción, rutas, cantidades de insumos ni usar futuro real.

## Piloto

Reutilizar `torneo.py`, ambos asientos. Pool de ocho representantes públicos:
tds, hybu, ars40, hsov, v13, obr, h2965, guru6. Se omite hl59 por duplicación
conductual con tds; no elegir rivales después de resultados. Semillas
**990000–990007**, cuatro brazos, 32 cruces contra pool + seis directos:
**608 episodios**. Una sonda de dos episodios antes valida el wrapper del loader.

Primario: delta gate − base por rival/semilla, asientos promediados. Reportar
IC95 por semilla y dos vías de `pareado_torneo.py`, desglose por rival y asientos.
Los directos y off son diagnósticos. No seleccionar off como nuevo ganador de
esta misma confirmación. Medir acciones emitidas antes del motor; noop idéntico
en acciones, rewards y estados de finalización; errores invalidan el bloque.

Toreno anterior tenía deficiencias concretas: sobrescribía resultados, omitía
hashes de acciones y sólo avisaba de cambios de código. Se endurece ese mismo
harness con manifiesto previo, archivo de fuentes, hashes, cobertura completa,
fallo ante errores y captura de acciones usando el loader oficial de Kaggle.
No se crea otro sistema de evaluación.

## Decisión y parada

- Gate ≥+5 puntos y al menos dos rivales positivos, ninguno <−15: PROMISING;
  confirmar contra los mismos ocho y semillas **991000–991015** (dos brazos,
  ocho rivales + directo: **544 episodios**). Interpretar IC como incertidumbre.
- Gate entre 0 y +5: dejar PROMISING débil; sólo continuar si la sonda de mecanismo
  encuentra corrección clara de un fallo en replays reales. No ampliar por dinero.
- Gate ≤0: no gastar confirmación en esta variante. Si IC cruza cero, decir
  ausencia de mejora observada, no prueba de perjuicio ni nulo exacto.
- Si gate no modifica acciones, parar y revisar activación antes de medir más.
- Confirmación con punto ≥+5, al menos dos rivales positivos y sin regresión
  >15 por rival permite REAL_WORLD_CANDIDATE aunque un IC cruce cero; ambos
  IC positivos fortalecen evidencia, no promueven automáticamente a CHAMPION.

VQ ya fue enviada como **56535264** usando evidencia anterior, antes de este
piloto. Sigue activa arshs3 original 56511619. Si surge otro envío, considerar
que desplaza al más antiguo (arshs3); no reemplazar ambos con cambios casi iguales.



---

## SOURCE: docs/research/PREREG_PUBLIC_REFRESH_2026-09-25.md

# Referencias públicas actualizadas: tds y Harvest Ledger

Registrado antes de medir estas versiones. Es una comparación nueva: ambos
archivos cambiaron respecto a los hashes de los torneos rr1–rr4.

- [tds](https://www.kaggle.com/code/tetsutani/demand-preserving-turn-sale-timing):
  última ejecución pública 2026-09-24 16:06 UTC; SHA descargado **127ed3e6**,
  antes 178ae0f7. Nuevo paquete de aproximadamente 0,5 MB y capas MG/IG de cola;
  no asumir equivalencia conductual por mantener el título del notebook.
- [Harvest Ledger](https://www.kaggle.com/code/haodou092/kaggriculture-harvest-ledger):
  ejecución 2026-09-24 09:18 UTC; nuevo SHA **1dfd4630**, antes 37d284d4.
  Cambio de producción: precios esperados de trigo/zanahoria a tres días, mezcla
  80% futuro / 20% observado, siembras hasta d26, buffer de semillas 6. Riesgo:
  sobreestimar oferta que no se cosechará y perjudicar alimento/producción.

Archivos descargados en `results/publicos_20260925/`, hashes y fecha del listado
en `docs/evidencia/research_20260925/`. Avisos Apache-2.0 conservados. Auditoría
estática: stdlib, exec de cadenas constantes; remove sobre listas; único open
en rama desactivada por path=None. No ejecutar notebooks ni scripts de descarga.

**Hipótesis de alto potencial:** una producción y logística distintas pueden
superar a arshs3vq donde micro-capas sólo intercambian partidas. Confianza LOW;
las versiones nuevas son candidatas, no mejoras ya demostradas.

## Diseño

Reutilizar `torneo.py`, sin editarlo durante bloques. Base/noop arshs3vq,
tds25 y hl25; ocho rivales congelados del piloto forecast: tds anterior, hybu,
ars40, hsov, v13, obr, h2965, guru6. Semillas **992000–992007**, ambos asientos,
38 cruces = **608 episodios**. En pares con tds antiguo se mide también cambio
de versión. Directos entre brazos se reportan aparte. No mezclar rating ajeno
anunciado con nuestros resultados medidos.

Primario: delta pareado W/L/T vs base por rival/semilla, asientos promediados,
IC95 semilla y dos vías, desglose por rival. Noop exacto y cero errores.

Selección exploratoria por mayor delta global, desempate alfabético. Si el mejor
alcanza ≥+5 y al menos dos rivales positivos sin ninguno <−20, PROMISING:
confirmar únicamente ese candidato frente a base/noop en **993000–993015**, mismo
pool y ambos asientos (27 cruces ×32 = **864 episodios**). Confirmación no se
fusiona con piloto ni se amplía al mirar resultados. Si el punto de confirmación
es ≥+5 y no hay regresión >20 por rival, puede justificar un envío como
REAL_WORLD_CANDIDATE con incertidumbre explícita. No promover champion sólo por
esta selección; exige respuesta real. Si no cumple, conservar resultado y causa,
sin reenviar otra versión casi idéntica a modo de boleto.

Un resultado ≤0 o un IC que cruza cero no prueban inutilidad universal del
mecanismo: sólo impiden gastar el bloque registrado en estas versiones. Si una
regresión contiene información de mecanismo útil, investigar esa diferencia en
otra hipótesis registrada. No lanzar ambos bloques a la vez con 16 workers;
esperar que termine forecast y conservar su evidencia.



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

> **Estado vigente (2026-09-25 UTC): leer primero `docs/research/ESTADO_INVESTIGACION.md`.**
> Desde el 2026-09-21 el usuario autorizó un loop autónomo de investigación que
> incluye submissions experimentales ("También tienes capacidad para crear y
> subir submissions reales. Usa ambas cosas"). Mejor referencia real:
> **arshs3 (56511619), 2292,5 @148 episodios**; VQ experimental **56535264**
> enviada y COMPLETE. No volver al campeón histórico de 1180. Creencias con evidencia:
> `docs/research/RESEARCH_BELIEFS.md`; historial reproducible de envíos:
> `docs/research/SUBMISSION_HISTORY.json`; qué métrica local predice el ladder:
> `docs/research/HARNESS_VS_LEADERBOARD.md`. Lo que sigue abajo es el estado
> del 2026-09-14 y se conserva como historia.

## Loop continuo vigente

El 2026-09-25 UTC el usuario pidió explícitamente investigar y probar muchas
variantes en un loop continuo: **no parar al cerrar cada ronda**. Objetivo
persistente activo. Leer `docs/evidencia/loop_publicos_20260925/pipeline_state.json`
y `docs/research/SCORECARDS_LOOP_2026-09-25.md` antes de lanzar corridas.
`continuar_loop_publicos.py`, `continuar_loop_herd.py`,
`continuar_loop_recuperacion.py`, `continuar_loop_tomate.py` y
`continuar_loop_productos.py`, `continuar_loop_relleno.py` y
`continuar_loop_patrones.py` encadenan bloques
registrados; no duplicar procesos ni alterar sus agentes en ejecución. Confirm1
terminó: top3 +10,795 pp, candidata real; loop3 sin mejoras, loop4 inconcluso
(una de64 partidas cambia, +1,5625pp). Confirm5 tomate−21,591pp: REJECTED.
Loop6 sin seleccionadas; loop7 corre y loop8 está validado/encolado. No repetir las
versiones infill2/3: v4 corrige interferencia R51 y overflow de cosecha.
Top3 enviada **56537205 COMPLETE**, commit ba1fda8, sha9668e30a; validación720
pasos DONE/DONE sin errores/timeouts. VQ2364,6 en snapshot02:04UTC, aún joven.
Conserva VQ56535264 como control; tres envíos restantes reportados. Ver historial.
Al completar los bloques, revisar resultados y seguir con la siguiente hipótesis
o submission justificada. Cierre de bloque no equivale a cierre de investigación.

## Estado y autorización

- El usuario autorizó explícitamente subir `maj_107674293`: «Subela a kaggle pa
  que coja calle». Envío realizado: **56245770**, inicialmente PENDING, el
  2026-09-14 23:52 America/Bogota. Esta autorización sustituye la restricción
  anterior para ese envío; no autoriza envíos adicionales automáticos.
- El 2026-09-14 el usuario autorizó investigación pública y nuevos experimentos
  locales ambiciosos a partir de ocho replays. Para esta ronda seguir el diseño,
  costes y reglas de parada de `docs/EXPERIMENTOS_ATREVIDOS_2026-09-14.md`.
  La autorización posterior de envío se documenta arriba; HOZ sigue como base
  local de comparación, y `submission/main.py` ahora contiene la cinta enviada.
- `CAMPEONA_HOZ` sigue siendo la base. `HOZ_LOTES` no fue adoptado tras su réplica;
  tener una configuración o un `main.py` preparado no significa aprobación.

## Leer en este orden

1. `docs/ESTADO_ACTUAL.md`: decisiones vigentes, qué está probado y qué falta.
   Para la ronda actual, `docs/RESULTADOS_LIDER_2026-09-14.md`,
   `docs/ANALISIS_LIDER_2026-09-14.md` y su pre-registro.
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
Ronda del 2026-09-14: `docs/evidencia/lider_20260914/`, `evaluar_lider.py` y
`bots/experimentos_lider.py`. No modificar fuentes incluidas en un manifiesto
mientras esté corriendo el bloque correspondiente.
`results/`, `replays/` y `.venv/` están ignorados por Git; comprobar disponibilidad.
No ejecutar las sondas antiguas que importan `lab.py` sin verificarlo: ese archivo
no está en este checkout.

Para preparar contexto para otro LLM, sin red ni simulaciones:

```bash
./.venv/bin/python preparar_contexto_llm.py
```

Genera `docs/CONTEXTO_LLM.md` y comprueba la evidencia histórica de lotes.
Verificar la nueva ronda por separado con `./.venv/bin/python verificar_lider.py`.
La petición concreta para otro LLM está en `docs/REVISION_LIDER_PARA_LLM.md`.
No empaqueta ni envía
submissions. Para información actual de Kaggle, usar una consulta explícita y
fechada; los ratings en documentos son snapshots.



---

## SOURCE: docs/ESTADO_ACTUAL.md

# Estado actual — leer primero

> **Este archivo conserva el traspaso del 14-sep.** Para decisiones vigentes,
> leer [ESTADO_INVESTIGACION](research/ESTADO_INVESTIGACION.md): loop autónomo
> autorizado, referencia arshs3 56511619 y VQ 56535264. No relanzar ni bloquear
> trabajo por las autorizaciones históricas que siguen.

## Envío autorizado — 2026-09-14, 23:52 America/Bogota

El usuario pidió «Subela a kaggle pa que coja calle». Se envió **`maj_107674293`**
como `submission/main.py`, submission **56245770**. Kaggle confirmó recepción;
estado inicial **PENDING**, sin score todavía. La CLI indicó **4 envíos restantes**
después de subir. Esto sustituye la prohibición previa para este envío concreto;
no implica autorizar más submissions ni que el candidato haya ganado en el ladder.

El paquete de 13.506 bytes incluye la cinta y sólo usa biblioteca estándar.
SHA-256: `7894c015654e18803b7f31e2c2d37127accb143fce007cec6e2db519f997ca08`.
Se comprobaron 721 acciones, aislamiento frente a mutaciones y cuatro pares de
partidas archivo/módulo, con 720 estados de juego equivalentes por par (ocho
episodios adicionales, semillas 218000–218001 y ambos asientos).

El archivo anterior se conserva en
`submission/archivo/main_cfad10b88abc38f8f7f79a3b83148f11e37d57865f37cea648cffa9bbcf1e1d7.py`.
`CAMPEONA_HOZ` permanece intacta como referencia local. Evidencia del envío y
validación: `docs/evidencia/envio_maj_20260914/`. No volver a enviar por encontrar
un estado PENDING; consultar por ID y distinguirlo de un envío fallido.

Snapshot de consulta anterior al envío: HOZ **702,0**, grano **718,4**. Son
ratings observados en esta consulta, no los 818,1/774,8 del historial.
Los informes de experimentos de abajo conservan el estado previo a este envío.

## Ronda del líder — 2026-09-14

El usuario autorizó investigación pública, análisis de ocho replays nuevos de
Majkel1337 y experimentos locales ambiciosos. En esa fase no había autorización
de envío; fue concedida después, como se registra arriba.
**Resultado de confirmación:** `maj_107674293` obtiene 71,49% frente a 57,13%
de HOZ: **+14,36 puntos**, IC95 por semilla **[+9,02; +19,71]**, dos vías
**[+6,71; +22,02]**. Se completaron 7.296 episodios, 19 semillas nuevas y ambos
asientos. Noop exacto en 1.824 comparaciones; FB −19,35 puntos, con ambos
intervalos negativos. Hay mejora positiva en el panel fijo, pero el estimador
queda por debajo del umbral registrado de 15 puntos para declarar el salto.

El piloto comparó once candidatos y tres controles. La cinta y el árbol empataron
en 64,06%; se eligió la cinta por desempate alfabético registrado, no por ventaja
demostrada sobre el árbol. La variante de ventas cambió acciones sin cambiar
W/L/T frente al árbol. Contra los ocho rivales nuevos de confirmación, el candidato
queda en 48,68% frente a 37,50% de HOZ; no confundir 71,49% agregado con dominar
el meta actual. Duelo diagnóstico contra HOZ vivo: 12 victorias y 4 derrotas.

Estrés completo de 512 episodios contra las ocho cintas de Majkel: candidato
90,62%, HOZ 11,72%. Son fuentes de desarrollo y el control FB cruza cero;
este resultado no es confirmación independiente ni una victoria sobre su agente
reactivo. Total de la ronda: 9.634 episodios locales, incluidos los diagnósticos
y reproducciones. Los registros, controles y fuentes se verificaron al terminar.

`CAMPEONA_HOZ` continúa como base y `submission/main.py` conserva el hash anotado
abajo. El candidato queda experimental, sin empaquetar ni enviar.

- [Resultados y diagnósticos](RESULTADOS_LIDER_2026-09-14.md).
- [Auditoría de los ocho replays](ANALISIS_LIDER_2026-09-14.md).
- [Protocolo anterior a las pruebas](EXPERIMENTOS_ATREVIDOS_2026-09-14.md).
- [Petición preparada para otro LLM](REVISION_LIDER_PARA_LLM.md).

**Historial anterior:** lo que sigue conserva las decisiones de septiembre 5–6;
sus restricciones de barridos no describen la nueva petición. Los ratings son
snapshots antiguos, no una consulta actual. La investigación del 14 no consultó
submissions por CLI ni verificó la cuota de envíos.

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
| IC95 de confirmación por semilla | [−0,67; +10,36] puntos; t=2,08 | Inconcluso según el criterio registrado |
| **Réplica, 16 semillas nuevas (103000–103015), 5.120 episodios** | **+0,23 puntos; t=+0,08 por semilla y a dos vías; ambos IC95 incluyen cero** | **REFUTADO. No adoptar; mecanismo cerrado** |

`noop` exacto en 1.280 episodios, `_peor` a −26,95 (t=−12,43) y el candidato
cambia acciones en 1.280/1.280: la bandera dispara y el panel discrimina. Es un
resultado nulo real. Ver [pre-registro](PREREGISTRO_REPLICA_LOTES.md).

**`harvest_76` REFUTADO (2026-09-05).** Ablación con 16 semillas nuevas
(104000–104015): `sin_h76` da **−0,08**, IC95 **[−0,65; +0,49]** por semilla y
[−0,63; +0,47] a dos vías. El intervalo **excluye el +2,5 atribuido**. Cambia
acciones en sólo 102/1.280 episodios. Sigue en la base activa por inercia; no
daña, pero no aporta. Ver [pre-registro](PREREGISTRO_ABLACION_H76.md).

**Calibración de la escalera:** `hoz` y `grano` son idénticas en el 92% de los
episodios y difieren −0,08 en panel, pero la escalera las separa 43 puntos
(818,1 vs 774,8). **Diferencias <50 puntos entre submissions propias no
informan.**

**`seed_stock_aware` CONFIRMADO (2026-09-06).** Ablación con 16 semillas nuevas
(105000–105015): `sin_ssa` da **−6,25**, IC95 [−11,15; −1,35] por semilla y
[−11,32; −1,18] a dos vías. **Ambos excluyen cero.** La magnitud replica el +6,4
original medido con semillas distintas. **El campeón está bien fundado**; su
ventaja sobre `CAMPEONA_FASE` viene de aquí, no de `harvest_76`.

**Diagnóstico del protocolo:** con 8 semillas el MDE al 80% de potencia es
**10,4 puntos**. Los tres mecanismos medidos (6,4 · 4,84 · 2,5) estaban por
debajo: nunca tuvimos potencia. Protocolo nuevo en
[BITACORA.md](BITACORA.md#2026-09-06) — piloto para estimar sd, dimensionar el
bloque, dos vías como análisis primario, ablación sobre la base activa.

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

## SOURCE: docs/RESULTADOS_LIDER_2026-09-14.md

# Resultados de la ronda del líder — 2026-09-14

**Mejora positiva en este panel, sin alcanzar el umbral registrado de 15 puntos.** El candidato `maj_107674293` mejora 14.36 puntos W/L/T frente a HOZ en confirmación. No se envió nada a Kaggle; `CAMPEONA_HOZ` y `submission/main.py` siguen intactos.

[Análisis de los ocho replays](ANALISIS_LIDER_2026-09-14.md) · [Protocolo anterior a las pruebas](EXPERIMENTOS_ATREVIDOS_2026-09-14.md) · [Evidencia](evidencia/lider_20260914/README.md)

## Confirmación independiente por semillas

Panel fijo: 40 cintas históricas y ocho rivales extraídos de los nuevos replays; 19 semillas 215000–215018, ambos asientos. Cuatro brazos, 7.296 episodios; 1.824 por brazo. W/L/T vale victoria=1, empate=0,5, derrota=0. Deltas e intervalos en puntos porcentuales frente a HOZ.

| Brazo | W/L/T | Delta | IC95 por semilla | IC95 dos vías |
|---|---:|---:|---:|---:|
| `base` | 57.13% | +0.00 | [+0.00; +0.00] | [+0.00; +0.00] |
| `noop` | 57.13% | +0.00 | [+0.00; +0.00] | [+0.00; +0.00] |
| `_peor` | 37.77% | -19.35 | [-22.05; -16.66] | [-25.69; -13.02] |
| `maj_107674293` | 71.49% | +14.36 | [+9.02; +19.71] | [+6.71; +22.02] |

Desglose descriptivo de confirmación (no cambia la regla primaria):

| Rivales | HOZ | Candidato | Delta |
|---|---:|---:|---:|
| 40 históricos | 61.05% | 76.05% | +15.00 |
| 8 nuevos | 37.50% | 48.68% | +11.18 |

Regla registrada: delta ≥15 puntos, ambos intervalos del candidato por encima de cero y ambos del control FB por debajo de cero. Candidato positivo en ambos: **True**; control FB negativo en ambos: **True**. El umbral de 15 se aplica al estimador puntual, no al límite inferior del intervalo.

El tamaño de 19 semillas se fijó antes de confirmar usando la dispersión del piloto. No se amplió al mirar resultados. Esta es confirmación en semillas disjuntas, con rivales parcialmente compartidos; no es validación externa del ladder.

## Todos los candidatos del piloto

Cuatro semillas 214000–214003, 16 rivales y ambos asientos: 128 episodios por brazo, 1.792 en total. La selección usa W/L/T agregado y desempate alfabético, fijados antes de correr. No se eligió por dinero ni por el intervalo más favorable.

| Brazo | W/L/T | Delta vs HOZ | Históricos (8) | Nuevos (8) |
|---|---:|---:|---:|---:|
| `maj_107674293` | 64.06% | +17.97 | 75.00% | 53.12% |
| `tree` | 64.06% | +17.97 | 62.50% | 65.62% |
| `tree_liquid` | 64.06% | +17.97 | 62.50% | 65.62% |
| `maj_107692988` | 59.38% | +13.28 | 62.50% | 56.25% |
| `maj_107710951` | 57.03% | +10.94 | 57.81% | 56.25% |
| `maj_107673304` | 55.47% | +9.38 | 73.44% | 37.50% |
| `maj_107674284` | 54.69% | +8.59 | 62.50% | 46.88% |
| `warmstart10` | 52.34% | +6.25 | 67.19% | 37.50% |
| `maj_107685970` | 48.44% | +2.34 | 56.25% | 40.62% |
| `maj_107675268` | 46.88% | +0.78 | 56.25% | 37.50% |
| `base` | 46.09% | +0.00 | 54.69% | 37.50% |
| `noop` | 46.09% | +0.00 | 54.69% | 37.50% |
| `maj_107696961` | 37.50% | -8.59 | 37.50% | 37.50% |
| `_peor` | 33.59% | -12.50 | 29.69% | 37.50% |

La cinta 107674293, el árbol y el árbol con ventas empataron en 64,06%. Confirmar la cinta cumple el desempate, pero no demuestra que supere al árbol. Las ventas reactivas cambiaron las acciones en los 128 episodios y no cambiaron W/L/T frente al árbol en ninguno: ejecución sin mejora observada. La apertura seguida de HOZ quedó en +6,25 puntos exploratorios.

El piloto pondera 50% rivales históricos y 50% nuevos; la confirmación pondera 40/48 y 8/48. Esa diferencia estaba registrada, pero puede cambiar qué arquitectura destaca. No reinterpretar los estratos después para rescatar un candidato.

Limitación de la variante de ventas: el proyector asume tablero 10×10 y shed de 100 unidades y no modela el caso en que PLACE de un animal cae al shed. No es un simulador general exacto. El bloque terminado mide esta implementación concreta; corregirla requiere otra variante y otro registro, no cambiar el código de una corrida. El candidato seleccionado no usa ese proyector.

## Diagnósticos posteriores, sin selección

Contra las ocho cintas de Majkel: ocho semillas 216000–216007, ambos asientos, cuatro brazos, 512 episodios. Son fuentes usadas para construir candidatos, no rivales reservados. Una cinta no responde como el agente original.

| Brazo | W/L/T | Delta vs HOZ | IC95 por semilla |
|---|---:|---:|---:|
| `base` | 11.72% | +0.00 | [+0.00; +0.00] |
| `noop` | 11.72% | +0.00 | [+0.00; +0.00] |
| `_peor` | 10.16% | -1.56 | [-14.59; +11.46] |
| `maj_107674293` | 90.62% | +78.91 | [+68.86; +88.95] |

En este estrés, el intervalo del control FB cruza cero: el bloque no demuestra discriminación entre FB y HOZ. Su ventaja observada para el candidato se conserva como diagnóstico; no satisface por sí sola el protocolo de confirmación ni prueba que gane al líder reactivo.

Contra HOZ vivo: **12 victorias, 4 derrotas y 0 empates**, W/L/T 75.00%, en 16 partidas (ocho semillas 217000–217007, ambos asientos). IC95 t por semilla del score: [+36.30; +113.70] puntos. Es un diagnóstico pequeño; este intervalo aproximado no está restringido al rango [0,100].

## Integridad y límites

Los tres paneles completos tienen cobertura cartesiana, cero episodios inválidos y noop exacto en acciones emitidas, rewards, estados de finalización, pasos y llamadas. Los hashes de acciones se capturan antes del motor. Se archivaron fuentes y protocolo antes de cada bloque y se comprobaron hashes de motor y cintas al finalizar. Los paneles conservan hashes, no todos los estados intermedios; la comparación explícita de 720 estados completos corresponde a las ocho reproducciones originales.

`verificar_lider.py` vuelve a comprobar registros comprimidos, cobertura, controles y fuentes archivadas, y reconstruye los resúmenes con la función estadística del evaluador. No constituye una segunda implementación independiente de los intervalos.

Coste: 1.792 piloto + 7.296 confirmación + 512 estrés + 16 duelo + 18 reproducciones/sondas = **9.634 episodios locales**. No consumen envíos de Kaggle. Los tiempos de decisión registrados son locales, no una prueba del paquete en el runtime de Kaggle.

No se verificó Elo, rank actual ni el comportamiento reactivo del líder. Los ocho replays son victorias seleccionadas. Tres de sus rivales comparten un prefijo de 120 acciones: agrupar por nombre no garantiza independencia de estrategias. Un buen resultado local contra cintas no garantiza transferencia a oponentes nuevos o adaptativos.

## Qué probar después

1. **Reservar familias de rivales nuevas antes de desarrollar.** La principal incertidumbre es transporte, no optimizar décimas en este panel. Propuesta: ocho familias no usadas, 16 semillas y ambos asientos, cuatro brazos = 1.024 episodios; fijar identidades, hashes y regla de decisión antes del primer resultado. Si no hay familias nuevas verificables, no llamar a la prueba holdout de rivales.
2. **Aprender las ramas del árbol con información visible.** El árbol actual usa una regla manual de tiendas. Comparar cinta seleccionada, árbol congelado y router aprendido con partición por familias y semillas; no elegir tiendas o pesos mirando confirmación. Primero definir dataset y presupuesto, luego evaluar.
3. **Reparar compromisos de la ruta, no sólo vender más.** La capa de ventas no aportó victorias en el piloto. Una reparación útil debe registrar compras ejecutadas, inventario y cohortes para evitar que una acción fallida rompa el calendario. Comenzar con diagnóstico de 16 partidas preseleccionadas; sin evidencia de ese mecanismo, parar antes de un barrido.

La idea de rutas y ligas tiene precedentes públicos: el autor de [Three Day Shop Router](https://www.kaggle.com/code/yhay81/three-day-shop-router/comments) describe copias simplificadas de rutas públicas y evaluación en muchas semillas. Es un reporte del autor; no descargamos su implementación ni verificamos su velocidad anunciada. Esta ronda construye y mide nuestras propias variantes.

## Reproducir y revisar con otro LLM

```bash
./.venv/bin/python verificar_lider.py
./.venv/bin/python preparar_contexto_llm.py
./.venv/bin/python preparar_contexto_llm.py --check
```

Entrada experimental de la cinta: `bots.meta.tape.make('maj_107674293')`. Las variantes nuevas están en `bots/experimentos_lider.py`. Los evaluadores rechazan sobrescribir una corrida existente: para repetirla usar una copia del repo y conservar los originales. No ejecutar `submission/main.py` ni empaquetar por interpretar este informe como autorización de envío.



---

## SOURCE: docs/ANALISIS_LIDER_2026-09-14.md

# Qué muestran los ocho replays de Majkel1337

Análisis del 2026-09-14. [Experimentos y pre-registro](EXPERIMENTOS_ATREVIDOS_2026-09-14.md). [Evidencia](evidencia/lider_20260914/README.md). No se realizó ningún envío a Kaggle.

## Qué está comprobado

Se reprodujeron exactamente las ocho partidas, comparando 720 estados en cada una. Las ventas y compras se midieron al ejecutarse en el motor y los flujos concilian con el dinero final de ambos jugadores. Las cantidades siguientes son operaciones efectivas, no órdenes solicitadas.

| Episodio | Rival | Dinero Majkel / rival | COW / SHEEP / GOOSE d15 | Mayor ingreso efectivo |
|---|---|---:|---:|---:|
| 107673304 | jps | 172,108 / 22,437 | 14 / 4 / 0 | MILK: 98,205 |
| 107674284 | aditya emmadishetty | 166,660 / 42,759 | 5 / 14 / 0 | WOOL: 75,653 |
| 107674293 | yaki-imo | 83,495 / 65,976 | 5 / 9 / 4 | WOOL: 27,264 |
| 107675268 | VYSHAKH G NAIR | 144,211 / 36,028 | 7 / 10 / 0 | WOOL: 54,043 |
| 107685970 | PursueML | 91,028 / 81,433 | 6 / 3 / 4 | STRAWBERRY: 30,034 |
| 107692988 | xiao xiongwei | 75,166 / 61,639 | 6 / 3 / 4 | WHEAT: 26,199 |
| 107696961 | goh | 138,737 / 116,161 | 7 / 15 / 0 | WOOL: 90,156 |
| 107710951 | Ryosei Hara | 149,376 / 130,400 | 11 / 3 / 2 | MILK: 68,513 |

![Economías y rebaños](evidencia/lider_20260914/economias_lider.png)

## Mecanismos que merecen una prueba

1. **Apertura con compromisos coordinados.** Compra dos vacas y tres ovejas en los dos primeros turnos en las ocho partidas. Planta doce melones temprano, compra el segundo cuadrante en step 149 (d6 h5) y amplía el rebaño desde d6. No equivale a subir una perilla de animales en nuestra apertura actual.

2. **Economías diferentes entre partidas.** En d15 tiene 13–22 animales; hay casos con 15 ovejas y otros con 14 vacas. La lana aporta 90.156 monedas contra goh y la leche 98.205 contra jps. Es compatible con adaptación a demanda/rival, pero ocho trazas no identifican su regla ni separan causalmente los efectos de tiendas y rivales.

3. **Comprar forraje y vender trigo no se contradicen automáticamente.** Compra 174–389 unidades de trigo por partida, además de cosechar y vender 290–680. La fecha, ubicación y caja son parte de la política. Un cambio global de BUY_FEED no reproduce esa secuencia.

4. **Rutas compatibles permiten ramificar.** Cuatro cintas comparten sus primeras 86 acciones completas. Dos de ellas comparten 145. Las tiendas aparecen desde d3, de modo que se puede decidir en ese punto usando información ya visible, sin cambiar el prefijo ejecutado ni consultar el futuro. Esto motivó el árbol probado.

5. **El coste del trabajo también cambia.** Sus compras efectivas de peones cuestan entre 4.662 y 5.086 monedas por partida. Las órdenes PASS representan 0,68–0,97% de las acciones emitidas de unidades; movimiento y acciones fallidas no se cuentan como PASS y no son necesariamente trabajo útil.

## Lo que no podemos concluir

- El Elo y rank no vienen en los JSON. El usuario identifica al líder; no se verificó el ranking actual mediante la página, cuyo contenido dinámico no se recuperó.

- Los IDs y sus diferencias no bastan para afirmar evolución durante varios días. Tampoco un marcador alto identifica un rival de Elo bajo.

- Son ocho victorias seleccionadas. No estiman win rate del líder ni representan toda la población. Tres rivales (xiao xiongwei, goh y Ryosei Hara) comparten sus primeras 120 acciones; ocho nombres no significan ocho estrategias independientes.

- Reproducir una cinta con su semilla y rival originales prueba fidelidad de extracción. En escenarios nuevos, la cinta deja de representar las respuestas que elegiría el agente original.

## Errores de las conclusiones anteriores que estos datos obligan a revisar

La réplica de lotes con +0,23 e IC95 aproximadamente [−6,2; +6,7] no prueba un efecto exactamente nulo: no confirma la mejora. Tampoco una diferencia aislada de ratings demuestra que toda diferencia menor de 50 sea informativamente nula. El supuesto techo de la apertura se midió alterando capital de un planner concreto; no acota el valor de cambiar su calendario completo, geometría y logística. Conservamos esas notas como historia, no como motivos para prohibir estas pruebas.

Para decisiones competitivas se usarán los bloques preregistrados y sus controles, no los ingresos de esta tabla. Ver [resultados y diagnósticos completos](RESULTADOS_LIDER_2026-09-14.md).



---

## SOURCE: docs/EXPERIMENTOS_ATREVIDOS_2026-09-14.md

# Experimentos estructurales a partir de ocho replays nuevos

Fecha: 2026-09-14. Petición vigente: investigar en internet, analizar los ocho
replays y ejecutar experimentos locales ambiciosos. **No autoriza envíos a
Kaggle.** Las restricciones anteriores sobre barridos quedan sustituidas para
esta investigación. `CAMPEONA_HOZ` y `submission/main.py` se conservan.

## Evidencia antes de los experimentos

Los ocho episodios corresponden a Majkel1337 contra ocho rivales distintos.
El usuario lo identifica como primer lugar; los archivos no contienen Elo ni
rank. No asignaremos Elo por dinero final. Son ocho victorias seleccionadas,
no una muestra aleatoria. Los IDs no demuestran por sí solos fechas distintas.

`investigar_lider.py` extrajo ambas cintas con offset +1. Reprodujo los 720 estados
de cada episodio con su semilla original, comparando granjas, privados, mercado,
tiendas, día y hora. Todos coinciden. Un ledger observado en `_commit_unit`
registra operaciones aceptadas, precio por unidad y costes atómicos; concilia
exactamente $3.000 + flujos con el dinero final de cada jugador. No usamos el
estimador antiguo `ventas_reales.py`, que no resuelve ventas a $1, órdenes
fallidas, DROP simultáneo ni precios de cada unidad de la ráfaga.

Datos: `evidencia/lider_20260914/replays.json`, `validacion.json` y ledgers.
Cintas: `bots/meta/tapes/maj_*.json.gz` y `sepopp_*.json.gz`.

Hallazgos descriptivos: 12 melones tempranos en todas las aperturas; segundo
cuadrante en step 149 en las ocho; al día 15 hay entre 13 y 22 animales con
composiciones diferentes. Son calendarios e interacciones que no se reproducen
simplemente aumentando `animals` en nuestro chasis. Los cuatro replays 107685970,
107692988, 107696961 y 107710951 comparten sus primeras 86 acciones; los dos
últimos comparten 145. Es posible ramificar sin cambiar el prefijo de acciones.

## Información pública consultada

- [Experiencia de un participante con cintas y ligas](https://www.kaggle.com/competitions/kaggriculture/discussion/739273):
  reporta fuerte transferencia de economías grabadas y renovación del meta.
  Es evidencia reportada por su autor, no nuestra réplica.
- [Ramificar replays según tiendas](https://www.kaggle.com/competitions/kaggriculture/discussion/738727):
  Yusuke Hayashi describe ramificación temprana como técnica de su agente.
  Inspira nuestra comparación de prefijos; no se descargó ni copió su código.
- [Resultados preliminares de RL](https://www.kaggle.com/competitions/kaggriculture/discussion/740022):
  Roy Wei reporta 350 millones de pasos y falta de validación contra una liga.
  No es evidencia de que RL sea imposible ni garantía de un ganador rápido.
- [Límites de clonación de conducta](https://www.kaggle.com/competitions/kaggriculture/discussion/738079):
  el autor describe errores acumulados al pasar de evaluación offline a ejecución.
  Motiva verificar la conducta y la legalidad en partidas completas.

## Pre-registro de exploración (antes de evaluar candidatos)

Pregunta: ¿un cambio de arquitectura supera claramente a HOZ, y las adiciones
reactivas mejoran una cinta sin romper su economía? Buscamos saltos de al menos
15 puntos W/L/T; esta ronda no intenta resolver décimas.

Implementaciones nuevas, aisladas en `bots/experimentos_lider.py`:

1. **Ocho cintas originales:** controles de transferencia y ocho candidatos de
   referencia, sin modificar acciones. Seleccionarlas también es búsqueda.
2. **Árbol de rutas:** usa sólo información visible. Prefijo común hasta d3;
   elige ruta por la tienda actual. Rama lana/leche a d6 sólo entre las dos
   cintas que comparten ese prefijo. Nunca consulta tiendas futuras ni semilla.
3. **Árbol con ventas reactivas:** misma producción; vende productos no usados
   como insumo cuando realmente están en shed, incluyendo DROP del mismo turno.
   Conserva cantidades programadas de WHEAT/FERTILIZER y las otras compras.
   Hipótesis: menor retraso al monetizar sin desfinanciar la ruta.
4. **Apertura transferida:** sigue una cinta hasta d10 y continúa con HOZ.
   Hipótesis: el planificador propio aprovecha una estructura inicial distinta.
   No es repetir la antigua perturbación de cantidad de animales.

Base HOZ, noop exacto y control anterior FB exacto: **14 brazos** en total.
Piloto: **cuatro semillas 214000–214003**, ambos asientos, ocho cintas `lad_`
espaciadas uniformemente por nombre (índices 0,5,...,35) y los ocho rivales
`sepopp_` aportados. Selección del panel independiente del rendimiento.
Coste: 14 × 16 × 4 × 2 = **1.792 episodios**, además de ocho reproducciones y
sondas técnicas pequeñas. Progreso y registros incrementales; ocho workers.

El piloto sólo selecciona UNA configuración por W/L/T agregado, con desempate
por nombre. Reportar todos los brazos y los dos estratos. Es exploración, no
confirmación; estos 16 rivales no se presentan como muestra del ladder actual.
En piloto la integridad exige noop exacto y cero errores; el control FB debe
dar delta negativo, sin exigir significancia con cuatro semillas. La confirmación
sí exige intervalos negativos para ese control. La sonda técnica previa (semilla
213000, un rival, cinco brazos) sólo comprobó prefijos, conducta y finalización;
sus marcadores no eligen al ganador del piloto.

## Confirmación prevista

Si el mejor candidato mejora al menos 15 puntos a HOZ en piloto con controles
válidos, congelarlo y compararlo con base, noop y FB en **las 40 cintas lad_ y
los ocho sepopp_**, ambos asientos, semillas desde **215000**. Ese panel es fijo;
40 rivales antiguos y ocho recientes no equivalen al leaderboard futuro.

Dimensionar ANTES de confirmación con sd de los cuatro promedios por semilla:
`n = min(32, max(16, ceil(((1.96+0.84)*max(sd,0.10)/0.15)**2)))`.
Es aproximación de potencia al 80% para 15 puntos en panel fijo; con cuatro
semillas sd es incierto, por eso suelo 0,10 y mínimo 16. Si requiere >32,
declarar el límite presupuestario y no afirmar potencia suficiente. Máximo
48 × 32 × 4 × 2 = **12.288 episodios**. No se aumenta n al mirar resultados.

Primario: delta pareado por (rival,semilla), asientos promediados, IC95 t entre
promedios de semilla. Sensibilidad registrada: agrupamiento a dos vías
`V_rival + V_semilla - V_celda`, df del clúster menor. El panel es fijo para
el estimando primario; dos vías no convierte familias de cintas en rivales
independientes. Exigiremos ambos intervalos >0, delta >=15 puntos y control FB
negativo en ambos para llamar al resultado salto local confirmado. La varianza
de dos vías negativa se reporta como inválida, no como certeza.

Noop debe ser idéntico por episodio en acciones, rewards, estados y pasos.
Errores, timeouts, faltantes o cambios de fuentes invalidan el bloque. Se congelan
hashes del código, motor y cintas; no se editan mientras corre.

Después, diagnóstico contra las ocho cintas del líder (fuentes de entrenamiento,
no holdout independiente) y contra HOZ vivo, con nuevas semillas y ambos asientos.
No llamar al candidato ganador del ladder por esos diagnósticos. El candidato
sigue experimental y no se empaqueta en `submission/main.py`.

Si el piloto no supera el umbral, documentar fallos y el mecanismo observado;
no gastar el bloque de confirmación ni rescatar por dinero final.



---

## SOURCE: docs/evidencia/lider_20260914/README.md

# Evidencia de la investigación del líder — 2026-09-14

`replays.json` describe los ocho archivos de Downloads, sus hashes y sus
resúmenes de conducta. Los JSON originales no se modifican ni se duplican aquí.
No contienen Elo de los jugadores. `validacion.json` registra reproducción exacta
de 720 estados en cada partida y contabilidad efectiva por operación/producto.

`ledger_*.jsonl.gz`: commits efectivos del mercado y costes de HIRE/BUY_LAND,
con jugador, turno, producto y cambio de dinero. Los SELL de una unidad a $1
también se contabilizan. Proceden del motor 1.32.7 durante la reproducción exacta.

Las 16 cintas compactas de ambos jugadores están en `bots/meta/tapes/`:
`maj_<episodio>.json.gz` y `sepopp_<episodio>.json.gz`. Incluyen el offset +1
correcto y PASS terminal. No sustituyen las cintas `lad_` del panel histórico.

Los archivos de evaluación usan prefijos `pilot`, `confirm_*` y `stress_*`:

- `*.meta.json`: diseño, estado, versiones, hashes, configuraciones, resúmenes.
- `*.episodes.jsonl` y su copia `.gz`: resultados incrementales, estados, tiempos
  y hashes de acciones emitidas. Conservar al menos la copia comprimida junto al manifiesto.
- `*.sources.tgz`: código y protocolo congelados antes de la corrida.
- `sonda_tecnica.json` y `perfiles_sonda.json`: diagnósticos, no confirmaciones.
- `confirmacion_registro.json`: selección y tamaño registrados desde el piloto,
  antes de lanzar confirmación. `decision.json` aplica los criterios registrados.
- `duelo_hoz.json` y sus episodios: diagnóstico contra HOZ vivo, ocho semillas
  nuevas y ambos asientos. Su script guarda el diseño antes de ejecutar.
- `perfil_control_apertura.json`: cinta original de control para interpretar la
  sonda de apertura, sin usar su dinero para seleccionar candidatos.

Verificación sin partidas: `./.venv/bin/python verificar_lider.py`. Revisa los
tres paneles, selección, fuentes estables entre bloques, semillas y duelo. Usa
la misma función estadística del evaluador; no es una réplica independiente del
cálculo de intervalos. `resultados_lider.py` genera el informe desde los cuatro
bloques completos. No interpretar archivos `running` como resultado final.

`economias_lider.png` se genera desde datos descriptivos con `resumir_lider.py`.
Las fuentes del experimento se congelan durante cada bloque; nunca inferir fuerza
de un bloque cuyo manifiesto no diga `complete`. Las tablas no predicen Elo.

Estos archivos quedan fuera de exclusiones Git, pero no se crea automáticamente
un commit ni se envía nada. Para repetir la auditoría de estados completos hacen
falta los JSON originales; para repetir evaluaciones bastan código, motor y cintas.



---

## SOURCE: docs/REVISION_LIDER_PARA_LLM.md

# Revisión independiente de la ronda del líder

Esta es una plantilla que el usuario puede entregar a otro LLM. No autoriza
envíos a Kaggle ni nuevas simulaciones por sí misma.

## Petición sugerida

Actúa como revisor crítico de este repositorio. Lee `ESTADO_ACTUAL.md`,
`RESULTADOS_LIDER_2026-09-14.md`, `ANALISIS_LIDER_2026-09-14.md` y el protocolo
`EXPERIMENTOS_ATREVIDOS_2026-09-14.md`. No aceptes el veredicto sólo porque dos
modelos coincidan. Distingue observaciones, inferencias, propuestas y resultados.

Reconstruye desde `docs/evidencia/lider_20260914/`:

1. Selección del candidato entre los once candidatos y tres controles del
   piloto. Comprueba el empate entre cinta y árbol, el desempate registrado y
   que el tamaño de confirmación se fijó antes de observar sus resultados.
2. Deltas pareados con ambos asientos, agregación por semilla y sensibilidad a
   dos vías. Recalcula las fórmulas independientemente de `summarize` si vas a
   afirmar una auditoría estadística independiente.
3. Noop exacto, control FB, cobertura completa, hashes, semillas disjuntas y
   ausencia de errores. Verifica qué se conserva como estados y qué sólo como
   hashes de acciones; no confundas emisión con ejecución económica.
4. Límites del panel: cambio registrado de pesos 8/8 a 40/8, rivales compartidos
   entre desarrollo y confirmación, familias con prefijos comunes, ocho victorias
   seleccionadas y falta de Elo en los JSON. Explica qué afirmación permiten
   los datos y cuál no.
5. Código de `bots/experimentos_lider.py`: disponibilidad temporal de tiendas,
   prefijos antes de ramificar, copia de acciones, transferencia a HOZ y límites
   del proyector de inventario. Un defecto en una variante no prueba un defecto
   en el candidato que no la usa.

Entrega objeciones priorizadas con archivo, evidencia y consecuencia. Para cada
idea nueva especifica mecanismo, intervención aislada, control, unidad de
análisis, tamaño, coste, partición de desarrollo/confirmación, criterio y regla de
parada antes de proponer ejecutar. El objetivo es transporte a escenarios nuevos,
no rescatar retrospectivamente una celda o ganar dinero en una sola sonda.

## Material mínimo

- Lectura rápida: este archivo y el informe de resultados.
- Contexto documental completo: `docs/CONTEXTO_LLM.md`.
- Auditoría: repo completo con `docs/evidencia/lider_20260914/` y las cintas de
  `bots/meta/tapes/`. `results/` no es necesario para los resúmenes transportables.
- Reproducción de los 720 estados originales: requiere además los ocho JSON de
  Downloads indicados en `replays.json`; sus rutas externas pueden no existir en
  otro equipo. La evaluación frente a cintas no requiere esos JSON originales.

```bash
# Sólo lectura/verificación; no ejecuta nuevas partidas ni usa Kaggle.
./.venv/bin/python verificar_lider.py
./.venv/bin/python preparar_contexto_llm.py --check
```

El primer comando requiere scipy para cuantiles t. El segundo usa biblioteca
estándar y verifica la evidencia histórica de lotes y la vigencia del contexto;
no sustituye la verificación de los experimentos nuevos.



---

## SOURCE: docs/BRIEFING.md

# Kaggriculture — briefing de incorporación

**Ronda nueva del 2026-09-14:** ver [resultados del líder](RESULTADOS_LIDER_2026-09-14.md)
y [auditoría de los ocho replays](ANALISIS_LIDER_2026-09-14.md). Los ratings y
restricciones temporales que aparecen abajo pertenecen al historial anterior.

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

## Ronda vigente — 2026-09-14

El usuario autorizó los experimentos locales de la ronda del líder. Consultar
[protocolo](EXPERIMENTOS_ATREVIDOS_2026-09-14.md) y
[resultados](RESULTADOS_LIDER_2026-09-14.md) antes de proponer otro bloque.
La cola técnica siguiente es histórica; no justifica repetir compras parciales
sin revisar la réplica posterior ni desplaza la nueva investigación de rutas.
Las propuestas siguientes a esta ronda están en el informe de resultados, con
sus costes y reglas de parada. No se autoriza ningún envío a Kaggle.

Para otro LLM: reconstruir primero selección, controles y deltas de la nueva
evidencia con `verificar_lider.py`, y distinguir semillas nuevas de rivales nuevos.
Preguntar si las familias de rutas compartidas y la ponderación 8/8 frente a
40/8 limitan la conclusión. El acuerdo entre modelos no sustituye una réplica.

## Cola histórica del traspaso anterior

Estado anterior: propuestas, no experimentos autorizados. La última corrida de Kaggle
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
Estado final (2026-09-05, tras réplica): **REFUTADO**. Tres bloques: +5,00 (4
semillas), +4,84 (8), **+0,23 (16)**. El bloque de mayor potencia da cero con
integridad impecable. No adoptar; mecanismo cerrado.

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


## Bloque 3 — réplica independiente (2026-09-05)

Pre-registrado en [PREREGISTRO_REPLICA_LOTES.md](PREREGISTRO_REPLICA_LOTES.md)
antes de ejecutar. Semillas **103000–103015** (16), disjuntas de los bloques 1 y
2 y de la sonda. 40 cintas × 2 asientos × 4 brazos = **5.120 episodios**.

Motivo: el reanálisis mostró que el veredicto del bloque 2 dependía de la unidad
de agrupamiento (celda +2,45 / semilla +2,08 / cinta +2,83 / dos vías +2,52).
El diseño es **cruzado** (40 cintas × 8 semillas, ambas dimensiones aleatorias),
así que el estimador correcto es el de dos vías `V_cinta + V_semilla − V_celda`.
**Conflicto declarado en el pre-registro:** ese estimador se calculó DESPUÉS de
ver el bloque 2 y cambiaba el veredicto. Mitigación: exigir que **ambos**
criterios excluyan cero.

### Integridad

- `noop` **exacto** en los 1.280 episodios.
- `_peor` (CAMPEONA_FB exacta): **−26,95**, t=−12,43 por semilla y −7,77 a dos
  vías. El panel **tiene resolución**.
- `partial_batch` cambia acciones en **1.280/1.280** episodios: la bandera
  dispara. Resultado nulo real, **no** test nulo.

### Resultado

| criterio | t | IC95 | veredicto |
|---|---|---|---|
| por semilla (n=16) | +0,08 | [−6,20; +6,67] | incluye cero |
| dos vías (df=15) | +0,08 | [−6,01; +6,48] | incluye cero |

**Ambos incluyen cero → NO adoptar.** Por el pre-registro no se encadena un
cuarto bloque ni se fusionan los tres.

### Lección de método

El veredicto conservador del bloque 2 ("inconcluso, no adoptar") era el correcto.
El reanálisis a dos vías es estadísticamente más apropiado para este diseño, pero
se usó para **cruzar la línea con un resultado fronterizo después de verlo**.
Ante un efecto en el borde, la respuesta no es un estimador mejor: son más datos.

**Corolario abierto:** `harvest_76` está en la misma situación (+2,50, t=+1,76 a
dos vías, IC95 [−0,85; +5,85]) y nunca tuvo réplica con potencia. Está dentro de
`CAMPEONA_HOZ`, la base activa.



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

## Veredicto histórico de lotes reproducido desde episodios

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
