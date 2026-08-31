# Kaggriculture — briefing para una segunda opinión

Estoy compitiendo en **Kaggriculture** (Kaggle, simulación de granja, deadline 2026-09-30, ~6.400 equipos, top-10 gana $5.000 c/u). Llevo semanas y estoy **estancado**. Quiero ideas frescas, no confirmación de lo que ya hago. Abajo está todo lo verificado: úsalo, contradíceme si algo no cuadra, y **no me propongas cosas que ya medí como fallidas** (hay lista al final).

## 1. El juego (reglas verificadas contra el motor, no supuestas)

- 2 jugadores, **720 turnos = 30 días de 24 horas**. Gana quien termine con más dinero. Empiezas con $3.000.
- Sandbox del agente: **1,6 vCPU, 100 MiB, 1 segundo por turno**. Sin LLM en runtime: es un planner en Python puro.
- Granja en cuadrantes de 25 tiles. Empiezas con 1; comprar el 2º cuesta $1.000, el 3º $2.000, el 4º $4.000.
- Unidades: 1 granjero + peones contratables. **Salario fibonacci acumulativo**: 8 peones cuestan $54/día, 12 → $376/día, 13 → $609, 14 → $986, 16 → $2.583. Cada unidad hace **1 acción por turno** (moverse cuenta como acción).
- Cultivos (unidades al pico, días que ocupan la tile): WHEAT (4, 5), CARROT (3, 4), MELON (6, 11), TOMATO (4, 13 — *ongoing*), STRAWBERRY (4, 18 — *ongoing*, 4 tandas a edades 10/12/14/16). Hay que **regar cada día** o la planta muere. Fertilizar **duplica** el rendimiento de un tick (ventana de 3 días).
- Animales (coste, estructura, primer producto, intervalo, producto): GOOSE $300/COOP/día 4/cada 1 día/EGG; COW $400/PASTURE/día 8/cada 2/MILK; SHEEP $500/PASTURE/día 6/cada 3/WOOL. Comen wheat a diario o escapan. `CARE` sube la producción.
- **Precios base**: WHEAT 25, CARROT 35, TOMATO 60, STRAWBERRY 120, MELON 250, EGG 50, MILK 160, WOOL 200, FERTILIZER 100.
- **Curvas de precio** (esto es lo más importante del juego y casi nadie lo mira). El precio depende del inventario del mercado, con forma distinta por producto al saturar:
  - **EGG: logarítmica.** +100 unidades → $42; +200 → $41; **+400 → $40**. Es el ÚNICO producto cuyo precio es imposible de estrellar.
  - **WOOL: cuadrática.** Se hunde a la mitad con +42 unidades y al piso de **$1 con +59**.
  - **MILK: lineal.** Piso con +76 unidades.
  - MELON: cuadrática y **ninguna tienda del pueblo lo compra** → nunca se recupera el precio.
  - Consecuencia medida: oveja y vaca **se auto-estrangulan** al escalar; el ganso no.
- **El pueblo drena inventario y sostiene precios.** Se desbloquea 1 tienda cada 3 días (steps 72, 144, 216...). Cada tienda consume 1 unidad de cada producto suyo cada 4 turnos (**6/día**), y **el doble (12/día) si la tienda es de un solo producto**. Tiendas: BAKERY(huevo,trigo), PIZZA(leche,tomate,trigo), BRUNCH(huevo,trigo,fresa), **YARN_STORE(lana)**, ICE_CREAM(fresa,leche,trigo), **PET_CAFE(zanahoria)**, SMOOTHIE(fresa,leche), FARMERS_MARKET(trigo,zanahoria,tomate,fresa).
  - Medido: la demanda de lana de una temporada va de **30 unidades (sin yarn store) a 750 (con tres)**. Un factor de 25x según la partida.
- Máximo **10 órdenes de mercado por turno**. El almacén tope 100 unidades; lleno, las compras **fallan en silencio**.

## 2. Mi bot

Planner en Python (~1.100 líneas) sobre un chasis configurable. Cada turno: planifica rutas al amanecer (serpentina, reparto por coste, atender todo lo pendiente de una tile antes de moverse), asigna tareas por prioridad, y arma órdenes de mercado. Composición **fija**: 8 peones (12 efectivos con 3 cuadrantes), **4 vacas + 4 ovejas, cero gansos, nunca un coop**, ~30 tiles de cultivo objetivo.

Mecanismos validados que ya tiene: scorer de cultivos por $/tile-día con espejo de la curva de precios; lectura de la oferta del rival; orden de venta por daño al precio; anticipación de oleadas de venta rival; tope de melón; protocolo de cierre de temporada.

**Rating actual: 802,8. El top-1 público: 3.040.** En 22 partidas reales del ladder voy **11 victorias - 11 derrotas**, con **$85.052 de media contra $91.234 del rival**. O sea: no pierdo por táctica, **produzco menos**.

## 3. El diagnóstico estructural que tengo abierto (mi mejor hipótesis, sin resolver)

Mezcla de acciones, medida sobre mis 22 partidas contra la de un rival que me ganó $150.822 vs $96.407:

| | yo | Around30 |
|---|---|---|
| regar (WATER) | **51%** de las acciones | 17% |
| animales (FEED+CARE+COLLECT) | 21% | **56%** |
| tiles de cultivo | 62 | **9** |
| estructuras de animales | 8 | **38** |
| peones | 12 | 12 |

**Con la misma mano de obra, él dedica casi todo a animales y yo a regar.** Mi granja tiene demasiado cultivo para las manos que tiene, y el riego se come el presupuesto de acciones.

Pero cuidado: **añadir animales encima de mi granja ya falló tres veces** (ver lista de fallidos). El cuello no parece ser el rebaño sino la **proporción**, y no he logrado cambiarla sin perder.

Otros datos que quizá signifiquen algo:
- Vendo **0 huevos** en 22 partidas, y **18 de mis 22 rivales tampoco**. El pueblo demanda ~157 huevos por temporada que **nadie cobra**.
- Produzco **111 unidades de lana siempre**, sin importar si el pueblo demanda 30 o 750.
- Mi banco llega a **$29.000-52.000 ocioso desde el día 20** sin reinvertir.
- Rendimiento por tile-día medido: **animales $191**, melón $97, fresa $46 (y la fresa es mi mayor asignación con diferencia).

## 4. LO QUE MÁS IMPORTA: mi aparato de medición estaba roto (ya corregido)

Perdí días por esto. Si me propones algo, **pregúntate cómo se mediría**, porque aquí es donde me equivoqué:

1. **El evaluador contaba los empates como derrotas.** El motor es determinista, así que un cambio inocuo produce empates exactos; un brazo de control "no-op" leía 33% en vez de 50%. Con ese medidor probé 19 variantes en un día y **las 19 salieron negativas** — era la firma del medidor, no 19 malas ideas.
2. **Medir contra un clon de mi propio bot no sirve.** Le daba la misma lectura (5%) a un cambio cualquiera y a mi propia generación anterior. En un duelo espejo ambos compiten por el mismo mercado en un equilibrio delicado: cualquier desviación rompe la simetría y el clon la explota. Estaba midiendo **distancia a mi óptimo local**, no calidad.
3. **Un panel de rivales puede fallar por los dos extremos**: contra rivales fáciles mi bot ganaba 97% (sin margen para mostrar mejoras); contra los muy fuertes, 30% (sin resolución para mostrar daños, no distinguía ni una diferencia conocida).
4. **La búsqueda evolutiva no tenía potencia**: 18 episodios por candidato = ±33 puntos de intervalo. El ranking era ruido, los élites se elegían al azar y la búsqueda derivó sola hacia la config de partida — lo cual *parecía* una confirmación del campeón.

**Cómo mido ahora:** empates a 0,5; sigma agrupada por par (los episodios espejados comparten semilla y no son independientes); **brazos de control obligatorios** — un `_noop` que debe leer igual que la base, y un `_peor` (mi generación anterior, peor por evidencia externa del ladder) que además **prueba si el panel discrimina**. El panel oficial es [una cinta élite + mi generación anterior + una vieja]: base 65,2%, `_noop` +0,0σ, `_peor` −2,8σ. Con ±$15-25k de desviación por partida, menos de ~100 episodios por variante invierte conclusiones.

## 5. Ya medido y FALLIDO (no me lo vuelvas a proponer sin un ángulo nuevo)

- **Escalar el rebaño** (6+6, 8+8, o comprar animales durante la partida guiado por la demanda del pueblo): falló **tres veces**, la última muy por debajo del suelo de control. El scorer sí elegía bien (con dos yarn stores prefería ovejas y rechazaba vacas), pero no paga: los peones ya están saturados regando.
- **Plantar en las tiles vacías** que quedan libres: mató **727 plantas por partida** (nadie las riega) contra 24 de la base. Las tiles vacías no son negligencia, son el límite de la capacidad de riego.
- **Repartir trabajo al peón ocioso** (que termina su ruta y se queda quieto ~20 turnos): −1,5σ. Robar tareas rompe la localidad de la ruta: más caminata, menos trabajo. El peón ocioso cuesta $90 por partida — no es el problema.
- **Cambiar la plantilla de peones**: medido de 6 a 16. Cualquier recorte o ampliación pierde; 12 es el óptimo y el salario fibonacci hace el resto obvio.
- **Ir a buscar fertilizante al almacén** para fertilizar más fresas: cuadruplicaba las fertilizaciones (18 → 73) pero no paga sobre el bot actual.
- **Más trigo**: parecía el hallazgo mayor hasta que descubrí que mi analizador contaba las **compras** del rival como ventas suyas. Neto, le gano en trigo.
- **Zonificar el mapa por unidad**, **crecer el melón**, **priorizar por urgencia horaria**, **valorar la fresa fertilizada con un multiplicador fijo** (rechazado 3 veces).

## 6. Lo que SÍ funcionó (para que veas por dónde suele venir lo bueno)

Las dos últimas mejoras reales no fueron ideas nuevas: fueron **incoherencias internas** que encontré mirando repeticiones.

- **El scorer tenía dos caminos con dos economías distintas.** Cuando el tope de melón cortaba ese cultivo, el "segundo mejor" se elegía con otra fórmula (sin considerar el calendario ni el fertilizante) y por eso plantaba **44 zanahorias a $42 con las fresas a $186**. Unificar las dos fórmulas: **+14 puntos de win-rate** y el récord actual del ladder.
- **El scorer no sabía en qué día estaba.** Valoraba igual una fresa plantada el día 5 (que da sus 4 tandas) que una del día 18 (que alcanza una). Ahora el rendimiento esperado se calcula sobre los días que quedan.

## 7. Qué te pido

1. **Ideas estructurales**, no perillas. Ya barrí el espacio de parámetros; lo que falla es la forma de la granja o la forma de decidir.
2. Si tienes una hipótesis, dime **cómo la falsarías** con el aparato de medición descrito, y **qué esperarías ver si es falsa**.
3. Cuestiona mis premisas. Especialmente: ¿es correcto mi diagnóstico de que el riego es el cuello? ¿Hay una lectura mejor de los datos de la sección 3?
4. Puntos ciegos que sospecho pero no he explorado: (a) la **secuencia de apertura** de los días 0-2 (todo lo temprano compone); (b) usar la **identidad de las tiendas** para elegir la economía completa de la partida, no solo el cultivo del día; (c) **vender en el momento** correcto en vez de por reglas de piso de precio; (d) que el verdadero recurso escaso no sea ni el dinero ni las tiles sino **las acciones por turno**, y que haya que optimizar eso explícitamente.

No hace falta que seas amable: si algo de lo que hago está mal planteado desde la raíz, dímelo.
