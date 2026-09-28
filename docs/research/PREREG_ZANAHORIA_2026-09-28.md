# Pre-registro — dosis-respuesta de _CA_MARGIN (más conversión trigo → zanahoria)

Escrito antes de evaluar. 2026-09-28 ~00:50 UTC.

- **Mecanismo:** CARROT2 convierte trigo en zanahoria si
  3·(p_zanahoria − _CA_DROP) − 20 > 4·p_trigo − 10 + _CA_MARGIN. Más negativo → más
  zanahoria. Base tds27top3: −15. Barrido: −22 +3,1 (etapa 1) y +5,0 (etapa 2);
  −8 −6,9. Los privados que nos ganan plantan más zanahoria en la segunda mitad.
- **Brazos:** ref (tds27top3), cam22, cam30, cam40 (asignación al final del módulo).
- **Evaluación:** `torneo.py --out results/torneo_zanahoria --sin-cruces`, rivales
  tds27, cha22, hl836, top3cc, hl74; semillas 4630000-4630031 (32 nuevas), dos
  asientos; pesos `pesos_barrido_0928.json`.
- **Regla:** adoptar el brazo con mayor punto si su delta ponderado tiene IC95 por
  semilla > 0 y ningún linaje con IC entero < −10 pp. Si cam22 lo cumple, pasa a
  sustituir a tds27top3 en el slot 1; si lo cumple cam30/cam40, a probar en real.

## Resultado (torneo_zanahoria, 1.280 partidas, 0 errores, semillas 4630000-031)

cam22 **−0,23** [−6,09; +5,62]; cam30 −1,25 [−8,08; +5,58]; **cam40 −11,02 [−20,20; −1,83]**
(peor, IC excluye 0). Ningún brazo se adopta. "Más zanahoria" no es palanca: óptimo
cerca de −15..−22; cam22 ≈ neutro en tres bloques (+3,1 / +5,0 / −0,2). La submission
56624199 (cam22) queda como segunda tirada del mismo nivel que tds27top3.
