# Loop28: ausencia de ventas observables frente a ausencia de ventas reales

Registro previo a construir candidatas y ejecutar desarrollo. La auditoría
offline de las seis trayectorias reales0914reproduce exactamente1.650selecciones
nativas dePREDICT. El matcher penaliza un evento de biblioteca sin pareja incluso
si ese producto/turno no era observable por su propio filtro de precio.

Se registraron dos máscaras antes de analizarlas: elegibilidad nativa(precio
anterior>3) y elegibilidad más ausencia de mínimo alcanzado al terminar mercado.
Ambas alteran selecciones y señales en los seis replays. No son acciones nuevas
ni resultados competitivos: los futuros rivales quedan grabados en ese diagnóstico.
No seleccionar la máscara por acierto offline, dinero o resultado del replay.

## Cuatro políticas sin combinar la corrección27

Factorial padreVQ/top3 × máscara`native`/`floor`. Cada política mantiene los
eventos positivos observados y el coste nativo de eventos observados sin pareja.
Sólo evita penalizar una venta de biblioteca ausente cuando no fueron observables
los tres turnos de su vecindad±1. Conserva ventana240, pesos, umbrales, orden
estable de empates, número de patrones de cada padre y `_hp_quantity`.

Native: un turno es observable si el precio anterior era>3, igual que el filtro
que permite registrar la observación original. Floor: además reconstruir stock
justo después del mercado como stock actual+consumo conocido del pueblo anterior;
exigir precio>1a ese stock. Para los productos premium, que no pueden comprarse,
el stock de mercado crece durante las ventas; el mínimo rompe su identificación.
La máscara se calcula sólo con información pública disponible al decidir ahora.
No usar recibos reales, acciones rivales, semilla del mundo ni precios futuros.

Modificar únicamente el rankingPREDICT. PREDICT2y el detector de carreras
permanecen con su código nativo. No purgar eventos positivos ni corregir la
instantánea de ventas propias en este experimento; ese cambio ya es loop27.
Registrar esa limitación, sin llamar la máscara inferencia perfecta.

## Desarrollo fijo

1071000/1071001nuevos y2111590720dirigido, ambos asientos contraV7reactivo del
panel25. VQ/top3,noop de cada uno y cuatro candidatas:48partidas. Fuentes y
acciones archivadas, runtimePYTHONHASHSEED0,720DONE, caja y cantidades físicas,
errores observados0, máximo<1segundo. Noops exactos de ambos jugadores.
Comprobar máscara contra ledger oficial: todo turno declarado observable por
floor debe tener incremento de mercado igual a ventas premium totales aceptadas.
Registrar rankings y acciones distintas por candidata; cada una debe cambiar
acciones en al menos un mundo antes de competir. No escoger por rewards.
Medir alimentación/cosecha/tiendas/escapes/pérdidas/stock terminal sin exigir
invariancia: el cambio de ventas puede modificar decisiones económicas futuras.

## Piloto y confirmación

Después de27, un único torneo grande. Piloto1072000–1072015, cuatro rivales
mirrorVQ/mirrorTop3/V7/HS4 del manifiesto25, ambos asientos. BaseVQ/noopVQ,
top3control y cuatro políticas:1.568partidas. Hasta dos con deltaW/L/Tpositivo
frente a ambas referencias, orden por menor delta y nombre. Excluir cruces
entre brazos de los estimadores, sin cambiar paneles previos.

Confirmación1073000–1073031, mismos cuatro másHarvest68/arshs3:1.920/2.560
episodios para una/dos candidatas. Gate≥3ppfrente aVQ,≥0frente atop3, peor
rival≥−20pp frente a ambas, acciones propias distintas en≥2semillas frente a
su padre, controles y revisión mecánica/runtime. IC por semilla y dos vías;
forks no son linajes independientes por tener otro nombre. Antes de enviar,
sensibilidad a hashes y qué referencia real desplazaría. Sin envío automático.

Fuentes de27y paneles20–27intactos. Ausencia de selección implica seguir con
otra hipótesis, no ampliar muestras mirando resultados ni relajar el gate.
