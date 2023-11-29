from threading import Thread
from pessoa import Pessoa
from time import sleep
import random
import variaveis_globais as vg

simulacao_faixas = ["A", "A", "A", "B", "B", "C"]

class CriaPessoas(Thread):
    def __init__(self, entrada):
        super().__init__()
        self.entrada = entrada

    def run(self):
        threads_de_pessoas = []

        for index in range(self.entrada.N_PESSOAS):
            tempo_ate_entrar_na_fila = random.randint(
                1, self.entrada.MAX_INTERVALO * self.entrada.UNID_TEMPO
            )
            sleep(tempo_ate_entrar_na_fila)
            # faixa_etaria = random.choice(["A", "B", "C"]) TODO: descomentar após testes da linha de baixo
            faixa_etaria = simulacao_faixas[index]
            pessoa = Pessoa(faixa_etaria, index + 1, self.entrada)
            pessoa.start()
            threads_de_pessoas.append(pessoa)

        for thread in threads_de_pessoas:
            thread.join()
