# Pre-registro — extensiones de MS: listas de 9 órdenes (msb90b) y lado venta (MSS)

Escrito antes de la confirmación. 2026-09-28 ~09:00 UTC.

- msb90b = msb90 pero actúa también cuando la lista tiene exactamente 9 órdenes (el índice 9
  sigue libre). Criba m (8 semillas × 2 asientos, ref final_xc1_sa_bp_ms90): +$20 de margen
  medio, **96/96 celdas ≥ +$16**.
- msb90b_mss = msb90b + MSS(X≤90) (venta extra de trigo/fertilizante del stock y recompra en
  el índice 9 cuando MS no actúa). Criba k (sobre ms90): MSS +$4-36, mínimo −$2.
- **Confirmación** `torneo_msb1`: ref final_xc1_sa_bp_ms90; brazos msb90b, msb90b_mss;
  rivales tds27, hl836, hl0928, top3cc, fcast2, cha22, hl74; semillas 5080000-5080047; dos
  asientos; pesos `pesos_censo_0928c.json`. Regla: adoptar si IC95 del ponderado > 0 y ningún
  linaje dañado; PROMETEDORA si punto ≥ 0, ningún linaje dañado y margen vs familia tds27
  con IC > 0 (para una extensión del mismo mecanismo ya adoptado, PROMETEDORA basta para
  incluirla en el envío).

## Resultado confirmación (torneo_msb1, 2.016 partidas, 0 errores, semillas 5080000-047)

Referencia final_xc1_sa_bp_ms90 (gana el 96,6%, casi saturado).

| brazo | ponderado | celdas | margen familia tds27 | margen resto | celdas < 0 |
|---|---|---|---|---|---|
| msb90b | +0,31 [−0,32; +0,94] | 1/336, a favor | +22,6 [+20,4; +24,8] | +22 (IC > 0 en todos) | 0/672 (mín +4) |
| msb90b_mss | +0,31 [−0,32; +0,94] | 1/336, a favor | **+30,3 [+27,0; +33,7]** | +43-52 (IC > 0 en todos) | 4/672 (mín −130) |

Ambas **PROMETEDORAS** (y extensiones del mecanismo ya adoptado). Por el desempate fijado
(mayor margen contra la familia tds27): **msb90b_mss** entra en la candidata del 29-sep:
`submission/main_publico_final_29.py` = xc1 + SA + BP + MS(X≤90, también con 9 órdenes) +
MSS(X≤90).
