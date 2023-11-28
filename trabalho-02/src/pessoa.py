from threading import Thread
import variaveis_globais as vg


class Pessoa(Thread):
    def __init__(self, faixa_etaria, id):
        super().__init__()
        self.faixa_etaria = faixa_etaria
        self.id = id

    def run(self):
        vg.fila.put(self)
        print(
            f"[Pessoa {self.id} / {self.faixa_etaria}] Entrou na Ixfera (quantidade = 0)."
        )  # {}).")
