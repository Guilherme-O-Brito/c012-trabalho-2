from caixa import Caixa
from cliente import Cliente
import time
import copy

class SuperMercado:
    # clientes deve ser uma lista de instancias da classe Cliente
    def __init__(self, clientes):
        self.caixa = Caixa(0.5)
        self.clientes = clientes

    def simular_fcfs(self):
        # quem chega primeiro é atendido primeiro
        clientes = copy.deepcopy(self.clientes)
        inicio = time.time()
        
        for cliente in clientes:
            espera = time.time() - inicio
            cliente.espera = espera
            print(f'Iniciando atendimento do {cliente}')
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            self.caixa.passar_compras(cliente)
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print(f'{cliente} foi atendido com tempo de espera de {espera :.2f}')
        

        print('\n\n\n')
        print('Atendimento fcfs terminou com:')
        for cliente in clientes:
            print(f'{cliente} esperou {cliente.espera :.2f}s e saldo de R${cliente.dinheiro :.2f}')
    
    def simular_sjf(self):
        # os com menos compras vem primeiro
        clientes = copy.deepcopy(self.clientes)
        # ordena a fila colocando os clientes com menos compras na frente
        fila_ordenada = sorted(clientes, key=lambda obj: len(obj.compras))
        inicio = time.time()

        for cliente in fila_ordenada:
            espera = time.time() - inicio
            cliente.espera = espera
            print(f'Iniciando atendimento do {cliente}')
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            self.caixa.passar_compras(cliente)
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print(f'{cliente} foi atendido com tempo de espera de {espera :.2f}')
        

        print('\n\n\n')
        print('Atendimento sjf terminou com:')
        for cliente in clientes:
            print(f'{cliente} esperou {cliente.espera :.2f}s e saldo de R${cliente.dinheiro :.2f}')

    def simular_ps(self):
        # prioridade usando idade como parametro
        clientes = copy.deepcopy(self.clientes)
        # ordena a fila garantindo que as pessoas com idade maior ou igual a 60 anos fiquem na frente
        # e caso contrario mantem a ordem de chegada
        fila_ordenada = sorted(clientes, key=lambda obj: (obj.idade < 60))
        inicio = time.time()

        for cliente in fila_ordenada:
            espera = time.time() - inicio
            cliente.espera = espera
            print(f'Iniciando atendimento do {cliente}')
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            self.caixa.passar_compras(cliente)
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print(f'{cliente} foi atendido com tempo de espera de {espera :.2f}')
        

        print('\n\n\n')
        print('Atendimento ps com prioridade para idade >= 60 terminou com:')
        for cliente in clientes:
            print(f'{cliente} esperou {cliente.espera :.2f}s e saldo de R${cliente.dinheiro :.2f}')
