# Loop28: no penalizar ventas que no podíamos observar

La auditoría offline reproduce exactamente las 1.650 selecciones nativas de
PREDICT en los seis replays reales del corte0914. De 21.540 pares producto/turno,
719 no eran elegibles por el filtro nativo de precio anterior>3; el criterio
adicional de mínimo alcanzado excluye otros154. Aun así, el matcher nativo
penaliza eventos de biblioteca sin pareja en esas ventanas.

Las dos máscaras se fijaron antes de analizar resultados. Native altera432
rankings y129señales; floor447rankings y137señales. Las179.937/195.122
penalizaciones omitidas se cuentan repetidamente sobre ventanas solapadas:
no son observaciones independientes. No se usó acierto predictivo ni dinero
para elegir una máscara. Evidencia: `forecast_censor_audit.*` y
`auditar_censura_forecast.py`.

## Desarrollo validado

48partidas: tres mundos, ambos asientos, V7reactivo, padresVQ/top3, sus dos
noops y cuatro candidatas. Noops exactos en8.628turnos de ambos jugadores;
caja reconciliada y720DONE; cero errores observados, máximo406,79ms.
86.160comprobaciones de máscara y40.306pares declarados observables por floor:
en todos, las ventas aceptadas coinciden con el incremento físico de mercado.
Las cantidades de ventas propias antiguas aún pueden estar mal atribuidas;
esa corrección se experimenta por separado en27 y no se combina aquí.

| Política | Celdas con acciones propias distintas | Rankings distintos |
|---|---:|---:|
| censor_native_vq | 6/6 | 294 |
| censor_floor_vq | 6/6 | 306 |
| censor_native_top3 | 4/6 | 448 |
| censor_floor_top3 | 4/6 | 454 |

Las dos máscaras top3 tienen acciones y rewards iguales en estas seis celdas,
aunque sus rankings internos difieren. SobreVQ se separan en el mundo dirigido
2111590720. No presentarlas como cuatro réplicas independientes.

Márgenes por asiento (ambos coinciden en esta cuadrícula):

| Mundo | VQ → native / floor | top3 → native / floor |
|---|---|---|
| 1071000 | +115 → +258 / +258 | +669 → +508 / +508 |
| 1071001 | −1.298 → −1.301 / −1.301 | +323 → +323 / +323 |
| 2111590720 | −1.531 → −2.772 / −2.169 | −708 → −792 / −792 |

Ningún W/L/T cambia en desarrollo. Corregir el uso de evidencia ausente no
garantiza mejorar decisiones. En el tercer mundo, las dos variantesVQ aceptan
un FEEDovino adicional y cosechan211lanas frente a210; cambia también la
pérdida nocturna. Más producto coincide aquí con peor margen. En los demás
casos se conserva el trabajo/cosecha/pérdidas registrados. Tiendas iguales y
cero escapes de ambos jugadores en los48juegos. No afirmar producción
universalmente invariable ni exactitud perfecta de inferencia.

Fuentes y ledgers en `forecast_censor_smoke.*`; verificador reproducible
`verificar_censura_forecast.py`, resultado `forecast_censor_validation.json`.
El runner28 está en espera tras27. Piloto1.568 contra panel cercano, confirmación
disjunta1.920/2.560 si procede, con ambas submissions reales como referencias.
Gates y semillas en el preregistro28. No hay evidencia competitiva todavía.
