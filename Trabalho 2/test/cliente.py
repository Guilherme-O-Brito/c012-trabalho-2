import threading

class Cliente(threading.Thread):
    '''
        as compras deve ser um vetor de tuplas com nome e valor do produto 
        EX:
        [('1L de leite', 7.5), ('0.5Kg de contra-file',25)]
    '''
    def __init__(self, nome, idade, compras, dinheiro):
        super().__init__()
        self.nome = nome
        self.idade = idade
        self.compras = compras
        self.dinheiro = dinheiro
        self.caixa = None

    def set_caixa(self, caixa):
        self.caixa = caixa

    def __str__(self):
        return self.nome       

    def run(self):
        print(f'Iniciando o atendimento de {self.nome}')
        self.caixa.passar_compras(self) 