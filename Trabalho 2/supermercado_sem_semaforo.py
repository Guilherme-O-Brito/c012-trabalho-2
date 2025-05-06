#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simulação de supermercado SEM semáforo
"""

import threading
import time
import random

class CaixaSemProtecao:
    """Um caixa de supermercado sem proteção contra acesso concorrente"""
    
    def __init__(self):
        self.valor_total = 0.0
    
    def calcular_compra(self, cliente_id, valor):
        """Calcula o valor total da compra SEM proteção - sujeito a condições de corrida"""
        print(f"Cliente {cliente_id} quer pagar R$ {valor:.2f}")
        
        print(f"Cliente {cliente_id} está sendo atendido")
        
        # Simula o tempo de processamento
        time.sleep(0.1)
        
        # Operações não atômicas que causam problema de concorrência
        # 1. Lê o valor atual
        valor_atual = self.valor_total
        print(f">>> Cliente {cliente_id} leu o valor atual: R$ {valor_atual:.2f}")
        
        # 2. Pequena pausa que simula o tempo de processamento
        time.sleep(0.2)
        
        # 3. Calcula novo valor
        novo_valor = valor_atual + valor
        
        # 4. Outra pequena pausa antes de atualizar
        time.sleep(0.1)
        
        # 5. Atribui o novo valor
        self.valor_total = novo_valor
        
        print(f"Cliente {cliente_id} pagou R$ {valor:.2f}. Caixa: {valor_atual:.2f} -> {self.valor_total:.2f}")


def cliente(id_cliente, caixa, valor_compra):
    """Função que representa um cliente"""
    caixa.calcular_compra(id_cliente, valor_compra)


def main():
    print("\nSIMULAÇÃO DE SUPERMERCADO SEM SEMÁFORO\n")
    
    # Inicializa o caixa
    caixa = CaixaSemProtecao()
    
    # Número de clientes
    num_clientes = 10
    
    # Cria valores aleatórios para as compras (sem seed fixa)
    valores_compra = [round(random.uniform(10, 100), 2) for _ in range(num_clientes)]
    
    # Lista para armazenar todas as threads
    threads = []
    
    # Criando e iniciando as threads (clientes)
    for i in range(1, num_clientes + 1):
        t = threading.Thread(target=cliente, args=(i, caixa, valores_compra[i-1]))
        threads.append(t)
        t.start()
    
    # Aguarda todas as threads terminarem
    for t in threads:
        t.join()
    
    # Verifica se o cálculo está correto
    valor_esperado = sum(valores_compra)
    
    print("\nResultados:")
    print(f"Valor total calculado no caixa: R$ {caixa.valor_total:.2f}")
    print(f"Soma das compras individuais: R$ {valor_esperado:.2f}")
    print(f"Diferença: R$ {valor_esperado - caixa.valor_total:.2f}")


if __name__ == "__main__":
    main()