# Loop27: sincronización de ventas propias validada

Dos candidatas congeladas sobreVQ/top3. No modifica acciones directamente:
tras la acción final, proyecta trabajo propio con `_r127_fields` y actualiza
`_V9_RACE.prev.own/left`. Esto afecta después al detector de carreras y a los
dos predictores que consumen esa instantánea. Mantiene bibliotecas, horizontes,
umbrales y tratamiento del precio mínimo. Motivación: seis replays exactos
con65cantidades propias mal anotadas; ver FEEDBACK_0914.

- sales_sync_vq:094a5face24b1375b70c8ca5c9827a4fe6bee21b8c12f3faf59e68184ef6f1e3
- sales_sync_top3:739f18d546b2f6767d1d2773637ee5ffc3430d61690e9e49482c38cd4e2ba221

## Desarrollo y extensión registrada

48partidas originales: cuatro mundos, ambos asientos, dos padres/dos noops/dos
candidatas, frente aV7 reactivo. Cantidades y controles pasan; VQcorrige120
instantáneas pero no cambia acciones en8celdas. Top3corrige110y cambia2/8.
El verificador exigía activación por candidata y abortó; original preservado
junto con el motivo y hash, sin piloto iniciado ni corrección del criterio.

Adenda registrada antes de24partidas adicionales: mismos cuatro mundos, ambos
asientos, VQ/noopVQ/candidata contra mirrorTop3. Bloque completo, sin parar por
primera activación ni seleccionar por rewards. VQcorrige122instantáneas más y
cambia6/8celdas de esa extensión, en tres mundos. No equivale a confirmación
competitiva ni aumenta la muestra OOS del piloto.

Validación agregada PASS:72partidas,17.256turnos noop exactos de ambos jugadores,
120.792comparaciones producto/turno con cantidades propias aceptadas exactas.
Máximo403,44ms, cero errores observados. Tiendas, trabajo de unidades efectivo,
cosechas, pérdidas nocturnas y escapes se conservan frente al padre en todos
los desarrollos. Cero escapes y productos terminales; las pérdidas existentes
siguen presentes. Fuentes y oponente comprobados contra archivos congelados.

## Corregir la medición no garantiza mejorar decisiones

Auditoría de los cinco productosPREDICT con el filtro nativo de precio:

| Bloque / padre | Eventos falsos padre→corregido | Ventas reales omitidas padre→corregido |
|---|---|---|
|V7 / VQ|26→0|124→120|
|V7 / top3|10→0|120→122|
|mirrorTop3 / VQ|28→0|120→124|

No se cuentan los noops otra vez. Las trayectorias pueden cambiar entre padre
y candidata, así que no interpretar diferencias de omisiones como efecto
causal sobre las mismas observaciones. Con cantidad propia correcta, restar
ventas propias totales a incrementos del mercado no puede inventar más ventas
rivales que las aceptadas. Pero las ventas propias al mínimo siguen restando
cantidad que no entró al mercado; pueden ocultar ventas rivales reales.

En las celdas con acciones distintas, los márgenes de desarrollo empeoran:
top3frente aV7,560→459en1068000; VQfrente amirrorTop3,−221→−340,
−2187→−2287y−1478→−1586en1068000/1068001/2111590720. Ambos asientos dan esos
valores. Ningún W/L/T cambia. No adoptar porque el registro sea más exacto;
no seleccionar por estos rewards dirigidos.

## Piloto en cola

Runner27validó hashes y espera26. Piloto1069000–015,960partidas contra el panel
cercano congelado, VQbase y top3control. Confirmación1070000–031sólo si procede,
1.920/2.560partidas; gates originales intactos. Antes de envío, mecanismos,
hashes alternativos y revisión de ambas submissions activas. Sin subida automática.

Total93variantes construidas, además de dos prototipos17detenidos. El piloto20
sigue ejecutándose;21–27esperan en secuencia, un solo torneo principal.

Reproducir sin partidas: `verificar_cobertura_atribucion_ventas.py`; la versión
`verificar_atribucion_ventas.py` conserva intencionalmente el fallo de cobertura
original y no es el verificador final. Inferencia:
`medir_inferencia_atribucion.py` sobre evidencia ya completa. Archivos
`sale_attribution_*`; fuentes, órdenes, snapshots y ledgers archivados.
