from threading import Thread
from time import sleep, time
import variaveis_globais as vg


class Pessoa(Thread):
    def __init__(self, faixa_etaria, id, entrada):
        """Construtor da classe Pessoa
        :param faixa_etaria: Faixa etária da pessoa
        :param id: Identificador da pessoa
        :param entrada: Objeto com os dados de entrada do usuário
        :param inicio_espera: Tempo em que a pessoa entrou na fila
        :param fim_espera: Tempo em que a pessoa saiu da fila
        """
        super().__init__()
        self.faixa_etaria = faixa_etaria
        self.id = id
        self.entrada = entrada
        self.inicio_espera = None
        self.fim_espera = None

    def run(self):
        """Lógica da Thread Pessoa"""
        # Aguarda a liberação da fila e entra nela
        with vg.mutex_fila:
            vg.fila.put(self)
            self.inicio_espera = time()
        print("[Pessoa {self.id} / {self.faixa_etaria}] Aguardando na fila.")

        # Tira Ixfera do estado de pausa
        if vg.pessoas_na_ixfera.empty() and vg.fila.qsize() == 1:
            vg.ixfera_sem.release()

        # Aguarda a liberação da vaga na experiência e entra nela
        vg.entrada_na_atracao_sem.acquire()
        print(
            "[Pessoa {self.id} / {self.faixa_etaria}] Entrou na Ixfera (quantidade = {vg.pessoas_na_ixfera.qsize()})."
        )

        # Aguarda o tempo de permanência na experiência
        sleep(self.entrada.PERMANENCIA * self.entrada.UNID_TEMPO)

        # Sai da experiência
        with vg.mutex_pessoas_na_ixfera:
            vg.pessoas_na_ixfera.get()
        print(
            "[Pessoa {self.id} / {self.faixa_etaria}] Saiu da Ixfera (quantidade = {vg.pessoas_na_ixfera.qsize()})."
        )

        # Libera a vaga na experiência, caso esteja lotada
        if vg.pessoas_na_ixfera.qsize() == self.entrada.N_VAGAS - 1:
            vg.espera_liberar_vaga_sem.release()

        # Libera próxima experiência, caso seja a última pessoa da ixfera
        if vg.pessoas_na_ixfera.qsize() == 0:
            vg.espera_experiencia_sem.release()
