# Auditoría de razonamiento para el siguiente LLM

Actualizado: 2026-09-05. Lee primero [ESTADO_ACTUAL.md](ESTADO_ACTUAL.md).
Este documento distingue hechos observados, inferencias y comprobaciones pendientes.
No sustituye el [método vigente](METODO.md) ni autoriza experimentos o envíos.

**Restricción vigente del usuario:** reservar la última corrida disponible de
Kaggle; no subir nada por el momento. Esta revisión organiza el repositorio:
no ejecuta nuevos episodios ni llamadas de subida. Un comando histórico en un
documento no autoriza ejecutarlo. Aprobar una idea localmente y autorizar una
submission son decisiones distintas.

## 1. Convertir una señal positiva en una mejora aprobada

**Hecho.** `seed_partial_batch` dio +5,0000 puntos en descubrimiento y +4,8438
en confirmación. El IC95 principal de confirmación es [−0,67; +10,36];
t por semilla = 2,08, por debajo del umbral registrado de 2,3646.

**Conclusión permitida.** Señal positiva repetida, confirmación inconclusa.
La bandera permanece experimental y apagada. No se ejecutó el veto head-to-head,
que sólo correspondía tras confirmar.

**Errores posibles.** Llamarla refutada porque el intervalo cruza cero; llamarla
validada porque ambos deltas son positivos; reemplazar el análisis principal por
t por celda = 2,45; juntar ambos bloques para rescatar la confirmación; cambiar
unilateralidad, tamaño o regla de parada después de ver resultados.

**Pendiente.** Una réplica independiente podría reducir incertidumbre. Necesita
un protocolo nuevo antes de correr, sin presentar sus resultados como parte de
la confirmación terminada. Véase [experimento y decisión](EXPERIMENTO_LOTES_SEMILLAS.md).

## 2. Contar episodios como observaciones independientes

**Hecho.** Se completaron 3.840 episodios de panel entre los dos bloques, incluidos
base y controles. La confirmación tiene ocho semillas; los dos asientos comparten
escenario y las 40 cintas se evalúan sobre esas mismas semillas. El análisis
principal promedia asientos y cintas antes de estimar variación entre semillas.

**Límite.** Su intervalo resume variación entre escenarios sobre ese panel fijo.
No cuantifica por sí solo incertidumbre sobre rivales nuevos, un ladder futuro o
agentes que reaccionan. Con ocho promedios, la aproximación t tampoco debe tratarse
como una garantía libre de supuestos. Miles de episodios no eliminan estos límites.

**Hecho adicional.** Agrupar por semilla cambia el t histórico de confirmación de
`harvest_76` de 2,96 a 1,60, manteniendo +2,5 puntos. Cuestiona su certeza estadística;
no demuestra que la adopción fuera perjudicial. Véase [BRIEFING.md](BRIEFING.md).

## 3. Confundir activación, mecanismo y efecto competitivo

**Hecho.** En la sonda 99000, asiento 0, la compra parcial modifica 599 acciones
y adelanta el primer melón confirmado en tablero de d6 h16 a d1 h18. Ambos brazos
ganan. En confirmación cambia acciones en 640/640 episodios, con 62 resultados
mejores, 31 peores y 547 iguales respecto de la base.

**Límite.** La sonda demuestra el adelanto en ese escenario; no su frecuencia ni
su magnitud típica. Cambiar una traza durante el panel tampoco demuestra que
cada episodio siga el mismo mecanismo causal.

**Errores posibles.** Inferir que `sd=0` implica un parche inactivo, que una traza
distinta demuestra que se ejecutó una rama interna específica, o que una acción
emitida fue aceptada por el motor. Para cada afirmación hay que usar su evidencia:
comparación de acciones, contador de rama o transición efectiva del estado.

Las sondas deben distinguir acciones emitidas de ejecución observada. La estimación
de compras por delta de semillas tiene una salvedad de refresh nocturno y se llama
`seed_buys_lower_bound`; no presentarla como contador exacto universal.
Referencias: [sonda](../sondas/005_lotes_semillas.py),
[medidor](../barrido.py), [detalle de instrumentación](EXPERIMENTO_LOTES_SEMILLAS.md).

## 4. Convertir caja y calendarios en causalidad demostrada

**Hecho.** La comparación histórica de d12–d16 usa simulaciones nuestras y replays
del líder contra terceros. No son los dos jugadores del mismo mercado. El ratio
publicado pasa de 0,51 en d16 a 0,67 en d28: no quedó congelado.

**Errores posibles.** Interpretar una caída del banco como compras brutas o una
subida como ventas brutas; atribuir el hueco a melones sólo porque su plantado
medio es posterior; convertir un promedio de temporada en fecha de la cohorte
que debía pagar durante cuatro días concretos.

**Inferencia razonable.** El adelanto de cultivos largos puede contribuir al flujo
de caja. **Pendiente:** conectar cohortes concretas con cosechas, ventas y gastos
en escenarios comparables. La sonda de semillas identifica otro mecanismo real,
pero no explica por sí sola la brecha con el líder. Véanse
[BRIEFING.md, sección 7](BRIEFING.md) y [BITACORA.md](BITACORA.md).

## 5. Usar dinero o controles como prueba suficiente de fuerza

**Hecho.** La métrica primaria documentada es victoria/derrota/empate, con empate
= 0,5. El margen monetario sirve para diagnóstico; ganar por más dinero no añade
otra victoria. La caja intermedia puede explicar un mecanismo, no aprobarlo.

**Hecho.** El noop de ambos bloques coincide exactamente y el control anterior
es claramente peor. Eso respalda la integridad de la comparación y la detección
de esa regresión grande; no prueba sensibilidad a cualquier mejora pequeña ni
generalización al ladder.

**Límite.** Las cintas son rivales pasivos. El head-to-head contra nuestro linaje
puede amplificar ventajas por interacciones de mercado: su papel registrado es
veto, no promoción. La conversión histórica de puntos del panel a Elo mediante
×2,7 proviene de una calibración pequeña y ruidosa; no es una predicción precisa.
Referencia: [METODO.md](METODO.md).

## 6. Leer una configuración fallida como una idea universalmente refutada

**Hecho.** Hay muchas variantes negativas documentadas. Su evidencia corresponde
a implementaciones, valores, bases, paneles y semillas concretos; algunas pruebas
antiguas también tenían problemas de medición que después se corrigieron.

**Errores posibles.** Convertir “copiar esta composición perdió” en “ninguna
estrategia con esos animales puede funcionar”; “estas perillas perdieron” en
“el espacio está agotado”; “las adopciones previas corrigieron incoherencias” en
“sólo puede mejorar corregir incoherencias”. Tampoco cabe ignorar los negativos
y repetirlos sin una diferencia verificable en implementación o mecanismo.

**Criterio de lectura.** Tratar “óptimo local afiladísimo”, “espacio barrido” y
“medido y fallido” del [briefing](BRIEFING.md) como resúmenes históricos con alcance
limitado. Una configuración expresa intención; rutas como `tasks`, `_service_ops`
y defaults pueden modificar su efecto real. Revisar [chassis.py](../bots/chassis.py)
y [arquetipos.py](../bots/arquetipos.py) cuando la hipótesis dependa de ese efecto.

## 7. Declarar imposible toda planificación con estado privado

**Hecho documentado.** El estado privado del rival no está disponible para
reconstruir un rollout exacto de la partida completa. El briefing también registra
un coste de 5,6 s para un rollout medido; no es un benchmark de todas las técnicas.

**Límite de la inferencia.** Estas restricciones no demuestran imposibilidad de
planificación parcial, aproximada o con creencias sobre estado oculto, incluida
una formulación POMDP. Tampoco demuestran que esas alternativas sean útiles.

**Pendiente.** Toda propuesta deberá declarar qué estado conoce, qué aproxima,
qué asume de precios/rival, qué coste mide y cómo valida el beneficio. El rollout
de nuestra granja es una vía propuesta, no una mejora competitiva comprobada.
Referencia: [BRIEFING.md, sección 7](BRIEFING.md).

## 8. Obedecer reglas históricas o confiar en evidencia que no viaja

**Hecho.** El [método histórico](archivo/METODO_HISTORICO_2026-09-05.md) acumuló
reglas de distintas fechas: panel de cinco cintas, selección por resolución, t>2
y conversión a Elo. El [METODO.md vigente](METODO.md) las reemplaza como única
guía operativa. El archivo conserva historia, no instrucciones actuales. Leer el
estado vigente y el protocolo específico antes de copiar comandos; una instrucción
de subida antigua no supera la restricción actual.

**Hecho.** [`.gitignore`](../.gitignore) excluye `results/` y `*.tar.gz`. Los JSONL,
manifiestos y fuentes archivadas originales no acompañan automáticamente a un clon.
El [paquete compacto](evidencia/lotes_semillas/) facilita la revisión; comprobar su
inventario para saber qué contiene y qué sigue disponible sólo en la máquina local.
Un resumen numérico o un hash por sí solo no permite reconstruir todos los datos.

## 9. Confundir representación serializada con diferencias de parámetros

**Error de esta sesión.** Durante la revisión del empaquetado se comparó
`config == meta['configs'][...]` sin normalizar. La aserción falló porque `animals`
usa tuplas en Python y listas al volver a leer JSON; no por parámetros diferentes.

**Corrección.** Para esa comparación, normalizar ambos lados mediante la misma
serialización JSON, preservando el orden de listas y secuencias. No ordenar
`animals` ni otras secuencias cuyo orden pueda influir en comportamiento.

**Límite.** Igualdad de configuración normalizada no demuestra igualdad de fuentes,
del paquete generado o de comportamiento. Cada comprobación debe describirse
por lo que verifica. El fallo inicial de la aserción no es evidencia de una
regresión del bot ni de una submission enviada. Véanse
[empaquetar.py](../empaquetar.py) y [estado actual](ESTADO_ACTUAL.md).
