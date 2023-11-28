from threading import Thread
import variaveis_globais as vg


class Ixfera(Thread):
    def __init__(self, entrada) -> None:
        super().__init__()
        self.pessoas_na_ixfera = 0
        self.experiencia = None
        self.entrada = entrada
        self.pessoas = []

    def run(self):
        print("[Ixfera] Simulacao iniciada.")
        self.iniciar_experiencia()
        self.preencher_vagas()
        self.debug_fila()
        self.debug_pessoas()

    def iniciar_experiencia(self):
        """Inicia a experiência da Ixfera

        - Incrementa a pessoas_na_ixfera de pessoas na Ixfera (self.pessoas_na_ixfera)
        - Define a experiência como a faixa_etaria da primeira pessoa a entrar na Ixfera (self.experiencia)
        - Adiciona essa pessoa a lista de pessoas da Ixfera (self.pessoas)
        - Exibe na tela Iniciando a Experiencia
        """
        vg.ixfera_sem.acquire()  # Espera a inserção de pessoas na queue

        if not vg.fila.empty():
            pessoa = vg.fila.get()
            self.pessoas.append(pessoa)
            self.pessoas_na_ixfera += 1
            self.experiencia = pessoa.faixa_etaria

        print(f"[Ixfera] Iniciando a experiencia {pessoa.faixa_etaria}.")

    def preencher_vagas(self):
        """ """
        vg.ixfera_sem.acquire()  # Espera a inserção de pessoas na queue
        vg.mutex_fila.acquire()
        if not vg.fila.empty():
            for pessoa in list(vg.fila.queue):
                print("A")
                if self.pessoas_na_ixfera < self.entrada.N_VAGAS:
                    if pessoa.faixa_etaria == self.experiencia:
                        proxima_pessoa = vg.fila.get()
                        self.pessoas.append(proxima_pessoa)
                        self.pessoas_na_ixfera += 1
                        print(
                            f"[Pessoa {pessoa.id} / {pessoa.faixa_etaria}] Entrou na Ixfera (pessoas_na_ixfera = {self.pessoas_na_ixfera})"
                        )
                    else:
                        print(
                            f"[DEBG] Pessoa {pessoa.id}/{pessoa.faixa_etaria}, faixa etaria invalida"
                        )
                else:
                    print("Experiencia finalizada")
        vg.mutex_fila.release()

    def pausar_experiencia(self):
        # Lógica para pausar uma experiência na Ixfera
        pass

    def pessoa_entra(self, pessoa):
        # Lógica para uma pessoa entrar na Ixfera
        pass

    def pessoa_sai(self, pessoa):
        # Lógica para uma pessoa sair da Ixfera
        pass

    """ Funcionalidades para Debuggar Código """

    def debug_fila(self):
        from time import sleep

        sleep(1)
        print("\n---------- DEBUGGING FILA ----------")
        print(f"Tamanho da Fila: {vg.fila.qsize()}")
        for pessoa in list(vg.fila.queue):
            print("Pessoa ", pessoa.id, pessoa.faixa_etaria)
        print("---------- END DEBUGGING ----------\n")

    def debug_pessoas(self):
        from time import sleep

        sleep(1)
        print("\n---------- DEBUGGING PESSOAS ----------")
        print(f"Tamanhoa da lista Pessoas: {len(self.pessoas)}")
        for pessoa in self.pessoas:
            print("Pessoa ", pessoa.id, pessoa.faixa_etaria)
        print("---------- END DEBUGGING ----------\n")
