#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simulação simples de supermercado COM semáforo
"""

import threading
import time
import random

class Caixa:
    """Um caixa de supermercado"""
    
    def __init__(self):
        self.valor_total = 0.0
        self.semaforo = threading.Semaphore(1)  # Semáforo para controle de acesso
    
    def calcular_compra(self, cliente_id, valor):
        """Calcula o valor total da compra usando semáforo para proteção"""
        print(f"Cliente {cliente_id} quer pagar R$ {valor:.2f}")
        
        # Adquire o semáforo - garante acesso exclusivo
        self.semaforo.acquire()
        try:
            print(f"Cliente {cliente_id} está sendo atendido")
            
            # Simula o tempo de processamento
            time.sleep(0.5)
            
            # Atualiza o valor total (operação protegida pelo semáforo)
            valor_anterior = self.valor_total
            self.valor_total += valor
            
            print(f"Cliente {cliente_id} pagou R$ {valor:.2f}. Caixa: {valor_anterior:.2f} -> {self.valor_total:.2f}")
        finally:
            # Libera o semáforo após o uso
            self.semaforo.release()


def cliente(id_cliente, caixa):
    """Função que representa um cliente"""
    # Valor aleatório entre 10 e 100
    valor_compra = random.uniform(10, 100)
    caixa.calcular_compra(id_cliente, valor_compra)
    return valor_compra


def main():
    print("SIMULAÇÃO DE SUPERMERCADO COM SEMÁFORO\n")
    
    # Inicializa o caixa
    caixa = Caixa()
    
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
    print("Com semáforo, não deve haver diferença significativa.")


if __name__ == "__main__":
    main()
