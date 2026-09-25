# Harness vs leaderboard — qué métrica local predice el ladder

## Lectura nueva — 2026-09-25 UTC

Arshs3 **2292,5 @148 episodios**, v13 **1857,9 @136**, tras aproximadamente 20 h
activos. Ambos superan las cintas propias (seek 1324,8, decem 1285,9); el orden
arshs3 > v13 coincide con el torneo cerrado (20-0 directo). Evidencia API:
`docs/evidencia/research_20260925/*_episodes_snapshot.json` y
`submissions_after_vq.json`. Ratings observados, no una estimación causal del
delta ni un ranking actual del equipo; no se consultó ese ranking.

VQ (56535264) separará otra pregunta: 0 efecto contra pool histórico, pero
ventaja repetida contra copias, ¿sirve en una población real poblada de forks?
Se conservó arshs3 original como control activo. No comparar el rating de arranque
de VQ con 148 episodios del original para rechazarla. Muestra descriptiva de 16
partidas recientes de arshs3: 4V/11D/1E, no su tasa acumulada.

La frase histórica «sólo ≥100 Elo informa» no debe usarse como umbral universal.
La información depende de episodios, rival, edad y ruido observado. Asimismo,
muchas cintas/forks emparentados no son muchas familias independientes.

## Historial de calibración

Actualizado: 2026-09-23 18:00. Dataset acumulado y conclusiones provisionales.

## Dataset

| submission | candidato | local: delta global vs HOZ | local: vs FUERTES | ladder | episodios |
|---|---|---|---|---|---|
| 55993562 | grano (seed_stock_aware) | +6,4 | — | 772 (vs hoz 677) | 71 |
| 55994874 | hoz (+harvest_76, refutado) | +2,5 → −0,08 | — | 677–831 según fecha | 68 |
| 56245770 | **maj_107674293** (cinta fija) | +14,4 / +10,0 | **43,0%** (peor de todos) | **857** | 126 |
| 56444202 | tree_v1 | +9,0 / +6,1 | 53,1% (+10,2) | **967** @19 ep (TEMPRANO) | 19 |
| 56444505 | maj+guard6 | ≈ cinta (harness no ve el fallo) | — | 714 @32 ep (53% W/L) | 32 |
| 56447472 | tree_v1 + guard(6) | +6,1 global | fuerte: tree 20,2% | **1.132** @81 | 81 |
| 56449108 | **107570947 + guard(8)** | — | fuerte (guard 6): 54,8% · **gcal: 53,1% (cal1)** · 42,7% (rivales r2) | **1.164** @78 | 78 |
| 56504082 | **110304538 + gcal(8)** | — | cal1 62,5% · **rivales r2 61,6% (+18,9 vs 107570947)** | pendiente | 0 |

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

**5. (2026-09-23) La población de rivales importa más que el tamaño del bloque.**
La misma cinta de referencia rinde 53,1% contra rivales de Majkel/DSM/UMG/Vadim
(sep 11-20) y 42,7% contra los rivales del top-13 de esta semana. El campo se
endurece; confirmar siempre contra la población más reciente disponible.

**6. (2026-09-23) La selección sobre un piloto grande está dominada por ruido.**
111 candidatas × 64 celdas: el 1º (87,5%) cae a 31,0% en población fresca; el 4º
sube a 1º. Successive halving en ≥2 etapas + confirmación en rivales y semillas
disjuntos, siempre.

**7. (2026-09-24) El harness de cintas nunca midió el nivel ABSOLUTO.** Cada
"confirmación" comparaba variantes propias contra rivales-cinta pasivos. Los
agentes públicos (2500-2950 en ladder) nos ganan 20-0 en bucle cerrado. Desde
ahora: toda candidata se mide también en `torneo.py` contra el pool público.

## Regla operativa derivada

- **Métrica primaria local: WR vs panel FUERTE** (80 rivales de Majkel/DSM,
  `fuerte_*`). El panel `lad_` de 40 se conserva como control de no-regresión
  contra rivales débiles.
- Un candidato que gana vs fuertes y pierde poco vs débiles (perfil de
  `107570947`: +21,5 / −0,6) es preferible a uno que gana vs débiles y pierde vs
  fuertes (perfil de la cinta campeona).
