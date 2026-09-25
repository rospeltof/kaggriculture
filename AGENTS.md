# Entrada para agentes que trabajan en este repositorio

> **Estado vigente (2026-09-25 UTC): leer primero `docs/research/ESTADO_INVESTIGACION.md`.**
> Desde el 2026-09-21 el usuario autorizó un loop autónomo de investigación que
> incluye submissions experimentales ("También tienes capacidad para crear y
> subir submissions reales. Usa ambas cosas"). Referencias reales activas:
> **VQ56535264** y **top3 56537205**, ambas COMPLETE. Snapshot10:48UTC:
> 2291,5/101episodios y2138,5/91 respectivamente; incluyen validación.
> No volver al campeón histórico de1180. Creencias con evidencia:
> `docs/research/RESEARCH_BELIEFS.md`; historial reproducible de envíos:
> `docs/research/SUBMISSION_HISTORY.json`; qué métrica local predice el ladder:
> `docs/research/HARNESS_VS_LEADERBOARD.md`. Lo que sigue abajo es el estado
> del 2026-09-14 y se conserva como historia.

## Loop continuo vigente

## Corte operativo 11:01 UTC — confirm21 activa, prioridad31 validada y en cola

Piloto21 cerró 2.016 partidas/noop352 a10:49:39UTC. Sólo `extra_half` pasa a
confirmación: +0,5208pp vs top3, ICdos vías [−8,3859;9,4275], +23,4375vsVQ.
Rank2 −5,2083 inconclusa; quorum −21,875 y short12 −10,4167 rechazadas en este
panel. Todas activas en16semillas. **Confirm21 corre 1.856 partidas**, no mirar
resultados parciales ni reiniciar;22–31 esperan en secuencia. Un torneo principal.

Loop31 validado:48partidas/noop8.628, máximo364ms,162compras/cierres y8.100unidades
exactas. Preserva cola nativa al cerrar town50. Ambas capas activas4/6; caso dirigido
recupera369de margen y dos derrotas pasan a victorias, sin cambio de producción.
Son desarrollos; piloto1.568 con semillas nuevas pendiente tras30. Analizador de
tres referencias validado con fixture1.920/noop448. Fuentes congeladas y runner31
vivo. Total103variantes competitivas más2prototipos17detenidos. Leer PRIORIDAD_CIERRE.

Otra auditoría explica cinco escapes preexistentes en1080001: venta de trigo
antes de recogidas5/2/2, almacén vacío y FEED fallidos. Un control exacto y dos
perturbaciones válidas: conservar trigo evita1escape; conservar y comprar9 evita5,
con cambios de cosechas y margen+120, aún victoria. Un brazo sólo compra fue
inválido por once órdenes; archivado, no usar su resultado. **Preregistro32 escrito;
candidatas NO construidas ni runner32**. Siguiente trabajo: implementar protección
de déficit para recogidas nativas y validar36partidas antes de encolar tras31.

API10:48:09UTC: VQ2291,5/101, top32138,5/91, COMPLETE. Seis nuevos controles
1050 reproducen719acciones/720estados/caja; seis alternativas con rival fijo,
ningún cambioW/L/T. Hallazgo separado: replay113252591 conserva una vaca comprada
sin colocar; DIG33quita maleza pero no reconstruye pasto, PLACE69falla. Auditoría
ofline exacta, reparación todavía no diseñada ni probada. Leer FEEDBACK_1050 y
TRIGO_RUTA_TARDIA. No nuevo envío; cuota antigua no es vigente.

## Corte operativo 10:36 UTC — confirm20 cerrada, 21 activo, nueva prioridad31

Confirm20 terminó10:25:05UTC:3.200episodios/noop832. Town20+0,2841pp,
town50+1,1364pp; ambos ICdos vías cruzan0 y gatefalse. Ambas cambian704/704
acciones propias, no inertes. No envío; contra los cuatro rivales del piloto,
delta0. Seis celdas W/L/Tdistintas auditadas con tres brazos:18partidas exactas,
167compras/cierres y6.280unidades. Leer CIERRE_REVENTAS20.

Daño v13/1050019: cierre de trigo delante de leche661pierde198propias y gana
171al rival. Dos fases idénticas salvo prioridad verifican recuperación369
con leche primero, mismos inventarios. Preregistro31fija dos variantes sobre
los town50 de VQ/top3, con controles originales adicionales. TODAVÍA no se
han construido ni hay runner31; siguiente trabajo: implementar/validar48juegos
sin tocar20–30. V1del capturador falló por wrapper, v2reproducecontrol exacto.

21corre;22–30esperan, no duplicar procesos.30validado48/noop11.504/max314ms,
32aperturas exactas. BUY12/SELL7mantiene stock5 y sólo cambia acción0en8/8
celdas por política. Pierde2de margen contraVQ (cuatro empates→derrotas en brazo
VQ), gana4contraV7sin cambiar derrotas. Mantiene producción en desarrollo,
no garantía global. Piloto960tras29.101variantes más2prototipos17detenidos.

Último ladder consultado10:02UTC:VQ2295,1/98y top32135,7/88; no nuevo envío.
Lectura pública1018archivada con fuentes primarias; no prueba estrategia nueva.


## Corte operativo 10:08 UTC — 29 validado y feedback real actualizado

Confirm20 continúa (3.200episodios previstos);21–29esperan en secuencia.
No duplicar ni reiniciar runners.29:48desarrollos/noop8.628/max331ms, los
cuatro brazos activos6/6,368compras/cierres y13.720unidades exactas. Conservan
trabajo/cosechas/pérdidas/tiendas en esta cuadrícula, cero escapes; sin cambios
W/L/T. Dos fuentesVQ nuevas y dos top3reutilizadas;99variantes más2prototipos.
Ver REVENTA_DOS_PADRES y preregistro29. Piloto1.568después de28, sin autoenvío.

API10:02:07UTC:VQ2295,1/98episodios listados;top32135,7/88, COMPLETE. Siete
replays nuevos reproducidos719acciones/720estados/caja, max214ms, cero errores
observados/escapes/productos terminales propios. Alternativas contra rival
fijo: top3mejora cinco márgenes, empeora dos; Farmerjay851→−340. Esto no mide
respuesta reactiva ni fuerza poblacional. Leer FEEDBACK_1003; ninguna nueva
submission. Las verificaciones de28/29y los diagnósticos están cerrados.


## Corte operativo 10:01 UTC — confirm20 activa, 28 validado, 29 en desarrollo

Pilot20 cerró1.920episodios/noop448: los tres tamaños+3,125pp, intervalos
cruzan0, cuatro celdas mejores en tres semillas. Town20/50 seleccionadas por
regla previa; confirm20 corre3.200juegos. No consultar deltas parciales ni
reiniciar.21–28esperan en secuencia;28ya verificó sus fuentes congeladas.

Auditoría20:12partidas exactas,150compras/cierres y7.722unidades conciliadas.
Town20/50 conservan alimento/cosechas en los tres casos; town80pierde dos
huevos en1049013. Los efectos sobre ventas nativas/rival impiden identificar
todo el margen como beneficio aislado. Leer REVENTA_TOWN.

Loop28: cuatro máscaras de evidencia negativa sobreVQ/top3;48desarrollos,
noop8.628, max407ms,86.160checks y40.306pares floorobservables físicamente
verificados. Todas activas; cero cambiosW/L/T. En mundoNiA, VQproduce una lana
más pero empeora margen. No se combina arreglo27. Piloto1.568tras27; informe
CENSURA_FORECAST y preregistro28.99variantes construidas más2prototipos17:
las dos últimas son reventasVQ del loop29, todavía SIN validación/cola.

Loop29 preinscrito antes de construir: factorial padresVQ/top3 × tamaños20/50,
48desarrollos frente aV7corriendo; reutiliza fuentes top3exactas de20. Panel
cercano y ambas referencias reales, no cambiar confirm20 ni sumar N. Leer
preregistro29. Catálogo público09:49:34UTC:50entradas sin cambios vs09:01.
Último snapshot de ladder sigue09:13UTC; sin nueva consulta ni envío.



## Actualización 09:36 UTC —27aprobado para piloto

72desarrollos, noop17.256turnos y120.792cantidades propias exactas, max404ms.
Primero falló coberturaVQ(0/8contraV7); adenda previa+24contra mirrorTop3activa
6/8celdas, tres mundos. Top3activa2/8en original. Noop/campo/cosecha/tiendas/
pérdidas preservados, cero escapes/productos terminales.64eventos falsos de
padres→0en candidatas; persisten omisiones por mínimo. Márgenes de desarrollo
peores donde cambia acción; W/L/Tiguales. No adoptar por arreglo de medición.
Runner27en espera tras26, piloto960, gates intactos.93variantes más2prototipos.
Ver ATRIBUCION_VENTAS y adenda; usar verificar_cobertura_atribucion_ventas.py.

Actualización09:28UTC: confirm19_fixedhash0cerrada/noop832, ambasdelta0,
seis trayectorias propias distintas en tres semillas, todas ya ganadas; no
selección.20corriendo y21–26en cola. No repetir.27en desarrollo: sincronizar
_V9_RACE.prev.own/left con las órdenes finales, porque65desajustes en seis
replays contaminaron observaciones rivales. No cambia biblioteca/umbrales ni
resuelve ventas al mínimo. Preregistro27,48desarrollos antes de encolar.

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
`continuar_loop_adelanto_trigo.py`, `continuar_loop_panel_cercano.py` y
`continuar_loop_semillas_tardias.py` y
`continuar_loop_atribucion_ventas.py` y `continuar_loop_censura_forecast.py` y
`continuar_loop_reventa_dos_padres.py` y `continuar_loop_apertura12.py` encadenan bloques
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
3.200juegos/bothyfront. **Actualización08:44UTC:confirm19original quedó inválido
por cuatro hashes rivales noop; misma caja/acciones propias.48reproducciones
localizan sorted(set)sin desempate y estados económicos idénticos. Corre
`recuperar_confirm19.py` → `confirm19_fixedhash0`, misma muestra/gates, runtime0.
No reiniciar runner19viejo ni relajar controles.20–25waiters reiniciados una vez
tras verificar salida de todos, con logs `_fixedhash_0843.log`.**
Leer `docs/research/REPARACION_HASH_RUNTIME_2026-09-25.md`.
Loop25congela cinco fuentes existentes
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

Loop26valida semillasWHEATpor cultivo/reposición:40juegos/noop5.752,
76compras aceptadas, conserva campo y producción en cuatro mundos. Ahorro
0–20sin cambiosW/L/T; no adoptar por dinero. En cola tras25,960piloto, padres
VQy top3control; no repetir una guarda terminal genérica porqueE402ya existe.
91variantes competitivas más2prototipos detenidos. Leer informe/preregistro26.

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
