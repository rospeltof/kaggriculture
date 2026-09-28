#!/bin/zsh
# Cola 28-sep (c): criba de capas nuevas y confirmacion XC. Ejecutar con nohup.
cd /Users/rospel/Desktop/kaggriculture
P=.venv/bin/python
R="tds27=results/publicos_0927/tetsutani/main.py cha22=submission/main_publico_cha22.py"
test -e results/criba_b.jsonl || nice -n 15 $P torneo.py --out results/criba_b --seeds 3 --seed0 4830000 --workers 11 --sin-cruces --vs final,s738w,s738f,s738wf,ml8,ml10,bf144,bf24 final=submission/main_publico_final_frps.py s738w=results/exp_0928b/s738w.py s738f=results/exp_0928b/s738f.py s738wf=results/exp_0928b/s738wf.py ml8=results/exp_0928b/ml8.py ml10=results/exp_0928b/ml10.py bf144=results/exp_0928b/bf144.py bf24=results/exp_0928b/bf24.py hl0928=results/exp_0928b/rival_hl0928.py ${=R} > results/criba_b.txt 2>&1
touch results/criba_b.done
test -e results/torneo_xc2.jsonl || nice -n 15 $P torneo.py --out results/torneo_xc2 --seeds 48 --seed0 4820000 --workers 11 --sin-cruces --vs ref,xc1,xcs ref=submission/main_publico_final_frps.py xc1=results/exp_0928b/xc1.py xcs=results/exp_0928b/xcs.py ${=R} hl836=results/publicos_0927c/haodou092_kaggriculture-harvest-ledger/main.py top3cc=submission/main_publico_top3cc.py hl74=results/publicos_0926/haodou092_kaggriculture-harvest-ledger/main.py > results/torneo_xc2.txt 2>&1
touch results/torneo_xc2.done
