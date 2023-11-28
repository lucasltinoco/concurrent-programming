import queue
import threading


def iniciar_variaveis_globais():
    global fila, mutex_fila

    fila = queue.Queue()

    mutex_fila = threading.Lock()
