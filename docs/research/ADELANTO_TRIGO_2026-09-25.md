# Comprar trigo antes: loop24 validado, pendiente de torneo

La pista viene de VQcontraGrimReaper, replay113198597. Nuestro código real
reproduce719acciones/720estados. El rival pide las mismas19compras grandes
un turno antes; no conocemos su algoritmo. Antes de construir se registraron
dos candidatas con la misma regla, una sobreVQy otra sobre top3.

La regla ve una compra nativa próxima≥20con reventa posterior, proyecta
acciones actuales y capacidad, exige caja conservadora más3000y adelanta lo
que cabe. En la siguiente observación mide trigo recibido y lo descuenta de
esa compra en `_route_action`, antes de guardas reactivas. Mantiene las cintas
inmutables y órdenes ajenas al trigo. No anticipa a través de la noche ni
superpone deudas. Una cantidad parcial deja el resto del compromiso pendiente.

Fuentes: `advance_vq` SHAa35c696c y `advance_top3` SHA106aa563.36desarrollos
en1060000/1060001/593858505, ambos asientos contraarshs3reactivo, con controles
de cada padre. Noop8.628turnos exactos, caja/hashes/720DONEválidos, máximo
307,58ms, cero errores observados.64compras adelantadas,4.480unidades llenadas
y canceladas del compromiso nativo. Cuatro casos parciales compran86de89en415;
la orden residual3en416no llena por capacidad. No se duplican esas86unidades.

Ambos brazos son inertes frente a su propio padre en los dos mundos nuevos.
En593858505cada uno adelanta16compras/1120unidades por asiento. Sin escapes,
productos terminales ni diferencias de tiendas. Se conservan pérdidas nocturnas
previas de1060001; no afirmar cero pérdidas globales. Quedan semillas.

El efecto incluye decisiones posteriores. El mismo trigo comprado1492unidades
cuesta62618→61466(ahorro1152), pero las ventas cambian de1679a1682unidades y
70838→70312enVQ. Las guardas de ventas pueden anticipar la salida al tener
stock antes. Alimentación animal no cambia en estos desarrollos. En453,
actor4/(0,9), la cosecha pasa de3CARROT a3WHEAT; único evento de unidades
instrumentadas distinto. Top3tiene el mismo cambio respecto a su padre.
No presentar esta intervención como modificar sólo precio de compra.

Márgenes de desarrollo593858505:VQ281→1508, top3240→1467, ambos asientos;
no cambia W/L/T allí. Estos resultados no seleccionan candidatas.

Sonda aparte contra acciones grabadas deGrimReaper:16adelantos/1120unidades,
base−3070→+313. Cantidades de todas las transacciones se conservan en ambos
jugadores. Nuestra caja sube1638:608de ahorro de trigo y1030de mayores ingresos
de trigo. Rival pierde1745:596más de compra de trigo,1147menos de venta de
trigo y una moneda menos enEGGy otra enFERTILIZER. Es un contrafactual contra
cinta; no demuestra victoria frente a su política reactiva.

## Separación sintética de comprar y vender antes

`sonda_tiempos_compra_venta.py` fija384escenarios de tres turnos295–297,
inventarios10100/10000/9700/9300, demanda0/1/3/6, cantidades48/90, dinero30000,
sin trabajo de campo.1.152piernas de mercado del modelo coinciden exactamente
con motor oficial. Compara compra296/venta297, compra295/venta297 y
compra295/venta296contra cuatro horarios rivales. No son frecuencias poblacionales.

Sólo comprar antes mejora84/128márgenes, empeora12y empata32; pierde dinero
propio32veces. Adelantar ambas mejora96, empeora24y empata8; el peor efecto
relativo es perder el consumo del pueblo cuando el rival es pasivo.
EjemploI9700/demanda3/q48:

| Horario propio | Rival pasivo: margen | Rival compra295/vende297: margen |
|---|---:|---:|
|Compra296, venta297|+6|−64|
|Compra295, venta297|+6|0|
|Compra295, venta296|0|+58|

La secuencia cambia quién captura el movimiento de precio; la mejora no se
deduce de comprar antes sin considerar las ventas y el rival.

Runner24validado y esperando23. Piloto2.560/32semillas1061000–031, VQbase y
top3control, seis rivales congelados. Confirmación disjunta1062000–031,
3.712/4.800partidas,13rivales. Gate≥3ppvsVQ,≥0vstop3, peor rival≥−20;
advance_top3debe además mejorar a su padre, y ambos cambiar acciones en al
menos dos semillas. Revisar mecanismo/runtime antes de un envío.89variantes
competitivas construidas, aparte2prototipos17detenidos. No nueva submission.

Evidencia en `docs/evidencia/loop_publicos_20260925/`: `advance_wheat_*`,
`grim_advance_probe.*`, `wheat_timing_factorial.*`; preregistro24y constructores
incluidos. Catálogo público consultado08:02:50UTC(sufijo0803): ninguna de las
50entradas cambia ref/lastRunTime frente a07:12. No se descargó un duplicado.
