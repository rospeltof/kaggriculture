# Reparación de reproducibilidad tras confirm19

El bloque original terminó3.200episodios a las08:35UTC, todos válidos para el
motor, pero el verificador estricto rechazó cuatro de832comparaciones noop:
hybu/asiento0, tds/ambos y hl25/asiento0, siempre semilla1047024. Sólo difiere
el hash de acciones RIVAL; las acciones propias, rewards, estados terminales
reportados, número de pasos y W/L/T coinciden entre base/noop.

El pipeline se detuvo, propagando el fallo a los seis runners pendientes20–25.
Se comprobó la terminación de todos antes de cualquier reinicio. No comenzaron
partidas20–25. Se conserva `confirm19` completo, el primer diagnóstico y el
estado de fallo. No se ejecutó selección sobre sus deltas ni se cambia el gate.

Sonda registrada48juegos: tres rivales afectados, ambos asientos, dos réplicas
por combinación, PYTHONHASHSEED0/1/2/3 en procesos separados. Reproduce ambos
hashes originales de las cuatro discrepancias. Las dos réplicas de cada hash
coinciden; entre hashes, las seis celdas conservan acciones propias, rewards y
los **720estados económicos de `compact_state`** comparados por digest. La única
diferencia rival se ubica en466paraHybu y465paraTDS/HL: orden de ventas de
MILK/WOOL. Esto identifica el mecanismo en estas celdas, no garantiza que toda
permutación de órdenes sea inocua ni que todo código externo sea determinista.

Dos juegos adicionales perfilan los retornos del agente Hybu en466, hashes0/2:
primera diferencia en `_v12_advance` (línea7861), orden generado por
`sorted({item ...}, key=lambda name: -int(prices.get(name, 0)))` en7900.
El precio no desempata nombres con la misma cotización; `set` hereda el orden
del hash del proceso. TDS6949/HL6952 contienen el mismo patrón. Las capas
posteriores cambian otra vez la cola; la diferencia emitida final es la
permutaciónMILK/WOOL descrita arriba. Fuentes externas intactas.

## Decisión fijada antes de la nueva ejecución

El control original sigue incumpliendo igualdad literal. No se borra la acción
distinta ni se relaja `validar_torneo.py` para darlo por aprobado. Se repetirá
**toda** la confirmación registrada con runtime fijo bajo el nombre nuevo
`confirm19_fixedhash0`: mismas fuentes, base/noop, dos candidatas, once rivales,
32semillas1047000–031 y ambos asientos;3.200episodios. No es una confirmación
estadística adicional ni una ampliación de muestra: reemplaza la medición
invalidada. La selección del piloto19y gates≥3pp/peor rival≥−20se conservan.

Antes de arrancar se fija PYTHONHASHSEED=0 para el proceso del torneo y todos
sus workers mediante el entorno del lanzador común. `torneo.py` registra
versión de Python, método de multiprocessing, semilla de hash y hash testigo
de WHEAT en proceso padre y cada episodio. El verificador exige coherencia de
ese entorno cuando esos nuevos campos existen, además de los controles
literales previos. Los agentes quedan byte por byte iguales.

Verificación técnica previa: torneo `runtime_fixed_smoke`, seis episodios con
base/noop/Hybu en1047024, ambos asientos y dos workers. Completo, noop2/2exacto,
cero errores; proceso padre y todos los workers registran hashseed0y el mismo
testigo8460755321718155249. No se usa su puntuación para elegir una política.
Dos copias temporales con hashseed/testigo alterados fueron rechazadas por el
verificador. También se comprobó que el confirm19original sigue rechazado:
la reparación no debilitó noop. `runtime_guard_checks.json`, cero juegos nuevos.

La misma configuración se aplica prospectivamente a20–25, aún sin partidas.
No cambian sus brazos, rivales, semillas ni reglas. Sus fuentes, manifiestos y
preregistros anteriores se conservan; esta nota es la adenda de runtime común.
Una sola confirmación grande, seguida de la cola anterior. Runners nuevos con
logs separados; no duplicar procesos antiguos ni reutilizar el prefijo original.

Los resultados serán condicionales a ese runtime. Antes de enviar una futura
candidata, comprobar sensibilidad a hashes alternativos en celdas de mecanismo
y daño; un cambio de mercado puede ser relevante en otros contextos. No basta
haber encontrado aquí permutaciones económicamente neutras.

Evidencia: `confirm19.control_failure.json`, `confirm19.pipeline_failure.json`,
`confirm19.noop_probe.plan.json`, `.results.json`, `confirm19_hash0–3.*`, y
sonda de localización `confirm19.order_origin.*`, bajo
`docs/evidencia/loop_publicos_20260925/`.
