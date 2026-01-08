import os
import sys
import time
import msvcrt
import random

# --- CONFIGURAÇÕES DE CORES E ANSI ---
RESET = '\033[0m'
BOLD = '\033[1m'
HIDDEN_CURSOR = '\033[?25l'
SHOW_CURSOR = '\033[?25h'
MOVE_HOME = '\033[H'

# Cores
C_BACK = '\033[36m'   # Ciano (verso)
C_FRONT = '\033[32m'  # Verde (frente)
C_SEL = '\033[33m'    # Amarelo (seleção)
C_BONUS = '\033[35m'  # Roxo (carta bônus)

# Caracteres da borda
C_TL, C_H, C_TR = '╭', '─', '╮'
C_V             = '│'
C_BL, C_H, C_BR = '╰', '─', '╯'

def configurar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
    sys.stdout.write(HIDDEN_CURSOR)

def restaurar_terminal():
    sys.stdout.write(RESET + SHOW_CURSOR)
    os.system('cls' if os.name == 'nt' else 'clear')

def criar_baralho():
    """Cria 4 pares + 1 carta bônus (Total 9)."""
    simbolos = ['A', 'B', 'C', 'D']
    baralho = (simbolos * 2) + ['★']
    random.shuffle(baralho)
    return baralho

def obter_entrada():
    """Lê teclas sem bloquear."""
    key = msvcrt.getch()
    if key == b'\xe0': 
        key = msvcrt.getch()
        if key == b'H': return 'up'
        if key == b'P': return 'down'
        if key == b'K': return 'left'
        if key == b'M': return 'right'
    elif key == b'\r' or key == b' ':
        return 'enter'
    elif key == b'\x1b':
        return 'esc'
    return None

def desenhar_carta(simbolo, estado, selecionado):
    """
    estado: 0=escondido, 1=revelado temp, 2=resolvido
    """
    cor_borda = C_SEL if selecionado else C_BACK
    cor_conteudo = C_BACK
    conteudo = "?" 
    
    if estado > 0: # Revelado ou Resolvido
        cor_borda = C_SEL if selecionado else C_FRONT
        cor_conteudo = C_FRONT
        conteudo = simbolo
        
        # Cor especial se for a carta bônus
        if simbolo == '★':
            cor_conteudo = C_BONUS
            if not selecionado: cor_borda = C_BONUS

    # Montagem gráfica
    topo = f"{cor_borda}{C_TL}{C_H*3}{C_TR}{RESET}"
    meio = f"{cor_borda}{C_V} {cor_conteudo}{BOLD}{conteudo}{RESET}{cor_borda} {C_V}{RESET}"
    base = f"{cor_borda}{C_BL}{C_H*3}{C_BR}{RESET}"
    
    return [topo, meio, base]

def renderizar_jogo(baralho, estados, cursor_pos, largura_grid=3, mensagem=""):
    buffer = [MOVE_HOME] 
    buffer.append(f"{BOLD}--- JOGO DA MEMÓRIA (3x3) ---{RESET}\n")
    buffer.append("Encontre os pares e a carta bônus (★).\n\n")

    for y in range(0, len(baralho), largura_grid):
        linha_cartas = baralho[y : y + largura_grid]
        linhas_visuais = ["", "", ""] 
        
        for x, carta in enumerate(linha_cartas):
            idx_real = y + x
            eh_selecionado = (idx_real == cursor_pos)
            estado_atual = estados[idx_real]
            
            desenho = desenhar_carta(carta, estado_atual, eh_selecionado)
            
            espaco = "  "
            linhas_visuais[0] += desenho[0] + espaco
            linhas_visuais[1] += desenho[1] + espaco
            linhas_visuais[2] += desenho[2] + espaco
        
        buffer.append(linhas_visuais[0] + "\n")
        buffer.append(linhas_visuais[1] + "\n")
        buffer.append(linhas_visuais[2] + "\n")
        buffer.append("\n") 

    buffer.append(f"{C_SEL}{mensagem}{RESET}          ")
    
    sys.stdout.write("".join(buffer))
    sys.stdout.flush()

def main():
    configurar_terminal()
    
    baralho = criar_baralho()
    total_cartas = 9
    colunas = 3
    
    estados = [0] * total_cartas 
    cursor = 0
    selecoes = [] 
    mensagem = ""

    executando = True
    
    try:
        while executando:
            renderizar_jogo(baralho, estados, cursor, colunas, mensagem)
            mensagem = "" 

            # Venceu?
            if estados.count(2) == total_cartas:
                renderizar_jogo(baralho, estados, cursor, colunas, "PARABÉNS! JOGO COMPLETO!")
                time.sleep(3)
                executando = False
                continue

            # Lógica de par
            if len(selecoes) == 2:
                idx1, idx2 = selecoes
                if baralho[idx1] == baralho[idx2]:
                    estados[idx1] = 2
                    estados[idx2] = 2
                    mensagem = f"PAR ENCONTRADO! ({baralho[idx1]})"
                    renderizar_jogo(baralho, estados, cursor, colunas, mensagem)
                    time.sleep(0.5)
                else:
                    mensagem = "NÃO É PAR..."
                    renderizar_jogo(baralho, estados, cursor, colunas, mensagem)
                    time.sleep(1)
                    estados[idx1] = 0
                    estados[idx2] = 0
                
                selecoes = []

            acao = obter_entrada()
            
            if acao == 'esc':
                executando = False
            
            # --- NAVEGAÇÃO ---
            elif acao == 'right':
                cursor = (cursor + 1) % total_cartas
            elif acao == 'left':
                cursor = (cursor - 1) % total_cartas
            elif acao == 'down':
                cursor = (cursor + colunas) % total_cartas
            elif acao == 'up':
                cursor = (cursor - colunas) % total_cartas
            
            elif acao == 'enter':
                if estados[cursor] == 0 and len(selecoes) < 2:
                    if baralho[cursor] == '★':
                        estados[cursor] = 2 # Bônus
                        mensagem = "BÔNUS ENCONTRADO!"
                    else:
                        estados[cursor] = 1 
                        selecoes.append(cursor)

    except KeyboardInterrupt:
        pass
    finally:
        restaurar_terminal()
        print("Jogo encerrado.")

if __name__ == "__main__":
    main()
