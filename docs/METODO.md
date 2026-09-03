# Método de evaluación — cómo decidimos que algo es una mejora

Documento hermano de `RULES.md` (modelo del motor) y `BITACORA.md` (registro de
experimentos). Aquí va el **aparato de medición**: qué medimos, con qué, y qué
tiene que pasar para encender un mecanismo.

Nace de una constatación incómoda (2026-08-31): en un solo día se midieron doce
mecanismos con un instrumento inválido y **los dos que resultaron ser mejoras
reales estaban en la lista de descartes**. El cuello del proyecto no era la falta
de ideas: era no tener un medidor capaz de decir que sí.

Regla general: **cuando un candidato y un control se contradicen, el sospechoso es
el instrumento, no el candidato.**

---

## 1. El objetivo: el Elo paga W/L/T, no margen

El ladder da rating por **victoria / derrota / empate**. El margen de monedas **no
compra rating**: ganar por $1 vale igual que ganar por $50,000.

Por tanto **el dinero es un proxy, y malo**. Evidencia directa:

| mecanismo | dinero vs C95 | win-rate vs panel | qué pasó |
|---|---|---|---|
| `sell_floor 0` | +$506 (t=1.72) | +4.5 pts, +28 h2h | casi se descarta |
| `fert_dawn_load` | **−$3,879** | **+15.5 pts** (t=3.70) | **se descartó** |

Con `fert_dawn_load` hasta se dio una explicación aritmética correcta al dólar de
por qué perdía dinero (convierte fertilizante de $85 en fresa de $25). La
aritmética era cierta y la conclusión falsa: **la caja baja y los duelos suben.**

**La causa raíz del error:** se medía dinero contra C95, que nos gana el 100% de
las partidas. En un régimen donde el resultado está fijo, el dinero no mide
"¿mejoré?" sino **"¿de qué tamaño es la derrota?"** — justo lo que el Elo ignora.

> ❌ Nunca promocionar por dinero. El dinero sirve como diagnóstico de MECANISMO
> (¿hizo lo que creía que hacía?), nunca como criterio de decisión.

---

## 2. El instrumento: `harness.py`

```bash
./.venv/bin/python harness.py bots.arquetipos:campeona_alba bots.meta.tape:artfix -n 20
```

Tres propiedades que lo hacen válido:

- **Espejo.** Cada seed se juega **dos veces con los lados invertidos**. Es
  obligatorio: por `RULES.md` S5.4 el jugador 0 resuelve `HIRE` y `BUY_LAND`
  primero, así que sin espejo se mide el asiento. `-n 20` = 40 episodios.
- **Empates = 0.5.** El motor es determinista, así que un cambio inocuo produce
  **empates exactos**. Con empates contando como derrota, un `_noop` leía 33% en
  vez de 50%; con ese medidor se probaron 19 variantes en un día y **las 19
  salieron negativas** — era la firma del medidor, no 19 malas ideas.
- **Guarda un `.jsonl` por episodio** en `results/`, con dinero por seed. Sin eso
  no se puede hacer el análisis pareado, que es la sección siguiente.

---

## 3. Análisis pareado, nunca medias crudas

Los episodios espejados **comparten seed**, así que no son independientes.
Comparar medias crudas desperdicia esa estructura:

| | media cruda | pareado por seed |
|---|---|---|
| desviación típica | ~$18,000 | **$500 – $2,200** |
| `sell_marginal 0.6` | "−$3,430, ruido" | **t = −4.35, negativo duro** |
| `crop_max 8` | "−$1,220, negativo" | **t = −0.29, inconcluso** |

Misma data, conclusiones opuestas. Con medias crudas y 8 pares la banda es
±$6-8k y **todo cabe dentro del ruido**.

Procedimiento: para cada seed, media del par espejado por brazo → diferencia
variante − base → t pareado sobre esas diferencias.

---

## 4. Brazos de control: obligatorios

Nunca se mide un candidato solo. Van siempre:

- **`_noop`** — clon exacto de la base. **Debe leer delta 0.0.** Valida el
  MEDIDOR. Si no da 0.0, todo lo demás sobra.
- **`_peor`** — una generación anterior, peor por evidencia externa del ladder.
  **Debe leer claramente negativo.** Valida el PANEL: si `_peor` no baja, el panel
  no discrimina y un "no encontré mejora" no significa nada.
- **La base.**

Ejemplo de control funcionando (panel de cintas, 200 eps/brazo):
`_noop` +0.0 en las cinco celdas · `_peor` −18.5 (t=−3.32) · candidato +4.5 (t=+2.23).

Ejemplo de control **fallando** y salvando el día: el panel sintético
`c95_handicap` daba un dial aparentemente bueno, pero `_peor` leyó **+12.7 pts por
encima de la base** y el punto de calibración osciló **66% / 90% / 74%** entre
bloques de seeds. Instrumento descartado por sus propios controles.

---

## 5. El panel necesita RESOLUCIÓN — pero elegirlo POR resolución lo sesga

> ⚠️ **CORRECCIÓN 2026-09-02, la más importante de este documento.** La regla de
> abajo ("celdas con la base entre 30% y 70%") es necesaria pero **NO suficiente, y
> aplicada como criterio de SELECCIÓN produce un panel sobreajustado**.
>
> Evidencia: el panel de 5 cintas escogidas por tener resolución daba
> `campeona_ruta` **+15.6 puntos** sobre `campeona_alba`. El panel de **40 rivales
> reales** (todos los de una submission, sin seleccionar) da **−3.1** (t=0.83), y
> el ladder dice 844.9 vs 846.6 — es decir, empatadas. El panel de 40 reproduce el
> Elo; el de 5 no.
>
> | bot | Elo real | panel 5 (seleccionado) | panel 40 (completo) |
> |---|---|---|---|
> | campeona_ruta | 844.9 | **61.6%** | 51.6% |
> | campeona_alba | 846.6 | 46.0% | 54.7% |
> | campeona_fase | 826.4 | — | 56.9% |
>
> **Por qué falla:** elegir rivales donde la base puntúa 25-75% selecciona
> justamente aquellos donde nuestras diferencias se amplifican. Es selección sobre
> el estadístico que luego se mide.
>
> **Regla corregida:** el panel debe ser una **muestra REPRESENTATIVA** de la
> población del ladder — *todos* los rivales de una submission, sin descartar por
> conveniencia. La resolución se consigue con VOLUMEN (40 rivales), no eligiendo
> celdas. Herramienta: `extraer_todos.py <CARPETA>` + `panel40.py`.
>
> Coste: ~960 episodios (~7 min) por comparación de 3 brazos. Es caro y es el que
> decide. El panel pequeño sirve para triage rápido, nunca para promocionar.

## 5. El panel necesita RESOLUCIÓN

Una celda solo informa si la base puntúa aproximadamente entre **30% y 70%**.
Fuera de ahí está saturada y no puede mostrar cambios.

Así estaba el panel "oficial" hasta 2026-08-31:

| brazo | vs C95 | vs cinta v16 | vs campeona | vs rutera |
|---|---|---|---|---|
| base | 0% | 0% | 100% | 100% |
| `_noop` | 0% | 0% | 100% | 100% |
| candidato | 0% | 0% | 100% | 100% |
| `_peor` | 4% | 2% | 16% | 100% |

**Todas saturadas.** Solo `_peor` se movía → el panel detectaba **regresiones** y
era **ciego a las mejoras**. Causa raíz: no había ningún rival entre nuestro nivel
y el del meta (contra todo el linaje C90-C95 vamos 0%; contra generaciones
propias viejas, 100%).

### La solución: cintas de rivales reales

`reconstruir.py` extrae el schedule de 720 turnos de un rival desde un replay
NUESTRO y lo convierte en agente (`bots/meta/tape.py`). Es el método del meta:
C95 no es más que la cinta de un episodio.

- **Trampa del extractor:** en el replay descargado la acción del índice `t` es la
  que YA se aplicó para llegar a ese estado. Sin `shift=1` la simulación va un
  turno por detrás y la granja colapsa ($12,470 contra $85,804 reales) — se lee
  igual que "las cintas no funcionan". La firma que lo delata: `sim[t] == real[t-1]`.
- **Validación:** con el seed grabado, la cinta debe reproducir el marcador real.
  Estado actual: **8 de 8 EXACTAS**, cero turnos divergentes en 720.
- **Guard anti-mezcla:** solo replays de UNA submission, verificando `TeamNames`.
  El primer token de la descripción de la submission debe ser el nombre del bot,
  porque es lo que `bajar_replays.py` usa para separar carpetas.

**Limitación honesta:** una cinta es **CIEGA**, no reacciona a nosotros. Es algo
más débil que el rival original y sube su varianza en seeds ajenos. Los mecanismos
que explotan la pasividad del rival (p.ej. `sell_floor 0`, que gana vendiendo
antes) están **estructuralmente favorecidos** contra cintas. Las cintas fijas son
un diagnóstico correlacionado, no una puerta de promoción.

---

## 6. Los tres papeles, separados

| medición | contra qué | qué contesta | papel |
|---|---|---|---|
| **Head-to-head** | mejor solución actual | ¿rompí algo? | **veto** |
| **Panel de cintas** | rivales reales, celdas 30-70% | ¿es mejor, y cuánto? | **promoción** |
| **Linaje con Elo real** | submissions propias con rating | ¿mi panel mide habilidad? | **validación** |

### Por qué el head-to-head NO puede promocionar

Contra nuestro propio linaje, con Elo real conocido:

| rival | Elo real | Δ Elo | WR esperado | WR local | inflación |
|---|---|---|---|---|---|
| campeona | 772.3 | 33.4 | 54.8% | 93.3% | **+38.5** |
| campeona_season | 746.9 | 58.8 | 58.4% | 90.0% | **+31.6** |
| integral | 690.5 | 115.2 | 66.0% | 93.3% | **+27.3** |
| rutera | 667.9 | 137.8 | 68.9% | 100.0% | **+31.1** |

Infla **27-38 puntos** de forma sistemática, y **no ordena**: `campeona` (772.3) e
`integral` (690.5), separados por 82 puntos de Elo, leen **exactamente lo mismo**.
El signo es fiable; la magnitud no.

Motivo mecánico: en un duelo casi-espejo los dos bots están en un equilibrio de
mercado delicado y una ventaja pequeña convierte una fracción enorme de partidas.

### Validación del panel contra Elo real (la pata que faltaba)

Tenemos 11 submissions con rating externo. Un panel que mide habilidad debe
reproducir ese orden.

| bot | Elo real | panel de cintas |
|---|---|---|
| campeona_fb | 801.4 | 50.7% |
| campeona | 772.3 | 24.7% |
| campeona_season | 746.9 | 34.0% |
| integral | 690.5 | 28.7% |
| rutera | 667.9 | 4.7% |

**Spearman ρ = +0.70** — acierta los extremos, se equivoca en el medio. Frente al
head-to-head, cuyo ρ efectivo es ~0.

**Calibración: 1 punto de win-rate en el panel ≈ 2.7 puntos de Elo.**

> ⚠️ Con n=5 y ratings que traen ruido propio (`campeona_fb` se movió 805.7 → 801.4
> en un día sin tocar código), esta recta sirve para detectar si el panel está
> **plano o invertido**, no para calibración fina. ρ=0.70 con n=5 no es
> significativo formalmente.

---

## 7. La regla de decisión

1. **Win-rate**, nunca dinero.
2. Panel con celdas en **30-70%**; validar con `ρ ≥ 0.7` contra el Elo del linaje.
3. `_noop` = 0.0 y `_peor` claramente negativo. Si fallan, **se tira el panel, no
   el candidato**.
4. Test **pareado** por seed, **t > 2**, ~200 episodios.
5. **Head-to-head** contra el campeón vigente como veto.
6. Convertir el delta a predicción de Elo (×2.7) y **escribirla en BITACORA.md
   ANTES de subir**.
7. Subir dejando el incumbente activo como control; **no leer antes de 50-90
   episodios**.

---

## 8. Modos de fallo conocidos

| # | fallo | firma | fecha |
|---|---|---|---|
| 1 | empates contados como derrota | `_noop` lee 33% en vez de 50% | 08-31 (`b20844a`) |
| 2 | medir contra un clon propio | misma lectura para cualquier cambio | s/f (BRIEFING §4.2) |
| 3 | panel saturado por ambos extremos | base en 0% o 100%; solo `_peor` se mueve | s/f (§4.3) + 08-31 |
| 4 | potencia insuficiente | <100 eps/variante invierte conclusiones | s/f (§4.4) |
| 5 | **lente equivocada (dinero)** | mide el tamaño de derrotas fijas | **08-31** |
| 6 | **medias crudas** | sd $18k se traga todo; usar pareado | **08-31** |
| 7 | **panel sin validar** | `_peor` positivo; dial inestable entre seeds | **08-31** |
| 8 | extractor de cintas sin shift | `sim[t] == real[t-1]`, granja a $0 | **08-31** |
| 9 | transcripción no byte-fiel | espejo 8-0 (imposible entre iguales) | 08-19 |

Para el #9 la prueba es doble: espejo con **dinero idéntico y misma sd**, y
comparación decisión a decisión (`0 de 2,157 distintas` en `campeona_alba`).

---

## 9. Estado vivo

- **Panel actual:** `takahirohon`, `ahmad_ali`, `artfix`, `masih_pemula_beneran`,
  `uman_n3l` (base 50-57%, ρ=0.70).
- **Predicción registrada:** `campeona_alba` midió +15.5 pts sobre `campeona_fb`
  → ×2.7 ≈ **+42 Elo** → **~843**.
- **Observado:** 826.7 con 40 episodios (umbral: 50-90). Dirección correcta, por
  debajo de la predicción, **aún no concluyente**.

---

## 10. Comandos

```bash
./.venv/bin/python bajar_replays.py --bajar 20      # replays (ojo: --activas)
./.venv/bin/python derrotas.py --perfil             # clasificar V/D + perfil rival
./.venv/bin/python reconstruir.py --derrotas 8      # extraer cintas + validar
./.venv/bin/python harness.py A B -n 20 --seed0 31000
./.venv/bin/python autopsia.py A B -n 3             # diagnóstico de mecanismo
./.venv/bin/python empaquetar.py CAMPEONA_HOZ      # submission/main.py
./.venv/bin/python muerde.py CAMPEONA_HOZ          # que banderas MUERDEN de verdad
./.venv/bin/python barrido.py 92000                # barrido de prioridades vivas
./.venv/bin/python barrido.py 92500 harvest_76     # confirmacion en seeds disjuntas
./.venv/bin/kaggle competitions submit -c kaggriculture -f submission/main.py -m "..."
```

## 11. Dos trampas que ya nos costaron caro

**`sd = 0.0` significa "no se ejecuto", no "no sirve".** Un brazo identico al
base en las 160 celdas es un TEST nulo, no un resultado nulo. Antes de leer un
"+0.0" como rechazo, comprobar con `muerde.py` que la bandera dispara. Nos paso
tres veces el 2026-09-03 (`hands_cap 14`, `endgame_reap` v1 y v2) porque el
chasis tiene DOS implementaciones de la misma decision y los parches tocaban la
mitad muerta: **`_service_ops` es la que manda cuando `router=True`**.

**Una sonda de UN episodio sirve para comprobar que una bandera MUERDE, nunca
para estimar su efecto.** El 2026-09-03 una sonda dio \$100k para los gansos
contra \$82k de la base; el panel de 40 dio 19% de winrate contra 59%. La
mediana real de ese brazo era \$63k: la sonda pego en la cola alta.

**La curva de precios `_price_at(producto, 10000+d)` mide exceso de inventario
INSTANTANEO, no ventas acumuladas.** Las ventas se reparten en 25 dias y el town
drena en continuo, asi que el exceso nunca llega a las 100 unidades de golpe.
WOOL termina la partida a \$247 (base \$200) despues de vender 119 lanas.

**Quitar una clave cuyo valor == default es un no-op POR CONSTRUCCION.** Ahi hay
que PERTURBAR el valor, y proporcionalmente (restar 30 a 2000 no prueba nada).
`muerde.py` lo detecta y lo hace solo.

```bash
```
