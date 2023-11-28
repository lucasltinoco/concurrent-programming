import random
from entrada import Entrada
from cria_pessoas import CriaPessoas
import variaveis_globais as vg


def main():
    entrada = Entrada()

    random.seed(entrada.SEMENTE)

    vg.iniciar_variaveis_globais()

    CriaPessoas(entrada).start()

    print(f"pessoas_na_fila {vg.fila.qsize()}")

    print("[Ixfera] Simulacao iniciada.")


if __name__ == "__main__":
    main()
