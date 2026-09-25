# Loop 5: invertir antes en una campaña completa de tomates

Motivación: cuatro replays recientes de DSM muestran cuarta tierra al día 10
y producción abundante de tomate. Nuestro piloto de umbrales al día 18 apenas
cambió comportamiento. Probar una fecha productiva distinta, sin copiar las
acciones grabadas como si fueran una política reactiva.

Constructor `construir_tomate_temprano.py`, padre VQ 9b463dfb. Conserva diez
tiles de V219, observación de trabajadores realmente contratados y chequeos
de caja/índices. Cambia campaña completa: siembra, riegos alternos, fertilizante,
calendario de cuadrillas y cuatro amaneceres productivos. Cesa contratación
después de última cosecha; respeta fechas absolutas del resto de la granja.
Modelo de oferta rival finita, futuras tiendas cada tres días, liquidez inicial
6.000 (más chequeo real de presupuesto y reserva 3.000 del request).

| Variante | Siembra | Ingreso mínimo proyectado |
|---|---:|---:|
| early12_9k | 12 | 9.000 |
| early12_6k | 12 | 6.000 |
| early14_6k | 14 | 6.000 |
| early16_6k | 16 | 6.000 |
| late18_6k | 18 | 6.000 |

late18_6k es comparador de calendario: difiere de tomato6000 de loop2 por
liquidez y modelo finito, por eso no es una repetición exacta. El primario sigue
siendo delta W/L/T contra VQ; comparaciones entre brazos son exploratorias.

**Aclaración de desarrollo anterior al piloto:** seed1004000 reveló que otra
capa reactiva de VQ abre SE para seis ovejas al día 12. No figura en futuras
cintas. Early12 puede sustituir esa inversión; las fechas tardías ya encuentran
SE ocupado y no se activan. El experimento mide efecto total de asignación de
tierra/capital más calendario, no una fecha aislada. No ocultar este coste de
oportunidad ni declarar mejor inversión por el ingreso bruto de tomates.

Antes del piloto: ocho episodios de desarrollo, seed **1004000**, ambos
asientos contra arshs3 original, base/noop de transformación de calendario/
early12_6k/late18_6k. Noop conserva fechas, proyección y liquidez originales;
debe emitir exactamente las mismas acciones. Comprobar ramas/plantas/cosechas,
errores y conciliación de caja. Si la intervención no se activa en ese mundo,
diagnosticar elegibilidad; no usar su W/L/T como criterio de selección. Si hay
defecto, versionar corrección y repetir solamente validación necesaria antes
de congelar el piloto, dejando constancia del defecto y los hashes.

Piloto: cinco variantes + base/noop VQ, ocho rivales habituales, **1005000–003**,
ambos asientos, 616 episodios. Ejecutar tras loop4, sin segundo torneo grande
simultáneo. Torneo/validación/pareado existentes, fuentes congeladas antes de
empezar. Reportar activación por hashes y por siembras observadas; no usar
monedas para rescatar delta W/L/T agregado negativo.

Seleccionar hasta dos brazos de mayor delta estrictamente positivo, sin exigir
significación en este piloto pequeño. Confirmación **1006000–015**, once rivales
de confirm1: 1.152 episodios si uno, 1.600 si dos. Semilla como unidad y ambos
asientos; IC95 por semilla y dos vías si estimable. No elegir rivales a posteriori.

Gate de candidata real: delta confirmado ≥3 pp, ningún rival <−20 pp,
acciones válidas, runtime admisible y revisión de mecanismo. IC cruzando cero
se informa como incertidumbre; no convierte una señal útil en CHAMPION ni es
un veto absoluto a experimentar en ladder. Mantener los registros negativos.
