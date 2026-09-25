# Líder actual y fuentes públicas — 2026-09-25 UTC

Consulta reproducible ~01:36 UTC, separada de los replays históricos del primer
lugar. DSM figura con **3128,7**, mejor submission **56518845**, 112 episodios
listados. Su submission más reciente es otra; no confundir fecha de equipo con
identidad del agente que sostiene el mejor score.

Se eligieron los **cuatro episodios completados más recientes, sin filtrar
resultado**: 113091953, 113086007, 113079205, 113073385. Dos rivales distintos;
cuatro victorias no constituyen su WR general. Reproducción oficial de ambas
cintas: 720 estados exactos en cada replay y dinero conciliado con transacciones
aceptadas. Hashes, selección y ledgers en
`docs/evidencia/loop_publicos_20260925/dsm_current_analysis.json` y
`dsm_*.ledger.jsonl.gz`. Script: `minar_lider_actual.py`.

| Replay | Rival | Margen DSM | Tomate vendido DSM/rival | Ingreso tomate DSM/rival |
|---|---|---:|---:|---:|
| 113091953 | 吃白饭的大肥鱼 | +10.333 | 211 / 120 | 16.867 / 9.028 |
| 113086007 | DECEM | +8.888 | 116 / 68 | 6.308 / 3.626 |
| 113079205 | 吃白饭的大肥鱼 | +10.096 | 231 / 144 | 15.980 / 9.460 |
| 113073385 | DECEM | +5.348 | 134 / 136 | 7.354 / 7.200 |

Hallazgos observados:

- Cuarto cuadrante en día 10, con sólo 9–319 monedas restantes a esa altura.
  Máximo de 12 peones. La inversión productiva es anterior a nuestro módulo
  opcional de diez tomates del día 18. **Corrección posterior:** nuestra base
  también tiene una ampliación adaptativa de ovejas al día 12; no afirmar que
  siempre espera al 18 para abrir tierra. Véase diagnóstico siguiente.
- Ya tiene 4–10 tomates al día 10; llega a 14–32 según partida y momento.
  Adapta ganado y cultivos: por ejemplo 18 ovejas frente a DECEM en un mundo,
  12 vacas y 5 gansos al día 10 en otro. No copiar una composición universal.
- Los cuatro juegos tienen 5/16/7/8 escapes. Muchos son tardíos; la traza por sí
  sola no distingue abandono deliberado de fallo. «Cero escapes» no es una
  función objetivo válida sin valorar cuidados, producción futura y trabajo.
- Las acciones de unidades difieren en cientos de turnos entre juegos, desde
  los pasos 25/42/78. Hay rutas/comportamiento diferentes según mundo; esto no
  revela su algoritmo ni demuestra aprendizaje automático.

Interpretación: estudiar producción y asignación de capital, además del timing
de ventas. Los tomates explican parte de varias diferencias económicas, pero
**no se ha identificado causalmente el mecanismo que hace ganar a DSM**. El
cuarto replay gana con prácticamente igual cantidad de tomates. Una intervención
local cambia RNG, tiendas, rival reactivo y otros ingresos: medir efecto total.

Primera hipótesis implementable: desplazar coherentemente nuestra campaña
V219 a días 12/14/16, con su riego, fertilización y ventana finita de cosecha.
Se limita inicialmente a diez tiles; no replica la explotación completa de DSM.
Comparar también día 18 con igual modelo económico para separar calendario de
criterio de inversión. Riesgos: precios todavía bajos, peones marginales caros,
agotamiento de caja y conflicto con obligaciones del padre.

Diagnóstico posterior `early_tomato_qualification.json`, seed1004000: al día
12 VQ tiene SE cerrado y 13.089 monedas; al día 14 ya hay seis ovejas allí,
colocadas el día 12. No aparecen como BUY_LAND en las cintas futuras porque
provienen de otra capa adaptativa. El chequeo heredado de futuras cintas no
detecta este coste de oportunidad. El brazo temprano toma ese espacio antes,
siembra diez tomates y vende 60, pero pierde frente al original en ambos
asientos de desarrollo. Por tanto, el loop5 mide también sustitución de una
inversión productiva: no atribuir su efecto sólo a días de cosecha. La versión
tardía no se activa en ese mundo porque SE ya está abierto y ocupado, aunque
su ingreso proyectado supere el umbral. Ésta es una razón de cobertura real,
distinta de una proyección económica demasiado conservadora.

## Fuentes públicas examinadas, sin repetir experimentos

Lista de notebooks recientes y descargas congeladas en el mismo directorio de
evidencia (`public_notebooks_latest.json`, `public_deduplication.json`,
`public_source_review.json`). No se ejecutaron notebooks externos.

- [CHA22](https://www.kaggle.com/code/abhinav0370/cha22-agent): main idéntico byte
  por byte a tds25, ya evaluado. No repetir por el nombre.
- [evgendvorkin](https://www.kaggle.com/code/evgendvorkin/kaggriculture): mismo
  texto normalizado y AST que tds25; diferencia CRLF/LF. No repetir.
- [Graph reinforcement learning](https://www.kaggle.com/code/djamilabenchikh/graph-reinforcement-learning):
  residual GCN/DQN sobre V16 para aplazar ventas, 18 partidas de entrenamiento.
  Su salida pública informa media pareada 0,0 y 0/4 pares positivos frente a
  V16, criterio monetario. Se auditó main sin ejecutarlo: no merece desplazar
  todavía las pruebas de hipótesis con mecanismo concreto. No se afirma que
  todo RL sea inútil ni se lo declara refutado sin torneo propio.
