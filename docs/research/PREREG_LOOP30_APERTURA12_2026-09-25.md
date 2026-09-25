# Loop30: tamaño de la reventa inicial, conservando cinco trigos

Registrado antes de construir candidatas y jugar partidas completas. La auditoría
previa evaluó q=5/8/12/20/43 en el primer turno de los13replays de recencia0914
y1003, ambos asientos:130escenarios parciales. El control8 reproduce los13
estados originales. Stock final, semillas y trabajo son iguales; sólo difiere caja.
Q12 da margen medio+1,231, peor−6;5/20/43 tienen media negativa y ninguna celda
positiva. Esto es descubrimiento sobre aperturas grabadas, no una estimación
de fuerza ni prueba de dominancia. Conservar todos los resultados explorados.

Probar sólo `open12_vq` y `open12_top3`: cambiar la constante de apertura de
BUY8/SELL3 a BUY12/SELL7, dejando el mismo stock5 y todas las demás órdenes.
Nada de nueva producción, modificación de la primera vaca, reventa posterior,
adelanto de compras, señales extra, semillas o correcciones de inferencia.
Loop12 cambió cultivos/apertura productiva;19excluyó expresamente aperturas;
20/29 operan después de288. Esta variable aún no tuvo torneo competitivo.

## Desarrollo y controles

1077000nuevo y362118074dirigido, ambos asientos frente a mirrorVQ yV7reactivos
del manifiesto25. Dos padres, sus noops de apertura8 y dos candidatas:48juegos.
Fuentes/acciones archivadas, runtimehash0,720DONE/caja conciliada,0errores y
max<1s. Noops exactos de ambos jugadores. Confirmar que BUY12/SELL7 llegan al
motor en0, ambas cantidades llenan y el stock es5en1; no vuelve a cambiarse
la apertura en pasos posteriores. Registrar mínimas cajas por día, compras,
semillas, HIRE, campo/alimento/cosecha/pérdidas/tiendas/escapes y stock final.
No exigir producción idéntica: pequeñas diferencias de caja pueden cambiar
decisiones. Ambas políticas deben cambiar acciones antes del piloto.
No elegir por rewards ni excluir una pérdida como supuesto fallo técnico.

## Panel, selección y confirmación

Después de29, único torneo principal. Piloto1078000–1078015contra mirrorVQ,
mirrorTop3,V7,HS4del panel25, ambos asientos:VQbase/noopVQ/top3control y las dos
candidatas=960episodios. Seleccionar hasta dos con deltaW/L/Testrictamente
positivo frente a ambas referencias; ordenar por menor delta y nombre.

Confirmación1079000–1079031contra los cuatro másHarvest68/arshs3;1.920/2.560
episodios con una/dos seleccionadas. Gate≥3ppvsVQ y≥0vstop3, peor rival≥−20pp
contra ambas, acciones propias distintas en≥2semillas contra su padre,
controles exactos, mecanismo y runtime. ICpor semilla y dos vías; no tratar
forks como linajes independientes. No ampliar muestras mirando resultados.

No añadir nuevas cantidades por resultados de desarrollo/piloto. No cambiar
fuentes/paneles20–29. Antes de enviar: hashes alternativos, cuota y referencia
desplazada, además de las comprobaciones anteriores. Sin autoenvío.
