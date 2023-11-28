import random
from entrada import Entrada
from cria_pessoas import CriaPessoas
import variaveis_globais as vg
from ixfera import Ixfera


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

    Ixfera(entrada).start()

    CriaPessoas(entrada).start()


if __name__ == "__main__":
    main()
