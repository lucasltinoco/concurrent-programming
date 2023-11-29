from threading import Thread
from time import sleep, time
import variaveis_globais as vg
from datetime import datetime


class Pessoa(Thread):
    def __init__(self, faixa_etaria, id, entrada):
        super().__init__()
        self.faixa_etaria = faixa_etaria
        self.id = id
        self.entrada = entrada  # Objeto da classe Entrada
        self.inicio_espera = None
        self.fim_espera = None

    def run(self):
        """Lógica para entrar na fila e exibir na tela"""
        with vg.mutex_fila:
            vg.fila.put(self)
            self.inicio_espera = time()

        print(
            f"{datetime.now().isoformat().split('T')[1]} [Pessoa {self.id} / {self.faixa_etaria}] Aguardando na fila."
        )
        if vg.pessoas_na_ixfera.empty() and vg.fila.qsize() == 1:
            vg.ixfera_sem.release()

        vg.entrada_na_atracao_sem.acquire()
        print(
            f"{datetime.now().isoformat().split('T')[1]} [Pessoa {self.id} / {self.faixa_etaria}] Entrou na Ixfera (quantidade = {vg.pessoas_na_ixfera.qsize()})."
        )

        sleep(self.entrada.PERMANENCIA * self.entrada.UNID_TEMPO)

        with vg.mutex_pessoas_na_ixfera:
            vg.pessoas_na_ixfera.get()
        print(
            f"{datetime.now().isoformat().split('T')[1]} [Pessoa {self.id} / {self.faixa_etaria}] Saiu da Ixfera (quantidade = {vg.pessoas_na_ixfera.qsize()})."
        )

        if vg.pessoas_na_ixfera.qsize() == self.entrada.N_VAGAS - 1:
            vg.espera_liberar_vaga_sem.release()

        if vg.pessoas_na_ixfera.qsize() == 0:
            vg.espera_experiencia_sem.release()
