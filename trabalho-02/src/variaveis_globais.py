import queue
import threading


def iniciar_variaveis_globais():
    global fila, mutex_fila, ixfera_sem, pessoas_na_ixfera, mutex_pessoas_na_ixfera, entrada_na_atracao_sem, espera_experiencia_sem, espera_liberar_vaga_sem, pessoas_atendidas

    fila = queue.Queue()

    mutex_fila = threading.Lock()

    ixfera_sem = threading.Semaphore(0)

    pessoas_na_ixfera = queue.Queue()

    mutex_pessoas_na_ixfera = threading.Lock()

    entrada_na_atracao_sem = threading.Semaphore(0)

    espera_experiencia_sem = threading.Semaphore(0)

    espera_liberar_vaga_sem = threading.Semaphore(0)
    
    pessoas_atendidas = []
