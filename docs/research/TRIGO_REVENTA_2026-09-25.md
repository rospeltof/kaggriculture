# Del replay de today a tres intervenciones verificadas

El replay113164976 pierde1.702. Nuestra fuente top3 sha9668e30a, ejecutada
contra las acciones archivadas del rival, reproduce **719acciones propias y
720estados exactos**, recompensas84.445/82.743. Es comprobación del origen
del comportamiento; el rival congelado no sirve para evaluar una mejora.

Entre pasos288–695 hay44turnos con una compra grande de trigo por ambos.
El rival pide ceil(mitad) en11, la misma cantidad en32y otra cantidad en1.
En20coloca el trigo primero cuando nosotros lo compramos después de semillas.
Nuestras44cantidades coinciden con la cinta nativa;39prevén vender esa misma
cantidad el turno siguiente. Sólo38cumplen la elegibilidad exacta de loop19.
No conocemos el código rival ni atribuimos su victoria a estos cambios aislados.

## Variantes y mecanismo comprobado

Loop19 separa prioridad, mitad de volumen y ambas. Sólo una compra grande con
otras órdenes de semillas y reventa próxima en nuestra cinta; no modifica
aperturas ni los pedidos pequeños de forraje. No recorta artificialmente la
venta posterior: el inventario y los módulos nativos pueden limitarla y reponer
alimento. Ver el protocolo completo antes de reutilizar estas fuentes.

30juegos de desarrollo, tres semillas y ambos asientos contra arshs3 reactivo.
Noop4.314turnos exactos,720DONE/caja conciliada, max305ms, errores observados0,
escapes0y productos terminales0. Fuentes y30ledgers/30registros de unidades
archivados. Cantidades/slots emitidos y compras/ventas aceptadas verificados.

En588616997, prioridad cambia20turnos; mitad y ambas intervienen en38compras
y cambian79turnos totales. Mismas tiendas y pérdidas nocturnas. La prioridad
mantiene alimentación/cosechas; mitad y ambas añaden2FEEDCOW/2MILK. No afirmar
que esta política preserve producción en cualquier mundo. En1045000/1028000
no hay compras elegibles: los tres brazos son exactamente inertes.

Flujos de trigo en588616997/asiento0, **contra arshs3 reactivo**, no contra today:

| Brazo | Compras aceptadas / coste | Ventas aceptadas / cobro |
|---|---:|---:|
| base | 3.388 / 152.918 | 3.683 / 166.989 |
| prioridad | 3.388 / 151.703 | 3.683 / 166.989 |
| mitad | 2.011 / 88.571 | 2.304 / 103.687 |
| ambas | 2.011 / 88.249 | 2.304 / 103.687 |

Las1.420unidades recortadas de solicitudes no son1.420compras evitadas:
capacidad, órdenes posteriores y reposición cambian las cantidades aceptadas.
Los rewards dirigidos no eligen variantes ni cuentan como confirmación.

## Cobertura antes de iniciar el piloto

Las cintas nativas contienen estas grandes secuencias en rutas103/112/124,
asociadas a5de64pares de tiendas de la tabla. Eso no es frecuencia poblacional
medida ni garantía de elegibilidad final. Explica la inercia de dos mundos y
motiva ampliar **antes del piloto** a32semillas por bloque: piloto1.920,
confirmación2.304/3.200. Mismos inicios, rangos consecutivos, gate intacto.
Ningún resultado de piloto19se conocía al enmendar. El proceso19en espera se
detuvo y sustituyó por el de32semillas sin afectar al piloto14activo.

Código: `capa_trigo_reventa.py`, constructor/sonda/verificador correspondientes
y `continuar_loop_trigo_reventa.py`. Evidencia bajo
`docs/evidencia/loop_publicos_20260925/`: `top3_0548_wheat_orders.json`,
`top3_0548_wheat_policy_trace.json`, `wheat_trade_coverage.json`,
`wheat_trade_smoke.*`, `wheat_trade_validation.json`, `wheat_trade_variants.json`.
Encolado después de18. No hubo envío ni combinación con almacén13.
