# Kaggriculture

Planner determinista de Python para una simulación de granja 1v1. No usa un
LLM durante la partida. Este repositorio contiene el agente, el aparato de
medición y el registro de experimentos.

**Estado vigente, 2026-09-25 UTC:** mejor referencia real **arshs3 56511619**
(2292,5 @148 partidas); variante **VQ 56535264** enviada y validada por Kaggle.
**VQ + top3 56537205 COMPLETE** tras confirmar +10,795 pp localmente;
conserva VQ como control. Loops de producción y reparación siguen encadenados.
El loop autónomo permite investigación y submissions experimentales. Leer primero
[ESTADO_INVESTIGACION](docs/research/ESTADO_INVESTIGACION.md),
[creencias](docs/research/RESEARCH_BELIEFS.md) y
[registro de envíos](docs/research/SUBMISSION_HISTORY.json).
`submission/main.py` conserva arshs3 original; el archivo enviado como VQ fue
`submission/main_publico_arshs3_vq.py`. Los informes del 14-sep son históricos.

## Para retomar con otro LLM

1. Darle acceso al repo y pedir que lea [AGENTS.md](AGENTS.md), o generar el
   archivo único de contexto con el comando de abajo.
2. Compartir las [scorecards del loop activo](docs/research/SCORECARDS_LOOP_2026-09-25.md).
3. Revisar el historial y registrar una hipótesis nueva antes de ejecutarla,
   dentro del loop autónomo autorizado. El prompt `REVISION_LIDER_PARA_LLM.md`
   corresponde a la ronda histórica del 14 de septiembre.

```bash
python3 preparar_contexto_llm.py
```

El generador usa sólo biblioteca estándar: verifica hashes, controles y deltas
históricos de lotes guardados, y escribe [docs/CONTEXTO_LLM.md](docs/CONTEXTO_LLM.md). No usa la red,
no simula partidas ni genera o envía un `main.py`.
Los torneos actuales se verifican sin simular con:

```bash
./.venv/bin/python validar_torneo.py docs/evidencia/research_20260925/forecast_pilot
./.venv/bin/python validar_torneo.py docs/evidencia/research_20260925/public_refresh
```

`verificar_lider.py` comprueba por separado la ronda histórica del 14 de septiembre.

## Ruta de lectura

| Archivo | Propósito |
|---|---|
| [ESTADO_ACTUAL](docs/ESTADO_ACTUAL.md) | Autorización, base, candidato, resultados y pendientes |
| [Resultados del líder](docs/RESULTADOS_LIDER_2026-09-14.md) | Piloto completo, confirmación, diagnósticos y decisión registrada |
| [Análisis del líder](docs/ANALISIS_LIDER_2026-09-14.md) | Ocho replays, contabilidad exacta, diferencias de conducta y límites |
| [Experimentos actuales](docs/EXPERIMENTOS_ATREVIDOS_2026-09-14.md) | Rutas por tiendas, ventas reactivas y transferencia de apertura |
| [BRIEFING](docs/BRIEFING.md) | Proyecto completo y experimentos anteriores |
| [AUDITORIA_LLM](docs/AUDITORIA_LLM.md) | Errores de inferencia y límites de las conclusiones |
| [METODO](docs/METODO.md) | Guía general; complementada por el protocolo de esta ronda |
| [IDEAS_Y_PRUEBAS](docs/IDEAS_Y_PRUEBAS.md) | Cola corta, coste y ficha de revisión entre LLMs |
| [RULES](docs/RULES.md) | Modelo del motor con evidencia; leer antes del motor |
| [Experimento de lotes](docs/EXPERIMENTO_LOTES_SEMILLAS.md) | Protocolo registrado y resultado inconcluso |
| [Evidencia](docs/evidencia/lotes_semillas/README.md) | Datos, manifiestos y fuentes del experimento |
| [BITACORA](docs/BITACORA.md) | Historia; consultar mediante búsquedas |

`docs/archivo/` conserva documentos superados. No copiar sus instrucciones como
si fueran decisiones vigentes.

## Código y herramientas

- `bots/chassis.py`: `decide`, router, servicios, scorer y compras.
- `bots/arquetipos.py`: `CAMPEONA_HOZ` (base) y `HOZ_LOTES` (experimental).
- `barrido.py`: panel pareado, controles, episodios y manifiestos.
- `evaluar_lider.py`: piloto, confirmación y estrés de las nuevas arquitecturas.
- `bots/experimentos_lider.py`: árbol por tiendas, ventas reactivas y apertura transferida.
- `verificar_lider.py`: reanálisis de evidencia de esta ronda sin simulaciones.
- `muerde.py`: perturbaciones; compara acciones, dinero y estados por separado.
- `sondas/005_lotes_semillas.py`: activación y cohortes de la compra parcial.
- `harness.py`: episodios y espejo. Un duelo contra el linaje no promociona solo.
- `empaquetar.py`: genera `submission/main.py`; ejecutarlo no autoriza subirlo.
- `empaquetar_cinta.py`: exporta una cinta autónoma y archiva el main anterior.
- `verificar_paquete_cinta.py`: equivalencia de acciones y estados entre paquete y cinta.

Las sondas antiguas 001–004 importan `lab.py`, que no está en este checkout.
El README anterior lo anunciaba como existente: no usar esas sondas sin recuperar
su dependencia. Tampoco hay que inventar carpetas `agent/` o `tests/` por ese texto.

## Entorno y reproducción

El entorno local observado usa Python **3.13.5**, `kaggle-environments==1.32.7`,
CLI `kaggle==2.2.4` y `scipy==1.18.0`. No actualizar el motor indiscriminadamente:
un cambio de versión cambia el experimento. El generador de contexto no requiere
estas dependencias. Las simulaciones existentes usan `./.venv/bin/python`.

`results/`, `replays/`, `.venv/` y `*.tar.gz` están ignorados por Git. La evidencia
compacta se copió a `docs/evidencia/` en formatos no ignorados. Los cambios de
este traspaso aún no están guardados en un commit: hacer un clon ahora no incluye por
sí solo archivos nuevos del working tree. El contexto único sí puede compartirse
como archivo independiente.
