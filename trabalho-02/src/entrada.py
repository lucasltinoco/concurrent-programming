from sys import argv


class Entrada:
    def __init__(self):
        if len(argv) != 7:
            print(
                "Uso: python3 ixphere.py <N_PESSOAS> <N_VAGAS> <PERMANENCIA> <MAX_INTERVALO> <SEMENTE> <UNID_TEMPO>"
            )
            return

        self.N_PESSOAS = int(argv[1])
        self.N_VAGAS = int(argv[2])
        self.PERMANENCIA = int(argv[3])
        self.MAX_INTERVALO = int(argv[4])
        self.SEMENTE = int(argv[5])
        self.UNID_TEMPO = int(argv[6]) / 1000
