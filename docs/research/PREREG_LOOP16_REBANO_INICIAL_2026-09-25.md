# Loop16: composición del ganado inicial, antes de conocer tiendas

La base compra dos vacas y dos ovejas en1. Los cuatro animales tienen rutas,
pasturas y trabajadores ya presupuestados. Probar una composición distinta
afecta producción desde el primer ciclo, sin contratar un rebaño adicional.
Es una decisión bajo incertidumbre de tiendas; no se sintetiza demanda futura
ni se usa seed/identidad rival para elegirla. No repetir el gate tardío loop9
ni las fechas3–7de loop10/15.

Cuatro variantes sobre top3, únicamente en compra inicial1:

- `initial_sheep1`: sustituir una COW por SHEEP, total1COW/3SHEEP.
- `initial_sheep2`: sustituir dos, total0COW/4SHEEP.
- `initial_cow1`: sustituir una SHEEP por COW, total3COW/1SHEEP.
- `initial_cow2`: sustituir dos, total4COW/0SHEEP.

Mantener costes reales (±100/200), sin inyectar dinero. Usar `_y_cash` con
margen100 para el turno actual; no prometer financiación de los días futuros.
Dividir orden para cantidades parciales, respetar máximo10órdenes. Registrar
crédito sólo tras compra aceptada y reutilizar PICKUP/PLACE/ventas del controlador
nativo. No reescribir rutas ni sustituir ganado existente. Las decisiones nativas
posteriores pueden reaccionar a la nueva composición: medir el efecto total.

Auditoría previa: ambos PICKUP COW son unitarios en2; los dos PICKUP SHEEP son
unitarios en3/6. Si una ruta cambia esa estructura, no suponer que crédito1
puede satisfacer PICKUP2. Desarrollo verificará cantidades físicas y posiciones,
en vez de deducir colocación de una orden emitida.

Desarrollo fijo **1036000**, **1004000**, **1272457736**, **1018001**, ambos
asientos vsarshs3 reactivo; base/cuatro/noop=**48partidas**. Último mundo es
conocido por tensión de alimento en otro rival, no una réplica de aquel fallo.
Comprobar noop, compras/colocaciones, ganado al cierre de día0, crédito pendiente,
alimentación aceptada, producción/ventas, escapes, errores/tiempo y caja. No
elegir composición según rewards de esos mundos. Archivar fallos de implementación.

Piloto **1037000–1037031**, cuatro rivales fijos arshs3,tds,hybu,ars40,
ambos asientos:6brazos×4+15internos,×64=**2.496episodios**. Unidad semilla,
W/L/T vsbase pareado primario, hasta dos positivos por delta y luego nombre.
Registrar cobertura y equivalencia de acciones. Noop exacto, cero errores.

Confirmación **1038000–1038031**, once rivales,**2.304/3.200episodios**.
Gate≥3pp y peor rival≥−20pp, IC95 y mecanismos favorables/adversos, runtime.
No cambiar muestra ni umbrales por el piloto. Encolar tras loop15 al validar
desarrollo; sin envío automático. Mayor n porque el cambio afecta a todos los
mundos y renuncia a la diversificación inicial, con riesgo de grandes regresiones.

Desarrollo validado:48juegos, noop5.752turnos exactos, máximo328,55ms,
cero errores. Costes±100/200, cuatro animales colocados en las mismas tiles,
crédito pendiente0al día1. Todas las variantes cambian acciones en4mundos.
Sheep1/2cambian primeras tiendas en los4mundos por cambios posteriores de
campo/RNG; no aislar el efecto en precio de lana. Sheep2pierde una vaca215
en1272457736.1036000incluye cinco escapes695en base y seis671/695en cow1;
son datos del episodio, no se descartan ni se cambian los brazos. Stock privado
final0en todos. Se conserva el diseño sin selección por esos rewards.
