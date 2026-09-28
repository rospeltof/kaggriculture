# Pre-registro — barrido de parámetros de tds27top3 (eliminación sucesiva)

Escrito antes de ejecutar. 2026-09-28 ~00:15 UTC.

- **24 variantes** de un parámetro cada una (±) sobre tds27top3 (sha fb31fb24), en
  `results/exp_0928/barrido/`: zanahoria (V9_CARROT_RATIO 1,5/2,2; BOOM 2,8/4,5;
  _CA_MARGIN −22/−8), carrera (V9_RACE_MARGIN 8/16, WINDOW 20/40, DEFAULT 36/48,
  _RACE_HORIZON_MIRROR 12/36), rebaño (V9_HERD_MIN_WOOL 100/200, _HD2_RATIO 1,15/1,5),
  pronóstico (_V92_P_H 32/64, _HP_WINDOW 3/6), fertilizante (V9_FERT_FIRST_DAY 12/16).
  Asignación al final del módulo: las que se leen al importar quedarán inertes.
- **Etapa 1:** `torneo.py --out results/torneo_barrido_p1 --sin-cruces --vs ref,<24>`,
  rivales tds27, cha22, hl836, top3cc, hl74; semillas 4600000-4600007 (8), dos asientos.
  Métrica: delta pareado ponderado (`pesos_barrido_0928.json`) frente a ref.
  Pasan las 5 con mayor punto (con punto > 0).
- **Etapa 2:** las 5 + ref, mismos rivales, semillas 4610000-4610023 (24 nuevas).
  Adoptar la mejor si su delta ponderado tiene IC95 por semilla > 0 y ningún linaje
  con IC95 entero < −10 pp. Etapa 2 se analiza sola (sin sumar la etapa 1).

## Resultado etapa 1 (torneo_barrido_p1, 2.000 partidas, 0 errores)

**18/24 variantes inertes** (delta exacto 0): la asignación al final del módulo no llega
a esas constantes (se leen al importar). Activas: hp3 +8,12 [−4,89; +21,14]; hp6 +5,00
[−6,82; +16,82]; cam22 +3,12 [−4,26; +10,51]; ff12 +3,12 [−16,22; +22,47]; cam8 −6,88;
rd36 −14,38. Pasan a etapa 2 (punto > 0): **hp3, hp6, cam22, ff12**.

## Adenda: barrido 1b (antes de ver datos)

Las 18 inertes se repiten sustituyendo el valor EN SU LÍNEA de definición (misma
lista de valores), mismo diseño que la etapa 1 (semillas 4600000-007), para que la
etapa de criba sea válida para todas. Mismas reglas.

## Adenda: criba de inercia y barrido 2 (antes de ver resultados de etapa 1b/2b)

Criba (2 semillas × 2 asientos vs cha22, comparación exacta con ref):
- 1b (sustitución en su línea): activas cr15, ff16, hw200; 15 inertes.
- 2 (40 variantes de capas recientes): activas cab5, cxo15, cxr12, or2m16, s731b,
  s738l3, s738l6, sr12, sr4; 31 inertes.
**Etapa 1b** para las 12 activas: mismo diseño que la etapa 1 (semillas 4600000-007,
mismos rivales y pesos, `--sin-cruces`); pasan las 5 mejores con punto > 0 a una
etapa 2b con 24 semillas nuevas (4620000-4620023) y la misma regla de adopción.

## Resultado etapa 2 (torneo_barrido_p2, 1.200 partidas, 0 errores, semillas 4610000-023)

hp3 −2,08 [−7,35; +3,19] (regresión desde +8,1); hp6 +1,67 [−0,72; +4,05]; **cam22 +5,00
[−2,26; +12,26]** (cha22 +4,2, tds27 +7,8, harvest 0, resto +2,1); ff12 +0,42. **Ninguna
se adopta** por la regla. cam22 queda PROMISING (signo positivo en ambas etapas y en todos
los linajes; mismo ajuste elegido por haodou092) → se usa como **instrumento en el slot 2**
(el mandato lo permite; slot 2 era top3cc, sin aporte al máximo) y se sigue confirmando.

## Resultado etapa 1b (torneo_barrido_p1b, 1.040 partidas, 0 errores)

sr12 +5,00 [−6,82; +16,82]; s738l6 +3,12 [−4,26; +10,51]; 0,00 (activas en acciones, sin
cambio de resultado): sr4, or2m16, hw200, ff16, cxr12, cxo15, cr15; −3,12: s738l3, s731b,
cab5. Pasan a etapa 2b (punto > 0): **sr12, s738l6** (semillas 4620000-4620023).

## Resultado etapa 2b (torneo_barrido_p2b, 720 partidas, 0 errores, semillas 4620000-023)

sr12 +2,60 [−1,20; +6,41] (tds27 +5,5; harvest +4,2); s738l6 +4,48 [−2,32; +11,28]
(tds27 +9,1; harvest +4,2; resto +4,2). Ninguna se adopta sola; ambas positivas en las
dos etapas y sobre todo contra la familia tds27 (40% de los rivales reales el 28-sep).

## Pre-registro: combinación s738l6 + sr12 (antes de evaluar)

`results/exp_0928/combo_s738l6_sr12.py` (sustitución en su línea de ambas). Evaluación
`torneo_combo1`: ref vs combo, mismos 5 rivales y pesos, semillas 4640000-4640047 (48
nuevas), dos asientos. Adoptar (slot 1 o 2) si delta ponderado con IC95 por semilla > 0
y ningún linaje con IC entero < −10 pp.
