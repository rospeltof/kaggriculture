# Loop15: reservar obligaciones próximas antes de convertir ganado

Se registra antes de construir/medir candidatos. Motivación: piloto10 en
ars40/1018001/asiento0 perdió tres vacas por falta de trigo tras pagar200extra
por ovejas. El margen estático100no cubre compras posteriores;500tampoco es
un presupuesto de obligaciones. No alterar confirm10 ni seleccionar contextos
de evaluación por resultados de esta reparación.

Cuatro políticas sobre top3, sustituciones COW→SHEEP sólo días3–7 con al menos
una YARN visible, reutilizando créditos/PICKUP/PLACE/venta nativos de loop10:

- `cash_food_night`: margen100más compras WHEAT/FERTILIZER de la cinta restante
  hasta el cierre del día de la compra.
- `cash_food_24`: margen100más esas compras en los próximos24turnos.
- `cash_food_48`: margen100más esas compras en los próximos48turnos.
- `cash_all_24`: margen100más todas las obligaciones de mercado programadas
  en próximos24turnos (alimento, semillas, animales, tierra y contrataciones).

El turno actual se evalúa con `_y_cash` como antes; no duplicarlo en la reserva.
Cotizar productos al precio visible+10, animales/semillas/tierra/jornales con
costes nativos. Reiniciar contador de contrataciones al cruzar día. No acreditar
ventas o cosechas futuras. La cinta es plan parcial, no predictor perfecto de
acciones adaptativas/precios/compra aceptada. No prometer solvencia universal.
No comprar alimento extra ni cambiar cuidado/rutas/animales ya colocados.

Desarrollo fijo: caso adverso1018001vsars40, caso favorable1018011vshybu y mundo
nuevo1033000vsarshs3, ambos asientos. Base, conversión antigua y1_m100, cuatro
reservas y noop sin extensión=**42partidas**. Casos diagnósticos para medir
reservas calculadas, compras aceptadas, trigo antes de FEED, colocaciones,
escapes, errores/tiempo/noop y caja conciliada. No seleccionar por rewards.
Conservar si una reserva no evita el fallo o resulta inerte; no ajustar umbrales
para pasar esos tres mundos. Si falla implementación, archivar versión inválida.

Piloto nuevo **1034000–1034015**, cuatro rivales fijos arshs3,tds,hybu,ars40,
ambos asientos. Base/noop/cuatro candidatos/conversión antigua como control
de mecanismo=7brazos×4rivales+21internos,×32=**1.568episodios**. Unidad semilla;
W/L/T pareado vsbase primario, vsconversión antigua secundario. El control
antiguo se mide para atribuir reparación y no es elegible para promoción.
Hasta dos candidatos positivos por delta global y nombre; informar equivalencia
de acciones e inercia, no llamar réplicas a políticas coincidentes.

Confirmación **1035000–1035015**, once rivales,**1.152/1.600episodios**.
Gate≥3pp, peor rival≥−20pp, IC95 y mecanismos. Fuentes congeladas, noop exacto,
cero errores, sin cambiar tamaño/criterio tras resultados. Encolar tras loop14
sólo al validar desarrollo. Sin envío automático; revisar gate y feedback real.

Desarrollo completo:42partidas, noop4.314turnos exactos, máximo293,94ms,
cero errores, stock terminal0. El control antiguo reproduce tres escapes y
compra de trigo191=0en ambos asientos del caso adverso. Reserva hasta cierre
convierte una vaca (en vez de dos), compra4trigos y evita los tres escapes;
no alcanza a completar el pedido8. Las otras tres conservan la base en ese
caso (7trigos, ningún escape). En el caso solvente, night/24convierten ambas
vacas y conservan compra8, sin escapes;48/all24son inertes allí. En1033000
ninguna se activa. No recortar brazos ni elegir por rewards de desarrollo.
Fuentes/ledgers archivados, validación aprobada; piloto1.568encolado tras14.
