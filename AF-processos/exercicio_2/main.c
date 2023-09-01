#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <stdio.h>
//                          (principal)
//                               |
//              +----------------+--------------+
//              |                               |
//           filho_1                         filho_2
//              |                               |
//    +---------+-----------+          +--------+--------+
//    |         |           |          |        |        |
// neto_1_1  neto_1_2  neto_1_3     neto_2_1 neto_2_2 neto_2_3

// ~~~ printfs  ~~~
//      principal (ao finalizar): "Processo principal %d finalizado\n"
// filhos e netos (ao finalizar): "Processo %d finalizado\n"
//    filhos e netos (ao inciar): "Processo %d, filho de %d\n"

// Obs:
// - netos devem esperar 5 segundos antes de imprmir a mensagem de finalizado (e terminar)
// - pais devem esperar pelos seu descendentes diretos antes de terminar
#define CHILDREN 2
#define GRANDCHILDREN 6

void grandchild()
{
    printf("Processo %d, filho de %d\n", getpid(), getppid());
    sleep(5);
    printf("Processo %d finalizado\n", getpid());
}

void child()
{
    pid_t grandchild_pid;
    pid_t child_pid = getpid();
    printf("Processo %d, filho de %d\n", getpid(), getppid());

    for (int i = 0; i < GRANDCHILDREN / 2; i++)
    {
        grandchild_pid = fork();

        if (grandchild_pid == 0)
        {
            grandchild();
            break;
        }
    }

    while (wait(NULL) >= 0)
        ;

    if (getpid() == child_pid)
        printf("Processo %d finalizado\n", getpid());
}

int main(int argc, char **argv)
{
    pid_t parent_pid = getpid();
    pid_t child_pid;

    for (int i = 0; i < CHILDREN; i++)
    {
        child_pid = fork();

        if (child_pid == 0)
        {
            child();
            break;
        }
    }

    while (wait(NULL) >= 0)
        ;

    if (getpid() == parent_pid)
        printf("Processo principal %d finalizado\n", getpid());

    return 0;
}
