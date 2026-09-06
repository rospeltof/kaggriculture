# Kaggriculture

Planner determinista de Python para una simulación de granja 1v1. No usa un
LLM durante la partida. Este repositorio contiene el agente, el aparato de
medición y el registro de experimentos.

**Estado:** compra parcial prometedora pero inconclusa. **No subir a Kaggle:**
el usuario reservó su última corrida disponible. No hay envíos ni evaluaciones
en curso. Leer [el estado actual](docs/ESTADO_ACTUAL.md) antes de actuar.

## Para retomar con otro LLM

1. Darle acceso al repo y pedir que lea [AGENTS.md](AGENTS.md), o generar el
   archivo único de contexto con el comando de abajo.
2. Copiar el [prompt de traspaso](docs/PROMPT_SEGUNDO_CEREBRO.md).
3. Pedir revisión de evidencia y **una** siguiente prueba, antes de ejecutar.

```bash
python3 preparar_contexto_llm.py
```

El generador usa sólo biblioteca estándar: verifica hashes, controles y deltas
guardados, y escribe [docs/CONTEXTO_LLM.md](docs/CONTEXTO_LLM.md). No usa la red,
no simula partidas ni genera o envía un `main.py`.

## Ruta de lectura

| Archivo | Propósito |
|---|---|
| [ESTADO_ACTUAL](docs/ESTADO_ACTUAL.md) | Autorización, base, candidato, resultados y pendientes |
| [BRIEFING](docs/BRIEFING.md) | Proyecto completo y experimentos anteriores |
| [AUDITORIA_LLM](docs/AUDITORIA_LLM.md) | Errores de inferencia y límites de las conclusiones |
| [METODO](docs/METODO.md) | Única guía operativa vigente de evaluación |
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
- `muerde.py`: perturbaciones; compara acciones, dinero y estados por separado.
- `sondas/005_lotes_semillas.py`: activación y cohortes de la compra parcial.
- `harness.py`: episodios y espejo. Un duelo contra el linaje no promociona solo.
- `empaquetar.py`: genera `submission/main.py`; ejecutarlo no autoriza subirlo.

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
