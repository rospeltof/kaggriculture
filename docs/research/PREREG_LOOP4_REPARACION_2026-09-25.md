# Loop 4: cobertura de una reparación rara en mundos nuevos

Pregunta: ¿con qué frecuencia se activa recover_now y qué efecto total tiene
frente a copias reactivas? El piloto de loop2 no activó la reparación en sus
cuatro semillas; no fue una evaluación informativa de ese mecanismo.

Evidencia nueva posterior: en la semilla del fallo real de 113061732, cuatro
episodios frente a arshs3 vivo reprodujeron identidad en asiento 0 y recuperaron
la fresa en asiento 1: margen −671 → +53. Es un caso dirigido y cambia tiendas,
por lo que no estima efecto promedio ni aísla dinero de la planta. Justifica
medir frecuencia/efecto en mundos aleatorios nuevos, no promover el parche.

El espejo opcional original de loop2 exigía activación en su piloto y no se
ejecutará bajo esa regla. Este bloque distinto se registra tras nueva evidencia,
con una pregunta de cobertura y semillas nuevas; no se sumará al piloto como si
fuera confirmación prevista allí. No retocar la variante ni elegir semillas
que contengan maleza después de observarlas.

## Diseño

Base/noop VQ, recover_now congelado de loop2 y arshs3 original. Todos contra
todos, **1003000–1003031**, ambos asientos: 6 cruces ×64 = **384 episodios**.
Usar torneo.py y validar_torneo.py; correr tras pipeline1/2 y loop3, sin otro
torneo grande simultáneo. Primario: delta recover_now vs base contra arshs3,
por semilla promediando asientos. IC95 t por semilla; IC dos vías no aplica
con un único rival. Directo contra VQ es diagnóstico aparte.

Registrar hashes de acciones y proporción de episodios cambiados, errores,
tiempos, número de semillas con mejora/daño y resultados por asiento. Noop exacto.
No cambiar criterio por un directo favorable ni por dinero.

Delta positivo y al menos dos semillas positivas: PROMISING, estudiar mecanismo
de cambios y valorar una prueba real o panel amplio según tamaño/daño. Delta cero
con acciones idénticas: sigue sin cobertura; revisar frecuencia antes de otra
corrida. Daño con intervalo enteramente negativo: REJECTED. Otros resultados:
inconclusos. Este bloque de clones no demuestra mejora universal ni nombra campeón.

La reparación merece conservarse como hipótesis separada aunque las variantes
de predictor mejoren. Cualquier combinación requerirá A, B y A+B en otro bloque.
