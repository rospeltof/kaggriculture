# Pre-registro — arshs3vq + ADV (adelanto de ventas, Ahmed Berat Özer EXP293)

Escrito antes de ejecutar. 2026-09-24 ~06:45 UTC.

- **Motivo:** las 95 derrotas de arshs3 en los torneos son por $257 (p25) /
  $521 (mediana) / $1.147 (p75): no se voltean con micro-ajustes. Sus rivales
  más duros (tds 23 derrotas, hl59 15) llevan la capa ADV y arshs3 no.
- **Hipótesis:** vender antes lo que la cinta vendería en ≤4 turnos (si ya está
  en el cobertizo) gana la carrera del libro de precios a rivales que venden lo
  mismo; debería ganar partidas sobre todo contra tds/hl59/hybu/lp16.
- **Brazos:** ref = arshs3vq (sha 9b463dfb, ya confirmado en espejo);
  cand = arshs3_adv_vq (`apilar_capa_vq.py base tds out adv vq`, sha 2abbca9a).
- **Pool (12):** tds, hl59, hybu, lp16, ars40, hsov, v13, obr, h2965, guru6, wz15, v94.
- **Semillas:** 970000-970009 (nuevas), dos asientos, + directo.
- **Unidad y regla:** como PREREG_VQ. Ambos IC > 0 → candidata a sustituir a
  arshs3vq; punto > 0 con IC que incluye 0 → PROMISING (confirmar con 10
  semillas nuevas sin fusionar); punto ≤ 0 → REJECTED. Riesgo específico:
  choque con la capa PREDICT de arshs3 (ambas adelantan ventas) → vigilar
  el delta contra rivales donde arshs3 ya ganaba 20-0.

## Resultado del descubrimiento (torneo_adv1, 500 partidas, 0 errores)

delta +10,0 pts (81,2% → 91,2%); IC95 semilla [−10,2; +30,2]; dos vías
[−10,0; +30,0]; 22 celdas a favor / 10 en contra. Por rival: tds +30, hl59 +30,
wz15 +25, hybu +20, lp16 +20, h2965 +10, hsov +10, v13 0, v94 0, guru6 −5,
ars40 −10, obr −10. Directo 10-10. Veredicto: **PROMISING**.

## Regla de confirmación (fijada antes de correrla)

- Semillas 980000-980009, mismos brazos y mismo pool de 12; el bloque se
  analiza SOLO, sin fusionar con el descubrimiento.
- Ambos IC > 0 → REAL_WORLD_CANDIDATE firme.
- Punto > 0 y delta medio > 0 en el subgrupo fijado de antemano del linaje tds
  (tds, hl59, hybu, lp16, wz15) → REAL_WORLD_CANDIDATE como instrumento (el
  mandato permite subir con IC que incluye 0 si corrige una debilidad observada).
- Punto ≤ 0 → REJECTED.
- Extra (no decide): arshs3 puro y hsov2 (copia de arshs3) como rivales, para
  comprobar que la ventaja en espejo de VQ se conserva con ADV.

## Resultado de la confirmación (torneo_adv2, 580 partidas, 0 errores)

delta **−2,08** pts; IC95 semilla [−20,2; +16,0]; dos vías [−20,4; +16,2];
12 a favor / 16 en contra. Por rival: hybu +25, tds +10, hl59 +10, lp16 +5,
wz15 +5, ars40 0, v13 0, v94 0, guru6 −10, h2965 −20, hsov −20, obr −30.
**Veredicto: REJECTED** (punto ≤ 0). Lectura: ADV intercambia partidas entre
linajes (gana al linaje tds, pierde con herd-safe/order-book); neto ≈ 0.
Extra: arshs3vq y arshs3advvq ganan 95% a arshs3 y a hsov2 (copia de arshs3):
tercera confirmación de la ventaja de VQ en espejo.
