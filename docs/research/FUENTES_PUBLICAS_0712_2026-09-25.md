# Harvest Ledger V68: nueva fuente y ablación registrada

Catálogo consultado07:12UTC, descargas07:12:48–49UTC. Harvest Ledger tiene
ejecución06:59:42UTC. [Notebook público](https://www.kaggle.com/code/haodou092/kaggriculture-harvest-ledger).
Master Hybrid descargado otra vez es V7cda529cb byte exacto al de05:48,
incluido notebook: deduplicado sin otro torneo.

Harvest V68 SHA256 `3b543611448947399c9902e6ca1e45b84e904031156ff012ea675947dc74197e`,
1.056.066bytes, extraído por literales AST de FILES/base85/zlib con comparación
de EXPECTEDhashes. LICENSE/NOTICE conservados. No se ejecutó el notebook.
Dependencias estándar, mismos dos exec internos que su padre revisado,
biblioteca forecast ff3423idéntica. El fallback de archivos externos tiene
pathNone. Esto documenta la revisión de esta fuente, no una garantía universal.

La entrada oficial `get_last_callable`, el último callable del namespace,
`agent` y `submission_v68` apuntan todos a `_final_sell_block_reorder_entrypoint`.
El helper `_dsm_herd_target` no es entrada porque después se agregan aliases
nuevos. Se comprobó equivalencia oficial/nominal durante8.628turnos de juego.

La novedad visible en selector COW/SHEEP compara valor restante usando
`_hd2_ev`, días6–20, diferencia>250por animal y ventaja relativa>15%, sin
tiendas futuras nuevas. Hereda conversión de gansos y múltiples capas previas,
incluido reordenamiento final de bloques SELL. No atribuir todo el paquete
a ese selector ni dar por probado el benchmark que declara el autor.

Dos variantes preregistradas en loop22: fuente cruda y
`harvest68_no_ev` SHAab4cbb92, mismo programa con selectorNone. La ablación
no restaura la regla antigua por tiendas; desactiva esta decisión nueva.

Desarrollo42juegos, semillas1054000/1054001/1578791335, ambos asientos contra
top3reactivo: base/noop/VQ y dos entradas de cada candidata. Noop4.314turnos,
fuentes/720DONE/caja válidos, máximo712,6ms, cero errores en contadores
top-level observables. Los except heredados sin contador no se verifican así.

Selector activo en los tres mundos: cambia una SHEEP→COW en cada uno de los
dos primeros; dos COW→SHEEP en1578791335. Compras aceptadas conciliadas con
colocaciones y stock final, todos los créditos/pendingYliquidados. Cero escapes
y cero productos finales; quedan semillas2/0/6por mundo. Tiendas iguales a
top3en los primeros dos y distintas en1578791335, tanto full como off. No es
comparación aislada de precios. Cambios de acciones full120/102/190y off113/90/123,
idénticos recuentos en ambos asientos. Rewards de desarrollo no seleccionan.

Runner22validado y esperando21: piloto1.280juegos/16semillas, confirmación
disjunta1.856/2.400, controlVQy13rivales en confirmación. Gate≥3ppvs top3,
≥0vsVQ, peor rival≥−20, ICdos vías, mecanismo y runtime. Ningún envío nuevo.

Evidencia en `docs/evidencia/loop_publicos_20260925/`: `public_sources_0712.tgz`,
`public_extraction_0712.json`, `public_0712.entry_audit.json`, manifiesto,
`public_0712_smoke.*`, `public_0712_validation.json` y metadatos de consulta.
