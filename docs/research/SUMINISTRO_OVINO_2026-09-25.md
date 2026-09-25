# Trigo compartido entre trabajadores: una causa de lana perdida

El replay113174624contra daviondk pertenece a los cuatro episodios top3más
recientes del snapshot06:52UTC, seleccionados antes de leer rewards. Se audita
su derrota después de esa selección; no es una muestra poblacional nueva.
Seed1578791335, asiento0, fuente enviada9668e30a. Margen real−2.904.

`auditar_lana_davion.py` reproduce719acciones y720estados exactamente,
concilia dinero y balance de lana producida/vendida/perdida. Tenemos las mismas
17ovejas y6vacas finales que el rival, pero producción389vs414, ventas385vs410,
almacén nocturno pierde4cada uno. Cero cap animal, overflow de cosecha o lana
residual en campo/inventario. El déficit no es una cosecha sin vender.

En602, el actor9retira5trigos del almacén antes que el trabajador12adicional.
Quedan1de los6que pide éste. La función compacta `_v233_worker` exige tener
trigo para todo el grupo antes de empezar; de603a623emite PICKUPWHEAT0,
21turnos seguidos. Seis ovejas en(5..7,5..6) quedan sin alimentar/cuidar y
producen1cada una en623, frente a4del rival. No se emitió FEEDfallido: medir
sólo rechazos del motor o PASS no detectaba este atasco. Había más de80.000
monedas, pero la guarda de insumos sólo proyectaba próximas retiradas nativas,
sin contar el trabajador agregado. La compra6en601cubre menos que5+6necesarios.

Balance propio:335FEEDy336CAREovinos aceptados; rival341/343. Los tres skips
económicos R85de650/652/653 son posteriores, bonus0y no causan la omisión623.
La pérdida inmediata de alimento cuantificada es18unidades; no incluye el
cuidado que habría generado banco posterior ni es una estimación de dinero.

Sonda dirigida preregistrada (`davion_supply_probe`), compra601de6→11,
resto de nuestra política reactiva y rival grabado: retiro12completo, seisFEED
yCARErestaurados, yield4cada una; ventas propias409vs385. Lana propia ingresa
85.457vs85.254, rival84.951vs89.095, volumen rival410sin cambios. Caja propia
107.373→107.395, rival110.277→106.140, margen−2.904→+1.255. Tiendas iguales.
La ventaja condicional depende del mercado compartido, no de dinero propio
proporcional a producción. No equivale a ganar contra la política rival reactiva.

Loop23preregistra dos reglas generales, buy y hold, al contratar al peón
compacto: necesidad nativa anterior+seisovejas, respetando fondos/capacidad y
compras existentes. Sin seed, idrival ni paso601. La reproducción adicional
`davion_general_supply_probe` confirma que buy encuentra ese déficit por estado
y obtiene los mismos resultados de la sonda dirigida, con predicción de stock
exacta y cero errores. Desarrollo inicial24juegos contra arshs3: ambos inertes,
con10consultas por asiento en mundo davion y0en los otros dos. Se registró
una adenda antes de nuevas partidas:24juegos contraVQ/V7/HS4, mismo mundo
y ambos asientos. V7sí reproduce el atasco; en ambos brazos/asientos se compra11,
peón retira6, alimento335→341y lana cosechada389→413. Margen−5090→−1093;
seguimos perdiendo. Caja propia−168, rival−4165. VQ/HS4son inertes.

Las48pruebas pasan noop8.628turnos, caja/hashes/runtime(max327ms), cuatro
predicciones de stock y retiradas reales exactas. Cero escapes/productos
terminales; tiendas iguales. Buy/hold coinciden en estas12celdas, la rama de
retener una venta aún no se activa: no son réplicas independientes. Validación
archivada, runner23encolado tras22:2.560partidas piloto y confirmación disjunta
condicional. No seleccionar por rewards de desarrollo. Dos brazos añaden87variantes competitivas
construidas en total, aparte de2prototipos17detenidos.

Evidencia: `davion_wool_audit.*`, `davion_supply_probe.*`,
`davion_general_supply_probe.*` y futuros `sheep_supply_smoke.*`, todos bajo
`docs/evidencia/loop_publicos_20260925/`. Fuente real archivada con pilot16y
replay original en `paired_feedback_0653.replays.tgz`. Esta hipótesis es distinta
del alimento indiscriminado14y de la falta de dinero de conversiones10/15.
