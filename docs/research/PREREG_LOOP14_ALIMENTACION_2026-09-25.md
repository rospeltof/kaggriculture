# Loop14: valor económico de alimentar al ganado

Motivación: auditoría de los ocho replays de top3 ya seleccionados antes por
recencia. Reconstrucción720estados por juego, sin escoger nuevos resultados.
Los PASS pueden anticipar trabajo que otro actor completa: tras observar el
estado justo antes del refresh no quedan CARE omitidos en animales alimentados
con producción futura útil entre esas oportunidades.60casos
únicos día/tile sin WATER no añaden yield inmediato/siguiente amanecer ni
previenen muerte esa noche según reglas del motor. No convertir todos los
PASS en trabajo por asumir que son desperdicio.

Sí quedan261casos únicos día/tile sin FEED con oportunidades previas de
alimentar. No afirmar que todos sean errores ni que todos procedan del mismo
filtro. La base tiene `_r85_feed`, que omite alimento si un valor estimado de
CARE perdido es menor que el precio del trigo, garantizando alimentación
programada mañana o fin de juego. `_r88_feed_bonus_cost` respeta fase y
horizonte pero usa precio actual del producto. El tradeoff puede ser ahorro
real o infraproducción; se prueba causalmente, no se infiere por más ganado.

Cuatro brazos sobre top3 sha9668e30a, sin cambiar compras, recorridos, activos
ni instrucciones de CARE:

- `feed_half`: multiplicador de valoración0,5 en vez de1,25; omite más FEED.
- `feed_double`:2,5; omite menos FEED. Es el doble del multiplicador original.
- `feed_keep_sheep`: regla original salvo que nunca recorta FEED de SHEEP.
- `feed_all`: desactiva únicamente el filtro `_R85_FEED`, preserva todo FEED
  que el padre solicitaba. No crea nuevas visitas ni obliga a alimentar donde
  el plan padre no lo hacía.

Se reutiliza literalmente el cuerpo nativo de `_r85_feed` por AST, salvo
esas dos condiciones, y se captura el último callable correcto de top3.
`feed_noop` con1,25/sin excepción ovina exige igualdad completa de acciones.
La retirada económica de fertilizante y demás guardas siguen como estaban.

Desarrollo: **1030000**, **1004000**, **1272457736**, ambos asientos contra
arshs3 reactivo; base/cuatro/noop =**36juegos**. Mundos diagnósticos, no estimador
competitivo. Contar solicitudes, FEED aceptados/consumo real por especie,
CARE aceptados, cosechas reales, compras/ventas, pérdidas de almacén, animales
sin alimentar al cierre y escapes. Comprobar noop, errores, fuente y tiempo.
No elegir brazos por dinero o resultados de estos tres mundos.

Piloto nuevo **1031000–1031015**, cuatro rivales fijos arshs3,tds,hybu,ars40,
ambos asientos: seis brazos×4+15internos,×32=**1.248episodios**. Unidad semilla,
W/L/T pareado primario; hasta dos positivas por delta y luego nombre. Noop
exacto, cero errores. Reportar si distintos brazos son inertes o coinciden.

Confirmación **1032000–1032015**, once rivales,**1.152/1.600episodios**.
Gate≥3pp y peor rival≥−20pp; IC95, mecanismo, tiempo. Reservas de grano y
producción pueden reaccionar: el efecto competitivo es total, con rival reactivo.
No interpretar caja bruta como ganancia ni cambiar umbral después de observar.
Encolar detrás de loop13 sólo tras validar desarrollo. Sin envío automático.

Desarrollo completo:36juegos, noop4.314turnos exactos, máximo271,1ms. Cero
errores/escapes/inventario final; tiendas iguales a base. Las cuatro políticas
cambian acciones en los tres mundos. Cada FEED aceptado consume un trigo,
verificado directamente en motor. En1030000, alimentaciones COW177→161 con
half,190con double y201con all; milk242→228/256/266respectivamente.
No seleccionar por esas cantidades o rewards:
más producción puede reducir precio y caja. Fuentes/ledgers de campo y mercado
archivados; piloto1.248encolado tras loop13.
