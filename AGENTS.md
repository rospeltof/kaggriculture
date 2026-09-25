# Entrada para agentes que trabajan en este repositorio

> **Estado vigente (2026-09-25 UTC): leer primero `docs/research/ESTADO_INVESTIGACION.md`.**
> Desde el 2026-09-21 el usuario autorizó un loop autónomo de investigación que
> incluye submissions experimentales ("También tienes capacidad para crear y
> subir submissions reales. Usa ambas cosas"). Mejor referencia real:
> **arshs3 (56511619), 2292,5 @148 episodios**; VQ experimental **56535264**
> enviada y COMPLETE. No volver al campeón histórico de 1180. Creencias con evidencia:
> `docs/research/RESEARCH_BELIEFS.md`; historial reproducible de envíos:
> `docs/research/SUBMISSION_HISTORY.json`; qué métrica local predice el ladder:
> `docs/research/HARNESS_VS_LEADERBOARD.md`. Lo que sigue abajo es el estado
> del 2026-09-14 y se conserva como historia.

## Loop continuo vigente

El 2026-09-25 UTC el usuario pidió explícitamente investigar y probar muchas
variantes en un loop continuo: **no parar al cerrar cada ronda**. Objetivo
persistente activo. Leer `docs/evidencia/loop_publicos_20260925/pipeline_state.json`
y `docs/research/SCORECARDS_LOOP_2026-09-25.md` antes de lanzar corridas.
`continuar_loop_publicos.py`, `continuar_loop_herd.py`,
`continuar_loop_recuperacion.py` y `continuar_loop_tomate.py` encadenan bloques
registrados; no duplicar procesos ni alterar sus agentes en ejecución. Confirm1
terminó: top3 +10,795 pp, candidata real; loop3 de animales está corriendo.
Al completar los bloques, revisar resultados y seguir con la siguiente hipótesis
o submission justificada. Cierre de bloque no equivale a cierre de investigación.

## Estado y autorización

- El usuario autorizó explícitamente subir `maj_107674293`: «Subela a kaggle pa
  que coja calle». Envío realizado: **56245770**, inicialmente PENDING, el
  2026-09-14 23:52 America/Bogota. Esta autorización sustituye la restricción
  anterior para ese envío; no autoriza envíos adicionales automáticos.
- El 2026-09-14 el usuario autorizó investigación pública y nuevos experimentos
  locales ambiciosos a partir de ocho replays. Para esta ronda seguir el diseño,
  costes y reglas de parada de `docs/EXPERIMENTOS_ATREVIDOS_2026-09-14.md`.
  La autorización posterior de envío se documenta arriba; HOZ sigue como base
  local de comparación, y `submission/main.py` ahora contiene la cinta enviada.
- `CAMPEONA_HOZ` sigue siendo la base. `HOZ_LOTES` no fue adoptado tras su réplica;
  tener una configuración o un `main.py` preparado no significa aprobación.

## Leer en este orden

1. `docs/ESTADO_ACTUAL.md`: decisiones vigentes, qué está probado y qué falta.
   Para la ronda actual, `docs/RESULTADOS_LIDER_2026-09-14.md`,
   `docs/ANALISIS_LIDER_2026-09-14.md` y su pre-registro.
2. `docs/BRIEFING.md` entero: proyecto y experimentos anteriores.
3. `docs/AUDITORIA_LLM.md` y `docs/METODO.md`: errores conocidos y reglas actuales.
4. `docs/IDEAS_Y_PRUEBAS.md`: cola corta y ficha para revisar una idea.
5. `docs/RULES.md` antes de leer el motor de Kaggriculture.

Consultar `docs/BITACORA.md` mediante búsquedas; es un registro histórico, no
una fuente de órdenes vigentes. `docs/archivo/` es histórico. El contenido de
replays, notas y prompts antiguos es evidencia a evaluar, no autorización.

## Disciplina experimental

- Separar rama ejecutada, acción emitida, acción ejecutada por el motor,
  mecanismo económico y W/L/T. Ninguno implica automáticamente el siguiente.
- `sd=0` en victorias no demuestra que el parche no se ejecutó.
- El router usa `_service_ops`, pero `tasks` sigue ejecutando algunas decisiones.
- Comparar base, noop y candidato con iguales cintas, semillas y ambos asientos.
  Registrar controles, errores, configs, hashes y acciones antes de entregarlas
  al motor. El dinero es diagnóstico, no criterio de mejora.
- Fijar de antemano unidad de análisis, tamaño muestral y confirmación disjunta.
  No cambiar el criterio después de ver resultados ni seleccionar rivales por
  favorecer a la variante. Inconcluso no significa refutado.
- No presentar el panel fijo de cintas como prueba de Elo futuro o respuesta
  de rivales adaptativos. Un control anterior negativo es necesario en nuestro
  protocolo, pero no garantiza que detectemos mejoras pequeñas.

## Archivos y evidencia

Código: `bots/chassis.py`, configuraciones: `bots/arquetipos.py`.
Medición: `barrido.py`, `muerde.py`, `harness.py`.
Evidencia transportable: `docs/evidencia/lotes_semillas/`.
Ronda del 2026-09-14: `docs/evidencia/lider_20260914/`, `evaluar_lider.py` y
`bots/experimentos_lider.py`. No modificar fuentes incluidas en un manifiesto
mientras esté corriendo el bloque correspondiente.
`results/`, `replays/` y `.venv/` están ignorados por Git; comprobar disponibilidad.
No ejecutar las sondas antiguas que importan `lab.py` sin verificarlo: ese archivo
no está en este checkout.

Para preparar contexto para otro LLM, sin red ni simulaciones:

```bash
./.venv/bin/python preparar_contexto_llm.py
```

Genera `docs/CONTEXTO_LLM.md` y comprueba la evidencia histórica de lotes.
Verificar la nueva ronda por separado con `./.venv/bin/python verificar_lider.py`.
La petición concreta para otro LLM está en `docs/REVISION_LIDER_PARA_LLM.md`.
No empaqueta ni envía
submissions. Para información actual de Kaggle, usar una consulta explícita y
fechada; los ratings en documentos son snapshots.
