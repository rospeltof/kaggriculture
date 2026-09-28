# Calendario de envíos hasta el cierre (fijado 2026-09-28 18:40 UTC)

Regla del usuario (28-sep): **al cierre, las dos submissions activas deben ser nuestros dos
mejores bots; no gastar los envíos finales en experimentos.** Solo cuentan las 2 más
recientes y cada envío nuevo desplaza a la activa más antigua.

## Activas ahora
- 56628181 final_xc1 (probada: ~2345-2385, 58W-20L en 78 partidas reales).
- 56626892 final_frps (dominada por final_xc1; se va con el próximo envío).

## Plan
1. **29-sep 00:00 UTC:** enviar final_29 (`submission/main_publico_final_29.py`, sha cf129189;
   +7,55 pp [+3,80; +11,31] frente a final_xc1, 29/29 celdas a favor). Par: final_xc1 + final_29.
2. **Resto del 29:** ningún envío experimental. Solo se envía un bot nuevo si (a) pasa piloto
   y confirmación con semillas disjuntas y mejora a final_29, y (b) final_29 rinde bien en
   partidas reales (así el par sigue siendo dos bots fuertes). Ese envío desplazaría a
   final_xc1.
3. **30-sep, decisión del par final antes de las ~18:00 UTC:**
   - Por defecto no se hace nada: final_29 + final_xc1.
   - Si final_29 rinde en real por debajo de final_xc1 en la misma franja (≥ 60 partidas),
     se investiga antes de tocar nada.
   - Si hay un bot confirmado mejor: el par final = los dos mejores confirmados.
   - Comprobar que ambas activas están en COMPLETE; reservar al menos 2 envíos del 30 para
     reenviar si alguna falla la validación.
4. **Después de las ~20:00 UTC del 30:** ningún envío salvo para reparar una validación fallida.

## Opciones para el segundo hueco (decidir el 30 con datos reales de final_29)

| par final | a favor | en contra |
|---|---|---|
| final_29 + final_xc1 | cobertura real: final_xc1 ya probada (~2345-2385) y sin SA/BP/MS | final_xc1 es 7,5 pp peor en el harness |
| final_29 + final_xc1_sa_bp_ms90 | los dos con MS (confirmada); cubre solo las extensiones MSB | casi sin diversidad |
| final_29 + final_29 (reenvío) | dos sorteos independientes del mejor bot | ninguna cobertura |

Criterio: si tras ≥ 60 partidas reales final_29 gana claramente más que final_xc1 en la misma
franja, el segundo hueco pasa a un bot con MS (fila 2 o 3); si no, se queda final_xc1.

## Lectura 28-sep 22:40 UTC (antes del envío de final_29)

final_xc1: 123 partidas reales, 73W-50L (59%); las últimas 45 (ya a ~2350) 15W-30L y el rating
baja a 2318: su equilibrio está hacia 2320-2350. De esas 30 derrotas, 21 son por menos de
$1.000 (8 en pares YARN) — lo que atacan SA y MS — y 9 por más de $1.000; las más grandes
(−$22.600 weense, −$11.000 Yaroslav) son de producción: el rival cultiva mucho tomate (21 y
11 casillas) y lo vende en lotes de 20-56. No hay defensa rápida para eso.
