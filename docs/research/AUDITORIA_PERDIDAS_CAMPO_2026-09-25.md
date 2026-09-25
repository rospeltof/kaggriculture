# Pérdidas de producción en doce partidas reales de top3

Muestra: los doce replays ya fijados por recencia en tres consultas anteriores;
sin nuevo filtro por resultado. `auditar_perdida_cosecha.py` reproduce720estados
exactos por partida y concilia caja. Hooks alrededor de funciones reales de
decay/refresco/DIG, sin cambiar acciones. Evidencia `field_loss_audit.json`.

Totales propios sobre doce partidas (no estimadores poblacionales):

| Mecanismo | Unidades observadas | Interpretación |
|---|---:|---|
| Deterioro por edad |3CARROT| Una planta en113106269, turnos552/554/556. |
| Muerte por sequía con yield positivo |1CARROT|113155577, turno671; no toda muerte de planta destruye producto.|
| Capacidad de producción ovina |0WOOL|No se observa lana truncada por cap en esta muestra.|
| Capacidad de producción vacuna |33MILK|Banco de cuidado antes de primera producción; inventario previo0.|
| Capacidad de producción de gansos |14EGG|Inventario ya acumulado; vaciar antes podría rescatar hasta14si hubiera ruta/entrega viable.|
| Producto maduro aún en campo al final |4MILK|Una unidad en(6,2)en cuatro partidas.|

Los33MILK no se recuperan cosechando antes: cada tile estaba vacía cuando llegó
la primera producción. Se trata de bonus de cuidado que excede capacidad6,
en vacas colocadas6/7/9/10/11. Las vacas iniciales no explican esos eventos.
La próxima hipótesis es reducir alimento/cuidado sin valor marginal antes de
primera producción, preservando supervivencia y banco útil; no agregar cosechas
indiscriminadas. La base sólo aplica su regla económica FEED entre días10–28.

Los14EGG ocurren en tres partidas; no equivalen a14ventas extras. Hay que
alcanzar la tile, cosechar y entregar, y respetar el trabajo desplazado. La
auditoría PASS anterior no encontró huecos de cosecha contra cap entre sus ocho
partidas. No afirmar que no existe ruta mejor; tampoco fingir que es trabajo gratis.

No convertir estos totales a dinero con una cotización puntual ni confundir
inventario final privado0 con ausencia de pérdidas intermedias/campo pendiente.
La pequeña pérdida visible por deterioro no justifica otro parche general de
cosecha sin identificar primero una oportunidad ejecutable.

## Hipótesis siguiente, aún sin experimento competitivo registrado

`_r88_feed_bonus_cost` cobra un cuidado futuro incluso cuando el banco ya tiene
cinco bonus y todavía no llega la primera producción de la vaca. En ese caso
un bonus adicional no cabe:6unidades máximas=1base+5bonus. Un día sin comer
puede ahorrar trigo si no había hambre previa y se confirma alimentación mañana;
omitir dos noches o la noche de producción sí dañaría el animal/bonus.

Otra corrección posible: en la noche productiva, valorar el bonus realmente
admitido por el cap, `min(cap,held+1+pending)-min(cap,held+1)`, en vez del banco
completo. El CARE de esa noche se banca después y requiere valoración separada.
Son hipótesis distintas de multiplicar precios en loop14. Antes de competir:
noop exacto, seguimiento de producción/pending/FEED aceptado, trigo consumido,
escapes y ventas; mantener rutas. La alimentación prevista por `_r86_next_feed`
es una lectura de la cinta, no garantía de ejecución física mañana. No usar
esta nota para saltarse desarrollo ni cambiar los brazos de loop14 en cola.
