# Pre-registro — guardia contra copiadores de MS (f29g)

Escrito antes de la confirmación: 2026-09-29 21:20 UTC. No se cambia nada tras ver resultados.

## Variante
`results/guarda_0929/f29g.py` (sha a77f667c) = bytes de final_29 intactos (prefijo sha cf129189)
+ capa GS (`apilar_guarda_ms.py`, sha a7affe6b). Tras cada paso en que nuestra acción final lleva
la firma MS o MSS (144 ≤ t < 700), simula exactamente el mercado contra un rival «benigno» (una
orden por producto en cualquier índice) y mide gap = mínimo benigno − dinero observado. Apaga MS
y MSS el resto de la partida si gap > 150, o al segundo golpe > 20 (paso MS) / > 60 (paso MSS).
Solo lee; sin disparo, las acciones son las de final_29.

## Evidencia previa (workflow `guarda-copiadores-ms`, 6 agentes, 2 revisores aptos)
- Copiadores reales: 8 de los últimos 33 rivales de final_29 compran X extra y revenden antes
  de nuestro índice 9; código privado (ningún notebook público lo contiene).
- En los replays de final_29 (dentro de muestra), la capa real dispara en los 8 copiadores y en
  0 de 124 sin copiador. Resimulación con el motor y la cinta rival grabada: +32.773 de margen,
  3 derrotas → victorias.
- **Fuera de muestra** (191 replays de final_xc1, cinta rival grabada): 12 disparos; 10 son
  copiadores o sándwiches reales, 1 falso positivo (HireMe, −73, sigue ganando), 1 dudoso (+151).
  +27.206 de margen (+142/partida), 1 derrota → victoria, 0 victorias → derrota.
- Humo local: identidad 36/36 + 16/16 celdas; contra 4 copiadores sintéticos, victorias 22/48 → 30/48.

## Confirmación (semillas nuevas, PYTHONHASHSEED=0, nice 15)
- `confirm_guarda_cp`: brazos f29g y final_29 (--sin-cruces) contra cp_xl, cp_dd, cp_fin6,
  cp_ady_p35 (`results/copiadores_0929/`), semillas 5310000-5310095, dos asientos (1.536 partidas).
- `confirm_guarda_panel`: brazos f29g y final_29 contra tds27, hl836, hl0928, top3cc, fcast2,
  cha22, hl74, semillas 5310000-5310047, dos asientos (1.344 partidas).

## Regla de decisión
f29g queda **CONFIRMADA** si se cumplen las cuatro:
1. 0 partidas inválidas o con error en ambos brazos.
2. Panel: el hash de nuestras acciones difiere de final_29 en ≤ 2 % de las celdas (disparo falso),
   y en esas celdas no hay pérdida neta de W/L (victorias perdidas ≤ victorias ganadas).
3. Copiadores: W/L de f29g − final_29 pareado por celda con IC95 (bootstrap por semilla) > 0, y
   margen medio mayor con f29g contra cada uno de los 4 copiadores.
4. Tiempo máximo por turno de f29g no supera al de final_29 en más de 100 ms en el mismo torneo.

Uso si queda confirmada: sustituye a la «copia exacta de final_29» en la regla del par final
de CALENDARIO_ENVIOS.md. Si la regla del 30 se cumple, se propone al usuario enviar f29g, en
lugar de la copia, para sustituir a final_xc1; el par sería final_29 + f29g. Siempre con
aprobación explícita del usuario en ese momento. Si no queda confirmada, no se usa.
