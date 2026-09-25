# Loop26: presupuesto de semillas por cultivo y compra justo antes de sembrar

Registrado antes de construir o ejecutar las candidatas. Auditoría de18replays
ya seleccionados por recencia, fuentes reales reproducidas:54semillasWHEAT
residuales en16partidas y7CARROTen2. Desde624se compraron99WHEAT/255CARROT.
Manteniendo congeladas las acciones observadas y respetando validación atómica
dePLANT, se podrían omitir42comprasWHEATy7CARROT. Es un diagnóstico con futuro
conocido, no una política desplegable ni una estimación de mejora competitiva.

La guardaE402ya limita compras desde624: suma todos losPLANTfuturosWHEATyCARROT
y usa esa misma cota para cada cultivo. No repetir una guarda terminal genérica.
La conversiónCApuede cambiarWHEATaCARROThasta día28; no usar una cota de zanahoria
que ignore futuras conversiones. No volver a crop_end26, que modificaba siembra.

## Dos políticas sobre VQ, referencia real de mayor rating observado

- `seed_kind`: conservar sólo compras deWHEATnecesarias para el número de
  PLANTWHEATen la cinta propia restante, más todas las solicitudesWHEATpendientes
  de reparación. Misma ventana624–718. Disponibles: semillas actuales menos
  todas las solicitudesPLANTWHEATde este turno, como cota conservadora.
  Recortar cantidades, conservar posición de todas las demás órdenes y usar
  `[]` para cero. No tocarCARROTni agregar compras.
- `seed_jit`: desde624, sustituir comprasWHEATpor la necesidad del siguiente
  turno nativo más todos losPLANTWHEATpendientes, descontando semillas tras
  acciones actuales proyectadas con `_r127_fields`. Puede añadir una compra
  donde el padre no compra: usar su primer slotWHEATsi existe, un slot vacío
  o el final de la cola si hay espacio. No mover otras órdenes. Presupuesto
  conservador `_r97_budget`, sin acreditar ventas actuales. Si falta slot o
  fondos, conservar la acción padre completa y registrar rechazo. Nunca
  omitir una compra parcial del padre y luego fallar la reposición.

Ambas reciben sólo observación actual y planes propios existentes. Sin acceso
a semillas de episodios, replay futuro ni acciones privadas rivales. JIT
necesita probar explícitamente reposición y validación atómica: una semilla
no utilizada puede ser necesaria para que otra siembra del mismo turno pase
el control de cantidad total solicitado. No inferir seguridad por stock final.

## Desarrollo y criterios de integridad

Cuatro mundos fijados:1065000/1065001 nuevos,102886466 (residual observado) y
1943089929 (sin sobrante observado). Ambos asientos contra arshs3reactivo,
VQ/noopVQ/top3control/seed_kind/seed_jit:40partidas. RuntimePYTHONHASHSEED0.
Noop5.752turnos exactos; fuentes y órdenes antes del motor archivadas, caja
conciliada y720DONE. Compras/siembras efectivamente aceptadas, reservas antes
de cadaPLANT, unidades en bolsas y semillas finales. Registrar slots, fondos,
modificaciones, errores, tiempo y escapes. Candidato con menos siembras,
alimentación, cosecha o cambios de rutas no explicados queda detenido antes
del piloto; no aprobarlo por ahorrar dinero. No elegir brazos por rewards
de desarrollo. Si es necesario reparar implementación, conservar versiones.

## Evaluación nueva, panel cercano explícito

Usar el harness existente, un torneo grande tras25. Piloto1066000–1066015,
ambos asientos contra cuatro fuentes congeladas: mirrorVQ, mirrorTop3, V7yHS4
del panel25. Cinco brazos contando base/noop/top3:960partidas. Ambas candidatas
se comparan con VQy top3en los mismos rivales, excluyendo cruces entre brazos.
Hasta dos con delta>0frente a ambas referencias, orden por menor delta y nombre.

Confirmación1067000–1067031, mismos cuatro rivales más Harvest68y arshs3,
1.920/2.560partidas para una/dos seleccionadas. Gate≥3ppfrente aVQy≥0frente
atop3, peor rival≥−20ppfrente a ambas, acciones propias distintas en≥2semillas,
controles exactos, mecanismo y tiempo. Intervalos por semilla y dos vías;
copias/forks no se convierten en familias independientes por tener otro nombre.
Reportar dinero sólo como diagnóstico. Sin selección positiva, continuar otra
hipótesis; sin envío automático. Antes de enviar, sensibilidad a hashes alternativos
y revisión del agente activo que sería desplazado según la adenda de runtime.

Esta población es distinta del panel antiguo; no reescribe sus resultados ni
las decisiones previas. Los bloques19–25 conservan fuentes y diseños.
