# Confirmación20: mejora pequeña, sin criterio de envío

Terminó el2026-09-25 a10:25:05UTC.3.200episodios completos,32semillas nuevas,
11rivales, ambos asientos;832noops exactos, hashes archivados verificados,
cero errores observados, runtimePYTHONHASHSEED0uniforme. Base85,3693%.

| Variante | Resultado | Delta pp | IC95 por semilla | IC95 dos vías | Celdas mejores / peores |
|---|---:|---:|---|---|---:|
| town20 |85,6534%|+0,2841|[−0,730;1,298]|[−0,859;1,427]|2 /1|
| town50 |86,5057%|+1,1364|[−0,476;2,749]|[−0,759;3,032]|5 /1|

El piloto+3,125pp no se sostiene con la misma magnitud. Ambas quedan PROMISING
según el clasificador, pero `registered_submission_gate=false`: no se envían.
Inconcluso no equivale a refutado. En los cuatro rivales del piloto, ambas
dan delta0 y128celdas iguales; el ICdos vías indefinido no prueba efecto nulo.

No son inertes: ambas cambian acciones propias en704/704partidas del panel,
en las32semillas. Cambian acciones rivales en206/306. Los conteos de celdas de
la tabla promedian asientos; los cambios por asiento son4/2 y10/2respectivamente.
Se conserva20sin modificar políticas, muestras ni criterios.29ya estaba
registrado con otra población y VQcomo segundo padre; no reinterpreta este bloque.

## Ejecución de todos los cambios W/L/T

Seis combinaciones rival/semilla cambian algún W/L/T. Sus dos asientos tienen
el mismo resultado: se reproduce asiento0 con base y las dos variantes,
18partidas. Hashes propios, rewards y caja exactos.167compras y167cierres,
6.280unidades compradas/revendidas al turno siguiente. Cero errores de capas;
esto no significa que toda operación beneficie el resultado.

| Rival / semilla | Base | town20 | town50 |
|---|---:|---:|---:|
| tds25 /1050001 |−3|46|120|
| tds25 /1050010 |−54|−19|32|
| hl25 /1050022 |−181|1.004|1.022|
| hsov /1050027 |−32|−14|8|
| h2965 /1050027 |−24|−6|16|
| v13 /1050019 |265|−79|−35|

En hl25, nuestras cajas ganan53/71, pero el rival pierde1.132: gran parte del
margen procede del efecto sobre él. Cambiamos tres trigos cosechados por tres
zanahorias. El ganso que escapa en695ya escapaba en base y sigue escapando en
ambas candidatas; no se oculta. En los otros casos auditados no hay escapes
propios y las cosechas coinciden. No inferir invariancia universal del campo.

## Daño por posición de la orden de cierre

En v13/1050019 se conservan cantidades cosechadas/vendidas de leche. Las
reventas aportan25/69monedas, pero en661 añadimos SELLWHEAT20/50 delante de
SELLMILK13. Ambos lados venden13leches ese turno: nuestra caja de leche pasa
1.815→1.617, la rival1.815→1.986. Total propio−173/−129, rival+171; margen
−344/−300. No fue una reventa de trigo que perdiera dinero por sí sola.

`sonda_prioridad_cierre_town.py` reproduce un control completo adicional de
town50 y captura la fase661después de unidades. Sobre dos copias idénticas,
procesa trigo primero o leche primero: cajas propias de esa fase3.611/3.809,
rivales1.986/1.815, margen mejora369. Inventarios privados y mercado finales
idénticos. Sólo se aísla causalmente esa fase; una política nueva puede alterar
trayectorias posteriores. Motiva el preregistro31, sin construirla todavía.

El primer intento del capturador omitió el wrapper de ledger entre el motor y
su hook y no capturó estado. V1/plan/traceback se conservan; v2corrige la captura,
reproduce719acciones/rewards y ledger entero exactos antes del contraste.
No contar el intento ni la fase aislada como una réplica competitiva.

Fuentes: `confirm20.*`, `town_close_priority_probe_v2.*`, los auditores de
confirmación y sus scripts de resumen.21comenzó automáticamente después;
22–30esperan en secuencia. Objetivo continuo activo.
