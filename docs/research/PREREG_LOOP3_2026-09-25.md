# Loop 3: elegir animales por valor económico y oferta visible

Registrado antes de correr. Revisión de VQ: `_HD2_FUTURE=0` omite demanda
esperada de tiendas futuras en el modelo de elección de gansos/vacas/ovejas.
La capa posterior `_y_target` convierte vacas en ovejas si existe YARN_STORE,
sin valorar el inventario ni la oferta futura del rival. No es el antiguo
barrido de tamaño de rebaño de HOZ; se conserva cantidad y logística del agente
público fuerte y se cambia el criterio de especie en sus compras previstas.

El ledger real 113056789 muestra más leche/lana vendida por nosotros pero
menores ingresos en ambos productos que el rival. No prueba que estas nuevas
reglas lo resuelvan: fundamenta medir oferta y precios conjuntamente.

## Hipótesis

Constructor `construir_herd_loop.py`, base VQ 9b463dfb, atribuciones conservadas.

- `herd_future`: demanda esperada de nuevas tiendas con peso 1 en `_hd2_ev`.
- `herd_ev600`: reemplazar la regla binaria de YARN_STORE por comparación del
  valor previsto de dos vacas versus dos ovejas, incluyendo oferta de ambos,
  precio endógeno y coste. Requiere ganancia modelada de 600. Sólo días 8–11
  y tamaños que la capa heredada ya permitía. Mantiene control de caja y créditos
  de compras efectivas; no convierte estructuras a tipos nuevos.
- `herd_ev1500`: mismo mecanismo con umbral 1.500.
- `herd_ev_future`: EV600 + demanda futura. Factorial parcial permite comparar
  A, B y A+B en vez de asumir aditividad.

Potencial HIGH, confianza LOW. Riesgos: el modelo supone más cuidado del que
ofrece la ruta, usa el mismo calendario de cosecha tras cambiar especie, y
modela imperfectamente reposición/demanda y reacción rival. Diagnosticar cambios
de compras, producción aceptada y precios si aparece señal o daño.

## Diseño

Base/noop + cuatro candidatas, mismos ocho rivales públicos congelados.
**1001000–1001003**, ambos asientos: 48+15 cruces, **504 episodios**.
Primario delta W/L/T pareado; otros brazos excluidos. Noop exacto, cero errores,
fuentes archivadas y máximo por turno. Ejecutar después del pipeline loop1/2,
sin añadir ocho workers a corridas ya activas.

Confirmar hasta dos candidatas con delta >0, orden por delta y nombre, en
**1002000–1002015**, pool fijo expandido a once: ocho originales más tds25,
hl25 y arshs3 original. Dos candidatas 1.600 episodios, una 1.152. REAL_WORLD_CANDIDATE
si delta confirmado ≥3 pp sin rival <−20 pp; IC amplio informado, no veto binario.
Promoción a campeón requiere además evidencia real. Si ninguna mejora, pasar
a otra familia de mecanismos conservando este resultado.
