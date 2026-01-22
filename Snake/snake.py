import os
import time
import msvcrt
import random

# Códigos ANSI para cores (usados para colorir o texto no terminal)
REINICIAR = "\033[0m"
VERDE = "\033[32m"  # Para a cobra
AMARELO = "\033[33m"  # Para o item
BRANCO = "\033[37m"  # Para a borda

# Dimensões do tabuleiro (área interna, sem as bordas)
LARGURA = 30
ALTURA = 15

# Caracteres usados no jogo
CARACTER_COBRA = '⬮'  # Representa a cobra
CARACTER_ITEM = '✰'  # Representa o item que a cobra coleta

# Caracteres para desenhar as bordas do tabuleiro
CANTO_SUPERIOR_ESQUERDO = '╭'
CANTO_SUPERIOR_DIREITO = '╮'
CANTO_INFERIOR_ESQUERDO = '╰'
CANTO_INFERIOR_DIREITO = '╯'
HORIZONTAL = '─'  # Linha horizontal
VERTICAL = '│'    # Linha vertical

# Direções possíveis para o movimento da cobra
CIMA = (0, -1)    # Move para cima
BAIXO = (0, 1)    # Move para baixo
ESQUERDA = (-1, 0)  # Move para a esquerda
DIREITA = (1, 0)   # Move para a direita

def limpar_tela():
    """
    Esta função limpa a tela do terminal e move o cursor para o topo esquerdo.
    Isso evita que a tela pisque ao atualizar o jogo.
    """
    print("\033[2J\033[H", end='')

def desenhar_tabuleiro(cobra, item, pontuacao):
    """
    Esta função constrói e desenha o tabuleiro do jogo no terminal.
    - cobra: lista de posições da cobra
    - item: posição do item a ser coletado
    - pontuacao: pontos atuais do jogador
    """
    # Cria uma lista de linhas para o tabuleiro
    linhas = []
    
    # Borda superior
    superior = BRANCO + CANTO_SUPERIOR_ESQUERDO + HORIZONTAL * LARGURA + CANTO_SUPERIOR_DIREITO + REINICIAR
    linhas.append(superior)
    
    # Linhas do meio (o tabuleiro em si)
    for y in range(ALTURA):
        linha = BRANCO + VERTICAL + REINICIAR
        for x in range(LARGURA):
            if (x, y) in cobra:
                linha += VERDE + CARACTER_COBRA + REINICIAR  # Desenha parte da cobra
            elif (x, y) == item:
                linha += AMARELO + CARACTER_ITEM + REINICIAR  # Desenha o item
            else:
                linha += ' '  # Espaço vazio
        linha += BRANCO + VERTICAL + REINICIAR
        linhas.append(linha)
    
    # Borda inferior
    inferior = BRANCO + CANTO_INFERIOR_ESQUERDO + HORIZONTAL * LARGURA + CANTO_INFERIOR_DIREITO + REINICIAR
    linhas.append(inferior)
    
    # Mostra a pontuação abaixo do tabuleiro
    linhas.append(f"Pontuação: {pontuacao}")
    
    # Imprime todas as linhas de uma vez para atualizar a tela suavemente
    print('\n'.join(linhas), end='')

def obter_entrada(direcao_atual):
    """
    Esta função verifica se o jogador pressionou uma tecla e atualiza a direção da cobra.
    - direcao_atual: direção atual da cobra
    Retorna a nova direção ou a atual se nada for pressionado.
    Suporta tanto WASD quanto setas do teclado.
    """
    if msvcrt.kbhit():
        tecla = msvcrt.getch()
        if tecla == b'\xe0':  # Prefixo para teclas de seta
            tecla = msvcrt.getch()  # Pega o segundo byte
            if tecla == b'H' and direcao_atual != BAIXO:  # Seta para cima
                return CIMA
            elif tecla == b'P' and direcao_atual != CIMA:  # Seta para baixo
                return BAIXO
            elif tecla == b'K' and direcao_atual != DIREITA:  # Seta para esquerda
                return ESQUERDA
            elif tecla == b'M' and direcao_atual != ESQUERDA:  # Seta para direita
                return DIREITA
        else:
            if tecla == b'w' and direcao_atual != BAIXO:
                return CIMA
            elif tecla == b's' and direcao_atual != CIMA:
                return BAIXO
            elif tecla == b'a' and direcao_atual != DIREITA:
                return ESQUERDA
            elif tecla == b'd' and direcao_atual != ESQUERDA:
                return DIREITA
    return direcao_atual

def principal():
    """
    Esta é a função principal do jogo. Ela inicia o jogo, controla o loop principal
    e gerencia o movimento da cobra, colisões e pontuação.
    """
    # Posição inicial da cobra: uma lista de tuplas (x, y), com a cabeça no índice 0
    cobra = [(LARGURA // 2, ALTURA // 2)]
    direcao = DIREITA  # Direção inicial: para a direita
    item = (random.randint(0, LARGURA-1), random.randint(0, ALTURA-1))  # Posição aleatória do item
    pontuacao = 0  # Pontuação inicial
    jogo_terminado = False  # Flag para indicar se o jogo acabou
    
    # Ativa códigos ANSI no Windows, se necessário
    os.system('')  # Isso habilita cores no terminal do Windows
    
    limpar_tela()  # Limpa a tela antes de começar
    
    while not jogo_terminado:
        # Desenha o estado atual do jogo
        desenhar_tabuleiro(cobra, item, pontuacao)
        
        # Pausa breve para controlar a velocidade do jogo (0.1 segundos por movimento)
        time.sleep(0.1)
        
        # Obtém a nova direção baseada na entrada do jogador
        direcao = obter_entrada(direcao)
        
        # Calcula a nova posição da cabeça da cobra
        cabeca_x, cabeca_y = cobra[0]
        dx, dy = direcao
        nova_cabeca = (cabeca_x + dx, cabeca_y + dy)
        
        # Verifica colisões: com bordas ou com o próprio corpo
        if (nova_cabeca[0] < 0 or nova_cabeca[0] >= LARGURA or
            nova_cabeca[1] < 0 or nova_cabeca[1] >= ALTURA or
            nova_cabeca in cobra):
            jogo_terminado = True  # Termina o jogo se houver colisão
            continue
        
        # Adiciona a nova cabeça à cobra
        cobra.insert(0, nova_cabeca)
        
        # Verifica se a cobra comeu o item
        if nova_cabeca == item:
            pontuacao += 1  # Aumenta a pontuação
            # Gera um novo item em uma posição aleatória não ocupada pela cobra
            while True:
                item = (random.randint(0, LARGURA-1), random.randint(0, ALTURA-1))
                if item not in cobra:
                    break
        else:
            # Remove a cauda da cobra (ela não cresce se não comeu)
            cobra.pop()
        
        # Limpa a tela para o próximo quadro
        limpar_tela()
    
    # Mensagem final quando o jogo termina
    print("Jogo Terminado! Pontuação Final:", pontuacao)

if __name__ == "__main__":
    principal()
