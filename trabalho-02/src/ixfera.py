from threading import Thread
import variaveis_globais as vg
from time import time


class Ixfera(Thread):
    def __init__(self, entrada) -> None:
        """Construtor da classe Ixfera
        :param entrada: Objeto com os dados de entrada do usuário
        :param experiencia: Faixa etária da experiência atual
        :param entrada: Objeto com os dados de entrada do usuário
        :param atracao_ativa: Flag que indica se a atração está ativa
        :param tempo_atracao: Lista com os tempos de duração de cada experiência
        :param inicio: Tempo em que a experiência atual iniciou
        :param fim: Tempo em que a experiência atual terminou
        """
        super().__init__()
        self.experiencia = None
        self.entrada = entrada
        self.atracao_ativa = False
        self.tempo_atracao = []  # Lista de tuplas com inicio e fim
        self.inicio = 0.0
        self.fim = 0.0

    def run(self):
        """Lógica da Thread Ixfera"""
        # Enquanto a quantidade de pessoas atendidas for menor que a quantidade de pessoas que devem ser atendidas
        while len(vg.pessoas_atendidas) <= self.entrada.N_PESSOAS:
            # Pausa a experiência atual, caso não haja pessoas na fila e na ixfera
            if (
                vg.pessoas_na_ixfera.empty()
                and vg.fila.empty()
                and self.experiencia != None
                and self.atracao_ativa
            ):
                print("[Ixfera] Pausando a experiencia {self.experiencia}.")
                self.fim = time()
                self.tempo_atracao.append(self.fim - self.inicio)
                self.inicio = 0.0
                self.fim = 0.0
                self.atracao_ativa = False
                if len(vg.pessoas_atendidas) == self.entrada.N_PESSOAS:
                    break
                vg.ixfera_sem.acquire()

            # Inicia a experiência, caso haja pessoas na fila e na ixfera
            if not self.atracao_ativa:
                self.iniciar_experiencia()
            # Preenche as vagas da experiência, caso haja pessoas na fila
            else:
                self.preencher_vagas()

    def iniciar_experiencia(self):
        """Inicia a experiência no início da simulação ou após uma pausa"""
        if not vg.fila.empty():
            with vg.mutex_fila:
                pessoa = vg.fila.get()
                pessoa.fim_espera = time()
            with vg.mutex_pessoas_na_ixfera:
                vg.pessoas_na_ixfera.put(pessoa)
            vg.pessoas_atendidas.append(pessoa)
            self.experiencia = pessoa.faixa_etaria
            self.atracao_ativa = True
            print("[Ixfera] Iniciando a experiencia {pessoa.faixa_etaria}.")
            self.inicio = time()
            vg.entrada_na_atracao_sem.release()

    def preencher_vagas(self):
        """Preenche as vagas da experiência"""
        if not vg.fila.empty():
            pessoa = vg.fila.queue[0]
            # Se a pessoa da fila tiver a mesma faixa etária da experiência atual e a experiência estiver lotada, a pessoa aguarda a liberação de uma vaga
            if (
                self.experiencia == pessoa.faixa_etaria
                and vg.pessoas_na_ixfera.qsize() == self.entrada.N_VAGAS
            ):
                vg.espera_liberar_vaga_sem.acquire()
            # Se a pessoa da fila tiver uma faixa etária diferente da experiência atual, a pessoa aguarda a liberação da experiência
            elif (
                pessoa.faixa_etaria != self.experiencia
                and not vg.pessoas_na_ixfera.empty()
            ):
                vg.espera_experiencia_sem.acquire()
                self.experiencia = pessoa.faixa_etaria
                print("[Ixfera] Iniciando a experiencia {pessoa.faixa_etaria}.")
                if self.inicio == 0.0:
                    self.inicio = time()
            with vg.mutex_fila:
                pessoa = vg.fila.get()
                pessoa.fim_espera = time()
            with vg.mutex_pessoas_na_ixfera:
                vg.pessoas_na_ixfera.put(pessoa)
            vg.pessoas_atendidas.append(pessoa)
            vg.entrada_na_atracao_sem.release()
