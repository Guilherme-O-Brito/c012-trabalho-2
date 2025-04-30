#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simulação simples de supermercado SEM semáforo
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
        time.sleep(0.5)
        
        # Operação não atômica que causa problema de concorrência
        # 1. Lê o valor atual
        valor_atual = self.valor_total
        
        # 2. Pequena pausa para maximizar as chances de condição de corrida
        time.sleep(0.1)
        
        # 3. Calcula novo valor
        novo_valor = valor_atual + valor
        
        # 4. Outra pequena pausa 
        time.sleep(0.1)
        
        # 5. Atribui o novo valor - se outro thread modificou valor_total enquanto isso,
        # essa mudança será sobrescrita
        self.valor_total = novo_valor
        
        print(f"Cliente {cliente_id} pagou R$ {valor:.2f}. Caixa: {valor_atual:.2f} -> {self.valor_total:.2f}")


def cliente(id_cliente, caixa):
    """Função que representa um cliente"""
    # Valor aleatório entre 10 e 100
    valor_compra = random.uniform(10, 100)
    caixa.calcular_compra(id_cliente, valor_compra)
    return valor_compra


def main():
    print("SIMULAÇÃO DE SUPERMERCADO SEM SEMÁFORO\n")
    
    # Inicializa o caixa
    caixa = CaixaSemProtecao()
    
    # Lista para armazenar todas as threads e valores
    threads = []
    valores_compra = []
    
    # Cria e inicia 10 threads (clientes)
    for i in range(1, 11):
        # Valor da compra
        valor = random.uniform(10, 100)
        valores_compra.append(valor)
        
        # Cria e inicia a thread
        t = threading.Thread(target=cliente, args=(i, caixa))
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
    print("Sem semáforo, provavelmente há diferença devido a condições de corrida!")


if __name__ == "__main__":
    main()