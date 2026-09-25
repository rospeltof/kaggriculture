# Loop11: biblioteca de ventas con fuentes recientes

Auditoría previa: la base top3 contiene2.398streams y cubre64/64pares de
primeras tiendas. No tiene fechas/ids originales utilizables. Doce streams
nuevos provienen de transacciones ACEPTADAS, reproducciones exactas de720
estados y caja conciliada: cuatro DSM y ocho rivales de top3, muestras fijadas
por recencia antes de ver rewards. Nuevos por fingerprint que preserva los
umbrales del predictor; no agregan pares de tiendas. No afirmar que la
biblioteca antigua esté desactualizada ni que novedad sea precisión.

Tres brazos sobre top3 sha9668e30a: `library_dsm` agrega4, `library_ladder`
agrega8, `library_all` agrega12. Sólo datos de partidas históricas públicas;
tienda/ajuste del episodio corriente se observan por la API normal. Preserva
ranking nativo, historia240, top3, K4, horizonte48, extensión4 y desempates:
streams originales preceden a nuevos cuando puntúan igual. No combinar con
history360/phase2 mientras se están confirmando, ni repetir gate/off.

Desarrollo: dos mundos ya conocidos,1004000(FARM/FARM sin datos nuevos) y
1272457736(YARN/YARN con datos). Base/tres candidatas/noop sin nuevos streams,
ambos asientos vsarshs3 reactivo:20juegos. Mundo sin datos exige acciones
COMPLETAS/rewards idénticos en todas las variantes; noop también en YARN.
Contar candidatos nuevos expuestos, patrones realmente seleccionados, acciones
cambiadas y tiempo. Es una sonda de activación, no evidencia OOS: uno de los
seeds procede de un replay fuente. No seleccionar por W/L de desarrollo.

Como sólo10/64pares tienen datos nuevos, aumentar diversidad de mundos:
piloto **1021000–1021031**,32semillas nuevas, ambos asientos, cuatro rivales
fijos arshs3 original, tds, hybu, ars40. Cinco brazos×4+10cruces internos,
×64=**1.920 episodios**. Unidad semilla, primario deltaW/L/T pareado vsbase;
no seleccionar por margen monetario ni precisión offline. Hasta dos positivas,
por delta y luego nombre. Cero errores/noop exacto/hashes íntegros requeridos.

Confirmación **1022000–1022031**,32semillas disjuntas, once rivales fijos de
confirm1:2.304episodios con una seleccionada o3.200con dos. Gate≥3pp, ningún
rival<−20pp; informar IC semilla/dos vías, cobertura de activación y tiempo.
Subpanel de los cuatro del piloto sólo diagnóstico. No cambiar gate después.

Validar y congelar antes de encolar detrás de loop10. Un torneo grande a la
vez; no editar sus fuentes activas. Gate local no demuestra Elo: decisión de
envío también revisa mecanismo, coste runtime y feedback de nuestras activas.

Desarrollo terminado:20juegos, noop2.876turnos completos idénticos y todas las
variantes idénticas en par sin datos. Máximo249,8ms. En YARN/YARN el streamDSM
se expone pero no se selecciona; ladder/all seleccionan113126108 en164ajustes
por asiento y cambian18turnos. No se eliminan brazos ni se cambian reglas por
ese resultado. Fuentes/manifest sellados; runner espera fin del loop10.
