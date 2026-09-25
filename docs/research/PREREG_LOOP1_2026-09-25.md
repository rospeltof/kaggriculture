# Loop continuo 1: producción y extensión de señales útiles

Registrado antes de evaluar. El usuario pidió explícitamente continuar un loop
con muchos experimentos, sin detenerse al cerrar cada ronda. VQ sigue como
referencia local; el original arshs3 y VQ están activos en ladder.

## Hipótesis y riesgos

Base SHA 9b463dfb; constructor `construir_loop_publicos.py`. No se repiten VQ,
ADV, gate/off ni paquetes tds25/hl25. Se aíslan mecanismos dentro de VQ:

| Variante | Cambio | Hipótesis | Potencial / confianza | Riesgo |
|---|---|---|---|---|
| crop40 | Mezcla 40% precio a tres días | Evitar sembrar para un precio que desaparecerá | HIGH / LOW | Oferta futura sobreestimada |
| crop80 | Misma estimación, 80% | Mayor respuesta a la saturación visible | HIGH / LOW | Error de modelo amplificado |
| crop_end26 | Fin de siembra alternativa d26, buffer 6 | Menos capital y semillas que no producen al cierre | MEDIUM / LOW | Perder última cosecha útil |
| crop_edge0 | Margen mínimo 0 en vez de −15 | No sustituir trigo cuando la zanahoria pierde margen previsto | HIGH / LOW | Modelo omite valor de alimento/rutas |
| pred_top3 | Tres patrones rivales en vez de uno | Cobertura de políticas con timing variable | HIGH / MEDIUM | Más falsas alarmas |
| pred_h96 | Venta propia planeada hasta 96 turnos | Aprovechar presión rival aunque la cinta venda más tarde | HIGH / MEDIUM | Renunciar a demanda futura |
| pred_fast2 | Actualizar cada turno, señal mínima dos unidades | Responder a ventas pequeñas y cambios rápidos | HIGH / MEDIUM | Adelantos excesivos y coste CPU |
| pred_window6 | Extensión de 4 a 6 turnos, mismo filtro lejano | Ampliar alcance conservando la protección inmediata | MEDIUM / LOW | Predicción lejana imprecisa |

La idea crop proviene del código público Harvest Ledger (sha 1dfd4630), cuyo
paquete completo no mejoró. Esto aísla valoración, sin adoptar simultáneamente
sus otros cambios. Forecast ablation reveló gran valor de la capa; expandir su
cobertura es una dirección distinta de volver a filtrarla o desactivarla.

## Piloto amplio

Base/noop y ocho variantes; ocho rivales congelados: tds viejo, hybu, ars40,
hsov, v13, obr, h2965, guru6. Semillas **995000–995003**, ambos asientos.
10 brazos y ocho rivales: 80 cruces con pool + 45 entre brazos, **1.000 episodios**.
Métrica primaria delta pareado W/L/T vs VQ en los ocho rivales comunes; otros
brazos excluidos de la estimación. Directos, monedas y hashes son diagnósticos.
No mirar resultados parciales para cambiar la muestra o las variantes.

Seleccionar hasta tres candidatas con delta >0, ordenadas por delta, desempate
alfabético; máximo dos de una familia (crop/pred). Si no hay positiva, continuar
con una nueva hipótesis estructural, sin ampliar este mismo piloto para rescatarlo.
Intervalos amplios no son rechazo automático. Sin cambios W/L/T pero acciones
diferentes = neutral en este panel, no parche inactivo.

## Confirmación

Base/noop más seleccionadas; semillas **996000–996015**, disjuntas. Pool expandido
fijado ahora: los ocho previos + tds25 + hl25 + arshs3 original. Reportar por
separado ocho rivales comunes y tres adicionales; principal = once equiponderados.
Con tres candidatas: (55+10) cruces ×32 = **2.080 episodios**; con dos: 1.600;
con una: 1.152. No cambiar rivales tras ver qué beneficia a cada variante.

Puede justificar REAL_WORLD_CANDIDATE: delta confirmado ≥3 pp y ausencia de
regresión >20 pp por rival, aunque IC cruce cero. Un resultado con daño claro,
bugs o exceso de tiempo se rechaza. Ninguna selección local implica CHAMPION.
Una señal específica grande se documenta para otro experimento, sin cambiar
retrospectivamente esta regla. Si hay varias candidatas positivas, estudiar
combinación en un bloque nuevo que incluya A, B y A+B, con semillas nuevas.

## Integridad

Usar `torneo.py`, `validar_torneo.py`, `pareado_torneo.py`; noop exacto, cero
errores, ambos asientos y fuentes archivadas. No modificar runner/agentes en
ejecución. Controlar máximo de tiempo por turno. Guardar resultados, mecanismos,
estado y siguiente hipótesis antes de pasar al bloque siguiente. Este preregistro
define una ronda del loop, no una razón para detener toda la investigación.
