# Pre-registro — capa "trigo primero" (BUY_PRODUCT WHEAT antes de HIRE)

Escrito antes de evaluar. 2026-09-28 ~01:55 UTC.

- **Origen:** casi-copia de tds27 del ladder (Ryu Sonoda) que nos ganó; su diferencia
  con tds27 es sobre todo el orden de mercado: compra de trigo antes que contrataciones.
- **Candidata:** tds27top3 + `apilar_trigo_primero.py` (sha bef4d43e). Sonda: actúa en
  0-3 turnos por partida; no inerte.
- **Evaluación:** `torneo_trigo1`: ref vs trigo1, rivales tds27, cha22, hl836, top3cc,
  hl74; semillas 4650000-4650031 (32 nuevas), dos asientos, `--sin-cruces`,
  pesos `pesos_barrido_0928.json`.
- **Regla:** adoptar si delta ponderado con IC95 por semilla > 0 y ningún linaje con IC
  entero < −10 pp. Si el punto es > 0 pero el IC incluye 0: PROMISING (candidata a
  combinar con otras capas positivas en una confirmación nueva).
