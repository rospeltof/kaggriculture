# Pre-registro — barrido de PREDICT sobre tds27top3 (eliminación sucesiva)

Escrito antes de evaluar. 2026-09-27 ~10:15 UTC.

- **Motivo:** tds27top3 (activa, 2280 @83, 47-13 en real) es nuestra mejor pieza; el
  segundo slot (top3cc, 2082) apenas aporta al máximo del equipo. TOP 1→3 ganó el
  espejo a tds27; puede haber un ajuste mejor.
- **Variantes (una línea añadida a tds27top3):** top2 (TOP=2), top5 (TOP=5), k3
  (TOP=3, K=3), every1 (TOP=3, EVERY=1).
- **Piloto:** `torneo.py --out results/torneo_barrido27 --vs tds27top3,top2,top5,k3,every1`
  con pool tds27, cha22, cha22sfko, top3cc, hl74; semillas 4000000-4000011 (12).
  Pasa a confirmación la variante con mayor puntuación en el directo contra
  tds27top3 si además su delta contra el pool (vs tds27top3) es ≥ 0.
- **Confirmación:** 16 semillas nuevas (4010000-4010015). Adoptar para el segundo
  slot si directo vs tds27top3 con IC95 por semilla > 50% y pool sin daño (límite
  inferior dos vías > −5 pp). Si ninguna pasa: segundo slot = tds27top3 idéntico
  reenviado NO (no aporta información); se mantiene top3cc como cobertura.

## Resultado del piloto (torneo_barrido27, 840 partidas, 0 errores)

Directo contra tds27top3: **top5 14-4-6 (70,8%)**, every1 2-0-22 (54,2%), top2 37,5%,
k3 29,2%. top5 contra el pool: **−5,83 pp** [−23,65; +11,98] dos vías; 1 celda a favor,
5 en contra (tds27 −12,5, cha22 −8,3, cha22sfko −8,3). **Ninguna variante pasa** (la de
mejor directo tiene delta de pool < 0). No transitivo: TOP=5 gana a TOP=3 en el espejo
pero pierde más contra TOP=1. Se mantienen tds27top3 (slot 1) y top3cc (slot 2).
