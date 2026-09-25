# Referencias públicas actualizadas: tds y Harvest Ledger

Registrado antes de medir estas versiones. Es una comparación nueva: ambos
archivos cambiaron respecto a los hashes de los torneos rr1–rr4.

- [tds](https://www.kaggle.com/code/tetsutani/demand-preserving-turn-sale-timing):
  última ejecución pública 2026-09-24 16:06 UTC; SHA descargado **127ed3e6**,
  antes 178ae0f7. Nuevo paquete de aproximadamente 0,5 MB y capas MG/IG de cola;
  no asumir equivalencia conductual por mantener el título del notebook.
- [Harvest Ledger](https://www.kaggle.com/code/haodou092/kaggriculture-harvest-ledger):
  ejecución 2026-09-24 09:18 UTC; nuevo SHA **1dfd4630**, antes 37d284d4.
  Cambio de producción: precios esperados de trigo/zanahoria a tres días, mezcla
  80% futuro / 20% observado, siembras hasta d26, buffer de semillas 6. Riesgo:
  sobreestimar oferta que no se cosechará y perjudicar alimento/producción.

Archivos descargados en `results/publicos_20260925/`, hashes y fecha del listado
en `docs/evidencia/research_20260925/`. Avisos Apache-2.0 conservados. Auditoría
estática: stdlib, exec de cadenas constantes; remove sobre listas; único open
en rama desactivada por path=None. No ejecutar notebooks ni scripts de descarga.

**Hipótesis de alto potencial:** una producción y logística distintas pueden
superar a arshs3vq donde micro-capas sólo intercambian partidas. Confianza LOW;
las versiones nuevas son candidatas, no mejoras ya demostradas.

## Diseño

Reutilizar `torneo.py`, sin editarlo durante bloques. Base/noop arshs3vq,
tds25 y hl25; ocho rivales congelados del piloto forecast: tds anterior, hybu,
ars40, hsov, v13, obr, h2965, guru6. Semillas **992000–992007**, ambos asientos,
38 cruces = **608 episodios**. En pares con tds antiguo se mide también cambio
de versión. Directos entre brazos se reportan aparte. No mezclar rating ajeno
anunciado con nuestros resultados medidos.

Primario: delta pareado W/L/T vs base por rival/semilla, asientos promediados,
IC95 semilla y dos vías, desglose por rival. Noop exacto y cero errores.

Selección exploratoria por mayor delta global, desempate alfabético. Si el mejor
alcanza ≥+5 y al menos dos rivales positivos sin ninguno <−20, PROMISING:
confirmar únicamente ese candidato frente a base/noop en **993000–993015**, mismo
pool y ambos asientos (27 cruces ×32 = **864 episodios**). Confirmación no se
fusiona con piloto ni se amplía al mirar resultados. Si el punto de confirmación
es ≥+5 y no hay regresión >20 por rival, puede justificar un envío como
REAL_WORLD_CANDIDATE con incertidumbre explícita. No promover champion sólo por
esta selección; exige respuesta real. Si no cumple, conservar resultado y causa,
sin reenviar otra versión casi idéntica a modo de boleto.

Un resultado ≤0 o un IC que cruza cero no prueban inutilidad universal del
mecanismo: sólo impiden gastar el bloque registrado en estas versiones. Si una
regresión contiene información de mecanismo útil, investigar esa diferencia en
otra hipótesis registrada. No lanzar ambos bloques a la vez con 16 workers;
esperar que termine forecast y conservar su evidencia.
