#!/bin/bash

inicio=$(date +%s.%N)

echo "kb,loads,misses,miss_rate,time" > resultados.csv

for kb in \
4 8 16 32 64 128 256 512 \
1024 2048 4096 8192 \
16384 32768 
do

    echo "Testando ${kb}KB"

    output=$(sudo perf stat \
        -e L1-dcache-loads,L1-dcache-load-misses \
        ./cache_size $kb 2>&1)

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

    missrate=$(LC_NUMERIC=C awk \
        -v l="$loads" \
        -v m="$misses" \
        'BEGIN { printf "%.6f", m/l }')

    echo "$kb,$loads,$misses,$missrate,$time" \
        >> resultados.csv

    echo "feito ($time s)"
done

python3 detectar_regiao.py

echo "kb,loads,misses,miss_rate,time" > resultados_finos.csv

while read kb
do

    echo "Refinando ${kb}KB"

    output=$(sudo perf stat \
        -e L1-dcache-loads,L1-dcache-load-misses \
        ./cache_size $kb 2>&1)

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

    missrate=$(LC_NUMERIC=C awk \
        -v l="$loads" \
        -v m="$misses" \
        'BEGIN { printf "%.6f", m/l }')

    echo "$kb,$loads,$misses,$missrate,$time" \
        >> resultados_finos.csv

done < regioes.txt


fim=$(date +%s.%N)

tempo_total=$(awk \
    -v i="$inicio" \
    -v f="$fim" \
    'BEGIN { printf "%.2f", f-i }')

echo
echo "Tempo total: $tempo_total segundos"

python3 graficos_cache.py 