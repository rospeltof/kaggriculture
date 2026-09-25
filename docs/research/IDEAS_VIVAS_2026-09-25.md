# Fronteras después de loops7–9

Estado04:39UTC: piloto9 completo, seis variantes inertes128/128; conversión
temprana loop10 corriendo. Biblioteca reciente loop11 y aperturas loop12
validadas/encoladas. Loop13 almacén también validado y en cola. No duplicar corridas.

## Reasignar compras futuras de vacas con demanda de lana ya visible

El caso c0nrad auditado dejó sólo4.294 de venta de134 leches propias, frente a
69.502 por391 lanas. Agregar peones tarde es caro: los rebaños del loop9 pagan
jornales Fibonacci, y su proyección corregida rechaza el mundo de desarrollo.
Una alternativa distinta es aprovechar pasturas, trabajadores y recorridos ya
presupuestados para futuras vacas, comprando ovejas cuando las tiendas visibles
y caja lo justifiquen. No convertir animales existentes ni quitar alimento.

Loop3 modificó la decisión **GOOSE→otro animal** de HD2 y extrapoló tiendas
futuras; esto no propone repetirlo. Antes de implementar, localizar compras
nativas COW posteriores a conocer tiendas y separar las que genera HD2. Evitar
mezclar cohortes COW/SHEEP: confirmar compra, reescribir PICKUP/PLACE de los
actores correspondientes, confirmar colocación y vender lana realmente recogida.
Verificar si HARVEST/CARE/retornos del padre son agnósticos al animal. Mantener
reserva para100 extra por cabeza y obligaciones del padre. No asumir que todas
las rutas tienen compras tardías elegibles ni que el reemplazo conserva trabajo.

Prueba dirigida sólo para mecánica, noop exacto y diagnóstico de cobertura;
luego registrar semillas/rivales nuevos antes de competir. Comparar efecto
total W/L/T, oferta comprometida propia/rival y coste de oportunidad. Ningún
delta local anterior garantiza esta combinación ni su Elo.

**Implementada como loop10:** auditoría encontró que `_y_controller` YA
convierte compras entre8–11. La novedad se limita3–7, sin modelo EV ni tiendas
futuras. Seis políticas,48juegos dirigidos válidos; primera activación observada
en173/178, dos animales colocados y49lanas cosechadas. Piloto1018000–015,
confirmación1019000–015 registrados. Runner espera loop9. No reinventar otro
controlador ni repetir desarrollo; consultar `PREREG_LOOP10_VACAS_2026-09-25.md`.

## Revisar oferta comprometida del tomate adicional

En pilot7/ars40/1010001/infill4_d18, el padre ya comprometió su campaña V219
pero varias plantas aún no existen al cotizar. La función de v4 sólo enumera
plantas visibles; puede omitir parte de esas80 unidades futuras. La cotización
de9.756 para4 plantas no es ingreso incremental observado. El total de tomate
vendido pasa80→96 y su ingreso30.024→34.386; también cambian tiendas y otros
ingresos. Conservar confirm7 íntegra, después considerar una nueva versión
con oferta comprometida si la evidencia justifica dedicarle otro bloque.

Confirm7 terminó inerte352/352por variante, sin selección. Corregir oferta
solamente estrecharía el gate: no gastar otro piloto idéntico por esa corrección.

## Actualizar biblioteca de ventas rivales sin volver a cintas pasivas

Top3 confirmó ventaja local al admitir más patrones. Ahora hay cuatro replays
recientes de top3 y cuatro de DSM con transacciones aceptadas exactas. Se puede
estudiar cobertura temporal de la biblioteca existente y agregar streams
actuales agrupados por primeras tiendas, deduplicados y sin filtrar W/L.
No usar replays de entrenamiento como confirmación ni interpretar predicción
offline como fuerza competitiva. La comparación competitiva exige rivales
reactivos y mundos nuevos, además de revisar coste de cómputo. El gate de
confianza/off ya perdió mucho en la ronda anterior: no repetir esa poda.

Auditoría hecha:2.398streams,64/64pares de tiendas,24–63por par. No se conoce
fecha original porque los ids están sustituidos por−1. Doce fuentes fijadas
por recencia (DSM4 y rivales top3 ocho) son nuevas con fingerprint que preserva
umbrales nativos de cantidades; no agregan pares de tiendas. Artefactos
`forecast_library_audit.json` y `recent_sale_streams.json`. **Implementada en
loop11:** tres fuentesets preservan desempate original, noop exacto y20juegos
validados. Ladder/all sí seleccionan streams nuevos. Piloto/confirmación con
32semillas por bloque, fuentes congeladas. No repetir desarrollo ni confundir
inclusión de nuevos datos con mejora de precisión o W/L. Ver protocolo loop11.

## Señal residual y diagnóstico pendientes, sin nueva corrida registrada

History360 terminó confirm8 en+2,8409pp, IC dos vías[−1,249;6,931], debajo
del gate3. No fue enviada ni refutada; no redondear, reutilizar seeds o cambiar
el gate. Si la biblioteca confirma ventaja, una interacción historia×biblioteca
necesita diseño nuevo, no sumar deltas de bloques distintos.

La referencia MarketShock nueva motivó loop12 de aperturas controladas.
TomatoInsteadOfCow sólo entrega4tomates en desarrollo: evaluar piloto antes
de suponer que una planta temprana compensa toda la leche sacrificada. La
telemetría de trigo de base/cycle espera53, pero el motor cosecha en87; futuros
diagnósticos deben usar acciones aceptadas y cronología real. No hay aún una
variante de mantenimiento/replantado ni evidencia de que convenga.

## Capacidad nocturna y reasignación productiva

c0nrad113107623: motor confirma33unidades destruidas en nuestras descargas,
rival0. No es stock terminal ni inferencia por órdenes. Guardas existentes no
rescatan estas cinco noches manteniendo la misma mezcla de productos. Loop13
implementa venta de insumos excedentes para liberar capacidad, bajo reservas
1/2días. V2completó36juegos, noop4.314,22activaciones exactas contra motor;
cero escapes/diferencias en alimentación nocturna, máximo291ms. V1inválida por
omitir VQ queda archivada y no se usa. No añadir otra guarda equivalente sin leer
`PREREG_LOOP13_ALMACEN_2026-09-25.md`. En671 sólo hay carga>100 y almacén0:
ese caso necesita logística previa; la variante no promete resolverlo.

La auditoría de trabajo encuentra759PASS/3.186movimientos propios frente a
280/2.556del rival, y302vs113riegos efectivos de fresa. c0nrad duplica cuidados
ovinos con menos jornales. Próxima frontera estructural: reemplazar cultivos o
rutas futuras por cuidado ovino con las mismas horas, previa auditoría de
factibilidad por posición/hora. No tratar PASS agregado como peón disponible.
El piloto9 inerte no refuta todas las inversiones: no activó cambios en este
panel. Sus razones de rechazo por caso no se guardaron en el torneo; no
atribuir todo a un gate específico sin sonda. Repetirlo sin política nueva
no enseña más.

La predicción de overflow requiere observaciones del motor reconstruido:
el JSON ordena bolsas alfabéticamente y produjo pérdida/acción falsa en527.
Cinco comparaciones de observación viva coinciden con el motor. Mantener esta
distinción al diseñar diagnósticos futuros; no se demostró vínculo con pilot7.

## Incidencia neutral pendiente del harness

Cuatro filas de pilot7 tienen hash TDS alternativo pese a acciones propias,
rewards y W/L/T iguales. Ocho reproducciones con PYTHONHASHSEED0–3 no lo
reprodujeron y preservaron720 estados entre base/infill inerte. No afecta
selección observada; el origen aún no se ha identificado. Si reaparece, capturar
las acciones anteriores al motor y el primer estado divergente; no cambiar el
harness, eliminar rivales ni atribuirlo a hashes/tiempo sin prueba.
