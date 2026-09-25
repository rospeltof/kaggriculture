# Loop7: tomate en tierra ya comprada, sin sustituir al padre

Hipótesis nueva tras inspeccionar la interacción de loop5: utilizar cuatro u
ocho tiles vacíos de las filas7–8 del cuadrante SE, sin comprar tierra ni
ocupar las filas5–6 de ovejas/V219. Padre **top3**, sha9668e30a. Las variantes
del loop5 siguen congeladas y no se modifican por esta idea posterior.

Cuatro brazos: infill4_d16, infill8_d16, infill4_d18, infill8_d18. No usan
fertilizante: cuatro producciones por planta, riego en edades0/2/4/6/8/10
y cosechas de dos unidades en edades9/11. Una cuadrilla adicional por grupo de
cuatro plantas. Contratar sólo cuando finalicen las contrataciones nativas y
los proyectos existentes hayan reservado sus trabajadores; usar índices
observados y confirmar contratación. Comprobar tiempo de siembra+riego y
preservar las acciones de trabajadores anteriores.

Inversión sólo si ingreso modelado ≥ semillas+jornales proyectados+600. Oferta
visible de ambos jugadores con vida finita, expectativas de tiendas futuras,
coste de peones por día y reserva de caja actual4.000. El modelo omite decisiones
futuras no observadas y el efecto sobre otros proyectos/precios, por lo que el
beneficio calculado es criterio experimental, no una garantía de rentabilidad.

Fuente `capa_tomate_relleno.py`, constructor `construir_tomate_relleno.py`.
Antes de simulación, revisión estática corrigió acumulación del coste de HIRE
del padre y venta posterior a la última cosecha. Los cuatro prototipos v1 no
se evaluaron. V2 completó16 diagnósticos, pero la auditoría de jornales detectó
que contratar en horas1–3 inhibía al fertilizador R51 del padre: exige que todos
los trabajadores actuales pertenezcan a módulos que conoce. **V3 contrata sólo
desde hora4**, tras cerrar la ventana R51, y conserva las comprobaciones de
tiempo/índices. Repetir16 diagnósticos por esta corrección antes del piloto.
V3 pasó16 diagnósticos y conservó R51 (un peón/siete aplicaciones), pero el
caso forced8 vendió28 de32 tomates: al amanecer28 perdió cuatro por overflow.
Flujo guardado en `infill_v3_forced8_flow.json`. **V4 separa riego y cosecha**
durante madurez: WATER8, HARVEST9 (dos unidades), WATER10, HARVEST11 (dos).
Mismos ocho días de contratación, más tiempo para entregar; modelo económico
ajustado a ventas agrupadas9/11. Repetir validación de conservación/venta antes
del piloto. No modificar V2/V3 archivados ni sus resultados. Noop con tamaño0 y dos variantes forzadas
sólo para comprobar ejecución; jamás incluirlas en el piloto ni subirlas.

Desarrollo: seed1004000 ya conocida como mundo SE con ovejas; ocho brazos
(base, cuatro normales, noop, dos forzados)×ambos asientos =16 episodios. No
inferir rendimiento de esa elección dirigida. Conciliar caja, confirmar
plantas/cosechas, observar supervivencia del proyecto ovino, cero errores.
Un defecto observado exige corregir/versionar y validar antes de congelar.

Piloto de cobertura: **1010000–1010015**, ambos asientos, cuatro rivales fijados
ahora: arshs3 original, tds, hybu y ars40. Base/noop top3 +cuatro brazos nuevos:
24 cruces con pool +15 entre brazos, ×32 =**1.248 episodios**. Mayor número de
mundos para activar condiciones espaciales/económicas, sin seleccionar semillas
que contengan tiendas concretas. Reportar proporción de acciones cambiadas;
primario delta W/L/T contra top3 en cuatro rivales comunes, unidad semilla.

Seleccionar hasta dos brazos con delta>0, orden delta y empate alfabético.
Confirmación disjunta **1011000–1011015**, once rivales de confirm1 y ambos
asientos; 1.152/1.600 episodios según una/dos seleccionadas. Reportar además
subpanel de los cuatro rivales del piloto. IC95 por semilla y dos vías cuando
estimable. Gate real ≥3pp frente a top3, ningún rival<−20pp, controles y runtime
válidos, revisión de mecanismo. No promover por dinero bruto o por los casos
forzados de desarrollo. Una activación rara sin efecto deja la pregunta abierta.

Runner espera a loop6, nunca dos torneos grandes simultáneos. No incluye envíos
automáticos; considerar edad/evidencia de top3 y VQ antes de desplazar una activa.

Validación V4 completada:16 episodios, noop1.438 acciones idénticas, R51 siete
aplicaciones y108 lanas del proyecto preservadas. Forzados4/8 cosechan/venden
16/32 unidades. Sin errores ni contrataciones faltantes. Cuatro normales
inertes por gate económico en este mundo dirigido; no usarlo como selección.
Manifiesto congelado `infill_variants.json`; fuentes v2/v3/v4 archivadas en
`infill_development.sources.tgz`. Piloto encolado detrás de loop6.
