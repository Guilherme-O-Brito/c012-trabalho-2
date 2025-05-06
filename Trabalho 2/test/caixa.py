from cliente import Cliente
import time

class Caixa:
    def __init__(self, tempo_de_processamento = 0.2):
        self.tempo_de_processamento = tempo_de_processamento

    def passar_compras(self, cliente: Cliente):
        compras = cliente.compras
        total = 0
        for compra in compras:
            item, valor = compra
            total += valor
            print(f'+ {item} passado na compra do {cliente}, total ate o momento R${total :.2f} +')
            time.sleep(self.tempo_de_processamento)
        cliente.dinheiro -= total
