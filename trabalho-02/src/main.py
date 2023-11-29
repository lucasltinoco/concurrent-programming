import random
from entrada import Entrada
from cria_pessoas import CriaPessoas
import variaveis_globais as vg
from ixfera import Ixfera
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


if __name__ == "__main__":
    main()
