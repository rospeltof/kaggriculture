# Loop27: registrar nuestras ventas finales antes de inferir las rivales

Registrado antes de construir candidatas o ejecutar su desarrollo.
La auditoría de seis replays elegidos por recencia reproduce719acciones,
720estados y ledger exacto en cada uno. En20.821pares producto/turno elegibles,
la instantánea `_V9_RACE.prev.own` difiere65veces de las ventas aceptadas.
Doce eventos atribuidos al rival ocurrieron sin que éste vendiera al menos dos
unidades; también se omiten ventas reales. Las capas posteriores cambian
órdenes después de guardar esa instantánea. Por ejemplo, en113221090/528
registramos cero lana propia y luego vendemos tres, atribuidas al rival.

Hay otra limitación separada: las ventas al precio mínimo no incrementan
inventario del mercado. La instantánea difiere156veces del incremento propio
efectivo;65no significa que las otras91se arreglen corrigiendo órdenes.
No tocar el tratamiento del mínimo en esta ronda ni atribuir toda la derrota
deNiA a este fallo. VQ frente aNiA deja16lanas en552 y vende en564, dos turnos
después del rival; top3 sólo recupera245de margen contra su cinta grabada.

## Dos políticas, sin cambiar reglas de venta directamente

`sales_sync_vq` y `sales_sync_top3` añaden la misma capa a las dos referencias
reales. Después de obtener la acción definitiva, proyectar unidades propias
con `_r127_fields`, incluidos PLANT atómicos y DROP/PICKUP. Para los productos
premium deV9 que no pueden comprarse, recorrer las primeras10órdenes finales
y calcular cantidadesSELL aceptables con ese stock, sin duplicar inventario.
Actualizar solamente `prev.own` y `prev.left` de `_V9_RACE` para ese turno.
Mantener precios, inventario público, tiendas, umbrales, bibliotecas y horizonte.

Esos datos los consumen el detector de carreras, PREDICT y PREDICT2. Es su
efecto total; no afirmar que cambia sólo una función. No usar ledger futuro,
semilla del mundo ni acciones privadas rivales. La observación siguiente no
revela cuántas ventas al mínimo fueron propias: esto sigue sin resolverse.

## Desarrollo predefinido

1068000/1068001 nuevos y2111590720/2042899352 dirigidos, ambos asientos frente
al V7 reactivo ya congelado del panel25. VQ/top3, noop de cada padre y las dos
candidatas:48partidas. RuntimePYTHONHASHSEED0; fuentes archivadas antes de correr.
Noops exactos de ambos jugadores,720DONE, caja y ledger conciliados, errores,
tiempo<1segundo. Registrar cambios en la instantánea, acciones emitidas,
ventas físicas aceptadas, alimentación/cosecha, tiendas, escapes y productos
terminales. Cantidad propia calculada debe coincidir con SELL realmente
aceptado en cada producto/turno; si falla, detener y reparar con versión nueva.
No exigir producción idéntica: las decisiones de mercado pueden cambiar
alimentación económica y cultivo. No escoger padres ni variantes por rewards
de desarrollo. Verificar que corregir datos cambia acciones en al menos un mundo.

## Evaluación registrada, detrás de26

Piloto1069000–1069015, cuatro rivalesVQ/top3/V7/HS4, mismos archivos delpanel25,
ambos asientos; VQbase/noopVQ/top3control/dos candidatas=960episodios.
Seleccionar hasta dos con deltaW/L/T positivo frente a ambas referencias,
ordenar por menor delta y nombre. No elegir por dinero ni parciales.

Confirmación disjunta1070000–1070031, agregaHarvest68/arshs3 del mismo manifiesto,
1.920/2.560episodios. Gate≥3pp frente aVQ,≥0frente atop3; peor rival≥−20pp frente
a ambas, acciones distintas en≥2semillas frente a su padre correspondiente,
controles, mecanismo y tiempo. Reportar IC por semilla y dos vías, sin tratar
forks como familias independientes. Antes de enviar, revisar sensibilidad a
hashes alternativos y desplazamiento de la submission activa más antigua.
Sin envío automático; si no hay seleccionadas, seguir con otra hipótesis.

No cambia diseños ni fuentes congeladas de19–26. La evidencia original de
atribución está en `feedback_0914.attribution.*`; no repetir el ajuste de
cantidad/historia de patrones ya probado enloops8/11/21.
