# Estado de investigación — leer primero para continuar

## Loop activo desde 2026-09-25 01:02 UTC

El usuario pidió explícitamente seguir investigando y probando en un **loop
continuo**, sin detenerse al cerrar una ronda. Objetivo persistente activo.

- Loop1: ocho variantes sobre VQ, producción/forecast, 1.000 episodios completos.
  PROMISING: pred_top3 +9,375 pp; pred_fast2 +3,125. Ambas a confirmación.
  Protocolo `PREREG_LOOP1_2026-09-25.md`; semilla 995000–995003.
- Loop2: recuperación de siembras + inversión en tomates, cinco variantes,
  616 episodios completos; ninguna señal agregada positiva. Reparaciones
  y dos variantes de tomate no se activaron en estas cuatro semillas.
  Protocolo `PREREG_LOOP2_2026-09-25.md`; semilla 998000–998003.
- `continuar_loop_publicos.py` encadena esos pilotos, verifica controles,
  selecciona según reglas fijadas y ejecuta confirmaciones disjuntas. Usa
  `torneo.py` y `pareado_torneo.py`; no es otro harness. NO subir automáticamente.
- **Confirm1 completa**, 1.600 episodios, noop416/416, cero errores. Top3
  **+10,795 pp**, IC95 dos vías [−0,115;21,706], cumple gate de prueba real;
  fast2 +2,841 pp, no cumple gate. Top3 máximo757ms, mecanismo de mejora y
  única celda de daño reproducidos. Decisión en `DECISION_ENVIO_TOP3_2026-09-25.md`.
- Loop3 completo: 504 episodios; herd_future −84,375 pp, EV600 −34,375,
  EV1500 0 (inerte), EV_future −40,625. No seleccionadas, sin confirmación.
  Noop96/96, cero errores. Sonda para explicar el gran daño de herd_future.
- Loop4 completo: 384 episodios, noop128/128; recover_now cambia una de64
  partidas, +1,5625pp, IC95 semilla [−1,62;4,75]. Sólo una semilla positiva;
  no pasa gate de dos. INCONCLUSIVE, no envío. No sumar el caso dirigido previo.
- Piloto loop5 completo: 616 episodios, noop104/104, cero errores. Early12_9k
  inerte; early12/14/16_6k −18,75pp, late18_6k +3,125pp. Sólo seed1005002
  activa cambios. **Confirm5 completa**: late18_6k −21,591pp, IC95 dos vías
  [−36,90;−6,28], 1.152 episodios, noop384/384, cero errores. REJECTED.
  Cambió156/352 partidas; ninguna celda mejor y38 peores. No enviar.
- Loop6 completo:736 episodios, noop112/112, cero errores. EGG/MELON/ambos
  delta0; EGG cambia46/64 acciones y MELON es inerte. Top3+fast2 −6,25pp.
  Ninguna seleccionada. Controles factoriales: VQ78,125%, fast2 70,313%,
  top3 96,875%, combinado90,625%. No asumir suma de efectos de rondas previas.
- Loop7 completo: cuatro políticas de tomates en suelo SE libre, 4/8
  plantas d16/d18, sobre top3. V2 podía inhibir R51; v3 corrigió contratación
  pero perdió cuatro tomates por overflow. V4 separa riego/cosecha:16 diagnósticos
  completos, plantas y ventas16/32 confirmadas, R51 y ovejas conservados.
  Piloto1.248 completo, noop256/256. D16 inertes; d18 +1,5625pp cada una,
  IC dos vías[−3,41;6,54], cambia16/128 partidas en dos semillas.
  **Confirm7 completa**:1.600 episodios, noop416/416, cero errores. Ambas
  d18 inertes en352/352 partidas del pool; delta0, IC dos vías indefinido.
  INCONCLUSIVE_NOT_SELECTED: no prueba de beneficio, no envío.
- Loop8: seis variantes de patrones (rank5/7, historia120/360,
  ajuste por producto y desfase temporal). Validación16 juegos completa,
  noop1.438 acciones idénticas, cero errores, máximo271ms. Piloto1.472
  completo:1.472 episodios, noop224/224, cero errores. History360, phase2 y
  rank5 +1,5625pp cada uno (una celda mejor); rank7−3,125, history120−10,9375,
  product3−1,5625. Desempate registrado selecciona history360/phase2.
  **Confirm8 completa**:1.600 episodios, noop416/416, cero errores.
  History360+2,8409pp, IC dos vías[−1,249;6,931], debajo del gate3; PROMISING
  sin envío. Phase2−3,4091pp, IC[−13,23;6,412], inconcluso sin selección.
- Loop9 completo: seis rebaños incrementales (2/3/6 ovejas, día12/14),
  sin comprar tierra y con demanda YARN ya visible. Se validan22 partidas
  dirigidas por versión antes de encolar1.920. V2 corrige cosechas tardías;
  motor confirmó36/53/83 entregas completas en ambos asientos. **V3** incluye
  seis ovejas compradas pero aún sin colocar y lana privada en la proyección.
  Otros22 juegos válidos, forzadas byte de acciones/rewards idéntico a v2;
  seis variantes normales inertes en ese mundo. Manifiesto v3 actualizado
  antes del piloto9. **1.920 completos**, noop320/320, cero errores; las seis
  inertes128/128contra pool, acciones propias/rivales idénticas, delta0 e IC
  dos vías indefinido. Sin selección/confirmación. Total42variantes competitivas.
- Loop10 piloto completo: adelantar conversión COW→SHEEP a días3–7,
  fuera de la regla8–11 ya existente. Seis políticas de fecha/demanda/caja.
 48 juegos dirigidos, noop4.314 turnos exactos, max284ms. En mundo YARN/YARN:
  dos compras/colocaciones aceptadas,49 lanas cosechadas, cero escapes/créditos
  pendientes/inventario final. En dos mundos sin YARN temprano son inertes.
  Piloto1.920 válido, noop320/320, cero errores: y2_m100 +2,34375pp (ambas
  fechas), y1_m100 −8,59375pp, y1_m500 −2,34375pp. D3/D6 tienen acciones y
  rewards idénticos128/128por pareja: no son réplicas independientes.
  **Confirm10 completa**,1.600episodios nuevos1019000–015, noop416/416,
  cero errores. Ambas y2 inertes352/352contra pool; delta0, ICdos vías indefinido.
  INCONCLUSIVE_NOT_SELECTED, sin envío. No refuta beneficio en contextos ausentes.
  Auditoría del daño y1:200monedas extra impiden compra de trigo191 (7→0),
  fallan alimentaciones y escapan tres vacas239; base0. No atribuirlo sólo
  a precios de lana. Próxima hipótesis: reservar insumos futuros antes del swap.
  Y2 sólo actúa en una de16semillas; cobertura rara limita inferencia/gate global.
- Biblioteca auditada:2.398 streams,64/64 pares de tiendas,24–63 por par.
  Doce streams recientes de ventas aceptadas son nuevos por fingerprint; no
  agregan pares de tiendas. Fecha de biblioteca original desconocida (ids−1).
  Loop11 ahora valida tres bibliotecas (DSM4, ladder8, todas12):20juegos,
  noop2.876turnos exactos, max250ms; ladder/all sí seleccionan un stream nuevo.
  Piloto1.920 con32semillas1021000–031, luego confirmación de32semillas;
  **Piloto11 corriendo desde05:11:34UTC**. No mezclar con history360 aún no promovida.
- Loop12 validado/encolado: tres aperturas nativas sobre top3 y MarketShock
  público con entrada corregida.12juegos, noop1.438turnos, max229ms; tomate
  inicial produjo4unidades y sustituye una vaca. Trigo temporal de base/cycle
  se cosecha en87, distinto al contador heredado que esperaba53. MarketShock
  tiene un escape tardío de ganso; no se oculta.1.008episodios, semillas1025000–007,
  después de loop11. Total55variantes competitivas construidas en este loop.
- Loop13 validado/encolado: cuatro ventas preventivas de excedente WHEAT/FERTILIZER
  con reservas1/2días. V1 inválida por omitir VQ al capturar entrada antigua;
  fuente/evidencia conservadas. **V2**36juegos completos, noop4.314turnos,
 22activaciones con vector final/pérdida exactos del motor, max291ms,
  cero errores/escapes/diferencias en animales sin alimentar al cierre.
  Piloto1.248 después de loop12, semillas1028000–015. Total59variantes construidas.
  Motivación: c0nrad nos ganó con menos movimiento/jornales y se verificaron
  33unidades propias perdidas en cinco descargas nocturnas; rival0. Guardas ya
  existentes no lo solucionan conservando el vector final. JSON aislado cambia
  orden de bolsas y da predicción falsa en527; reconstrucción viva sí coincide
  con motor en5/5. Ver feedback y `c0nrad_*_audit.json`.
  En mundo dirigido1272457736 contra arshs3 reactivo, reserva1día reduce
  pérdida27→8, reserva2días27→20; quedan pérdidas residuales. En1004000
  brazo2días inerte;1027000 permite diferenciar trigo/fertilizante. No es W/L OOS.
- Loop14 validado/encolado: cuatro reglas de valor del alimento, multiplicador
  0,5/2,5, conservar FEED ovino o conservar todo FEED nativo.36juegos, noop4.314,
  máximo271ms, cero errores/escapes/inventario final; todas cambian acciones
  en tres mundos, consumo de trigo y producción confirmados por motor.
  Piloto1.248 semillas1031000–015 tras loop13. Total63variantes competitivas.
  Auditoría previa de8replays top3: PASS no implica trabajo útil pendiente;
  ningún CARE útil omitido entre esas oportunidades y60huecos WATER sin
  efecto inmediato/próximo amanecer ni muerte evitada esa noche.261huecos
  FEED motivan ablar filtro económico, sin asumir que todos fueran errores.
- Loop15 validado/encolado: cuatro reservas de caja antes de sustituir vacas,
  alimento hasta cierre/24/48h o todas las obligaciones24h.42juegos válidos,
  noop4.314, max294ms. En caso adverso:night permite una oveja, compra4trigos
  y evita tres escapes; resto conserva base. En caso solvente:night/24permiten
  dos ovejas,48/all24inertes. No seleccionar por esos rewards. Piloto1.568
  con control antiguo, semillas1034000–015 tras14. Total67variantes construidas.
- Fuentes públicas nuevas: MasterEngine actualizado es tds25 byte exacto,
  excluido. MarketShock12ad317e diferente; loader elegía instalador. Corrección
  de entrada1c94b979 probada idéntica al `module.agent` del autor en8juegos.
  Fuente/adaptación separadas en `FUENTES_PUBLICAS_0400_2026-09-25.md`.
- Auditoría piloto7: cuatro filas TDS con acción propia idéntica y hash rival
  distinto, pero rewards/WLT idénticos. Ocho reproducciones (hashseeds0–3)
  dieron acciones/estados idénticos; origen de la variación neutral no resuelto.
  No afecta selección observada ni justifica afirmar determinismo universal.
- Scorecards actualizadas: `SCORECARDS_LOOP_2026-09-25.md`.
- Estado máquina: `docs/evidencia/loop_publicos_20260925/pipeline_state.json`.
  Logs: `results/loop_publicos_20260925_pipeline.log` y los logs de cada bloque.
  No modificar `torneo.py`, ni agentes de un bloque mientras corre. No lanzar
  otro torneo de ocho workers mientras el pipeline ocupe el equipo.
- Sonda nueva: falta una fresa tras DIG por maleza en replay 113061732. Reparación
  con reintento entre trabajadores no actúa por falta de riego el mismo día;
  inserción en un sufijo con turno final redundante sí recupera planta. Cambia
  tiendas/RNG, así que la sonda frente a replay NO mide ganancia competitiva.

Sonda posterior en bucle cerrado (mismo seed del fallo, ambos asientos, rival
arshs3 reactivo): reparación inerte en asiento 0; recupera planta y −671→+53 en
asiento 1, con tiendas diferentes. Caso dirigido, no estimación poblacional.
La prueba de cobertura quedó registrada y encolada como loop4.

Líder actual consultado 01:36 UTC: DSM 3128,7, submission 56518845. Cuatro replays
recientes reproducidos exactamente; compra cuarta tierra día 10 y cultiva más
tomates, con diferencias grandes de composición por mundo. No inferir causalidad
ni algoritmo del score. Informe: `LIDER_Y_FUENTES_2026-09-25.md`. Dos notebooks
con nombre nuevo eran copias de tds25: se deduplicaron sin repetir torneo.

Snapshot histórico01:52UTC: VQ56535264 **2319,5 /24 episodios listados**, original
56511619 **2275,7**. VQ aún joven, no afirmar superioridad por este rating.
Top3 **56537205 COMPLETE**, enviada 2026-09-25 01:56:34 UTC, commit ba1fda8,
sha9668e30a byte exacto de confirmación. Validación113099118: 720 pasos,
DONE/DONE, cero errores/timeouts. Recibo confirma tres envíos restantes.
Desplaza al original y conserva VQ, su padre, como control. Snapshot02:04UTC:
VQ2364,6 y top3 729,5 inicial. Snapshot02:33UTC: VQ2306,3 y top3 1459,1;
top3 tiene10 episodios listados02:34, incluida validación. Cuatro replays
por recencia:3V/1D, cero escapes propios, inventario terminal0 y cero errores
fatales. Derrota contra c0nrad−23.180: rival32 ovejas frente a17, casi sin tomate.
Cuatro reproducciones exactas y caja conciliada. Lana391/759 unidades,
ingresos69.502/113.264; rival paga menos jornales y tierra. Ver
`FEEDBACK_TOP3_2026-09-25.md`. Muestra pequeña, no WR ni fuerza estable.
Snapshot posterior02:58UTC: top3 1738,5 / VQ2268,6, sin recuento nuevo sincronizado.
Snapshot **03:39:41UTC**: top3 **1941,6 /30 episodios listados**, VQ
**2259,1 /56**, ambos COMPLETE; recuentos incluyen validación. Cuatro nuevas
partidas seleccionadas por endTime antes de leer rewards:4V, márgenes923–2891.
720 estados exactos×4, caja conciliada, cero escapes propios/inventario final.
Producción muy similar a rivales en esa muestra; no es superioridad causal vsVQ.
Archivos con sufijo0333 se consultaron03:39; metadatos `.fetch.json` dan hora real.
Snapshot **04:30:35UTC**:top3 **2022,5 /46episodios listados** y VQ
**2288,2 /69**, ambas COMPLETE. Archivos sufijo0431; hora real en metadatos.
Último snapshot **05:13:31UTC**:top3 **2068,8 /58episodios listados** y VQ
**2287,2 /81**, ambas COMPLETE. Archivos sufijo0515; hora real en metadatos.
Recuentos incluyen validación; ninguna submission nueva desde top3.
Cuatro replays nuevos por recencia0515:4V,márgenes240–1.480,720estados exactos
y caja conciliada cada uno; cero escapes propios/stock terminal. Originales
archivados. No estima WR global ni ventaja causal sobre VQ; ver FEEDBACK_TOP3.

Lo siguiente es el cierre de la ronda anterior; no significa parar este loop.

## Estado vigente — 2026-09-25 UTC / 2026-09-24 America/Bogota

Esta sección sustituye los planes y estados «en curso» históricos de abajo.
Consulta API archivada en `docs/evidencia/research_20260925/`:

| Agente | Submission | Score observado | Episodios | Estado |
|---|---:|---:|---:|---|
| arshs3 público original | 56511619 | 2292,5 | 148 | Mejor referencia real, activa |
| v13 público | 56511611 | 1857,9 | 136 | Desplazada por VQ |
| arshs3 + VQ | 56535264 | 810 inicial | sin actualizar | REAL_WORLD_CANDIDATE, COMPLETE |

VQ se envió desde `submission/main_publico_arshs3_vq.py`, commit a9f59ee,
sha 9b463dfb, usando la evidencia ya existente (40-0 espejo y otros bloques,
0 cambios W/L/T en el pool). No se repitió el barrido VQ ni ADV. La CLI confirmó
4 envíos restantes tras subirla. Arshs3 original queda activa para comparar;
otro envío desplazaría a esa referencia. `submission/main.py` aún es el original;
el archivo efectivamente enviado está identificado en SUBMISSION_HISTORY.

**Hallazgos nuevos:** muestra fija por recencia, 16 partidas arshs3 y 8 v13,
sin seleccionar por resultado. Arshs3 4V/11D/1E, cero escapes, inventario terminal
propio cero. No es su WR histórico. Cuatro partidas se usan para diagnosticar
el predictor: la primera sonda contó 12/67 coincidencias, pero omitía ventas
simultáneas. **CORRECCIÓN:** cuatro reproducciones exactas con ledger dan 50/67
en t..t+4, 42 en el mismo turno. Una acción reconstruida del agente difiere de
la real (SELL WHEAT en step 623); el ledger se validó contra las acciones reales,
sin esa discrepancia. No atribuir causalidad a cada coincidencia.

**TERMINADO:** `forecast_pilot` (608 episodios), noop exacto 160/160. Gate
**−51,56** puntos (IC dos vías [−78,92; −24,20]); off **−68,75**
([−89,57; −47,93]). REJECTED ambos; no se ejecuta confirmación ni se suben.
Sonda causal de fallo: primeras acciones distintas step 440, mismas cantidades
totales vendidas, peor timing y +89 monedas pasa a −78. Protocolo inalterado:
`PREREG_FORECAST_GATE_2026-09-25.md`; resultados `forecast_results.json`.

**TERMINADO:** `public_refresh` (608 episodios), noop exacto 160/160.
Las versiones nuevas tds25 / hl25 (sha 127ed3e6 / 1dfd4630) obtienen **−7,81**
y **−9,38** puntos vs VQ. IC dos vías [−27,29; +11,67] y [−29,79; +11,04]:
inconcluso, sin señal agregada de mejora; ninguna cumple el criterio registrado.
No se ejecuta confirmación ni otro envío. No rescatar tds25 por su 10/16 en directo.
Protocolo `PREREG_PUBLIC_REFRESH_2026-09-25.md`; `public_refresh_results.json`.

**Cierre de esta ronda:** 1.216 partidas de torneo + ocho diagnósticas; todos
los procesos terminaron. Consulta final: original 2288,6; VQ 1198,5 con apenas
media hora de vida, sin actualizar episodios. No compararlos por ese rating.
El informe completo es [RESULTADOS_2026-09-25.md](RESULTADOS_2026-09-25.md).
Siguiente frontera: aprender de pérdidas actuales y separar producción de precios
realmente ejecutados; preservar el predictor y dejar que VQ reúna evidencia real.
No hay monitoreo automático programado ni candidato nuevo pendiente de envío.

Se endureció el mismo `torneo.py`: no sobrescribir, abortar ante inválidos o
cambios de fuentes, comprobar cobertura, archivar fuentes y capturar acciones
antes del motor. La sonda comparó el wrapper con el loader oficial: 1.438 acciones
y rewards idénticos (dos episodios). No usar `pareado_torneo.py` sin comprobar
antes que el bloque está completo y que cada celda contiene ambos asientos.

La autorización autónoma de investigación y submissions continúa. No hay una
aprobación pendiente para los agentes públicos ya enviados. Las restricciones
anteriores y las listas de procesos de septiembre 21–24 se conservan abajo sólo
como historial; no relanzar sus comandos por leerlos aquí.

## Historial previo a esta revisión

Actualizado: 2026-09-23 20:45 (America/Bogota) = 2026-09-24 01:45 UTC. Deadline 2026-09-30 23:59 UTC.
Loop autónomo autorizado por el usuario (mensaje del 2026-09-21): harness + ladder
como evidencia complementaria, submissions como instrumento (5/día).

## ⚠️ PIVOTE 2026-09-24: el techo real está en los agentes PÚBLICOS

**Leaderboard 2026-09-24 01:02 UTC (9.937 equipos):** #1 3057 · #10 2921 · #100 2715 ·
#500 2499 · #1000 2308 · #2000 1807 · **nosotros ~1160 = puesto ~3.500**.
280 equipos ≥ 2600, 1.635 ≥ 2000.

**Causa:** existe un ecosistema de agentes públicos Apache-2.0 (Code tab) —
cintas de ruta (yhay81) + router por tiendas + capas reactivas (Ahmed Berat Özer
V25-V48, Thomas Tschinkel v9/4 y v13, familia Herd-Safe de Dmitrii Gluzdov /
arsgorynich, haideptry...)— que puntúan 2500-2950 en el ladder. El de Thomas
(v9/4, sub 56269928) documenta **2944,7 con 201 partidas**. Desde el 2026-09-02
no volvimos a medirnos contra ellos: optimizamos dentro de una familia débil.

**Torneo en bucle cerrado** (`torneo.py`, motor oficial 1.32.7, cargados como Kaggle
= último callable, 10 semillas 910000-009 × 2 asientos, 720 partidas, 0 errores,
máx 215 ms/turno). Evidencia: `docs/evidencia/torneo_publicos/torneo_rr1.*`.

| agente | origen | % vs resto | nota |
|---|---|---|---|
| **arshs3** | arsgorynich, Herd-Safe v3 forecast4 | **98,8%** | gana a TODOS (ars40 18-2, resto 20-0) |
| ars40 | arsgorynich, More Wheat v11 | 81,2% | |
| hsov | haideptry, Shepherds Ledger herd-safe | 76,2% | |
| h2965 | haideptry, 2965 Master Hybrid (V59) | 67,5% | |
| guru6 | guruprasaathas111, Master Engine V6 | 47,5% | |
| v13 | Thomas Tschinkel, Metav4 v13 | 41,2% | gana a v94 20-0 |
| v94 | Thomas Tschinkel, 2945 Farm (ladder 2944,7) | 25,0% | pierde con toda la familia Herd-Safe |
| seek+gcal | nuestra activa 56507746 | 8,8% | pierde 0-20 con CADA público, −$12..16k |
| decem+gcal | nuestra activa 56507747 | 3,8% | idem |

**Rondas 2 y 3** (`torneo_rr2`, `torneo_rr3`; seeds 920000-009 y 930000-009;
560+560 partidas, 0 errores, máx 291 ms/turno; límite de Kaggle 1 s + reserva):

| agente | rr2 % | rr3 % | directo vs arshs3 |
|---|---|---|---|
| arshs3 | 82,9 | 77,1 | — (**invicto: 22/22 cruces en las 3 rondas**) |
| tds (tetsutani, demand-preserving, 22-sep) | 72,9 | 78,6 | 8-12 / 7-13 (margen −$10..−$14) |
| hl59 (haodou092, Harvest Ledger V59) | — | 78,6 | 7-13 (≈ tds: 14 empates de 20) |
| hybu (wzhengbiao) | — | 53,6 | 8-12 |
| ars40 ≈ dmw (More Wheat) | 50,7 | — | 6-14 |
| wz15, lp16, obr, ob3, hsov≈hs2700≈st25, bv48 | 26-44 | 5-44 | 1-19 .. 7-13 |

Entre los públicos top los márgenes medios son de decenas de dólares sobre ~$115k:
las partidas se deciden en el margen.

**Activas desde 2026-09-24 04:28 UTC:** 56511611 (v13) y **56511619 (arshs3)**.
v13 se mantiene a propósito como segunda familia: su rating frente al de arshs3
mide si el bucle cerrado intra-público transfiere al ladder.

**Experimentos de capas sobre arshs3 (2026-09-24):**
- **VQ** (compactación de cola, tetsutani): contra el pool 0/120 celdas cambian
  (+$20/partida, mínimo −$6) → inerte en W/L; en ESPEJO gana 17-3, 40-0 (20
  semillas nuevas) y 95% (tercer bloque). `hsov2` (haideptry, 24-sep) ya es copia
  de arshs3: las copias circulan. **REAL_WORLD_CANDIDATE: arshs3vq** (sha 9b463dfb,
  `results/exp_publicos/arshs3_vq.py`, construido con `apilar_capa_vq.py` @e43ce1d).
- **ADV** (adelanto de ventas, Ahmed EXP293): descubrimiento +10 [−10; +30],
  confirmación −2,1 [−20; +16] → **REJECTED**. Intercambia partidas entre linajes.
- Derrotas de arshs3: mediana $521 (p25 $257, p75 $1.147); sólo 7/95 < $100.
  Micro-capas de final de partida no las voltean.

**Plan de envíos (día UTC 2026-09-25; hoy queda 1 envío sin usar a propósito):**
v13 y arshs3 juntan ~18 h de ladder = prueba de transferencia bucle cerrado →
ladder (predicción: arshs3 ≫ v13; 20-0 local). Luego: (1) subir arshs3vq, (2)
subir la segunda según esa lectura (v13 si transfiere mal; si no, tds o hl59,
el otro linaje top). El envío nuevo siempre desplaza al activo MÁS ANTIGUO.

Ficheros auditados estáticamente (sólo stdlib; `exec` de cadenas constantes sin
imports peligrosos; `open` sólo tras una variable de entorno de desarrollo o
`path=None`). Código en `results/publicos/` (gitignored; hashes en el meta).

**Decisión pendiente del usuario:** subir agentes públicos (código de terceros,
Apache-2.0). Propuesta: arshs3 (campeón en bucle cerrado) + v13 (rama distinta,
autor con el mejor registro de ladder documentado). Las cintas propias quedan
superadas por ~+1.500 Elo esperados.

**Limitaciones:** el torneo es intra-familia (forks emparentados); no mide contra
los top-10 adaptativos (mtmr_s1, feel the agi, DeeperNet), que según Thomas
abandonan la cinta en d12-18 y le ganaron 36-0 a v9/4. Ranking en ladder entre
públicos: incierto (±100 de ruido por submission según Thomas).

## BEST_CURRENT_CHAMPION (hasta el 2026-09-23; historia)

**CHAMPION_CANDIDATE: `107570947 + guardias`** — 56449108, commit 6527d3a,
**1.180 @24 ep, 15-9 (62%)**, 24/24 con 4 manos y 3 cuadrantes, derrotas ajustadas.
Paquete: `submission/main_107570947_guard.py` (= `submission/main.py`).
Segunda: `tree_v1+guardias` 56447472, 1.136 @40 (23-17). Ambas activas.
Champion formal anterior: `maj_107674293` (56245770, 857, 126 ep) — superada.

**Escalera de ratings a episodios comparables:** cinta 857 (126) · tree_v1 1082 (40) ·
tree_v1+g 1136 (40) · **107570947+g 1180 (24)**.

**Panel FUERTE (80 rivales de Majkel/DSM), la métrica que predice el ladder:**
guard:107570947 54,8% · 107570947 36,3% · guard:tree_v3 29,5% · tree 20,2% ·
cinta campeona 17,4% · HOZ 9,5%. **Las guardias valen +15-18 vs fuertes.**

## RESEARCH_FRONTIER (estados)

| id | qué | estado | evidencia |
|---|---|---|---|
| `maj+guard6` | cinta campeona + guardia de caja d0 | **VALIDADO en ladder** — 56444505: 32/32 con 4 manos, 17-15 (53%) vs 40% | rating 714 @32 es dinámica de arranque, no rendimiento |
| `tree_v1` | árbol 4 cintas Majkel, ramas por tienda d3/d6 | **CHAMPION_CANDIDATE** — 56444202: 31-9 (78%), 1082 @40 | local +6..+9 global pero **+10 vs fuertes**; ladder confirma |
| `tree_v1+guardias` | lo anterior + guard_cash + guard_commitments | **REAL_WORLD_CANDIDATE** — sub **56447472** (2026-09-22 03:10) | combinación de validados (#6); 8/9 derrotas del tree eran manos d1 |
| `107570947` (cinta sola) | mejor cinta del successive halving | **PROMISING** | compare2: +13,1 global; **+21,5 vs fuertes [5,7; 37,3]**, −0,6 vs débiles. Panel fuerte en curso |
| `tree_v2` | árbol 30 victorias Majkel, NN sobre tiendas | **PROMISING→REJECTED como está**: +4,8 [−5,0; +14,7], < v1 < cinta | defecto: cambia entre cintas con prefijos distintos (12 prefijos) → estado inconsistente al ramificar. Arreglable: ramificar sólo entre cintas con prefijo idéntico |
| `mejor cinta sola` | successive halving sobre 30 victorias como cintas fijas | **EN CURSO** — piloto `tapes` 4 seeds (4.096 ep) | compare dice cinta sola > árboles localmente |
| `tree_v3` | árbol con cintas de DSM/UMG/Vadim (top-3, 2850-2880) | **PENDIENTE** — replays bajando | — |
| `tree_liquid` | árbol + ventas reactivas | PROMISING (empató con tree en piloto, 0 cambios de W/L/T) | no confirmar solo |
| `warmstart10` | cinta hasta d10 + HOZ | PROMISING débil (+6,25 piloto, < cinta pura) | baja prioridad |
| matching por contexto (rival/hierbas) | elegir cinta por más que la tienda | idea, no implementada | LOW confidence |

## REJECTED (resumen; detalle en RESEARCH_BELIEFS.md y BITACORA.md)

Todo el espacio de perillas del chasis (13 barridos), gansos, ventas retenidas,
fertilizar un corte, superficie, rebaño, plantilla, copiar por piezas, cadencia,
compete_aware, compra parcial, harvest_76, apertura dentro del planner.

## REGLA REFORZADA (violada dos veces hoy)

**`evaluar_lider.py` hashea sus fuentes (evaluar_lider.py, chassis, arquetipos,
tape.py, arbol_lider*.py, guardia_cinta.py, clasif json) al inicio y al final.
NO editar NINGUNO mientras una fase corre.** Preparar ediciones en el scratchpad
y aplicarlas al terminar. Si se edita por error: `git checkout <fichero>` antes de
que termine (funcionó el 2026-09-22 05:05).

## PROCESOS EN CURSO (al escribir esto)

- `evaluar_lider.py --phase majkel2 --seeds 4` → `results/majkel2.txt`: 12 cintas de
  Majkel ACTUAL (vs top-3) + guardias, vs 71 fuertes sin Majkel. Referencia
  guard:107570947.
- **Pendiente de lanzar al terminar:** fase `dsm` (27 victorias de DSM, nº1 actual)
  — la edición está en `scratchpad/evaluar_lider_con_dsm.py`; copiar sobre
  `evaluar_lider.py` cuando `majkel2` termine.
- Terminados: compare, compare2, tapes, fuerte; descargas (DSM 40, UMG 30, VADIM 30,
  MAJTAPE_LADDER 60, TREE1_LADDER 40, GUARD_LADDER 32).

## HALLAZGOS DE HOY (resumen; detalle en RESEARCH_BELIEFS.md)

1. **Manos d1 → resultado** (60 reales): 0-2 manos 0%, 3: 23%, 4: 60%. Guardia
   `bots/guardia_cinta.py` reserve=6. Sólo d1 (d2 residual 3/60; d3+ ninguno).
2. **Divergencia harness/ladder**: 71,5% local vs 40% real. Cintas pasivas no
   mueven el mercado d0.
3. **Tienda d3 explica derrotas** de la cinta fija: 60% BAKERY … 14% PIZZA.
4. **DSM vs Majkel 3-6**; cima decidida por 1-5%. Cintas de DSM no son mejor materia.
5. **compare**: cinta +12,1 > tree +9,0 > tree_v2 +4,8 (vs HOZ). Más cintas mezcladas, peor.

## SESION 2026-09-23 — en curso

**Ladder @13:11:** 56449108 (107570947+g) **1.163,7** @78 ep; 56447472 (tree_v1+g)
1.131,6 @81 ep. Rank equipo **3.510 / 9.919**. Nuevo nº1: Boey (3.112).

**Fallo de método encontrado:** el evaluador aplicaba las guardias con
`reserve=6` fijo; 72 de 79 cintas necesitan \$7+ (5 HIRE al alba, usan 4).
Todas las comparaciones previas entre cintas con guardias se hicieron con la
guardia a medias. Nuevo prefijo `gcal:` con `reserve_auto` (da 8 para
107570947 = exactamente la submission). `guard:` se conserva para reproducir.

**En curso:**
- Piloto `cal1` (`results/cal1.txt`): 111 cintas (Majkel-2652 ×30, Majkel-3075
  ×12, DSM ×27, UMG ×21, Vadim ×21) con `gcal:`, vs 32 fuertes balanceados
  (8 por fuente) × 2 seeds × 2 asientos = 14.592 ep.
- Descargas (`results/bajar_ronda2.txt`): 25 replays de Boey (56309208),
  M&M&P&Q (56378284), DECEM (56446088), Majkel-nuevo (56407295), Vadim-nuevo
  (56427964), seek inspiration (56407833).

**Hecho:** `cal1` (111 cintas) → `confirm_cal1` vs 148 rivales NUEVOS (rivales
del top-13 actual). Ganadora confirmada: **`110304538` (Majkel-3075) + gcal:
+18,9 [−0,5; +38,4] vs 107570947+gcal, positiva vs las 6 fuentes → subida como
56504082** (17:30). La #1 del piloto (umg_111191811) se desplomó a −11,7.

**Activas en ladder:** 56449108 (107570947+g, 1.164) y 56504082 (110304538+gcal).
⚠️ La próxima submission desplaza a **56449108**: sólo subir si 56504082 ≥ 56449108
o si la candidata nueva supera a ambas.

**En curso:** piloto `cal2` (`results/cal2.txt`, centinela `results/cal2.done`):
93 cintas de Boey/MMPQ/DECEM/Majkel-nuevo/Vadim-nuevo/seek + anclas, vs 32
rivales de fuentes viejas no usados en cal1, 2 seeds. Filtro grueso → etapa 2
(~20 brazos, más celdas) → confirmación vs `results/rivales_reserva_confirm2.json`
(76 rivales nunca usados), siempre con `gcal:110304538` y `gcal:107570947` en el
mismo bloque.

**Herramientas nuevas:** `comparar_pareado.py` (delta pareado, IC semilla y dos
vías, desglose por fuente), `extraer_fuente.py` (victorias + rivales de una
carpeta), fase `spec` del evaluador (brazos/rivales/semillas desde JSON).
**Lección de infraestructura:** esperar por fichero centinela, nunca por
`pgrep -f` con un patrón que aparece en el propio comando del bucle.

## CIERRE DE SESION 2026-09-22 — decision: CONSOLIDAR (revisada el 23)

Todas las vias de mejora sobre la cinta estan medidas y cerradas:
- Mejor cinta fija: 107570947, de ~70 candidatas de Majkel-2652/Majkel-3075/DSM.
- Guardias (caja d0 + compromisos): +15-18 vs fuertes; 100% mecanicas en real.
- Arboles: peores que la cinta sola vs fuertes (tree_v3+g 29.5% vs 54.8%).
- Hibrido cinta+chasis: colapsa al nivel del chasis (10-17% vs 43%).
- Cierre limpio (0.6%), acciones fallidas ~1%, ocio 4.7% (+2-4% maximo).

**Champion: `107570947 + guardias` (56449108).** Dejar converger. Segundo billete:
`tree_v1 + guardias` (56447472). El score de equipo es el mejor submission.

## NEXT_EXPERIMENTS (si se retoma; orden)

1. Leer 56449108 y 56447472 a ~100 ep (rating convergido, W/L por rival).
2. Unica capa barata no probada: dar trabajo a los peones sin orden (4.7% de
   mano-turnos), p.ej. barrido de riego a partir de h18 y DIG de maleza. +2-4%
   estimado, riesgo de interferir con la cinta. Medir vs fuertes antes de subir.
3. Si el ladder converge por debajo de 1150: subir 107570947+g de nuevo como
   billete adicional NO es investigacion (misma esperanza, mas varianza del max).
   Solo si el usuario lo pide.

### (historial de la cola)

0. **Leer piloto `dsm`** (`results/dsm.txt`, 27 victorias de DSM nº1 + guardias vs
   62 fuertes, 4 seeds). Top-3 → `--phase` de confirmación pareada con 8 seeds
   contra guard:107570947 (añadir fase análoga a `majkel2_confirm`). Si alguna
   supera con IC dos vías > 0 → subir con guardias (reserve calibrada a sus
   HIRE del alba: ver `empaquetar_cinta_guard.py --reserve`).
1. Si DSM no supera: **el enfoque de cinta fija ha llegado a su techo** (~el plan
   de Majkel-2652). Opciones: (a) consolidar 107570947+g y dejarlo converger;
   (b) subir 2-3 cintas top en paralelo (5/día) y dejar que el ladder elija;
   (c) capa reactiva — pero la evidencia dice que el gap con los fuertes es
   produccion tardía (+5-7% d21-25), no ventas.
2. `tree_v1+guardias` tiene 3/40 con 3 manos: sus cintas necesitan reserve=8.
   Sólo relevante si se vuelve a subir un árbol.
3. Leído majkel2 (hecho): ninguna cinta de Majkel-3075 > 107570947 (+1,85
   [−26; +30]). El valor de Majkel actual está en la adaptación, no la secuencia.

### (anteriores)

1. Leer piloto `tapes` → top-3 cintas a `--phase confirm` (16 seeds). Si alguna
   supera a 107674293 con IC dos vías > 0 → nueva cinta base (+guardia) al ladder.
2. Leer 56444505 (guardia) y 56444202 (tree v1) a ~60 ep → HARNESS_VS_LEADERBOARD.
   Predicción guardia: claramente > 852,6 si las manos d1 eran la causa dominante.
3. Si guardia transfiere Y tree v1 ≥ cinta en ladder → `tree_v1 + guard` (combinación
   de validados, criterio #6).
4. Arreglar `tree_v2`: ramificar sólo entre cintas con prefijo IDÉNTICO hasta el
   paso de ramificación (agrupar por hash de prefijo). Medir vs tree v1.
5. `tree_liquid` (ventas reactivas) al ladder si hay slot: 0 efecto local por
   rivales pasivos — mismo patrón de divergencia que la guardia.
6. Ampliar guardia al d1 (until_step=48) si 56444505 muestra déficit residual en d2.

## HARNESS_VS_LEADERBOARD (dataset acumulado)

| exp | local delta (vs HOZ) | ladder | transferencia |
|---|---|---|---|
| campeona_grano (seed_stock_aware) | +6,4 | 772 vs hoz 677 | ruido de ladder ±40; no concluyente |
| campeona_hoz (+harvest_76) | +2,5 (falso: −0,08) | 677–831 según fecha | ruido |
| **maj_107674293** | **+14,36** | **852,6** | **SÍ: salto grande transfiere** |
| tree_v1 | +17,97 (piloto) | pendiente | — |

Lección provisional: el ladder sólo resuelve saltos ≥ ~100 Elo; el harness sólo
efectos ≥ ~7 puntos. Buscar cambios GRANDES, no micro.

## HIGH_UPSIDE_HYPOTHESES

- **H1 (VERY HIGH / MEDIUM):** una cinta fija de un agente de 3075 rinde 852 → el
  valor está en la adaptación. Cuantas más cintas y mejor matching de contexto,
  más cerca del agente original. `tree_v2`/`tree_v3` prueban esto.
- **H2 (HIGH / LOW):** las cintas de los top-3 actuales (≈2870) son mejores
  materia prima que las de Majkel (sub a 2652).
- **H3 (HIGH / LOW):** el rival explota a la cinta de forma identificable en los
  replays reales (p. ej. inunda el producto que la cinta vende tarde). Si es así,
  una capa reactiva mínima (ventas) sobre la cinta lo corrige.
