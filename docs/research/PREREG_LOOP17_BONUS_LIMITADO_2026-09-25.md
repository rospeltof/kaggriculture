# Loop17: valor del alimento con capacidad de producción limitada

**Estado posterior: DETENIDO EN DESARROLLO. No ejecutar piloto17 ni enviar.**
El diseño original queda abajo para trazabilidad.24juegos válidos para control
de ejecución/noop, pero la valoración de cap_fullusa stock presente como stock
nocturno:1039000omiteFEED682, cosecha4huevos687y recoge1en700en vez de2.
La cosecha intermedia invalida la premisa de bonus marginal0. Cap_firstcambia
una valoración en otro mundo pero ninguna acción. No es rechazo por rewards
ni prueba poblacional; no gastar704partidas con ese modelo temporal incorrecto.
`capped_bonus_decision.json` marca competitive_ready=False y el runner rechaza
el lanzamiento sin sobrescribir pipeline. No hay proceso17esperando; loop18,
si valida, se encadena directamente después de16.

Se registra antes de construir/medir candidatos. Auditoría de12replays top3:
33MILK truncadas en primera producción de vacas tardías, con inventario previo0.
El banco puede acumular más cuidado del que cabe en producción. Loop14cambia
multiplicadores de precio; esta ronda cambia unidades marginales valoradas.
Conservar íntegros sus agentes/resultados.

Dos brazos sobre top3, misma regla nativa FEED de días10–28, factor1,25y
comprobación `_r86_next_feed`, sin nuevas rutas ni trabajo:

- `cap_first`: si el próximo amanecer todavía precede la primera producción
  y el banco tiene al menos `max_held−1`, valorar en0el cuidado extra de hoy.
  No omitir alimentación por esta excepción en una noche productiva.
- `cap_full`: lo anterior y, cuando el próximo amanecer sí produce, valorar
  sólo `min(cap,held+1+pending)−min(cap,held+1)`unidades de bonus inmediato.
  El cuidado nuevo de esta noche se banca DESPUÉS de la producción; conservar
  su valoración nativa y horizonte. No borrar ese coste futuro por ver cap hoy.

El filtro nativo exige hambre previa0, trigo en mano y alimentación mañana
prevista por cinta. Es una previsión, no garantía física: medir FEED aceptado,
escapes y producción en el motor. La valoración modificada puede ejecutarse
sin cambiar acción; separar ambos hechos. No modificar `care` ni otras compras.
Noop devuelve literalmente la valoración original.

Desarrollo fijo **1039000**, **1004000**, **1272457736**, ambos asientos contra
arshs3 reactivo, base/dos/noop=**24partidas**. Registrar cambios de valoración,
FEED/CARE aceptados, trigo consumido, cosechas, ventas, hambre y escapes, fuentes
y tiempo. No elegir el brazo por rewards; informar si coinciden o no se activan.

Piloto **1040000–1040015**, cuatro rivales fijos arshs3,tds,hybu,ars40,
ambos asientos:4brazos×4+6internos,×32=**704episodios**. Unidad semilla,
W/L/T pareado vsbase primario, hasta dos positivas ordenadas por delta/nombre.
Noop exacto y cero errores. Sin parar por observar una mejora temprana.

Confirmación **1041000–1041015**, once rivales,**1.152/1.600episodios**.
Gate≥3pp y peor rival≥−20pp, IC95, mecanismo y runtime. Semillas disjuntas.
Encolar tras loop16sólo al validar desarrollo. Sin envío automático ni adoptar
por ahorro de trigo que no cambie resultado competitivo.
