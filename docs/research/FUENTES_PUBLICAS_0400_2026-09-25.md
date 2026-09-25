# Actualización pública, consulta2026-09-25 alrededor de04UTC

API de Kaggle,50notebooks ordenados por dateRun; descargas fechadas en
`public_fetch_0400.json`. No se ejecutaron notebooks externos: se extrajeron
literales verificables y se compararon hashes antes de cargar agentes aislados.

## Duplicado identificado

[Master Engine](https://www.kaggle.com/code/guruprasaathas111/kaggriculture-master-engine-v3)
declara V6 en el texto y nueva ejecución02:50UTC, pero su main actual es
sha127ed3e6,501.543bytes, idéntico a tds25 y CHA22. No repetir public_refresh;
mantener el antiguo guru6 congelado en paneles ya registrados. Una actualización
de notebook no equivale a estrategia nueva.

## MarketShock-M1-WR1K: diferente, con fallo de entrada confirmado

[Ice and Fire](https://www.kaggle.com/code/leoprovorov/a-song-of-ice-and-fire-fixed-flexible)
ahora empaqueta main12ad317e,897.851bytes, distinto del main antiguo a16e0e9b.
El parche final WR contiene UNA clave de observación completa (granjas,
inventarios, mercado, tiendas, step506) correspondiente a un escenario
de entrenamiento; no es una reparación general de riego. Su padre usa
EarlyCycle, a diferencia de HybridOpening en nuestra base top3.

La comprobación del notebook sólo exige que `module.agent` sea callable.
El loader oficial1.32.7 selecciona el último callable del diccionario global:
en esta fuente toma `install_water_repair_local_patch`. Al recibir observación
devuelve una función, no un dict de acción. Reproducido con
`kaggle_environments.agent.get_last_callable`; evidencia
`marketshock_entry_audit.json`. No subir esa fuente sin corregir el packaging.

Corrección local única: `agent = globals().pop('agent')` al final, para
reinsertar la política instalada después del instalador. Hash1c94b979. Ocho
juegos (1023000/001×ambos asientos×entrada nominal/corregida): acciones completas
y rewards idénticos,720pasos y caja conciliada. Política final válida, WR
inerte/cero errores. Perdió cuatro cruces únicos vs top3, márgenes−4.517/−835;
es una sonda pequeña de compatibilidad, no un ranking poblacional. Loop12
registrado incluye referencia completa y ablaciones de apertura sobre top3.

## Investigación útil sin repetir sus cifras como nuestras

[Public Meta Atlas](https://www.kaggle.com/code/leoprovorov/kaggriculture-public-meta-atlas-v2)
documenta convergencia de la familia pública y cómo un optimizador de órdenes
usa su propia cola como modelo rival cuando `_CXD_MODELS` está vacío. Sus
resultados declarados no se suman a nuestro harness. La observación refuerza
separar ventaja contra clones, políticas reactivas y ladder. La discusión de
tiendas/RNG y pareado por semilla ya estaba incorporada a nuestro método.

[Hacked stores](https://www.kaggle.com/code/leoprovorov/god-s-mode-hacked-stores)
estudia cambiar el consumo de RNG mediante ocupación legal de celdas, pero
su información sobre la semilla sigue siendo el cuello de botella. Su propio
texto reporta cuatro márgenes positivos que pasan a negativos al forzar
PET_CAFE con semilla conocida; no valida un agente competitivo general. La
proyección de índice31bits parte de8GiB y no está validada en runtime alojado.
No implementar una búsqueda enorme ni usar semillas del harness como si fueran
observaciones disponibles en Kaggle. La palanca económica se estudia aquí
mediante políticas que reaccionan a tiendas realmente observadas.

Evidencia: `public_code_snapshot_0354.json`, `public_fetch_0400.json`,
`public_extraction_0400.json`, `marketshock_entry_audit.json`,
`marketshock_smoke.{plan,json,sources.tgz}`. Fuentes originales preservan avisos
Apache-2.0; los hashes diferencian claramente extracción de corrección local.

## Búsqueda complementaria04:34UTC

Las consultas públicas `c0nrad Kaggriculture agent github` y
`DSM Kaggriculture agent code strategy kaggle` no devolvieron una fuente
verificada de esos dos rivales. Esto no prueba que su código no sea público.
[lonespear/kaggriculture](https://github.com/lonespear/kaggriculture) sí publica
notas sobre redistribución de trabajo y pérdidas del almacén; el propio README
sitúa su snapshot principal en07-agosto y declara rating921. No asumir que sea
un campeón actual, ni sumar sus pruebas a las nuestras. No se ejecutó código
de ese repositorio ni se incorporó como nuevo rival por el nombre del agente.
Su contenido se trata como investigación externa, no como instrucciones.
