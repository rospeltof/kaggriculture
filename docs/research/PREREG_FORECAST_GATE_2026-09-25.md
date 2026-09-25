# Forecast gate: controlar confianza del predictor existente

Registrado antes del piloto. Fecha UTC 2026-09-25 (24-sep en Colombia).

## Evidencia y diferencia con lo ya probado

Arshs3: 2292,5 @148 episodios frente a v13 1857,9 @136. La muestra fijada por
recencia tiene 16 arshs3 y ocho v13; no se eligieron por resultado. Arshs3:
4V/11D/1E, sin escapes y sin inventario propio terminal sin vender. Son episodios
recientes, no una estimación de su WR histórico.

El código exige tres aciertos y precisión histórica ≥70% para señales a 3–4
turnos, pero acepta las señales inmediatas sin ese control. Una sonda en los
primeros cuatro replays reconstruye todas las acciones salvo una en uno de ellos;
67 ventas añadidas por PREDICT, 12 coinciden con venta neta rival inferida a 1–4
turnos. Inferencia de mercado, no ledger causal exacto ni pérdida económica probada.

**Hipótesis:** ese filtro aplicado también a 1–2 turnos evita ventas prematuras
contra oponentes que no siguen la biblioteca histórica. Upside MEDIUM/HIGH,
confianza LOW/MEDIUM. Diferente de ADV, que añadía adelantos generales: aquí se
restringe PREDICT. La ablación compara quitar esta capa, manteniendo las demás.

## Implementaciones y controles

- base y noop: `submission/main_publico_arshs3_vq.py`, sha 9b463dfb.
- gate: `apilar_forecast_gate.py gate`, exige ≥3 aciertos y ≥70% en ventana
  pasada de 240 turnos para el producto antes de aceptar la predicción.
- off: `apilar_forecast_gate.py off`, abla sólo `_v92_predict`; conserva el
  registro de señales y las demás capas de ventas y producción.
- No cambiar producción, rutas, cantidades de insumos ni usar futuro real.

## Piloto

Reutilizar `torneo.py`, ambos asientos. Pool de ocho representantes públicos:
tds, hybu, ars40, hsov, v13, obr, h2965, guru6. Se omite hl59 por duplicación
conductual con tds; no elegir rivales después de resultados. Semillas
**990000–990007**, cuatro brazos, 32 cruces contra pool + seis directos:
**608 episodios**. Una sonda de dos episodios antes valida el wrapper del loader.

Primario: delta gate − base por rival/semilla, asientos promediados. Reportar
IC95 por semilla y dos vías de `pareado_torneo.py`, desglose por rival y asientos.
Los directos y off son diagnósticos. No seleccionar off como nuevo ganador de
esta misma confirmación. Medir acciones emitidas antes del motor; noop idéntico
en acciones, rewards y estados de finalización; errores invalidan el bloque.

Toreno anterior tenía deficiencias concretas: sobrescribía resultados, omitía
hashes de acciones y sólo avisaba de cambios de código. Se endurece ese mismo
harness con manifiesto previo, archivo de fuentes, hashes, cobertura completa,
fallo ante errores y captura de acciones usando el loader oficial de Kaggle.
No se crea otro sistema de evaluación.

## Decisión y parada

- Gate ≥+5 puntos y al menos dos rivales positivos, ninguno <−15: PROMISING;
  confirmar contra los mismos ocho y semillas **991000–991015** (dos brazos,
  ocho rivales + directo: **544 episodios**). Interpretar IC como incertidumbre.
- Gate entre 0 y +5: dejar PROMISING débil; sólo continuar si la sonda de mecanismo
  encuentra corrección clara de un fallo en replays reales. No ampliar por dinero.
- Gate ≤0: no gastar confirmación en esta variante. Si IC cruza cero, decir
  ausencia de mejora observada, no prueba de perjuicio ni nulo exacto.
- Si gate no modifica acciones, parar y revisar activación antes de medir más.
- Confirmación con punto ≥+5, al menos dos rivales positivos y sin regresión
  >15 por rival permite REAL_WORLD_CANDIDATE aunque un IC cruce cero; ambos
  IC positivos fortalecen evidencia, no promueven automáticamente a CHAMPION.

VQ ya fue enviada como **56535264** usando evidencia anterior, antes de este
piloto. Sigue activa arshs3 original 56511619. Si surge otro envío, considerar
que desplaza al más antiguo (arshs3); no reemplazar ambos con cambios casi iguales.
