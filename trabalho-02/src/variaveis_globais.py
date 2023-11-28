import queue
import threading


def iniciar_variaveis_globais():
    global fila, mutex_fila, ixfera_sem

    fila = queue.Queue()

    mutex_fila = threading.Lock()

    ixfera_sem = threading.Semaphore(0)
