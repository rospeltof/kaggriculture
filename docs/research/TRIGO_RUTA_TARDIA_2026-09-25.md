# Trigo para recogidas nativas: diagnóstico de una ruta tardía

Origen: desarrollo31, mundo1080001 contra v13. Los ocho brazos pierden cinco
animales propios en695, con el mismo mecanismo; el cambio de cola31no interviene
allí. Una reproducción VQ adicional verifica ambos hashes y rewards78045/76774,
720DONE y caja, y archiva95observaciones finales. No es una muestra competitiva.

En649 quedan siete trigos antes de las unidades; las recogidas de ese turno
consumen seis. SELLWHEAT6 vende el único restante. En650los trabajadores2/3/7
piden5/2/2, pero el almacén está vacío. Emisiones FEED posteriores no consumen
trigo. Cinco animales reciben dos noches consecutivas sin alimento y escapan695.
Hay más de62000monedas: la causa aquí no es falta de caja ni descarte económico
R85 de esas órdenes. El guardia R127 se abstiene si ya hay BUY/SELL de trigo.

## Perturbaciones dirigidas, no candidatas

Se registraron tres modificaciones locales a649: retirar venta, añadir compra9,
y retirar venta+comprar9. Son intervenciones de diagnóstico con turno/semilla
fijos, nunca agentes para enviar. El rival sigue reactivo.

| Intervención válida | Recogidas650 | Escapes propios | Margen |
|---|---|---:|---:|
|Control|0/0/0|5|1271|
|Retirar venta|1/0/0|4|1280|
|Retirar venta y comprar9|5/2/2|0|1391|

La segunda intervención registrada, comprar9sin retirar nada, era **inválida**:
había diez órdenes y habría agregado una undécima. La aserción la bloqueó y el
verificador rechazó la partida con ERROR. Se archivan v1/código/log/fallo; no
usar su resultado. V2 ejecuta sólo la combinación ya registrada y legal de diez
órdenes. No repite el control ni la retirada válida. Total: control adicional,
dos perturbaciones válidas y un intento inválido documentado.

La combinación compra las nueve unidades y añade3FEEDSHEEP,3FEEDCOW y1FEEDGOOSE.
Cosechas: WHEAT407→403, CARROT238→242, MILK223→230, WOOL151→152, EGG89→91;
STRAWBERRY249 y MELON72 iguales. También cambian cultivos: el aumento120de
margen no es ingreso aislado de los animales. Todos los brazos válidos siguen
ganando: ninguna prueba aquí estima mejora global W/L/T.

Próxima hipótesis registrada enloop32: conservar/reponer **el déficit observado**
para recogidas próximas de la ruta nativa, sólo donde la venta actual impide la
guarda existente. En este caso el déficit sería8tras conservar1; no optimizar
la compra9del diagnóstico como parámetro. No confundir con23, que abastece
trabajadores ovinos adicionales, ni24, que adelanta una compra ya existente.

Evidencia:late_escapes_1080001.*, late_route_wheat_probe.* y
late_route_wheat_probe_v2.*. Ninguna fuente desplegable modificada por este diagnóstico.
