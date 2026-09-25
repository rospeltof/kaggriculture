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

Esta observación motivó los rebaños de loop9 y la conversión temprana de loop10.
Actualización04:29UTC: piloto9 terminó inerte en128/128partidas por variante,
sin confirmación; piloto10 ya corre. No volver a planificarlos como pendientes.

Evidencia: `top3_replay_selection_0236.json`,
`top3_accepted_transactions_0234.json`, `top3_*.ledger.jsonl.gz`, hashes de
replays en cada resumen. Reconstrucción: `auditar_replays_top3.py`; utiliza
el ledger aceptado de `sonda_fallo_forecast.run`. El antiguo `ventas_reales.py`
no se utilizó: su aproximación con precios previos y órdenes emitidas no es
equivalente a transacciones aceptadas por el motor.

## Actualización03:39:41UTC

Top31941,6/30episodios listados; VQ2259,1/56. Ambos COMPLETE. Los recuentos
incluyen validaciones, no equivalen a partidas competitivas ganadas. Los
archivos tienen sufijo0333, pero sus `.fetch.json` registran la hora real.

Cuatro nuevas completadas por endTime, fijadas ANTES de leer rewards:

| Episodio | Rival | Margen propio |
|---|---|---:|
| 113127276 | shikaikaikaikai | +1.659 |
| 113126108 | 62326368 | +923 |
| 113124966 | wqlun06 | +1.279 |
| 113125627 | Clement Lau | +2.891 |

Motor reproduce720 estados×4, caja conciliada, DONE/DONE, sin escapes propios
ni inventario privado final. Contrataciones/tierra coinciden por pareja y
cantidades de producción son muy similares: por ejemplo410lanas/162leches
en ambos lados contra62326368. El precio/timing y pequeñas diferencias de
otras producciones importan en esa muestra. No atribuir causalmente las
victorias a top3 sin contrafactual; tampoco generalizarlas a adversarios de
economía diferente como c0nrad. Evidencia `top3_audit_0339.json` y ledgers;
reconstrucción `auditar_replays_recientes.py` con selección archivada.

## Trabajo y pérdidas intermedias: auditoría posterior de c0nrad

Dos reconstrucciones adicionales de113107623,720estados exactos y caja
conciliada. Hooks del motor separan orden intentada de cambio aceptado.

| Medida | Nosotros | c0nrad |
|---|---:|---:|
| Contrataciones / jornales |307 /10.217|274 /8.273|
| Desplazamientos emitidos |3.186|2.556|
| PASS emitidos |759|280|
| WATER emitidos, todos cultivos |1.096|804|
| Riegos de fresa efectivos |302|113|
| FEED ovino efectivo |334|642|
| CARE ovino efectivo |343|642|
| Cosechas ovinas efectivas |95|174|
| Lana cosechada |395|759|
| Fresa cosechada |249|86|

El rival asigna más trabajo a ovejas y menos a fresas y desplazamientos.
Son totales de una partida; PASS no implica que exista una reasignación viable
desde esa posición/hora, y estos datos no identifican su algoritmo. Añadir
peones con salario Fibonacci no reproduce su eficiencia. Una futura política
de rutas/productos debe medir cuidados y entregas aceptados, además de caja.

La diferencia cosecha→venta revela pérdida intermedia:5fresas y4lanas propias.
Instrumentar `_end_of_day` confirma **33unidades destruidas**, frente a0rival:

| Turno | Pérdida real propia | Total privado antes→después |
|---:|---|---:|
|527|2fresas,3fertilizantes|105→100|
|575|7trigos,3fresas,4lanas,5fertilizantes|119→100|
|623|4fertilizantes|104→100|
|647|3fertilizantes|103→100|
|671|2fertilizantes|102→100|

No valorar esas pérdidas con precio puntual como si fuera ingreso realizable.
Hay guardas de overflow y SHEDROOM ya instaladas. Reaplicar `_ov_apply` al
final no cambia ninguna de las cinco acciones: exige preservar todo el vector
de inventario al amanecer y no puede sustituir insumos sobrantes por cosecha.
En671 el almacén ya queda vacío y la carga sola excede100: una venta del
almacén en ese turno no lo resuelve. La hipótesis loop13 acepta cambiar mezcla
de inputs bajo reservas explícitas; no promete eliminar todos los casos.

**Advertencia metodológica demostrada:** JSON del replay ordena alfabéticamente
productos en bolsas; el motor vivo mantiene inserción histórica. En527,
consultar helpers sobre JSON aislado predice perder2trigos en vez de2fresas y
modifica espuriamente `_ov_apply`. En la reconstrucción viva, las cinco
predicciones de pérdida/vector final coinciden exactamente con el motor.
No se modificó el harness ni se atribuyó a esto la incidencia neutral de pilot7.

Evidencia: `c0nrad_labor_audit.json`, `c0nrad_inventory_audit.json`,
`c0nrad_guard_audit.json`; scripts `auditar_trabajo_c0nrad.py`,
`auditar_overflow_c0nrad.py`, `auditar_guardas_c0nrad.py`.

Snapshot posterior04:30:35UTC:top32022,5/46episodios listados y VQ2288,2/69,
ambas COMPLETE. Incluyen validación. Sin nuevo muestreo de replays en esta
consulta ni inferencia causal entre sus ratings; ficheros sufijo0431 con
metadatos de hora real.

## Consulta05:13UTC y cuatro partidas recientes

Top356537205:2068,8/58episodios listados;VQ56535264:2287,2/81, ambasCOMPLETE.
El sufijo0515es una etiqueta; la consulta real empezó05:13:31UTC. Incluyen
validación. No es un experimento pareado entre submissions ni prueba de que
la ventaja local se traduzca al ladder.

Cuatro episodios fijados por endTime/id antes de leer rewards, todos públicos
y completados; plan `top3_feedback_0515.plan.json`. Reconstrucción exacta de
720estados cada uno y flujo de caja conciliado; originales comprimidos en
`top3_feedback_0515.replays.tgz`. Cero escapes propios y stock terminal0.

| Episodio | Rival | Margen propio |
|---:|---|---:|
|113155577|Aderian Setiawan|+823|
|113154362|ShadowT_T|+240|
|113153102|xsong2020|+1.480|
|113151865|Aleix López|+971|

Cuatro victorias de una ventana temporal corta; no estimador del WR global ni
de fuerza vsVQ. En113151865ambos venden idénticas cantidades de cada producto
y pagan mismos jornales; cobro de fresa20.537vs19.535explica gran parte de la
diferencia, compensada por otros flujos. En otras partidas hay diferencias de
cantidades; no atribuir toda victoria a forecast. Sin nuevos fallos mecánicos
observados en esos cuatro; mantener investigación con rivales/contextos nuevos.


## Cuatro replays del snapshot05:47UTC, descargados06:06UTC

Regla fijada antes de leer recompensas: cuatro episodios públicos completos
más recientes por endTime/id en `top3_episodes_0548.json`. No muestra por W/L.
Cada uno reproduce720estados exactamente y caja conciliada. Cero escapes
propios y productos terminales en almacén/bolsas; originales archivados en
`top3_feedback_0548.replays.tgz`. No estima WR global ni compara causalmenteVQ.

| Episodio | Rival | Margen propio |
|---:|---|---:|
|113164976|today|−1.702|
|113163783|DeeperNet|+35|
|113162622|Yuta Tomimasu|+1.230|
|113162882|sneaky6767|+459|

Contra today, misma composición en los snapshots y mismos costes agregados
de animales/tierra/jornales/semillas. Vendemos2huevos más; otras cantidades
premium iguales. Diferencia principal contable: neto SELLWHEAT−BUY_PRODUCTWHEAT
propio **12.308**, rival **15.501** (brecha−3.193), compensado por+1.491en
los otros flujos. Compramos3.388/vendemos3.685trigos, frente a3.271/3.567.
Más operaciones no significa mayor ganancia. Pero cultivo, alimentación y
trading comparten producto; esto **no separa beneficio causal del arbitraje**
ni demuestra que reducir volumen arregle la derrota. Próxima auditoría debe
reconstruir inventario, órdenes aceptadas, decisiones y precios por turno.
No repetir ADV de ventas ni desactivar forecast por una descomposición contable.

Evidencia `top3_audit_0548.json`, cuatro ledgers y `top3_0548_wheat_gap.json`.
