# Fronteras después de loops7–9

Estado03:49UTC: la primera idea ya se convirtió en loop10, validado/encolado.
Las demás siguen pendientes. Leer bloques completos; no duplicar corridas.

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
`forecast_library_audit.json` y `recent_sale_streams.json`. Siguiente paso
posible: agregar streams con desempate que preserve prioridad de los existentes,
medir si llegan a seleccionarse, validar noop cuando no hay datos nuevos para
el par, y registrar mundo nuevo/confirmación. No confundir inclusión de nuevos
datos con una mejora de predicción ni de W/L. Aún no existe candidata loop11.

## Incidencia neutral pendiente del harness

Cuatro filas de pilot7 tienen hash TDS alternativo pese a acciones propias,
rewards y W/L/T iguales. Ocho reproducciones con PYTHONHASHSEED0–3 no lo
reprodujeron y preservaron720 estados entre base/infill inerte. No afecta
selección observada; el origen aún no se ha identificado. Si reaparece, capturar
las acciones anteriores al motor y el primer estado divergente; no cambiar el
harness, eliminar rivales ni atribuirlo a hashes/tiempo sin prueba.
