"""Construye el informe final desde bloques completos; cero simulaciones."""
import json
from evaluar_lider import ROOT, OUT


def read(name):
    return json.loads((OUT / name).read_text())


def interval(values):
    return "inválido" if values is None else f"[{100*values[0]:+.2f}; {100*values[1]:+.2f}]"


def main():
    register = read("confirmacion_registro.json")
    candidate = register["candidate"]
    pilot = read("pilot.meta.json")
    confirm = read(f"confirm_{candidate}.meta.json")
    stress = read(f"stress_{candidate}.meta.json")
    duel = read("duelo_hoz.json")
    assert all(m["state"] == "complete" for m in (pilot, confirm, stress, duel))
    effect = confirm["summary"][candidate]["delta"]
    control = confirm["summary"]["_peor"]["delta"]
    positive = all(effect[k] is not None and effect[k][0] > 0 for k in ("seed_ci95", "twoway_ci95"))
    negative_control = all(control[k] is not None and control[k][1] < 0 for k in ("seed_ci95", "twoway_ci95"))
    passed = effect["mean"] >= .15 and positive and negative_control
    verdict = ("Salto local confirmado según el criterio registrado" if passed else
               "Mejora positiva en este panel, sin alcanzar el umbral registrado de 15 puntos"
               if positive and negative_control else
               "No se confirmó el salto local con todos los controles exigidos")
    lines = ["# Resultados de la ronda del líder — 2026-09-14", "",
        f"**{verdict}.** El candidato `{candidate}` mejora {100*effect['mean']:.2f} puntos W/L/T frente a HOZ en confirmación. No se envió nada a Kaggle; `CAMPEONA_HOZ` y `submission/main.py` siguen intactos.", "",
        "[Análisis de los ocho replays](ANALISIS_LIDER_2026-09-14.md) · [Protocolo anterior a las pruebas](EXPERIMENTOS_ATREVIDOS_2026-09-14.md) · [Evidencia](evidencia/lider_20260914/README.md)", "",
        "## Confirmación independiente por semillas", "",
        "Panel fijo: 40 cintas históricas y ocho rivales extraídos de los nuevos replays; 19 semillas 215000–215018, ambos asientos. Cuatro brazos, 7.296 episodios; 1.824 por brazo. W/L/T vale victoria=1, empate=0,5, derrota=0. Deltas e intervalos en puntos porcentuales frente a HOZ.", "",
        "| Brazo | W/L/T | Delta | IC95 por semilla | IC95 dos vías |",
        "|---|---:|---:|---:|---:|"]
    for arm in ("base", "noop", "_peor", candidate):
        r = confirm["summary"][arm]; d = r["delta"]
        lines.append(f"| `{arm}` | {r['score']:.2%} | {100*d['mean']:+.2f} | {interval(d['seed_ci95'])} | {interval(d['twoway_ci95'])} |")
    lines += ["", "Desglose descriptivo de confirmación (no cambia la regla primaria):", "",
              "| Rivales | HOZ | Candidato | Delta |", "|---|---:|---:|---:|"]
    for prefix,label in (("lad_","40 históricos"),("sepopp_","8 nuevos")):
        b=confirm["summary"]["base"]["strata"][prefix]
        c=confirm["summary"][candidate]["strata"][prefix]
        lines.append(f"| {label} | {b:.2%} | {c:.2%} | {100*(c-b):+.2f} |")
    lines += ["", f"Regla registrada: delta ≥15 puntos, ambos intervalos del candidato por encima de cero y ambos del control FB por debajo de cero. Candidato positivo en ambos: **{positive}**; control FB negativo en ambos: **{negative_control}**. El umbral de 15 se aplica al estimador puntual, no al límite inferior del intervalo.", "",
        "El tamaño de 19 semillas se fijó antes de confirmar usando la dispersión del piloto. No se amplió al mirar resultados. Esta es confirmación en semillas disjuntas, con rivales parcialmente compartidos; no es validación externa del ladder.", "",
        "## Todos los candidatos del piloto", "",
        "Cuatro semillas 214000–214003, 16 rivales y ambos asientos: 128 episodios por brazo, 1.792 en total. La selección usa W/L/T agregado y desempate alfabético, fijados antes de correr. No se eligió por dinero ni por el intervalo más favorable.", "",
        "| Brazo | W/L/T | Delta vs HOZ | Históricos (8) | Nuevos (8) |",
        "|---|---:|---:|---:|---:|"]
    for arm, r in sorted(pilot["summary"].items(), key=lambda item: (-item[1]["score"], item[0])):
        lines.append(f"| `{arm}` | {r['score']:.2%} | {100*r['delta']['mean']:+.2f} | {r['strata']['lad_']:.2%} | {r['strata']['sepopp_']:.2%} |")
    lines += ["", "La cinta 107674293, el árbol y el árbol con ventas empataron en 64,06%. Confirmar la cinta cumple el desempate, pero no demuestra que supere al árbol. Las ventas reactivas cambiaron las acciones en los 128 episodios y no cambiaron W/L/T frente al árbol en ninguno: ejecución sin mejora observada. La apertura seguida de HOZ quedó en +6,25 puntos exploratorios.", "",
        "El piloto pondera 50% rivales históricos y 50% nuevos; la confirmación pondera 40/48 y 8/48. Esa diferencia estaba registrada, pero puede cambiar qué arquitectura destaca. No reinterpretar los estratos después para rescatar un candidato.", "",
        "Limitación de la variante de ventas: el proyector asume tablero 10×10 y shed de 100 unidades y no modela el caso en que PLACE de un animal cae al shed. No es un simulador general exacto. El bloque terminado mide esta implementación concreta; corregirla requiere otra variante y otro registro, no cambiar el código de una corrida. El candidato seleccionado no usa ese proyector.", "",
        "## Diagnósticos posteriores, sin selección", "",
        "Contra las ocho cintas de Majkel: ocho semillas 216000–216007, ambos asientos, cuatro brazos, 512 episodios. Son fuentes usadas para construir candidatos, no rivales reservados. Una cinta no responde como el agente original.", "",
        "| Brazo | W/L/T | Delta vs HOZ | IC95 por semilla |",
        "|---|---:|---:|---:|"]
    for arm in ("base", "noop", "_peor", candidate):
        r = stress["summary"][arm]
        lines.append(f"| `{arm}` | {r['score']:.2%} | {100*r['delta']['mean']:+.2f} | {interval(r['delta']['seed_ci95'])} |")
    lines += ["", "En este estrés, el intervalo del control FB cruza cero: el bloque no demuestra discriminación entre FB y HOZ. Su ventaja observada para el candidato se conserva como diagnóstico; no satisface por sí sola el protocolo de confirmación ni prueba que gane al líder reactivo.", "",
        f"Contra HOZ vivo: **{duel['wins']} victorias, {duel['losses']} derrotas y {duel['ties']} empates**, W/L/T {duel['score']:.2%}, en 16 partidas (ocho semillas 217000–217007, ambos asientos). IC95 t por semilla del score: {interval(duel['seed_ci95'])} puntos. Es un diagnóstico pequeño; este intervalo aproximado no está restringido al rango [0,100].", "",
        "## Integridad y límites", "",
        "Los tres paneles completos tienen cobertura cartesiana, cero episodios inválidos y noop exacto en acciones emitidas, rewards, estados de finalización, pasos y llamadas. Los hashes de acciones se capturan antes del motor. Se archivaron fuentes y protocolo antes de cada bloque y se comprobaron hashes de motor y cintas al finalizar. Los paneles conservan hashes, no todos los estados intermedios; la comparación explícita de 720 estados completos corresponde a las ocho reproducciones originales.", "",
        "`verificar_lider.py` vuelve a comprobar registros comprimidos, cobertura, controles y fuentes archivadas, y reconstruye los resúmenes con la función estadística del evaluador. No constituye una segunda implementación independiente de los intervalos.", "",
        "Coste: 1.792 piloto + 7.296 confirmación + 512 estrés + 16 duelo + 18 reproducciones/sondas = **9.634 episodios locales**. No consumen envíos de Kaggle. Los tiempos de decisión registrados son locales, no una prueba del paquete en el runtime de Kaggle.", "",
        "No se verificó Elo, rank actual ni el comportamiento reactivo del líder. Los ocho replays son victorias seleccionadas. Tres de sus rivales comparten un prefijo de 120 acciones: agrupar por nombre no garantiza independencia de estrategias. Un buen resultado local contra cintas no garantiza transferencia a oponentes nuevos o adaptativos.", "",
        "## Qué probar después", "",
        "1. **Reservar familias de rivales nuevas antes de desarrollar.** La principal incertidumbre es transporte, no optimizar décimas en este panel. Propuesta: ocho familias no usadas, 16 semillas y ambos asientos, cuatro brazos = 1.024 episodios; fijar identidades, hashes y regla de decisión antes del primer resultado. Si no hay familias nuevas verificables, no llamar a la prueba holdout de rivales.",
        "2. **Aprender las ramas del árbol con información visible.** El árbol actual usa una regla manual de tiendas. Comparar cinta seleccionada, árbol congelado y router aprendido con partición por familias y semillas; no elegir tiendas o pesos mirando confirmación. Primero definir dataset y presupuesto, luego evaluar.",
        "3. **Reparar compromisos de la ruta, no sólo vender más.** La capa de ventas no aportó victorias en el piloto. Una reparación útil debe registrar compras ejecutadas, inventario y cohortes para evitar que una acción fallida rompa el calendario. Comenzar con diagnóstico de 16 partidas preseleccionadas; sin evidencia de ese mecanismo, parar antes de un barrido.", "",
        "La idea de rutas y ligas tiene precedentes públicos: el autor de [Three Day Shop Router](https://www.kaggle.com/code/yhay81/three-day-shop-router/comments) describe copias simplificadas de rutas públicas y evaluación en muchas semillas. Es un reporte del autor; no descargamos su implementación ni verificamos su velocidad anunciada. Esta ronda construye y mide nuestras propias variantes.", "",
        "## Reproducir y revisar con otro LLM", "",
        "```bash\n./.venv/bin/python verificar_lider.py\n./.venv/bin/python preparar_contexto_llm.py\n./.venv/bin/python preparar_contexto_llm.py --check\n```", "",
        "Entrada experimental de la cinta: `bots.meta.tape.make('maj_107674293')`. Las variantes nuevas están en `bots/experimentos_lider.py`. Los evaluadores rechazan sobrescribir una corrida existente: para repetirla usar una copia del repo y conservar los originales. No ejecutar `submission/main.py` ni empaquetar por interpretar este informe como autorización de envío.", ""]
    (ROOT / "docs/RESULTADOS_LIDER_2026-09-14.md").write_text("\n".join(lines))
    (OUT / "decision.json").write_text(json.dumps(dict(candidate=candidate, local_jump_confirmed=passed,
        candidate_both_ci_positive=positive, control_both_ci_negative=negative_control,
        delta=effect["mean"], kaggle_submitted=False), indent=2) + "\n")
    print(verdict)


if __name__ == "__main__":
    main()
