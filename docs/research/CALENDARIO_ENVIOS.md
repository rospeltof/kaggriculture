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

## Regla del par final para el 30-sep (fijada 2026-09-29 18:40 UTC, antes de ver datos nuevos)

Datos a las 18:18-18:34 UTC (workflow `par-final-datos-reales`, 8 agentes, 3 escépticos):
final_29 2209-2215 con 141 partidas públicas (105-36); final_xc1 2211 con 200 (100-100).
Desde las 12:00 UTC: f29 23-15, xc1 8-26, +37 pp [+14; +55]. Modelo logístico con el rating
actual de cada rival: f29 − xc1 = +92 a +135 puntos (IC inferior > 0 en todas las variantes
salvo una contaminada por partidas del 28). Los 8 episodios ERRORED de f29 (04:14-06:34 UTC)
son una caída de la plataforma: otros equipos tienen ERRORED en el mismo tramo y Kaggle no
deja bajar esos replays (403).

Comprobación: `./.venv/bin/python revisar_par_final.py --desde 2026-09-29T18:40` entre las
12:00 y las 13:00 UTC del 30 (solo lectura). **Se propone al usuario reenviar la copia exacta
de final_29** (`submission/main_publico_final_29.py`, sha cf129189, descripción «copia exacta
de 56655371») para que sustituya a final_xc1 si se cumplen (a) y (b) y (c):

- (a) basta una: (a1) rating f29 − rating xc1 ≥ +40; o (a2) solo partidas públicas creadas
  después de 2026-09-29T18:40Z, ≥ 30 por bot, xc1 gana ≤ 40 % y f29 gana ≥ 45 %.
  (Corrige la regla del workflow: el % en un tramo ya visto mide cuánto va cada rating por
  detrás de su equilibrio, no la fuerza; con bots iguales pasaba el 65 % de las veces.)
- (b) f29 gana ≥ 45 % de sus últimas 30 y, desde el corte, no tiene 3 o más ERRORED que xc1.
- (c) rating f29 ≥ rating xc1 − 25.

El usuario tiene que aprobarlo en el chat en ese momento; la regla no es una aprobación.
Si falla cualquiera, no se toca nada: el par final es final_29 + final_xc1.

Envío y fallos (corrección del tercer escéptico):
1. Enviar al principio de la ventana (12:00-13:00 UTC) para tener margen.
2. Tras enviar, listar las submissions y comprobar el estado de la copia.
3. Si la copia queda en ERROR: si final_xc1 sigue listada como activa y juega partidas nuevas,
   el ERROR no ocupó hueco y se puede reintentar una vez con el mismo archivo. Si final_xc1 ya
   no juega, el ERROR ocupó su hueco: **no reintentar** (otro envío desplazaría a final_29) y
   el par final queda en final_29 sola.
4. Nunca usar final_xc1_sa_bp_ms90 ni variantes nuevas en este hueco, salvo que pasen su propio
   pre-registro completo y el usuario lo apruebe (ver PREREG_GUARDA si existe).

### Enmienda 2026-09-29 22:10 UTC — f29g confirmada (PREREG_GUARDA)

La regla (a)/(b)/(c) no cambia. Cambia solo el fichero que se propone si se cumple:
**`results/guarda_0929/f29g.py` (sha a77f667c)** = bytes de final_29 + guardia contra copiadores
de MS. Confirmación: 0/672 celdas distintas de final_29 sin copiador; +44,9 pp [+38; +51]
contra copiadores; fuera de muestra (191 cintas reales) +142 $/partida, 1 L→W, 0 W→L.
Par resultante: final_29 (asentada) + f29g. Descripción del envío: «f29g = final_29 (sha
cf129189) + guardia GS contra copiadores de MS; confirmación PREREG_GUARDA».

Fallo de validación de f29g: si final_xc1 sigue activa, el único reintento se hace con la
**copia exacta de final_29** (sha cf129189, ya validada en Kaggle), no con f29g. Si final_xc1 ya
no juega, no se reintenta (par final = final_29 sola), como arriba.
Antes de enviar: copiar f29g a `submission/main.py` y comprobar el sha a77f667c.

### Procedimiento del 30-sep (preparado 01:40 UTC)
1. 12:00 UTC: `./.venv/bin/python revisar_par_final.py --desde 2026-09-29T18:40` (solo lectura).
2. Si la regla se cumple → pedir aprobación explícita al usuario en el chat. Sin ella, nada.
3. Con aprobación: `cp submission/main_publico_f29g.py submission/main.py`; comprobar sha
   a77f667c; `kaggle competitions submit -c kaggriculture -f submission/main.py -m "f29g = final_29
   (sha cf129189) + guardia GS contra copiadores de MS; PREREG_GUARDA: +44,9 pp [+38; +51] contra
   copiadores, 0/1.152 celdas distintas de final_29 sin copiador. Apache-2.0: tetsutani et al."`
4. Vigilar hasta COMPLETE; comprobar que las activas son 56655371 y la nueva; si ERROR, seguir la
   regla de fallos (reintento solo con la copia exacta de final_29 y solo si xc1 sigue activa).
5. Registrar en SUBMISSION_HISTORY.json y en ESTADO_INVESTIGACION.md; commit.
