from sys import argv


class Entrada:
    def __init__(self):
        if len(argv) != 7:
            print(
                "Uso: python3 ixphere.py <N_PESSOAS> <N_VAGAS> <PERMANENCIA> <MAX_INTERVALO> <SEMENTE> <UNID_TEMPO>"
            )
            return

        self.N_PESSOAS = int(
            argv[1]
        )  # Número de pessoas que irão participar da simulação
        self.N_VAGAS = int(argv[2])  # Número de vagas na experiência
        self.PERMANENCIA = int(argv[3])  # Tempo de permanência na experiência
        self.MAX_INTERVALO = int(
            argv[4]
        )  # Intervalo máximo entre a chegada de pessoas na fila
        self.SEMENTE = int(argv[5])  # Semente para gerar números pseudo-aleatórios
        self.UNID_TEMPO = int(argv[6]) / 1000  # Unidade de tempo em milissegundos
