# Loop19: orden y volumen de compras de trigo para reventa

Registrado antes de construir y evaluar. Replay real113164976 contra today:
derrota1.702, brecha contable neta de trigo−3.193. En varios turnos el rival
compra aproximadamente la mitad y coloca BUY_PRODUCTWHEAT antes de BUY_SEED.
No sabemos su algoritmo ni que esos cambios causen su ventaja. Ambos cultivan
y alimentan con el mismo producto: no confundir flujo neto con arbitraje puro.

Tres intervenciones separadas sobre top3, sin copiar acciones futuras rivales:

- `wheat_front`: mueve la compra de trigo al primer slot.
- `wheat_half`: compra ceil(cantidad/2), conserva su slot.
- `wheat_both`: ambas modificaciones.

Elegibilidad común: pasos288–695, excluido h23; exactamente una compra
BUY_PRODUCTWHEAT de al menos20unidades, resto de órdenes exclusivamente
BUY_SEED (o ninguna otra), y cinta propia nativa prevé SELLWHEAT de al menos
ceil(cantidad/2) el turno siguiente. Se refiere al plan conocido en ese
momento, no a una ejecución garantizada. Conservar cantidades de semillas,
órdenes de unidad y todas las otras capas; no tocar aperturas ni compras de
forraje pequeñas. No se modifica la venta del siguiente turno: puede quedar
limitada por inventario y activar compras de recuperación nativas. Este riesgo
es parte de la política, no una promesa de equivalencia física.

Hipótesis: prioridad reduce el coste al evitar comprar después del rival;
menor volumen limita impacto propio en precio/capital inmovilizado. Ambas son
hipótesis, no ganancias garantizadas: interacción lockstep/consumo/rival puede
invertirlas. No usar la derrota contra today para estimar ventaja poblacional.
Esta prueba es distinta de ADV (adelantar ventas premium) ya rechazado.

Desarrollo fijo: **588616997** (semilla de today, rival ahora arshs3 reactivo),
**1045000** nueva y **1028000** (sensibilidad de alimentación ya observada).
Ambos asientos, base/tres/noop=**30juegos**. Verificar noop exacto, fuentes,
720DONE/caja, tiempos, orden/cantidad emitidos, compras/ventas reales, errores,
alimento consumido, producción y escapes. Los rewards son diagnósticos y no
eligen brazos. Parar si implementación/entrada/noop es incorrecta; un cambio
económico adverso no se borra ni etiqueta como error sólo por perder.

Piloto **1046000–1046031**, cuatro rivales fijos arshs3/tds/hybu/ars40,
5brazos×4+10pares internos,×64=**1.920episodios**. W/L/T pareado primario,
unidad semilla, hasta dos deltas positivos por magnitud y nombre. Noop/hash
y cero errores; no interrumpir por recompensa parcial.

Confirmación **1047000–1047031**, once rivales,**2.304/3.200episodios**,
gate≥3pp/peor rival≥−20pp, IC95, mecanismo y runtime. Muestras disjuntas,
sin cambiar criterio según resultados. Encolar después de18sólo al validar
desarrollo. Ningún envío automático ni combinación con almacén13sin otra prueba.

## Enmienda de cobertura antes del piloto — 06:23UTC

El plan original fijaba16semillas por bloque. Antes de ejecutar ningún episodio
de piloto19, inspección de las cintas/rutas encuentra secuencias grandes de
compra/reventa en tres rutas asociadas a sólo5/64pares de tiendas en la tabla
nativa. Desarrollo: los tres brazos actúan en588616997y son inertes en los
otros dos mundos. Se amplía prospectivamente a32semillas en piloto y32en
confirmación, rangos consecutivos nuevos, sin escoger tiendas/rivales/semillas
favorables ni cambiar gate. No se usa la magnitud de rewards dirigidos para
justificar la ampliación.5/64es cobertura de tabla, no frecuencia poblacional
garantizada. El runner19en espera fue terminado antes de editarlo; estado14
preservado. Agentes y hashes no cambian. El torneo19aún no había empezado.
