# Pre-registro — ablación de `seed_stock_aware`

Escrito **antes** de ejecutar. Fecha: 2026-09-05. Autorización del usuario:
ejecutar este barrido local. **No autoriza subir nada a Kaggle.**

## Por qué es la medición que falta

`CAMPEONA_HOZ` = `CAMPEONA_FASE` + `seed_stock_aware` + `harvest_76`.
Con `harvest_76` **refutado** el mismo día (−0,08; IC95 [−0,65; +0,49]),
`seed_stock_aware` (+6,4 reportado) es **la única mejora que sostiene el linaje
de septiembre**.

⚠️ **Sus datos crudos de confirmación se perdieron**: `results/panel40.json` fue
sobrescrito por una corrida posterior. El +6,4 no es verificable sin remedir, y
además se calculó con la unidad de análisis equivocada (t por celda sobre un
diseño cruzado).

Precedente inmediato, dos veces el mismo día: la compra parcial (+5,00 y +4,84
en dos bloques → **+0,23** con 16 semillas) y `harvest_76` (+2,50 y +2,50 →
**−0,08** con 16 semillas). **Ambos siguieron el mismo guion: dos bloques
positivos, ninguna réplica potente, cero al replicar.**

## Diseño

- **Ablación leave-one-out** sobre la base activa: `sin_ssa` = `CAMPEONA_HOZ`
  con `seed_stock_aware=False`.
- **Semillas 105000–105015 (16)**, disjuntas de todo lo anterior
  (91xxx, 92xxx, 101xxx–104xxx).
- Brazos: `base`, `noop`, `_peor` (CAMPEONA_FB exacta), `sin_ssa`.
- 40 cintas × 16 semillas × 2 asientos × 4 brazos = **5.120 episodios**.

## Predicción falsable, fijada antes

| si `seed_stock_aware` vale el +6,4 reportado | `sin_ssa` ≈ **−6,4**, IC95 excluyendo cero |
|---|---|
| si era ruido, como los otros dos | `sin_ssa` ≈ **0** |
| si es real pero menor | valor intermedio, y sabremos cuánto |

## Regla de decisión

**Integridad primero:** `noop` exacto, `_peor` claramente negativo en ambos
criterios, cero errores. Si falla, no se interpreta.

| resultado | qué significa |
|---|---|
| ambos IC95 < 0 | el mecanismo es real; el campeón está bien fundado |
| ambos incluyen cero | **todo septiembre fue ruido**; el bot con respaldo es `campeona_fase` |
| discrepan | se reporta la discrepancia; no se adopta postura |

Bloque único, bilateral, sin encadenar. No se ajusta nada a partir de lo que se
vea aquí.

## La pregunta de fondo

Si este también sale a cero, el problema **no son los mecanismos sino el
protocolo**: confirmar con 8 semillas no tiene potencia para efectos de este
tamaño, y habríamos estado adoptando ruido de forma sistemática. Eso obligaría a
revisar las ocho adopciones anteriores, no sólo esta.
