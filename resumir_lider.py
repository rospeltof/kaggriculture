"""Genera gráfico y análisis descriptivo de replays ya auditados. Cero partidas."""
from collections import Counter
import json
from pathlib import Path
import statistics

ROOT=Path(__file__).resolve().parent
EVIDENCE=ROOT/"docs/evidencia/lider_20260914"


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    data=json.loads((EVIDENCE/"replays.json").read_text())
    validation={r["episode"]:r for r in json.loads((EVIDENCE/"validacion.json").read_text())}
    rows=data["episodes"]
    labels=[r["teams"][1-r["leader_seat"]].replace(" ","\n",1) for r in rows]
    x=np.arange(len(rows))
    fig,axes=plt.subplots(2,1,figsize=(13,9),constrained_layout=True)
    colors={"MILK":"#4c78a8","WOOL":"#aa74b6","STRAWBERRY":"#e45756","MELON":"#f2cf5b",
            "CARROT":"#f58518","WHEAT":"#b3a369","EGG":"#72b7b2","TOMATO":"#ff9da6","FERTILIZER":"#54a24b"}
    bottom=np.zeros(len(rows))
    for product,color in colors.items():
        values=np.array([validation[r["episode"]]["cashflows"][r["leader_seat"]].get("SELL:"+product,{}).get("cash",0)/1000 for r in rows])
        axes[0].bar(x,values,bottom=bottom,label=product,color=color,width=.7)
        bottom+=values
    net=[r["rewards"][r["leader_seat"]]/1000 for r in rows]
    axes[0].plot(x,net,"D",color="#222222",label="Dinero final",markersize=5)
    axes[0].set_ylabel("Miles de monedas")
    axes[0].set_title("Majkel1337: ingresos efectivos por producto y dinero final",loc="left",weight="bold")
    axes[0].set_xticks(x,labels,fontsize=8)
    axes[0].legend(loc="upper left",bbox_to_anchor=(1,1),frameon=False,fontsize=8)
    bottom=np.zeros(len(rows))
    for animal,color in (("COW","#4c78a8"),("SHEEP","#aa74b6"),("GOOSE","#72b7b2")):
        counts=np.array([r["player_summaries"][r["leader_seat"]]["snapshots"]["15"]["composition"].get(animal,0) for r in rows])
        axes[1].bar(x,counts,bottom=bottom,label=animal,color=color,width=.7)
        bottom+=counts
    axes[1].set_title("Composición del rebaño al amanecer del día 15",loc="left",weight="bold")
    axes[1].set_ylabel("Animales vivos")
    axes[1].set_xticks(x,labels,fontsize=8)
    axes[1].legend(loc="upper left",bbox_to_anchor=(1,1),frameon=False)
    for ax in axes:
        ax.spines[['top','right']].set_visible(False)
        ax.set_axisbelow(True);ax.grid(axis="y",alpha=.18)
    fig.suptitle("Ocho replays aportados · análisis 14 sep 2026\nRivales identificados por nombre; los archivos no incluyen Elo",fontsize=13)
    fig.savefig(EVIDENCE/"economias_lider.png",dpi=150)
    plt.close(fig)
    lines=["# Qué muestran los ocho replays de Majkel1337\n",
           "Análisis del 2026-09-14. [Experimentos y pre-registro](EXPERIMENTOS_ATREVIDOS_2026-09-14.md). "
           "[Evidencia](evidencia/lider_20260914/README.md). No se realizó ningún envío a Kaggle.\n",
           "## Qué está comprobado\n",
           "Se reprodujeron exactamente las ocho partidas, comparando 720 estados en cada una. "
           "Las ventas y compras se midieron al ejecutarse en el motor y los flujos concilian "
           "con el dinero final de ambos jugadores. Las cantidades siguientes son operaciones "
           "efectivas, no órdenes solicitadas.\n",
           "| Episodio | Rival | Dinero Majkel / rival | COW / SHEEP / GOOSE d15 | Mayor ingreso efectivo |",
           "|---|---|---:|---:|---:|"]
    for r in rows:
        p=r["leader_seat"];s=r["player_summaries"][p]
        c=s["snapshots"]["15"]["composition"]
        flow=validation[r["episode"]]["cashflows"][p]
        product,values=max(((k,v) for k,v in flow.items() if k.startswith("SELL:")),key=lambda kv:kv[1]["cash"])
        lines.append(f"| {r['episode']} | {r['teams'][1-p]} | {r['rewards'][p]:,.0f} / {r['rewards'][1-p]:,.0f} | "
                     f"{c.get('COW',0)} / {c.get('SHEEP',0)} / {c.get('GOOSE',0)} | {product[5:]}: {values['cash']:,.0f} |")
    lines += ["\n![Economías y rebaños](evidencia/lider_20260914/economias_lider.png)\n",
              "## Mecanismos que merecen una prueba\n",
              "1. **Apertura con compromisos coordinados.** Compra dos vacas y tres ovejas "
              "en los dos primeros turnos en las ocho partidas. Planta doce melones temprano, "
              "compra el segundo cuadrante en step 149 (d6 h5) y amplía el rebaño desde d6. "
              "No equivale a subir una perilla de animales en nuestra apertura actual.\n",
              "2. **Economías diferentes entre partidas.** En d15 tiene 13–22 animales; "
              "hay casos con 15 ovejas y otros con 14 vacas. La lana aporta 90.156 monedas "
              "contra goh y la leche 98.205 contra jps. Es compatible con adaptación a "
              "demanda/rival, pero ocho trazas no identifican su regla ni separan causalmente "
              "los efectos de tiendas y rivales.\n",
              "3. **Comprar forraje y vender trigo no se contradicen automáticamente.** "
              "Compra 174–389 unidades de trigo por partida, además de cosechar y vender "
              "290–680. La fecha, ubicación y caja son parte de la política. Un cambio global "
              "de BUY_FEED no reproduce esa secuencia.\n",
              "4. **Rutas compatibles permiten ramificar.** Cuatro cintas comparten sus primeras "
              "86 acciones completas. Dos de ellas comparten 145. Las tiendas aparecen desde "
              "d3, de modo que se puede decidir en ese punto usando información ya visible, "
              "sin cambiar el prefijo ejecutado ni consultar el futuro. Esto motivó el árbol probado.\n",
              "5. **El coste del trabajo también cambia.** Sus compras efectivas de peones "
              "cuestan entre 4.662 y 5.086 monedas por partida. Las órdenes PASS representan "
              "0,68–0,97% de las acciones emitidas de unidades; movimiento y acciones fallidas "
              "no se cuentan como PASS y no son necesariamente trabajo útil.\n",
              "## Lo que no podemos concluir\n",
              "- El Elo y rank no vienen en los JSON. El usuario identifica al líder; no se "
              "verificó el ranking actual mediante la página, cuyo contenido dinámico no se recuperó.\n",
              "- Los IDs y sus diferencias no bastan para afirmar evolución durante varios días. "
              "Tampoco un marcador alto identifica un rival de Elo bajo.\n",
              "- Son ocho victorias seleccionadas. No estiman win rate del líder ni representan "
              "toda la población. Tres rivales (xiao xiongwei, goh y Ryosei Hara) comparten "
              "sus primeras 120 acciones; ocho nombres no significan ocho estrategias independientes.\n",
              "- Reproducir una cinta con su semilla y rival originales prueba fidelidad de "
              "extracción. En escenarios nuevos, la cinta deja de representar las respuestas "
              "que elegiría el agente original.\n",
              "## Errores de las conclusiones anteriores que estos datos obligan a revisar\n",
              "La réplica de lotes con +0,23 e IC95 aproximadamente [−6,2; +6,7] no prueba "
              "un efecto exactamente nulo: no confirma la mejora. Tampoco una diferencia "
              "aislada de ratings demuestra que toda diferencia menor de 50 sea informativamente "
              "nula. El supuesto techo de la apertura se midió alterando capital de un planner "
              "concreto; no acota el valor de cambiar su calendario completo, geometría y logística. "
              "Conservamos esas notas como historia, no como motivos para prohibir estas pruebas.\n",
              "Para decisiones competitivas se usarán los bloques preregistrados y sus controles, "
              "no los ingresos de esta tabla. Ver [resultados y diagnósticos completos]"
              "(RESULTADOS_LIDER_2026-09-14.md).\n"]
    (ROOT/"docs/ANALISIS_LIDER_2026-09-14.md").write_text("\n".join(lines))
    print("Análisis descriptivo y gráfico generados, sin simulaciones.")


if __name__=="__main__":
    main()
