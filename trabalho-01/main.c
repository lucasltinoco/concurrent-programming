#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

#define MAX_CUSTOMERS 1000
#define MAX_WAITERS 100
#define MAX_ROUNDS 100
#define BASE_TIME 100000

// Estrutura para representar um pedido de cliente
typedef struct
{
  int customer_id;
  int round;
} Order;

// Variáveis globais
int round_orders;
int waiter_orders[MAX_WAITERS] = {0}; // Número de pedidos de cada garçom
int waiter_is_serving[MAX_WAITERS] = {false};
int rounds = 0; // Contador de rodadas

int num_customers, num_waiters, max_customers_per_waiter, max_rounds, max_converse_time, max_consume_time;

int count_order = 0;

// Semáforos
sem_t waiter_orders_sem[MAX_WAITERS];
sem_t waiter_serving_sem[MAX_WAITERS];
sem_t rounds_sem;
sem_t round_orders_sem;
sem_t consume_sem;

// Função para simular o tempo de conversa e consumo
void simulate_time(int max_time)
{
  // TODO: Checar se os max tempos estão sendo considerados
  usleep(BASE_TIME + (rand() % (max_time * 1000)));
}

// Função para que o cliente converse com amigos
void converse_with_friends(int customer_id) 
{
  printf("-- Cliente %d conversando com amigos (Rodada %d).\n", customer_id, rounds);
  fflush(stdout);
  simulate_time(max_converse_time);
}

// Função para que o cliente faça um pedido
int make_order(Order order)
{
  int waiter_id = rand() % num_waiters;
  sem_wait(&waiter_orders_sem[waiter_id]);
  while (waiter_orders[waiter_id] >= max_customers_per_waiter || waiter_is_serving[waiter_id])
  {
    sem_post(&waiter_orders_sem[waiter_id]);
    waiter_id = rand() % num_waiters;
    sem_wait(&waiter_orders_sem[waiter_id]);
  }
  // Pedido #n_cliente-n_garçom (e.g #8-2)
  printf("-- Cliente %d fez um pedido para Garçom %d (Pedido #%d-%d, Rodada %d).\n", order.customer_id, waiter_id, order.customer_id, waiter_id, rounds);
  fflush(stdout);
  waiter_orders[waiter_id]++;
  sem_post(&waiter_orders_sem[waiter_id]);
  return waiter_id;
}

// Função para que o cliente aguarde seu pedido
void wait_for_order(Order order, int waiter_id)
{
  sem_wait(&waiter_serving_sem[waiter_id]);
}

// Função para que o cliente consuma seu pedido
void consume_order(int customer_id)
{
  printf("-- Cliente %d consumindo pedido (Rodada %d).\n", customer_id, rounds);
  fflush(stdout);
  simulate_time(max_consume_time);
}

// Função para simular o cliente
void *customer(void *customer_id)
{
  int id = *(int *)customer_id;
  while (rounds < max_rounds)
  {
    bool customer_wants_a_drink = rand() % 100 < 75;
    converse_with_friends(id);
    if (customer_wants_a_drink)
    {
      Order order = {id, rounds};
      count_order +=1;
      int waiter_id = make_order(order);
      wait_for_order(order, waiter_id);
      consume_order(id);
    }
    else
    {
      printf("-- Cliente %d não quer beber (Rodada %d).\n", id, rounds);
      fflush(stdout);
      sem_wait(&round_orders_sem);
      round_orders--;
      sem_post(&round_orders_sem);
    }
    sem_post(&consume_sem);
    sem_wait(&rounds_sem);
  }
  return NULL;
}

void report() {
  printf("\n--------- Informações ---------\n");
  printf("Nº Clientes: %d\nNº Garçons: %d\nClientes/Garçom: %d\nRounds: %d\nMax. Conversa: %d\nMax. Consumo: %d\n\nTotal de Pedidos: %d", num_customers, num_waiters, max_customers_per_waiter, max_rounds, max_converse_time, max_consume_time, count_order);
}

// Função para simular o garçom
void *waiter(void *waiter_id)
{
  int id = *(int *)waiter_id;
  while (rounds < max_rounds)
  {
    int count_orders_with_waiters = 0;
    for (int i = 0; i < num_waiters; i++)
    {
      sem_wait(&waiter_orders_sem[i]);
      count_orders_with_waiters += waiter_orders[i];
      sem_post(&waiter_orders_sem[i]);
    }

    // Garçom espera até que todos os clientes tenham feito pedidos
    if (waiter_orders[id] > 0 && (waiter_orders[id] == max_customers_per_waiter || (waiter_orders[id] < max_customers_per_waiter && round_orders == count_orders_with_waiters)))
    {
      waiter_is_serving[id] = true;
      printf("-- Garçom %d indo buscar pedidos na copa (Rodada %d).\n", id, rounds);
      fflush(stdout);
      simulate_time(max_rounds);
      printf("-- Garçom %d entregando pedidos (Rodada %d).\n", id, rounds);
      fflush(stdout);
      simulate_time(max_rounds);
      for (int i = 0; i < waiter_orders[id]; i++)
      {
        sem_post(&waiter_serving_sem[id]);
      }

      sem_wait(&round_orders_sem);
      round_orders -= waiter_orders[id];
      waiter_is_serving[id] = false;
      waiter_orders[id] = 0;
      if (round_orders == 0)
      {
        round_orders = num_customers;
        for (int i = 0; i < num_customers; i++)
        {
          sem_wait(&consume_sem);
        }
        rounds++;
        for (int i = 0; i < num_customers; i++)
        {
          sem_post(&rounds_sem);
        }
      }
      sem_post(&round_orders_sem);
    }
  }
  return NULL;
}

int main(int argc, char *argv[])
{
  if (argc != 7)
  {
    printf("-- Uso: %s <clientes> <garcons> <clientes/garcon> <rodadas> <max.conversa> <max.consumo>\n", argv[0]);
    return 1;
  }

  num_customers = atoi(argv[1]);
  num_waiters = atoi(argv[2]);
  max_customers_per_waiter = atoi(argv[3]);
  max_rounds = atoi(argv[4]);
  max_converse_time = atoi(argv[5]);
  max_consume_time = atoi(argv[6]);

  round_orders = num_customers;

  srand(time(NULL));

  printf("\n\n----------- Bar Iniciado -----------\n\n");

  // Inicialização dos semáforos
  sem_init(&round_orders_sem, 0, 1);
  sem_init(&rounds_sem, 0, 0);
  sem_init(&consume_sem, 0, 0);
  for (int i = 0; i < MAX_WAITERS; i++)
  {
    sem_init(&waiter_orders_sem[i], 0, 1);
    sem_init(&waiter_serving_sem[i], 0, 0);
  }

  // Criação de threads para os garçons
  pthread_t waiter_threads[num_waiters];
  int waiter_ids[num_waiters];
  for (int i = 0; i < num_waiters; i++)
  {
    waiter_ids[i] = i;
    pthread_create(&waiter_threads[i], NULL, waiter, &waiter_ids[i]);
  }

  // Criação de threads para os clientes
  pthread_t customer_threads[num_customers];
  int customer_ids[num_customers];
  for (int i = 0; i < num_customers; i++)
  {
    customer_ids[i] = i;
    pthread_create(&customer_threads[i], NULL, customer, &customer_ids[i]);
  }

  // Aguarda a conclusão das threads dos clientes
  for (int i = 0; i < num_customers; i++)
  {
    pthread_join(customer_threads[i], NULL);
  }

  // Aguarda a conclusão das threads dos garçons
  for (int i = 0; i < num_waiters; i++)
  {
    pthread_join(waiter_threads[i], NULL);
  }

  report();

  printf("\n\n----- Bar Finalizado -----\n");

  return 0;
}
