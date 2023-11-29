from threading import Thread
from pessoa import Pessoa
from time import sleep
import random


class CriaPessoas(Thread):
    def __init__(self, entrada):
        """Construtor da classe CriaPessoas"""
        super().__init__()
        self.entrada = entrada

    def run(self):
        """Lógica da Thread CriaPessoas"""
        threads_de_pessoas = []

        # Cria as threads de pessoas
        for index in range(self.entrada.N_PESSOAS):
            tempo_ate_entrar_na_fila = random.randint(
                1, self.entrada.MAX_INTERVALO * self.entrada.UNID_TEMPO
            )
            sleep(tempo_ate_entrar_na_fila)
            faixa_etaria = random.choice(["A", "B", "C"])
            pessoa = Pessoa(faixa_etaria, index + 1, self.entrada)
            pessoa.start()
            threads_de_pessoas.append(pessoa)

        # Espera as threads de pessoas terminarem
        for thread in threads_de_pessoas:
            thread.join()
