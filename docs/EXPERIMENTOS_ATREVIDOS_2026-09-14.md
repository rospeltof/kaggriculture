# Experimentos estructurales a partir de ocho replays nuevos

Fecha: 2026-09-14. Petición vigente: investigar en internet, analizar los ocho
replays y ejecutar experimentos locales ambiciosos. **No autoriza envíos a
Kaggle.** Las restricciones anteriores sobre barridos quedan sustituidas para
esta investigación. `CAMPEONA_HOZ` y `submission/main.py` se conservan.

## Evidencia antes de los experimentos

Los ocho episodios corresponden a Majkel1337 contra ocho rivales distintos.
El usuario lo identifica como primer lugar; los archivos no contienen Elo ni
rank. No asignaremos Elo por dinero final. Son ocho victorias seleccionadas,
no una muestra aleatoria. Los IDs no demuestran por sí solos fechas distintas.

`investigar_lider.py` extrajo ambas cintas con offset +1. Reprodujo los 720 estados
de cada episodio con su semilla original, comparando granjas, privados, mercado,
tiendas, día y hora. Todos coinciden. Un ledger observado en `_commit_unit`
registra operaciones aceptadas, precio por unidad y costes atómicos; concilia
exactamente $3.000 + flujos con el dinero final de cada jugador. No usamos el
estimador antiguo `ventas_reales.py`, que no resuelve ventas a $1, órdenes
fallidas, DROP simultáneo ni precios de cada unidad de la ráfaga.

Datos: `evidencia/lider_20260914/replays.json`, `validacion.json` y ledgers.
Cintas: `bots/meta/tapes/maj_*.json.gz` y `sepopp_*.json.gz`.

Hallazgos descriptivos: 12 melones tempranos en todas las aperturas; segundo
cuadrante en step 149 en las ocho; al día 15 hay entre 13 y 22 animales con
composiciones diferentes. Son calendarios e interacciones que no se reproducen
simplemente aumentando `animals` en nuestro chasis. Los cuatro replays 107685970,
107692988, 107696961 y 107710951 comparten sus primeras 86 acciones; los dos
últimos comparten 145. Es posible ramificar sin cambiar el prefijo de acciones.

## Información pública consultada

- [Experiencia de un participante con cintas y ligas](https://www.kaggle.com/competitions/kaggriculture/discussion/739273):
  reporta fuerte transferencia de economías grabadas y renovación del meta.
  Es evidencia reportada por su autor, no nuestra réplica.
- [Ramificar replays según tiendas](https://www.kaggle.com/competitions/kaggriculture/discussion/738727):
  Yusuke Hayashi describe ramificación temprana como técnica de su agente.
  Inspira nuestra comparación de prefijos; no se descargó ni copió su código.
- [Resultados preliminares de RL](https://www.kaggle.com/competitions/kaggriculture/discussion/740022):
  Roy Wei reporta 350 millones de pasos y falta de validación contra una liga.
  No es evidencia de que RL sea imposible ni garantía de un ganador rápido.
- [Límites de clonación de conducta](https://www.kaggle.com/competitions/kaggriculture/discussion/738079):
  el autor describe errores acumulados al pasar de evaluación offline a ejecución.
  Motiva verificar la conducta y la legalidad en partidas completas.

## Pre-registro de exploración (antes de evaluar candidatos)

Pregunta: ¿un cambio de arquitectura supera claramente a HOZ, y las adiciones
reactivas mejoran una cinta sin romper su economía? Buscamos saltos de al menos
15 puntos W/L/T; esta ronda no intenta resolver décimas.

Implementaciones nuevas, aisladas en `bots/experimentos_lider.py`:

1. **Ocho cintas originales:** controles de transferencia y ocho candidatos de
   referencia, sin modificar acciones. Seleccionarlas también es búsqueda.
2. **Árbol de rutas:** usa sólo información visible. Prefijo común hasta d3;
   elige ruta por la tienda actual. Rama lana/leche a d6 sólo entre las dos
   cintas que comparten ese prefijo. Nunca consulta tiendas futuras ni semilla.
3. **Árbol con ventas reactivas:** misma producción; vende productos no usados
   como insumo cuando realmente están en shed, incluyendo DROP del mismo turno.
   Conserva cantidades programadas de WHEAT/FERTILIZER y las otras compras.
   Hipótesis: menor retraso al monetizar sin desfinanciar la ruta.
4. **Apertura transferida:** sigue una cinta hasta d10 y continúa con HOZ.
   Hipótesis: el planificador propio aprovecha una estructura inicial distinta.
   No es repetir la antigua perturbación de cantidad de animales.

Base HOZ, noop exacto y control anterior FB exacto: **14 brazos** en total.
Piloto: **cuatro semillas 214000–214003**, ambos asientos, ocho cintas `lad_`
espaciadas uniformemente por nombre (índices 0,5,...,35) y los ocho rivales
`sepopp_` aportados. Selección del panel independiente del rendimiento.
Coste: 14 × 16 × 4 × 2 = **1.792 episodios**, además de ocho reproducciones y
sondas técnicas pequeñas. Progreso y registros incrementales; ocho workers.

El piloto sólo selecciona UNA configuración por W/L/T agregado, con desempate
por nombre. Reportar todos los brazos y los dos estratos. Es exploración, no
confirmación; estos 16 rivales no se presentan como muestra del ladder actual.
En piloto la integridad exige noop exacto y cero errores; el control FB debe
dar delta negativo, sin exigir significancia con cuatro semillas. La confirmación
sí exige intervalos negativos para ese control. La sonda técnica previa (semilla
213000, un rival, cinco brazos) sólo comprobó prefijos, conducta y finalización;
sus marcadores no eligen al ganador del piloto.

## Confirmación prevista

Si el mejor candidato mejora al menos 15 puntos a HOZ en piloto con controles
válidos, congelarlo y compararlo con base, noop y FB en **las 40 cintas lad_ y
los ocho sepopp_**, ambos asientos, semillas desde **215000**. Ese panel es fijo;
40 rivales antiguos y ocho recientes no equivalen al leaderboard futuro.

Dimensionar ANTES de confirmación con sd de los cuatro promedios por semilla:
`n = min(32, max(16, ceil(((1.96+0.84)*max(sd,0.10)/0.15)**2)))`.
Es aproximación de potencia al 80% para 15 puntos en panel fijo; con cuatro
semillas sd es incierto, por eso suelo 0,10 y mínimo 16. Si requiere >32,
declarar el límite presupuestario y no afirmar potencia suficiente. Máximo
48 × 32 × 4 × 2 = **12.288 episodios**. No se aumenta n al mirar resultados.

Primario: delta pareado por (rival,semilla), asientos promediados, IC95 t entre
promedios de semilla. Sensibilidad registrada: agrupamiento a dos vías
`V_rival + V_semilla - V_celda`, df del clúster menor. El panel es fijo para
el estimando primario; dos vías no convierte familias de cintas en rivales
independientes. Exigiremos ambos intervalos >0, delta >=15 puntos y control FB
negativo en ambos para llamar al resultado salto local confirmado. La varianza
de dos vías negativa se reporta como inválida, no como certeza.

Noop debe ser idéntico por episodio en acciones, rewards, estados y pasos.
Errores, timeouts, faltantes o cambios de fuentes invalidan el bloque. Se congelan
hashes del código, motor y cintas; no se editan mientras corre.

Después, diagnóstico contra las ocho cintas del líder (fuentes de entrenamiento,
no holdout independiente) y contra HOZ vivo, con nuevas semillas y ambos asientos.
No llamar al candidato ganador del ladder por esos diagnósticos. El candidato
sigue experimental y no se empaqueta en `submission/main.py`.

Si el piloto no supera el umbral, documentar fallos y el mecanismo observado;
no gastar el bloque de confirmación ni rescatar por dinero final.
