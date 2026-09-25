# Scorecards del loop continuo — 2026-09-25 UTC

Estado09:11UTC:pilotos1–16/18/19y confirm1/5/7/8/10/13completos.
Confirm19original completo pero INVÁLIDO por cuatro noops de hash rival.
Confirm19_fixedhash0corre; mismo diseño, runtime fijado, no muestra adicional.
20–26validados/encolados;17detenido. Objetivo activo.

48reproducciones/4hashseeds identifican orden de ventas rival dependiente del
hash, mismos720estados económicos/acciones propias/rewards en seis celdas.
Perfilado2juegos localiza sorted(set)sin desempate; fuentes externas intactas.
Smoke técnico6juegos/noop2verifica hash0uniforme en workers. No validar original
ni usar sus deltas; adenda en `REPARACION_HASH_RUNTIME_2026-09-25.md`.

Loop25 reutiliza cinco fuentes validadas, sin aumentar el total89. Panel distinto
contra VQ/top3/V7/HS4 reactivos, confirmación con dos fuentes adicionales.
Piloto1.920 y confirmación1.920/2.560 pendientes; no hay resultados nuevos aún.
Analizador comprobado con fixture de1.920partidas históricas: +2,734375ppcontra
primera referencia y0contra segunda selecciona ninguna. Noop448exacto, cero
simulaciones nuevas. No cambiar los gates/resultados históricos de otros paneles.

## Loop26 en espera: semillas por cultivo y reposición

40desarrollos, noop5.752turnos, máximo327ms; seed_kind activa2/8celdas y
seed_jit8/8.76modificaciones de compra aceptadas exactas; campo, siembras,
alimentación, cosechas, tiendas, escapes y pérdidas conservados en desarrollo.
Ahorro0–20monedas, ceroW/L/Tcambiados; no estimación competitiva. Piloto960
tras25contra panel cercano, ambas referencias reales; total91variantes y
2prototipos detenidos. Ver informe/preregistro26; no hay resultados de piloto.

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

## Piloto7 y confirmación en curso

1.248 episodios, noop256/256, cero errores. Base89,0625%. Infill4/8_d16
inertes128/128. Infill4/8_d18 +1,5625pp cada una, IC95 dos vías[−3,41;6,54];
cambian16/128 partidas en semillas1010001/009. Ambas pasan a confirm7 según
regla positiva:1.600 partidas, once rivales,16 semillas disjuntas. Sin envío.

Mecanismo infill4_d18: ars40/1010001/asiento0, primera diferencia436. Cuatro
plantas/16 tomates extra, cosecha confirmada y sin faltantes. Venta total de
tomate80→96, ingreso30.024→34.386; margen−1→+2.206. Tiendas posteriores
cambian; no atribuir todo el margen al tomate. Modelo cotiza9.756 de ingreso
para inversión que cuesta4.614, pero omite tomates V219 comprometidos aún
sin plantar. Las fuentes del bloque activo permanecen intactas; registrar
esta omisión para revisar mecanismo/posible nueva variante tras confirmación.

Cuatro filas TDS en seed1010007: acciones propias iguales, hash rival distinto,
rewards/WLT idénticos. Ocho reproducciones con PYTHONHASHSEED0–3 dieron
estados/acciones idénticos y no reprodujeron el hash alternativo. Origen neutral
aún no resuelto; no afecta selección observada. No alterar harness basándose
en una conjetura. Evidencia `pilot7.neutral_trace_audit.json`.

## Loop9: rebaños, desarrollo terminado y fuentes v3 encoladas

Seis tamaños/fechas,2/3/6 ovejas desde12/14, sin tierra nueva. V1 iniciaba
cosechas demasiado tarde; V2 reserva viaje/cosecha/descarga.22 juegos válidos,
noop1.438 acciones y cero escapes antes de última producción. Motor real
confirma36/53/83 lanas cosechadas y depositadas en forzadas2/3/6, ambos asientos
(seis comprobaciones). V1 y V2 se conservan con sus fuentes/resultados.

V3 añade seis ovejas propias compradas aún sin colocar y lana privada al
modelo de oferta.22 juegos adicionales, controles exactos; forzadas tienen
exactamente las acciones de ambos agentes y rewards de v2, por lo que heredan
prueba de entrega. Normales inertes en el mundo dirigido, por filtro económico.
No es señal poblacional ni refuta la hipótesis. Manifiesto v3 fijado antes
de iniciar piloto9;1.920 partidas encoladas tras loop8. Máximo de desarrollo
<1s, volver a medir en bloque aleatorio.

Búsqueda pública adicional no identificó un código inequívoco de c0nrad.
[V35](https://www.kaggle.com/code/ahmedberatozer/kaggriculture-v35-reactive-sales-sheep-expansi)
describe expansión financiada ya presente en nuestra genealogía; no se repite
como candidata nueva. La fuente útil para esta ronda es el replay auditado.

## Confirm7: sin activación en muestra disjunta

1.600 episodios, noop416/416, cobertura y hashes archivados verificados.
Ambas d18 conservan acciones propias/rivales y rewards en352/352 partidas
contra el pool; base79,545%, delta0. IC95 dos vías indefinido, no evidencia
de precisión perfecta. INCONCLUSIVE_NOT_SELECTED: no beneficio confirmado;
no enviar ni bajar el gate a posteriori. La omisión de oferta V219 sigue
siendo un defecto del modelo, pero no justifica repetir el bloque sin una
hipótesis nueva. Piloto8 empezó03:23:41UTC tras cerrar confirm7.

## Piloto8: memoria larga y ajuste temporal a confirmación

1.472 episodios, noop224/224, cero errores, fuentes verificadas. Base96,875%:
techo alto del panel. Rank5/history360/phase2 empatan+1,5625pp (IC dos vías
[−2,13;5,26]), una celda mejor y ninguna peor. Desempate alfabético registrado
elige history360/phase2; no subir rank5 por parecer simple a posteriori.
Rank7−3,125pp, history120−10,9375, product3−1,5625; IC amplios cruzan cero.
Todas alteran acciones; history36086/128, phase296/128, demás128/128.
Confirm8 desde03:45:23UTC,1.600 episodios,16 semillas disjuntas/11rivales.

Cuatro reproducciones de mecanismo completas, rewards originales y caja
conciliados. History360 vsTDS/1013006/asiento0: tres acciones distintas desde625,
margen−254→+255, mismas tiendas/unidades vendidas; fresa+311de ingreso,
leche−12 y trigo+5. Phase2 vsTDS/1013007/asiento0:17acciones desde388,
margen−444→+69, tiendas iguales,142patrones desplazados; leche+263, dos
huevos extra/+88, lana+4 y fresa−12. Una activación forecast adicional en
cada caso. No atribuir todo el margen al precio propio: también cambia el
dinero del rival. Evidencia `pilot8.{history360,phase2}.mechanism.json`.

## Loop10: conversión temprana, desarrollo y cola

La base YA convierte vacas/gansos a ovejas con YARN entre días8–11. El hueco
nuevo es3–7, compras nativas de1–2 vacas; se conserva logística y no se compran
más peones/tierra. Seis políticas: inicio3/6 ×(mínimoYARN,reserva)=(1,100),
(2,100),(1,500). No es el modelo de futuras tiendas/EV del loop3.

48 juegos mecánicos:1004000/1017000 inertes por no haber YARN temprano;
1272457736, escogido por YARN/YARN del replay c0nrad, con rival arshs3 reactivo:
seis variantes idénticas en ese mundo, dos COW→SHEEP en173/178, dos colocaciones
aceptadas y49 lanas cosechadas. Sin escapes, créditos pendientes ni inventario
privado final. Noop4.314 turnos exactos, máximo284ms, sin errores. No se afirma
que sean idénticas en todos los mundos.1.920 partidas encoladas detrás de loop9.

La sonda ilustra el precio endógeno: lana propia410→459, ingreso94.662→93.400;
dinero114.856→112.753. Rival114.184→104.003 y margen+672→+8.750. Ambos ya
eran victorias; no seleccionar por ese margen ni confundir más lana con más
ingreso propio. Archivo `early_cow_validation.json`, protocolo loop10.

## Feedback03:39 y auditoría de biblioteca

Top31941,6/30episodios listados, VQ2259,1/56; consulta real03:39:41UTC,
aunque nombres de archivos dicen0333. Muestra fija por endTime: cuatro
victorias,923–2891de margen.720 estados exactos y caja conciliada por partida,
cero escapes propios/inventario final. Producción parecida a sus rivales;
no representa la diversidad de todo el ladder ni comparación causal conVQ.

Biblioteca original2.398streams,24–63por cada uno de64pares. Sin fechas/ids
originales recuperables (ids−1): no afirmar antigüedad. Doce streams aceptados
recientes (DSM4, rivales top3 ocho) son distintos semánticamente; Jaccard de
eventos más cercano0,118–0,573. No agregan pares de tiendas. Preparados en
`recent_sale_streams.json`, aún sin agente ni evaluación. No es precisión OOS.

## Confirm8: señal pequeña de memoria larga, desfase no confirma

1.600episodios, noop416/416, cero errores, fuentes/coverage verificadas. Base
82,9545%. History36085,7955%, delta+2,8409pp, IC95dos vías[−1,249;6,931];
6celdas mejores y1peor,318/352acciones cambian. PROMISING, pero no alcanza
gate3: no redondear ni enviar por seleccionar un subpanel. Ningún rival tiene
delta agregado negativo; eso no niega la existencia de la celda de daño.

Phase279,5455%, delta−3,4091pp, IC[−13,23;6,412];5celdas mejores/11peores,
298/352acciones cambian. INCONCLUSIVE_NOT_SELECTED. No envío para ambas.
Máximos propios history360220ms/phase2198ms, lejos del límite1s.

Daños reproducidos, tiendas iguales/caja conciliada: history360 vsTDS25,
1014014/asiento0, primera diferencia655 y6acciones; margen+189→−61,
mismas cantidades vendidas, leche−40/fresa+2 de ingreso propio. Phase2 vsars40,
1014006/asiento0, primera430/11acciones; margen+492→−79, leche−79,
fresa−74, lana−4 y dos huevos menos/−103. No son fallos de ejecución.
Sondas `confirm8.{history360,phase2}.harm.json`; no redefinen el estimador.

## Loop11: biblioteca reciente validada y en cola

Tres fuentesets sobre top3:DSM4, rivales recientes8, ambas12. Ranking nativo
intacto y prioridad de streams antiguos en empates.20juegos dirigidos,
noop2.876turnos exactos; variantes también idénticas en par FARM/FARM sin
datos. Máximo250ms. YARN/YARN: DSM se expone pero no se selecciona, ladder/all
seleccionan113126108 en164ajustes por asiento y cambian18turnos. Uno de los
mundos de desarrollo viene de un replay fuente: no presentarlo como OOS.

Piloto1.920con32semillas1021000–031, cuatro rivales fuertes fijos;
confirmación32semillas1022000–031,2.304/3.200con11rivales. Mayor diversidad
de mundos porque sólo10/64pares tienen datos nuevos. Runner espera loop10.

## Loop12: aperturas y actualización pública

MarketEngine de ejecución02:50 es tds25 byte exacto: excluido. MarketShock
cambió, pero su loader elegía instalador. Corrección de entrada verificada
contra política nominal del autor en8juegos;0–4 contra top3 en2semillas,
márgenes−4.517/−835, WR inerte. No es torneo de promoción/rechazo general.

Tres aperturas sobre top3 (Original/EarlyCycle/TomatoInsteadOfCow) más ese
paquete público se registran en loop12.12juegos de desarrollo, noop1.438turnos,
max229ms, cero errores observados. Original cambia42turnos; EarlyCycle sólo1,
mismos rewards; Tomato261, una vaca menos y4tomates cosechados/vendidos. No
asumir mejora por mayor dinero total: también cambian tiendas/rival. MarketShock
un escape de ganso647/asiento; se conserva el caso, no se oculta.

Trigo temporal observado: base/cycle cosechan3unidades en87; el contador
heredado espera cosecha53 y por eso marca0. Tomato/MarketShock cosechan2en53.
No concluir que la rama no corrió porque ese contador sea0. Piloto1.008,
semillas1025000–007; confirmación1026000–015. Runner detrás de loop11.

**Piloto12 terminado:**1.008 episodios, noop192/192, cero errores,
cobertura/hashes verificados. Base82,8125% frente a ocho rivales.

| Variante | Delta pp | IC95 dos vías | Acciones propias distintas | Decisión |
|---|---:|---|---:|---|
| open_original | −3,125 | [−10,276;4,026] | 128/128 | Inconcluso, no seleccionado |
| open_cycle | 0 | Indefinido | 128/128 | Sin señal W/L/T, no seleccionado |
| open_tomato | −80,46875 | [−104,038;−56,899] | 128/128 | Rechazado |
| marketshock | −64,0625 | [−104,437;−23,688] | 128/128 | Rechazado |

No se ejecuta confirm12. Los intervalos lineales no están truncados a los
límites físicos del delta. Cycle no es inerte pese al mismo W/L/T.
Seis juegos adicionales explican celdas registradas, sin ampliar la muestra:
tomate/ars40/1025000 pasa margen+2.441→−4.999 aunque propio88.750→93.280;
cambian tiendas. MarketShock en la misma celda pasa a−3.748 con mismas tiendas;
en1025004 mejora−85→+538, pero no rescata el resultado agregado. No atribuir
el paquete completo a una sola capa. Ledger/rewards reproducidos exactamente.
Evidencia `pilot12.results/validation/behavior.json` y `pilot12.*.harm/benefit.*`.

## Piloto9 completo: seis rebaños inertes

1.920episodios, noop320/320, cero errores, fuentes/cobertura verificadas.
Cada una de las seis políticas conserva acciones propias/rivales en128/128
partidas contra pool. Delta0, ICdos vías indefinido; no confirmar ni enviar.
No se guardaron motivos de rechazo por cada juego: no atribuir toda inercia
a la misma condición sin sonda. No repetir estos brazos para buscar seeds
favorables. Piloto10 arranca04:29:14UTC con1.920partidas de conversión temprana.

## Logística nocturna: mecanismo nuevo y desarrollo loop13

c0nrad113107623:33unidades propias perdidas en cinco noches, rival0;
720estados exactos/caja conciliada.395lanas cosechadas vs391vendidas y
249fresas vs244vendidas. El inventario terminal0 no detecta esa pérdida.
Motor vivo confirma las predicciones de guardas5/5; JSON aislado reordena
inventarios y predice pérdida espuria de trigo en527. No alterar harness
por esa observación ni vincularla sin prueba a la incidencia neutral pilot7.

Loop13 propone cuatro reservas1/2días y venta de trigo o ambos inputs para
liberar espacio. Cambia mezcla final y precio/timing: requiere competencia
reactiva.36juegos dirigidos registrados,1.248piloto nuevo tras loop12 si valida.
V1falló noop por entrada equivocada, omitiendo VQ. Se archiva como inválida;
V2corrige sólo captura del último callable y repite desarrollo. No seleccionar
por los diez resultados parciales de v1.

V2validada:36juegos, noop4.314turnos exactos,22activaciones con predicción
de pérdida/vector final exacta contra motor. Ventas aceptadas verificadas;
max291ms, cero errores/escapes/inventario final. Perfil de animales sin
alimentar al cierre y tiendas idénticos a base.1272457736:reserva1día27→8
unidades perdidas,2días27→20.1004000:1día24→16,2días inerte.1027000:trigo1día
y ambos inputs13→4; trigo2días inerte. FERT sí se vende con ambos inputs en
último mundo. Mecanismo validado, no selección competitiva ni solución completa.
Piloto1.248 encolado detrás de loop12, fuentev2 congelada.

Snapshot real04:30:35UTC:top32022,5/46episodios listados;VQ2288,2/69,
ambasCOMPLETE. Incluyen validación. Ficheros sufijo0431 con hora real en
metadatos. No envío nuevo ni declaración de superioridad causal.

## Piloto10 completo y financiación de alimento

1.920episodios, noop320/320, cero errores. Base88,28125%. Cada pareja D3/D6
es idéntica en acciones propias/rivales y rewards128/128; no son réplicas.

| Configuración (ambas fechas) | Delta pp | IC95 dos vías | Celdas mejores/peores | Acción cambia /128 |
|---|---:|---|---|---:|
| y2_m100 | +2,34375 | [−4,57;9,26] | 2/0 | 8 |
| y1_m100 | −8,59375 | [−32,30;15,11] | 2/7 | 32 |
| y1_m500 | −2,34375 | [−18,95;14,26] | 2/3 | 24 |

Y2activa sólo1018011. Las dos fechas seleccionadas por regla previa van a
confirm10 (1.600,1019000–015), desde04:52:36UTC. No intercambiar brazos tras
observar equivalencia ni presentar ocho celdas como ocho mundos independientes.

Mecanismo positivo reproducido hybu/1018011/asiento1: compras173/178,
SHEEP17→19/COW6→4, lana410→459, leche166→121, cero escapes, margen−355→+6.895.
Mecanismo adverso ars40/1018001/asiento0, y1_m100: mismos dos swaps, lana254→283
pero leche164→44, margen+1.037→−22.858. Tiendas idénticas, caja conciliada.
La auditoría física encuentra tres vacas escapadas239 sólo en candidato.

Cadena de financiación verificada: gasto extra200; antes de191 caja220→20,
ambos piden WHEAT8 y reciben7→0. En194/197/218/222/226, el actor base dispone
de5/4/5/4/3trigos y el candidato0. Tres vacas pasan dos noches sin alimento y
escapan239. No reducir este resultado a saturación de lana. Evidencia:
`pilot10.physical_audit.json`, `pilot10.funding_failure.json` y replays archivados.
La próxima política requerirá reservar insumos futuros; confirm10 queda intacta.

## PASS productivos y loop14 alimentación

Ocho replays previamente fijados por recencia,720estados exactos cada uno y
caja conciliada. Auditar antes del refresh elimina falsos huecos de trabajo
que otros actores completan después. Entre esas oportunidades no quedan CARE
útiles omitidos;60huecos WATER no mejoran yield inmediato/próximo amanecer ni
evitan muerte esa noche. No generalizar a rutas mejores o efectos posteriores.
261huecos FEED sí existen, pero pueden ser ahorro intencional del filtro nativo.

Loop14 abla esa valoración:0,5/2,5frente a1,25, conservar todo FEED ovino o
todo FEED nativo.36juegos en3mundos/ambos asientos, noop4.314turnos exactos,
max271ms, cero errores/escapes/stock terminal; todas activan en los3mundos.
Cada FEED aceptado consume1trigo según motor, cosechas también medidas. En
1030000, leche242→228/256/266 con half/double/all. Cantidad no equivale a
beneficio. Piloto1.248(1031000–015) encolado tras loop13; confirmación condicional
1032000–015. Fuentes y ledgers congelados antes del piloto.

## Confirm10 completa: contexto raro sin activación

1.600episodios, noop416/416, cero errores, cobertura/fuentes verificadas. Ambas
y2 conservan acciones propias/rivales352/352contra11rivales; delta0, ICdos vías
indefinido. No envío ni rechazo universal del mecanismo: no se activó aquí.
Piloto11 arrancó05:11:34UTC,1.920episodios/32semillas, biblioteca reciente.

Snapshot real05:13:31UTC:top32068,8/58episodios listados yVQ2287,2/81,
ambasCOMPLETE. Incluyen validación. Fuentes sufijo0515; no atribuir diferencia
de ratings a causalidad ni cambiar agente base de los bloques ya registrados.

## Loop15: reserva de caja para insumos próximos

Cuatro nuevas políticas reservan compras programadas de alimento hasta cierre,
24/48turnos, o todas las obligaciones24turnos. Costes visibles con colchón,
sin ingresos futuros acreditados; no es una simulación exacta de acciones
adaptativas futuras. Control antiguo y1_m100 se incluye sólo para atribución.

42juegos completos, noop4.314turnos exactos, máximo293,94ms, cero errores y
stock terminal0. El caso adverso reproduce compra191=0 y tres escapes en
antigua, frente a7compras/0escapes en base. Night convierte una vaca, compra
4trigos/0escapes; no financia todo el pedido8. Las otras tres conservan base.
En el solvente, night/24convierten ambas vacas y compran8trigos, sin escapes;
48/all24inertes allí. Nuevo1033000noactiva ninguna. No seleccionar por rewards.

Fuentes/ledgers congelados, `cash_validation.json` aprobada. Piloto1.568
(1034000–015) encolado tras14, control antiguo excluido de promoción;
confirmación1035000–015. Total67variantes competitivas distintas construidas.

## Piloto11 completo: datos nuevos, sin cambio W/L/T

1.920episodios,32semillas/4rivales/ambos asientos, noop448/448, cero errores.
Base89,453125%; DSM/ladder/all mismo WR, delta0 e ICdos vías indefinido. DSM
inerte256/256. Ladder/all cambian18/256acciones propias y10rivales, en semillas
1021015/024/025. Ambas coinciden en todos los hashes/rewards256/256del pool;
no son réplicas independientes. Sin selección/confirmación ni nuevo envío.

Primera celda ordenada con acción distinta, sin filtro W/L:ars40/1021015/asiento0.
Reproducción completa/caja conciliada, primeras diferencias436,12turnos distintos,
iguales tiendas y cantidades vendidas. Un stream nuevo se selecciona13veces;
forecast134→135unidades/21activaciones. Caja propia132.326→132.335; rival
131.215→131.237; margen1.111→1.098, ambas victorias. No inferir mejora de
precisión o fuerza sólo de añadir fuentes. `pilot11.library_ladder.changed.json`.

Piloto12comenzó05:35:02UTC,1.008episodios de aperturas.

## Campo y composición inicial (loop16)

Doce replays top3 reproducidos720estados cada uno:3CARROTdecay,1sequía,
4MILKmaduras al final.33MILKse truncan en primer yield de vacas tardías con
inventario previo0; cosechar antes no rescata ese exceso de cuidado.14EGGcon
inventario previo podrían requerir nuevas rutas/entregas. Ningún parche general
de cosecha registrado; siguiente hipótesis valora bonus limitado por capacidad.

Loop16: cuatro mezclas iniciales con±1/2vacas/ovejas, iguales trabajadores y
pasturas.48juegos, noop5.752turnos, max328,55ms, cero errores. Costes reales
±100/200 y cantidades exactas compradas/colocadas; crédito0al día1. Todas
cambian acciones en4mundos. Sheep1/2cambian primeras tiendas4/4: no es sólo
intercambiar producción sobre un mercado idéntico. Sheep2pierde una vaca215
en1272457736; base/cow1también tienen escapes tardíos en1036000. Se archivan
sin descartar esos episodios ni escoger por rewards. Stock privado final0.

Piloto2.496(1037000–031) encolado detrás de15, confirmación condicional32seeds
1038000–031. Total71variantes competitivas construidas, no71mejoras.


## Loop17 detenido antes del piloto: stock presente versus nocturno

Dos prototipos, cap_first/cap_full,24juegos de desarrollo en tres mundos,
noop4.314turnos, max284ms, fuentes y consumo de FEED verificados. El informe
`capped_bonus_validation.json` pasa ejecución; **no es aprobación competitiva**.
`capped_bonus_decision.json` marca DEVELOPMENT_STOPPED/competitive_ready=false.

Cap_first modifica una valoración de vaca en1272457736pero no las acciones:
la otra guarda nativa impide omitir ese FEED. Cap_full modifica tres turnos en
1039000por asiento: omite FEED682, luego HARVEST687de4EGG libera el espacio,
y HARVEST700recibe1EGG en vez de2. FEEDGOOSE52→51y EGG91→90. No escapa un
animal, pero el supuesto de bonus marginal0 es falso. Detención por error de
modelo, no por comparar dinero de estas partidas ni prueba poblacional.

No se ejecutaron las704partidas de piloto17. El runner rechaza arrancar y se
comprobó que no sobrescribe el estado activo. Una versión futura debe modelar
la cosecha antes de la noche o limitarse a stock vacío verificable y comprobar
la alimentación siguiente. No reciclar el mismo modelo bajo otro nombre.

## Loop18 validado y en cola: V7/HS4 públicos de04:09UTC

Fuentes cda529cb/8378f73c extraídas como literales y archivadas, distintas de
las anteriores.24juegos en1042000/1042001, ambos asientos contra top3; noop
2.876turnos e igualdad oficial/nominal5.752turnos. Máximo431ms,720DONEsin
estados fatales y nuevos contadores internos observados sin errores. No se
recopilaron todos los contadores heredados. Caja conciliada en cada partida.

Ambas cambian acciones en los dos mundos: V7133/122turnos yHS477/72.
Mismas tiendas, sin escapes ni productos finales en almacén/bolsas; sí quedan
1/5semillas. No se selecciona por24rewards ni por promesas del notebook.
Primera sonda falló por una aserción de identidad demasiado estricta entre
wrapper y función envuelta; evidencia archivada, fuentes sin modificar.

Piloto704semillas1043000–015, confirmación1044000–015, cuatro/once rivales,
gate≥3pp/peor rival≥−20pp. Runner espera fin16directamente;17no tiene torneo.
Total73variantes competitivas construidas más2prototipos17detenidos.


## Piloto13 completo: ahorro nocturno a confirmación

1.248 episodios, noop256/256, cero errores, hashes/cobertura completos.
Base87,5%. Wheat1/inputs1/inputs2:+4,6875pp, IC95semilla[−2,558;11,933],
ICdos vías[−6,969;16,344]. Wheat2:+3,125pp, ICdos vías[−5,997;12,247].
Inputs1/2: tres celdas mejores en dos semillas, ninguna peor; propias56/128
cambian y rivales52/48. Coinciden ambas acciones/rewards96/128, no son copias.
Desempate alfabético registrado selecciona inputs1/2. Confirm13de1.600juegos
con once rivales y16semillas nuevas comenzó06:02:06UTC; no leer parcial para
adoptar o detener. Todavía no cumple confirmación ni justifica subir.

`auditar_piloto_almacen.py`:12juegos (base/dos en todas las tres celdas mejores,
asiento0, más primera celda ordenada de acciones distintas/WLTigual), hashes
propios y rewards exactos del piloto,720DONE/caja conciliada. Ocho activaciones
predicen vector y pérdida nocturnos exactamente; mismas tiendas, ningún escape.

| Celda | Margen base | Inputs1 / inputs2 | Pérdida base | Inputs1 / inputs2 |
|---|---:|---:|---:|---:|
| arshs3/1028001 | −25 | +81 / +51 | 8 | 4 / 6 |
| arshs3/1028013 | −205 | +291 / +218 | 27 | 9 / 17 |
| tds/1028001 | −100 | +25 / +14 | 9 | 5 / 6 |
| ars40/1028000, neutral W/L | +151 | +634 / +634 | 6 | 3 / 3 |

En las tres primeras no cambia alimentación al cierre; inputs1/arshs3/1028001
fertiliza/cosecha7zanahorias más. En la neutral ambas omiten3FEEDCOWen652,
bajan cosechas3MILK/2EGG y dejan tres vacas más sin alimentar en671, sin escape.
Un FEEDfallido de oveja608ya existe en base, no atribuirlo al parche. Esto
no prueba escasez física: hay que separar orden omitida de FEED emitido fallido.
Las reservas no garantizan producción ni conducta futura, aunque aquí gane.
Fuentes en `pilot13.sources.tgz`; resultados físicos/summary/plan y24archivos
comprimidos de ledger/unidades bajo `pilot13.physical.*`. Diagnósticos no suman muestra estadística.


## Confirm13 terminada: mecanismo activo, sin cambio de resultados

1.600episodios1029000–015, noop416/416, cero errores, fuentes y cobertura
verificadas. Base91,19318%. Ambos candidatos delta0, ICdos vías indefinido,
0celdas mejores/peores,176iguales; **INCONCLUSIVE_NOT_SELECTED**, gatefalse.

No son inertes: inputs1cambia107/352acciones propias y78rivales en7semillas;
inputs2cambia86/352propias y66rivales en6semillas. Márgenes diagnósticos:
inputs1sube103veces/baja4, rango[−133;+1.190], media+88,83;
inputs2sube82/baja4, rango[−140;+1.183], media+76,47. No sustituir W/L/T por caja.

Cuatro reproducciones, primera celda ordenada con cambio de acciones por
candidato sin filtrar W/L: ars40/1029003/asiento0. Ambas cambian6turnos,
primero575, reportan9unidades rescatadas y conservan tiendas. Recompensas
base75.411/73.139→75.707/73.050: victoria antes y después. Ledger/caja exactos,
telemetría sin errores observados. Estos diagnósticos no agregan muestra.
Piloto14arrancó06:21:20UTC; no se envía almacén13.

## Loop19: compras grandes de trigo, separado de ADV

Nuevos brazos wheat_front/half/both sobre top3.30diagnósticos, noop4.314turnos,
max305ms,720DONEsin errores, fuentes y cantidades/slots reales comprobados.
En588616997vsarshs3reactivo, prioridad20turnos; mitad/ambas38compras editadas
y79turnos distintos. Prioridad conserva cantidades/cosechas, reduce coste
agregado de3.388compras152.918→151.703. Mitad/ambas compran2.011y venden2.304,
frente a3.388/3.683base; también añaden2FEEDCOW/2MILK. Mismas tiendas/pérdidas,
ningún escape ni producto terminal.1045000/1028000inertes en todos los brazos.
Esto no selecciona por dinero ni estima ventaja contra today.

Nuestra fuente exacta reprodujo719acciones/720estados del replay today. Sus
44compras grandes tienen cantidades idénticas al plan nativo; rival compra
mitad en11y prioriza slot en20. Cobertura estática sólo5/64pares de tiendas:
enmienda anterior a cualquier episodio piloto19amplía16→32semillas por bloque,
con rangos consecutivos/gate intactos. Se detuvo sólo el runner19en espera y
se reinició con32, sin tocar14activo. Piloto1.9201046000–031, confirmación
2.304/3.2001047000–031, en cola tras18. Total76variantes competitivas más2
prototipos17detenidos. Ver TRIGO_REVENTA, protocolo y wheat_trade_coverage.json.


## Piloto14 terminado: alimentación adicional no paga en este panel

1.248episodios1031000–015, noop256/256, cero errores, fuentes/cobertura válidas.
Base91,40625%. Todos los brazos cambian128/128acciones propias.

| Brazo | Delta pp | IC95dos vías | Decisión |
|---|---:|---|---|
| half | −12,5 | [−33,693;8,693] | Inconcluso, no seleccionado |
| double | −26,5625 | [−51,898;−1,227] | REJECTED |
| keep_sheep | −50,78125 | [−81,903;−19,66] | REJECTED |
| all | −64,84375 | [−92,17;−37,518] | REJECTED |

Ninguna confirmación/envío. Ocho diagnósticos: primera celda ordenada de daño
por brazo,720DONE/caja y rewards exactos, tiendas preservadas. Half/ars40/1031006
margen+738→−318; caja propia+1.989y rival+3.045. Double/1031002margen+333→−322,
MILK151→171vendidas pero8.038→7.785monedas. Keep_sheep/all/1031001coinciden:
WOOL259→278por sólo183monedas más, WHEAT384→365y−634monedas; margen322→−391.
Estos casos explican daños particulares; no suman muestra ni generalizan su
mecanismo a todas las derrotas. Archivos `pilot14.*.harm.*` y behavior.json.
Piloto15de1.568episodios arrancó06:36:09UTC. Objetivo continuo activo.


## Desarrollo20 completo y en cola

30juegos en1048000/1048001/588616997, ambos asientos frente a arshs3reactivo;
noop4.314turnos exactos, máximo357,83ms, fuentes verificadas,720DONE/caja
conciliada, cero errores/escapes/producto final. Tres brazos activos en tres
mundos:20unidades34operaciones/680unidades;50→56/2.800;80→56/4.382. Total146
compras y146cierres,7.862unidades, todas compradas y vendidas al turno siguiente.
42cierres ya contenían SELLWHEAT reactivo del padre por cantidad menor a la
comprada: se amplió hasta lo comprado mediante máximo, sin sumar ni duplicar
órdenes. Ninguna cantidad desviada a comida.

Alimento, cosecha, pérdidas y tiendas iguales a base en los18juegos candidatos.
En estos mundos la caja de cada operación coincide con el modelo sin rival;
no generalizar esa ausencia de interferencia. Rentas por juego/asiento:
1048000=26/64/105monedas,1048001=24/68/103,588616997=8/24/36. Son diagnóstico
mecánico, no criterio de selección ni efecto competitivo probado. No elegir80
por esos ingresos. Piloto1.920/32semillas1049000–031en cola tras19; confirmación
condicional1050000–031. Total79variantes competitivas más2prototipos17detenidos.


## Piloto15completo: financiación reparada no basta

1.568episodios1034000–015, noop288/288, cero errores/fuentes/cobertura válidas.
Base96,875%. Night/24−12,5pp, ICdos vías[−36,221;11,221], no seleccionadas;
48/all24delta0, inertes128/128. Legacy−18,75(ICcruza0), sólo control diagnóstico.
Night/24mejoran6,25ppcontra legacy pero no pasan criterio primario vs base.
Night/24cambian40/32partidas propias, en5/4semillas; iguales entre sí104/128
partidas por ambos hashes/rewards. No son réplicas independientes ni equivalentes
por tener el mismo W/L/T. Sin confirmación/envío.16arrancó06:55:12UTC.

Ocho diagnósticos: primera celda ordenada dañada vsbase y primera reparada
vslegacy, todos enars40/asiento0, cuatro brazos por caso. Hashpropio/rewards
exactos del torneo, caja conciliada; tiendas iguales a base.

- 1034010 daño: base+1.619; legacy/night/24−3.173. Compran8trigos en191y ningún
 escape. DosCOW→SHEEP; WOOLvendida278→324pero50.174→45.380monedas; MILK191→137
 y35.962→27.989. No atribuir esta derrota a escasez de alimento.
- 1034015 reparación: base+845; legacy−25.130, trigo191=0y tresCOWescapan239;
 night+2.102, una conversión/trigo4/ceroescapes;24conserva base/trigo7. Night
 cambia producción, sin promesa de preservar leche; repair es caso dirigido.

Evidencia `pilot15.physical.*`,16ledgers de mercado/unidades y plan de selección.
Diagnósticos no agregan muestras estadísticas; no rescatar por caso favorable.


## Loop21: señales adicionales, VQ control y fuentes nuevas

42 partidas en tres mundos y ambos asientos; noop idéntico en 4.314 turnos,
fuentes verificadas, 720 estados DONE y caja conciliada. Máximo 292,36 ms,
sin errores, escapes ni producto privado al final. Los cuatro brazos cambian
acciones en los tres mundos. Se verificaron apoyo, cantidad y horizonte de
las señales emitidas y las ventas reales frente a las órdenes finales.

En 1051000, rank2/quorum/short12 cambian 101/110/100 turnos por asiento y
sustituyen 18 unidades de trigo cosechado por 15 zanahorias; lana +8/+8/+9.
Half cambia 48 turnos y cosecha tres lanas menos. En 1326447728, los cuatro
cambian 38–47 turnos, con lana +5/+6 y leche −3/−4. En 1418183474 cambian
2/3/12/7 turnos, sin diferencias de comida/cosecha. Tiendas preservadas en
todos. Son efectos del estado y precios posteriores, no una promesa de que
un cambio de ventas conserve todas las decisiones productivas.

No se seleccionaron brazos por estos rewards. Piloto de 2.016 partidas en
1052000–015 en cola tras20; confirmación disjunta1053000–015. VQ control
ineligible, seis rivales piloto/trece confirmación, gate adicional ≥0 frente
al VQ del mismo bloque. Fuentes en `extra_forecast_smoke.sources.tgz`;
validación `extra_forecast_validation.json`. Total83variantes más2prototipos.

## Cierre de pilotos16y18; fuente22y suministro23

Piloto16:2.496episodios,32semillas/noop512, cero errores. Base92,1875%.
Todos los brazos cambian256/256acciones propias y rivales del pool.

| Variante | Delta pp | IC95dos vías | Decisión |
|---|---:|---|---|
| initial_sheep1 | −86,71875 | [−95,610;−77,828] | REJECTED |
| initial_sheep2 | −92,1875 | [−101,469;−82,906] | REJECTED |
| initial_cow1 | −92,1875 | [−101,469;−82,906] | REJECTED |
| initial_cow2 | −92,1875 | [−101,469;−82,906] | REJECTED |

Sin seleccionadas ni confirmación. Intervalo lineal sin truncar; −101no es
probabilidad. Cuatro diagnósticos (primera celda adversa de sheep1y cow1,
ambas ars40/1037000/asiento0) reproducen rewards y caja. Cambian tiendas.
Sheep1: propia134642→135473(+831), rival134465→143436(+8971), margen177→−7963.
Cow1: propia105990/rival111109, margen−5119; leche245→248vendidas,
pero ingresos48611→26013. Lana99→127, ingreso5498→21802. No aislar especies
sin considerar el calendario de tiendas y otras decisiones inducidas.

Piloto18:704episodios/16semillas/noop192, cero errores; base90,625%.
V7−21,875pp, ICdos vías[−57,741;13,991], INCONCLUSIVE_NOT_SELECTED.
HS4−30,46875pp, IC[−56,648;−4,290], REJECTED. Ambos cambian128/128acciones
propias,128/126rivales; no seleccionados ni confirmados. Se conservan como
rivales22/23según preregistro, sin retirar a posteriori por rendimiento.
Cuatro diagnósticos con caja/rewards exactos, tiendas preservadas:V7en
ars40/1043000margen898→−62, HS4enars40/1043005margen821→−158.
HS4vende254lanas en ambos, pero ingreso24682→24240. V7cambia producción
(leche201→204, huevos89→91, fresas251→249): no es sólo cola de ventas.

Harvest V68nuevo07:12+selector-off:42desarrollos válidos/noop4314/entrada8628,
max713ms. Selector añade1/1/2animales distintos, créditos cerrados, cero escapes
ni productos finales; tienda cambia en un mundo. Piloto22de1280en cola tras21.
Ver `FUENTES_PUBLICAS_0712_2026-09-25.md`;85variantes construidas al registro.

Suministro23buy/hold: construcción87variantes total, aparte2prototipos17.
24desarrollos contra arshs3completos, ambos brazos inertes en tres mundos.
Contra replaydavion la regla general compra11en vez de6, rescata24lanas,
margen−2904→1255; no prueba poblacional ni contra rival reactivo. Adenda24
partidas de cobertura contraVQ/V7/HS4fijada antes de observarlas. No seleccionar
por rewards dirigidos ni confundir cero cambios con refutación del mecanismo.

Validación23completa:48juegos/noop8.628/max326,96ms,0errores/escapes/productos
finales, mismas tiendas. Ambos brazos activos sólo contraV7reactivo en mundo
1578791335, ambos asientos: compra11/retirada6verificadas,6FEEDrestaurados,
WOOL389→413cosechada. Margen−5090→−1093; sigue derrota. Buy/holdequivalentes
12/12celdas de desarrollo; rama de venta retenida sin cobertura aún. Runner23
encolado tras22, piloto2.560con32semillas nuevas yVQcontrol. No es envío aprobado.


## Piloto19positivo y loop24validado

Piloto19:1.920/noop448/ceroerrores,32semillas. Base87,109375%, cada variante
89,84375%; delta+2,734375pp, ICdos vías[−3,903;9,372],4celdas mejores/0peores.
Las tres activas16/256en2semillas; igualesW/L/T256/256pero sólo240/256pares de
acciones/rewards. Desempate registrado selecciona both/front; confirmación3.200
1047000–031contra11rivales activa07:57UTC. No adopción antes de confirmación.
Ocho auditorías físicas reproducen hashes/rewards/caja, mismas tiendas, cero
escapes:frontahorra1508/941por las mismas3385/3382compras de trigo. Half/both
reducen volumen; en1046028cambian cosechaWHEAT505→508yCARROT180→177.

Loop24:advanceVQ/advanceTop3, adelanto de compra nativa y descuento del llenado
real antes de guardas.36juegos/noop8.628/max307,58ms,64compras/4480unidades
confirmadas. Activa sólo593858505, dos mundos inertes. Cuatro adelantos parciales
86/89con residual3que no llena por capacidad; resto total. Alimento igual,
una cosecha3CARROT→3WHEAT, ventas también adelantadas. Noop separado por padre.
VQbase y top3control en piloto2.560/32semillas pendiente tras23.89variantes
construidas más2prototipos detenidos. Reproducción rivalgrabadoGrimReaper
−3070→313; no estima WRreactivo. Sonda384escenarios/1152piernas exactas explica
interacción con horario rival/consumo; no selección por dinero sintético.
