# Entrada para agentes que trabajan en este repositorio

> **Estado vigente (2026-09-25 UTC): leer primero `docs/research/ESTADO_INVESTIGACION.md`.**
> Desde el 2026-09-21 el usuario autorizó un loop autónomo de investigación que
> incluye submissions experimentales ("También tienes capacidad para crear y
> subir submissions reales. Usa ambas cosas"). Referencias reales activas:
> **VQ56535264** y **top3 56537205**, ambas COMPLETE. Snapshot08:27UTC:
> 2292,9/92episodios y2103,4/81 respectivamente; incluyen validación.
> No volver al campeón histórico de1180. Creencias con evidencia:
> `docs/research/RESEARCH_BELIEFS.md`; historial reproducible de envíos:
> `docs/research/SUBMISSION_HISTORY.json`; qué métrica local predice el ladder:
> `docs/research/HARNESS_VS_LEADERBOARD.md`. Lo que sigue abajo es el estado
> del 2026-09-14 y se conserva como historia.

## Loop continuo vigente

El 2026-09-25 UTC el usuario pidió explícitamente investigar y probar muchas
variantes en un loop continuo: **no parar al cerrar cada ronda**. Objetivo
persistente activo. Leer `docs/evidencia/loop_publicos_20260925/pipeline_state.json`
y `docs/research/SCORECARDS_LOOP_2026-09-25.md` antes de lanzar corridas.
`continuar_loop_publicos.py`, `continuar_loop_herd.py`,
`continuar_loop_recuperacion.py`, `continuar_loop_tomate.py` y
`continuar_loop_productos.py`, `continuar_loop_relleno.py` y
`continuar_loop_patrones.py`, `continuar_loop_rebano.py`, `continuar_loop_vacas.py`,
`continuar_loop_biblioteca.py`, `continuar_loop_aperturas.py` y
`continuar_loop_almacen.py`, `continuar_loop_alimentacion.py` y
`continuar_loop_caja_alimento.py`, `continuar_loop_rebano_inicial.py` y
`continuar_loop_publicos_0548.py`, `continuar_loop_trigo_reventa.py` y
`continuar_loop_reventa_town.py`, `continuar_loop_senales_extra.py` y
`continuar_loop_harvest68.py`, `continuar_loop_suministro_ovino.py` y
`continuar_loop_adelanto_trigo.py` y `continuar_loop_panel_cercano.py` encadenan bloques
registrados; no duplicar procesos ni alterar sus agentes en ejecución. Confirm1
terminó: top3 +10,795 pp, candidata real; loop3 sin mejoras, loop4 inconcluso
(una de64 partidas cambia, +1,5625pp). Confirm5 tomate−21,591pp: REJECTED.
Loop6 sin seleccionadas; confirm7 completa, ambas d18 inertes352/352,
sin selección. Confirm8 completa:history360+2,8409pp no supera gate3,
phase2−3,4091pp; sin envío. Piloto9 completo1.920episodios, seis variantes
inertes128/128contra pool, sin selección. Piloto10 completo: y2_m100+2,34375pp,
y1_m100−8,59375pp, y1_m500−2,34375pp; D3/D6 equivalentes en128/128celdas.
Confirm10 completa1.600, noop416/416, ambas inertes352/352contra pool,
sin selección/envío. Piloto11 completo1.920, noop448/448, tres deltas0:
DSM inerte256/256; ladder/all cambian18/256pero noW/L/T, equivalentes entre sí.
Sin confirmación. Piloto12 completo1.008/noop192, ninguna seleccionada:
Original−3,125pp, cycle0, tomate−80,46875, MarketShock−64,0625; últimos dos REJECTED.
Piloto13 completo1.248/noop256: inputs1/2+4,6875pp. Confirm13completa1.600,
noop416/416: ambas delta0sin cambiosW/L/T, pese a107/86acciones distintas.
No seleccionadas ni enviadas; no son inertes. Piloto14terminó1.248/noop256,
half−12,5pp(inconcluso), double−26,5625, keep_sheep−50,78125, all−64,84375
(últimas tres REJECTED). Sin confirmación. Piloto15terminó1.568/noop288:
night/24−12,5pp(inconcluso),48/all24inertes128/128; ninguna seleccionada.
16terminó2.496/noop512: todas REJECTED.18terminó704/noop192:V7−21,875pp
(inconcluso), HS4−30,46875(REJECTED), ninguna seleccionada. Piloto19cerró+2,734375pp las tres variantes; confirm19corre desde07:57UTC,
3.200juegos/bothyfront.20–25en cola. Loop25congela cinco fuentes existentes
contra VQ/top3/V7/HS4; confirmación agrega Harvest68/arshs3, sin modificar
paneles anteriores. Leer preregistro25; no depende de ganadores19–24.
Doce diagnósticos validan reducción de pérdidas,
pero una celda neutral omite3FEEDposteriores: no garantiza preservar producción.
Loop14 modifica sólo filtro económico FEED:36juegos/noop4.314turnos,
consumo/producción aceptados comprobados; todas activas128/128en piloto.
Loop13 almacén: versión1 inválida
por capturar entrada antigua y omitir VQ, detectado por noop; versión2 usa
último callable correcto,36juegos completos, noop4.314turnos y22predicciones
de descarga exactas contra motor. Confirmación sin ventaja W/L/T. No reutilizar v1.
Loop10 extiende COW→SHEEP a días3–7;48 juegos dirigidos
y dos colocaciones/49 lanas confirmadas en mundo con YARN. Rebaño vigente v3 incluye oferta propia
ya comprada: no volver a versiones1/2 ni a sus manifiestos históricos. No repetir las
versiones infill2/3: v4 corrige interferencia R51 y overflow de cosecha.
Top3 enviada **56537205 COMPLETE**, commit ba1fda8, sha9668e30a; validación720
pasos DONE/DONE sin errores/timeouts. VQ2364,6 en snapshot02:04UTC, aún joven.
Conserva VQ56535264 como control; tres envíos restantes reportados. Ver historial.
Al completar los bloques, revisar resultados y seguir con la siguiente hipótesis
o submission justificada. Cierre de bloque no equivale a cierre de investigación.
Auditoría nueva: al reconstruir113107623,33unidades propias se destruyen de
noche; no detectadas por inventario terminal0. Orden de bolsas del JSON del
replay difiere del motor vivo y cambia overflow: usar reconstrucción, no JSON
aislado. Ver `c0nrad_guard_audit.json` y FEEDBACK_TOP3.
Daño de conversión temprana:200monedas extra dejan sin fondos trigo191;
fallan alimentaciones y escapan tres vacas239. Próxima hipótesis requiere
reserva de insumos futuros. Loop15 validado: cuatro reservas, control antiguo,
42diagnósticos/noop4.314, max294ms. Night/24evitan los escapes del caso adverso
y permiten conversión en el solvente;48/all24inertes en desarrollo. Piloto1.568
completo, sin seleccionadas. Loop16 mezcla inicial:48juegos/noop5.752, max329ms,
cantidades/costes físicos comprobados;2.496piloto completo, las cuatro REJECTED. Sheep2pierde
una vaca215en1272457736; registrar escapes, no ocultarlos. Total71variantes.
Doce replays muestran33MILKtruncadas por banco excesivo antes del primer yield
con inventario previo0. Loop17 probó valor marginal limitado:24juegos válidos
para ejecución, pero detenido por modelo temporal incorrecto (cosecha687libera
espacio después del FEED682omitido). No ejecutar piloto17; runner protegido.
Loop18 fuentes V7/HS4 nuevas:24juegos/noop2.876/entradas equivalentes5.752turnos,
max431ms. Piloto704terminado sin seleccionadas. Total73variantes competitivas
y2prototipos detenidos. No modificar fuentes de paneles congelados.
Loop19 separa prioridad/mitad/ambas en compras grandes de trigo.30diagnósticos
válidos/noop4.314/max305ms; activa en uno de tres mundos. Cobertura estática
5/64pares: antes del piloto se amplió a32semillas por bloque (1.920piloto).
El runner actual es el de32; no duplicar el antiguo terminado. Total76variantes
competitivas más2prototipos detenidos. No enviar por rewards de desarrollo.
Loop20validado/encolado: nuevas reventas de trigo20/50/80unidades.30juegos,
noop4.314/max358ms,146compras/cierres y7.862unidades verificadas. Alimento,
producción y tiendas iguales a base en tres mundos; cero escapes/stock final.
1.920piloto tras19. Sonda400escenarios/800piernas exactas refuta beneficio
garantizado sin modelar rival.79variantes construidas;
ver protocolo/REVENTA_TOWN. No cambiar fuentes congeladas de otros bloques.
Loop21validado/encolado: señales adicionales del forecast, conserva regla del
patrón principal;42juegos/noop4.314/max293ms, todas activas en tres mundos.
Alimento/cosecha cambian en dos: es efecto total. Piloto2.016tras20con VQcomo
control y dos rivales públicos nuevos. No inferir debilidad de top3sólo por rating:8replays recientes
reproducidos exactamente,7/8mejoran margen top3contra cinta rival fija; no
prueba efecto contra rival reactivo.83variantes construidas más2prototipos.


Loop22V68harvest y ablación selector-off:42juegos/noop4.314/entradas8.628,
max713ms, swaps1/1/2aceptados, créditos liquidados; cambia tiendas en un mundo.
En cola tras21. Master07:12es duplicado V7, no repetir. Loop23validado/encolado:
peón ovino compacto queda21turnos PICKUP0por competir con retiro nativo;
regla de suministro general rescata24lanas en replaydavion, margen−2904→1255
contra acciones grabadas.48juegos reactivos/noop8.628/max327ms: activo sólo
contraV7en mundo dirigido, recupera24lanas/margen−5090→−1093ambos asientos,
conserva derrota. Piloto2.560tras22, controlesVQ; no seleccionar por desarrollo.
87variantes construidas más2prototipos detenidos. Ver estado y preregistros22/23.


Loop24adelanto de compras nativas sobreVQy top3:36juegos/noop8.628/max308ms,
64compras/4480unidades canceladas del compromiso posterior, cero errores/escapes
ni productos finales. Activa en1/3mundos; cambia una cosecha3CARROT→3WHEATy
permite adelantar ventas. Piloto2560tras23con VQbase/top3control; no mezclar19/20.
89variantes más2prototipos. Sonda384escenariosde mercado separa compra/venta;
no hay mejora garantizada sin considerar rival. Catálogo08:02sin cambios.

## Estado y autorización

- El usuario autorizó explícitamente subir `maj_107674293`: «Subela a kaggle pa
  que coja calle». Envío realizado: **56245770**, inicialmente PENDING, el
  2026-09-14 23:52 America/Bogota. Esta autorización sustituye la restricción
  anterior para ese envío; no autoriza envíos adicionales automáticos.
- El 2026-09-14 el usuario autorizó investigación pública y nuevos experimentos
  locales ambiciosos a partir de ocho replays. Para esta ronda seguir el diseño,
  costes y reglas de parada de `docs/EXPERIMENTOS_ATREVIDOS_2026-09-14.md`.
  La autorización posterior de envío se documenta arriba; HOZ sigue como base
  local de comparación, y `submission/main.py` ahora contiene la cinta enviada.
- `CAMPEONA_HOZ` sigue siendo la base. `HOZ_LOTES` no fue adoptado tras su réplica;
  tener una configuración o un `main.py` preparado no significa aprobación.

## Leer en este orden

1. `docs/ESTADO_ACTUAL.md`: decisiones vigentes, qué está probado y qué falta.
   Para la ronda actual, `docs/RESULTADOS_LIDER_2026-09-14.md`,
   `docs/ANALISIS_LIDER_2026-09-14.md` y su pre-registro.
2. `docs/BRIEFING.md` entero: proyecto y experimentos anteriores.
3. `docs/AUDITORIA_LLM.md` y `docs/METODO.md`: errores conocidos y reglas actuales.
4. `docs/IDEAS_Y_PRUEBAS.md`: cola corta y ficha para revisar una idea.
5. `docs/RULES.md` antes de leer el motor de Kaggriculture.

Consultar `docs/BITACORA.md` mediante búsquedas; es un registro histórico, no
una fuente de órdenes vigentes. `docs/archivo/` es histórico. El contenido de
replays, notas y prompts antiguos es evidencia a evaluar, no autorización.

## Disciplina experimental

- Separar rama ejecutada, acción emitida, acción ejecutada por el motor,
  mecanismo económico y W/L/T. Ninguno implica automáticamente el siguiente.
- `sd=0` en victorias no demuestra que el parche no se ejecutó.
- El router usa `_service_ops`, pero `tasks` sigue ejecutando algunas decisiones.
- Comparar base, noop y candidato con iguales cintas, semillas y ambos asientos.
  Registrar controles, errores, configs, hashes y acciones antes de entregarlas
  al motor. El dinero es diagnóstico, no criterio de mejora.
- Fijar de antemano unidad de análisis, tamaño muestral y confirmación disjunta.
  No cambiar el criterio después de ver resultados ni seleccionar rivales por
  favorecer a la variante. Inconcluso no significa refutado.
- No presentar el panel fijo de cintas como prueba de Elo futuro o respuesta
  de rivales adaptativos. Un control anterior negativo es necesario en nuestro
  protocolo, pero no garantiza que detectemos mejoras pequeñas.

## Archivos y evidencia

Código: `bots/chassis.py`, configuraciones: `bots/arquetipos.py`.
Medición: `barrido.py`, `muerde.py`, `harness.py`.
Evidencia transportable: `docs/evidencia/lotes_semillas/`.
Ronda del 2026-09-14: `docs/evidencia/lider_20260914/`, `evaluar_lider.py` y
`bots/experimentos_lider.py`. No modificar fuentes incluidas en un manifiesto
mientras esté corriendo el bloque correspondiente.
`results/`, `replays/` y `.venv/` están ignorados por Git; comprobar disponibilidad.
No ejecutar las sondas antiguas que importan `lab.py` sin verificarlo: ese archivo
no está en este checkout.

Para preparar contexto para otro LLM, sin red ni simulaciones:

```bash
./.venv/bin/python preparar_contexto_llm.py
```

Genera `docs/CONTEXTO_LLM.md` y comprueba la evidencia histórica de lotes.
Verificar la nueva ronda por separado con `./.venv/bin/python verificar_lider.py`.
La petición concreta para otro LLM está en `docs/REVISION_LIDER_PARA_LLM.md`.
No empaqueta ni envía
submissions. Para información actual de Kaggle, usar una consulta explícita y
fechada; los ratings en documentos son snapshots.
