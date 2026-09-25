# Dos fuentes públicas nuevas y validación de entrada

Consulta del catálogo **2026-09-25 05:47:41 UTC**, descargas 05:48:03–05:48:05.
Se extrajo el literal `AGENT_B64`; no se ejecutaron los notebooks completos.
Los avisos Apache se conservan. Versiones archivadas en `public_sources_0548.tgz`.

| Fuente | Última ejecución declarada UTC | SHA256 del agente |
|---|---|---|
| [The 2965 Master Hybrid Engine](https://www.kaggle.com/code/haideptry/the-2965-master-hybrid-engine) | 04:09:14 | `cda529cb6b359fc4a9ab124d4d7950d5912bd5de846dcec4be70ca83b7150b2d` |
| [The Shepherd's Ledger Herd Safe Sovereign](https://www.kaggle.com/code/haideptry/the-shepherds-ledger-herd-safe-sovereign) | 04:09:40 | `8378f73c82db7624ce5d0369cf896aa0761a662af147b119f67254f1f8634c56` |

Ambos difieren de los agentes locales anteriores; no se sobrescribieron los
rivales `hsov`/`h2965` de los paneles congelados. La fecha, el nombre y las
afirmaciones externas de dominancia no prueban fuerza competitiva.

## Lectura del código

V7 agrupa protección del almacén, reajuste de cantidades, anticipación de
ventas, poda de semillas tardías, fusión de órdenes, control de inventario y
recogida de trigo para alimentar. La fusión también abarca compras; no extender
la afirmación de invariancia de compras de una capa a todo el paquete. La
recogida extra usa al granjero, pasos192–695, hasta2trigos y reserva2en almacén.

HS4 anticipa ventas futuras de MILK/WOOL/STRAW de su propia cinta y descuenta
después el crédito correspondiente. Su indicador `_HS4_T4_OPP_PREEMPT` sólo se
inicializa/reinicia aFalse: el adelanto de2turnos de esa capa no se activa. El
forecast nativo de4turnos sigue existiendo; no es correcto llamarlo todo inerte.
Las listas CXD de modelos están vacías y recurren a una cola espejo; no son
acceso al inventario privado rival ni demostración de predicción acertada.

Los dos módulos auxiliares ejecutados desde literales coinciden en hash con
los ya inspeccionados del padre. La ruta de carga externa está desactivada con
`path=None`. No hubo ejecución del código de publicación del notebook.

## Entrada y diagnóstico

La primera sonda exigía identidad de objetos entre el último callable y
`agent`. Falló **en nuestra aserción**, antes de jugar con las fuentes nuevas:
la entrada nominal es un wrapper trivial de `v7_hr_agent` o `hs4_ig_agent`, que
son las entradas oficiales. No fue un error del agente ni una partida perdida.
Se conservan la sonda v1 y `public_0548_smoke.v1_failure.json`.

Sonda v2: **24 partidas completas**, semillas1042000/1042001, ambos asientos,
rival top3 reactivo. Noop exacto **2.876 turnos**; entrada oficial/nominal con
acciones de ambos jugadores y recompensas idénticas **5.752 turnos**. Caja
conciliada para los dos jugadores en cada partida; máximo **431ms/turno**.
No hubo estados fatales ni errores en los contadores nuevos V7/HS4 observados;
no se recopilaron exhaustivamente todos los contadores internos heredados.

V7 cambia133/122turnos propios en los dos mundos; HS4 cambia77/72. Tiendas
idénticas a base, cero escapes observados, cero productos en almacén/bolsas
al final. Quedan1/5semillas respectivamente: no afirmar inventario total0.
HR recoge1trigo extra y el adelanto HS4 aplica créditos; la capa de2turnos
permanece en0. Esto valida ejecución, no utilidad ni superioridad en el ladder.

`verificar_publicos_0548.py` reproduce hashes, cobertura, controles, igualdad
de entradas y caja desde las evidencias. El **loop18** registra704episodios
nuevos y confirmación disjunta si procede. Encolado después de16, porque17se
detuvo en desarrollo. No hay envío nuevo ni selección por estos24rewards.

Fuentes de evidencia: `public_code_snapshot_0548.*`, `public_fetch_0548.json`,
`public_extraction_0548.json`, `public_0548.entry_audit.json`,
`public_0548_smoke_v2.*`, `public_0548_validation.json`, en
`docs/evidencia/loop_publicos_20260925/`.
