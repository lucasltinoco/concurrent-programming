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

// Avalia se o prod_escalar é o produto escalar dos vetores a e b. Assume-se
// que ambos a e b sejam vetores de tamanho size.
void avaliar(double *a, double *b, int size, double prod_escalar);

// Estrutura que representa um chunk de um vetor
typedef struct chunk
{
    double *a;
    double *b;
    int start;
    int end;
} prod_chunk;

// Função que será executada por cada thread. Calcula o produto de dois vetores em um chunk
void *chunk_product(void *arg)
{
    prod_chunk chunk = *((prod_chunk *)arg);
    double *chunk_result = malloc(sizeof(double));
    *chunk_result = 0;

    for (size_t i = chunk.start; i < chunk.end; i++)
        *chunk_result += chunk.a[i] * chunk.b[i];

    return chunk_result;
}

int main(int argc, char *argv[])
{
    srand(time(NULL));

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

    // Previne mais threads que o necessário
    if (n_threads > a_size)
        n_threads = a_size;

    // Cria array de instâncias de pthread_t
    pthread_t threads[n_threads];
    // Divide partes do vetor para as threads
    int chunk_size = a_size / n_threads;
    prod_chunk chunks[n_threads];

    // Cria as threads e passa as partes do vetor (chunks) como argumento para cada uma delas
    for (int i = 0; i < n_threads; ++i)
    {
        chunks[i].a = a;
        chunks[i].b = b;
        chunks[i].start = i * chunk_size;
        chunks[i].end = (i == n_threads - 1) ? a_size : chunks[i].start + chunk_size;

        pthread_create(&threads[i], NULL, chunk_product, (void *)&chunks[i]);
    }

    // Espera as threads terminarem e pega o resultado de cada uma
    double *result_array[n_threads];
    for (int i = 0; i < n_threads; ++i)
    {
        pthread_join(threads[i], (void **)&result_array[i]);
    }

    // Soma os resultados de cada thread
    double result = 0;
    for (int i = 0; i < n_threads; ++i)
    {
        result += *result_array[i];
        free(result_array[i]);
    }

    //    +---------------------------------+
    // ** | IMPORTANTE: avalia o resultado! | **
    //    +---------------------------------+
    avaliar(a, b, a_size, result);

    // Libera memória
    free(a);
    free(b);

    return 0;
}
