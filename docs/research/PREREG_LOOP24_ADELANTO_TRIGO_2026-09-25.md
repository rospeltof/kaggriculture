# Loop24: comprar antes el trigo ya previsto, sobre VQ y top3

Registrado antes de construir candidatas o simularlas. Feedback0742contra
GrimReaper:19/19compras grandes iguales por cantidad pedida ocurren un turno
antes en el rival. Coste59427/56439para1361/1359unidades aceptadas. Es cronología,
no prueba causal ni recuperación de su algoritmo. Diferente de prioridad/cantidad19,
operaciones nuevas20y de ADVde ventas. No combinar con ellas en esta ronda.

Dos candidatas, misma regla sobre VQy sobre top3. Referencia principalVQ,
controltop3separado. Adelantar parte o toda una compra nativa de WHEAT≥20que
tenga venta nativa≥mitad en el turno posterior. Elegibilidad:288–693, hora≤21,
sin orden actual de WHEAT, sitio para una orden más, sin DROP/PLACEen el
siguiente plan nativo. Proyectar nuestras acciones actuales y órdenes heredadas;
comprar hasta la capacidad libre, preservando fondos conservadores sin ingresos
actuales y3000monedas adicionales. Añadir al final, sin reordenar otras órdenes.

En la próxima observación medir llenado real por diferencia de trigo frente al
stock proyectado antes de compra. Restarlo sólo de la compra nativa concreta
en `_IMPL.chassis._route_action`, antes de guardas reactivas. No borrar una
compra final que pudiera incluir alimento agregado por esas guardas. Mantener
las cintas inmutables y espacios originales del plan; registrar llamadas al hook,
cancelación nativa, orden final y cantidad observada. No repetir el callback
padre para predecirlo. Observación inconsistente/cancelación fallida detiene
promoción. El nuevo stock puede cambiar ventas/alimento posteriores: medirlo,
no presentar adelanto como invariancia de producción garantizada.

Desarrollo36partidas:1060000/1060001/593858505, ambos asientos contra arshs3
reactivo; VQ/noopVQ/top3/noopTop3/advanceVQ/advanceTop3. Noop8.628turnos entre
los dos padres. Verificar hashes,720DONE/caja, runtime<1s, llenado real, deuda
nativa cancelada, no errores, pérdidas/escapes/insumos/stock terminal. Dos juegos
adicionales baseVQ/advanceVQcontra replayGrimReaper validan mecanismo; no se
selecciona por dinero ni signos de estos mundos dirigidos.

Piloto1061000–1061031, seis rivales congelados de22/23:2.560partidas con cinco
brazos (baseVQ/noopVQ/top3control/dos candidatas). Unidad semilla, ambos asientos,
W/L/T pareado vsVQ; top3no elegible. Hasta dos deltas positivos; reportar también
contra top3y efectos de cada una frente a su propio padre. No mirar parciales
para cambiar diseño. Confirmación1062000–1062031contra13rivales,3.712/4.800
partidas para una/dos seleccionadas. Gate≥3ppvsVQ,≥0vstop3, peor rival≥−20,
IC95dos vías, mecanismo/runtime. Encolar tras23sólo si desarrollo válido.
No modificar fuentes activas ni enviar automáticamente.

Precisión de promoción, fijada antes del piloto: `advance_top3` debe superar
también a su propio padre en confirmación (delta>0contra top3); empatarlo no
justifica reenviar una política ya probada en el ladder. Para ambos brazos
exigir acciones propias distintas en al menos dos semillas de confirmación,
además del mecanismo y los gates anteriores. Esta regla no altera semillas,
brazos ni selección del piloto y no utiliza sus resultados todavía inexistentes.
