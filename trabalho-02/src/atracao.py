from threading import Thread


class Atracao(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        # Lógica da thread da pessoa
        ...
