#!/bin/bash

echo "stride,loads,misses,miss_rate,time" > resultados_gerais.csv

# Varredura grosseira
for s in 1 2 4 8 16 32 64 128
do
    echo "Teste geral stride=$s"

    output=$(sudo perf stat -e L1-dcache-loads,L1-dcache-load-misses ./stride $s 2>&1)

    loads=$(echo "$output" |
        grep "cpu_core/L1-dcache-loads/" |
        awk '{print $1}' |
        tr -d '.')

    misses=$(echo "$output" |
        grep "cpu_core/L1-dcache-load-misses/" |
        awk '{print $1}' |
        tr -d '.')

    time=$(echo "$output" |
        grep "seconds time elapsed" |
        awk '{print $1}' |
        tr ',' '.')

    missrate=$(LC_NUMERIC=C awk -v l="$loads" -v m="$misses" \
        'BEGIN { printf "%.6f", m/l }')

    echo "$s,$loads,$misses,$missrate,$time" >> resultados_gerais.csv
done

# Descobrir região para refinar
python3 detectar_regiao.py

read inicio fim < regiao.txt

echo "stride,loads,misses,miss_rate,time" > resultados_finos.csv

for ((s=inicio; s<=fim; s += 4))
do
    echo "Teste fino stride=$s"

    output=$(sudo perf stat -e L1-dcache-loads,L1-dcache-load-misses ./stride $s 2>&1)

    loads=$(echo "$output" |
        grep "cpu_core/L1-dcache-loads/" |
        awk '{print $1}' |
        tr -d '.')

    misses=$(echo "$output" |
        grep "cpu_core/L1-dcache-load-misses/" |
        awk '{print $1}' |
        tr -d '.')

    time=$(echo "$output" |
        grep "seconds time elapsed" |
        awk '{print $1}' |
        tr ',' '.')

    missrate=$(LC_NUMERIC=C awk -v l="$loads" -v m="$misses" \
        'BEGIN { printf "%.6f", m/l }')

    echo "$s,$loads,$misses,$missrate,$time" >> resultados_finos.csv
done

python3 grafico.py