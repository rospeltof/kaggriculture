# Loop20: nuevas compras y reventas alrededor del consumo del pueblo

Registrado antes de construir y simular agentes. Loop19 modifica únicamente
compras grandes ya presentes en cinco de64pares de tiendas. Aquí se crean
operaciones nuevas donde la política heredada no tenía órdenes de mercado.
No se combina con los brazos19ni se espera su resultado para elegir tamaños.

La sonda sintética `town_roundtrip_probe.json` concilia800piernas de mercado
en400escenarios. El beneficio sin rival NO está garantizado:78casos pierden
dinero pese a beneficio positivo del modelo sin rival, y dos ganan dinero
propio pero empeoran margen frente a abstenerse. Es una motivación para
medir contra rivales reactivos, no un modelo de beneficio causal.

Tres brazos sobre top3: `town20`, `town50`, `town80`, con esos máximos de
unidades. Pasos288–695, horas4/8/12/16/20 (consumo conocido, sin medianoche).
Sólo si hay demanda actual de trigo; mercado final del padre vacío ahora y
mercado de cinta propia vacío el turno siguiente; ninguna acción de unidad
PICKUP/DROP/PLACE en esos dos planes. Capacidad libre menos cinco unidades,
caja remanente al menos5.000estimada al coste con100compras rivales previas,
y beneficio anunciado por curva sin rival estrictamente positivo.
No usar información futura rival ni privada ajena. La cinta propia futura es
un plan conocido, no garantía de ejecución. El tamaño puede reducirse por
caja/capacidad; los tres nombres son topes, no llenados garantizados.

Al turno siguiente se observa cuántas unidades compró el motor por cambio
del trigo privado (sin operaciones propias de shed en la compra ni noche).
La política solicita venderlas en primer slot, integrando cualquier SELLWHEAT
ya solicitado por el padre mediante máximo, no suma. Las unidades siguen
intactas. Si una decisión reactiva de PICKUP consume ese trigo, se registra
el desvío y la venta se limita por el shed; no se roba alimento ni se mantiene
una posición oculta. No nuevas compras mientras hay liquidación pendiente.
El efecto total puede alterar alimentación, ventas, precios y respuesta rival.

Desarrollo fijo:1048000/1048001nuevos en partidas y588616997contexto de
reventas reales, ambos asientos contra arshs3, base/tres/noop=30juegos.
Verificar noop completo, fuentes,720DONE/caja, activación, llenados compra
y venta, desvíos/órdenes heredadas, comida/cosecha/escapes, inventario final,
errores y máximo<1segundo. El dinero diagnóstico no selecciona brazos.
Detener/reparar por fallo de implementación; no borrar una pérdida económica.

Piloto1049000–1049031, cuatro rivales fijos arshs3/tds/hybu/ars40, ambos
asientos:1.920episodios. Unidad semilla, W/L/T pareado primario; hasta dos
deltas positivos por magnitud y nombre. Noop/hash, cero errores y cobertura
de acciones; no parar ni escoger por recompensas parciales.

Confirmación1050000–1050031, once rivales,2.304/3.200episodios. Gate≥3pp,
peor rival≥−20pp, IC95dos vías, mecanismo y tiempo. Muestras disjuntas.
Encolar después de19sólo tras validar desarrollo. Sin envío automático;
cualquier prueba real requiere evaluar riesgo de desplazar VQ y evidencia.

Desarrollo terminado:30juegos/noop4.314/max358ms.146compras y cierres exactos,
7.862unidades,42ventas heredadas integradas sin duplicación. Cero errores,
escapes o productos terminales; alimento/cosecha/tiendas/pérdidas preservados
en esos tres mundos. Validación aprobada, runner20encolado detrás de19.
