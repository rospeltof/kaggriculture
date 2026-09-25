# Loop12: aperturas nativas y nueva referencia pública

Motivación: la actualización pública MarketShock usa EarlyCycle, mientras
top3 usa HybridOpening. Cambian la caja inicial y el uso temporal de un futuro
pastizal. La base contiene además un modo TomatoInsteadOfCow aún no evaluado
en este loop. Los antiguos barridos de apertura de HOZ/C95 no usaban este
chasis público; no transferir su refutación sin probar esta política concreta.

Tres ablaciones sobre top3 sha9668e30a:

- `open_original`: cinta inicial nativa sin el intercultivo temporal de trigo.
- `open_cycle`: conserva intercultivo, sustituye órdenes iniciales por compra
  de5trigos+1semilla y desactiva CT_TABLE; mecanismo de financiación distinto.
- `open_tomato`: EarlyCycle y reemplaza una de dos primeras vacas por un tomate
  en(4,4), con riego/cosecha por las visitas nativas y venta de stock observado.
  Presupuesto/rutas/cuidado pueden cambiar mucho; no asumir mejora por liberar350.

Cuarta candidata `marketshock`: paquete público completo MarketShock-M1-WR1K,
fuente12ad317e y sólo corrección de entrada. El cargador oficial seleccionaba
el instalador y devolvía una función; reinsertar `agent` al final lo corrige.
Ocho juegos de control (dos semillas×asientos×dos entradas) prueban igualdad
completa con la política `module.agent` del autor, no fuerza general. Su parche
de riego necesita una observación exacta de entrenamiento y no se activó.
Se perdió0–4 contra top3 en esos dos mundos; no se descarta ni promociona por
esa muestra dirigida de compatibilidad. No se ejecutó el notebook externo.

Desarrollo previo al piloto: seed1024000, ambos asientos vsarshs3 original,
base/tres ablaciones/MarketShock/noop HybridOpening =12juegos. Verificar
noop completo, compras/producción aceptadas, reporte de apertura, errores,
stock al cierre y tiempo. Contar muertes/escapes si aparecen. Son diagnósticos;
no elegir brazos por sus rewards, no usar esta semilla para estimar mejora.

Piloto **1025000–1025007**, ocho rivales públicos originales de loop1,
ambos asientos;6brazos×8+15internos,×16=**1.008episodios**. Seis brazos
incluyenbase/noop/cuatro candidatas. Unidad semilla y primario W/L/T pareado;
hasta dos positivas por delta y luego nombre. Controles exactos y cero errores.

Confirmación **1026000–1026015**, once rivales de confirm1, ambos asientos,
1.152/1.600episodios. Gate≥3pp y ningún rival<−20pp. Informar IC, mecanismo
y tiempo; no cambiar umbral tras observar resultado. Mercado/endógeno y tiendas
cambiantes forman parte del efecto total, no usar cintas rivales pasivas.

Validar, congelar y encolar después de loop11. No enviar automáticamente.
La actualización pública MasterEngine02:50UTC resultó tds25 byte exacto,
sha127ed3e6: excluida antes del piloto para no repetir public_refresh.

Desarrollo completado:12juegos, noop1.438turnos exactos y máximo228,4ms.
Original cambia42turnos, EarlyCycle sólo1 y mismos rewards en este mundo;
Tomato cambia261, compra una vaca menos y cosecha/vende cuatro tomates en
195/218/246/267. No confundir capacidad teórica de la planta con producción.
Inventario privado final0 en todos. MarketShock tiene un escape de ganso en647
por asiento, documentado; no borrar el caso. Sin errores fatales/contadores
observados. La telemetría heredada espera trigo en53, pero base/EarlyCycle
lo cosechan en87(3unidades); Tomato/MarketShock sí cosechan en53(2unidades).
Validación/mecanismo conservados; no seleccionar por rewards de este mundo.
