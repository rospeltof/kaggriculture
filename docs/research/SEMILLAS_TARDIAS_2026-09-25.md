# Semillas tardías: auditoría y desarrollo del loop26

Corte: 2026-09-25, 09:11 UTC. Dos políticas nuevas sobre VQ, todavía sin
resultados competitivos. El loop26 espera al bloque25; no hay otro torneo
principal ejecutándose. Registro previo: `PREREG_LOOP26_SEMILLAS_2026-09-25.md`.

## Evidencia que motivó la prueba

`auditar_semillas_tardias.py` concilia 18 replays ya elegidos por recencia en
0653/0742/0828, sin escoger victorias o derrotas. Fuentes exactas reproducidas
anteriormente, compras aceptadas en ledger y consumo de semillas por turno.
Quedaron 54 semillas de trigo en 16 partidas y 7 de zanahoria en dos. Después
del paso624 se compraron 99 de trigo y 255 de zanahoria.

Una auditoría con órdenes futuras congeladas permite quitar 42 compras de
trigo (420 monedas) y 7 de zanahoria (140 monedas), respetando la validación
atómica de PLANT: no basta con conservar el consumo realizado, porque el motor
puede exigir todas las semillas solicitadas para aceptar una acción. Esto es
un diagnóstico con futuro conocido, no una política desplegable ni beneficio
competitivo demostrado.

La guarda E402 ya recorta compras tardías, pero utiliza la suma de PLANT de
trigo y zanahoria como cota para cada cultivo. La conversión CA puede cambiar
trigo por zanahoria hasta el día28. Se mantiene intacta la compra de zanahoria.

## Políticas congeladas y desarrollo

- `seed_kind`, SHA ac36e98c1cd9059e07ba543ffea4405535f8157a71c9949b002f04bf9c62a510:
  recorta trigo usando sólo PLANT WHEAT restantes y reparaciones pendientes.
- `seed_jit`, SHA 68433a06df1a7eea7e5e2cedc7335dd8b9aac65458511ead4acba5077c6383cd:
  reserva semillas para el próximo turno nativo y todas las reparaciones
  pendientes; proyecta las acciones actuales y puede reponer donde el padre
  no compra. Rechazo por fondos/slots conserva la acción padre completa.

Ambas operan desde624 hasta718, con observación y planes propios disponibles.
No alteran comandos de campo ni acceden a futuro rival o a la semilla del mundo.
El total construido pasa a 91 variantes competitivas y dos prototipos17
retenidos; estos últimos siguen sin piloto.

40 juegos de desarrollo: cuatro mundos, ambos asientos contra arshs3 reactivo,
VQ/noopVQ/top3 y las dos variantes. Runtime fijo PYTHONHASHSEED=0. Noop exacto
5.752 turnos; máximo327,19ms. Se archivan fuentes, ledger y eventos físicos de
unidades antes/después de la aplicación del motor. Validación PASS.

| Mundo | Trigo comprado base/kind/JIT | Semillas finales base/kind/JIT | Ahorro kind/JIT | Turnos de mercado cambiados kind/JIT |
|---|---|---|---|---|
|1065000|164 / 163 / 163|1 / 0 / 0|10 / 10|1 / 11|
|1065001|166 / 166 / 166|0 / 0 / 0|0 / 0|0 / 10|
|102886466|160 / 160 / 158|5 / 5 / 3|0 / 20|0 / 6|
|1943089929|166 / 166 / 166|0 / 0 / 0|0 / 0|0 / 10|

Las dos plazas dan los mismos valores de esta tabla. Kind activa dos de ocho
celdas; JIT las ocho. Los 76 turnos modificados tienen cantidades de compra
aceptadas exactas, incluida reposición sin compra original. Todas las órdenes
de campo, PLANT/FEED/CARE/HARVEST/FERT efectivos, tiendas, escapes, pérdidas
nocturnas y composición final se conservan frente a VQ en estos mundos.
Cero errores observados y rechazos de slots/presupuesto. Cero escapes propios
y productos finales; sí quedan semillas y pérdidas nocturnas, iguales a base.
Por ejemplo1065001 conserva pérdidas de trigo/fresa/lana/fertilizante en575
más trigo/fertilizante en671. No afirmar ausencia de desperdicio general.

No cambia ningún W/L/T de desarrollo: todos ganan a este rival. Ahorrar dinero
no acredita mejora. La conservación mecánica está comprobada en estos cuatro
mundos, no garantizada para todos los contextos. JIT conserva tres semillas en
102886466: el siguiente plan nativo puede terminar convertido por CA.

## Evaluación en espera

Piloto960 juegos en1066000–1066015 contra VQ/top3/V7/HS4; selección positiva
frente a ambas referencias. Confirmación disjunta1067000–1067031 agrega
Harvest68 y arshs3, 1.920/2.560 juegos según seleccionadas. Gate registrado:
≥3pp frente a VQ, ≥0 frente a top3, peor rival≥−20pp frente a ambas y acciones
propias distintas en al menos dos semillas. Revisión física y sensibilidad a
hashes alternativos antes de proponer un envío. Sin envío automático.

Evidencia: `docs/evidencia/loop_publicos_20260925/late_seed_*`. Construcción:
`construir_semillas_tardias.py`; verificación: `verificar_semillas_tardias.py`;
runner: `continuar_loop_semillas_tardias.py`. No modificar fuentes congeladas.

Consulta pública adicional09:01 UTC: las 50 entradas del catálogo no cambian
ref ni lastRunTime respecto de08:03. No se descargan duplicados. Esto no prueba
que no existan cambios fuera de esa página o código privado nuevo.
