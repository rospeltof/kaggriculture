# Piloto21: moderar señales secundarias

Cerró el2026-09-25 a10:49:39UTC con2.016partidas válidas,352controlesnoop
exactos, cero errores y fuentes archivadas. Runtime Python3.13.5/spawn,
PYTHONHASHSEED=0; witness8460755321718155249. Seis rivales,16semillas,
dos asientos; unidad estadística rival/semilla promediando asientos.
Referencia primaria top3:85,4167%; controlVQ:62,5% en este panel.

| Política | Delta pp vs top3 | IC95 dos vías | Delta vsVQ | Resultado |
|---|---:|---|---:|---|
|extra_half|+0,5208|[−8,3859;9,4275]|+23,4375|Confirmación|
|extra_rank2|−5,2083|[−14,5234;4,1067]|+17,7083|Inconclusa, no seleccionada|
|extra_quorum|−21,875|[−42,6629;−1,0871]|+1,0417|Rechazada en este panel|
|extra_short12|−10,4167|[−19,0403;−1,7930]|+12,5|Rechazada en este panel|

Half mejora tres celdas y empeora otras tres,90iguales; una pérdida es medio
punto y de ahí el pequeño delta positivo. No llamar robusta esta señal. Las
reglas previas seleccionan sólohalf; confirm21 ya corre1.856juegos en semillas
1053000–015 y13rivales. No mirar deltas parciales ni cambiar la variante.

Ninguna variante es inerte:half/rank2/quorum cambian190/192trayectorias propias,
short12cambia184/192; las cuatro actúan en las16semillas. Ver
`pilot21.behavior.json` para todas las diferencias W/L/T y acciones.

La gran ventaja local de top3 sobreVQ vuelve a coexistir con menor rating en
ladder. Eso no identifica la causa: sus poblaciones/rivales son diferentes.
Conservar las dos referencias reales en futuros bloques ya registrados;
no elegir una variante sólo porque superaVQ en este panel.
