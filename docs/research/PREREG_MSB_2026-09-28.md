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
