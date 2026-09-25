# Fronteras después de loops7–10

Actualización09:28UTC: confirm19_fixedhash0cerrada/noop832, ambasdelta0,
seis trayectorias propias distintas en tres semillas, todas ya ganadas; no
selección.20corriendo y21–26en cola. No repetir.27en desarrollo: sincronizar
_V9_RACE.prev.own/left con las órdenes finales, porque65desajustes en seis
replays contaminaron observaciones rivales. No cambia biblioteca/umbrales ni
resuelve ventas al mínimo. Preregistro27,48desarrollos antes de encolar.

Estado 09:11 UTC: confirm19 original completo pero noop inválido; repetición
confirm19_fixedhash0 en curso con runtime uniforme. Piloto +2,734375 pp
conserva su selección; 20–26 en cola, ninguna partida duplicada.
16/18 completos sin seleccionadas; 17 detenido por modelo temporal erróneo.
No duplicar corridas. 91 variantes construidas más 2 prototipos detenidos. Leer
estado y scorecards actuales antes de usar las propuestas históricas de abajo.

Leer `REPARACION_HASH_RUNTIME_2026-09-25.md` antes de ejecutar: cuatro controles
discrepaban sólo en orden de ventas rival;48sondas reprodujeron hashes y estados
económicos iguales. No se relaja noop; la nueva confirmación reemplaza la
medición inválida y no aumenta el N estadístico. No reiniciar procesos anteriores.

Loop25 prueba cinco fuentes existentes contra copias reactivas de VQ/top3 y
V7/HS4, confirmación con Harvest68/arshs3 adicionales. Fuentes fijadas antes de
resultados pendientes; no escoger las ganadoras de 19–24. Motiva auditoría de
15 replays con campo muy parecido y mercado distinto. No presume código
compartido ni altera gates anteriores. Piloto1.920 tras24, confirmación nueva;
ver preregistro25 y `SIMILITUD_RIVALES_2026-09-25.md`.

Nueva frontera21: moderar sólo señales de patrones secundarios, mantener
la regla del principal.42juegos/noop4.314/max293ms, cuatro brazos activos en
tres mundos; cambian alimento/cosecha en dos, sin escapes. Piloto2.016incluye
VQcomo control y dos fuentes nuevas escogidas antes de su piloto18. Confirmar
contra13rivales con ≥3ppvs top3y≥0vs VQ, además de guardas previas. La muestra
real emparejada7/8márgenes favorables a top3usa rival grabado: no prueba fuerza.

Nueva frontera20: crear compras en pulsos de consumo observable del pueblo.
30juegos/noop4.314/max358ms,146compras/cierres y7.862unidades verificados.
Sonda sintética prueba que una previsión sin rival positiva puede perder caja
propia y margen: no llamarlo arbitraje garantizado. Piloto1.920tras19,
semillas1049000–031. Mantener VQcomo referencia real: top3gana localmente,
pero no demostró superar su rating actual. Todo próximo envío debe valorar
que desplazaría VQ. No cambiar los paneles de bloques ya registrados.

Loop26valida semillasWHEATpor cultivo/reposición:40juegos/noop5.752,
76compras aceptadas, conserva campo y producción en cuatro mundos. Ahorro
0–20sin cambiosW/L/T; no adoptar por dinero. En cola tras25,960piloto, padres
VQy top3control; no repetir una guarda terminal genérica porqueE402ya existe.
91variantes competitivas más2prototipos detenidos. Leer informe/preregistro26.

## Nueva prioridad: financiar alimento antes de cambiar vacas por ovejas

Piloto10 demuestra un fallo concreto en ars40/1018001/asiento0: dos ovejas
cuestan200más; la caja220→20 antes de191 impide comprar trigo (7unidades→0).
FEED194/197/218/222/226 llegan sin trigo y tres vacas escapan239. Margen
+1.037→−22.858. En hybu/1018011/asiento1 el mismo tipo de conversión con
dosYARN eleva lana410→459 y margen−355→+6.895, sin escapes. Son diagnósticos
dirigidos, no estimadores. `pilot10.funding_failure.json` guarda la cadena.

Hipótesis nueva: reserva de caja para las compras de insumos próximas antes de
autorizar sustitución temprana. El margen estático100/500 no mide obligaciones
de alimento. Auditar la cinta futura y el coste de compra, sin contar cosechas
inciertas ni inyectar trigo. Validar que evita la compra fallida del caso adverso
y permite activación en mundos solventes; después semillas disjuntas. No tocar
confirm10 (ya completa/inactiva) ni rescatar y1 por el caso positivo.

**Implementación registrada loop15:** reserva de alimento hasta cierre,24/48h
y reserva de todas las obligaciones24h.42diagnósticos antes del piloto1.568
(1034000–015), control antiguo incluido sólo para atribuir reparación. No
acredita ingresos futuros ni cambia alimento/rutas.42diagnósticos válidos,
noop4.314, max294ms:night/24evitan escapes en el caso adverso y permiten
conversión en el solvente;48/all24inertes en desarrollo. Piloto1.568completo, sin seleccionadas: leer el diagnóstico de rentabilidad15.
Consultar protocolo15, no presentar estas sondas como ganancia competitiva.

Las tres parejas D3/D6 fueron idénticas128/128por pareja; no contarlas como
réplicas independientes. Y2 sólo cambió8/128celdas de pool en una semilla.
Si las dos primeras tiendas fueran independientes/uniformes entre8opciones,
YARN/YARN sería1/64: una política exclusiva de ese contexto tendría techo
global nominal1,56pp aun corrigiendo todas sus derrotas. Es una deducción bajo
supuesto, no prevalencia medida; el gate3actual se conserva. Diseños futuros
para efectos raros necesitan estratos definidos sin mirar resultados y pesos
poblacionales, no escoger semillas favorables después del torneo.

## Reasignar compras futuras de vacas con demanda de lana ya visible

El caso c0nrad auditado dejó sólo4.294 de venta de134 leches propias, frente a
69.502 por391 lanas. Agregar peones tarde es caro: los rebaños del loop9 pagan
jornales Fibonacci, y su proyección corregida rechaza el mundo de desarrollo.
Una alternativa distinta es aprovechar pasturas, trabajadores y recorridos ya
presupuestados para futuras vacas, comprando ovejas cuando las tiendas visibles
y caja lo justifiquen. No convertir animales existentes ni quitar alimento.

Loop3 modificó la decisión **GOOSE→otro animal** de HD2 y extrapoló tiendas
futuras; esto no propone repetirlo. Antes de implementar, localizar compras
nativas COW posteriores a conocer tiendas y separar las que genera HD2. Evitar
mezclar cohortes COW/SHEEP: confirmar compra, reescribir PICKUP/PLACE de los
actores correspondientes, confirmar colocación y vender lana realmente recogida.
Verificar si HARVEST/CARE/retornos del padre son agnósticos al animal. Mantener
reserva para100 extra por cabeza y obligaciones del padre. No asumir que todas
las rutas tienen compras tardías elegibles ni que el reemplazo conserva trabajo.

Prueba dirigida sólo para mecánica, noop exacto y diagnóstico de cobertura;
luego registrar semillas/rivales nuevos antes de competir. Comparar efecto
total W/L/T, oferta comprometida propia/rival y coste de oportunidad. Ningún
delta local anterior garantiza esta combinación ni su Elo.

**Implementada como loop10:** auditoría encontró que `_y_controller` YA
convierte compras entre8–11. La novedad se limita3–7, sin modelo EV ni tiendas
futuras. Seis políticas,48juegos dirigidos válidos; primera activación observada
en173/178, dos animales colocados y49lanas cosechadas. Piloto1018000–015,
confirmación1019000–015 registrados. Runner espera loop9. No reinventar otro
controlador ni repetir desarrollo; consultar `PREREG_LOOP10_VACAS_2026-09-25.md`.

## Revisar oferta comprometida del tomate adicional

En pilot7/ars40/1010001/infill4_d18, el padre ya comprometió su campaña V219
pero varias plantas aún no existen al cotizar. La función de v4 sólo enumera
plantas visibles; puede omitir parte de esas80 unidades futuras. La cotización
de9.756 para4 plantas no es ingreso incremental observado. El total de tomate
vendido pasa80→96 y su ingreso30.024→34.386; también cambian tiendas y otros
ingresos. Conservar confirm7 íntegra, después considerar una nueva versión
con oferta comprometida si la evidencia justifica dedicarle otro bloque.

Confirm7 terminó inerte352/352por variante, sin selección. Corregir oferta
solamente estrecharía el gate: no gastar otro piloto idéntico por esa corrección.

## Actualizar biblioteca de ventas rivales sin volver a cintas pasivas

Top3 confirmó ventaja local al admitir más patrones. Ahora hay cuatro replays
recientes de top3 y cuatro de DSM con transacciones aceptadas exactas. Se puede
estudiar cobertura temporal de la biblioteca existente y agregar streams
actuales agrupados por primeras tiendas, deduplicados y sin filtrar W/L.
No usar replays de entrenamiento como confirmación ni interpretar predicción
offline como fuerza competitiva. La comparación competitiva exige rivales
reactivos y mundos nuevos, además de revisar coste de cómputo. El gate de
confianza/off ya perdió mucho en la ronda anterior: no repetir esa poda.

Auditoría hecha:2.398streams,64/64pares de tiendas,24–63por par. No se conoce
fecha original porque los ids están sustituidos por−1. Doce fuentes fijadas
por recencia (DSM4 y rivales top3 ocho) son nuevas con fingerprint que preserva
umbrales nativos de cantidades; no agregan pares de tiendas. Artefactos
`forecast_library_audit.json` y `recent_sale_streams.json`. **Implementada en
loop11:** tres fuentesets preservan desempate original, noop exacto y20juegos
validados. Ladder/all sí seleccionan streams nuevos. Piloto/confirmación con
32semillas por bloque, fuentes congeladas. No repetir desarrollo ni confundir
inclusión de nuevos datos con mejora de precisión o W/L. Ver protocolo loop11.

Piloto11terminó:1.920, noop448/448, cero errores; DSM inerte256/256,
ladder/all cambian18acciones propias/10rivales, cero diferenciasW/L/T. Ambas
son equivalentes256/256en este pool. Sin selección, no confirmar bibliotecas
por el solo hecho de añadir datos. ICdos vías indefinido, no evidencia de efecto0
en todos los contextos. La interacción con history360no se registra sin nueva
motivación: biblioteca no confirmó ventaja para justificarla aquí.

## Señal residual y diagnóstico pendientes, sin nueva corrida registrada

History360 terminó confirm8 en+2,8409pp, IC dos vías[−1,249;6,931], debajo
del gate3. No fue enviada ni refutada; no redondear, reutilizar seeds o cambiar
el gate. Si la biblioteca confirma ventaja, una interacción historia×biblioteca
necesita diseño nuevo, no sumar deltas de bloques distintos.

La referencia MarketShock nueva motivó loop12 de aperturas controladas.
Piloto completo1.008/noop192: tomate−80,46875pp yMarketShock−64,0625pp,
ambos rechazados con ICdos vías negativos. Original−3,125pp, cycle0; no
selección ni confirmación. Cycle sí cambia128/128acciones. La
telemetría de trigo de base/cycle espera53, pero el motor cosecha en87; futuros
diagnósticos deben usar acciones aceptadas y cronología real. No hay aún una
variante de mantenimiento/replantado ni evidencia de que convenga.

## Capacidad nocturna y reasignación productiva

c0nrad113107623: motor confirma33unidades destruidas en nuestras descargas,
rival0. No es stock terminal ni inferencia por órdenes. Guardas existentes no
rescatan estas cinco noches manteniendo la misma mezcla de productos. Loop13
implementa venta de insumos excedentes para liberar capacidad, bajo reservas
1/2días. V2completó36juegos, noop4.314,22activaciones exactas contra motor;
cero escapes/diferencias en alimentación nocturna, máximo291ms. V1inválida por
omitir VQ queda archivada y no se usa. No añadir otra guarda equivalente sin leer
`PREREG_LOOP13_ALMACEN_2026-09-25.md`. En671 sólo hay carga>100 y almacén0:
ese caso necesita logística previa; la variante no promete resolverlo.

La auditoría de trabajo encuentra759PASS/3.186movimientos propios frente a
280/2.556del rival, y302vs113riegos efectivos de fresa. c0nrad duplica cuidados
ovinos con menos jornales. Próxima frontera estructural: reemplazar cultivos o
rutas futuras por cuidado ovino con las mismas horas, previa auditoría de
factibilidad por posición/hora. No tratar PASS agregado como peón disponible.
Auditoría posterior de los mismos8replays: no queda CARE útil omitido al cierre
entre oportunidades PASS observadas.60huecos de WATER no aumentan producción
inmediata/próximo amanecer ni evitan muerte esa noche. No prueba ausencia de
beneficio a mayor horizonte ni rutas óptimas.261huecos FEED motivan **loop14**:
cuatro ablaciones del filtro económico nativo,36juegos de mecánica válidos,
noop4.314turnos y piloto1.248encolado. No añadir fallback ciego a cada PASS.

El piloto9 inerte no refuta todas las inversiones: no activó cambios en este
panel. Sus razones de rechazo por caso no se guardaron en el torneo; no
atribuir todo a un gate específico sin sonda. Repetirlo sin política nueva
no enseña más.

La predicción de overflow requiere observaciones del motor reconstruido:
el JSON ordena bolsas alfabéticamente y produjo pérdida/acción falsa en527.
Cinco comparaciones de observación viva coinciden con el motor. Mantener esta
distinción al diseñar diagnósticos futuros; no se demostró vínculo con pilot7.

## Composición inicial y cuidado que excede capacidad

Loop16 registra cuatro mezclas iniciales:1/2vacas→ovejas y1/2ovejas→vacas,
sin nuevos trabajadores ni rutas, costes reales±100/200. Se verifica compra
y colocación con créditos nativos; no se conocen aún las tiendas. Desarrollo
48juegos válidos/noop5.752/max329ms, piloto2.496con32semillas1037000–031en cola
tras15. Las cuatro composiciones compradas/colocadas correctamente; sheep2pierde
una vaca215en1272457736. No confundir
desarrollo con ventaja poblacional ni omitir cambios de cultivos/RNG posteriores.

La auditoría de12replays encuentra33MILK truncadas con yield previo0: exceso
de cuidado antes del primer yield de vacas tardías. Cosecha adicional no ayuda
en esas tiles vacías. Loop17 probó valor marginal limitado en24partidas, pero
se detuvo: cap_full ignora cosechas entre FEED y producción. Omite FEED682,
cosecha4huevos687y pierde un huevo en700; premisa temporal falsa. Cap_first
cambia valoración pero no acciones en tres mundos. No ejecutar piloto17.
Una versión futura necesita stock proyectado tras cosechas o una tile
demostrablemente vacía, además de alimentación siguiente factible. Ver
`capped_bonus_decision.json`; no repetir fórmula ni renombrar multiplicadores14.
14EGG sí se pierden
con inventario previo, pero rescatar requiere ruta/entrega factible.

## Fuentes públicas renovadas, loop18

V7cda529cb/HS48378f73c son distintos de los anteriores, extraídos de notebooks
actualizados04:09UTC y archivados.24juegos verifican entradas oficial/nominal,
noop, caja y tiempos; cambian acciones en ambos mundos. Piloto704en cola tras16,
confirmación disjunta si procede. No asumir dominancia por texto del notebook
ni reemplazar los rivales antiguos. El indicador HS4de adelanto2turnos no se
activa; no significa que su forecast nativo completo esté inerte.

## Incidencia neutral pendiente del harness

Cuatro filas de pilot7 tienen hash TDS alternativo pese a acciones propias,
rewards y W/L/T iguales. Ocho reproducciones con PYTHONHASHSEED0–3 no lo
reprodujeron y preservaron720 estados entre base/infill inerte. No afecta
selección observada; el origen aún no se ha identificado. Si reaparece, capturar
las acciones anteriores al motor y el primer estado divergente; no cambiar el
harness, eliminar rivales ni atribuirlo a hashes/tiempo sin prueba.


## Actualización06:08UTC: confirmación nocturna y frente de trigo

Piloto13:+4,6875pp en tres de cuatro variantes, tres celdas mejores en dos
semillas. Inputs1/2seleccionadas por desempate registrado; confirm13en marcha.
Diagnóstico12juegos confirma reducción de pérdidas y también cambios de
producción/alimentación en una celda neutral. No convertir esa señal en
ventaja confirmada ni mover reservas usando la confirmación parcial.

Nuevo replay real113164976contra today pierde1.702con composición/costes
similares. Neto de compra/venta de trigo propio12.308vs15.501rival; resto de
flujos compensa1.491. Auditoría futura: cronología de arbitraje/inventario y
precio aceptado. Todavía no hay una ablación nueva registrada; no interpretar
comprar/vender más como causa probada ni repetir ADV ya rechazado. Este frente
es distinto del ahorro nocturno y puede investigarse mientras termina el panel.


## Actualización06:28UTC: confirm13 sin mejora y trigo19 validado

Confirm13:1.600/noop416, cero errores, delta0ambas. No inertes:107/86acciones
distintas, margen sube103/82y baja4cada una, sin cambiar W/L/T. No adoptar ni
redefinir criterio por dinero. Piloto14ya corre desde06:21:20UTC.

La auditoría de trigo reprodujo nuestra fuente exacta719acciones/720estados.
Rival today pide mitad en11de44compras grandes y anticipa slot en20. Loop19
separa prioridad, mitad y ambas,30juegos/noop4.314/max305ms: actúan en el mundo
dirigido, inertes en los otros dos; no selección por recompensas. Fuentes/caja,
slots y transacciones físicas comprobados. Cobertura estática5/64pares motivó
ampliar antes del piloto a32semillas en ambos bloques. Encolado después de18.
No tratar cobertura de tabla como frecuencia poblacional ni reutilizar semillas.

Nuevo frente todavía sin experimento registrado: las secuencias de reventa
son cantidades de cinta en44/44decisiones grandes de la derrota. Podría
estudiarse un criterio dinámico para proponer o dimensionar compras según
consumo observable del town, inventario, capacidad y rival estimado, separado
de loop19. Requiere verificar exactamente el coste de ida/vuelta lockstep;
no asumir ganancia por la diferencia entre precios anunciados ni usar futuro
rival real en la política. También vigilar transferencia: VQ2294,3/85frente
a top32084,7/73en06:26UTC, comparación descriptiva, no efecto causal probado.


## Actualización07:40UTC: cobertura de suministro

16rechaza las cuatro mezclas iniciales incondicionales;18no seleccionaV7/HS4.
No repetirlas ni alterar el panel de21/22por sus resultados. Harvest V68es
fuente nueva con selector restante COW/SHEEP;22validado y en cola.

Prioridad23: demanda nativa+peón ovino dinámico. La derrota real davion muestra
21PICKUP0y seis ovejas sin alimento pese a caja suficiente. Regla general rescata
24lanas contra replay fijo;24desarrollos reactivos arshs3inertes, cobertura
adicional24contraVQ/V7/HS4completa: activaV7ambos asientos, recupera24lanas
y margen−5090→−1093, sigue derrota.48juegos/noop8.628validados,23encolado. Mantener ausencia de cobertura visible,
no seleccionar semillas positivas para estimar W/L/T. Presupuesto piloto32
semillas ya fijado antes; no ampliarlo mirando parciales. Tras esto investigar
si mecanismos raros requieren pruebas estratificadas por situaciones observables,
con población/ponderación fijadas de antemano, sin mezclar con panelglobal.


## Hipótesis ya construida: adelantar compras nativas de trigo (loop24)

Feedback0742, VQcontraGrimReaper:19/19compras grandes iguales por cantidad
solicitada, rival un turno antes;2988monedas menos con1359vs1361unidades.
Nuestra fuente real reproduce719acciones/720estados. Diferente de19(slot/cantidad)
y20(nuevas operaciones), y deADV(ventas). Revisar cancelación del compromiso
nativo al turno siguiente, capacidad nocturna, insumos y fondos. Probar sobreVQ
con top3como control, no escoger padre sólo por panel local. Registrar antes de
crear variantes; no inferir algoritmos de una trayectoria ni adoptar por ahorro.


Actualización08:11UTC: loop24validado36juegos/noop8.628/max308ms;64adelantos,
4480unidades descontadas del compromiso. VQy top3probados, piloto conVQbase.
No repetir. El adelanto permite también SELLantes, y cambia3CARROTpor3WHEAT;
no separar causalmente sin intervención adicional. Sonda384mercados temporales
valida dependencia del rival y efecto de perder consumo del pueblo.19piloto
+2,734375pp en dos semillas: confirmacióncorre, aún sin adoptar/componer.
Catálogo08:02no tiene nuevas ejecuciones en50entradas; no descargar duplicados.
