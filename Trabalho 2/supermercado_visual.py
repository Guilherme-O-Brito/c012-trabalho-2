#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simulação de Supermercado com Interface Visual em Pixel Art
"""

import pygame
import threading
import time
import random
import sys
from pygame.locals import *

# Configurações da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
BROWN = (139, 69, 19)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_BLUE = (173, 216, 230)
ORANGE = (255, 165, 0)

# Classe para representar um Cliente na interface gráfica
class ClienteVisual:
    def __init__(self, id_cliente, valor_compra, x, y, cor=None):
        self.id = id_cliente
        self.valor_compra = valor_compra
        self.x = x
        self.y = y
        self.cor = cor or (
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255)
        )
        self.estado = "espera"  # espera, atendimento, concluido
        self.caixa_atendimento = None
        self.moedas = []  # Lista de moedas para animar
        self.tamanho = TILE_SIZE
        self.destino_x = x
        self.destino_y = y
        self.velocidade = 1.5  # Velocidade aumentada de volta para o original
        self.tempo_inicio = None
        self.tempo_fim = None
        # Animação
        self.frame = 0
        self.max_frames = 20
        self.direcao = 1  # 1: direita, -1: esquerda

    def mover_para(self, x, y):
        self.destino_x = x
        self.destino_y = y

    def atualizar(self):
        # Movimento em direção ao destino
        if self.x < self.destino_x:
            self.x += min(self.velocidade, self.destino_x - self.x)
            self.direcao = 1
        elif self.x > self.destino_x:
            self.x -= min(self.velocidade, self.x - self.destino_x)
            self.direcao = -1

        if self.y < self.destino_y:
            self.y += min(self.velocidade, self.destino_y - self.y)
        elif self.y > self.destino_y:
            self.y -= min(self.velocidade, self.y - self.destino_y)

        # Atualizar moedas
        moedas_para_remover = []
        for moeda in self.moedas:
            moeda[1] -= 2  # Move para cima
            moeda[2] -= 0.1  # Diminui a opacidade
            if moeda[2] <= 0:
                moedas_para_remover.append(moeda)
        
        # Remover moedas que sumiram
        for moeda in moedas_para_remover:
            self.moedas.remove(moeda)
            
        # Atualizar animação se estiver esperando
        if self.estado == "espera":
            self.frame = (self.frame + 1) % self.max_frames

    def adicionar_moeda(self):
        # [x, y, opacidade]
        self.moedas.append([self.x + self.tamanho/2, self.y, 1.0])

    def desenhar(self, screen, font):
        # Desenhar o cliente (um pequeno retângulo com cabeça redonda)
        cor_ajustada = self.cor
        
        # Animação diferente para o estado de espera
        if self.estado == "espera":
            # Animação suave de balanço enquanto espera
            offset = int(2 * (self.frame / self.max_frames - 0.5) ** 3)
            pygame.draw.circle(screen, cor_ajustada, (self.x + self.tamanho//2 + offset, self.y - 5), self.tamanho//3)
            pygame.draw.rect(screen, cor_ajustada, (self.x + offset, self.y, self.tamanho, self.tamanho))
            
            # Desenhar balão de pensamento mostrando impaciência (apenas a cada certo tempo)
            if self.frame % self.max_frames < self.max_frames // 3:
                # Balão de pensamento
                pygame.draw.ellipse(screen, WHITE, (self.x + self.tamanho + 2, self.y - 20, 25, 15))
                pygame.draw.ellipse(screen, BLACK, (self.x + self.tamanho + 2, self.y - 20, 25, 15), 1)
                pygame.draw.circle(screen, WHITE, (self.x + self.tamanho - 3, self.y - 10), 3)
                pygame.draw.circle(screen, WHITE, (self.x + self.tamanho - 7, self.y - 5), 2)
                
                # Símbolo de interrogação ou relógio dentro do balão
                texto_espera = font.render("?", True, BLACK)
                screen.blit(texto_espera, (self.x + self.tamanho + 12, self.y - 20))
        elif self.estado == "atendimento":
            # Desenhar cliente com cor mais brilhante no atendimento
            cor_brilhante = tuple(min(c + 40, 255) for c in cor_ajustada)
            pygame.draw.circle(screen, cor_brilhante, (self.x + self.tamanho//2, self.y - 5), self.tamanho//3)
            pygame.draw.rect(screen, cor_brilhante, (self.x, self.y, self.tamanho, self.tamanho))
            
            # Adicionar ícone de carrinho de compras
            pygame.draw.rect(screen, DARK_GRAY, (self.x + self.tamanho + 5, self.y + 10, 15, 10), 1)
            pygame.draw.circle(screen, DARK_GRAY, (self.x + self.tamanho + 8, self.y + 22), 2, 1)
            pygame.draw.circle(screen, DARK_GRAY, (self.x + self.tamanho + 15, self.y + 22), 2, 1)
        elif self.estado == "concluido":
            # Cliente com uma expressão mais simples (sem rosto complexo)
            pygame.draw.circle(screen, cor_ajustada, (self.x + self.tamanho//2, self.y - 5), self.tamanho//3)
            pygame.draw.rect(screen, cor_ajustada, (self.x, self.y, self.tamanho, self.tamanho))
            
            # Adicionar bolha de diálogo com "Obrigado!" sempre que o cliente estiver no estado concluído
            pygame.draw.ellipse(screen, WHITE, (self.x + self.tamanho, self.y - 25, 60, 20))
            pygame.draw.ellipse(screen, BLACK, (self.x + self.tamanho, self.y - 25, 60, 20), 1)
            pygame.draw.circle(screen, WHITE, (self.x + self.tamanho - 3, self.y - 15), 3)
            pygame.draw.circle(screen, WHITE, (self.x + self.tamanho - 7, self.y - 10), 2)
            
            texto_obrigado = font.render("Obrigado!", True, BLACK)
            screen.blit(texto_obrigado, (self.x + self.tamanho + 5, self.y - 23))

        # Desenhar o ID
        texto_id = font.render(str(self.id), True, BLACK)
        screen.blit(texto_id, (self.x + self.tamanho//2 - texto_id.get_width()//2, 
                              self.y + self.tamanho//2 - texto_id.get_height()//2))

        # Desenhar as moedas (animação de pagamento)
        for moeda in self.moedas:
            raio = 8
            cor_moeda = (255, 215, 0, int(moeda[2] * 255))
            moeda_surface = pygame.Surface((raio*2, raio*2), pygame.SRCALPHA)
            pygame.draw.circle(moeda_surface, cor_moeda, (raio, raio), raio)
            screen.blit(moeda_surface, (moeda[0] - raio, moeda[1] - raio))

# Classe para representar um Caixa na interface gráfica
class CaixaVisual:
    def __init__(self, id_caixa, x, y, com_semaforo=True):
        self.id = id_caixa
        self.x = x
        self.y = y
        self.com_semaforo = com_semaforo
        self.cliente_atual = None
        self.valor_total = 0.0
        self.estado = "livre"  # livre, ocupado
        self.largura = TILE_SIZE * 3
        self.altura = TILE_SIZE * 2
        self.cor = GREEN if com_semaforo else RED
        self.erro_valor = 0.0  # Diferença entre valor esperado e registrado
        self.clientes_atendidos = 0
        # Animação
        self.frame = 0
        self.max_frames = 30

    def atualizar(self):
        # Atualizar animação
        self.frame = (self.frame + 1) % self.max_frames

    def desenhar(self, screen, font):
        # Desenhar o balcão do caixa
        balcao_rect = pygame.Rect(self.x, self.y, self.largura, self.altura)
        pygame.draw.rect(screen, BROWN, balcao_rect)
        
        # Desenhar detalhes do balcão (bordas)
        pygame.draw.rect(screen, DARK_GRAY, balcao_rect, 2)
        
        # Desenhar o monitor/registradora no caixa com animação
        monitor_rect = pygame.Rect(self.x + 10, self.y - 20, 30, 20)
        pygame.draw.rect(screen, DARK_GRAY, monitor_rect)
        
        # Animação de piscar no monitor
        tela_cor = (0, 100, 0) if self.frame < self.max_frames//2 else (0, 130, 0)
        pygame.draw.rect(screen, tela_cor, (self.x + 12, self.y - 18, 26, 16))
        
        # Indicador de status (semáforo)
        status_cor = GREEN if self.estado == "livre" else RED if self.com_semaforo else YELLOW
        pygame.draw.circle(screen, status_cor, (self.x + self.largura - 15, self.y - 10), 8)
        
        # Desenhar pulse ao redor do semáforo quando ocupado
        if self.estado == "ocupado":
            pulse_size = 2 + int(2 * abs(self.frame / self.max_frames - 0.5))
            pygame.draw.circle(screen, status_cor, (self.x + self.largura - 15, self.y - 10), 8 + pulse_size, 1)
        
        # Texto do caixa
        texto_caixa = font.render(f"Caixa {self.id}", True, WHITE)
        screen.blit(texto_caixa, (self.x + 5, self.y + 5))
        
        # Texto do valor
        texto_valor = font.render(f"R$ {self.valor_total:.2f}", True, WHITE)
        screen.blit(texto_valor, (self.x + 5, self.y + 25))
        
        # Se houver erro no valor (versão sem semáforo)
        if abs(self.erro_valor) > 0.01:
            texto_erro = font.render(f"Erro: R$ {self.erro_valor:.2f}", True, RED)
            screen.blit(texto_erro, (self.x + 5, self.y + 45))

# Simulação com interface visual
class SimulacaoVisual:
    def __init__(self, num_clientes=10, com_semaforo=True):
        self.num_clientes = num_clientes
        self.com_semaforo = com_semaforo
        self.titulo = f"Simulação de Supermercado {'COM' if com_semaforo else 'SEM'} Semáforo"
        
        # Valores para controle da simulação
        self.clientes = []
        self.fila_clientes = []
        self.caixas = []
        self.valor_esperado_total = 0.0
        self.simulacao_iniciada = False
        self.simulacao_concluida = False
        self.tempo_inicio = None
        self.tempo_fim = None
        self.clientes_inicializados = False
        self.voltar_ao_menu = False
        
        # Semáforo para controle na versão com proteção
        self.semaforo = threading.Semaphore(1)

    def inicializar_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(self.titulo)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 14)
        self.font_grande = pygame.font.SysFont('Arial', 24)
        
        # Inicializar o ambiente visual
        self.inicializar_ambiente()

    def inicializar_ambiente(self):
        # Criar caixas
        self.caixas = [CaixaVisual(1, SCREEN_WIDTH // 2 - 50, 200, self.com_semaforo)]
        
        # Área de espera dos clientes
        self.area_espera_x = 100
        self.area_espera_y = 400
        
        # Área de clientes atendidos
        self.area_concluido_x = SCREEN_WIDTH - 200
        self.area_concluido_y = 400
        
        # Carregar som de caixa registradora (se disponível)
        try:
            pygame.mixer.init()
            self.som_caixa = pygame.mixer.Sound("cash_register.wav")
        except:
            self.som_caixa = None

    def criar_clientes(self):
        """Cria os clientes com posições aleatórias na parte inferior da tela"""
        self.clientes = []
        self.fila_clientes = []
        
        for i in range(1, self.num_clientes + 1):
            # Posicionar fora da tela inicialmente
            x = random.randint(-100, -50)
            y = SCREEN_HEIGHT - 50 - random.randint(0, 100)
            
            # Valor de compra aleatório
            valor = round(random.uniform(10.0, 100.0), 2)
            self.valor_esperado_total += valor
            
            # Criar o cliente
            cliente = ClienteVisual(i, valor, x, y)
            self.clientes.append(cliente)
            self.fila_clientes.append(cliente)
        
        self.clientes_inicializados = True
        
        # Inicializar a entrada dos clientes na fila de espera com espaçamento temporal
        threading.Thread(target=self.entrada_clientes_fila, daemon=True).start()
        
    def entrada_clientes_fila(self):
        """Controla a entrada gradual dos clientes na fila de espera"""
        # Esperar um tempo antes de começar a processar clientes
        time.sleep(1.0)  # Reduzido de 2.0 para 1.0
        
        # Posicionar cada cliente na fila, um por um, com uma pequena pausa entre eles
        for i, cliente in enumerate(self.clientes):
            # Posição na fila
            if self.com_semaforo:
                offset = (i % 2) * 5  # Pequeno offset para visualização
                pos_x = self.area_espera_x + (i * 35)
                pos_y = self.area_espera_y + offset
            else:
                pos_x = self.area_espera_x + (i % 5) * 40 + random.randint(-5, 5)
                pos_y = self.area_espera_y + (i // 5) * 40 + random.randint(-5, 5)
            
            # Mover o cliente para a posição na fila
            cliente.mover_para(pos_x, pos_y)
            
            # Pequena pausa entre a entrada de cada cliente
            time.sleep(0.3)  # Reduzido de 0.8 para 0.3

    def desenhar_ambiente(self):
        """Desenha o ambiente do supermercado"""
        # Preencher o fundo
        self.screen.fill(LIGHT_BLUE)
        
        # Desenhar o chão
        pygame.draw.rect(self.screen, GRAY, (0, SCREEN_HEIGHT - 120, SCREEN_WIDTH, 120))
        
        # Desenhar área de caixas
        pygame.draw.rect(self.screen, DARK_GRAY, (0, 150, SCREEN_WIDTH, 100))
        
        # Desenhar uma placa com o título da simulação
        texto_titulo = self.font_grande.render(self.titulo, True, WHITE)
        pygame.draw.rect(self.screen, PURPLE, (SCREEN_WIDTH//2 - texto_titulo.get_width()//2 - 10, 30, texto_titulo.get_width() + 20, 40))
        pygame.draw.rect(self.screen, BLACK, (SCREEN_WIDTH//2 - texto_titulo.get_width()//2 - 10, 30, texto_titulo.get_width() + 20, 40), 2)
        self.screen.blit(texto_titulo, (SCREEN_WIDTH//2 - texto_titulo.get_width()//2, 40))
        
        # Desenhar áreas de espera e conclusão
        pygame.draw.rect(self.screen, (200, 200, 200, 128), (50, 350, 200, 150), 2)
        texto_espera = self.font.render("Fila de Espera", True, BLACK)
        self.screen.blit(texto_espera, (50, 330))
        
        pygame.draw.rect(self.screen, (200, 200, 200, 128), (SCREEN_WIDTH - 250, 350, 200, 150), 2)
        texto_concluido = self.font.render("Atendimento Concluído", True, BLACK)
        self.screen.blit(texto_concluido, (SCREEN_WIDTH - 250, 330))

        # Exibir valores esperados e registrados
        valor_registrado = sum(caixa.valor_total for caixa in self.caixas)
        texto_valor_esperado = self.font.render(f"Valor Esperado: R$ {self.valor_esperado_total:.2f}", True, BLACK)
        texto_valor_registrado = self.font.render(f"Valor Registrado: R$ {valor_registrado:.2f}", True, BLACK)
        texto_diferenca = self.font.render(f"Diferença: R$ {self.valor_esperado_total - valor_registrado:.2f}", True, RED if abs(self.valor_esperado_total - valor_registrado) > 0.01 else GREEN)
        
        self.screen.blit(texto_valor_esperado, (20, 80))
        self.screen.blit(texto_valor_registrado, (20, 100))
        self.screen.blit(texto_diferenca, (20, 120))

        # Exibir tempo decorrido
        if self.simulacao_iniciada and not self.simulacao_concluida:
            tempo_atual = time.time()
            tempo_decorrido = tempo_atual - self.tempo_inicio
            texto_tempo = self.font.render(f"Tempo: {tempo_decorrido:.1f}s", True, BLACK)
            self.screen.blit(texto_tempo, (SCREEN_WIDTH - 150, 80))
        
        # Se a simulação estiver concluída, mostrar tempo total
        if self.simulacao_concluida:
            tempo_total = self.tempo_fim - self.tempo_inicio
            texto_tempo_total = self.font.render(f"Tempo Total: {tempo_total:.1f}s", True, BLACK)
            self.screen.blit(texto_tempo_total, (SCREEN_WIDTH - 150, 80))
            
            # Desenhar botão para voltar ao menu
            pygame.draw.rect(self.screen, ORANGE, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 70, 200, 40))
            pygame.draw.rect(self.screen, BLACK, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 70, 200, 40), 2)
            texto_botao = self.font_grande.render("Voltar ao Menu", True, BLACK)
            self.screen.blit(texto_botao, (SCREEN_WIDTH//2 - texto_botao.get_width()//2, SCREEN_HEIGHT - 60))
            
            # Mensagem de conclusão
            texto_concluido = self.font_grande.render("Simulação Concluída!", True, GREEN)
            self.screen.blit(texto_concluido, (SCREEN_WIDTH//2 - texto_concluido.get_width()//2, SCREEN_HEIGHT - 100))

    def processar_cliente(self, cliente, caixa):
        """Função para processamento do cliente em uma thread separada"""
        # Movendo o cliente para o caixa
        cliente.estado = "atendimento"
        cliente.caixa_atendimento = caixa
        
        # Posicionar o cliente em frente ao caixa, mas deslocado para evitar sobreposição
        # com outros clientes que possam estar sendo atendidos simultaneamente (caso sem semáforo)
        if not self.com_semaforo:
            # Gerar um deslocamento lateral aleatório para evitar sobreposição
            deslocamento_x = random.randint(-30, 30)
        else:
            deslocamento_x = 0
            
        cliente.mover_para(caixa.x + caixa.largura//2 - cliente.tamanho//2 + deslocamento_x, 
                          caixa.y + caixa.altura + 5)
        
        # Esperar o cliente chegar ao caixa
        while cliente.x != cliente.destino_x or cliente.y != cliente.destino_y:
            time.sleep(0.05)
        
        # Simular o tempo de processamento
        caixa.estado = "ocupado"
        caixa.cliente_atual = cliente
        
        # Registrar o tempo de início
        cliente.tempo_inicio = time.time()
        
        # Simular o processamento de pagamento (reduzido para acelerar)
        time.sleep(1.0)  # Reduzido de 2.0 para 1.0
        
        # Atualizando o caixa
        # COM semáforo - operação protegida
        if self.com_semaforo:
            # Adquire o semáforo
            self.semaforo.acquire()
            try:
                # Registra o valor total corretamente
                valor_atual = caixa.valor_total
                time.sleep(0.3)  # Reduzido de 0.8 para 0.3
                caixa.valor_total += cliente.valor_compra
                
                # Animar moedas sendo pagas (reduzido para acelerar)
                for _ in range(3):  # Reduzido de 5 para 3 moedas
                    cliente.adicionar_moeda()
                    time.sleep(0.1)  # Reduzido de 0.3 para 0.1
            finally:
                # Libera o semáforo
                self.semaforo.release()
        # SEM semáforo - sujeito a condições de corrida
        else:
            # Leitura do valor atual
            valor_atual = caixa.valor_total
            
            # Animação de moedas sendo pagas (reduzido para acelerar)
            for _ in range(3):  # Reduzido de 5 para 3 moedas
                cliente.adicionar_moeda()
                time.sleep(0.1)  # Reduzido de 0.3 para 0.1
            
            # Pausa para aumentar chance de condição de corrida (reduzido para acelerar)
            time.sleep(0.3)  # Reduzido de 0.8 para 0.3
            
            # Cálculo e atribuição não atômicos
            novo_valor = valor_atual + cliente.valor_compra
            time.sleep(0.2)  # Reduzido de 0.4 para 0.2
            caixa.valor_total = novo_valor  # Possível perda de atualizações
        
        # Registrar o tempo de fim
        cliente.tempo_fim = time.time()
        
        # Tempo adicional antes de liberar o caixa (reduzido)
        time.sleep(0.5)  # Reduzido de 1.0 para 0.5
        
        # Liberar o caixa
        caixa.estado = "livre"
        caixa.cliente_atual = None
        caixa.clientes_atendidos += 1
        
        # Atualizar erro no valor (diferença entre o esperado e o registrado)
        soma_valores = sum(c.valor_compra for c in self.clientes if c.estado == "concluido" or c == cliente)
        caixa.erro_valor = soma_valores - caixa.valor_total
        
        # Movendo o cliente para a área de concluído
        cliente.estado = "concluido"
        pos_concluido_x = self.area_concluido_x + ((caixa.clientes_atendidos - 1) % 5) * 40
        pos_concluido_y = self.area_concluido_y + ((caixa.clientes_atendidos - 1) // 5) * 40
        cliente.mover_para(pos_concluido_x, pos_concluido_y)

    def verificar_proximo_cliente(self):
        """Verifica se há cliente na fila e caixa disponível"""
        # Se houver clientes na fila e o caixa estiver livre
        if self.fila_clientes and self.caixas[0].estado == "livre":
            # Verificar se o cliente já está posicionado na fila de espera
            # (Verifica se ele chegou aproximadamente ao seu destino)
            cliente = self.fila_clientes[0]
            distancia_x = abs(cliente.x - cliente.destino_x)
            distancia_y = abs(cliente.y - cliente.destino_y)
            
            # Só atende o cliente se ele já estiver posicionado na fila de espera
            if distancia_x < 5 and distancia_y < 5:
                # Obter o próximo cliente
                cliente = self.fila_clientes.pop(0)
                caixa = self.caixas[0]
                
                # Iniciar thread para processar o cliente
                threading.Thread(target=self.processar_cliente, args=(cliente, caixa)).start()

    def verificar_fim_simulacao(self):
        """Verifica se a simulação terminou"""
        if self.simulacao_iniciada and not self.fila_clientes and all(caixa.estado == "livre" for caixa in self.caixas):
            if not self.simulacao_concluida:
                self.simulacao_concluida = True
                self.tempo_fim = time.time()

    def posicionar_clientes_fila(self):
        """Posiciona os clientes na fila de espera com animação melhorada"""
        # Versão com semáforo - fila organizada
        if self.com_semaforo:
            for i, cliente in enumerate(self.fila_clientes):
                # Organizar em uma fila reta com pequeno offset
                offset = (i % 2) * 5  # Pequeno offset para visualização
                pos_x = self.area_espera_x + (i * 35)
                pos_y = self.area_espera_y + offset
                cliente.mover_para(pos_x, pos_y)
        # Versão sem semáforo - fila desorganizada
        else:
            for i, cliente in enumerate(self.fila_clientes):
                # Distribuição mais aleatória e caótica
                pos_x = self.area_espera_x + (i % 5) * 40 + random.randint(-5, 5)
                pos_y = self.area_espera_y + (i // 5) * 40 + random.randint(-5, 5)
                cliente.mover_para(pos_x, pos_y)

    def verificar_clique_botao(self, pos_mouse):
        """Verifica se houve clique no botão de voltar ao menu"""
        if self.simulacao_concluida:
            botao_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 70, 200, 40)
            if botao_rect.collidepoint(pos_mouse):
                self.voltar_ao_menu = True
                return True
        return False

    def executar(self):
        """Executa a simulação visual"""
        self.inicializar_pygame()
        
        # Loop principal
        rodando = True
        self.voltar_ao_menu = False
        
        while rodando:
            # Processar eventos
            for event in pygame.event.get():
                if event.type == QUIT:
                    rodando = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        rodando = False
                    elif event.key == K_SPACE and not self.simulacao_iniciada:
                        # Iniciar a simulação quando pressionar espaço
                        self.simulacao_iniciada = True
                        self.tempo_inicio = time.time()
                        self.criar_clientes()
                    elif event.key == K_RETURN and self.simulacao_concluida:
                        # Voltar ao menu com a tecla Enter quando concluído
                        self.voltar_ao_menu = True
                        rodando = False
                elif event.type == MOUSEBUTTONDOWN:
                    # Verificar clique no botão de voltar ao menu
                    if self.verificar_clique_botao(event.pos):
                        self.voltar_ao_menu = True
                        rodando = False
            
            # Limpar a tela
            self.screen.fill(WHITE)
            
            # Desenhar o ambiente
            self.desenhar_ambiente()
            
            # Atualizar e desenhar caixas
            for caixa in self.caixas:
                caixa.atualizar()
                caixa.desenhar(self.screen, self.font)
            
            # Se a simulação foi iniciada
            if self.simulacao_iniciada:
                # Verificar o próximo cliente
                self.verificar_proximo_cliente()
                
                # Verificar fim da simulação
                self.verificar_fim_simulacao()
                
                # Posicionar clientes na fila
                self.posicionar_clientes_fila()
                
                # Atualizar e desenhar cada cliente
                for cliente in self.clientes:
                    cliente.atualizar()
                    cliente.desenhar(self.screen, self.font)
            else:
                # Mostrar mensagem para iniciar
                texto_iniciar = self.font_grande.render("Pressione ESPAÇO para iniciar", True, BLACK)
                self.screen.blit(texto_iniciar, (SCREEN_WIDTH//2 - texto_iniciar.get_width()//2, SCREEN_HEIGHT//2))
            
            # Atualizar a tela
            pygame.display.flip()
            self.clock.tick(30)  # Reduzido de 60 para 30 FPS
        
        return self.voltar_ao_menu

# Criar menu de escolha
def menu_principal():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Menu - Simulação de Supermercado")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 24)
    font_titulo = pygame.font.SysFont('Arial', 36)
    
    # Opções
    opcoes = [
        "Simulação COM semáforo",
        "Simulação SEM semáforo",
        "Sair"
    ]
    
    opcao_selecionada = 0
    
    rodando = True
    while rodando:
        # Processar eventos
        for event in pygame.event.get():
            if event.type == QUIT:
                rodando = False
                return None
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    rodando = False
                    return None
                elif event.key == K_UP:
                    opcao_selecionada = (opcao_selecionada - 1) % len(opcoes)
                elif event.key == K_DOWN:
                    opcao_selecionada = (opcao_selecionada + 1) % len(opcoes)
                elif event.key == K_RETURN:
                    if opcao_selecionada == 0:
                        return True  # Com semáforo
                    elif opcao_selecionada == 1:
                        return False  # Sem semáforo
                    else:
                        return None  # Sair
            elif event.type == MOUSEBUTTONDOWN:
                # Verificar clique nos botões
                for i, opcao in enumerate(opcoes):
                    botao_rect = pygame.Rect(SCREEN_WIDTH//2 - 150, 220 + i * 60, 300, 40)
                    if botao_rect.collidepoint(event.pos):
                        if i == 0:
                            return True  # Com semáforo
                        elif i == 1:
                            return False  # Sem semáforo
                        else:
                            return None  # Sair
        
        # Limpar a tela
        screen.fill(LIGHT_BLUE)
        
        # Desenhar título
        titulo = font_titulo.render("SIMULAÇÃO DE SUPERMERCADO", True, BLACK)
        screen.blit(titulo, (SCREEN_WIDTH//2 - titulo.get_width()//2, 100))
        
        subtitulo = font.render("Escolha uma opção:", True, BLACK)
        screen.blit(subtitulo, (SCREEN_WIDTH//2 - subtitulo.get_width()//2, 160))
        
        # Desenhar botões
        for i, opcao in enumerate(opcoes):
            cor_botao = ORANGE if i == opcao_selecionada else DARK_GRAY
            pygame.draw.rect(screen, cor_botao, (SCREEN_WIDTH//2 - 150, 220 + i * 60, 300, 40))
            texto_opcao = font.render(opcao, True, BLACK)
            screen.blit(texto_opcao, (SCREEN_WIDTH//2 - texto_opcao.get_width()//2, 220 + i * 60 + 10))
        
        # Atualizar a tela
        pygame.display.flip()
        clock.tick(60)

# Executar o menu e a simulação
if __name__ == "__main__":
    executar_novamente = True
    
    while executar_novamente:
        # Mostrar menu de escolha
        escolha = menu_principal()
        
        # Executar a simulação escolhida
        if escolha is not None:
            simulacao = SimulacaoVisual(num_clientes=15, com_semaforo=escolha)
            voltar_ao_menu = simulacao.executar()
            executar_novamente = voltar_ao_menu
        else:
            executar_novamente = False
    
    # Garantir que o pygame seja encerrado
    pygame.quit()
    sys.exit()