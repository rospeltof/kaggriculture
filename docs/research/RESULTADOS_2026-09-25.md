# Revisión y experimentos — 25 septiembre UTC / 24 septiembre Colombia

**Decisión:** mantener arshs3 original (56511619) y medir en ladder la nueva
arshs3+VQ (56535264). VQ está COMPLETE. Ninguna de las cuatro candidatas medidas
en esta ronda justifica otro envío. El próximo trabajo debe aprender de derrotas
actuales y aislar un mecanismo nuevo, conservando la predicción de ventas.

## Punto de partida y envío

Se revisaron los cambios hasta a9f59ee, el estado de investigación, las creencias,
el historial de submissions, la bitácora y los protocolos VQ/ADV. La bitácora
principal terminaba en septiembre 14, mientras la investigación reciente estaba
en `docs/research/`. Se actualizaron las entradas para evitar seguir planes vencidos.

La primera consulta de esta ronda encontró arshs3 en **2292,5 / 148 episodios**
y v13 en **1857,9 / 136**. Es evidencia favorable al orden local arshs3 > v13,
sin calibrar una conversión de victorias locales a Elo ni demostrar superioridad
contra la cima del ladder.

Se envió el archivo ya guardado y validado
`submission/main_publico_arshs3_vq.py`, commit **a9f59ee**, SHA-256
`9b463dfb8076b4c63946e1ae4249cd1cfc3cc58b63115cf2bd5b00f96f188976`.
Submission **56535264**, 2026-09-25 **00:22:43 UTC**, COMPLETE.
La CLI informó cuatro envíos restantes. Desplazó a v13 y conservó arshs3 como
referencia activa. `submission/main.py` sigue siendo el original.

La evidencia previa de VQ se verificó sin repetir sus partidas: 0/120 celdas
cambian W/L/T en el pool, pero 40-0 en una confirmación espejo y bloques
adicionales favorables. ADV ya había fallado su confirmación; tampoco se repitió.

Última consulta al cerrar la ronda: original **2288,6**, VQ **1198,5**; edades
muy distintas y número de episodios sin actualizar en esa consulta. El rating
inicial de VQ fue 810. No usar estas lecturas tempranas para decidir su fuerza.
No se programó monitoreo automático.

## Experimentos nuevos

Cada bloque contiene 608 episodios: base/noop/dos candidatas, ocho rivales
congelados, ocho semillas y ambos asientos. La tabla usa únicamente el panel
común de ocho rivales, 128 episodios por brazo; los duelos entre brazos se
informan aparte. Puntuación W/L/T = 1/0/0,5. Delta en puntos porcentuales.

| Bloque / candidata | Base VQ | Candidata | Delta | IC95 dos vías | Decisión |
|---|---:|---:|---:|---:|---|
| Forecast / gate | 76,56% | 25,00% | −51,56 | [−78,92; −24,20] | REJECTED |
| Forecast / off | 76,56% | 7,81% | −68,75 | [−89,57; −47,93] | REJECTED |
| Públicos / tds25 | 92,19% | 84,38% | −7,81 | [−27,29; +11,67] | Inconcluso, no seleccionado |
| Públicos / hl25 | 92,19% | 82,81% | −9,38 | [−29,79; +11,04] | Inconcluso, no seleccionado |

Las semillas difieren entre bloques: 990000–990007 y 992000–992007.
La diferencia entre los porcentajes de la base muestra sensibilidad a la semilla;
no comparar porcentajes entre bloques como si fueran efectos de una intervención.
Los intervalos por semilla, desglose por rival y celdas están en los JSON de resultados.

**Forecast:** gate exige un historial mínimo de aciertos también a predicciones
inmediatas; off desactiva `_v92_predict`. Ambas variantes empeoran claramente
en este panel. No se ejecutó el bloque de confirmación ni se enviaron.

**Públicos actualizados:** se descargaron versiones distintas de
[tds](https://www.kaggle.com/code/tetsutani/demand-preserving-turn-sale-timing)
(SHA 127ed3e6) y
[Harvest Ledger](https://www.kaggle.com/code/haodou092/kaggriculture-harvest-ledger)
(SHA 1dfd4630), publicadas el 24 de septiembre. tds cambia sustancialmente su
paquete de política y colas; HL cambia el cálculo de precios futuros para
producción y parámetros de siembra. Se conservaron atribuciones Apache-2.0.
Ninguna supera el umbral registrado de +5 puntos, dos rivales positivos y
ninguno por debajo de −20. No se gastaron los 864 episodios de confirmación.
Los intervalos amplios no demuestran una regresión universal de estas versiones.

En directo tds25 gana 10/16 a VQ, pero pierde globalmente frente al pool;
hl25 gana 6/16. Seleccionar por el directo después de ver el agregado negativo
cambiaría el criterio registrado. No se hizo.

## Qué aprendimos del agente fuerte y de nuestros errores

Se descargaron 24 replays elegidos por recencia: 16 arshs3 y ocho v13.
Arshs3 obtiene 4 victorias, 11 derrotas y un empate en esa ventana, sin escapes
de animales propios y sin stock final propio sin vender. Esta ventana reciente
no estima su WR histórico ni contiene el Elo de los rivales.

**Corrección de medición:** la primera sonda del predictor contó 12/67 señales
con flujo rival inferido en t+1..t+4. Omitía las ventas simultáneas del turno t.
Se reprodujeron cuatro replays con las acciones reales, verificando los **720
estados** de cada uno y conciliando los flujos de caja de ambos jugadores.
El ledger de ventas aceptadas da **50/67 coincidencias en t..t+4**, de las cuales
**42/67 ocurren en t**. La cifra anterior se conserva como evidencia del error,
no como precisión válida. Una coincidencia no prueba por sí sola el beneficio
causal de una venta anticipada. La reconstrucción de la política difirió en una
acción de un replay (SELL WHEAT, paso 623); el ledger usó las acciones grabadas
y sí reprodujo exactamente los estados.

**Mecanismo local:** primera celda ordenada donde base gana y gate pierde:
ars40, semilla 990000, asiento 0. Primera divergencia en paso 440: VQ vende dos
lanas y gate espera; el rival también vende dos lanas ese mismo turno. Se
reproducen los resultados originales: margen **+89 → −78**. Las cantidades
totales vendidas por producto son idénticas; cambia el dinero cobrado por timing,
principalmente después en fresas. No atribuir toda la diferencia a esas primeras
dos lanas: las decisiones posteriores también divergen.

Esto respalda conservar el predictor y estudiar precios ejecutados y ventas
simultáneas. La observación de acciones, el flujo neto de inventario y el dinero
efectivamente recibido responden preguntas diferentes.

## Evidencia, validación y coste

Se reutilizó y reforzó `torneo.py`: captura hashes de acciones antes del motor,
archiva fuentes, rechaza sobrescritura, errores, cobertura incompleta y cambios
de fuentes durante el bloque. El wrapper se comparó con el loader oficial:
1.438 acciones y rewards idénticos en dos episodios. `pareado_torneo.py` ahora
rechaza episodios inválidos, duplicados y celdas incompletas.

Ambos torneos completos: **160 controles noop exactos por bloque**, cobertura
y hashes archivados verificados, cero errores, máximo observado menor de 272 ms
por turno. Coste nuevo: **1.216 episodios de torneo + 8 diagnósticos = 1.224**.
Los diagnósticos son dos del loader, dos del fallo gate y cuatro reproducciones
reales; no se mezclan con las muestras de evaluación.

- [Evidencia y comandos de verificación](../evidencia/research_20260925/README.md).
- [Resultados forecast](../evidencia/research_20260925/forecast_results.json).
- [Resultados públicos nuevos](../evidencia/research_20260925/public_refresh_results.json).
- [Protocolo forecast](PREREG_FORECAST_GATE_2026-09-25.md).
- [Protocolo públicos nuevos](PREREG_PUBLIC_REFRESH_2026-09-25.md).

Los torneos son contra ocho políticas públicas emparentadas, no una muestra
aleatoria del ladder. No evalúan directamente los mejores rivales privados.
Las fuentes exactas están en `.sources.tgz`; los replays originales siguen en
`replays/`, ignorado por Git, con selección, diagnósticos y ledgers conservados.

## Próxima decisión útil

1. Leer partidas de VQ cuando tenga una muestra útil, junto con la referencia
   original y la fuerza observable de sus rivales. Otro envío desplazaría al
   original: debe aportar una hipótesis diferente o evidencia favorable nueva.
2. Investigar pérdidas actuales descomponiendo unidades producidas y precios
   ejecutados por fase. La predicción simultánea ya mostró valor; no volver a
   gate/off con los mismos parámetros ni a ajustes agotados del chasis HOZ.
3. Si aparecen pérdidas por elección de cultivo, aislar sobre VQ una decisión
   de producción basada en oferta futura visible. La versión HL completa no
   mejoró, lo cual no aísla ese mecanismo. Antes de ejecutarla, registrar la
   intervención, los riesgos de alimento/producción y semillas nuevas; todavía
   no es una candidata implementada ni aprobada por evidencia.
