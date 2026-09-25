# Loop21: moderar señales adicionales conservando el patrón principal

Registrado antes de construir o ejecutar variantes. La diferencia de rating
VQ/top3 no es causal. Ocho replays recientes seleccionados por fecha, cuatro
de cada fuente, reproducen719acciones/720estados con el agente enviado. Con
rival grabado, top3 mejora el margen en siete y empeora en uno; no prueba
ventaja W/L/T frente a una política reactiva. No apagar forecast por el rating.

Aquí se conservan siempre las señales del primer patrón y se modifica sólo
la aportación de los patrones segundo/tercero. Distinto de gate/off (filtrar
todo forecast por precisión retrospectiva), top5/7 y bibliotecas nuevas.
No se seleccionan variantes por los rewards de estos ocho replays.

Cuatro brazos sobre top3 sha9668e30a:

- `extra_rank2`: acepta señal del primero o segundo, no sólo del tercero.
- `extra_quorum`: sin apoyo del primero, exige apoyo de ambos restantes.
- `extra_half`: sin apoyo del primero, vende ceil(cantidad/2).
- `extra_short12`: sin apoyo del primero, sólo adelanta volumen propio
  planificado para los próximos12turnos, frente a48de la regla original.

Se conserva la extensión `_hp_quantity`, actualización, librería, ranking,
orden de venta y todas las capas de producción/VQ. Se extrae la última función
`_v92_predict` mediante AST y se cambian sólo selección/cantidad/horizonte de
señales adicionales. El noop usa la misma transformación con regla original.
Calcular cada señal exactamente una vez para preservar contadores heredados.

Desarrollo:1051000nuevo y1326447728/1418183474, las dos primeras semillas del
muestreo real anterior (un diagnóstico adverso y otro favorable a top3 con
rival fijo). Ahora rival arshs3reactivo y ambos asientos. Base/cuatro/noop/VQ
control=42juegos. Noop4.314turnos; hashes/caja/720DONE/errores/tiempo<1s,
activación y volumen emitido; alimento/cosecha/escapes/tiendas documentados.
No elegir brazos por dinero o victorias de desarrollo. Corregir fallos antes
de congelar, sin descartar perjuicios económicos como errores de ejecución.

Piloto1052000–1052015, cuatro rivales históricos arshs3/tds/hybu/ars40 más
las fuentes nuevas V7/HS4 archivadas a05:48UTC, seleccionadas ANTES de conocer
su piloto18. Se añaden por recencia/diversidad del panel, no por favorecer una
variante. Base/noop/cuatro/VQ=7brazos×6rivales+21internos,×32=2.016episodios.
VQ es control ineligible para promoción, no una candidata nueva. W/L/T pareado
primario contra top3 en seis rivales equiponderados, unidad semilla. Seleccionar
hasta dos deltas positivos por magnitud/nombre, sin resultados parciales.
Reportar también diferencias contra VQ sobre las mismas celdas, excluyendo
todos los otros brazos. Noop/hash, errores y cobertura antes de interpretar.

Confirmación1053000–1053015: once rivales de confirmaciones anteriores más
V7/HS4=13, mismos controles. Con una/dos candidatas=1.856/2.400episodios.
Gate≥3ppcontra top3, peor rival≥−20pp y delta≥0contra VQ en el mismo panel;
IC95dos vías, comportamiento/mecanismo/tiempo. Rangos disjuntos. Este gate
adicional protege la referencia real que desplazaría un envío, no se aplica
retroactivamente a bloques previos. No comparar ratings como experimento causal.

Encolar después de20sólo con desarrollo validado. Sin envío automático ni
combinación con reventa, caja o rebaño antes de otra prueba registrada.


## Validación de desarrollo y cola

42 partidas en tres mundos y ambos asientos; noop idéntico en 4.314 turnos,
fuentes verificadas, 720 estados DONE y caja conciliada. Máximo 292,36 ms,
sin errores, escapes ni producto privado al final. Los cuatro brazos cambian
acciones en los tres mundos. Se verificaron apoyo, cantidad y horizonte de
las señales emitidas y las ventas reales frente a las órdenes finales.

En 1051000, rank2/quorum/short12 cambian 101/110/100 turnos por asiento y
sustituyen 18 unidades de trigo cosechado por 15 zanahorias; lana +8/+8/+9.
Half cambia 48 turnos y cosecha tres lanas menos. En 1326447728, los cuatro
cambian 38–47 turnos, con lana +5/+6 y leche −3/−4. En 1418183474 cambian
2/3/12/7 turnos, sin diferencias de comida/cosecha. Tiendas preservadas en
todos. Son efectos del estado y precios posteriores, no una promesa de que
un cambio de ventas conserve todas las decisiones productivas.

No se seleccionaron brazos por estos rewards. Piloto de 2.016 partidas en
1052000–015 en cola tras20; confirmación disjunta1053000–015. VQ control
ineligible, seis rivales piloto/trece confirmación, gate adicional ≥0 frente
al VQ del mismo bloque. Fuentes en `extra_forecast_smoke.sources.tgz`;
validación `extra_forecast_validation.json`. Total83variantes más2prototipos.
