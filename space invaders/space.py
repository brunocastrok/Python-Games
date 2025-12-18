import sys
import os
import time
import msvcrt
import random

# --- CÓDIGOS DE CORES ANSI ---
RESET = "\033[0m"
VERDE = "\033[32m"
VERMELHO = "\033[31m"
CIANO = "\033[36m"
AMARELO = "\033[33m"
BRANCO_BRILHANTE = "\033[97m"
AZUL = "\033[34m"

# --- CONFIGURAÇÕES E VARIÁVEIS GLOBAIS ---
LARGURA_JOGO = 80
ALTURA_JOGO = 24

jogador_x = LARGURA_JOGO // 2
jogador_y = ALTURA_JOGO - 2

tiros_jogador = []
tiros_inimigos = []
invasores = []
direcao_invasor = 1
contador_velocidade_invasor = 0
pontuacao = 0
fim_de_jogo = False
vitoria = False
vidas = 3

def inicializar_jogo():
    global invasores
    for linha in range(4):
        for coluna in range(10):
            x = 10 + coluna * 6
            y = 3 + linha * 2
            invasores.append([x, y])

def capturar_tecla():
    if msvcrt.kbhit():
        tecla = msvcrt.getch()
        if tecla == b'\xe0':
            tecla = msvcrt.getch()
            if tecla == b'K': return 'ESQUERDA'
            elif tecla == b'M': return 'DIREITA'
        elif tecla == b' ': return 'ATIRAR'
        elif tecla.lower() == b'q': return 'SAIR'
    return None

def processar_entrada(comando):
    global jogador_x
    if comando == 'ESQUERDA':
        jogador_x = max(1, jogador_x - 2)
    elif comando == 'DIREITA':
        jogador_x = min(LARGURA_JOGO - 4, jogador_x + 2)
    elif comando == 'ATIRAR':
        if len(tiros_jogador) < 3:
            tiros_jogador.append([jogador_x + 1, jogador_y - 1])

def atualizar_tiros():
    global fim_de_jogo, vidas
    for tiro in tiros_jogador[:]:
        tiro[1] -= 1
        if tiro[1] < 0:
            tiros_jogador.remove(tiro)
            
    for tiro in tiros_inimigos[:]:
        tiro[1] += 1
        if tiro[1] >= ALTURA_JOGO:
            tiros_inimigos.remove(tiro)
        elif (tiro[1] == jogador_y and 
            jogador_x <= tiro[0] <= jogador_x + 2):
            tiros_inimigos.remove(tiro)
            vidas -= 1
            if vidas <= 0:
                fim_de_jogo = True

def atualizar_invasores():
    global contador_velocidade_invasor, direcao_invasor, fim_de_jogo, vitoria
    if not invasores:
        vitoria = True
        return
    
    contador_velocidade_invasor += 1
    if contador_velocidade_invasor < 10:
        return
    
    contador_velocidade_invasor = 0
    mudar_direcao = False
    
    for inv in invasores:
        if (inv[0] <= 1 and direcao_invasor == -1) or \
            (inv[0] >= LARGURA_JOGO - 4 and direcao_invasor == 1):
            mudar_direcao = True
            break
            
    if mudar_direcao:
        for inv in invasores:
            inv[1] += 1
            if inv[1] >= jogador_y - 1:
                fim_de_jogo = True
        direcao_invasor *= -1
    else:
        for inv in invasores:
            inv[0] += direcao_invasor

def checar_colisoes():
    global pontuacao
    for tiro in tiros_jogador[:]:
        for inv in invasores[:]:
            if (tiro[1] == inv[1] and inv[0] <= tiro[0] <= inv[0] + 2):
                if tiro in tiros_jogador: tiros_jogador.remove(tiro)
                invasores.remove(inv)
                pontuacao += 10
                break

def inimigos_atiram():
    if invasores and random.random() < 0.05:
        inv = random.choice(invasores)
        tiros_inimigos.append([inv[0], inv[1] + 1])

def desenhar():
    # Usamos uma string única para evitar cintilação (flicker)
    output = '\033[H' # Cursor no topo
    
    # Borda Superior
    output += AZUL + "+" + "-" * LARGURA_JOGO + "+" + RESET + "\n"
    
    for y in range(ALTURA_JOGO):
        linha_char = [' '] * LARGURA_JOGO
        
        # Como cores ANSI ocupam espaço invisível na string, 
        # desenhamos os objetos um a um na linha finalizada.
        
        linha_finalizada = list(" " * LARGURA_JOGO)
        
        # Jogador (Ciano)
        if y == jogador_y:
            for i, char in enumerate('/A\\'):
                if 0 <= jogador_x + i < LARGURA_JOGO:
                    linha_finalizada[jogador_x + i] = CIANO + char + RESET
        
        # Invasores (Verde)
        for inv in invasores:
            if y == inv[1] and 0 <= inv[0] < LARGURA_JOGO - 2:
                for i, char in enumerate('<M>'):
                    linha_finalizada[inv[0] + i] = VERDE + char + RESET
                
        # Tiros Jogador (Amarelo)
        for tx, ty in tiros_jogador:
            if y == ty: linha_finalizada[tx] = AMARELO + "|" + RESET
            
        # Tiros Inimigos (Vermelho)
        for tx, ty in tiros_inimigos:
            if y == ty: linha_finalizada[tx] = VERMELHO + "!" + RESET
            
        output += AZUL + "|" + RESET + "".join(linha_finalizada) + AZUL + "|" + RESET + "\n"
        
    # Borda Inferior
    output += AZUL + "+" + "-" * LARGURA_JOGO + "+" + RESET + "\n"
    
    # HUD
    status = f"{BRANCO_BRILHANTE}Pontos: {AMARELO}{pontuacao}{RESET} | "
    status += f"{BRANCO_BRILHANTE}Vidas: {VERMELHO}{vidas}{RESET} | "
    status += f"{CIANO}SETAS: Mover | ESPAÇO: Atirar | Q: Sair{RESET}\n"
    output += status
    
    if fim_de_jogo: 
        output += f"\n{VERMELHO}*** FIM DE JOGO! OS INVASORES DOMINARAM! ***{RESET}\n"
    elif vitoria: 
        output += f"\n{VERDE}*** VITÓRIA! TERRA SALVA! ***{RESET}\n"
    
    sys.stdout.write(output)
    sys.stdout.flush()

def rodar_jogo():
    # Prepara o terminal
    if sys.platform == 'win32':
        os.system('color') # Ativa suporte ANSI no Windows
    os.system('cls' if os.name == 'nt' else 'clear')
    sys.stdout.write('\033[?25l') 
    inicializar_jogo()
    
    try:
        while not fim_de_jogo and not vitoria:
            comando = capturar_tecla()
            if comando == 'SAIR': break
            if comando: processar_entrada(comando)
            
            atualizar_tiros()
            atualizar_invasores()
            checar_colisoes()
            inimigos_atiram()
            desenhar()
            
            time.sleep(0.05)
        
        if fim_de_jogo or vitoria:
            time.sleep(2)
    finally:
        sys.stdout.write('\033[?25h')
        sys.stdout.flush()

if __name__ == '__main__':
    rodar_jogo()
