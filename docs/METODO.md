# Método vigente — evaluar ideas sin engañarnos

Actualizado el 2026-09-05. Sustituye las reglas operativas anteriores. La versión
con paneles históricos se conserva en [archivo](archivo/METODO_HISTORICO_2026-09-05.md).
El estado y las autorizaciones están en [ESTADO_ACTUAL.md](ESTADO_ACTUAL.md).

## 1. Qué pregunta contesta cada medición

| Nivel | Medición | Qué no demuestra |
|---|---|---|
| Ejecución interna | Contador de la rama prevista | Que cambie la acción |
| Conducta | Primera acción distinta / hash de acciones emitidas | Que el motor acepte la orden |
| Mecanismo | Estado siguiente: compra, plantado, cosecha, venta realizada | Que ganemos más |
| Resultado local | Delta pareado W/L/T contra panel | Rating real ni generalización a todos los rivales |
| Resultado externo | Episodios reales del candidato y control en Kaggle | Causalidad limpia si cambia el emparejamiento o falta muestra |

El dinero final y la caja diaria son diagnósticos. La variable de decisión local
es victoria=1, empate=0,5, derrota=0. No promocionar por un margen de monedas.

## 2. Antes de gastar CPU

Completar la ficha de [IDEAS_Y_PRUEBAS.md](IDEAS_Y_PRUEBAS.md): una hipótesis,
línea o función que sostiene el mecanismo, parche aislado, controles, resultado
falsador, coste y regla de decisión. Buscar antecedentes en BRIEFING/BITACORA.
No repetir una variante descartada sin explicar qué cambia en esta prueba.

Separar aprobación para estudiar una idea, autorización de un barrido y decisión
de enviarla a Kaggle. Hoy no hay autorización para nuevos envíos ni barridos.
El segundo LLM puede revisar y recomendar; su acuerdo no autoriza gastos.

## 3. Verificar disparo y mecanismo

1. Congelar base, configuración y fuentes. La bandera nueva debe estar apagada
   por defecto. Comparar el comportamiento de la base con el chasis previo.
2. Perturbar el valor real: quitar una clave igual a su default es un noop por
   construcción. Identificar qué camino ejecuta (`tasks`, router u otro).
3. Capturar acciones antes de entregarlas al motor, que puede mutar las listas.
   Un contador de rama y una primera divergencia ayudan más que un hash aislado.
4. Comprobar el cambio previsto en el estado siguiente. Una orden BUY/PLANT/SELL
   emitida puede fallar, truncarse o ejecutarse parcialmente.
5. Una o pocas sondas demuestran posibilidad del mecanismo, no frecuencia ni
   fuerza. En episodios posteriores divergentes ya cambian las observaciones:
   para atribuir la primera decisión, usar la misma observación y estado del router.

`muerde.py` registra hashes, dinero y estados por cinta/semilla. Una traza igual
no demuestra que una clave sea universalmente inútil. `sd=0` en W/L/T sólo
significa delta constante; no informa sobre ejecución del parche.

## 4. Panel, espejo y controles

- Panel operativo: las 40 cintas `lad_` existentes, sin elegir por resultado.
  Guardar nombres y hashes. No mezclar `top_` con `lad_` como si fueran la misma
  población. El panel de cinco rivales es histórico, no el panel actual.
- Cada semilla se juega en ambos asientos. Empates cuentan 0,5.
- Base y noop exacto en cada bloque. Deben coincidir por episodio las acciones,
  dinero, estados y W/L/T. Cualquier discrepancia invalida la corrida.
- Control anterior definido antes de medir. En la prueba de lotes fue la
  configuración **exacta CAMPEONA_FB**, no una mezcla parcial con HOZ.
- Error, timeout, episodios faltantes, configuración o fuentes cambiadas:
  investigar el instrumento antes de interpretar deltas. No convertir errores
  o recompensas ausentes en derrotas ordinarias silenciosamente.

Un control anterior claramente peor comprueba sensibilidad a esa regresión.
No certifica potencia para detectar una mejora pequeña, ni transporte al ladder.
No seleccionar celdas porque la base esté entre 30% y 70%: sesga el panel.

## 5. Unidad de análisis e incertidumbre

Sea r el W/L/T por episodio. Para cada cinta t y semilla s:

```text
d[t,s] = media de asientos(r_candidato[t,s] - r_base[t,s])
D[s]   = media de las 40 cintas(d[t,s])
delta  = media de semillas(D[s])
SE     = desviación muestral(D[s]) / sqrt(n_semillas)
IC95   = delta ± t_0.975(n_semillas-1) × SE
```

El t por celda se conserva como comparación histórica, **no como sustituto
posterior** del análisis primario. Compartir semillas crea escenarios comunes;
el análisis principal actual trata cada semilla como un bloque del panel fijo.
Con ocho semillas hay ocho promedios independientes a ese nivel, no 640 ni 2.560.

El intervalo t es una aproximación con pocas semillas y no incorpora selección
del panel, variantes ya probadas, familias de rivales ni adaptación del rival.
Si otra pregunta requiere bootstrap, bloques por rival o inferencia de dos vías,
debe registrarse antes; no elegir después el método que dé el menor p.

Semillas disjuntas comprueban repetición en escenarios nuevos del mismo panel.
Para afirmar generalización a rivales nuevos hay que reservar también rivales
o familias fuera del proceso de selección. Las cintas son pasivas y pueden
favorecer cambios que explotan su calendario fijo de ventas/compras.

## 6. Descubrimiento, confirmación y decisiones

Fijar antes: candidato, panel, semillas, tamaño, controles, métrica primaria,
umbral, regla de parada y qué se hará si el resultado es inconcluso. Si se prueban
varios brazos, registrar multiplicidad y selección; el mejor t de muchos brazos
no merece la misma confianza que una hipótesis única preregistrada.

Para **lotes de semillas** se fijó:

- Descubrimiento: cuatro semillas, delta positivo y controles válidos para
  pasar a confirmación; no exigía significancia del descubrimiento.
- Confirmación: ocho semillas nuevas, IC95 por semilla completamente positivo
  (t>2,3646). El control anterior debía tener IC95 completamente negativo.
- Sólo después correspondía un head-to-head como veto, nunca como promotor.

Son los criterios de ese experimento, no tamaños universales adecuados para
cualquier idea. La confirmación de lotes cruza cero: **inconclusa**. No mezclar
bloques, cambiar a prueba unilateral, cambiar la unidad de análisis ni añadir
semillas hasta conseguir significancia. Una réplica futura es una nueva prueba,
con presupuesto y decisión fijados antes, manteniendo visible este resultado.

| Decisión | Evidencia mínima |
|---|---|
| No dispara en la sonda | Ninguna acción cambia en los estados examinados; revisar camino, no declarar idea falsa |
| Mecanismo no observado | Cambia conducta, pero no la variable intermedia prevista |
| Inconcluso | El intervalo incluye efectos compatibles con cero / falta generalización |
| Regresión local | Evidencia negativa bajo el diseño registrado |
| Mejora local confirmada | Pasa criterio primario y controles en bloque independiente |
| Candidato para ladder | Decisión separada, paquete verificado y nueva instrucción del usuario |

## 7. Integridad y reproducción

`barrido.py` escribe pares compatibles, episodios JSONL incrementales y manifiesto
con configs, seeds, archivos, versiones y hashes. No sobrescribe resultados
anteriores; añade sufijo si hace falta. Comparar configs Python con JSON tras
normalizar tuplas/listas mediante serialización **preservando orden**; el orden
de algunos diccionarios sí puede afectar al agente.

Conservar evidencia accesible fuera de `results/`, que está ignorado por Git.
El paquete [lotes_semillas](evidencia/lotes_semillas/README.md) incluye datos y
fuentes congeladas; `preparar_contexto_llm.py` verifica hashes y reanaliza el
resultado con biblioteca estándar, sin simulaciones ni red.

Los comandos de barridos históricos se documentan en el informe del experimento.
Copiarlos no autoriza ejecutarlos. No hay un comando de envío en esta guía para
evitar confundir documentación operativa con la autorización vigente.

## 8. Qué sustituye de la documentación antigua

- Panel de cinco seleccionado por resolución → panel fijo de 40 con sus límites.
- «sd=0 implica no ejecución» → separar trazas, ejecución y resultados.
- t>2 universal / contar celdas como independientes → diseño y grados de libertad explícitos.
- Elo ≈ delta×2,7 → calibración histórica débil; no usar como predicción precisa.
- Self-play como promotor → sólo diagnóstico o veto definido de antemano.
- «Toda idea plausible ya falló» → fallaron implementaciones y diseños concretos.
