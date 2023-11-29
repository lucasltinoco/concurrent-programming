from threading import Thread
import variaveis_globais as vg
from time import sleep, time
from datetime import datetime


class Ixfera(Thread):
    def __init__(self, entrada) -> None:
        super().__init__()
        self.experiencia = None
        self.entrada = entrada
        self.atracao_ativa = False

    def run(self):
        while len(vg.pessoas_atendidas) < self.entrada.N_PESSOAS:
            if (
                vg.pessoas_na_ixfera.empty()
                and vg.fila.empty()
                and self.experiencia != None
                and self.atracao_ativa
            ):
                print(
                    f"{datetime.now().isoformat().split('T')[1]} [Ixfera] Pausando a experiencia {self.experiencia}."
                )
                self.atracao_ativa = False
                vg.ixfera_sem.acquire()

            if not self.atracao_ativa:
                self.iniciar_experiencia()
            else:
                self.preencher_vagas()

    def iniciar_experiencia(self):
        """Inicia a experiência da Ixfera

        - Incrementa a quantidade de pessoas na Ixfera (self.pessoas_na_ixfera)
        - Define a experiência como a faixa_etaria da primeira pessoa a entrar na Ixfera (self.experiencia)
        - Adiciona essa pessoa a lista de pessoas da Ixfera (self.pessoas)
        - Exibe na tela Iniciando a Experiencia
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
            vg.entrada_na_atracao_sem.release()

    def preencher_vagas(self):
        #     """ """
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
            with vg.mutex_fila:
                pessoa = vg.fila.get()
                pessoa.fim_espera = time()
            with vg.mutex_pessoas_na_ixfera:
                vg.pessoas_na_ixfera.put(pessoa)
            vg.pessoas_atendidas.append(pessoa)
            vg.entrada_na_atracao_sem.release()

    def debug_fila(self):
        sleep(1)
        print("\n---------- DEBUGGING FILA ----------")
        print(f"Tamanho da Fila: {vg.fila.qsize()}")
        for pessoa in list(vg.fila.queue):
            print("Pessoa ", pessoa.id, pessoa.faixa_etaria)
        print("---------- END DEBUGGING ----------\n")

    def debug_pessoas(self):
        sleep(1)
        print("\n---------- DEBUGGING PESSOAS ----------")
        print(f"Tamanhoa da lista Pessoas: {vg.pessoas_na_ixfera.qsize()}")
        for pessoa in list(vg.pessoas_na_ixfera.queue):
            print("Pessoa ", pessoa.id, pessoa.faixa_etaria)
        print("---------- END DEBUGGING ----------\n")
