#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdio.h>
#include <pthread.h>

// Lê o conteúdo do arquivo filename e retorna um vetor E o tamanho dele
// Se filename for da forma "gen:%d", gera um vetor aleatório com %d elementos
//
// +-------> retorno da função, ponteiro para vetor malloc()ado e preenchido
// |
// |         tamanho do vetor (usado <-----+
// |         como 2o retorno)              |
// v                                       v
double *load_vector(const char *filename, int *out_size);

// Avalia o resultado no vetor c. Assume-se que todos os ponteiros (a, b, e c)
// tenham tamanho size.
void avaliar(double *a, double *b, double *c, int size);

// Estrutura que representa um chunk de um vetor
typedef struct chunk
{
    double *a;
    double *b;
    double *c;
    int start;
    int end;
} sum_chunk;

// Função que será executada por cada thread. Calcula a soma de dois vetores em um chunk
void *chunk_sum(void *arg)
{
    sum_chunk chunk = *((sum_chunk *)arg);

    for (size_t i = chunk.start; i < chunk.end; i++)
        chunk.c[i] = chunk.a[i] + chunk.b[i];

    pthread_exit(NULL);
}

int main(int argc, char *argv[])
{
    // Gera um resultado diferente a cada execução do programa
    // Se **para fins de teste** quiser gerar sempre o mesmo valor
    // descomente o srand(0)
    srand(time(NULL)); // valores diferentes
    // srand(0);        //sempre mesmo valor

    // Temos argumentos suficientes?
    if (argc < 4)
    {
        printf("Uso: %s n_threads a_file b_file\n"
               "    n_threads    número de threads a serem usadas na computação\n"
               "    *_file       caminho de arquivo ou uma expressão com a forma gen:N,\n"
               "                 representando um vetor aleatório de tamanho N\n",
               argv[0]);
        return 1;
    }

    // Quantas threads?
    int n_threads = atoi(argv[1]);
    if (!n_threads)
    {
        printf("Número de threads deve ser > 0\n");
        return 1;
    }
    // Lê números de arquivos para vetores alocados com malloc
    int a_size = 0, b_size = 0;
    double *a = load_vector(argv[2], &a_size);
    if (!a)
    {
        // load_vector não conseguiu abrir o arquivo
        printf("Erro ao ler arquivo %s\n", argv[2]);
        return 1;
    }
    double *b = load_vector(argv[3], &b_size);
    if (!b)
    {
        printf("Erro ao ler arquivo %s\n", argv[3]);
        return 1;
    }

    // Garante que entradas são compatíveis
    if (a_size != b_size)
    {
        printf("Vetores a e b tem tamanhos diferentes! (%d != %d)\n", a_size, b_size);
        return 1;
    }
    // Cria vetor do resultado
    double *c = malloc(a_size * sizeof(double));

    // Previne mais threads que o necessário
    if (n_threads > a_size)
        n_threads = a_size;

    // Cria array de instâncias de pthread_t
    pthread_t threads[n_threads];
    // Divide partes do vetor para as threads
    int chunk_size = a_size / n_threads;
    sum_chunk chunks[n_threads];

    // Cria as threads e passa as partes do vetor (chunks) como argumento para cada uma delas
    for (int i = 0; i < n_threads; ++i)
    {
        chunks[i].a = a;
        chunks[i].b = b;
        chunks[i].c = c;
        chunks[i].start = i * chunk_size;
        chunks[i].end = (i == n_threads - 1) ? a_size : chunks[i].start + chunk_size;

        pthread_create(&threads[i], NULL, chunk_sum, (void *)&chunks[i]);
    }

    // Espera as threads terminarem
    for (int i = 0; i < n_threads; ++i)
        pthread_join(threads[i], NULL);

    //    +---------------------------------+
    // ** | IMPORTANTE: avalia o resultado! | **
    //    +---------------------------------+
    avaliar(a, b, c, a_size);

    // Importante: libera memória
    free(a);
    free(b);
    free(c);

    return 0;
}
