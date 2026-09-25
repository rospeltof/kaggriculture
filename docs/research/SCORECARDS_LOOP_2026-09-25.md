# Scorecards del loop continuo — 2026-09-25 UTC

Estado05:38UTC: pilotos1–11 y confirm1/5/7/8/10 completos; piloto12 corriendo.
Loops13–16 validados y encolados. Objetivo persistente activo.

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
