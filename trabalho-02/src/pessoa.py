from threading import Thread
from time import sleep
import random
import variaveis_globais as vg


class Pessoa(Thread):
    def __init__(self, faixa_etaria, id, entrada):
        super().__init__()
        self.faixa_etaria = faixa_etaria
        self.id = id
        self.entrada = entrada

    def run(self):
        tempo_ate_entrar = random.randint(1, self.entrada.MAX_INTERVALO * self.entrada.UNID_TEMPO)
        sleep(tempo_ate_entrar)

        vg.mutex_fila.acquire()
        vg.fila.put(self)
        print(f"[Pessoa {self.id} / {self.faixa_etaria}] Aguardando na fila.")
        vg.mutex_fila.release()
        
        # print(
        #     f"[Pessoa {self.id} / {self.faixa_etaria}] Entrou na Ixfera (quantidade = 0)."
        # )  # {}).")
