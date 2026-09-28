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
