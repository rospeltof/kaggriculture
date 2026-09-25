# Loop9: rebaño adicional con demanda visible

Motivación: replay top3–c0nrad113107623, auditado en720 estados y transacciones
aceptadas. Rival32 ovejas contra17 nuestras,759 lanas contra391; ingresos por
lana113.264 frente a69.502 y menores jornales/tierra. Un caso genera hipótesis,
no demuestra mejora general. No se usa su cinta como rival ni se repite el
modelo de tiendas futuras que fracasó en loop3.

Seis brazos sobre top3 sha9668e30a:2/3/6 ovejas, inicio día12 o14. Usan filas7–8
del SE ya comprado y libre; un peón por grupo de hasta tres. Sin compra de
tierra ni sustitución de animales o peones del padre. Contratan desde hora4
para conservar ventana R51 y sólo tras las reservas de los proyectos del padre.
Prioridad inicial construir/colocar/alimentar todos; luego cuidar. Prioridad
diaria feed/care, lana, fertilizante; reservar regreso y descarga de ambos
productos. Comprar alimento incremental y evitar que ventas del padre lo
consuman antes de recogerlo. Comprobar inventario, dinero e índices observados.

Se requiere≥2 YARN visibles y margen modelado≥600. Proyección sin tiendas
futuras: demanda actual, ovejas visibles en ambas granjas, oferta nueva finita
hasta día29,5 unidades por primera cosecha y3 siguientes (descuento por tiempo
de cuidados/entrega). Costes: compra, alimento al precio actual+5 y jornales
Fibonacci adicionales previstos sobre cinta+proyecto del padre. No incluye
retorno del fertilizante. Omite nuevas compras rivales y cambios futuros de
demanda; rentabilidad modelada no garantiza beneficio ni W/L. Reserva inicial
4.000, mantenimiento1.000. Dejar de alimentar tras la última noche productiva;
cosechar lo pendiente y no comprar trabajo tras vaciar la última lana.

Desarrollo: seed1004000, mundo SE ovino ya conocido. Base+seis candidatas+noop
tamaño0+forzadas2/3/6 para activar controlador =11 brazos×ambos asientos=22
partidas. Forzadas sólo omiten margen económico, siguen requiriendo dos YARN,
espacio/caja/tiempo. No usar rewards para seleccionar; confirmar colocación,
alimento, lana real, retornos y ausencia de fallos de compra/contratación o
errores. Noop debe mantener1.438 acciones y rewards de ambos jugadores.
Contar escapes previos a la última producción por separado de los posteriores.
Versionar y repetir diagnósticos ante fallo antes de congelar candidatas.

Piloto: **1015000–1015015**,16 semillas nuevas, ambos asientos, cuatro rivales
fijados: arshs3 original, tds, hybu, ars40.8 brazos×4 rivales+28 cruces internos,
×32=**1.920 episodios**. Más mundos para cobertura de inversión espacial rara.
Primario delta W/L/T contra top3, unidad semilla; informar IC semilla/dos vías,
acciones cambiadas, cobertura y runtime. Hasta dos positivas, por delta y
desempate alfabético. No elegir por dinero bruto ni mezclar mundos dirigidos.

Confirmación disjunta **1016000–1016015**, once rivales de confirm1, ambos
asientos:1.152/1.600 partidas. Gate≥3pp en once rivales, ningún rival<−20pp,
controles exactos, runtime y mecanismos revisados. Subpanel de los cuatro
del piloto sólo diagnóstico. No cambiar gate después de observar resultados.

No encolar antes de validar controlador; ejecutar detrás de loop8, un único
torneo grande. No envíos automáticos. La edad y feedback de top3/VQ también
cuentan al decidir otra prueba real. No modificar fuentes durante cada bloque.

Primer intento de desarrollo abortó tras el primer juego base: el script
reutilizaba `path` para guardar el ledger y luego intentaba compilar ese gzip
en el segundo asiento. Corregido sólo en la sonda, sin cambiar candidatas;
`sheep_space_smoke_v2` repite el bloque y verifica el archivo de fuentes
original `sheep_space_smoke.sources.tgz`. No son dos experimentos competitivos.

El bloque smoke_v2 completó22 juegos del agente v1: sin errores/escapes tempranos,
36/53/105 lanas cosechadas en forzadas2/3/6, padre108 lanas/R51 siete
aplicaciones. Flujo de forced6 detectó cosechas tan tardías que parte de la lana
acababa en depósito automático nocturno: no bastaba regresar cuando ya había
carga. **Agente v2** filtra trabajo opcional por viaje+cosecha+entrega restantes,
y no inicia otra tarea si pone en riesgo carga existente. Mismo diseño económico.
Smoke_v3 repite22 juegos con nuevas fuentes/hashes:36/53/83 lanas, cero carga
suelta en la última hora, pero varias PLACE coinciden conh23. Sonda adicional
instrumenta directamente `_apply_unit_action` del motor real para confirmar
las descargas antes del reset; no confundir orden PLACE con aceptación.

Verificación directa terminada:36/53/83 unidades cosechadas y depositadas
aceptadas, ambos asientos, seis episodios adicionales. Ninguna se quedó en
tránsito al cierre. Se preservan108 lanas del padre y siete aplicaciones R51.

**Enmienda antes del piloto,03:20UTC:** v2 omitía oferta propia ya comprometida
en ovejas transportadas/shed y lana privada. V3 la incorpora, sin tiendas
futuras ni cambiar umbral, tamaños, fechas, semillas o rivales. En mundo de
desarrollo había6 ovejas sin colocar y8 lanas privadas; ingreso proyectado
de sheep3_d12 cae9.637→4.157 frente a coste8.615, y rechaza la inversión.
Smoke_v4:22 juegos nuevos; controles exactos y seis forzadas con hashes de
acciones de AMBOS agentes/rewards idénticos a v2. Conserva así la prueba directa
de entregas del motor. Seis candidatas normales inertes en ese mundo dirigido;
no se eliminan ni seleccionan por ese resultado. Fuentes v3 archivadas en
`sheep_space_smoke_v4.sources.tgz`; manifiesto previo preservado como
`sheep_space_variants_v2.json`, actual `sheep_space_variants.json` pasa a v3.
Runner aún esperaba loop8; piloto9 no había iniciado. Regla competitiva intacta.
