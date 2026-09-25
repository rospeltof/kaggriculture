# Cota pública del stock rival: mecánica válida, cobertura útil sin demostrar

Hipótesis investigada después de validar29: usar producción visible para
descartar previsiones imposibles de ventas animales. No es el bonus de alimento
del loop17, ni la censura de observaciones28. No se construyó una política30.

El auditor usa exclusivamente granja/posiciones públicas, inventario de mercado,
tiendas y nuestras órdenes finales anteriores. Suma posibles cosechas visibles
y resta sólo una cota inferior de ventas rivales: incremento visible del mercado
menos todas nuestras unidades solicitadas. No identifica ventas al mínimo.
Por la noche permite cosechas ocultas por nueva producción; ignora pérdidas
de inventario para mantener una cota superior conservadora. Si el mercado está
vacío no supone que el pueblo haya podido consumir toda su demanda.

Para los siguientes cuatro turnos añade todo producto visible aún en animales
y sus máximos por animal si se cruza una noche. No supone rutas o inventario
privado. El stock y ledger privado del replay sólo se leen fuera del estimador
para contrastarlo con la verdad. Los productos MILK/WOOL/EGG no pueden comprarse;
animales recién colocados no producen en un horizonte de cuatro turnos.

Plan previo al análisis: los seis controles exactos0914, sin filtro por resultado.
12.942 pares producto/turno cumplen cota≥stock rival real; en8.047 es exacta.
Otras12.942 comprobaciones cumplen cota futura≥ventas aceptadas en los cuatro
turnos siguientes. No hay nuevas simulaciones ni modificación de las fuentes.

De670 cantidades de biblioteca que alcanzarían el umbral4, la cota descartaría31:
25 deEGG, que el predictor nativo NO utiliza, y seis deMILK. El nombre histórico
`native_signals` en el JSON cuenta cantidades crudas de `_hp_quantity` en los
tres productos auditados; no cuenta órdenes emitidas. En las31, nuestra
mercancía disponible tras proyectar las unidades es0 y no hay una orden final
de ese producto. No se ha demostrado que la cota cambie una acción útil.

Decisión: conservar el auditor, no crear ni encolar una candidata con esta
motivación todavía. No es una refutación de todo uso futuro de la señal ni
prueba de inercia universal: sólo se revisaron estos seis replays y los275
turnos de actualización del ranking de cada uno. Antes de gastar un piloto,
hace falta una cobertura mecánica prospectiva que cambie acciones.

La primera versión falló al consultar una claveMILK ausente en el contador
inicial vacío. Fuente, plan y traceback se archivan como v1; fue un fallo de
salida del auditor, no violación de la cota. V2 devuelve ceros explícitos y pasa
todos los checks. `auditar_cota_stock_rival.py` y `revisar_cota_stock_rival.py`
reproducen análisis y contraste de acciones; evidencia `rival_stock_bound_*`.
