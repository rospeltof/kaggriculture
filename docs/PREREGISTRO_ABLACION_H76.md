# Pre-registro — ablación de `harvest_76`

Escrito **antes** de ejecutar. Fecha: 2026-09-05. Autorización del usuario:
ejecutar este barrido local. **No autoriza subir nada a Kaggle.**

## Por qué

`prio_harvest=76` se adoptó el 2026-09-03 con t por celda de +2,96 sobre 320
celdas. El diseño del panel es **cruzado** (40 cintas × 8 semillas): esas celdas
no son independientes. Con el estimador correcto a dos vías el mismo dato da
**t=+1,76, IC95 [−0,85; +5,85]** — no significativo. Nunca tuvo réplica con
potencia y **está dentro de `CAMPEONA_HOZ`, la base activa**.

Precedente directo: la compra parcial dio +5,00 y +4,84 en dos bloques y **+0,23**
al replicarla con 16 semillas. `harvest_76` tiene un efecto la mitad de grande
y el mismo historial de dos bloques sin réplica potente.

## Diseño

- **Ablación leave-one-out.** `CAMPEONA_HOZ` ya lleva 76, así que el brazo de
  prueba es `sin_h76` = `CAMPEONA_HOZ` con `prio_harvest=62` (el default del
  chasis, valor previo a la adopción).
- **Semillas 104000–104015 (16)**, disjuntas de todo lo anterior
  (91xxx, 92xxx, 101xxx, 102xxx, 103xxx).
- Brazos: `base`, `noop`, `_peor` (CAMPEONA_FB exacta), `sin_h76`.
- 40 cintas × 16 semillas × 2 asientos × 4 brazos = **5.120 episodios**.

## Predicción falsable, fijada antes

| si `harvest_76` vale lo que se le atribuyó | `sin_h76` ≈ **−2,5** con IC95 que excluye cero |
|---|---|
| si era ruido | `sin_h76` ≈ **0**, IC95 incluyendo cero |

## Regla de decisión

**Integridad primero:** `noop` exacto, `_peor` claramente negativo en ambos
criterios, cero errores. Si falla, no se interpreta.

| resultado | acción |
|---|---|
| IC95 por semilla **y** a dos vías ambos < 0 | `harvest_76` **queda confirmado**; se mantiene en la base |
| ambos incluyen cero | **no está respaldado**; se documenta y la decisión de revertir es del usuario |
| discrepan | se reporta la discrepancia como resultado; no se adopta postura |

Bloque único. No se encadena otro para rescatar ningún lado. Test bilateral.
No se ajusta nada a partir de lo que se vea aquí.

## Qué no decide

No mide generalización al ladder (las cintas son rivales pasivos). No dice nada
sobre `seed_stock_aware`, cuyos datos crudos de confirmación se perdieron al ser
sobrescritos por una corrida posterior — un fallo que el `barrido.py` actual ya
impide, pero que llega tarde para ese archivo.
