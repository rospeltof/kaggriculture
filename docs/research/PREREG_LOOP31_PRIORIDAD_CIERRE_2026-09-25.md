# Loop31: respetar la cola nativa al cerrar la reventa

Registro previo a construir candidatas y ejecutar desarrollo. Confirm20 queda
cerrada con sus resultados originales:20unidades+0,284pp,50+1,136pp; ninguna
pasa gate. En v13/1050019 ambas pierden una victoria al poner SELLWHEAT delante
de SELLMILK13 en661. El diagnóstico aislado sobre la fase real de town50
mantiene estado inicial e inventarios finales y mejora369de margen al preservar
MILK primero. No es un W/L/T de una política corregida ni una estimación global.

## Políticas y controles

Dos candidatas: `close_queue_vq` y `close_queue_top3`, basadas en las fuentes
town50_vq/top3 exactas de29. Tamaño50 fijo; no probar nuevas cantidades aquí.
Sólo en un cierre ya solicitado, mantener la posición de la primera orden
nativa SELLWHEAT, si existía; sustituir su cantidad por el máximo calculado por
TR y retirar duplicados como hacía TR. Si no existía, añadir el cierre al final
de las otras órdenes nativas. Respetar su orden relativo y límite10; no sumar
dos veces trigo ni cambiar compras, unidades, señales o reservas.

La nueva posición puede afectar compras o ventas de otros productos. Medirlo,
sin asumir que el buffer5000 o una fase favorable garantizan invariancia.
Registrar cola que calculó TR y acción finalmente emitida por la nueva capa.
No combinar arreglos de atribución27 ni censura28, ni tocar fuentes20–30.

Desarrollo:1080000/1080001nuevos y1050019dirigido, ambos asientos contra v13
reactivo congelado en20. VQ/top3, sus dos town50 originales, noops de las dos
town50 y las dos candidatas:48partidas. Noops de ambos jugadores exactos,
720DONE/caja conciliada,0errores, max<1s; cantidades solicitadas, compradas y
vendidas, prioridades emitidas, alimento/cosechas/tiendas/pérdidas/escapes.
Cada nueva capa debe cambiar acciones frente a su town50 en al menos un mundo.
No seleccionar por dinero ni resultados de desarrollo.

## Piloto y confirmación

Después de30, único torneo principal. Piloto1081000–1081015contra panel25:
mirrorVQ/mirrorTop3/V7/HS4. VQbase/noop,top3control, dos town50 como controles
ineligibles y dos candidatas=1.568episodios, ambos asientos. Estimar todos los
contrastes exclusivamente sobre los cuatro rivales, excluyendo otros brazos.
Elegir hasta dos con deltaW/L/Tpositivo frente aVQy top3 y≥0frente a su town50;
ordenar por mínimo delta de las dos referencias reales y nombre.

Confirmación1082000–1082031, añadeHarvest68/arshs3. Conservar sólo las town50
correspondientes a candidatas seleccionadas: una=5brazos/2.560episodios;
dos=7brazos/4.032. Gate≥3ppvsVQ,≥0vstop3 y≥0vs su town50; peor rival≥−20pp
frente a las tres referencias, acciones propias distintas en≥2semillas contra
su town50. Controles, ICpor semilla/dos vías, fuente/runtime y revisión física.
Comprobar explícitamente exclusión de controles en el analizador antes de correr.

No redefinir20ni29, sumar Nentre poblaciones o ampliar muestra por resultados.
Antes de un envío, revisar hashes alternativos, cuota y submission desplazada.
Sin autoenvío. Sin selección se conserva la evidencia y continúa otra hipótesis.
