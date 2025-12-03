import curses #pip install windows-curses (Windows)
import random

# =============================================================================
# CONFIGURAÇÕES DO JOGO
# =============================================================================

# As 7 formas das peças do Tetris (1=bloco cheio, 0=vazio)
PECAS = [
    [[1, 1, 1, 1]],              # I: reta horizontal
    [[1, 1], [1, 1]],            # O: quadrado 2x2
    [[1, 1, 0], [0, 1, 1]],      # S: forma S
    [[0, 1, 1], [1, 1, 0]],      # Z: forma Z
    [[1, 1, 1], [0, 1, 0]],      # T: forma T
    [[1, 1, 1], [0, 0, 1]],      # J: forma J
    [[1, 1, 1], [1, 0, 0]]       # L: forma L
]

LARGURA = 10    # Colunas do tabuleiro
ALTURA = 20     # Linhas do tabuleiro
BLOCO = "█"     # Símbolo dos blocos
VAZIO = "·"     # Símbolo dos espaços vazios

# =============================================================================
# FUNÇÕES BÁSICAS
# =============================================================================

def colidir(tab, p, x, y):
    """Verifica se a peça colide com bordas ou peças fixas."""
    h, w = len(p), len(p[0])
    for i in range(h):
        for j in range(w):
            if p[i][j]:
                nx, ny = x + j, y + i
                if nx < 0 or nx >= LARGURA or ny >= ALTURA:
                    return True
                if ny >= 0 and tab[ny][nx] > 0:
                    return True
    return False

def colocar(tab, p, x, y, id_cor):
    """Fixar peça no tabuleiro permanentemente."""
    h, w = len(p), len(p[0])
    for i in range(h):
        for j in range(w):
            if p[i][j]:
                ny, nx = y + i, x + j
                if 0 <= ny < ALTURA and 0 <= nx < LARGURA:
                    tab[ny][nx] = id_cor

def limpar_linhas(tab):
    """Remove linhas completamente preenchidas e desce as de cima."""
    nova_tab = []
    for linha in tab:
        if all(cell > 0 for cell in linha):  # Linha cheia?
            continue  # Remove linha cheia
        nova_tab.append(linha)
    
    # Adiciona linhas vazias no topo
    while len(nova_tab) < ALTURA:
        nova_tab.insert(0, [0] * LARGURA)
    
    return nova_tab

def desenhar(stdscr, tab, peca, x, y, id_cor):
    """Desenha tabuleiro, peça caindo e borda."""
    try:
        stdscr.clear()
        h_tela, w_tela = stdscr.getmaxyx()
        
        # Tabuleiro fixo
        for i in range(min(ALTURA, h_tela - 2)):
            for j in range(min(LARGURA, w_tela)):
                cell_id = tab[i][j]
                stdscr.addstr(i, j, BLOCO if cell_id > 0 else VAZIO, 
                            curses.color_pair(cell_id or 8))
        
        # Peça caindo (em negrito)
        if peca:
            h, w = len(peca), len(peca[0])
            for i in range(h):
                for j in range(w):
                    if peca[i][j]:
                        ny, nx = y + i, x + j
                        if 0 <= ny < h_tela - 2 and 0 <= nx < w_tela:
                            stdscr.addstr(ny, nx, BLOCO, 
                                        curses.color_pair(id_cor) | curses.A_BOLD)
        
        # Borda direita
        for i in range(min(ALTURA, h_tela - 2)):
            stdscr.addstr(i, LARGURA + 1, "|", curses.color_pair(8))
        
        stdscr.refresh()
    except curses.error:
        pass

def get_nova_peca():
    """Retorna peça aleatória e sua cor."""
    idx = random.randint(0, len(PECAS) - 1)
    return PECAS[idx], idx + 1

# =============================================================================
# JOGO PRINCIPAL
# =============================================================================

def main(stdscr):
    # Configura cores
    curses.start_color()
    curses.use_default_colors()
    cores = [
        curses.COLOR_CYAN, curses.COLOR_YELLOW, curses.COLOR_GREEN,
        curses.COLOR_RED, curses.COLOR_MAGENTA, curses.COLOR_BLUE, 
        curses.COLOR_WHITE
    ]
    for i, cor in enumerate(cores, 1):
        curses.init_pair(i, cor, -1)
    curses.init_pair(8, curses.COLOR_WHITE, -1)  # Vazio/borda
    
    # Configura terminal
    curses.curs_set(0)
    curses.noecho()
    stdscr.nodelay(1)
    stdscr.timeout(250)  # Velocidade fixa
    
    # Inicia jogo
    tab = [[0] * LARGURA for _ in range(ALTURA)]
    peca, id_cor = get_nova_peca()
    x, y = LARGURA // 2 - 2, 0
    
    while True:
        desenhar(stdscr, tab, peca, x, y, id_cor)
        
        # Controles
        k = stdscr.getch()
        if k == ord('q'):
            break
        elif k == curses.KEY_LEFT and not colidir(tab, peca, x - 1, y):
            x -= 1
        elif k == curses.KEY_RIGHT and not colidir(tab, peca, x + 1, y):
            x += 1
        elif k == curses.KEY_DOWN and not colidir(tab, peca, x, y + 1):
            y += 1
        elif k == curses.KEY_UP:
            nova = [list(reversed(col)) for col in zip(*peca)]
            if not colidir(tab, nova, x, y):
                peca = nova
        elif k == ord(' '):  # Hard drop
            while not colidir(tab, peca, x, y + 1):
                y += 1
        
        # Queda automática
        if not colidir(tab, peca, x, y + 1):
            y += 1
        else:
            # Fixa peça
            colocar(tab, peca, x, y, id_cor)
            
            # ✅ LIMPA LINHAS COMPLETAS
            tab = limpar_linhas(tab)
            
            # Nova peça
            peca, id_cor = get_nova_peca()
            x, y = LARGURA // 2 - 2, 0
            
            # Game Over
            if colidir(tab, peca, x, y):
                h_tela, _ = stdscr.getmaxyx()
                try:
                    msg = " GAME OVER! "
                    stdscr.addstr(h_tela // 2, LARGURA // 2 - len(msg)//2, 
                                msg, curses.A_REVERSE | curses.color_pair(4))
                    stdscr.refresh()
                    stdscr.getch()
                except curses.error:
                    pass
                break

if __name__ == "__main__":
    curses.wrapper(main)
