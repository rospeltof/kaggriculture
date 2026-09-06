# Pre-registro — 2×2 cadencia de riego × tamaño de rebaño

Escrito **antes** de ejecutar. Fecha: 2026-09-06. Autorización: barrido local.
**No autoriza subir nada a Kaggle.**

## Hipótesis

`water_cadence` y un rebaño grande **son complementarios**, y por eso ambos
fallaron al medirse por separado.

**Mecanismo, medido no supuesto:**
- El **68% de nuestro riego no compra rendimiento** (825 de 1.209 riegos por
  partida). Motor L431-443: en cultivos de un corte el riego sólo suma dentro de
  `win`. Motor L786-800: los continuos producen +1 **regadas o no**; el riego
  sólo da el ×2 con fertilizante, o evita la muerte por dos días secos.
- Un rebaño grande **cuesta acciones**: ~3/día por animal (FEED, CARE, COLLECT).
  Pasar de 8 a 13 animales pide ~15 acciones/día que hoy no existen.

Probar más animales sin liberar el riego es pedirle a la cuadrilla algo que no
cabe. Precedente en la bitácora: *"INTEGRAL: el paquete gana por INTERACCIONES"*.

## Diseño

2×2 completo, para aislar la interacción:

| brazo | cadencia | animales |
|---|---|---|
| `base` (CAMPEONA_HOZ) | no | 8 |
| `cad` | **sí** | 8 |
| `r13` | no | **13** |
| `cad_r13` | **sí** | **13** |

Más `noop` (copia exacta) y `_peor` (CAMPEONA_FB exacta).

- **Semillas 106500–106515 (16)**, disjuntas de todo lo anterior.
- 40 cintas × 16 semillas × 2 asientos × 6 brazos = **7.680 episodios**.

## Predicción falsable, fijada antes

| resultado | lectura |
|---|---|
| `cad_r13` > 0 **y** > `cad` **y** > `r13` | **interacción real**: el paquete gana donde las piezas pierden |
| `cad_r13` ≈ `cad` + `r13` (ambas negativas) | **sin interacción**: los efectos se suman y el frente se cierra |
| `cad_r13` < ambas | interacción negativa; frente cerrado con más razón |

## Regla de decisión

**Integridad primero:** `noop` exacto, `_peor` claramente negativo en ambos
criterios, cero errores. Si falla, no se interpreta.

Adoptar `cad_r13` sólo si su IC95 **por semilla y a dos vías** excluye cero por
arriba **y** su estimación puntual supera a `cad` y a `r13`.

**Potencia:** con el sd entre semillas típico de un mecanismo de huella grande
(~9-12 puntos), 16 semillas dan un MDE de ~7-9 puntos. El efecto en juego es la
distancia entre nuestra composición y la del top-1, del orden de decenas de
puntos. Si la interacción existe y es pequeña (<7 puntos), **este bloque no la
detectará y así se reportará** — no se declarará nula, se declarará no medible.

Bloque único, bilateral. No se encadena otro para rescatar ningún lado.
