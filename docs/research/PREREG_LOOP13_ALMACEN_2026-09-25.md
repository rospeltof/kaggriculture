# Loop13: vender insumos sobrantes antes de perder cosechas

Registrado antes de evaluar candidatos. La derrota real113107623 contra
c0nrad perdió5fresas,4lanas,7trigos y17fertilizantes en cinco noches. Rival0.
El inventario terminal vacío no detectaba esas33unidades. Reproducción exacta
de720estados y caja conciliada. Las guardas existentes están presentes:
`_ov_apply` preserva toda la composición final; SHEDROOM reserva inputs del
plan nativo. Volver a aplicar `_ov_apply` al final no cambia ninguna de las
cinco acciones con las observaciones vivas correctas.

Auditoría encontró orden alfabético de inventarios en el JSON del replay,
distinto al motor reconstruido. En527 produce una predicción falsa de pérdida
de2trigos en vez de2fresas y una modificación espuria de la guarda. No usar
estados JSON aislados para validar overflow; usar reconstrucción desde el seed.
Esto no explica la incidencia neutral de pilot7: no hay vínculo demostrado.

Hipótesis: vender trigo/fertilizante ya en almacén libera capacidad para
cosechas cargadas, manteniendo una reserva de insumos. **Cambia la composición
al amanecer** y el timing de mercado; no es una equivalencia ni mejora gratis.
Cuatro brazos sobre top3, sólo hora23:

- `night_wheat1`, `night_wheat2`: vende trigo sobrante; reserva1/2días por
  animal vivo más6unidades. Conserva todos los otros productos finales.
- `night_inputs1`, `night_inputs2`: permite además fertilizante; reserva
  aplicaciones FERTILIZE nativas de1/2días más6. Conserva los demás productos.

Se simulan acciones propias y órdenes actuales con helpers nativos, en el
orden de inventario recibido en vivo. No se modifica ninguna acción de unidad
ni compra previa. Sólo agrega hasta dos ventas al final si hay presupuesto
conservador y slots; cantidad≤pérdida y stock real proyectado. Exige disminuir
pérdida total y no reducir otros productos finales. El suelo de cada insumo
es mínimo entre reserva y cantidad original, para no inventar alimento.
La reserva biológica no garantiza cada PICKUP futuro: registrar fallos de
alimentación/escapes y efecto sobre producción. Fertilizante dinámico ajeno a
la cinta podría superar su estimación; por eso existe el brazo sólo trigo.

Desarrollo: semillas1272457736 (mundo de diagnóstico c0nrad, rival arshs3
reactivo),1004000 y1027000, ambos asientos; base/cuatro/noop desactivado =36
partidas. No seleccionar por rewards de desarrollo. Noop completo, tiempos,
errores, pérdidas reales `_end_of_day`, ventas aceptadas y comparación de
predicción contra motor en cada activación. Conservar pérdidas residuales.

Si la mecánica queda validada, piloto **1028000–1028015**, cuatro rivales
fijos arshs3,tds,hybu,ars40, ambos asientos. Seis brazos×4+15pares internos,
×32=**1.248episodios**. Hasta dos deltas W/L/T positivos, desempate alfabético.
Unidad semilla; noop/hash/errores obligatorios, sin selección por caja.

Confirmación **1029000–1029015**, once rivales, **1.152/1.600episodios**.
Gate≥3pp y peor rival≥−20pp, IC95 y mecanismo; sin ajustar criterios tras ver
resultados. No es evidencia de Elo futuro. Encolar después de loop12; no subir
automáticamente. Los mundos de desarrollo nunca son confirmación.

Incidencia de desarrollo: v1 capturó el símbolo global `agent`, que es una
capa heredada anterior a VQ, en lugar del último callable real. Diez filas
registradas y el primer noop falló igualdad completa (11juegos ejecutados).
No usar recompensas/mejoras aparentes de esa versión: familia INVALID_NOOP.
Fuente/plan/filas/log conservados en `night_development_v1_failure.json` y
`night_smoke.sources.tgz`. V2 sólo corrige captura de entrada y usa nombre
único de wrapper; no modifica reservas ni criterios.36juegos de desarrollo
repetidos bajo tag `night_smoke_v2`, sin iniciar piloto hasta validarlos.

V2validada:36juegos, noop4.314turnos exactos,22predicciones de vector final
y pérdida coinciden con motor, ventas aceptadas verificadas, max290,5ms.
Cero errores/escapes/inventario final; animales sin alimentar al cierre de
cada día idénticos a base en todos los cruces. Mismas tiendas. Eso no prueba
que toda necesidad futura de alimento/fertilizante quede cubierta fuera de
estos mundos. En1272457736 vsarshs3: reserva1día baja pérdida27→8,2días27→20;
en1004000,1día24→16 y2días inerte; en1027000 trigo1día y ambos inputs reducen
13→4, trigo2días inerte. Quedan pérdidas residuales. No usar estos deltas de
inventario como W/L competitivo ni seleccionar brazos por dinero.

Los dos brazos de ambos inputs sí venden fertilizante en1027000 (9unidades),
frente a trigo1día que vende9trigos; no son duplicados universales. Fuentes
congeladas en `night_smoke_v2.sources.tgz`, manifiesto/validación correspondientes.
Runner `continuar_loop_almacen.py` encolado detrás de loop12.
