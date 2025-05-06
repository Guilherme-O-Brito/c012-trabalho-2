#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Comparação direta entre simulações com e sem semáforo
"""

import subprocess
import time
import os

def executar_simulacoes():
    """Executa ambas as simulações em sequência"""
    print("="*50)
    print("EXECUÇÃO DA SIMULAÇÃO SEM SEMÁFORO")
    print("="*50)
    
    # Obtém o diretório atual do script
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    
    # Executa o programa sem semáforo com o caminho correto
    sem_semaforo_path = os.path.join(diretorio_atual, "supermercado_sem_semaforo.py")
    subprocess.run(["python", sem_semaforo_path], check=True)
    
    # Pequena pausa entre execuções
    time.sleep(1)
    
    print("\n" + "="*50)
    print("EXECUÇÃO DA SIMULAÇÃO COM SEMÁFORO")
    print("="*50)
    
    # Executa o programa com semáforo com o caminho correto
    com_semaforo_path = os.path.join(diretorio_atual, "supermercado_simulacao.py")
    subprocess.run(["python", com_semaforo_path], check=True)


def main():
    print("="*50)
    print("COMPARAÇÃO: SUPERMERCADO COM E SEM SEMÁFORO")
    print("="*50)
    
    # Executa ambas as simulações
    executar_simulacoes()
    
    print("\n" + "="*50)
    print("COMPARAÇÃO FINALIZADA")
    print("="*50)



if __name__ == "__main__":
    main()