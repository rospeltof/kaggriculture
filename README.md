# Kaggriculture

Agente para la competencia [Kaggriculture](https://www.kaggle.com/competitions/kaggriculture) de Kaggle: una simulación de granja por turnos (720 turnos / 30 días) donde gana quien termina con más dinero en el banco.

Enfoque: **planner determinista en Python puro** (sin LLMs en runtime — el sandbox de Kaggle corre offline con 1.6 vCPU y 100 MiB de submission). Deadline de submission final: 2026-09-30.

## Setup

```bash
python3 -m venv .venv
.venv/bin/pip install -U kaggle-environments pytest
```

## Estructura

- [lab.py](lab.py) — laboratorio de sondas: corre escenarios guionizados turno a turno para verificar mecánicas del juego contra el motor real.
- [docs/RULES.md](docs/RULES.md) — nuestro modelo de las reglas como afirmaciones falsables: ❓ predicción → ✅ verificada / ❌ refutada (con corrección).
- `tests/` *(próximamente)* — tests pytest que espejan las afirmaciones de RULES.md.
- `agent/` *(próximamente)* — el agente: modelo de estado → planner económico → scheduler de turno → módulo de mercado.

## Método de trabajo

1. Tres fuentes de verdad, en orden de autoridad creciente: página de la competencia → `kaggriculture.py` (el motor, incluido en `kaggle-environments`) → sonda ejecutada.
2. Predicciones primero, código del motor después: cada regla se escribe como predicción falsable antes de verificarla.
3. Ningún cambio de estrategia entra al agente sin pasar por el harness de evaluación (self-play A/B con seeds fijos).
