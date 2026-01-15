import curses  # Biblioteca para controlar o terminal
import random  # Biblioteca para sortear as letras
import time    # Para controlar o cronômetro

# --- CONFIGURAÇÕES DO JOGO ---
LINHAS = 5
COLUNAS = 5
PECAS = ['A', 'B', 'C', 'D', 'E', 'F']
TEMPO_TOTAL = 60  # Tempo em segundos para o jogo

def criar_tabuleiro():
    """Cria a matriz 5x5 preenchida com letras aleatórias."""
    tabuleiro = []
    for linha in range(LINHAS):
        nova_linha = []
        for coluna in range(COLUNAS):
            letra = random.choice(PECAS)
            nova_linha.append(letra)
        tabuleiro.append(nova_linha)
    return tabuleiro

def desenhar_tabuleiro(stdscr, tabuleiro, cursor_x, cursor_y, selecionado, pontos, tempo_restante):
    """Desenha o jogo, pontuação e tempo."""
    stdscr.clear()

    # --- CABEÇALHO (HUD) ---
    # Muda a cor do tempo se estiver acabando (menos de 10s)
    cor_tempo = curses.color_pair(0)
    if tempo_restante <= 10:
        cor_tempo = curses.color_pair(1) | curses.A_BOLD # Vermelho e negrito

    stdscr.addstr(0, 0, f" PONTOS: {pontos:04d}   TEMPO: {int(tempo_restante):02d}s", curses.A_BOLD)
    stdscr.addstr(1, 0, " Setas: Mover | Enter: Selecionar | Q: Sair")
    
    # Barra de tempo visual
    barra_tam = int((tempo_restante / TEMPO_TOTAL) * 20)
    stdscr.addstr(0, 35, "[" + "#"*barra_tam + "."*(20-barra_tam) + "]", cor_tempo)

    offset_y = 3 # Empurra o tabuleiro para baixo por causa do HUD

    for y in range(LINHAS):
        for x in range(COLUNAS):
            letra = tabuleiro[y][x]
            
            # --- DEFININDO AS CORES ---
            try:
                cor_index = PECAS.index(letra) + 1
            except ValueError:
                cor_index = 0
            
            if letra is None:
                cor = curses.color_pair(0)
                letra = " "
            else:
                cor = curses.color_pair(cor_index)

            if x == cursor_x and y == cursor_y:
                cor = cor | curses.A_REVERSE
            if selecionado == (x, y):
                cor = cor | curses.A_BOLD

            # --- DESENHANDO A "MOLDURA" ---
            pos_y_tela = (y * 3) + offset_y
            pos_x_tela = (x * 6) + 2

            try:
                stdscr.addstr(pos_y_tela,     pos_x_tela, "╭───╮", cor)
                stdscr.addstr(pos_y_tela + 1, pos_x_tela, f"│ {letra} │", cor)
                stdscr.addstr(pos_y_tela + 2, pos_x_tela, "╰───╯", cor)
            except curses.error:
                pass

    stdscr.refresh()

def trocar_pecas(tabuleiro, x1, y1, x2, y2):
    temp = tabuleiro[y1][x1]
    tabuleiro[y1][x1] = tabuleiro[y2][x2]
    tabuleiro[y2][x2] = temp

def verificar_matches(tabuleiro):
    para_remover = set()
    # 1. Verificar Linhas
    for y in range(LINHAS):
        for x in range(COLUNAS - 2):
            val1 = tabuleiro[y][x]
            val2 = tabuleiro[y][x+1]
            val3 = tabuleiro[y][x+2]
            if val1 and val1 == val2 == val3:
                para_remover.add((x, y))
                para_remover.add((x+1, y))
                para_remover.add((x+2, y))

    # 2. Verificar Colunas
    for x in range(COLUNAS):
        for y in range(LINHAS - 2):
            val1 = tabuleiro[y][x]
            val2 = tabuleiro[y+1][x]
            val3 = tabuleiro[y+2][x]
            if val1 and val1 == val2 == val3:
                para_remover.add((x, y))
                para_remover.add((x, y+1))
                para_remover.add((x, y+2))
    return para_remover

def aplicar_gravidade(tabuleiro, para_remover):
    if not para_remover: return False
    for (x, y) in para_remover:
        tabuleiro[y][x] = None

    for x in range(COLUNAS):
        pecas_vivas = []
        for y in range(LINHAS):
            if tabuleiro[y][x] is not None:
                pecas_vivas.append(tabuleiro[y][x])
        
        faltam = LINHAS - len(pecas_vivas)
        novas = []
        for _ in range(faltam):
            novas.append(random.choice(PECAS))
        
        nova_coluna = novas + pecas_vivas
        for y in range(LINHAS):
            tabuleiro[y][x] = nova_coluna[y]
    return True

def mostrar_game_over(stdscr, pontos):
    """Tela final de jogo."""
    stdscr.clear()
    altura, largura = stdscr.getmaxyx()
    msg1 = "FIM DE JOGO!"
    msg2 = f"Pontuação Final: {pontos}"
    msg3 = "Pressione Q para sair"
    
    stdscr.addstr(altura//2 - 2, (largura - len(msg1))//2, msg1, curses.A_BOLD | curses.color_pair(1))
    stdscr.addstr(altura//2,     (largura - len(msg2))//2, msg2)
    stdscr.addstr(altura//2 + 2, (largura - len(msg3))//2, msg3)
    stdscr.refresh()
    
    # Bloqueia até a pessoa apertar Q
    stdscr.nodelay(False) 
    while True:
        key = stdscr.getch()
        if key == ord('q') or key == ord('Q'):
            break

def jogo_principal(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    
    # Cores
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED, -1)
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.init_pair(3, curses.COLOR_YELLOW, -1)
    curses.init_pair(4, curses.COLOR_BLUE, -1)
    curses.init_pair(5, curses.COLOR_MAGENTA, -1)
    curses.init_pair(6, curses.COLOR_CYAN, -1)

    # Variáveis de Estado
    tabuleiro = criar_tabuleiro()
    cursor_x, cursor_y = 0, 0
    selecionado = None 
    pontos = 0
    
    # Variáveis de Tempo
    inicio_jogo = time.time()
    tempo_pausa_acumulado = 0  # Para descontar o tempo das animações
    
    # Configura input não-bloqueante com timeout
    # O getch() vai esperar 100ms. Se nada for digitado, retorna -1 e o loop segue.
    # Isso permite que o relógio atualize mesmo se o jogador não mexer.
    stdscr.timeout(100) 

    while True:
        # 1. Cálculo do Tempo
        tempo_atual = time.time()
        tempo_decorrido = tempo_atual - inicio_jogo - tempo_pausa_acumulado
        tempo_restante = TEMPO_TOTAL - tempo_decorrido

        # 2. Verifica Game Over
        if tempo_restante <= 0:
            mostrar_game_over(stdscr, pontos)
            break

        # 3. Desenha
        desenhar_tabuleiro(stdscr, tabuleiro, cursor_x, cursor_y, selecionado, pontos, tempo_restante)

        # 4. Lógica de Matches
        matches = verificar_matches(tabuleiro)
        if matches:
            # Pontuação: 10 pontos por bloco quebrado
            pontos += len(matches) * 10
            
            desenhar_tabuleiro(stdscr, tabuleiro, cursor_x, cursor_y, selecionado, pontos, tempo_restante)
            curses.napms(300) 
            # Como paramos o jogo por 300ms, adicionamos isso ao acumulado 
            # para o relógio não punir o jogador pela animação
            tempo_pausa_acumulado += 0.3 
            
            aplicar_gravidade(tabuleiro, matches)
            continue 

        # 5. Controles
        tecla = stdscr.getch()

        if tecla == -1: # Timeout (nenhuma tecla pressionada)
            continue

        if tecla == ord('q'):
            break
        elif tecla == curses.KEY_RIGHT:
            if cursor_x < COLUNAS - 1: cursor_x += 1
        elif tecla == curses.KEY_LEFT:
            if cursor_x > 0: cursor_x -= 1
        elif tecla == curses.KEY_DOWN:
            if cursor_y < LINHAS - 1: cursor_y += 1
        elif tecla == curses.KEY_UP:
            if cursor_y > 0: cursor_y -= 1
        
        elif tecla == ord('\n') or tecla == ord(' '):
            if selecionado is None:
                selecionado = (cursor_x, cursor_y)
            else:
                sel_x, sel_y = selecionado
                distancia = abs(sel_x - cursor_x) + abs(sel_y - cursor_y)
                
                if distancia == 1:
                    trocar_pecas(tabuleiro, cursor_x, cursor_y, sel_x, sel_y)
                    
                    # Desenha logo após a troca para dar feedback visual
                    desenhar_tabuleiro(stdscr, tabuleiro, cursor_x, cursor_y, selecionado, pontos, tempo_restante)
                    curses.napms(100) # Pequena pausa para ver a troca
                    tempo_pausa_acumulado += 0.1

                    if not verificar_matches(tabuleiro):
                        trocar_pecas(tabuleiro, cursor_x, cursor_y, sel_x, sel_y) # Desfaz
                    else:
                        # Se fez match, o loop reinicia e cai no bloco "if matches" lá em cima
                        pass
                    
                    selecionado = None
                else:
                    selecionado = (cursor_x, cursor_y)

if __name__ == "__main__":
    try:
        curses.wrapper(jogo_principal)
    except Exception as e:
        print(f"Erro: {e}")
