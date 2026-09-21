# Qué muestran los ocho replays de Majkel1337

Análisis del 2026-09-14. [Experimentos y pre-registro](EXPERIMENTOS_ATREVIDOS_2026-09-14.md). [Evidencia](evidencia/lider_20260914/README.md). No se realizó ningún envío a Kaggle.

## Qué está comprobado

Se reprodujeron exactamente las ocho partidas, comparando 720 estados en cada una. Las ventas y compras se midieron al ejecutarse en el motor y los flujos concilian con el dinero final de ambos jugadores. Las cantidades siguientes son operaciones efectivas, no órdenes solicitadas.

| Episodio | Rival | Dinero Majkel / rival | COW / SHEEP / GOOSE d15 | Mayor ingreso efectivo |
|---|---|---:|---:|---:|
| 107673304 | jps | 172,108 / 22,437 | 14 / 4 / 0 | MILK: 98,205 |
| 107674284 | aditya emmadishetty | 166,660 / 42,759 | 5 / 14 / 0 | WOOL: 75,653 |
| 107674293 | yaki-imo | 83,495 / 65,976 | 5 / 9 / 4 | WOOL: 27,264 |
| 107675268 | VYSHAKH G NAIR | 144,211 / 36,028 | 7 / 10 / 0 | WOOL: 54,043 |
| 107685970 | PursueML | 91,028 / 81,433 | 6 / 3 / 4 | STRAWBERRY: 30,034 |
| 107692988 | xiao xiongwei | 75,166 / 61,639 | 6 / 3 / 4 | WHEAT: 26,199 |
| 107696961 | goh | 138,737 / 116,161 | 7 / 15 / 0 | WOOL: 90,156 |
| 107710951 | Ryosei Hara | 149,376 / 130,400 | 11 / 3 / 2 | MILK: 68,513 |

![Economías y rebaños](evidencia/lider_20260914/economias_lider.png)

## Mecanismos que merecen una prueba

1. **Apertura con compromisos coordinados.** Compra dos vacas y tres ovejas en los dos primeros turnos en las ocho partidas. Planta doce melones temprano, compra el segundo cuadrante en step 149 (d6 h5) y amplía el rebaño desde d6. No equivale a subir una perilla de animales en nuestra apertura actual.

2. **Economías diferentes entre partidas.** En d15 tiene 13–22 animales; hay casos con 15 ovejas y otros con 14 vacas. La lana aporta 90.156 monedas contra goh y la leche 98.205 contra jps. Es compatible con adaptación a demanda/rival, pero ocho trazas no identifican su regla ni separan causalmente los efectos de tiendas y rivales.

3. **Comprar forraje y vender trigo no se contradicen automáticamente.** Compra 174–389 unidades de trigo por partida, además de cosechar y vender 290–680. La fecha, ubicación y caja son parte de la política. Un cambio global de BUY_FEED no reproduce esa secuencia.

4. **Rutas compatibles permiten ramificar.** Cuatro cintas comparten sus primeras 86 acciones completas. Dos de ellas comparten 145. Las tiendas aparecen desde d3, de modo que se puede decidir en ese punto usando información ya visible, sin cambiar el prefijo ejecutado ni consultar el futuro. Esto motivó el árbol probado.

5. **El coste del trabajo también cambia.** Sus compras efectivas de peones cuestan entre 4.662 y 5.086 monedas por partida. Las órdenes PASS representan 0,68–0,97% de las acciones emitidas de unidades; movimiento y acciones fallidas no se cuentan como PASS y no son necesariamente trabajo útil.

## Lo que no podemos concluir

- El Elo y rank no vienen en los JSON. El usuario identifica al líder; no se verificó el ranking actual mediante la página, cuyo contenido dinámico no se recuperó.

- Los IDs y sus diferencias no bastan para afirmar evolución durante varios días. Tampoco un marcador alto identifica un rival de Elo bajo.

- Son ocho victorias seleccionadas. No estiman win rate del líder ni representan toda la población. Tres rivales (xiao xiongwei, goh y Ryosei Hara) comparten sus primeras 120 acciones; ocho nombres no significan ocho estrategias independientes.

- Reproducir una cinta con su semilla y rival originales prueba fidelidad de extracción. En escenarios nuevos, la cinta deja de representar las respuestas que elegiría el agente original.

## Errores de las conclusiones anteriores que estos datos obligan a revisar

La réplica de lotes con +0,23 e IC95 aproximadamente [−6,2; +6,7] no prueba un efecto exactamente nulo: no confirma la mejora. Tampoco una diferencia aislada de ratings demuestra que toda diferencia menor de 50 sea informativamente nula. El supuesto techo de la apertura se midió alterando capital de un planner concreto; no acota el valor de cambiar su calendario completo, geometría y logística. Conservamos esas notas como historia, no como motivos para prohibir estas pruebas.

Para decisiones competitivas se usarán los bloques preregistrados y sus controles, no los ingresos de esta tabla. Ver [resultados y diagnósticos completos](RESULTADOS_LIDER_2026-09-14.md).
