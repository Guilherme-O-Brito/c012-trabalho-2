from supermercado import SuperMercado
from cliente import Cliente
from caixa import Caixa

if __name__ == '__main__':
    clientes = [
        Cliente('Cliente 1', 22, [('Pacote de Bolacha', 5)], 50),
        Cliente('Cliente 2', 45, [('1kg de carne de boi', 25), ('1kg de carne de porco', 21.65), ('2l de coca', 12.7), ('0.5kg de sal grosso', 8.99), ('5kg de carvão', 30)], 200),
        Cliente('Cliente 3', 16, [('2 pães', 2.05)], 10),
        Cliente('Cliente 4', 18, [('0.5kg de café',29.99), ('Filtros de café', 15)], 70),
        Cliente('Cliente 5', 69, [('1kg de arroz', 6.5), ('1kg de feijão', 7.5), ('1kg de açucar', 5.3)], 100)
    ]

    supermercado = SuperMercado(clientes)

    supermercado.simular()