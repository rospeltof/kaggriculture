# Reventas nuevas: primero verificar economía y ejecución

## Actualización: piloto completo y confirmación activa

Pilot20 terminó a09:45:49UTC:1.920episodios,448noops exactos, cero errores y
fuentes verificadas. Base91,40625%; los tres tamaños94,53125%, delta+3,125pp.
IC95 por semilla[−0,672;6,922], dos vías[−4,647;10,897]. Cuatro celdas mejores,
cero peores y124iguales tras promediar asientos; señal en tres semillas de32.
No es una mejora confirmada. Desempate registrado selecciona town20/town50;
confirm20 corre con3.200episodios disjuntos, sin modificar políticas ni gates.

Las tres políticas tienen W/L/Tiguales en256/256celdas del panel, pero ninguna
pareja coincide en acciones conjuntas ni rewards. Todas cambian acciones propias
en256/256; cambian las del rival en72/134/148respectivamente. Igual delta no
significa inercia ni tres corroboraciones independientes.

Auditoría mecánica: primera celda positiva ordenada por rival, asiento0, en cada
semilla mejorada; tres mundos×cuatro brazos=12partidas. Hash propio y rewards
exactos frente al piloto, caja oficial reconciliada.150compras y150cierres,
7.722trigos comprados y vendidos al turno siguiente;0errores/escapes, mismas
tiendas y compras/colocaciones animales. Es muestra seleccionada para explicar
mecanismo, no otra estimación de W/L/T.

| Semilla/rival | Margen base | town20 | town50 | town80 |
|---|---:|---:|---:|---:|
| 1049004/tds | −8 | +31 | +79 | +113 |
| 1049010/hybu | −45 | +47 | +166 | +268 |
| 1049013/tds | −33 | +8 | +106 | +105 |

En1049004todo el cambio de caja es trigo: +39/+87/+121 y caja rival igual.
En1049010la ganancia propia total es96/208/310, rival+4/−3/−3; el flujo de las
piernas de reventa suma85/193/295, también cambian ventas nativas. En1049013
town50 gana121propias y resta18al rival; sus piernas suman104. No atribuir todo
el margen a beneficio aislado del ciclo de compra/venta.

Town20/50 conservan alimento y cosechas en estos tres mundos. Town80 en1049013
omite una cosecha de ganso:227→225huevos, aunque su margen sube. La conservación
observada en el desarrollo original no era universal. No adoptar80por caja.
Evidencia: `pilot20.*`, auditoría `auditar_piloto_reventa_town.py` y conciliación
sin nuevas partidas `resumir_mecanismo_town20.py` → `pilot20.physical.summary.json`.

El preregistro29 evalúa dos tamaños sobreVQ/top3 contra el panel cercano. No
reescribe la confirmación20 ni suma ambas como réplicas de una misma población.

La operación comprar antes del consumo del pueblo y vender después gana la
diferencia de curva **sólo en ausencia de transacciones rivales**, con llenado
completo, fondos/espacio suficientes y sin consumo propio intermedio. No es
arbitraje garantizado contra otro agente.

`sonda_reventa_town.py` verifica400escenarios sintéticos: inventarios de
mercado10100/10000/9700/9300, consumo0/1/3/6, cantidades0/10/30/60/90 y cinco
comportamientos rivales prefijados. Cada pierna se ejecuta con el motor oficial;
800/800coinciden en caja con `_v44y_lockstep`. Inventario, stock y consumo se
comprueban también. El caso pasivo coincide con la suma analítica de precios.
No hay acciones físicas, escasez de caja ni saturación de shed en esta sonda;
no extrapolar esa exactitud a partidas completas.

- Inventario9700, consumo3, compra30: rival pasivo→+3monedas; rival vende30
  en la liquidación→−10monedas. Modelo sin rival sigue diciendo+3.
- Inventario10100, consumo1, compra60, rival compra30/revende30: modelo sin
  rival+1, caja propia−18, rival+22 y margen−40frente a no operar.
- Inventario9700, consumo1, compra90, rival vende30antes: caja propia+1pero
  margen frente a no comprar−1. Ni siquiera caja positiva basta.

En78casos se pierde dinero aunque la previsión sin rival sea positiva; en
dos la caja propia gana y el margen relativo pierde. Son conteos de esta
cuadrícula deliberada, no probabilidades poblacionales ni estimación W/L/T.

La primera versión de la sonda leyó atributos escalares de `Struct` después
de mutar sus claves mediante una función interna del motor: quedaron valores
viejos y aparentó caja inmutable. Falló en la segunda combinación. Se archivan
fuente/error `town_roundtrip_probe.v1_*`; la versión corregida lee claves del
diccionario y pasa las800piernas. No fue un error del agente, del mercado ni
de los diagnósticos completos que usan `env.step` y concilian caja al final.

El loop20 crea operaciones nuevas con topes20/50/80, reglas comunes de caja,
capacidad y cierre al siguiente turno. El pronóstico sin rival sólo habilita
una hipótesis; el torneo decide su efecto competitivo. Ver protocolo
`PREREG_LOOP20_REVENTA_TOWN_2026-09-25.md`. La comparación no cambia fuentes,
tamaños ni criterio según los rewards de desarrollo.


## Desarrollo20 completo y en cola

30juegos en1048000/1048001/588616997, ambos asientos frente a arshs3reactivo;
noop4.314turnos exactos, máximo357,83ms, fuentes verificadas,720DONE/caja
conciliada, cero errores/escapes/producto final. Tres brazos activos en tres
mundos:20unidades34operaciones/680unidades;50→56/2.800;80→56/4.382. Total146
compras y146cierres,7.862unidades, todas compradas y vendidas al turno siguiente.
42cierres ya contenían SELLWHEAT reactivo del padre por cantidad menor a la
comprada: se amplió hasta lo comprado mediante máximo, sin sumar ni duplicar
órdenes. Ninguna cantidad desviada a comida.

Alimento, cosecha, pérdidas y tiendas iguales a base en los18juegos candidatos.
En estos mundos la caja de cada operación coincide con el modelo sin rival;
no generalizar esa ausencia de interferencia. Rentas por juego/asiento:
1048000=26/64/105monedas,1048001=24/68/103,588616997=8/24/36. Son diagnóstico
mecánico, no criterio de selección ni efecto competitivo probado. No elegir80
por esos ingresos. Piloto1.920/32semillas1049000–031en cola tras19; confirmación
condicional1050000–031. Total79variantes competitivas más2prototipos17detenidos.
