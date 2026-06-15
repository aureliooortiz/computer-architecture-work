#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define N (64 * 1024 * 1024) // 64 milhões de ints (~256 MB)

volatile long long soma = 0;

int main(int argc, char *argv[]) {

    if (argc != 2) {
        fprintf(stderr, "Uso: %s <stride>\n", argv[0]);
        return 1;
    }

    int stride = atoi(argv[1]);

    int *vetor = malloc(N * sizeof(int));

    if (!vetor) {
        perror("malloc");
        return 1;
    }

    for (size_t i = 0; i < N; i++)
        vetor[i] = i;

    long long acessos_desejados = 1000000000LL; // 1 bilhão

    long long acessos_por_passada = N / stride;

    long long repeticoes = acessos_desejados / acessos_por_passada;

    if (repeticoes < 1)
        repeticoes = 1;

    for (long long r = 0; r < repeticoes; r++) {
        for (size_t i = 0; i < N; i += stride) {
            soma += vetor[i];
        }
    }

    printf("stride=%d repeticoes=%lld soma=%lld\n",
           stride, repeticoes, soma);

    free(vetor);

    return 0;
}