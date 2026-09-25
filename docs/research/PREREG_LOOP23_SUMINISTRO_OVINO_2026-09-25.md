# Loop23: contar el trigo del trabajador ovino adicional

Registrado antes de construir variantes y observar sus partidas. Origen:
replay113174624, seed1578791335, top3contra daviondk. El trabajador compacto
recibe sólo1de6trigos porque otro actor retira5primero; queda21turnos en
PICKUP0. Seis ovejas producen1en vez de4esa noche. La sonda dirigida601,
compra6→11, recupera24lanas vendidas en toda la partida y margen−2904→1255
contra acciones rivales grabadas. No es estimación competitiva ni candidato.

Hipótesis nueva: las guardas nativas proyectan retiradas de la cinta, pero no
la demanda del trabajador añadido. Actuar únicamente al contratar un peón
compacto ya comprometido, pendiente count1/targets6, fuera de días28/29 y
sin compra inicial. Proyectar campos/posiciones después de acciones propias,
spawn de contratados y demanda nativa del próximo turno antes del nuevo actor.
Sumar ovejas aún sin alimentar, en lugar de suponer que la compra6es suficiente.
No emplear seed, episodio, paso601, rival ni precio de venta conocido a futuro.

Dos variantes sobre top3:

- `sheep_supply_buy`: completar déficit ampliando compra existente posterior
  a la última venta de trigo, o añadiendo compra si hay sitio.
- `sheep_supply_hold`: primero reducir ventas de trigo existentes cuando sea
  físicamente seguro; completar resto igual que buy.

Conservar índices de órdenes existentes, compras originalmente previstas,
capacidad100, fondos conservadores sin ventas actuales, unidades intactas y
no actuar cruzando noche. No simular de nuevo el callback padre ni mutar sus
estados. `sheep_supply_noop` ejecuta la misma envoltura deshabilitada.
Registrar necesidad/predicción/órdenes emitidas, observación próxima y retirada
real del peón. Inconsistencia de predicción detiene promoción, no se oculta.

Desarrollo:1578791335,1057000,1057001, ambos asientos contra arshs3reactivo,
base/noop/dos candidatas =24partidas. Validar hashes/noop4.314, caja720DONE,
runtime<1s, compras/retiradas reales y alimento/producción/escapes/stock final.
Dos reproducciones adicionales dirigidas (base/candidata buy contra replay)
verifican que la regla general resuelve el mecanismo601; no seleccionan brazo.

Piloto1058000–1058031, seis rivales congelados del loop22, controlVQ elegible
sólo como diagnóstico:2.560partidas. Unidad semilla, ambos asientos, hasta dos
deltas positivos vs top3. Reportar cobertura, IC95dos vías, W/L/T; dinero no
selecciona. Confirmación disjunta1059000–1059031contra13rivales,3.712/4.800
partidas para uno/dos seleccionados. Gate≥3ppvs top3,≥0vsVQ, peor rival≥−20,
mecanismo reproducido y runtime. No autosubmit. Encolar tras22sólo con desarrollo
válido; no modificar fuentes de bloques activos.

Adenda de cobertura, después de completar los24desarrollos y antes de nuevas
partidas: ambas variantes son inertes en los seispares contra arshs3aunque
la guarda se consulta10veces por asiento en el mundo davion. La reproducción
general contra cinta sí actúa exactamente601. Para comprobar interacción con
rivales reactivos distintos, añadir24juegos dirigidos: mismo seed1578791335,
VQ/V7/HS4congelados, ambos asientos, base/noop/buy/hold. No cambiar piloto,
gate ni seleccionar variantes por resultados de este bloque. No afirmar cobertura
poblacional si sigue sin activarse; registrar ausencia como tal.
