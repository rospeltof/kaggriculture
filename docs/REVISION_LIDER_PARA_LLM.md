# Revisión independiente de la ronda del líder

Esta es una plantilla que el usuario puede entregar a otro LLM. No autoriza
envíos a Kaggle ni nuevas simulaciones por sí misma.

## Petición sugerida

Actúa como revisor crítico de este repositorio. Lee `ESTADO_ACTUAL.md`,
`RESULTADOS_LIDER_2026-09-14.md`, `ANALISIS_LIDER_2026-09-14.md` y el protocolo
`EXPERIMENTOS_ATREVIDOS_2026-09-14.md`. No aceptes el veredicto sólo porque dos
modelos coincidan. Distingue observaciones, inferencias, propuestas y resultados.

Reconstruye desde `docs/evidencia/lider_20260914/`:

1. Selección del candidato entre los once candidatos y tres controles del
   piloto. Comprueba el empate entre cinta y árbol, el desempate registrado y
   que el tamaño de confirmación se fijó antes de observar sus resultados.
2. Deltas pareados con ambos asientos, agregación por semilla y sensibilidad a
   dos vías. Recalcula las fórmulas independientemente de `summarize` si vas a
   afirmar una auditoría estadística independiente.
3. Noop exacto, control FB, cobertura completa, hashes, semillas disjuntas y
   ausencia de errores. Verifica qué se conserva como estados y qué sólo como
   hashes de acciones; no confundas emisión con ejecución económica.
4. Límites del panel: cambio registrado de pesos 8/8 a 40/8, rivales compartidos
   entre desarrollo y confirmación, familias con prefijos comunes, ocho victorias
   seleccionadas y falta de Elo en los JSON. Explica qué afirmación permiten
   los datos y cuál no.
5. Código de `bots/experimentos_lider.py`: disponibilidad temporal de tiendas,
   prefijos antes de ramificar, copia de acciones, transferencia a HOZ y límites
   del proyector de inventario. Un defecto en una variante no prueba un defecto
   en el candidato que no la usa.

Entrega objeciones priorizadas con archivo, evidencia y consecuencia. Para cada
idea nueva especifica mecanismo, intervención aislada, control, unidad de
análisis, tamaño, coste, partición de desarrollo/confirmación, criterio y regla de
parada antes de proponer ejecutar. El objetivo es transporte a escenarios nuevos,
no rescatar retrospectivamente una celda o ganar dinero en una sola sonda.

## Material mínimo

- Lectura rápida: este archivo y el informe de resultados.
- Contexto documental completo: `docs/CONTEXTO_LLM.md`.
- Auditoría: repo completo con `docs/evidencia/lider_20260914/` y las cintas de
  `bots/meta/tapes/`. `results/` no es necesario para los resúmenes transportables.
- Reproducción de los 720 estados originales: requiere además los ocho JSON de
  Downloads indicados en `replays.json`; sus rutas externas pueden no existir en
  otro equipo. La evaluación frente a cintas no requiere esos JSON originales.

```bash
# Sólo lectura/verificación; no ejecuta nuevas partidas ni usa Kaggle.
./.venv/bin/python verificar_lider.py
./.venv/bin/python preparar_contexto_llm.py --check
```

El primer comando requiere scipy para cuantiles t. El segundo usa biblioteca
estándar y verifica la evidencia histórica de lotes y la vigencia del contexto;
no sustituye la verificación de los experimentos nuevos.
