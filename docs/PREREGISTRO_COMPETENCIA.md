# Pre-registro — scorer consciente de la competencia de precio

Escrito **antes** de ejecutar. Fecha: 2026-09-06. Autorización: barrido local.
**No autoriza subir nada a Kaggle.**

## El hallazgo que lo motiva

Producimos **más** que el top-1 en aislamiento (140.532 vs 131.034 contra un
rival PASS) y perdemos **38%** al competir, contra su **26%**. Somos mejores
granjeros y peores competidores. Eso explica por qué doce barridos consecutivos
salieron negativos: todos medían la granja.

**Desglose por producto** (misma semilla con y sin rival): es competencia de
**precio pura**, no de volumen — vendemos 932 unidades aisladas y 977
compitiendo, a precios hundidos:

| producto | $/ud aislado | $/ud compitiendo | Δ | $ perdidos |
|---|---|---|---|---|
| WOOL (`sq`×3,20) | 240,9 | 85,2 | **−65%** | 18.846 |
| STRAWBERRY (`linear`×1,60) | 216,4 | 175,6 | −19% | 11.037 |
| MELON (`sq`×3,60) | 226,2 | 147,1 | −35% | 9.693 |
| MILK (`linear`×1,60) | 208,5 | 171,4 | −18% | 6.049 |
| CARROT (`hinge`) | 48,6 | 61,6 | **+27%** | −488 |
| WHEAT (`log`×0,20) | 34,4 | 39,0 | **+13%** | −2.654 |
| TOMATO (`hinge`) | 88,5 | 168,5 | **+90%** | −3.922 |

Las curvas frágiles se llevan todas las pérdidas; las robustas (`log`, `hinge`)
**mejoran** con rival, porque él drena esos mercados en vez de inundarlos.

## Mecanismo del cambio

El scorer evalúa `_price_at(crop, proj_inv + supply + u_eff)` con
`supply = pipeline + opp_incoming`, donde `opp_incoming` son las tiles rivales
**observadas hoy**. Eso subestima su oferta de temporada y por tanto
**sobrevalora los cultivos de curva frágil**.

`compete_aware` asume un rival comparable: `supply = compete_mult × pipeline +
opp_incoming`. No cambia rutas, plantilla, forraje, ventas ni prioridades.

**Disparo verificado** (sonda de 1 episodio, sólo mecanismo): `ca4` cambia 515
turnos y mueve la cesta de STRAWBERRY 250→78 y MELON 120→74 hacia WHEAT 232→384,
TOMATO 0→36 y CARROT 17→56. La cifra de dinero de esa sonda **no** se usa como
estimación de efecto.

## Diseño

- **Semillas 113000–113015 (16)**, disjuntas de todo lo anterior.
- Brazos: `base`, `noop`, `_peor` (CAMPEONA_FB exacta), `ca2`, `ca3`, `ca4`,
  y `mof2` (`opp_read=False`, `mkt_opp_factor=2`: el default viejo del chasis).
- 40 cintas × 16 semillas × 2 asientos × 7 brazos = **8.960 episodios**.

## Regla de decisión

**Integridad primero:** `noop` exacto, `_peor` claramente negativo en ambos
criterios, cero errores. Si falla, no se interpreta.
**No se toca `bots/chassis.py` mientras el barrido corre** (regla del 2026-09-06).

Adoptar el mejor `ca*` sólo si se cumplen **las dos**:
1. IC95 **por semilla** y **a dos vías** ambos por encima de cero.
2. La familia `ca2/ca3/ca4` muestra respuesta **monótona o de un solo pico**.
   Un patrón errático indica ruido aunque un brazo salga significativo.

**Multiplicidad declarada:** 5 brazos no-control contra una base. La condición 2
existe para no premiar al mejor de cinco sorteos.

**Potencia:** con 16 semillas el MDE al 80% es ~6,8 puntos para un mecanismo de
huella grande. El efecto en juego —la diferencia de coste de competir entre
nosotros y el top-1— es de ~12 puntos porcentuales de producción. Si el efecto
real es menor que el MDE, **se reportará como no medible, no como nulo**.

Bloque único, bilateral. No se encadena otro para rescatar ningún lado.
