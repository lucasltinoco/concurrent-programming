from threading import Thread
import variaveis_globais as vg
from time import sleep, time
from datetime import datetime


class Ixfera(Thread):
    def __init__(self, entrada) -> None:
        """
        """
        super().__init__()
        self.experiencia = None
        self.entrada = entrada
        self.atracao_ativa = False
        self.tempo_atracao = [] # Lista de tuplas com inicio e fim
        self.inicio = .0
        self.fim = .0

    def run(self):
        """
        """
        while len(vg.pessoas_atendidas) <= self.entrada.N_PESSOAS:
            if (
                vg.pessoas_na_ixfera.empty()
                and vg.fila.empty()
                and self.experiencia != None
                and self.atracao_ativa
            ):
                print(
                    f"{datetime.now().isoformat().split('T')[1]} [Ixfera] Pausando a experiencia {self.experiencia}."
                )
                self.fim = time()
                self.tempo_atracao.append(self.fim - self.inicio)
                self.inicio = .0
                self.fim = .0
                self.atracao_ativa = False
                if len(vg.pessoas_atendidas) == self.entrada.N_PESSOAS:
                    break
                vg.ixfera_sem.acquire()
            if not self.atracao_ativa:
                self.iniciar_experiencia()
            else:
                self.preencher_vagas()

    def iniciar_experiencia(self):
        """
        """
        if not vg.fila.empty():
            with vg.mutex_fila:
                pessoa = vg.fila.get()
                pessoa.fim_espera = time()
            with vg.mutex_pessoas_na_ixfera:
                vg.pessoas_na_ixfera.put(pessoa)
            vg.pessoas_atendidas.append(pessoa)
            self.experiencia = pessoa.faixa_etaria
            self.atracao_ativa = True
            print(
                f"{datetime.now().isoformat().split('T')[1]} [Ixfera] Iniciando a experiencia {pessoa.faixa_etaria}."
            )
            self.inicio = time()
            vg.entrada_na_atracao_sem.release()

    def preencher_vagas(self):
        """
        """
        if not vg.fila.empty():
            pessoa = vg.fila.queue[0]
            if (
                self.experiencia == pessoa.faixa_etaria
                and vg.pessoas_na_ixfera.qsize() == self.entrada.N_VAGAS
            ):
                vg.espera_liberar_vaga_sem.acquire()
            elif (
                pessoa.faixa_etaria != self.experiencia
                and not vg.pessoas_na_ixfera.empty()
            ):
                vg.espera_experiencia_sem.acquire()
                self.experiencia = pessoa.faixa_etaria
                print(
                    f"{datetime.now().isoformat().split('T')[1]} [Ixfera] Iniciando a experiencia {pessoa.faixa_etaria}."
                )
                if self.inicio == .0:
                    self.inicio = time()
            with vg.mutex_fila:
                pessoa = vg.fila.get()
                pessoa.fim_espera = time()
            with vg.mutex_pessoas_na_ixfera:
                vg.pessoas_na_ixfera.put(pessoa)
            vg.pessoas_atendidas.append(pessoa)
            vg.entrada_na_atracao_sem.release()
