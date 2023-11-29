import random
from entrada import Entrada
from cria_pessoas import CriaPessoas
import variaveis_globais as vg
from ixfera import Ixfera
from time import time
from datetime import datetime

def main():
    # Objeto para orgnanizar os dados de entrado do usuário
    entrada = Entrada()

    # Seed para calcular números pseudo-aleatórios
    random.seed(entrada.SEMENTE)

    # Variáveis Globais para sincronização de threads
    vg.iniciar_variaveis_globais()

    ixfera = Ixfera(entrada)

    print(f"{datetime.now().isoformat().split('T')[1]} [Ixfera] Simulacao iniciada.")
    tempo_inicio_simulacao = time()
    ixfera.start()

    cria_pessoas = CriaPessoas(entrada)
    cria_pessoas.start()

    cria_pessoas.join()
    ixfera.join()
    print(f"{datetime.now().isoformat().split('T')[1]} [Ixfera] Simulacao finalizada.")
    tempo_final_simulacao = time()
    tempo_espera_total_A = 0
    pessoas_atendidas_A = 0
    tempo_espera_total_B = 0
    pessoas_atendidas_B = 0
    tempo_espera_total_C = 0
    pessoas_atendidas_C = 0

    for pessoa in vg.pessoas_atendidas:
        if pessoa.faixa_etaria == "A":
            tempo_espera_total_A += pessoa.fim_espera - pessoa.inicio_espera
            pessoas_atendidas_A += 1
        elif pessoa.faixa_etaria == "B":
            tempo_espera_total_B += pessoa.fim_espera - pessoa.inicio_espera
            pessoas_atendidas_B += 1
        elif pessoa.faixa_etaria == "C":
            tempo_espera_total_C += pessoa.fim_espera - pessoa.inicio_espera
            pessoas_atendidas_C += 1

    print("\nTempo medio de espera:")
    print("Faixa A: {:.2f}".format(tempo_espera_total_A / pessoas_atendidas_A))
    print("Faixa B: {:.2f}".format(tempo_espera_total_B / pessoas_atendidas_B))
    print("Faixa C: {:.2f}".format(tempo_espera_total_C / pessoas_atendidas_C))
    #print(ixfera.tempo_atracao, tempo_final_simulacao - tempo_inicio_simulacao)
    print("\nTaxa de ocupacao: {:.2f}".format(sum(ixfera.tempo_atracao)/(tempo_final_simulacao - tempo_inicio_simulacao)))


if __name__ == "__main__":
    main()
