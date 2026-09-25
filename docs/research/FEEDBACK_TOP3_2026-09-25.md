# Primer feedback real de top3

Snapshot de submissions **2026-09-25 02:33:17 UTC**: top3 56537205 en1459,1;
VQ56535264 en2306,3. Top3 llevaba unos37 minutos. Listado02:34:01UTC devuelve
diez episodios, incluida validación113099118. Estos ratings no ordenan dos
políticas maduras. Fuente API cruda `ladder_snapshot_0233.txt`; el sufijo0236
del archivo de episodios es un nombre, no su hora real.

Selección fijada antes de descargar resultados: las cuatro completadas más
recientes por createTime, excluyendo validación conocida. No se filtró W/L.

| Episodio | Rival | Margen propio | Estado |
|---|---|---:|---|
| 113108628 | Neglected Turtle | +26.420 | DONE/DONE |
| 113107623 | c0nrad | −23.180 | DONE/DONE |
| 113107458 | StephenNedumpally | +4.037 | DONE/DONE |
| 113106269 | Platycerium | +7.776 | DONE/DONE |

Los cuatro se reprodujeron con **720 estados exactos**, motor1.32.7 y acciones
reales de ambos jugadores. Todas las transacciones aceptadas están registradas;
3.000 más flujo de caja coincide con ambos rewards. Cero ERROR/TIMEOUT/INVALID,
escapes propios0 e inventario propio final0. No es una estimación fiable de WR
global ni una comparación causal con VQ. Tampoco prueba ausencia de acciones
inútiles o pérdidas intermedias de inventario.

## La derrota contra c0nrad apunta a asignación productiva

Primeras tiendas YARN/YARN; al final cuatro YARN, tres BRUNCH y una PIZZA.
Al día15 el rival tenía32 ovejas y3 vacas, nosotros17 y6. Al día20 el dinero
era75.280 frente a56.505; terminó132.832 frente a109.652. Sólo tuvo un tomate
tardío. La hipótesis «nos ganan por tomate» no explica esta partida.

| Venta aceptada | Nosotros: unidades / ingreso | Rival: unidades / ingreso |
|---|---:|---:|
| Lana | 391 / 69.502 | 759 / 113.264 |
| Fresa | 244 / 29.825 | 86 / 11.003 |
| Leche | 134 / 4.294 | 83 / 4.370 |
| Melón | 72 / 16.425 | 90 / 14.119 |
| Fertilizante | 373 / 11.154 | 329 / 14.769 |
| Tomate | 0 / 0 | 8 / 536 |

El rival vendió368 lanas adicionales y cobró43.762 más por lana, pese a un
precio medio menor (149,2 frente a177,8). Nuestra ventaja en fresa no compensó.
Gastó menos en jornales:8.273 por274 contrataciones frente a10.217 por307;
y3.000 en tierra frente a7.000. Compró368 unidades de trigo frente a259:
más producción exigió más alimento, pero no más jornales agregados en ese mundo.

Esto sugiere estudiar densidad y calendario ovinos cuando la demanda ya es
visible, junto con el coste marginal de alimentar/cuidar/transportar. No justifica
forzar ovejas en todos los mundos, copiar la cinta rival ni subir una variante
sin comparación reactiva. Loop3 ya mostró daño de extrapolar tiendas futuras;
no repetir ese criterio bajo otro nombre.

La evaluación espacial de tomates loop7 y los seis predictores loop8 continúan
según sus protocolos. Siguiente hipótesis estructural a diseñar: uso de espacio
libre para un rebaño adicional pequeño, o reasignación de trabajo bovino con
demanda observada de lana, contabilizando jornales Fibonacci y capacidad de
alimentación. Aún no hay implementación, protocolo ni prueba de esa hipótesis.

Evidencia: `top3_replay_selection_0236.json`,
`top3_accepted_transactions_0234.json`, `top3_*.ledger.jsonl.gz`, hashes de
replays en cada resumen. Reconstrucción: `auditar_replays_top3.py`; utiliza
el ledger aceptado de `sonda_fallo_forecast.run`. El antiguo `ventas_reales.py`
no se utilizó: su aproximación con precios previos y órdenes emitidas no es
equivalente a transacciones aceptadas por el motor.

## Actualización03:39:41UTC

Top31941,6/30episodios listados; VQ2259,1/56. Ambos COMPLETE. Los recuentos
incluyen validaciones, no equivalen a partidas competitivas ganadas. Los
archivos tienen sufijo0333, pero sus `.fetch.json` registran la hora real.

Cuatro nuevas completadas por endTime, fijadas ANTES de leer rewards:

| Episodio | Rival | Margen propio |
|---|---|---:|
| 113127276 | shikaikaikaikai | +1.659 |
| 113126108 | 62326368 | +923 |
| 113124966 | wqlun06 | +1.279 |
| 113125627 | Clement Lau | +2.891 |

Motor reproduce720 estados×4, caja conciliada, DONE/DONE, sin escapes propios
ni inventario privado final. Contrataciones/tierra coinciden por pareja y
cantidades de producción son muy similares: por ejemplo410lanas/162leches
en ambos lados contra62326368. El precio/timing y pequeñas diferencias de
otras producciones importan en esa muestra. No atribuir causalmente las
victorias a top3 sin contrafactual; tampoco generalizarlas a adversarios de
economía diferente como c0nrad. Evidencia `top3_audit_0339.json` y ledgers;
reconstrucción `auditar_replays_recientes.py` con selección archivada.
