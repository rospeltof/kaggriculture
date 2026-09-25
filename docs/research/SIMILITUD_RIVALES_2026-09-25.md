# Similitud observada y siguiente prueba contra políticas cercanas

Auditoría descriptiva de los 15 replays únicos ya seleccionados por recencia
en los cortes 06:53 y 07:42 UTC. No se agregaron partidas ni se filtraron por
resultado. Se verificó el hash de cada replay; sus fuentes propias habían
reproducido las 719 acciones y 720 estados en las auditorías anteriores.

Por turno se compara el vector de órdenes del granjero y peones, sin mercado.
La mediana por partida de coincidencia del vector completo es **99,17%**;
la coincidencia de órdenes de mercado en turnos con al menos un mercado activo
tiene mediana **71,27%**. Son medianas de 15 partidas, no porcentajes de toda
la población del ladder ni estimaciones de fuerza.

| Rival | Vector completo de campo igual | Mercado activo igual | Turnos con igual número de actores |
|---|---:|---:|---:|
| Duvor Richard | 98,05% | 71,27% | 719 |
| hisatarosu | 100,00% | 86,25% | 719 |
| daviondk | 89,29% | 74,77% | 718 |
| kyosan | 96,11% | 57,78% | 719 |
| minghao mei | 99,86% | 63,06% | 719 |
| ZeroGrain | 70,38% | 66,37% | 508 |
| Mao Nishino | 99,44% | 67,35% | 719 |
| dauriel | 98,75% | 71,85% | 719 |
| Abhinav0370 | 96,80% | 67,44% | 718 |
| Fateyongheng | 45,20% | 55,51% | 444 |
| dijia zhang735 | 99,86% | 82,34% | 719 |
| Gemini IS ALL YOU NEED | 99,72% | 78,24% | 719 |
| Grim Reaper | 99,17% | 61,36% | 719 |
| 老乡 | 99,86% | 82,62% | 719 |
| Panagiotis Anagnostou | 100,00% | 84,11% | 719 |

El porcentaje de comandos individuales emparejados por índice tiene mediana
99,91%, pero omite los actores sin pareja. Por eso el vector completo y la
cantidad de actores son necesarios: Fateyongheng y ZeroGrain muestran la
limitación con claridad. Tampoco se igualan posiciones, estados ni efectos
aceptados por el motor. Una orden idéntica puede tener consecuencias distintas.
Nada de esto identifica código privado, cuenta familias independientes o
atribuye causalmente el resultado al mercado.

La señal justifica una pregunta nueva: ¿se conservan las ventajas al enfrentar
políticas reactivas tan cercanas como VQ y top3, además de fuentes públicas
recientes? Los paneles 19–24 permanecen congelados. Se registrará un bloque
separado con referencias y candidatas fijadas antes de sus partidas, semillas
nuevas y confirmación disjunta. No se usarán estas cintas como rivales pasivos
ni se cambiarán retrospectivamente los gates de los experimentos anteriores.

Reproducción: `auditar_similitud_rivales.py`; evidencia
`recent_rival_similarity.plan.json` y `recent_rival_similarity.json` en
`docs/evidencia/loop_publicos_20260925/`. Los replays originales están
archivados en los paquetes de feedback 0653 y 0742.
