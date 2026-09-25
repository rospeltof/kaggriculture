# Loop 6: cobertura de productos y combinación del predictor

Nueva base local de esta ronda: **top3 confirmado**, sha9668e30a, enviado como
56537205. No cambiar los padres de loops3–5, que siguen VQ según su preregistro.
Se pregunta qué mejora a top3, no qué vuelve a superar a un padre más débil.

Constructor `construir_forecast_productos.py`, cuatro brazos:

- top3_egg: incluye EGG en las anticipaciones. Curva hinge y producción frecuente;
  riesgo de vender antes de escasez mayor o contar oferta poco informativa.
- top3_melon: incluye MELON. Cosechas grandes y concentradas pueden hundir precio;
  riesgo de abandonar la ventana prevista de demanda.
- top3_egg_melon: ambas coberturas, para detectar interacción y competencia por
  slots de mercado. No inferir efecto de la suma sin evaluarla.
- top3_fast2: top3 + umbral2/actualización cada turno. Fast2 solo dio +2,841pp
  vs VQ en confirm1, sin pasar gate; ésta es una prueba nueva de interacción,
  no una reinterpretación ni repetición de su confirmación individual.

Piloto: base/noop top3, cuatro brazos nuevos y controles VQ/fast2 solos;
ocho rivales habituales. **1007000–003**, ambos asientos: ocho brazos×ocho
rivales +28 cruces entre brazos, **736 episodios**. VQ, A=top3, B=fast2 y A+B
conviven en la misma muestra; ambos brazos de producto y su combinación también.
Los controles VQ/fast2 no son rivales del estimador principal ni candidatos a
selección. Reportar sus deltas frente a top3 como contraste experimental.

Métrica primaria: delta W/L/T contra top3, ocho rivales equiponderados, unidad
semilla con ambos asientos. Semillas disjuntas de desarrollo y rondas previas.
Seleccionar hasta dos brazos nuevos con delta>0 (orden delta, empate alfabético).
CI por semilla y dos vías si estimable; registrar activación/hash/runtime/errores.
No aumentar muestra ni cambiar productos por resultados parciales.

Confirmación condicional **1008000–015**, once rivales fijados en confirm1,
base/noop top3 más seleccionadas: 1.152 si una, 1.600 si dos. Gate de prueba
real: ≥3pp contra top3, ningún rival<−20pp, ejecución válida, runtime y mecanismo
revisados. No garantizar superioridad de ladder por diferencias de panel.

Runner `continuar_loop_productos.py` espera a loop5. No lanzar segundo torneo
grande. No incluye envíos automáticos: antes de otro envío considerar evidencia
y edad de top3/VQ activos, coste de perder un control y cupo real disponible.
