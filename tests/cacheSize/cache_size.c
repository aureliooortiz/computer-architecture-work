#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

volatile long long soma = 0;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        fprintf(stderr, "Uso: %s <tamanho_em_KB>\n", argv[0]);
        return 1;
    }

    size_t kb = atol(argv[1]);

    size_t bytes = kb * 1024;
    size_t n = bytes / sizeof(int);

    int *vetor = malloc(n * sizeof(int));

    if (!vetor)
    {
        perror("malloc");
        return 1;
    }

    for (size_t i = 0; i < n; i++)
        vetor[i] = i;

    const size_t repeticoes = 10000;

    for (size_t r = 0; r < repeticoes; r++)
    {
        for (size_t i = 0; i < n; i += 16)
        {
            soma += vetor[i];
        }
    }

    printf("KB=%zu soma=%lld\n", kb, soma);

    free(vetor);

    return 0;
}