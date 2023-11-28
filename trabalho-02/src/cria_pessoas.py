from threading import Thread
from pessoa import Pessoa
import random
import variaveis_globais as vg

class CriaPessoas(Thread):
    def __init__(self, entrada):
        super().__init__()
        self.entrada = entrada

    def run(self):
        threads_de_pessoas = []

        for index in range(self.entrada.N_PESSOAS):
            faixa_etaria = random.choice(["A", "B", "C"])
            pessoa = Pessoa(faixa_etaria, index + 1, self.entrada)
            pessoa.start()
            threads_de_pessoas.append(pessoa)

        for thread in threads_de_pessoas:
            thread.join()
            
        print(vg.fila.qsize())
