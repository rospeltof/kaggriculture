# Estado actual — leer primero

> **Este archivo conserva el traspaso del 14-sep.** Para decisiones vigentes,
> leer [ESTADO_INVESTIGACION](research/ESTADO_INVESTIGACION.md): loop autónomo
> autorizado, referencia arshs3 56511619 y VQ 56535264. No relanzar ni bloquear
> trabajo por las autorizaciones históricas que siguen.

## Envío autorizado — 2026-09-14, 23:52 America/Bogota

El usuario pidió «Subela a kaggle pa que coja calle». Se envió **`maj_107674293`**
como `submission/main.py`, submission **56245770**. Kaggle confirmó recepción;
estado inicial **PENDING**, sin score todavía. La CLI indicó **4 envíos restantes**
después de subir. Esto sustituye la prohibición previa para este envío concreto;
no implica autorizar más submissions ni que el candidato haya ganado en el ladder.

El paquete de 13.506 bytes incluye la cinta y sólo usa biblioteca estándar.
SHA-256: `7894c015654e18803b7f31e2c2d37127accb143fce007cec6e2db519f997ca08`.
Se comprobaron 721 acciones, aislamiento frente a mutaciones y cuatro pares de
partidas archivo/módulo, con 720 estados de juego equivalentes por par (ocho
episodios adicionales, semillas 218000–218001 y ambos asientos).

El archivo anterior se conserva en
`submission/archivo/main_cfad10b88abc38f8f7f79a3b83148f11e37d57865f37cea648cffa9bbcf1e1d7.py`.
`CAMPEONA_HOZ` permanece intacta como referencia local. Evidencia del envío y
validación: `docs/evidencia/envio_maj_20260914/`. No volver a enviar por encontrar
un estado PENDING; consultar por ID y distinguirlo de un envío fallido.

Snapshot de consulta anterior al envío: HOZ **702,0**, grano **718,4**. Son
ratings observados en esta consulta, no los 818,1/774,8 del historial.
Los informes de experimentos de abajo conservan el estado previo a este envío.

## Ronda del líder — 2026-09-14

El usuario autorizó investigación pública, análisis de ocho replays nuevos de
Majkel1337 y experimentos locales ambiciosos. En esa fase no había autorización
de envío; fue concedida después, como se registra arriba.
**Resultado de confirmación:** `maj_107674293` obtiene 71,49% frente a 57,13%
de HOZ: **+14,36 puntos**, IC95 por semilla **[+9,02; +19,71]**, dos vías
**[+6,71; +22,02]**. Se completaron 7.296 episodios, 19 semillas nuevas y ambos
asientos. Noop exacto en 1.824 comparaciones; FB −19,35 puntos, con ambos
intervalos negativos. Hay mejora positiva en el panel fijo, pero el estimador
queda por debajo del umbral registrado de 15 puntos para declarar el salto.

El piloto comparó once candidatos y tres controles. La cinta y el árbol empataron
en 64,06%; se eligió la cinta por desempate alfabético registrado, no por ventaja
demostrada sobre el árbol. La variante de ventas cambió acciones sin cambiar
W/L/T frente al árbol. Contra los ocho rivales nuevos de confirmación, el candidato
queda en 48,68% frente a 37,50% de HOZ; no confundir 71,49% agregado con dominar
el meta actual. Duelo diagnóstico contra HOZ vivo: 12 victorias y 4 derrotas.

Estrés completo de 512 episodios contra las ocho cintas de Majkel: candidato
90,62%, HOZ 11,72%. Son fuentes de desarrollo y el control FB cruza cero;
este resultado no es confirmación independiente ni una victoria sobre su agente
reactivo. Total de la ronda: 9.634 episodios locales, incluidos los diagnósticos
y reproducciones. Los registros, controles y fuentes se verificaron al terminar.

`CAMPEONA_HOZ` continúa como base y `submission/main.py` conserva el hash anotado
abajo. El candidato queda experimental, sin empaquetar ni enviar.

- [Resultados y diagnósticos](RESULTADOS_LIDER_2026-09-14.md).
- [Auditoría de los ocho replays](ANALISIS_LIDER_2026-09-14.md).
- [Protocolo anterior a las pruebas](EXPERIMENTOS_ATREVIDOS_2026-09-14.md).
- [Petición preparada para otro LLM](REVISION_LIDER_PARA_LLM.md).

**Historial anterior:** lo que sigue conserva las decisiones de septiembre 5–6;
sus restricciones de barridos no describen la nueva petición. Los ratings son
snapshots antiguos, no una consulta actual. La investigación del 14 no consultó
submissions por CLI ni verificó la cuota de envíos.

Actualizado el 2026-09-05. Esta página resuelve contradicciones con notas antiguas;
las instrucciones nuevas del usuario prevalecen sobre cualquier documento.

## Decisión del usuario

**No subir nada a Kaggle por el momento.** El usuario indica que le queda una
corrida disponible y quiere reservarla. Ese cupo es información del usuario,
no una cuota verificada por API. El trabajo actual es preparar el traspaso y
revisar ideas; no se han autorizado más barridos ni envíos en este traspaso.

**No se envió ninguna submission en esta sesión.** Sólo se consultó la lista
de submissions. Se llegó a preparar un paquete experimental; luego se restauró
`submission/main.py` byte por byte al archivo anterior. Su SHA-256 es
`cfad10b88abc38f8f7f79a3b83148f11e37d57865f37cea648cffa9bbcf1e1d7`.

La copia experimental no enviada está sólo localmente en
`results/hoz_lotes_main_preparado_no_enviado.py`. No es el archivo de envío activo.

## Qué agente es cuál

| Nombre | Uso y estado |
|---|---|
| `CAMPEONA_HOZ` / `campeona_hoz` | Base actual; `seed_partial_batch` ausente y por tanto apagado |
| `HOZ_LOTES` / `hoz_lotes` | Copia de HOZ con `seed_partial_batch=True`; experimental, no aprobada |
| `CAMPEONA_FB` | Control anterior exacto en el experimento de compra parcial |
| `submission/main.py` | Paquete anterior restaurado; no asumir que refleja todos los cambios locales |

Última consulta CLI de esta sesión: `campeona_hoz` submission **55994874**, score
**818,1**; `campeona_grano` **55993562**, score **774,8**; ambas COMPLETE.
Son snapshots; no se verificó el rank actual ni el número actual de episodios.

## Hallazgo principal

`seed_partial_batch` reduce únicamente el tamaño del lote adaptativo hasta que
pase el mismo `_afford` con reserva de $100. Mantiene scorer, forraje y orden
de compras. Está implementado en `bots/chassis.py`; no se activó en la base.

| Evidencia | Resultado | Lo que permite concluir |
|---|---|---|
| Sonda 99000, una cinta, asiento 0 | Primer melón d6 h16 → d1 h18; primera fresa d8 h3 → d7 h19 | El mecanismo actúa en ese escenario |
| Descubrimiento, 4 semillas × 40 cintas × 2 asientos | Base 62,1875%, candidato 67,1875%; +5,0 puntos | Señal positiva para confirmar |
| Confirmación, 8 semillas nuevas, mismo panel | Base 60,0%, candidato 64,8438%; +4,8438 puntos | Señal repetida, incertidumbre aún demasiado amplia |
| IC95 de confirmación por semilla | [−0,67; +10,36] puntos; t=2,08 | Inconcluso según el criterio registrado |
| **Réplica, 16 semillas nuevas (103000–103015), 5.120 episodios** | **+0,23 puntos; t=+0,08 por semilla y a dos vías; ambos IC95 incluyen cero** | **REFUTADO. No adoptar; mecanismo cerrado** |

`noop` exacto en 1.280 episodios, `_peor` a −26,95 (t=−12,43) y el candidato
cambia acciones en 1.280/1.280: la bandera dispara y el panel discrimina. Es un
resultado nulo real. Ver [pre-registro](PREREGISTRO_REPLICA_LOTES.md).

**`harvest_76` REFUTADO (2026-09-05).** Ablación con 16 semillas nuevas
(104000–104015): `sin_h76` da **−0,08**, IC95 **[−0,65; +0,49]** por semilla y
[−0,63; +0,47] a dos vías. El intervalo **excluye el +2,5 atribuido**. Cambia
acciones en sólo 102/1.280 episodios. Sigue en la base activa por inercia; no
daña, pero no aporta. Ver [pre-registro](PREREGISTRO_ABLACION_H76.md).

**Calibración de la escalera:** `hoz` y `grano` son idénticas en el 92% de los
episodios y difieren −0,08 en panel, pero la escalera las separa 43 puntos
(818,1 vs 774,8). **Diferencias <50 puntos entre submissions propias no
informan.**

**`seed_stock_aware` CONFIRMADO (2026-09-06).** Ablación con 16 semillas nuevas
(105000–105015): `sin_ssa` da **−6,25**, IC95 [−11,15; −1,35] por semilla y
[−11,32; −1,18] a dos vías. **Ambos excluyen cero.** La magnitud replica el +6,4
original medido con semillas distintas. **El campeón está bien fundado**; su
ventaja sobre `CAMPEONA_FASE` viene de aquí, no de `harvest_76`.

**Diagnóstico del protocolo:** con 8 semillas el MDE al 80% de potencia es
**10,4 puntos**. Los tres mecanismos medidos (6,4 · 4,84 · 2,5) estaban por
debajo: nunca tuvimos potencia. Protocolo nuevo en
[BITACORA.md](BITACORA.md#2026-09-06) — piloto para estimar sd, dimensionar el
bloque, dos vías como análisis primario, ablación sobre la base activa.

Se ejecutaron 3.840 episodios de panel. Todos terminaron sin errores. Noop exacto
en las 960 comparaciones correspondientes; el control anterior perdió claramente
en ambos bloques. El candidato cambia acciones en sus 960 episodios, pero el
adelanto de cohortes se midió sólo en la sonda, no en todo el panel.

No se ejecutó el veto head-to-head planificado: exigía confirmación positiva.
El smoke posterior del paquete contra su mismo módulo tuvo dos episodios sin
errores y medias idénticas; **no es ese veto** ni prueba fuerza contra HOZ.

## Interpretaciones que debemos retirar

- W/L/T idéntico o dinero idéntico no implica decisiones idénticas.
- 3.840 episodios no son 3.840 muestras independientes: el análisis principal
  de confirmación tiene ocho promedios de semilla sobre un panel fijo.
- La brecha d12–d16 contra el líder es una pista, no una causa identificada.
- Fracasos de variantes concretas no prueban que toda búsqueda esté agotada.
- El t por celda de 2,45 no reemplaza después de observarlo el criterio por
  semilla que habíamos fijado. Tampoco se cambia a un test unilateral.

## Qué sigue y qué no está iniciado

1. Otro LLM revisa críticamente este estado, la auditoría y el protocolo.
2. Se escoge **una** siguiente prueba con coste y resultado falsador explícitos.
3. Se registra y acuerda el presupuesto antes de ejecutar otro barrido.
4. Una decisión futura sobre Kaggle necesita instrucción nueva del usuario.

No hay procesos de evaluación, subidas ni monitores programados por este traspaso.

## Dónde está la evidencia

- [Experimento detallado](EXPERIMENTO_LOTES_SEMILLAS.md): protocolo y resultados.
- [Auditoría del razonamiento](AUDITORIA_LLM.md): errores y límites.
- [Ideas y pruebas](IDEAS_Y_PRUEBAS.md): cola corta para evaluación crítica.
- [Evidencia transportable](evidencia/lotes_semillas/README.md): JSON, episodios
  comprimidos, manifiestos y fuentes exactas del panel.
- `results/`: originales locales, ignorados por Git.

Los archivos nuevos y modificados están en el working tree. Este trabajo no
creó un commit: para que viajen en un clon deben incorporarse a Git o compartirse
mediante el archivo de contexto generado. No dar por hecho que ya están remotos.
