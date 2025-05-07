#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simulação de supermercado COM semáforo
"""

import threading
import time
import random

class CaixaComSemaforo:
    """Um caixa de supermercado com proteção por semáforo contra acesso concorrente"""
    
    def __init__(self):
        self.valor_total = 0.0
        self.semaforo = threading.Semaphore(1)  # Semáforo para controle de acesso exclusivo
    
    def calcular_compra(self, cliente_id, valor):
        """Calcula o valor total da compra usando semáforo para proteção"""
        print(f"Cliente {cliente_id} quer pagar R$ {valor:.2f}")
        
        # Adquire o semáforo - garante acesso exclusivo
        self.semaforo.acquire()
        
        try:
            print(f"Cliente {cliente_id} está sendo atendido (tem acesso exclusivo)")
            
            # Simula o tempo de processamento
            time.sleep(0.1)
            
            # Operações na região crítica (protegidas pelo semáforo)
            # 1. Lê o valor atual
            valor_atual = self.valor_total
            
            # 2. Mesmo tempo de pausa do outro exemplo
            time.sleep(0.2)
            
            # 3. Calcula novo valor
            novo_valor = valor_atual + valor
            
            # 4. Outra pausa 
            time.sleep(0.1)
            
            # 5. Atribui o novo valor
            self.valor_total = novo_valor
            
            print(f"Cliente {cliente_id} pagou R$ {valor:.2f}. Caixa: {valor_atual:.2f} -> {self.valor_total:.2f}")
            
        finally:
            # Libera o semáforo ao terminar
            self.semaforo.release()


def cliente(id_cliente, caixa, valor_compra):
    """Função que simula um cliente realizando uma compra"""
    caixa.calcular_compra(id_cliente, valor_compra)


def main():
    print("\nSIMULAÇÃO DE SUPERMERCADO COM SEMÁFORO\n")
    
    # Inicializa o caixa
    caixa = CaixaComSemaforo()
    
    # Número de clientes
    num_clientes = 5
    
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
