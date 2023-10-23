#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>
#include <time.h>

sem_t orderSemaphore;
pthread_mutex_t orderMutex;

int numClients;
int numWaiters;
int clientsPerWaiter;
int maxTalk;
int maxConsumeTime;
int maxRounds;
int currentRound = 0;
int* orders;

void* clientThread(void* clientID) {
    int id  = *(int*)clientID;

    while (currentRound < maxRounds) {
        // Random Talk Time
        int talkTime = rand() % maxTalk;
        usleep(talkTime * 1000);
        
    }
}

void* waiterThread(void* args) {
    return NULL;
}

int main(int argc, char* argv[]) {
    if (argc != 7) {
        printf("Siga o padrão: %s <clientes> <garcons> <clientes/garcon> <rodadas> <max.conversa> <max.consumo>\n", argv[0]);
        return 1;
    }

    numClients = atoi(argv[1]);
    numWaiters = atoi(argv[2]);
    clientsPerWaiter = atoi(argv[3]);
    maxRounds = atoi(argv[4]);
    maxTalk = atoi(argv[5]);
    maxConsumeTime = atoi(argv[6]);

    orders = (int*)calloc(numClients, sizeof(int));

    pthread_t clients[numClients];
    pthread_t waiters[numWaiters];

    srand(time(NULL));

    sem_init(&orderSemaphore, 0, 0);
    pthread_mutex_init(&orderMutex, NULL);

    // Create clients threads
    for (int i = 0; i < numClients; i++) {
        int* clientID = (int*)malloc(sizeof(int));
        *clientID = i;
        pthread_create(&clients[i], NULL, clientThread, clientID);
    }

    // Create waiters threads
    for (int i = 0; i < numWaiters; i++) {
        pthread_create(&waiters[i], NULL, waiterThread, NULL);
    }

    // Join client threads
    for (int i = 0; i < numClients; i++) {
        pthread_join(clients[i], NULL);
    }

    // Join waiters threads
    for (int i = 0; i < numWaiters; i++) {
        pthread_join(waiters[i], NULL);
    }

    // Destroy semaphore and mutex
    sem_destroy(&orderSemaphore);
    pthread_mutex_destroy(&orderMutex);

    free(orders);

    return 0;
}
