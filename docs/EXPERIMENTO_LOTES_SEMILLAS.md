# Compra parcial de semillas — protocolo y evidencia

Fecha: 2026-09-05. Protocolo registrado antes del panel.
Estado final (2026-09-05, tras réplica): **REFUTADO**. Tres bloques: +5,00 (4
semillas), +4,84 (8), **+0,23 (16)**. El bloque de mayor potencia da cero con
integridad impecable. No adoptar; mecanismo cerrado.

**Alcance vigente:** el usuario suspendió cualquier envío a Kaggle y pidió
preparar una revisión por otro LLM. Los comandos de este documento registran
el experimento realizado; no autorizan volver a ejecutarlo. Ver
[estado actual](ESTADO_ACTUAL.md) y [evidencia transportable](evidencia/lotes_semillas/README.md).

## Hipótesis y cambio aislado

Exigir caja para el lote completo retrasa la compra y el plantado de cultivos
largos. `seed_partial_batch=True` reduce el lote adaptativo (máximo seis)
hasta que pase la misma función `_afford`, con la misma reserva de $100.
No cambia el cultivo elegido, el piso forrajero, el stock contabilizado,
las otras compras ni su orden. La bandera está apagada por defecto.

No confundir esta intervención con `order_funding`, `animal_first`, reducción
del piso de trigo o coordinación de los dos pedidos de semillas. No se combinan.

## Sonda de activación y mecanismo (antes del panel)

Comando:

```bash
git show HEAD:bots/chassis.py > /tmp/kaggriculture_chassis_antes_lotes.py
./.venv/bin/python sondas/005_lotes_semillas.py --reference /tmp/kaggriculture_chassis_antes_lotes.py
```

Semilla 99000, asiento 0, cinta `lad_abhi_kumar_agrawal_104715819`.
Archivo: `results/sonda_lotes_99000_s0.json`.

- Base, noop y chasis anterior: mismas 719 decisiones y dinero final.
- Candidato: 599 turnos con acciones distintas; todos los agentes acaban DONE.
- Primera diferencia: d1 h16, caja $472. La base no compra; el candidato compra
  cuatro semillas de melón por $320 y conserva la reserva.
- Primer melón **confirmado en el tablero**: base d6 h16, candidato d1 h18.
- Melones plantados hasta d4: base 0, candidato 5; hasta d6: ambos 8.
- Primera fresa confirmada: base d8 h3, candidato d7 h19.

La misma tile (2,1) explica cómo pocos turnos se convierten en varios días:
la base planta WHEAT en d1 h19 y no planta MELON allí hasta d6 h16. El
candidato planta MELON en d1 h18. Hasta d2 la base ha plantado 17 trigos y
ningún melón; el candidato, 12 trigos y cinco melones. El piso configurado
de trigo es el mismo. Es una observación de esta sonda, no una estimación de
frecuencia del mecanismo en la población.

La sonda comprueba activación y adelanto de cohortes en este escenario. No
estima mejora de win-rate. Ambos brazos ganan este episodio pese a sus acciones
distintas: igualdad de W/L/T no prueba igualdad de conducta.

Alcance de la instrumentación: se cuentan plantas visibles después del turno.
Las compras inferidas por delta de semillas son una cota inferior si un plantado
muere durante el refresh de ese mismo turno. En el JSON inicial ese campo se
llamó `executed_seed_buys`; la sonda lo etiqueta ahora `seed_buys_lower_bound`.
La primera compra descrita arriba ocurre en h16, antes del plantado de h18, y
está respaldada también por la acción emitida. No depende de esa salvedad nocturna.

## Diseño fijado antes de observar el panel

Población: las 40 cintas `lad_`, sin selección por resultados.

| Brazo | Configuración |
|---|---|
| base | CAMPEONA_HOZ |
| noop | copia exacta de CAMPEONA_HOZ |
| _peor | configuración exacta CAMPEONA_FB, generación anterior del linaje |
| partial_batch | CAMPEONA_HOZ + seed_partial_batch=True |

Descubrimiento: semillas 101000–101003, dos asientos, 1.280 episodios.
Confirmación prevista: semillas 102000–102007, dos asientos, 2.560 episodios.
La sonda 99000 no pertenece a ninguno de los dos bloques. No se ajustarán
parámetros ni se escogerán rivales a partir del descubrimiento.

## Integridad y criterio de decisión

1. El noop debe coincidir por episodio en acciones emitidas, dinero, estados
   y W/L/T; delta y sd de W/L/T deben ser cero. Un error o timeout invalida la
   evaluación y se investiga antes de interpretar resultados.
2. `_peor` debe dar una regresión clara. Se considera claro un intervalo 95%
   agrupado por semilla completamente por debajo de cero. Si falla, no se
   atribuye al panel autoridad para aprobar o rechazar una mejora pequeña.
3. Métrica de resultado: diferencia pareada de W/L/T por (cinta, semilla),
   promediando ambos asientos. El t por celda se conserva para comparación
   histórica; el análisis principal promedia primero las 40 cintas de cada
   semilla y estima la incertidumbre entre semillas.
4. Descubrimiento con delta positivo y controles válidos: pasa a confirmación.
   No se exige significancia en cuatro semillas para hacer ese cribado.
   Delta no positivo: no se adopta ni se gasta automáticamente la confirmación.
5. Confirmación: delta positivo e intervalo 95% agrupado por semilla por encima
   de cero (t > 2,3646 con ocho semillas). Si cruza cero, el resultado es
   inconcluso; no se presenta como mejora validada. Las cintas siguen siendo
   rivales pasivos, y nuevas semillas no validan generalización a otros rivales.
6. Sólo un candidato confirmado pasa al duelo contra el campeón como veto.
   No se cambia CAMPEONA_HOZ ni se envía una submission con este experimento.

Detalle del veto, fijado durante la confirmación y antes de leer su resultado:
40 semillas nuevas 103000–103039, dos asientos (80 episodios). Se exige ausencia
de errores y W/L/T medio al menos 50% contra CAMPEONA_HOZ. Su magnitud no se
usa para promocionar ni para convertir el efecto a Elo.

Coste: 1.280 episodios para el primer contraste; 2.560 adicionales sólo si pasa
el descubrimiento. Las mediciones de compras y cohortes son diagnóstico del
mecanismo; el dinero no sustituye la métrica de victorias.

## Resultado

Prueba de integración: `SET=semillas_parciales N_SEEDS=1 WORKERS=2
TAPES=lad_abhi_kumar_agrawal_104715819 ./.venv/bin/python barrido.py 99002`.
Ocho episodios DONE, noop exacto en ambos asientos, candidato y control anterior
con acciones distintas. Esta prueba de una cinta no decide fuerza.

Validaciones adicionales: ocho casos alrededor de los límites de reserva y
tamaño de lote (incluyendo caja igual al coste más reserva), ninguna orden de
cantidad cero y respeto de caja ya comprometida con `order_funding=True`.
El verificador noop acepta trazas idénticas y rechaza una traza distinta aunque
el dinero y W/L/T coincidan. Compilación y `git diff --check` correctos.

Comando del descubrimiento:

```bash
SET=semillas_parciales N_SEEDS=4 WORKERS=10 ./.venv/bin/python -u barrido.py 101000
```

Descubrimiento terminado: 1.280 episodios válidos; noop exacto en sus 320
comparaciones por episodio. Fuentes y cintas mantienen sus hashes.

| Brazo | W/L/T medio | Delta (puntos) | t por celda | t por semilla |
|---|---:|---:|---:|---:|
| base | 62,1875% | 0 | — | — |
| noop | 62,1875% | 0 | — | — |
| _peor | 36,2500% | −25,9375 | −5,94 | −15,07 |
| partial_batch | 67,1875% | +5,0000 | +1,41 | +1,68 |

El candidato cambia la traza en 320/320 episodios. La señal positiva no alcanza
significancia en descubrimiento; satisface el cribado predefinido y pasa a
confirmación sin ajustar el código ni seleccionar rivales.

IC95 del delta agrupado por semilla: candidato [−4,47; +14,47] puntos;
control anterior [−31,41; −20,46] puntos.

Evidencia: `results/barrido_101000.json`, `results/barrido_101000.meta.json`,
`results/barrido_101000.episodes.jsonl`, `results/lotes_descubrimiento_101000.txt`.
Las fuentes utilizadas se conservaron en `results/lotes_fuentes_20260905.tar.gz`;
sus hashes y los de las 40 cintas están en los manifiestos de las corridas.

Comando de confirmación (semillas 102000–102007):

```bash
SET=semillas_parciales N_SEEDS=8 WORKERS=10 ./.venv/bin/python -u barrido.py 102000
```

Confirmación terminada: 2.560 episodios válidos, noop exacto en 640/640
comparaciones, cero errores. Configs, fuentes y cintas idénticas al descubrimiento;
semillas disjuntas verificadas.

| Brazo | W/L/T medio | Delta (puntos) | t por celda | t por semilla |
|---|---:|---:|---:|---:|
| base | 60,0000% | 0 | — | — |
| noop | 60,0000% | 0 | — | — |
| _peor | 36,7188% | −23,2813 | −8,45 | −6,74 |
| partial_batch | 64,8438% | +4,8438 | +2,45 | +2,08 |

**IC95 agrupado por semilla del candidato: [−0,67; +10,36] puntos.**
Control anterior: [−31,45; −15,11], claramente inferior. El candidato modifica
las acciones en 640/640 episodios: mejora W/L/T en 62, empeora en 31 y conserva
el resultado en 547. No hay empates en ninguno de los brazos.

| Semilla de confirmación | Delta (puntos) |
|---|---:|
| 102000 | +13,75 |
| 102001 | +2,50 |
| 102002 | +2,50 |
| 102003 | 0,00 |
| 102004 | −2,50 |
| 102005 | +3,75 |
| 102006 | +16,25 |
| 102007 | +2,50 |

**Decisión según protocolo: inconcluso, no adoptar.** Se repite el signo y una
magnitud próxima al descubrimiento, pero el intervalo primario cruza cero y
t=2,08 no supera 2,3646. El t por celda de 2,45 no sustituye ahora el criterio
fijado. Tampoco se juntan ambos bloques para rescatar la confirmación.

No se ejecuta el veto head-to-head porque sólo correspondía después de una
confirmación positiva. `seed_partial_batch` queda experimental y apagado;
CAMPEONA_HOZ y la submission conservan su configuración. La hipótesis no queda
refutada: una réplica independiente con más semillas podría reducir incertidumbre,
pero no forma parte de esta corrida ni se añade mirando resultados intermedios.

Coste realizado: 3.840 episodios de panel; 8,19 minutos de pared en
descubrimiento y 16,82 en confirmación con diez workers. La sonda y la prueba
de integración son adicionales. Ambos bloques tienen controles válidos.

Evidencia de confirmación: `results/barrido_102000.json`,
`results/barrido_102000.meta.json`, `results/barrido_102000.episodes.jsonl`,
`results/lotes_confirmacion_102000.txt`. Resumen con intervalos y transiciones:
`results/lotes_veredicto_20260905.json`.


## Bloque 3 — réplica independiente (2026-09-05)

Pre-registrado en [PREREGISTRO_REPLICA_LOTES.md](PREREGISTRO_REPLICA_LOTES.md)
antes de ejecutar. Semillas **103000–103015** (16), disjuntas de los bloques 1 y
2 y de la sonda. 40 cintas × 2 asientos × 4 brazos = **5.120 episodios**.

Motivo: el reanálisis mostró que el veredicto del bloque 2 dependía de la unidad
de agrupamiento (celda +2,45 / semilla +2,08 / cinta +2,83 / dos vías +2,52).
El diseño es **cruzado** (40 cintas × 8 semillas, ambas dimensiones aleatorias),
así que el estimador correcto es el de dos vías `V_cinta + V_semilla − V_celda`.
**Conflicto declarado en el pre-registro:** ese estimador se calculó DESPUÉS de
ver el bloque 2 y cambiaba el veredicto. Mitigación: exigir que **ambos**
criterios excluyan cero.

### Integridad

- `noop` **exacto** en los 1.280 episodios.
- `_peor` (CAMPEONA_FB exacta): **−26,95**, t=−12,43 por semilla y −7,77 a dos
  vías. El panel **tiene resolución**.
- `partial_batch` cambia acciones en **1.280/1.280** episodios: la bandera
  dispara. Resultado nulo real, **no** test nulo.

### Resultado

| criterio | t | IC95 | veredicto |
|---|---|---|---|
| por semilla (n=16) | +0,08 | [−6,20; +6,67] | incluye cero |
| dos vías (df=15) | +0,08 | [−6,01; +6,48] | incluye cero |

**Ambos incluyen cero → NO adoptar.** Por el pre-registro no se encadena un
cuarto bloque ni se fusionan los tres.

### Lección de método

El veredicto conservador del bloque 2 ("inconcluso, no adoptar") era el correcto.
El reanálisis a dos vías es estadísticamente más apropiado para este diseño, pero
se usó para **cruzar la línea con un resultado fronterizo después de verlo**.
Ante un efecto en el borde, la respuesta no es un estimador mejor: son más datos.

**Corolario abierto:** `harvest_76` está en la misma situación (+2,50, t=+1,76 a
dos vías, IC95 [−0,85; +5,85]) y nunca tuvo réplica con potencia. Está dentro de
`CAMPEONA_HOZ`, la base activa.
