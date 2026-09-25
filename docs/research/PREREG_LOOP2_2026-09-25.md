# Loop 2: siembras fallidas y régimen de inversión en tomates

Registrado mientras corre loop1, antes de evaluar estas candidatas. Reusar
torneo.py; no cambiar el bloque anterior ni sus fuentes. Dos mecanismos nuevos:

## Evidencia y candidatas

Replay 113061732 contra Pand: a paso 185, maleza en (8,1) obliga a DIG en lugar
de PLANT STRAWBERRY. La reparación original abandona el intento al ver un
movimiento después del riego. El agente continúa regando esa casilla vacía.
El rival vende seis fresas adicionales y gana por 718. La atribución causal
exacta debe comprobarse en bucle cerrado, no sólo con este contraste.

Primer prototipo `recover_ongoing` busca otra visita de riego el mismo día;
detecta la intención pero no actúa en este caso: no hay segunda visita ese día.
Se conserva como diagnóstico, no se gasta un torneo en el prototipo inerte.
Nueva reparación inserta PLANT y desplaza un turno un sufijo que contiene sólo
movimientos, WATER y PASS. Exige que el último turno sea PASS o WATER duplicado:
ese turno redundante absorbe el retraso antes del reset nocturno. No añade hires.
Prueba de mecanismo recupera la fresa, pero cambia RNG/tiendas; su W/L contra
acciones grabadas no es evidencia competitiva.

- **recover_now:** fresas/tomates, recuperar el mismo día. Potencial HIGH,
  confianza MEDIUM en mecanismo, LOW en W/L. Riesgo: interacción entre capas y
  posiciones calculadas por la cinta versus acciones finalmente emitidas.
- **recover_later:** todos los cultivos, máximo dos días de retraso. Potencial
  HIGH, confianza LOW; riesgo adicional: cosecha planeada demasiado temprana.

La inversión de tomates ya existe y emplea un umbral de ingresos previstos de
9.000 monedas. Fuente inspeccionada: arshs3, capa shiiin9, Apache-2.0; el
[Meta Atlas público](https://www.kaggle.com/code/leoprovorov/kaggriculture-public-meta-atlas-v2)
señala incertidumbre del supuesto de reposición perpetua del rival. Su snapshot
es 22 septiembre, aunque la ejecución del notebook sea más reciente.

- **tomato6000:** umbral 6.000, estudiar un régimen de inversión más amplio.
  Potencial VERY HIGH / confianza LOW; riesgo de desplazar trabajo rentable.
- **tomato12000:** umbral 12.000, reservar inversión para demanda grande.
  Potencial HIGH / confianza LOW; riesgo de perder oportunidades rentables.
- **tomato_finite:** 9.000, oferta rival sólo hasta el fin biológico de las
  plantas visibles, más producto ya acumulado; corregir el próximo unlock
  esperado de d22 a d21 usando calendario y número de tiendas observado.
  Potencial HIGH / confianza LOW; riesgo: el rival sí puede replantar.

## Diseño y selección

Base/noop VQ + cinco candidatas, ocho rivales congelados iguales al piloto de
loop1; **998000–998003**, ambos asientos. 56+21 cruces, **616 episodios**.
Primario: delta W/L/T en ocho rivales comunes, por celda rival/semilla promediada
sobre asientos; IC95 por semilla y dos vías. Directos y monedas aparte.
Noop exacto, cero errores, fuentes archivadas, tiempos por turno.

Hasta dos candidatas con delta >0, máximo una por familia, orden por delta y
desempate alfabético. Confirmar con **999000–999015**, once rivales fijados: los
ocho del piloto + tds25 + hl25 + arshs3 original. Dos candidatas: 1.600 episodios;
una: 1.152. Candidata real si delta confirmado ≥3 pp sin rival <−20 pp; no exige
que el IC esté completamente sobre cero. No promover CHAMPION automáticamente.

Si una reparación es neutral en W/L/T pero modifica acciones válidas, se permite
un diagnóstico separado de clones por su mecanismo raro: 32 semillas fijadas
**1000000–1000031**, base/noop/una reparación (elegir recover_now por prudencia)
y arshs3 original, todos contra todos, **384 episodios**. Reportar este bloque
por separado; no presentarlo como confirmación del pool ni seleccionar entre
variantes después de mirarlo. Una señal espejo puede justificar estudio real
si conserva W/L/T en el pool y no tiene fallos mecánicos.

Una ronda negativa genera una hipótesis siguiente; no termina el loop solicitado.
