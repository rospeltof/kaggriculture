# Loop22: Harvest Ledger V68 y ablación de su selector de ganado

Registrado antes de construir la ablación o ejecutar partidas. Catálogo
consultado a07:12UTC: Harvest Ledger declara nueva ejecución06:59:42UTC.
Fuente extraída por literales FILES, SHA256
`3b543611448947399c9902e6ca1e45b84e904031156ff012ea675947dc74197e`.
Se conservan LICENSE/NOTICE; no se ejecutó el notebook de empaquetado.
La descarga de Master Hybrid es idéntica a V7ya en cola y se excluye.

La fuente V68 sustituye el selector por nombre de tienda por comparación de
valor restante COW/SHEEP durante días6–20, sin nuevas tiendas futuras y con
margen250por animal y mejora relativa15%. Conserva las guardas heredadas de
caja/crédito físico y otras capas, incluido reordenamiento final de ventas.
La declaración del autor no es evidencia de fuerza local ni de su rating.
La entrada oficial y el alias final resuelven a `_final_sell_block_reorder_entrypoint`;
el helper `_dsm_herd_target` no es la entrada de juego.

Dos candidatas:

- `harvest68`: fuente pública byte exacta.
- `harvest68_no_ev`: misma fuente con `_dsm_herd_target` devolviendoNone y
  alias final que conserva la entrada correcta. Aísla la selección nueva;
  NO equivale a restaurar todas las reglas o configuración del padre histórico.

No trasplantar directamente el EV a top3 ni mezclarlo con nuestra reserva15.
Su efecto incluye compras, composición, producción, precios y respuesta rival.
Es distinto del EV de conversión GOOSE del loop3 y de conversiones tempranas
por YARN de loops10/15. El paquete completo no atribuye diferencias a una sola
capa; la ablación sólo responde qué añade este selector sobre esta fuente.

Desarrollo fijado:1054000/1054001nuevos y1578791335de la derrota real contra
daviondk, ahora con rival top3reactivo, ambos asientos. Base/noop/VQcontrol,
cada candidata por entrada oficial y nominal:42partidas. Noop4.314turnos,
igualdad de ambas entradas para las dos candidatas8.628turnos. Verificar
720DONE/caja/hash, nuevos contadores y errores heredados observables, swaps,
compras/colocaciones, créditos, producción vendida, escapes, inventario final
y tiempo<1s. El dinero de estos mundos no selecciona brazos. Detener por
fallo de implementación; no ocultar resultados económicos adversos.

Piloto1055000–1055015, seis rivales del loop21 (arshs3/tds/hybu/ars40 y fuentes
V7/HS4de05:48). Base/noop/dos candidatas/VQcontrol=5brazos×6+10internos,
ambos asientos:1.280partidas. W/L/T pareado frente a top3, unidad semilla;
hasta dos deltas positivos, orden magnitud/nombre. VQcontrol no es elegible.
Reportar contra VQ y entre full/off sobre iguales celdas, sin seleccionar por
un rival o partida favorable. No mirar parciales para cambiar diseño.

Confirmación1056000–1056015, trece rivales del loop21;1.856/2.400partidas.
Gate≥3ppvs top3, peor rival≥−20pp y≥0vsVQ, IC95dos vías, mecanismo y runtime.
Fuentes y muestras disjuntas; encolar después de21sólo tras validar desarrollo.
No enviar automáticamente ni reemplazar fuentes de los bloques ya congelados.
