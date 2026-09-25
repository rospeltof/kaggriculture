# Loop10: adelantar sustituciones de compras COW por SHEEP

La hipótesis inicial de IDEAS_VIVAS se precisa tras auditar la base: ya existe
`_y_controller`, que convierte vacas/gansos en ovejas con YARN entre días8–11.
Las cintas nativas aún compran vacas en pasos88(d3),150(d6),169/176(d7), con
variaciones por ruta. El hueco nuevo es **d3–7**, sin tocar compras iniciales,
sin agregar terreno, trabajadores ni convertir animales que ya existen.
No repetir loop3: allí se cambiaba el modelo EV/tiendas futuras y las compras
que la ventana8–11 ya permitía. Aquí se reutiliza el controlador físico nativo.

Base top3 sha9668e30a. Seis brazos, inicio3/6 × políticas de(YARN mínimo,
reserva residual):(1,100),(2,100),(1,500). Sólo compras COW de1–2 unidades,
con demanda ya visible y sin animales en almacén/inventarios ni créditos
anteriores sin recoger, para evitar confundir cohortes. Mantiene8–11 intacto.
La reserva usa la estimación nativa de caja tras órdenes; no implica compra
garantizada. La regla por tiendas es una hipótesis, no una proyección de lucro.

Reutiliza confirmación física de compra, reescritura PICKUP/PLACE y ventas
del padre. Auditar compras realmente aceptadas, colocaciones observadas,
lana cosechada por el motor, alimentación/escapes, inventario y créditos al
cierre, coste y errores. La cadencia nativa puede no ser óptima para ovejas;
esa es una limitación a medir, no asumir neutralidad por conservar rutas.

Desarrollo fijado: mundo conocido1004000, arshs3 original reactivo, ambos
asientos; base/seis candidatas/noop con inicio8=16 episodios. Noop exige
acciones completas de ambos jugadores y rewards idénticos. No seleccionar
por rewards en ese mundo. Si faltase cobertura, fijar sondas dirigidas nuevas
antes de congelar; ninguna formará parte del estimador competitivo.

Piloto **1018000–1018015**, cuatro rivales fijados arshs3 original, tds,
hybu, ars40; ambos asientos,8brazos×4+28cruces,×32=**1.920 episodios**.
Semillas1017000–003 reservadas sólo para desarrollo adicional si hace falta.
Primario W/L/T pareado contra top3; unidad semilla, reportar IC semilla/dos
vías, cambios de acciones y runtime. Hasta dos candidatas con delta>0,
ordenadas por delta y después nombre. Cero errores y noop exacto obligatorios.

Confirmación **1019000–1019015**, once rivales fijos de confirm1, ambos
asientos;1.152/1.600 episodios. Gate≥3pp, ningún rival<−20pp. Revisar
mecanismo y tiempo antes de cualquier envío real. Subpanel del piloto sólo
diagnóstico. No cambiar reglas por resultados, dinero o rival favorable.

Después de validar desarrollo, encadenar detrás de loop9. Un solo torneo
grande; fuentes congeladas durante cada bloque. No envíos automáticos.

Desarrollo adicional antes del piloto:1004000 no tenía YARN hasta d9; las
seis variantes son inertes y noop exacto.1017000 tampoco activó las primeras
variantes observadas; completar la sonda. Para validar mecánica activa usar
el seed1272457736 del replay c0nrad ya auditado, escogido porque tiene YARN
temprano, con arshs3 reactivo en ambos asientos. No entra en el piloto ni
se escogerá variante por su W/L. Mismos seis brazos y noop, sin cambiar fuentes.

Desarrollo completo:48juegos; ambos primeros mundos inertes. Mundo YARN:
dos compras efectivas/colocaciones aceptadas por variante/asiento,49lanas
cosechadas; sin escapes/créditos/inventario final. Noop4.314turnos exactos,
max283,385ms y cero errores. `verificar_vacas_tempranas.py` valida archivos,
hashes archivados, compras, colocación, cosecha, inventario y controles.
Manifiesto `early_cow_variants.json` congelado y runner en espera de loop9.
