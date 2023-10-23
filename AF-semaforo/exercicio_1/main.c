#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>
#include <time.h>
#include <stdlib.h>

FILE* out;

<<<<<<< HEAD
sem_t semA, semB;


=======
sem_t semaphore_a, semaphore_b;
>>>>>>> origin/main

void *thread_a(void *args) {
    for (int i = 0; i < *(int*)args; ++i) {
	//      +---> arquivo (FILE*) destino
	//      |    +---> string a ser impressa
	//      v    v
<<<<<<< HEAD
		sem_wait(&semA);
        fprintf(out, "A");
        sem_post(&semB);
=======
        sem_wait(&semaphore_a);
        fprintf(out, "A");
        sem_post(&semaphore_b);
>>>>>>> origin/main
        // Importante para que vocês vejam o progresso do programa
        // mesmo que o programa trave em um sem_wait().
        fflush(stdout);
    }
    return NULL;
}

void *thread_b(void *args) {
    for (int i = 0; i < *(int*)args; ++i) {
<<<<<<< HEAD
    	sem_wait(&semB);
        fprintf(out, "B");
        sem_post(&semA);
=======
        sem_wait(&semaphore_b);
        fprintf(out, "B");
        sem_post(&semaphore_a);
>>>>>>> origin/main
        fflush(stdout);
    }
    return NULL;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        printf("Uso: %s [ITERAÇÕES]\n", argv[0]);
        return 1;
    }
    int iters = atoi(argv[1]);
    srand(time(NULL));
    out = fopen("result.txt", "w");

    pthread_t ta, tb;
<<<<<<< HEAD
    
    sem_init(&semA, 0, 1);
    sem_init(&semB, 0, 1);
=======

    sem_init(&semaphore_a, 0, 1);
    sem_init(&semaphore_b, 0, 1);
>>>>>>> origin/main

    // Cria threads
    pthread_create(&ta, NULL, thread_a, &iters);
    pthread_create(&tb, NULL, thread_b, &iters);

    // Espera pelas threads
    pthread_join(ta, NULL);
    pthread_join(tb, NULL);
<<<<<<< HEAD
    
    sem_destroy(&semA);
    sem_destroy(&semB);
=======

    sem_destroy(&semaphore_a);
    sem_destroy(&semaphore_b);
>>>>>>> origin/main

    //Imprime quebra de linha e fecha arquivo
    fprintf(out, "\n");
    fclose(out);
  
    return 0;
}
