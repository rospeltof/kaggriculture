# Scorecards del loop continuo — 2026-09-25 UTC

Estado: loops 1–4 y confirm1 terminados; loop5 de tomates corriendo;
loop6 encadenado. Objetivo persistente activo.

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
