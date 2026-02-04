import os
import time
import msvcrt
import random

# --- CONFIGURAÇÕES DO AMBIENTE ---
LARGURA = 60
ALTURA = 20
PADDLE_TAMANHO = 10
FPS = 0.05

# --- CARACTERES DE DESENHO ---
CANTO_SUP_ESQ, CANTO_SUP_DIR = '╭', '╮'
CANTO_INF_ESQ, CANTO_INF_DIR = '╰', '╯'
HORIZONTAL, VERTICAL = '─', '│'
BLOCO, BOLA, PADDLE_CHAR = '█', '●', '═'

# --- CORES ANSI ---
RESET = "\033[0m"
COR_BORDA = "\033[94m"   
COR_PADDLE = "\033[92m"  
COR_BOLA = "\033[93m"    
COR_TIJOLO = "\033[91m"  

# --- ESTADO DO JOGO ---
# pos_x e pos_y definem onde a bola está no plano cartesiano do terminal
pos_x, pos_y = float(LARGURA // 2), float(ALTURA - 4)

# AJUSTE DE MOVIMENTO:
# No terminal, um caractere é aproximadamente 2x mais alto que largo.
# Para evitar o zigue-zague, vel_x deve ser maior que vel_y.
vel_x, vel_y = 0.8, -0.4 

paddle_x = (LARGURA - PADDLE_TAMANHO) // 2
score = 0
game_over = False

# --- CRIAÇÃO DOS TIJOLOS ---
tijolos = []
# Geramos 50 tijolos distribuídos em 5 fileiras de 10
for y in range(2, 7):
    for x in range(5, LARGURA - 5, 5):
        tijolos.append([x, y])

def desenhar_tela():
    """
    Constrói o quadro atual do jogo. O uso do buffer (string 'output')
    garante que a atualização seja instantânea e sem saltos visuais.
    """
    output = "\033[H" 
    output += COR_BORDA + CANTO_SUP_ESQ + (HORIZONTAL * LARGURA) + CANTO_SUP_DIR + RESET + "\n"
    
    for y in range(ALTURA):
        line = COR_BORDA + VERTICAL + RESET
        row_chars = [" "] * LARGURA
        
        # Posicionamento da raquete (Paddle)
        if y == ALTURA - 1:
            for i in range(PADDLE_TAMANHO):
                if 0 <= paddle_x + i < LARGURA:
                    row_chars[paddle_x + i] = COR_PADDLE + PADDLE_CHAR + RESET
        
        # Posicionamento dos tijolos remanescentes
        for t in tijolos:
            if t[1] == y:
                # O tijolo ocupa 3 espaços para facilitar a colisão visual
                for offset in range(3):
                    if 0 <= t[0] + offset < LARGURA:
                        row_chars[t[0] + offset] = COR_TIJOLO + BLOCO + RESET
        
        # Posicionamento da bola (converte float para int para renderizar no caractere)
        bx, by = int(pos_x), int(pos_y)
        if by == y and 0 <= bx < LARGURA:
            row_chars[bx] = COR_BOLA + BOLA + RESET

        line += "".join(row_chars)
        output += line + COR_BORDA + VERTICAL + RESET + "\n"

    output += COR_BORDA + CANTO_INF_ESQ + (HORIZONTAL * LARGURA) + CANTO_INF_DIR + RESET + "\n"
    output += f" Pontuação: {score} | Tijolos: {len(tijolos)} | 'Q' para Sair"
    print(output)

# Prepara o terminal: esconde o cursor e limpa a tela
print("\033[?25l", end="")
os.system('cls' if os.name == 'nt' else 'clear')

try:
    while not game_over:
        # 1. CONTROLE DO JOGADOR
        if msvcrt.kbhit():
            tecla = msvcrt.getch()
            if tecla == b'\xe0': 
                tecla = msvcrt.getch()
                # Aumentamos o passo do paddle para acompanhar a nova largura
                if tecla == b'K' and paddle_x > 1: paddle_x -= 3
                elif tecla == b'M' and paddle_x < LARGURA - PADDLE_TAMANHO - 1: paddle_x += 3
            elif tecla.lower() == b'q':
                break

        # 2. LÓGICA DE MOVIMENTO
        # A bola se move suavemente usando valores decimais
        pos_x += vel_x
        pos_y += vel_y

        # 3. COLISÕES COM BORDAS
        # Rebate nas paredes laterais
        if pos_x <= 0 or pos_x >= LARGURA - 1:
            vel_x *= -1
            pos_x = max(0, min(pos_x, LARGURA - 1)) # Corrige posição para não prender na borda

        # Rebate no teto
        if pos_y <= 0:
            vel_y *= -1
            pos_y = 0

        # 4. COLISÃO COM A RAQUETE (FÍSICA DINÂMICA)
        # Se a posição arredondada da bola atingir a linha da raquete
        if int(pos_y) == ALTURA - 1:
            if paddle_x <= int(pos_x) < paddle_x + PADDLE_TAMANHO:
                # Inverte a direção vertical
                vel_y = -abs(vel_y)
                
                # Altera o ângulo horizontal baseado em ONDE a bola bateu na raquete
                # Bater nas pontas faz a bola sair mais inclinada
                centro = paddle_x + (PADDLE_TAMANHO / 2)
                impacto = (pos_x - centro) / (PADDLE_TAMANHO / 2)
                vel_x = impacto * 1.2 # O impacto define a nova direção X

        # 5. COLISÃO COM OS TIJOLOS
        for t in tijolos:
            if int(pos_y) == t[1] and t[0] <= int(pos_x) <= t[0] + 2:
                tijolos.remove(t)
                vel_y *= -1
                score += 10
                break

        # 6. FIM DE JOGO
        if pos_y >= ALTURA:
            game_over = True
        
        if not tijolos:
            desenhar_tela()
            print("\n VITORIA! VOCÊ DESTRUIU TODOS OS TIJOLOS!")
            break

        # 7. RENDERIZAÇÃO
        desenhar_tela()
        time.sleep(FPS)

finally:
    # Restaura o cursor para o usuário
    print("\033[?25h")

if game_over:
    print(f"\n FIM DE JOGO! Pontuação: {score}")
