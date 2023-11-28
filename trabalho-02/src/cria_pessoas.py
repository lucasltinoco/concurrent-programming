from threading import Thread
from pessoa import Pessoa
import random


class CriaPessoas(Thread):
    def __init__(self, entrada):
        super().__init__()
        self.entrada = entrada

    def run(self):
        for index in range(self.entrada.N_PESSOAS):
            faixa_etaria = random.choice(["A", "B", "C"])
            Pessoa(faixa_etaria, index + 1).start()
