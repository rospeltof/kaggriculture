# Loop29: misma reventa, dos políticas de partida

48 desarrollos completos frente a V7 reactivo: tres mundos, dos asientos,
VQ/top3, sus noops, dos tamaños sobre cada padre. 8.628 turnos noop exactos
para ambos jugadores; cero errores observados, máximo 330,63 ms. Las fuentes
top3 son byte exacto las de20; sólo se construyeron dos variantes competitivas
nuevas sobre VQ. Total del loop:99 variantes y dos prototipos17 detenidos.

Los cuatro brazos cambian acciones propias en6/6celdas. Cada padre ejecuta
78 ciclos del tamaño20 (1.560unidades) y106 del tamaño50 (5.300unidades).
Total368compras/cierres y13.720unidades, todas verificadas en recibos del motor
con reventa al siguiente turno. Sin pérdidas en las piernas de estos ciclos;
no generalizarlo: la sonda sintética20 demuestra pérdidas con interferencia.

Alimento, trabajo, cosechas, pérdidas nocturnas y tiendas iguales a su padre
en los24juegos candidatos; cero escapes en los48. Producción conservada en
esta cuadrícula, sin garantía general. Ningún W/L/T cambia. Margen por asiento
(ambos asientos coinciden aquí):

| Mundo | VQ base →20 /50 | top3 base →20 /50 |
|---|---|---|
| 1074000 | −1.355 →−1.338 /−1.310 | +233 →+253 /+266 |
| 1074001 | +1.508 →+1.521 /+1.595 | +807 →+820 /+894 |
| 1049013 | −141 →−100 /−29 | +137 →+178 /+249 |

En1074001, las piernas del tamaño20 suman59monedas, pero el margen sólo gana13;
las de50 suman137 y el margen87. Hay efectos posteriores y sobre el rival.
Registrar el flujo no identifica una mejora competitiva. No se eligió tamaño
por dinero ni se alteró la muestra a partir de resultados.

`verificar_reventa_dos_padres.py` valida la cuadrícula, hashes archivados,
controles y todas las cantidades. Evidencia `town_factorial_smoke.*` y
`town_factorial_validation.json`. El runner29 espera tras28 para su piloto
1.568contra el panel cercano y ambas referencias reales. Confirmación disjunta
si pasa selección:1.920/2.560partidas. Preregistro29 conserva tamaños, semillas,
panel y gates; no se suman sus resultados a20como réplicas intercambiables.
