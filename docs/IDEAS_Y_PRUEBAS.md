# Cola de ideas y revisión entre LLMs

Actualización09:28UTC: confirm19_fixedhash0cerrada/noop832, ambasdelta0,
seis trayectorias propias distintas en tres semillas, todas ya ganadas; no
selección.20corriendo y21–26en cola. No repetir.27en desarrollo: sincronizar
_V9_RACE.prev.own/left con las órdenes finales, porque65desajustes en seis
replays contaminaron observaciones rivales. No cambia biblioteca/umbrales ni
resuelve ventas al mínimo. Preregistro27,48desarrollos antes de encolar.

## Cola vigente — 2026-09-25

El loop autónomo, incluidas submissions experimentales justificadas, está
autorizado. Leer `research/ESTADO_INVESTIGACION.md` y la cola actual en
`research/IDEAS_VIVAS_2026-09-25.md`. Las restricciones y propuestas de abajo
son históricas. Confirm10 terminó inerte y biblioteca11sin mejora W/L/T;
piloto12 terminó sin seleccionadas. Confirm13 terminó delta0 pese a
107/86acciones distintas; no enviar. Piloto14sin seleccionadas: dar más alimento
perjudica en este panel.15sin seleccionadas: reserva de caja no garantiza
conversión rentable.16terminócon cuatro REJECTED;18sin seleccionadas. Confirm19corre tras+2,734375ppdel piloto;
Originalconfirm19terminópero quedó inválido por hash rival noop; ahora corre
confirm19_fixedhash0con mismos agentes/semillas/gates.48sondas identifican
sorted(set)sin desempate, runtime0fijado para bloques nuevos.20–25en cola
reiniciada; ver adendaREPARACION_HASH_RUNTIME.23valida suministro del peón ovino adicional, omitido por
la guarda de retiros nativos:48desarrollos/noop8.628/max327ms. ContraV7recupera
24lanas pero conserva derrota; piloto32semillas pendiente. No repetir alimentación indiscriminada14. Loop21modera señales extra
del forecast, con VQcomo control y rivales nuevos. Loop20validó146compras/cierres. Loop17
se detuvo por confundir stock actual con stock nocturno: una cosecha intermedia
libera capacidad y hace valiosa la alimentación omitida. No repetir ese modelo.
Loop18cerró704juegos:V7−21,875ppinconcluso, HS4−30,46875REJECTED.
Loop22compara Harvest V68y selector-off, fuente distinta; Master07:12duplicado.
Pista0742ya es loop24:adelanto sobreVQy top3,36pruebas/noop8.628válidas.
Compras/compromisos verificados; también cambia ventas y una cosecha.
No repetir ni asumir beneficio universal: prueba sintética revela dependencia del rival. No duplicar los bloques congelados ni repetir experimentos ya registrados.

Loop25: prueba separada de cinco fuentes existentes contra VQ/top3 y fuentes
públicas recientes, fijadas antes de resultados pendientes. Motiva similitud
de campo observada en15replays, no supuesto de código idéntico. Mantener intactos
los paneles19–24. Preregistro25 y manifiesto `close_panel_manifest.json`.

Loop26valida semillasWHEATpor cultivo/reposición:40juegos/noop5.752,
76compras aceptadas, conserva campo y producción en cuatro mundos. Ahorro
0–20sin cambiosW/L/T; no adoptar por dinero. En cola tras25,960piloto, padres
VQy top3control; no repetir una guarda terminal genérica porqueE402ya existe.
91variantes competitivas más2prototipos detenidos. Leer informe/preregistro26.

## Ronda vigente — 2026-09-14

El usuario autorizó los experimentos locales de la ronda del líder. Consultar
[protocolo](EXPERIMENTOS_ATREVIDOS_2026-09-14.md) y
[resultados](RESULTADOS_LIDER_2026-09-14.md) antes de proponer otro bloque.
La cola técnica siguiente es histórica; no justifica repetir compras parciales
sin revisar la réplica posterior ni desplaza la nueva investigación de rutas.
Las propuestas siguientes a esta ronda están en el informe de resultados, con
sus costes y reglas de parada. No se autoriza ningún envío a Kaggle.

Para otro LLM: reconstruir primero selección, controles y deltas de la nueva
evidencia con `verificar_lider.py`, y distinguir semillas nuevas de rivales nuevos.
Preguntar si las familias de rutas compartidas y la ponderación 8/8 frente a
40/8 limitan la conclusión. El acuerdo entre modelos no sustituye una réplica.

## Cola histórica del traspaso anterior

Estado anterior: propuestas, no experimentos autorizados. La última corrida de Kaggle
queda reservada. **Un episodio local no consume una submission de Kaggle**;
los costes de CPU local y el cupo de envíos son presupuestos distintos.

## Primera tarea recomendada: revisión de la evidencia existente

Antes de otra hipótesis, pedir a otro LLM que reconstruya el delta y los controles
desde `evidencia/lotes_semillas/`, cuestione la unidad de análisis y revise el
parche. Coste: cero episodios nuevos, cero llamadas Kaggle. Debe entregar sus
objeciones con referencias, no aceptar nuestros resúmenes por confianza.

Que dos LLMs estén de acuerdo no constituye evidencia experimental independiente.
Un revisor ayuda si detecta supuestos, rutas que no ejecutan, muestras compartidas
o criterios movidos después del resultado. La prueba empírica sigue pendiente.

## A. Extender el diagnóstico de cohortes — siguiente prueba barata candidata

1. **Hipótesis:** el lote parcial evita que el trigo ocupe antes las últimas
   tiles disponibles y por eso adelanta cohortes premium en varios escenarios,
   no sólo en la sonda 99000. Apoyo: `decide`, bloque `seed_partial_batch`;
   tile (2,1), trigo d1 h19 en base frente a melón d1 h18 en candidato.
2. **Cómo se falsa:** medir plantados confirmados, primeras cohortes y cash
   comprometido. Si cambia compras pero sólo acumula semillas sin adelantar
   cohortes, falla el mecanismo general propuesto. Si adelanta cohortes y W/L/T
   no mejora, el mecanismo no basta para demostrar fuerza.
3. **Disparo:** contar cuándo el lote completo falla `_afford`, cuándo el parcial
   pasa y qué compra/plantado se ejecuta; mantener noop. No usar sólo dinero.
4. **Coste propuesto:** cuatro cintas elegidas por regla determinista previa
   independiente de resultados, dos semillas, dos asientos, tres brazos
   (base/noop/candidato): **48 episodios**, sólo mecanismo. Este panel pequeño
   no puede aprobar una mejora. El diseño y semillas requieren fijación antes.

El valor de esta prueba es averiguar qué medir y dónde puede fallar la explicación;
no rescatar significancia ni buscar retrospectivamente los rivales favorables.

## B. Réplica de compra parcial — si se decide pagar más evidencia de resultado

1. **Hipótesis:** la ventaja esperada del candidato congelado es positiva en
   escenarios nuevos sobre el mismo panel de 40. Evidencia previa: +5,0 y +4,84
   puntos; confirmación inconclusa con ocho semillas.
2. **Cómo se falsa:** nuevo bloque independiente, métrica primaria por semilla,
   IC95 y controles fijados de antemano. Intervalo que cruza cero → inconcluso;
   intervalo completamente negativo → regresión en ese diseño. No fusionar
   bloques como si el tamaño se hubiera fijado antes ni parar al cruzar un umbral.
3. **Disparo:** reutilizar la sonda conocida, asegurar que config/chasis coinciden
   con el candidato congelado y conservar hashes/estados/acciones.
4. **Coste ilustrativo:** cuatro brazos × 40 cintas × 24 semillas × dos asientos
   = **7.680 episodios**, aproximadamente 50 minutos de pared con el rendimiento
   observado de diez workers. No es un presupuesto aprobado ni una garantía
   de potencia. El revisor debe justificar n con el efecto mínimo que importa,
   la varianza observada y la incertidumbre de estimarla con ocho semillas.

Esta réplica no resuelve rivales adaptativos ni rivales nuevos. Si el objetivo
es transporte al ladder, hay que proponer además un panel reservado por rival
o familia, evitando contaminarlo con decisiones del desarrollo.

## C. Separar la excepción forrajera de la expansión — hipótesis de código

1. **Hipótesis:** mientras `wheat_gap>0`, sobrescribir `adaptive_best` con WHEAT
   propaga el piso forrajero a compras expansivas que tenían otro propósito.
   Apoyo: `bots/chassis.py`, asignación de `adaptive_best`, compras de `idle_plant`
   y fallback ocioso. Se observó una salida inicial de 6+8 semillas de trigo
   con piso 8; eso no demuestra por sí solo sobrecompra, porque pueden caber.
2. **Cómo se falsa:** separar el cultivo elegido por scorer del pedido de forraje,
   conservando su piso y anticipación. Si el camino no cambia o el trigo deja
   de abastecer animales, revisar/rechazar esa implementación. Sólo panel válido
   y confirmación pueden juzgar beneficio competitivo.
3. **Disparo:** traza del `best` original, override forrajero, órdenes de ambos
   bloques, stock y cohortes. El doble pedido consulta el mismo stock anterior,
   pero hay que distinguir cantidad duplicada, necesidad física y preferencia.
4. **Coste:** primero una sonda, sin combinar con compra parcial. Si sobrevive,
   el diseño mínimo análogo de cuatro brazos/40 cintas/cuatro semillas/espejo
   cuesta 1.280 episodios, más confirmación si procede. Aún no implementado.

No equivale a quitar el trigo ni activar `idle_best_only`: esas implementaciones
ya dieron resultados negativos. El fallback ocioso sí puede plantar otras pilas,
por lo que no hay prueba de un bloqueo permanente de semillas ajenas al scorer.

## D. Planificación de nuestra granja — investigación posterior

1. **Hipótesis:** una simulación propia de horizonte corto ordena mejor compras
   o servicios que prioridades fijas. Se apoya en reglas deterministas de cultivo
   y animales, pero debe declarar precios futuros y estado oculto que aproxima.
2. **Cómo se falsa:** primero confrontar predicciones de estado propio contra el
   motor en transiciones conocidas. Errores de crecimiento, consumo o calendario
   invalidan el simulador. Exactitud predictiva no aprueba su política: después
   hacen falta activación, panel y confirmación de la decisión que cambie.
3. **Disparo:** limitar inicialmente a una decisión y registrar el ranking
   calculado frente al elegido; medir p95/p99 de tiempo y memoria reales.
4. **Coste:** prototipo y validación del modelo antes de barridos. No hay presupuesto
   estimado fiable todavía. Prioridad posterior a las pruebas baratas de arriba.

No declarar imposible toda planificación porque el rival tenga datos privados.
Tampoco iniciar MCTS completo suponiendo que podemos reconstruir esos datos.

## Ficha obligatoria de una propuesta

```text
ID / título / estado: propuesta (sin ejecutar)
Pregunta y efecto mínimo de interés:
Base exacta y hashes:
Antecedentes negativos y diferencia de esta implementación:
Hipótesis en una frase:
Función/línea y unidades de cada cantidad:
Variable intermedia y orden que debe ejecutarse:
Qué observación refutaría el mecanismo:
Sonda de disparo, noop y estados comparables:
Brazos, controles y por qué ese control:
Población de rivales; posibles sesgos de selección:
Semillas reservadas / separación de descubrimiento-confirmación:
Métrica primaria, unidad de análisis, IC y regla de parada:
Qué haré si es negativo, inconcluso o positivo:
Número exacto de episodios y coste estimado:
Archivos de salida / manifiestos / verificación del paquete:
Objeción más fuerte del otro LLM y respuesta verificable:
Autorización disponible: análisis / sonda / barrido / envío (separados)
```

## Contrato del LLM revisor

Entregar una decisión **revisar / listo para sonda / listo para propuesta de
barrido**, con motivo. Señalar qué dato falta para cambiarla. No declarar una
mejora confirmada por plausibilidad, autoridad del primer LLM o dinero de un seed.
No cambiar el código del autor durante una corrida congelada. Si propone otra
idea, debe competir por coste e información y no multiplicar automáticamente brazos.
