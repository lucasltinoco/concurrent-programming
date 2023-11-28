import random
from entrada import Entrada
from cria_pessoas import CriaPessoas
import variaveis_globais as vg


def main():
    entrada = Entrada()

    random.seed(entrada.SEMENTE)

    vg.iniciar_variaveis_globais()

    print("[Ixfera] Simulacao iniciada.")

    CriaPessoas(entrada).start()


if __name__ == "__main__":
    main()
