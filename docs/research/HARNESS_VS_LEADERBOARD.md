# Harness vs leaderboard — qué métrica local predice el ladder

Actualizado: 2026-09-22 02:30. Dataset acumulado y conclusiones provisionales.

## Dataset

| submission | candidato | local: delta global vs HOZ | local: vs FUERTES | ladder | episodios |
|---|---|---|---|---|---|
| 55993562 | grano (seed_stock_aware) | +6,4 | — | 772 (vs hoz 677) | 71 |
| 55994874 | hoz (+harvest_76, refutado) | +2,5 → −0,08 | — | 677–831 según fecha | 68 |
| 56245770 | **maj_107674293** (cinta fija) | +14,4 / +10,0 | **43,0%** (peor de todos) | **857** | 126 |
| 56444202 | tree_v1 | +9,0 / +6,1 | 53,1% (+10,2) | **967** @19 ep (TEMPRANO) | 19 |
| 56444505 | maj+guard6 | ≈ cinta (harness no ve el fallo) | — | 710 @14 ep (arranque) | 14 |

## Conclusiones (provisionales, se actualizan con cada lectura)

**1. El WR global del panel de 40 NO predice el ladder; el WR contra el subconjunto
FUERTE sí (evidencia: compare2, 2026-09-22).** En el mismo bloque, la cinta
campeona es la mejor vs 40 rivales de ~800 (72,1%) y la PEOR vs 8 rivales reales
de Majkel (43,0%). tree_v1 es −6,7 vs débiles y +10,2 vs fuertes — y en el ladder
va a 967 frente a 857. El ladder nos empareja con rivales de nuestro nivel: al
subir, el subconjunto fuerte es la población relevante.

**2. El harness de cintas pasivas subestima la fragilidad de una secuencia fija
al contexto.** 71,5% local vs 40% real para la misma cinta (56245770). Mecanismo
identificado: los rivales reales mueven el mercado del d0 lo justo para dejar la
caja en \$0 al alba (42% de partidas reales con <4 manos; 15% local).

**3. Los saltos grandes transfieren; los pequeños no se resuelven.** +14 de panel
→ +175 de ladder (cinta vs hoz). +6,4 y +2,5 → indistinguibles del ruido de
±40. Con ~60 episodios el ladder sólo resuelve ≥ ~100 Elo.

**4. Positive surprise pendiente de investigar (punto 13/16):** tree_v1 rinde
mejor en ladder de lo que el panel global predecía. Hipótesis: el ladder ya nos
enfrenta a rivales más fuertes que el panel `lad_` (rating ~800 → ahora 900+).
Comprobación: clasificar los replays de 56444202 por rating del rival y por
tienda d3 cuando pase de 50 episodios.

## Regla operativa derivada

- **Métrica primaria local: WR vs panel FUERTE** (80 rivales de Majkel/DSM,
  `fuerte_*`). El panel `lad_` de 40 se conserva como control de no-regresión
  contra rivales débiles.
- Un candidato que gana vs fuertes y pierde poco vs débiles (perfil de
  `107570947`: +21,5 / −0,6) es preferible a uno que gana vs débiles y pierde vs
  fuertes (perfil de la cinta campeona).
