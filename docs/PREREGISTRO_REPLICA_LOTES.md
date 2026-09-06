# Pre-registro — réplica independiente de la compra parcial

Escrito **antes** de ejecutar el bloque. Fecha: 2026-09-05.
Autorización del usuario: ejecutar este barrido local. **No autoriza subir nada
a Kaggle**; esa decisión se toma después y por separado.

## Por qué existe este bloque

`seed_partial_batch` dio +5,00 (descubrimiento, semillas 101000–101003) y +4,84
(confirmación, semillas 102000–102007). El veredicto registrado fue
**inconcluso** con el criterio agrupado por semilla: IC95 [−0,67; +10,36], t=2,08
contra un crítico de 2,3646.

El reanálisis del 2026-09-05 encontró que **el veredicto depende de la unidad de
agrupamiento**, y que ninguna de las dos usadas hasta ahora es la correcta:

| unidad | n | t (bloque de confirmación) | |
|---|---|---|---|
| celda | 320 | +2,45 | trata celdas cruzadas como independientes |
| semilla | 8 | +2,08 | descarta la dimensión de las cintas |
| cinta | 40 | +2,83 | descarta la dimensión del entorno |
| **dos vías (CGM)** | df=7 | **+2,52** | correcta para el diseño cruzado |

El panel es un diseño **cruzado**: 40 cintas × 8 semillas, ambas dimensiones son
factores aleatorios. La varianza correcta es `V_cinta + V_semilla − V_celda` con
los grados de libertad del clúster más pequeño.

## ⚠️ Conflicto de criterio declarado

**Calculé el agrupamiento a dos vías DESPUÉS de ver el resultado del bloque 2, y
cambia el veredicto de inconcluso a significativo.** Eso es selección de criterio
post-hoc, justo lo que advierte `AUDITORIA_LLM.md` §1.

Mitigación adoptada: **este bloque exige que AMBOS criterios excluyan cero.** Es
estrictamente más duro que cualquiera de los dos por separado, y por construcción
no puede favorecer al candidato por haber elegido el análisis.

## Diseño (fijado antes de observar nada)

- **Población:** las 40 cintas `lad_*`, sin selección por resultados. Idéntica a
  los bloques anteriores.
- **Semillas: 103000–103015 (16).** Disjuntas de descubrimiento (101000–101003)
  y de confirmación (102000–102007), y de la sonda (99000).
- **Dos asientos**, promediados por celda.
- **Brazos:** `base` (CAMPEONA_HOZ), `noop` (copia exacta), `_peor`
  (CAMPEONA_FB cargado como configuración exacta, no como update), y
  `partial_batch` (CAMPEONA_HOZ + `seed_partial_batch=True`).
- **Coste:** 40 × 16 × 2 × 4 = **5.120 episodios**, ~70 min de CPU local.

Tamaño elegido por potencia: con el sd entre semillas observado en el bloque 2
(6,60 puntos), 16 semillas dan t≈2,94 incluso con el criterio agrupado por
semilla, que es el más conservador de los dos.

## Regla de decisión (fijada antes)

**Integridad, primero.** Si alguna falla, el bloque no se interpreta:
1. `noop` idéntico a `base` por episodio (acciones emitidas, dinero, estado, W/L/T).
2. `_peor` con IC95 completamente por debajo de cero en **ambos** criterios.
3. Cero errores o timeouts.

**Resultado.** Con integridad válida, sobre el delta pareado de W/L/T:

| condición | veredicto |
|---|---|
| IC95 **por semilla** e IC95 **dos vías** ambos > 0 | **ADOPTAR** |
| ambos incluyen cero | **NO adoptar**; el mecanismo queda cerrado salvo argumento nuevo |
| discrepan entre sí | **NO adoptar**; se reporta la discrepancia como el resultado |

**Este bloque NO se fusiona con los anteriores.** Se reporta solo. Si sale
inconcluso, no se encadena un cuarto bloque para rescatarlo.

**No se ajusta ningún parámetro ni se elige ninguna cinta a partir de lo que se
vea aquí.** El test es bilateral. No se cambia el tamaño después de mirar.

## Qué NO decide este bloque

- No autoriza una submission: eso requiere instrucción nueva del usuario.
- No mide generalización al ladder. Las cintas son rivales **pasivos**; el panel
  estima comportamiento contra esa población fija, no contra agentes que
  reaccionan ni contra el ladder futuro.
- No valida `harvest_76`, que en el mismo reanálisis quedó **no respaldado**
  (dos vías: +2,50, t=+1,76, IC95 [−0,85; +5,85]) pese a estar en la base activa.
