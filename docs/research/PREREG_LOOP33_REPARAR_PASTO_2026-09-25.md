# Loop33: completar instalación animal en terreno que quedó vacío

Registro antes de construir candidatos o ejecutar desarrollo. Replay113252591:
DIG33 limpia maleza, pero el trabajador sale sin BUILD_PASTURE; PLACE_COW69
falla y la vaca queda en almacén. No repetir reparación de siembras del loop2.
No hay prueba todavía de que corregir esto mejore resultado competitivo.

## Dos candidatas

`animal_build_vq` y `animal_build_top3`, sobre referencias reales exactas.
Sólo una orden final PLACE de COW/SHEEP/GOOSE, animal realmente en mano,
casilla propia vacía (None), hora≤21 y paso<648. No quitar plantas/maleza ni
mover trabajadores. Los dos siguientes comandos de la ruta nativa del mismo
actor deben ser exactamente CARE y PASS, antes del cambio de día. Evitar
conflictos con otra unidad que ejecute una operación de terreno allí.

Reemplazar las tres órdenes por BUILD_PASTURE/BUILD_COOP, PLACE del animal,
y CARE. La construcción es una acción sin coste monetario en el motor vigente.
Confirmar estructura y animal observado antes de la siguiente etapa; si el
actor se desplaza, la casilla cambia o la orden final deja de ser la esperada,
abortar el resto y registrar. No sacrificar otra tarea nueva ni cambiar compras,
contrataciones o rutas. CARE emitido al último turno se verifica en el motor,
no con el flag de la mañana siguiente, que ya fue reiniciado.

Registrar cola original y orden emitida, construcción ejecutada, animal
consumido/colocado, cuidado, alimentación, cosechas, caja, tiendas y escapes.
Más producción puede cambiar precios y RNG/tiendas: no presumir invariancia.

## Desarrollo y decisión

VQ/top3, dos capas deshabilitadas y dos candidatas, semillas1086000/1086001
y2146809967 del replay, ambos asientos contra mirrorVQ congelado de25:
36partidas. Noops de ambos jugadores/rewards,720DONE,0errores, max<1s,
caja conciliada, cada candidata activa en≥1mundo, ciclo físico comprobado.
La cobertura dirigida no estima prevalencia; no seleccionar por margen.
Si falta cobertura, registrar primero y sólo después considerar adenda.

Tras32, piloto1087000–1087015 contra los cuatro rivales de25,
VQ/noop/top3/dos candidatas=960partidas. Seleccionar hasta dos con delta
estrictamente positivo frente aVQy top3, ordenar por el menor delta y nombre.
Confirmación1088000–1088031, seis rivales de25,1.920/2.560partidas.
Gate≥3ppvsVQ,≥0vstop3, peor rival≥−20ppfrente a ambas; acciones propias distintas
en≥2semillas contra padre correspondiente. ICpor semilla/dos vías, fuentes
congeladas, hashseed0y controles. No sumarNcon replay ni desarrollo ni otros loops.

Antes de una submission: revisar cambios físicos, hashes alternativos, cuota y
agente que desplazaría. Sin autoenvío. No modificar fuentes en bloques activos.
