#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <stdio.h>

//       (pai)
//         |
//    +----+----+
//    |         |
// filho_1   filho_2

// ~~~ printfs  ~~~
// pai (ao criar filho): "Processo pai criou %d\n"
//    pai (ao terminar): "Processo pai finalizado!\n"
//  filhos (ao iniciar): "Processo filho %d criado\n"

// Obs:
// - pai deve esperar pelos filhos antes de terminar!
#define CHILDREN 2

void child()
{
    printf("Processo filho %d criado\n", getpid());
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
        else
        {
            printf("Processo pai criou %d\n", child_pid);
        }
    }

    while (wait(NULL) >= 0)
        ;

    if (getpid() == parent_pid)
        printf("Processo pai finalizado!\n");

    return 0;
}
