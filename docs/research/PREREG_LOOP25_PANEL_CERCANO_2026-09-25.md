# Loop25: prueba nueva contra políticas cercanas y reactivas

Registrado el 2026-09-25 antes de construir el manifiesto o ejecutar partidas.
Motivación: auditoría descriptiva de 15 replays recientes, documentada en
`SIMILITUD_RIVALES_2026-09-25.md`. La pregunta es si las mejoras sobreviven
contra políticas de campo muy parecidas y diferencias pequeñas de mercado.
No se conoce el código de los rivales reales ni se pretende reconstruirlo.

Los bloques 19–24 conservan sus fuentes, muestras y criterios. Este panel es
una población experimental distinta: no convierte un resultado previo negativo
en positivo ni permite atribuirle un cambio de Elo. Se reutilizan fuentes
validadas, sin nuevas modificaciones y sin sumar variantes al total construido.

## Fuentes fijadas ahora

Referencia principal VQ enviada, control top3 enviado y noop de VQ. Cinco
candidatas escogidas antes de los resultados pendientes, una por mecanismo:

- `history360`, hash f8740132: señal residual del loop8; quedó debajo del gate
  anterior y conserva esa decisión. Aquí se prueba otra población.
- `wheat_front`, hash ab5ab19c: prioridad de compra sin reducir cantidad;
  aísla un cambio frente a la combinación de dos cambios de `wheat_both`.
- `advance_vq`, hash a35c696c: adelanto de compra sobre la referencia VQ.
- `sheep_supply_buy`, hash 7b3257ba: abastecimiento antes de contratar; no se
  incluye hold porque ambas coincidieron en las 12 celdas de desarrollo.
- `harvest68`, hash 3b543611: paquete público reciente completo como alternativa.

No se cambiarán estos nombres por los ganadores de los bloques 19–24. Todas
tienen desarrollo previo y fuentes archivadas. Revisar hashes antes de correr;
un nuevo fallo de integridad suspende el bloque, no provoca sustitución de brazo.

Piloto: cuatro rivales con nombres independientes de los brazos, todos reactivos:
`mirror_vq` (9b463dfb), `mirror_top3` (9668e30a), `public_v7` (cda529cb) y
`public_hs4` (8378f73c). Una copia es una nueva instancia del mismo fichero,
no una cinta grabada. No representan cuatro familias estadísticamente independientes.
Se incluyen V7/HS4 pese a sus resultados anteriores negativos.

Semillas nuevas **1063000–1063015**, ambos asientos. Ocho brazos contando
base/noop/top3, cuatro rivales: (8×4 + 28)×32 = **1.920 episodios**.
Se usa `torneo.py` sin modificar. Primaria: delta W/L/T pareado en los cuatro
rivales comunes, comparado tanto con VQ como con top3; cruces entre brazos
excluidos. Medias equiponderadas por rival y semilla, intervalos por semilla
y dos vías existentes, sin reinterpretar pocos rivales como diversidad efectiva.

Seleccionar hasta dos candidatas con delta estrictamente positivo frente a
AMBAS referencias. Ordenar por el menor de esos dos deltas, desempate por
nombre alfabético. No seleccionar por margen monetario, directos o resultados
parciales. Si no hay candidatas elegibles, cerrar el bloque sin confirmación.

## Confirmación y decisión

Semillas nuevas **1064000–1064031**, ambos asientos. Conservar los cuatro
rivales y agregar `recent_harvest68` (misma fuente que la candidata) y arshs3
original (fichero enviado anterior). Seis rivales fijados ahora; la auto-copia
de Harvest68 también es un enfrentamiento válido y se reporta como tal.
Una seleccionada: (4×6+6)×64 = **1.920 episodios**; dos: (5×6+10)×64 = **2.560**.

Gate para considerar prueba real: delta **≥3 pp contra cada referencia**,
ningún rival con delta <−20 pp contra ninguna, acciones propias distintas a su
referencia de comportamiento en ≥2 semillas de confirmación, controles exactos, cero errores y runtime
compatible con límite del motor. Reportar también los cuatro rivales originales
y los dos agregados, sin usarlos para rescatar un fallo de la métrica principal.
Mecanismo aceptado por motor y celdas de daño se revisan antes de cualquier envío.
La referencia de comportamiento es VQ para advance_vq y top3 para las otras
cuatro. Top3 es el padre de history360/wheat_front/sheep_supply_buy, pero para
Harvest68 es sólo un comparador: no se afirma que el paquete derive de top3.

Este gate hace una candidata revisable; no ordena subirla. Antes del siguiente
envío, revisar ladder y qué agente activo desplazaría, junto con el contraste
entre este panel y los bloques anteriores. No combinar scores de paneles
distintos como si fueran réplicas de una misma población.

Ejecutar tras terminar loop24, con el único torneo grande de ocho workers.
Noop exacto en acciones/rewards, cobertura completa y archivos de fuentes
congelados; no añadir simulaciones de desarrollo redundantes para código idéntico.
