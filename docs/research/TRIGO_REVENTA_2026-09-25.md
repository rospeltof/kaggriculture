# Del replay de today a tres intervenciones verificadas

**Actualización08:44UTC:** confirm19original terminó3.200episodios pero falló
igualdad noop en cuatro hashes rivales. Se conserva inválido; no hay resultado
de confirmación aceptado. Repetición íntegra `confirm19_fixedhash0` en curso
con idénticos agentes, muestra y gates; runtime uniforme verificado por worker.
48sondas aislaron sorted(set)sin desempate, sin efecto económico en esas celdas.
No relajar controles ni contar la repetición como muestra adicional; ver
`REPARACION_HASH_RUNTIME_2026-09-25.md`.

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


## Piloto19completo, confirmación activa desde07:57UTC

1.920episodios/32semillas, noop448/448, cero errores. Base87,109375%; las tres
variantes89,84375%, delta+2,734375pp, ICdos vías[−3,903;9,372]. Cuatro celdas
mejores, ninguna peor; señal sólo en1046006y1046028. Cada variante cambia16/256
acciones propias. Frontno cambia acciones rivales; half/bothcambian8/256.
Comparten W/L/T256/256pero sólo240/256pares de acciones/rewards entre ellas;
no son tres réplicas independientes. Desempate registrado elige both/front.
Confirmación3.200juegos1047000–031contra11rivales en curso; no usar parciales.

Ocho reproducciones, primera celda positiva ordenada en cada semilla, cuatro
brazos: hashes propios/rewards/caja exactos, tiendas preservadas, cero escapes.
Hybu1046006: margenbase−1805; front1189, half1627, both3786. Frontcompra3385
trigos en ambos pero coste148423→146915; ventas3667/158866iguales. Half/both
compran2050y venden2332; producción conservada en este caso.
Tds1046028:base−439, front1416, half2945, both4308. Frontcoste145680→144739
con3382comprados/3578vendidos idénticos y misma producción. Half/bothreducen
compras a2011y ventas a2210; trigo cosechado505→508y zanahoria180→177.
No afirmar que reducir cantidad preserve todas las decisiones de cultivo.

Evidencia `pilot19.*`, incluida auditoría física y contrastes de igualdad.
Esto no autoriza sumar las tres ventajas ni combinar con20/24sin nuevo test.
