from caixa import Caixa
from cliente import Cliente
import threading
import copy

class SuperMercado:
    # clientes deve ser uma lista de instancias da classe Cliente
    def __init__(self, clientes):
        self.caixa = Caixa(0.5)
        self.clientes = clientes

    def simular(self):

        # setando os caixas
        for cliente in self.clientes:
            cliente.set_caixa(self.caixa)

        # iniciando as threads
        for cliente in self.clientes:
            cliente.start()

        # esperando que todas as threads acabem
        for cliente in self.clientes:
            cliente.join()
            

        print('\n\n\n')
        print('Atendimento terminou com:')
        for cliente in self.clientes:
            print(f'{cliente} terminou com saldo de R${cliente.dinheiro :.2f}')