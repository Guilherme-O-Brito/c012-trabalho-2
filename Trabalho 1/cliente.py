class Cliente:
    '''
        as compras deve ser um vetor de tuplas com nome e valor do produto 
        EX:
        [('1L de leite', 7.5), ('0.5Kg de contra-file',25)]
    '''
    def __init__(self, nome, idade, compras, dinheiro):
        self.nome = nome
        self.idade = idade
        self.compras = compras
        self.dinheiro = dinheiro
        self.espera = 0

    def __str__(self):
        return self.nome        