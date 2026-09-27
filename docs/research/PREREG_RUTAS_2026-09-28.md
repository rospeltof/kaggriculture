# Pre-registro — router por par de tiendas (ruta 0 frente a la tabla EXP240)

Escrito antes de ver datos. 2026-09-27 23:10 UTC.

- **Precedente:** lucky-boy (leoprovorov) remapeó 10 pares a la ruta 0 en arshs3 tras
  un test de repetición forzada. tds27 usa el mismo router y las mismas tablas.
- **Criba (`torneo_rutas0`):** tds27top3 frente a `forzar_ruta.py ... r0` (ruta 0 del
  paso 144 al 647 en todos los pares), contra tds27 y cha22, semillas 4200000-4200299,
  dos asientos (3.000 partidas). Cada partida guarda su par de tiendas (`shops2`).
- **Selección (fijada ahora):** un par (a,b) entra en el remapeo a ruta 0 si tiene
  ≥ 4 celdas (rival × semilla, asientos promediados), delta medio de W/L/T > 0 **y**
  delta medio de margen propio > 0 (misma señal que usó lucky-boy).
- **Confirmación:** tds27top3 frente a tds27rf (`forzar_ruta.py ... remap:pares.json`),
  semillas 4300000-4300059 (60 nuevas), dos asientos, rivales tds27 y cha22 (los dos
  linajes que dominan la población). Adoptar si el delta pareado tiene IC95 por
  semilla > 0, con ningún rival con IC entero < −10 pp. Si no, se descarta.

## Resultado de la criba ruta 0 (torneo_rutas0, 3.000 partidas, 0 errores)

Ruta 0 en todos los pares es mucho peor: vs cha22 54,7% (tds27top3 80,7%), vs tds27
26,2% (tds27top3 64,0%). Por la regla se seleccionan 4 pares (BRUNCH/BRUNCH,
PIZZA/PIZZA, BAKERY/BRUNCH, FARMERS/FARMERS; 8-18 celdas cada uno), ~6% de las
partidas, con efectos que dependen del rival (BRUNCH/BRUNCH: +56 vs cha22, −44 vs
tds27). Ganancia global esperada ≤ ~1,5 pp: confirmación aplazada por baja potencia.

## Adenda (antes de ver datos): pares con YARN_STORE → ruta EXP240

Hoy los 15 pares con YARN van a la ruta 9 (`_V92_TABLE`); ~23% de las partidas.
Variante `tds27_yarnexp` (remap a `_R108_SHOP_ROUTES`). Criba: mismas semillas
4200000-4200299, rivales y asientos que torneo_rutas0; se reutilizan las partidas
de tds27top3 (determinista). Regla: igual que la de ruta 0, por par; y además el
agregado sobre todos los pares YARN: si delta W/L/T > 0 y margen > 0, pasa a
confirmación con semillas nuevas.

## Resultado de la criba YARN (torneo_rutasyarn + partidas de tds27top3 de torneo_rutas0)

Agregado pares YARN: **−38,8 pp, margen −$2.037** (98 celdas; vs tds27 −40,6, vs cha22
−37,0). Solo YARN/SMOOTHIE pasa la regla por par (7 celdas, ruido). **REJECTED**: la
ruta 9 de `_V92_TABLE` es muy superior. Conclusión del frente: las tablas del router
de tds27 están bien afinadas; mejoras por par pequeñas, ruidosas y dependientes del rival.
