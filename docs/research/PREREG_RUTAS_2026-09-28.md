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
