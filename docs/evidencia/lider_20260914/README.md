# Evidencia de la investigación del líder — 2026-09-14

`replays.json` describe los ocho archivos de Downloads, sus hashes y sus
resúmenes de conducta. Los JSON originales no se modifican ni se duplican aquí.
No contienen Elo de los jugadores. `validacion.json` registra reproducción exacta
de 720 estados en cada partida y contabilidad efectiva por operación/producto.

`ledger_*.jsonl.gz`: commits efectivos del mercado y costes de HIRE/BUY_LAND,
con jugador, turno, producto y cambio de dinero. Los SELL de una unidad a $1
también se contabilizan. Proceden del motor 1.32.7 durante la reproducción exacta.

Las 16 cintas compactas de ambos jugadores están en `bots/meta/tapes/`:
`maj_<episodio>.json.gz` y `sepopp_<episodio>.json.gz`. Incluyen el offset +1
correcto y PASS terminal. No sustituyen las cintas `lad_` del panel histórico.

Los archivos de evaluación usan prefijos `pilot`, `confirm_*` y `stress_*`:

- `*.meta.json`: diseño, estado, versiones, hashes, configuraciones, resúmenes.
- `*.episodes.jsonl` y su copia `.gz`: resultados incrementales, estados, tiempos
  y hashes de acciones emitidas. Conservar al menos la copia comprimida junto al manifiesto.
- `*.sources.tgz`: código y protocolo congelados antes de la corrida.
- `sonda_tecnica.json` y `perfiles_sonda.json`: diagnósticos, no confirmaciones.
- `confirmacion_registro.json`: selección y tamaño registrados desde el piloto,
  antes de lanzar confirmación. `decision.json` aplica los criterios registrados.
- `duelo_hoz.json` y sus episodios: diagnóstico contra HOZ vivo, ocho semillas
  nuevas y ambos asientos. Su script guarda el diseño antes de ejecutar.
- `perfil_control_apertura.json`: cinta original de control para interpretar la
  sonda de apertura, sin usar su dinero para seleccionar candidatos.

Verificación sin partidas: `./.venv/bin/python verificar_lider.py`. Revisa los
tres paneles, selección, fuentes estables entre bloques, semillas y duelo. Usa
la misma función estadística del evaluador; no es una réplica independiente del
cálculo de intervalos. `resultados_lider.py` genera el informe desde los cuatro
bloques completos. No interpretar archivos `running` como resultado final.

`economias_lider.png` se genera desde datos descriptivos con `resumir_lider.py`.
Las fuentes del experimento se congelan durante cada bloque; nunca inferir fuerza
de un bloque cuyo manifiesto no diga `complete`. Las tablas no predicen Elo.

Estos archivos quedan fuera de exclusiones Git, pero no se crea automáticamente
un commit ni se envía nada. Para repetir la auditoría de estados completos hacen
falta los JSON originales; para repetir evaluaciones bastan código, motor y cintas.
