# Loop32: proteger trigo de recogidas nativas cuando ya existe una venta

Registro previo a construir candidatos o medir su desarrollo. La auditoría
TRIGO_RUTA_TARDIA encuentra recogidas5/2/2que fallan después de una venta. Dos
perturbaciones válidas distinguen conservar de reponer; una tercera fue inválida
por once órdenes y queda excluida. Esto no demuestra mejora competitiva.

## Dos políticas

`route_wheat_vq` y `route_wheat_top3` sobre las fuentes reales exactas, sin
reventa town, cambio31, ni arreglos27/28. Entre pasos648y694, excluyendo el
último turno de día, sólo si ya existe SELLWHEAT y no BUY_PRODUCTWHEAT en las
órdenes finales. Estimar las recogidas de trigo de la ruta nativa del próximo
turno usando las posiciones tras las unidades actuales; contar sólo actores
existentes con acceso al almacén. No inventar trabajo ni incluir cosechas futuras.

Si la venta deja menos que esas recogidas: reducir ventas de trigo para
conservar la demanda, manteniendo orden relativo de las otras órdenes. Si el
stock tras las unidades ya es insuficiente, retirar esas ventas y agregar una
compra por el déficit, antes de las demás órdenes. No añadir unidades por un
parámetro ajustado. Máximo diez órdenes; abstenerse ante falta de capacidad,
configuración no estándar o dudas de proyección. Comprobar capacidad al punto
de compra y financiación conservadora de compras ya presentes, además de una
reserva5000. No cambiar órdenes de campo, compras posteriores o señales.

Registrar demanda, proyección, stock retenido, cantidades emitidas, llenados y
recogidas reales siguientes. El motor, no la proyección, decide la ejecución.
La reparación puede alterar producción/tiendas/precios; medirlo.

## Desarrollo antes de encolar

VQ/top3, dos capas deshabilitadas exactas y dos candidatas, semillas1083000,
1083001y1080001, ambos asientos contra v13 congelado de20:36partidas. Noops de
ambos jugadores/rewards,720DONE,0errores, caja conciliada, max<1s, actividad de
cada política en≥1mundo y cadena de compra/recogida/alimento verificable.
Escapes, cosechas, pérdidas, tiendas y producción terminal explícitos. No
seleccionar por dinero o victorias de desarrollo. Si una rama no se activa,
registrar falta de cobertura antes de decidir cualquier ampliación.

## Piloto y confirmación

Tras31, único torneo principal. Piloto1084000–1084015, panel25 de cuatro
rivales, VQ/noop/top3/dos candidatas:960partidas. Seleccionar hasta dos con
mejora estricta frente aVQy top3, ordenar por mínimo de ambos deltas y nombre.
Confirmación1085000–1085031, seis rivales,1.920/2.560partidas para1/2candidatas.
Gate≥3ppvsVQ,≥0vstop3, peor rival≥−20ppfrente a ambas, cambios propios en
≥2semillas frente al padre correspondiente. Unidad rival/semilla promediando
asientos, ICpor semilla/dos vías. Runtimehash0y controles/sourcearchives.

No tocar fuentes31ni bloques activos, no sumar estos datos a23/24. Antes de
cualquier envío: revisión física, hashes alternativos, cuota y submission
que se desplazaría. Sin autoenvío. Un resultado negativo continúa la investigación.
