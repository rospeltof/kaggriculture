# Apertura de mercado: tamaño del ciclo con stock final fijo

La fuente actual usa BUYWHEAT8 ySELLWHEAT3 en0, conservando cinco trigos.
Sus comentarios históricos justifican tamaños10/20frente a otra población;
no son una garantía vigente. La ronda12 cambió apertura productiva/cultivos,
no esta cantidad. No se modifica la parcela, la vaca ni el resto de órdenes.

Plan previo: todos los13replays de los cortes0914/1003, cantidades5/8/12/20/43,
ambos asientos.130escenarios oficiales de un turno; NO130partidas completas.
El control8 reproduce exactamente los13estados grabados en su asiento real.
Las alternativas conservan stock privado y semillas de ambos jugadores. El
rival usa su orden inicial grabada, no una política completa. La apertura es
simultánea, así que no puede reaccionar a nuestra orden de ese mismo turno.

| Cantidad comprada / revendida | Cambio medio de margen | Peor margen | Peor caja propia | Celdas mejores / peores |
|---|---:|---:|---:|---:|
| 5 /0 | −5,231 | −8 | −4 | 0 /20 |
| 8 /3 | 0 | 0 | 0 | 0 /0 |
| 12 /7 | +1,231 | −6 | −3 | 16 /8 |
| 20 /15 | −8,308 | −14 | −7 | 0 /24 |
| 43 /38 | −50,154 | −68 | −33 | 0 /24 |

Cada fila tiene26celdas; las faltantes son iguales. Los dos asientos dan el
mismo resultado aquí y varias aperturas rivales son idénticas: no hay26
observaciones independientes ni una estimación poblacional. Q12gana4de margen
frente aBUY20/SELL15, pierde2contra8/3y6contra10/5, empata contraBUY5. Ocho de
los13rivales de la muestra usan20/15; eso pesa en el promedio y no garantiza
su frecuencia futura. Los nombres distintos no representan mercados distintos.

Q43 deja hasta33monedas menos al final de0, antes de una secuencia nativa de
compras con poco margen. Mantener stock5 no conserva solvencia. No se atribuye
un efecto de cosecha todavía: estas simulaciones terminan después de0.

Se registra loop30 únicamente paraQ12 sobreVQ/top3. No se declara campeón por
+1,231monedas iniciales. Desarrollo48juegos frente aVQ/V7, piloto cercano960,
confirmación disjunta condicionada; ver preregistro30. Las cantidades5/20/43
quedan documentadas como hallazgos económicos de esta muestra, sin torneo.
Auditor reproducible: `auditar_apertura_mercado.py`, `opening_market_audit.*`.

## Desarrollo30 validado y en cola

48partidas completas,2mundos×2rivales×2asientos×6brazos. Noops exactos en
11.504turnos de ambos jugadores,32aperturas verificadas entre candidatas y
noops, caja reconciliada,0errores, máximo313,77ms. Las dos candidatas cambian
exactamente la acción0en sus8/8celdas;BUY12ySELL7llenan, stock5en1, sin otra
compra/venta de trigo en1. Se conserva alimento/cosechas/pérdidas/tiendas;
cero escapes o productos propios terminales en48juegos. No garantía universal.

Contra mirrorVQ, ambas pierden2de margen y llegan a mínimo de caja7. En VQ
eso convierte cuatro empates (dos mundos, ambos asientos) en derrotas−2.
Top3 conserva sus resultados anteriores. Contra V7 ambas ganan4de margen,
caja mínima14; siguen perdiendo las cuatro partidas de cada candidata.
La microventaja depende del rival: no seleccionar por promedio de caja ni
ocultar los empates perdidos. No se cambiaron brazos/panel/gates por este dato.

`verificar_apertura12.py` registra PASSED; fuentes y ledgers en
`opening12_smoke.*`. Runner30verificó fuentes y espera tras29 para el piloto960.
Total101variantes construidas y dos prototipos17detenidos. La nueva idea31
sobre orden del cierre está preregistrada; aún no tiene candidata ni proceso.
