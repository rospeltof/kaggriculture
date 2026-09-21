# Resultados de la ronda del líder — 2026-09-14

**Mejora positiva en este panel, sin alcanzar el umbral registrado de 15 puntos.** El candidato `maj_107674293` mejora 14.36 puntos W/L/T frente a HOZ en confirmación. No se envió nada a Kaggle; `CAMPEONA_HOZ` y `submission/main.py` siguen intactos.

[Análisis de los ocho replays](ANALISIS_LIDER_2026-09-14.md) · [Protocolo anterior a las pruebas](EXPERIMENTOS_ATREVIDOS_2026-09-14.md) · [Evidencia](evidencia/lider_20260914/README.md)

## Confirmación independiente por semillas

Panel fijo: 40 cintas históricas y ocho rivales extraídos de los nuevos replays; 19 semillas 215000–215018, ambos asientos. Cuatro brazos, 7.296 episodios; 1.824 por brazo. W/L/T vale victoria=1, empate=0,5, derrota=0. Deltas e intervalos en puntos porcentuales frente a HOZ.

| Brazo | W/L/T | Delta | IC95 por semilla | IC95 dos vías |
|---|---:|---:|---:|---:|
| `base` | 57.13% | +0.00 | [+0.00; +0.00] | [+0.00; +0.00] |
| `noop` | 57.13% | +0.00 | [+0.00; +0.00] | [+0.00; +0.00] |
| `_peor` | 37.77% | -19.35 | [-22.05; -16.66] | [-25.69; -13.02] |
| `maj_107674293` | 71.49% | +14.36 | [+9.02; +19.71] | [+6.71; +22.02] |

Desglose descriptivo de confirmación (no cambia la regla primaria):

| Rivales | HOZ | Candidato | Delta |
|---|---:|---:|---:|
| 40 históricos | 61.05% | 76.05% | +15.00 |
| 8 nuevos | 37.50% | 48.68% | +11.18 |

Regla registrada: delta ≥15 puntos, ambos intervalos del candidato por encima de cero y ambos del control FB por debajo de cero. Candidato positivo en ambos: **True**; control FB negativo en ambos: **True**. El umbral de 15 se aplica al estimador puntual, no al límite inferior del intervalo.

El tamaño de 19 semillas se fijó antes de confirmar usando la dispersión del piloto. No se amplió al mirar resultados. Esta es confirmación en semillas disjuntas, con rivales parcialmente compartidos; no es validación externa del ladder.

## Todos los candidatos del piloto

Cuatro semillas 214000–214003, 16 rivales y ambos asientos: 128 episodios por brazo, 1.792 en total. La selección usa W/L/T agregado y desempate alfabético, fijados antes de correr. No se eligió por dinero ni por el intervalo más favorable.

| Brazo | W/L/T | Delta vs HOZ | Históricos (8) | Nuevos (8) |
|---|---:|---:|---:|---:|
| `maj_107674293` | 64.06% | +17.97 | 75.00% | 53.12% |
| `tree` | 64.06% | +17.97 | 62.50% | 65.62% |
| `tree_liquid` | 64.06% | +17.97 | 62.50% | 65.62% |
| `maj_107692988` | 59.38% | +13.28 | 62.50% | 56.25% |
| `maj_107710951` | 57.03% | +10.94 | 57.81% | 56.25% |
| `maj_107673304` | 55.47% | +9.38 | 73.44% | 37.50% |
| `maj_107674284` | 54.69% | +8.59 | 62.50% | 46.88% |
| `warmstart10` | 52.34% | +6.25 | 67.19% | 37.50% |
| `maj_107685970` | 48.44% | +2.34 | 56.25% | 40.62% |
| `maj_107675268` | 46.88% | +0.78 | 56.25% | 37.50% |
| `base` | 46.09% | +0.00 | 54.69% | 37.50% |
| `noop` | 46.09% | +0.00 | 54.69% | 37.50% |
| `maj_107696961` | 37.50% | -8.59 | 37.50% | 37.50% |
| `_peor` | 33.59% | -12.50 | 29.69% | 37.50% |

La cinta 107674293, el árbol y el árbol con ventas empataron en 64,06%. Confirmar la cinta cumple el desempate, pero no demuestra que supere al árbol. Las ventas reactivas cambiaron las acciones en los 128 episodios y no cambiaron W/L/T frente al árbol en ninguno: ejecución sin mejora observada. La apertura seguida de HOZ quedó en +6,25 puntos exploratorios.

El piloto pondera 50% rivales históricos y 50% nuevos; la confirmación pondera 40/48 y 8/48. Esa diferencia estaba registrada, pero puede cambiar qué arquitectura destaca. No reinterpretar los estratos después para rescatar un candidato.

Limitación de la variante de ventas: el proyector asume tablero 10×10 y shed de 100 unidades y no modela el caso en que PLACE de un animal cae al shed. No es un simulador general exacto. El bloque terminado mide esta implementación concreta; corregirla requiere otra variante y otro registro, no cambiar el código de una corrida. El candidato seleccionado no usa ese proyector.

## Diagnósticos posteriores, sin selección

Contra las ocho cintas de Majkel: ocho semillas 216000–216007, ambos asientos, cuatro brazos, 512 episodios. Son fuentes usadas para construir candidatos, no rivales reservados. Una cinta no responde como el agente original.

| Brazo | W/L/T | Delta vs HOZ | IC95 por semilla |
|---|---:|---:|---:|
| `base` | 11.72% | +0.00 | [+0.00; +0.00] |
| `noop` | 11.72% | +0.00 | [+0.00; +0.00] |
| `_peor` | 10.16% | -1.56 | [-14.59; +11.46] |
| `maj_107674293` | 90.62% | +78.91 | [+68.86; +88.95] |

En este estrés, el intervalo del control FB cruza cero: el bloque no demuestra discriminación entre FB y HOZ. Su ventaja observada para el candidato se conserva como diagnóstico; no satisface por sí sola el protocolo de confirmación ni prueba que gane al líder reactivo.

Contra HOZ vivo: **12 victorias, 4 derrotas y 0 empates**, W/L/T 75.00%, en 16 partidas (ocho semillas 217000–217007, ambos asientos). IC95 t por semilla del score: [+36.30; +113.70] puntos. Es un diagnóstico pequeño; este intervalo aproximado no está restringido al rango [0,100].

## Integridad y límites

Los tres paneles completos tienen cobertura cartesiana, cero episodios inválidos y noop exacto en acciones emitidas, rewards, estados de finalización, pasos y llamadas. Los hashes de acciones se capturan antes del motor. Se archivaron fuentes y protocolo antes de cada bloque y se comprobaron hashes de motor y cintas al finalizar. Los paneles conservan hashes, no todos los estados intermedios; la comparación explícita de 720 estados completos corresponde a las ocho reproducciones originales.

`verificar_lider.py` vuelve a comprobar registros comprimidos, cobertura, controles y fuentes archivadas, y reconstruye los resúmenes con la función estadística del evaluador. No constituye una segunda implementación independiente de los intervalos.

Coste: 1.792 piloto + 7.296 confirmación + 512 estrés + 16 duelo + 18 reproducciones/sondas = **9.634 episodios locales**. No consumen envíos de Kaggle. Los tiempos de decisión registrados son locales, no una prueba del paquete en el runtime de Kaggle.

No se verificó Elo, rank actual ni el comportamiento reactivo del líder. Los ocho replays son victorias seleccionadas. Tres de sus rivales comparten un prefijo de 120 acciones: agrupar por nombre no garantiza independencia de estrategias. Un buen resultado local contra cintas no garantiza transferencia a oponentes nuevos o adaptativos.

## Qué probar después

1. **Reservar familias de rivales nuevas antes de desarrollar.** La principal incertidumbre es transporte, no optimizar décimas en este panel. Propuesta: ocho familias no usadas, 16 semillas y ambos asientos, cuatro brazos = 1.024 episodios; fijar identidades, hashes y regla de decisión antes del primer resultado. Si no hay familias nuevas verificables, no llamar a la prueba holdout de rivales.
2. **Aprender las ramas del árbol con información visible.** El árbol actual usa una regla manual de tiendas. Comparar cinta seleccionada, árbol congelado y router aprendido con partición por familias y semillas; no elegir tiendas o pesos mirando confirmación. Primero definir dataset y presupuesto, luego evaluar.
3. **Reparar compromisos de la ruta, no sólo vender más.** La capa de ventas no aportó victorias en el piloto. Una reparación útil debe registrar compras ejecutadas, inventario y cohortes para evitar que una acción fallida rompa el calendario. Comenzar con diagnóstico de 16 partidas preseleccionadas; sin evidencia de ese mecanismo, parar antes de un barrido.

La idea de rutas y ligas tiene precedentes públicos: el autor de [Three Day Shop Router](https://www.kaggle.com/code/yhay81/three-day-shop-router/comments) describe copias simplificadas de rutas públicas y evaluación en muchas semillas. Es un reporte del autor; no descargamos su implementación ni verificamos su velocidad anunciada. Esta ronda construye y mide nuestras propias variantes.

## Reproducir y revisar con otro LLM

```bash
./.venv/bin/python verificar_lider.py
./.venv/bin/python preparar_contexto_llm.py
./.venv/bin/python preparar_contexto_llm.py --check
```

Entrada experimental de la cinta: `bots.meta.tape.make('maj_107674293')`. Las variantes nuevas están en `bots/experimentos_lider.py`. Los evaluadores rechazan sobrescribir una corrida existente: para repetirla usar una copia del repo y conservar los originales. No ejecutar `submission/main.py` ni empaquetar por interpretar este informe como autorización de envío.
