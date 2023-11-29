import random
from entrada import Entrada
from cria_pessoas import CriaPessoas
import variaveis_globais as vg
from ixfera import Ixfera
from time import time
from datetime import datetime


def debug_entrada(entrada):
    print("\n---------- DEBUGGING ----------")
    print("N_PESSOAS", entrada.N_PESSOAS)
    print("N_VAGAS", entrada.N_VAGAS)
    print("PERMANENCIA", entrada.PERMANENCIA)
    print("MAX_INTERVALO", entrada.MAX_INTERVALO)
    print("SEMENTE", entrada.SEMENTE)
    print("UNID_TEMPO", entrada.UNID_TEMPO)
    print("---------- END DEBUGGING ----------\n")


def main():
    entrada = Entrada()
    # DEBUGGING LINE CODE
    debug_entrada(entrada)

    random.seed(entrada.SEMENTE)

    vg.iniciar_variaveis_globais()

    ixfera = Ixfera(entrada)

    print(f"{datetime.now().isoformat().split('T')[1]} [Ixfera] Simulacao iniciada.")
    ixfera.start()

    cria_pessoas = CriaPessoas(entrada)
    cria_pessoas.start()

    cria_pessoas.join()
    ixfera.join()
    print(f"{datetime.now().isoformat().split('T')[1]} [Ixfera] Simulacao finalizada.")
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

    print("\nTempo medio de espera")
    print("Faixa A: {:.2f}".format(tempo_espera_total_A / pessoas_atendidas_A))
    print("Faixa B: {:.2f}".format(tempo_espera_total_B / pessoas_atendidas_B))
    print("Faixa C: {:.2f}".format(tempo_espera_total_C / pessoas_atendidas_C))

    print(f"\nTaxa de ocupacao: ")


if __name__ == "__main__":
    main()
