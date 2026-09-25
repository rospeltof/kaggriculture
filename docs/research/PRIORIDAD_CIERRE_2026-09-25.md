# Prioridad de cierre: desarrollo del loop31

El cambio queda validado y en cola después de30; no hay resultado competitivo
ni nueva submission. Preregistro: PREREG_LOOP31_PRIORIDAD_CIERRE_2026-09-25.md.
Fuentes town50 exactas de29, cantidad50; conserva el lugar de la primera venta
nativa de trigo o agrega el cierre al final si no existía. La compra no cambia.

## Evidencia física

48 partidas, ocho brazos, tres semillas y ambos asientos contra v13 reactivo.
Las dos capas deshabilitadas reproducen ambos jugadores y rewards en8.628turnos.
Cero errores, todas720/DONE, caja conciliada, máximo363,96ms.162compras y cierres,
8.100unidades compradas/vendidas verificadas;28cierres incluyen venta nativa de
trigo. La cola calculada por TR y la acción final se guardan por separado.
Siete casos de contrato comprueban duplicados, compras, orden, cantidad0 y límite10.

Ambas nuevas políticas cambian4de6trayectorias propias, en dos mundos. Frente
a su town50 conservan trabajo aceptado, cosechas, pérdidas nocturnas, tiendas,
escapes e inventarios finales en las seis celdas por política.

| Semilla | Política | Margen town50 | Margen con prioridad | Cambios propios por asiento |
|---|---|---:|---:|---:|
|1080000|VQ|1513|1524|2|
|1080000|top3|2058|2058|1|
|1080001|VQ|1271|1271|0|
|1080001|top3|271|271|0|
|1050019|VQ|−318|51|1|
|1050019|top3|−35|334|2|

Cada fila tiene el mismo resultado en ambos asientos; no son réplicas
independientes. El caso dirigido recupera369 de margen con ambos padres y
convierte sus derrotas en victorias. VQ puro pierde por18; top3 puro gana265.
Los otros dos mundos siguen ganados. No se selecciona por estos resultados.

**Limitación observada:**1080001 ya pierde cinco animales propios en695 y un
ganso rival en647 en todos los ocho brazos. Son escapes preexistentes: no decir
que hubo cero escapes. Una reproducción adicional dirigida investiga su origen,
sin modificar este bloque ni atribuir un beneficio a impedirlos.

## Comparación que decidirá

Piloto1.568, semillas1081000–015, panel25 de cuatro rivales. VQ/noop, top3,
dos town50 antiguas como controles ineligibles y dos candidatas. Hasta dos
positivas frente aVQ/top3 y no negativas frente a su town50 pasan a confirmación.
Confirmación2.560/4.032, semillas1082000–031, seis rivales. Gate≥3ppvsVQ,
≥0vstop3/town50, peor rival≥−20pp frente a las tres, actividad en≥2semillas.

El analizador se verificó con1.920partidas archivadas y448noops en una copia
renombrada explícitamente como fixture: las tres comparaciones usan sólo rivales,
los controles no son elegibles y el contraste antiguo coincide con cálculo directo.
Casos de borde comprueban que mejorar ambas referencias reales pero empeorar
la town50 impide selección. No son1.920nuevas simulaciones.

Candidatas:VQ`d8990488996b915429dfce2ad110c0d19092ba633c3185afa21c4e84764e5a16`,
top3`2d0bcc01d4564cc8b7f4320ebdee2ee7229a63d9e25fbd1a963d4eba814f6b7a`.
Runner`continuar_loop_prioridad_cierre.py`; verificación física
`verificar_prioridad_cierre.py`; analítica`verificar_analisis_prioridad_cierre.py`.
Evidencia`close_queue_*` en docs/evidencia/loop_publicos_20260925.
