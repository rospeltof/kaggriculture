# Evidencia transportable del experimento de lotes

Copiada de `results/` sin nuevas simulaciones. Estos archivos están fuera de
las reglas de exclusión de Git; aún hay que incorporarlos a un commit para que
viajen en un clon. `indice.json` declara origen local, tamaño y SHA-256.

| Archivo | Contenido |
|---|---|
| `veredicto.json` | Resúmenes, intervalos, deltas por semilla, transiciones y decisión |
| `sonda_99000.json` | Acciones iniciales divergentes, cohortes y controles de la sonda |
| `pares_101000.json`, `pares_102000.json` | W/L/T por brazo y (cinta, semilla), asientos promediados |
| `manifiesto_101000.json`, `manifiesto_102000.json` | Configs exactas, seeds, fuentes/cintas, versiones y resultado |
| `episodios_101000.jsonl.gz`, `episodios_102000.jsonl.gz` | Los 1.280 y 2.560 episodios con rewards, estados y hashes de acciones |
| `fuentes_panel.tgz` | Fuentes exactas de barrido/chasis/arquetipos/tape/harness usadas en ambos bloques |

Los manifiestos conservan sus rutas originales `results/...`; esta tabla y el
índice indican sus copias transportables. Los originales no fueron reescritos.
Los hashes de acciones permiten verificar igualdad, **no reconstruir las acciones**.
La sonda sí contiene la primera diferencia y los plantados observados.

Las 40 cintas no se duplicaron aquí: los manifiestos enumeran sus nombres y
hashes; sus archivos están en `bots/meta/tapes/`. El generador verifica que estén
presentes e idénticos. Si faltan en otro checkout, no se podrá repetir el panel.
No incluye replays privados ni credenciales.

En el JSON de la primera sonda, `executed_seed_buys` es una inferencia por stock
y una cota inferior si un PLANT muere en el mismo refresh nocturno. La sonda
actual usa el nombre `seed_buys_lower_bound`; no se altera el archivo histórico.

Verificar y preparar contexto sin red ni simulaciones:

```bash
python3 preparar_contexto_llm.py
```

Para leer un JSONL comprimido usar `gzip.open(..., 'rt')`. Para las fuentes
usar `tarfile.open(..., 'r:gz')` y leer miembros; no hace falta extraer ni ejecutar.
El generador comprueba hashes, controles, pares y estadísticas primarias.
