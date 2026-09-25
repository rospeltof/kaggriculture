# Decisión de prueba real: VQ + predictor top3

**Enviada 56537205**, 2026-09-25 01:56:34 UTC, commit `ba1fda8`.
**COMPLETE**, verificado ~02:04 UTC. Replay de validación113099118: 720 pasos,
DONE/DONE, sin errores ni timeouts. Recibo confirma tres envíos restantes.

Envío experimental autorizado por el loop autónomo. Archivo exacto de
confirmación: `submission/main_publico_arshs3_vq_top3.py`, SHA-256
`9668e30ad08f79d485bd230a3c660d4cc420b9382e87f9387b6908e3c94a5145`.
Constructor `construir_loop_publicos.py`, cambio `_V92_P_TOP=3` frente a 1.
Se conservan avisos de licencia y atribuciones del padre público Apache-2.0.

Piloto: +9,375 pp, cuatro semillas y ocho rivales. Confirmación disjunta:
16 semillas, once rivales, ambos asientos; base 78,409%, candidato 89,205%,
**+10,795 pp**. IC95 por semilla [1,234; 20,357], dos vías
**[−0,115; 21,706]**. 20 celdas rival×semilla mejoran y una empeora. En los
ocho rivales originales: +9,375 pp, sin regresión por rival. Panel expandido:
peor rival arshs3 −6,25 pp, mejor tds25 +31,25. No se promete ese salto en Elo.

Cumple gate registrado ≥3 pp y ningún rival <−20 pp. Noop exacto 416/416,
1.600 episodios completos, cero errores, fuentes archivadas verificadas.
Máximo local 757 ms por turno con ocho workers; dentro del segundo nominal,
pero el servidor de Kaggle puede tener rendimiento distinto. Copia byte exacta
al archivo de envío, sin incorporar ningún experimento posterior.

Mecanismo favorable ya reproducido en piloto: primera diferencia en step559,
venta de leche anterior a la presión rival; margen −1.062 → +292, tiendas
iguales y caja conciliada. Se revisó también la única celda negativa de
confirmación: arshs3, seed996011, asiento0, +216 → −425. Primera venta adelantada
de leche step392; 24 turnos de acciones distintos, mismas tiendas y cero
errores. Más cobertura de patrones también causa anticipaciones perjudiciales;
no se oculta ese intercambio ni se culpa a un fallo de ejecución inexistente.

pred_fast2 queda PROMISING (+2,841 pp), sin superar el gate principal. No se
redondea a 3 ni se rescata por +4,688 pp en el subpanel original.

Estado real previo al envío: VQ56535264 2319,5 con 24 episodios listados,
arshs3 original56511619 2275,7. VQ es joven y la lista incluye validación;
no prueba aún que VQ supere al original. El próximo envío desplaza al original
y conserva VQ como control activo, que es el padre exacto de top3. Ambas
políticas quedan archivadas para recuperación. La incertidumbre real se
resolverá con emparejamientos de ladder, además de seguir investigando.

Evidencia: `confirm1.results.json`, `confirm1.validation.json`,
`confirm1.pred_top3.mechanism.json`, `pilot.pred_top3.mechanism.json`,
`top3_package.json` y snapshots API en `docs/evidencia/loop_publicos_20260925/`.
ID, fecha, commit y lecturas posteriores se registran en SUBMISSION_HISTORY.
