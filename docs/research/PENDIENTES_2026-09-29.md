# Pendientes para el 29-30 de septiembre (escrito 28-sep ~09:30 UTC)

1. **00:00 UTC del 29:** enviar `submission/main_publico_final_29.py` (sha cf129189) con
   `kaggle competitions submit -c kaggriculture -f submission/main.py` tras copiarlo a
   `submission/main.py`; registrar en SUBMISSION_HISTORY.json. Desplaza a final_frps
   (56626892); par activo: final_xc1 (56628181) + final_29.
2. **Durante el 29:** bajar sus partidas reales (`bajar_lider.py <id> FINAL29_LADDER_0929a`,
   carpetas nuevas por tanda), `resumen_ladder.py`, censo si hay >= 40 partidas. Comparar con
   final_xc1 en la misma franja (74% a ~2380).
3. **Segundo hueco del par final (decidir el 29-30):** mantener final_xc1 como cobertura, o
   sustituirla por otra variante fuerte de la misma familia si final_29 rinde en real como
   en el harness (+7,55 pp frente a final_xc1).
4. **Vigilar públicos nuevos** (tetsutani y forks). Si aparece una base mejor, reaplicar
   nuestras capas en este orden: TOP=3, combo (S738_LOOK=6, SR_MARGIN=12), CA_MARGIN=-22,
   FR+pre-venta (`apilar_frontrun.py --preventa`), XC (`apilar_pases.py 1 --cxd`), SA (línea
   del peón de ovejas), BP (`apilar_compra_tras_ventas.py`), MS (`apilar_mini_spec.py 90`,
   con `>= 10` en la comprobación de longitud), MSS (`apilar_mini_spec_venta.py 90`).
5. Ideas pequeñas no probadas: MS con segundo hueco para trigo cuando también se compra
   fertilizante; MSS cuando MS ya actuó (índice 8). Descartadas: WF, FG, BF, MS-siempre,
   guardia de hueco estricta, courier, presupuesto de reordenación.

## Cribas extra del 28-sep (tarde), sin cambios en final_29

- MS con dos productos (trigo y fertilizante en el mismo paso, índices 8 y 9): inerte en
  200 partidas (criba o).
- Ablaciones de capas de venta de tds27 sobre final_29 (criba p, 8 semillas × 2 asientos):
  sin S928 −$48/−$66 contra la familia tds27; sin S948 −$82 contra la familia tds27 pero
  +$95/+$135 contra cha22/fcast2; sin S758 −$190 contra la familia tds27. Esas capas ganan
  la carrera contra espejos; se mantienen. (Idea no probada: apagar S948 solo si el rival no
  es de la familia tds27; ganancia ponderada estimada ~+$30.)

## Exploración 12:30 UTC del 28-sep

- Harvest Ledger 12:01 (`results/exp_0928b/rival_hld.py`, sha 8cffc452): quita la inclinación
  de zanahoria con PET_CAFE y añade una guarda "fail-closed" (acción PASS si el padre falla);
  juego = tds27. final_29 16-0 (+$906), final_xc1 16-0 (+$385).
- flexonafft multi-route 10:57 (`rival_mroute2.py`, sha 489f5d19, 75 KB): trayectoria
  destilada de un episodio (Lev Neganov) con controlador; código embebido auditado
  estáticamente (solo stdlib, sin llamadas sensibles). final_29 y final_xc1 16-0 (+$33.000).
- Ladder 12:30: final_xc1 2368, final_frps 1453.

## Exploración 18:30 UTC del 28-sep

- tetsutani re-ejecutó su notebook a las 17:41: mismo main.py (55be5d5f = tds27). Sin cambios.
- God's mode (leoprovorov, 16:31; agente multifichero: base tipo tds + capa de predicción de
  tiendas), decodificado y auditado sin ejecutar (`results/publicos_0928e/godsmode_agent/`):
  final_29 12-0 (+$1.761), final_xc1 12-0 (+$1.080).
- Tiempo por turno: con `--fresco` y 11 procesos arrancando a la vez los máximos suben a
  1,4-2 s por contención de carga (también en el rival); sin contención final_29 y final_xc1
  tienen máximo ~90 ms y media ~1,7 ms (`tiempo_f29`). Sin problema de tiempo.
- Ladder 18:30: final_xc1 2345, final_frps 1496.

## Forks casi-tds27 que ganaron a final_xc1 (diff_fork.py, 28-sep ~20:00 UTC)

- naniwazu (ep 114550917): vende más leche/huevo y antes (MILK 6 en vez de 3; EGG a la hora 2).
- JezzLynn (ep 114566714): otro orden de ventas (leche y fresa antes que trigo; fertilizante
  primero) y lana 5 en el paso 600: carrera de índice, lo mismo que ataca XC.
- Nagahama (ep 114599272): vende más fresa (20 en vez de 10) y más fertilizante/trigo en pasos
  concretos.
Son los mismos tipos de retoque que ya tenemos (XC para el orden, LOOK 6 y MS para la carrera
de venta/compra). No hay nada nuevo que adoptar. Herramienta: `diff_fork.py <replay> <asiento>
<candidato.py> [N]`.
