# Loop8: selección de patrones del rival

Referencia top3 byte exacto sha9668e30a, independiente de resultados aún no
terminados de loops6–7. El beneficio confirmado de top3 frente a top1 sugiere
que reconocer varias rutas de venta merece una segunda ronda. Seis brazos:

- rank5/rank7: ampliar el conjunto de patrones que pueden anticipar una venta.
- history120/history360: adaptar con menos o más historia observada; el H48 de
  ventas propias permanece intacto. No repite pred_h96 del loop1.
- product3: escoger tres patrones por producto, evitando que el ajuste de lana
  determine el de leche. Requiere tres eventos observados de ese producto;
  en caso contrario conserva selección global. Misma tolerancia temporal±1.
- phase2: ajustar cada patrón por −2/−1/+1/+2 turnos sólo si mejora su ajuste
  pasado en más de2 unidades, después de penalización0,25×desplazamiento.

No cambia la oferta productiva, los productos autorizados, el umbral K4, la
ventana extendida ni el ritmo de recomputación. No usa observaciones futuras;
las cintas futuras de referencia son la biblioteca pública ya empaquetada.
El ajuste usa exclusivamente ventas observadas antes del callback actual.

Desarrollo antes del piloto: base, control de transformación global240/top3
y seis brazos, seed1012000, ambos asientos frente a arshs3 reactivo =16 juegos.
El control debe preservar1.438 acciones y ambos rewards. Cero errores, observar
telemetría de ajuste, medir máximo tiempo por callback y conciliación de caja.
Fallo mecánico se corrige/versiona antes de congelar. Rendimiento de este mundo
es diagnóstico, nunca criterio de selección.

Piloto: **1013000–1013007**, ocho rivales fijos de loop1, ambos asientos,
base/noop+seis candidatas:92 cruces×16=**1.472 episodios**. Se amplía de antemano
a ocho mundos para disminuir dependencia de cuatro semillas. No selección
adaptativa de rivales. Primario delta W/L/T frente a top3, unidad semilla;
reportar intervalos por semilla/dos vías y cobertura de cambios de acciones.
Seleccionar hasta dos positivas, orden delta descendente y empate alfabético.

Confirmación disjunta **1014000–1014015**, once rivales de confirm1 y ambos
asientos:1.152/1.600 episodios. Gate≥3pp en once rivales, ninguno<−20pp,
controles y runtime válidos, revisión de un mecanismo favorable y desfavorable
si existe. Lo local no garantiza ladder; examinar feedback real antes de gastar
otro envío. No modificar agentes después de comenzar un bloque.

Encolar detrás de loop7; un único torneo grande a la vez. No hace envíos
automáticos. Nuevas hipótesis, datos y hashes quedan archivados para no repetir.

Validación terminada:16 juegos, control de transformación con1.438 acciones
idénticas y rewards iguales; cero errores, máximo270,8ms entre estos callbacks.
Todas las seis variantes cambian acciones; product3 registra833 ajustes por
producto/asiento, phase2 usa114 patrones desplazados/asiento. Esto confirma
ejecución en el mundo de desarrollo, no mejora. Fuentes completas archivadas
en `patterns_smoke.sources.tgz`, manifiesto `patterns_variants.json`; runner
encolado tras loop7. Runtime se revisará también en los bloques aleatorios.
