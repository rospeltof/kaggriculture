# VQ y top3: ocho replays recientes y control de fuente enviada

Consulta API06:52:55UTC (archivo0653): top3 56537205 COMPLETE2094,7/75episodios listados;
VQ56535264 COMPLETE2289,1/88. Incluyen validación; no son muestras equilibradas
por edad, semillas ni rivales. El rating no demuestra que el forecast top3 sea
la causa de la diferencia. No se envió otra submission.

Se eligieron cuatro episodios públicos completados más recientes de cada
fuente por endTime/id ANTES de leer rewards. Dieciséis reproducciones: la
fuente realmente enviada y la otra fuente contra las acciones rivales grabadas.
Los ocho controles reproducen719acciones propias/720estados completos y
rewards exactos. Caja conciliada en los16, mismas tiendas en cada pareja,
cero escapes propios, máximo348ms. Un escape rival en dauriel persiste en
ambas reproducciones. Esto valida ejecución y procedencia, no fuerza poblacional.

| Episodio / rival | Fuente real | Margen VQ | Margen top3 | Diferencia top3 |
|---|---|---:|---:|---:|
| 113181522 / Duvor Richard | top3 | +686 | +222 | −464 |
| 113181570 / hisatarosu | top3 | +30 | +120 | +90 |
| 113174624 / daviondk | top3 | −3595 | −2904 | +691 |
| 113168442 / kyosan | top3 | +127 | +862 | +735 |
| 113181013 / minghao mei | VQ | −1225 | −1017 | +208 |
| 113180865 / ZeroGrain | VQ | +799 | +805 | +6 |
| 113176293 / Mao Nishino (mao1756) | VQ | −940 | +72 | +1012 |
| 113173184 / dauriel | VQ | +695 | +859 | +164 |

Los valores contrafactuales sólo valen **condicionados a las acciones grabadas**.
El rival no adapta sus ventas/compras a las nuevas observaciones. No sumar el
cambio de derrota a victoria contra Mao como W/L/T de un torneo reactivo,
ni transformar7/8márgenes positivos en tasa de éxito real o delta de Elo.
Las partidas reales de esta muestra son top3:3V/1D, VQ:2V/2D; tampoco es una
comparación causal o tasa global acumulada.

El caso adverso Duvor ilustra una externalidad: top3 gana16monedas propias
adicionales pero el rival gana480,460de ellas en WOOL con igual volumen.
Margen−464aunque sube nuestra caja. En los otros siete casos la diferencia
de margen es positiva, entre6y1012. No inferir que toda venta adicional sea
falsa alarma; cambiar timing mueve también el precio cobrado por el rival.
Kyosan/ZeroGrain/Mao cambian algunas cantidades propias: no prometer que
un parche de ventas conserva toda la producción futura.

Próximo loop21: conservar señales del primer patrón y moderar sólo las que
añaden segundo/tercero, mediante rango2, consenso, mitad o horizonte12. Se
añade VQ como control y los dos rivales públicos recientes por regla fijada
antes de conocer su piloto18. Las reglas se prueban contra agentes reactivos;
no se seleccionan por esta tabla. Ver `PREREG_LOOP21_SENALES_EXTRA_2026-09-25.md`.

Evidencia: `forecast_pair_replays_0653.plan.json`, informe del mismo prefijo,
16ledgers y16trazas de forecast, dos planes de muestreo y archivo
`paired_feedback_0653.replays.tgz`. Código `auditar_forecast_pareado_real.py`.
