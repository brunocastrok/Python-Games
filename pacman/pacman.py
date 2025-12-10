import os
import time
import msvcrt
import random

# Configuração para suportar cores
os.system('')

# --- CORES E CARACTERES ---
COR_AMARELO = '\033[93m'
COR_AZUL = '\033[94m'
COR_VERMELHO = '\033[91m'
COR_RESET = '\033[0m'

PACMAN_SPRITES = {'d': 'ᗧ', 'a': 'ᗤ', 'w': 'ᗢ', 's': 'ᗣ'}
FANTASMA_SPRITE = '⍾'
PASTILHA = '·'
VAZIO = ' ' 

MAPA_ORIGINAL = r"""
╭──────────────╮ ╭───────────────────╮ ╭──────────────╮
│ ************ │ │ ***************** │ │ ************ │
│ * ╭──────╮ * │ │ * ╭───────────╮ * │ │ * ╭──────╮ * │
│ * │ ╭────╯ * ╰─╯ * ╰───────────╯ * ╰─╯ * ╰────╮ │ * │
│ * │ │ *************************************** │ │ * │
│ * ╰─╯ * ╭╮ * ╭─╮ * ╭───     ───╮ * ╭─╮ * ╭╮ * ╰─╯ * │
│ ******* ││ * │ │ * │           │ * │ │ * ││ ******* │
│ * ╭─╮ * ╰╯ * ╰─╯ * ╰───────────╯ * ╰─╯ * ╰╯ * ╭─╮ * │
│ * │ │ *************************************** │ │ * │
│ * │ ╰────╮ * ╭─╮ * ╭───────────╮ * ╭─╮ * ╭────╯ │ * │
│ * ╰──────╯ * │ │ * ╰───────────╯ * │ │ * ╰──────╯ * │
│ ************ │ │ ***************** │ │ ************ │
╰──────────────╯ ╰───────────────────╯ ╰──────────────╯
"""

class JogoPacman:
    def __init__(self, mapa_str):
        linhas = mapa_str.strip().split('\n')
        self.mapa = [list(linha) for linha in linhas]
        self.altura = len(self.mapa)
        self.largura = len(self.mapa[0])
        self.score = 0
        self.game_over = False
        
        self.pacman_pos = [1, 2]
        self.direcao_atual = 'd'
        self.proxima_direcao = 'd'
        
        self.caminhos_permitidos = set()
        posicoes_iniciais_validas = []

        for y in range(self.altura):
            for x in range(len(self.mapa[y])):
                char = self.mapa[y][x]
                if char == '*':
                    self.caminhos_permitidos.add((y, x))
                    posicoes_iniciais_validas.append((y, x))
                    self.mapa[y][x] = PASTILHA

        if posicoes_iniciais_validas:
            self.pacman_pos = list(posicoes_iniciais_validas[0])
            py, px = self.pacman_pos
            self.mapa[py][px] = VAZIO

        self.fantasmas = []
        if len(posicoes_iniciais_validas) > 10:
            area_fantasmas = posicoes_iniciais_validas[10:] 
            for _ in range(3):
                pos = random.choice(area_fantasmas)
                self.fantasmas.append({'pos': list(pos), 'dir': 'd'})

    def ler_input(self):
        if msvcrt.kbhit():
            key = msvcrt.getch()
            # Verifica se é uma tecla especial (Setas começam com \xe0 ou \x00)
            if key == b'\xe0' or key == b'\x00':
                try:
                    # Pega o segundo código da tecla
                    sub_key = msvcrt.getch()
                    
                    if sub_key == b'H':   # Seta CIMA
                        self.proxima_direcao = 'w'
                    elif sub_key == b'P': # Seta BAIXO
                        self.proxima_direcao = 's'
                    elif sub_key == b'K': # Seta ESQUERDA
                        self.proxima_direcao = 'a'
                    elif sub_key == b'M': # Seta DIREITA
                        self.proxima_direcao = 'd'
                except:
                    pass

    def pode_mover(self, y, x):
        if (y, x) in self.caminhos_permitidos:
            return True
        return False

    def mover_entidade(self, pos_atual, direcao):
        y, x = pos_atual
        novo_y, novo_x = y, x

        if direcao == 'w': novo_y -= 1
        elif direcao == 's': novo_y += 1
        elif direcao == 'a': novo_x -= 1
        elif direcao == 'd': novo_x += 1
        
        if self.pode_mover(novo_y, novo_x):
            return [novo_y, novo_x], True
        return [y, x], False

    def atualizar_fantasmas(self):
        direcoes = ['w', 'a', 's', 'd']
        for f in self.fantasmas:
            nova_pos, moveu = self.mover_entidade(f['pos'], f['dir'])
            if moveu:
                f['pos'] = nova_pos
                if random.random() < 0.2: 
                    f['dir'] = random.choice(direcoes)
            else:
                f['dir'] = random.choice(direcoes)

            if f['pos'] == self.pacman_pos:
                self.game_over = True

    def update(self):
        nova_pos, moveu = self.mover_entidade(self.pacman_pos, self.proxima_direcao)
        if moveu:
            self.direcao_atual = self.proxima_direcao
            self.pacman_pos = nova_pos
        else:
            nova_pos, moveu = self.mover_entidade(self.pacman_pos, self.direcao_atual)
            if moveu:
                self.pacman_pos = nova_pos

        py, px = self.pacman_pos
        if self.mapa[py][px] == PASTILHA:
            self.mapa[py][px] = VAZIO
            self.score += 10

        self.atualizar_fantasmas()

    def desenhar(self):
        print('\033[H', end='')
        print(f"MOVER: setas | SAIR: control+c | SCORE: {self.score}")
        
        buffer_desenho = []
        for y in range(self.altura):
            linha_str = ""
            for x in range(len(self.mapa[y])):
                char = self.mapa[y][x]
                cor = COR_AZUL 
                
                if (y, x) in self.caminhos_permitidos:
                    cor = COR_RESET
                
                if char == PASTILHA:
                    char = PASTILHA
                    cor = COR_RESET
                
                for f in self.fantasmas:
                    if f['pos'] == [y, x]:
                        char = FANTASMA_SPRITE
                        cor = COR_VERMELHO
                        break
                
                if self.pacman_pos == [y, x]:
                    char = PACMAN_SPRITES[self.direcao_atual]
                    cor = COR_AMARELO

                linha_str += f"{cor}{char}{COR_RESET}"
            buffer_desenho.append(linha_str)
        print("\n".join(buffer_desenho))

def main():
    os.system('cls')
    jogo = JogoPacman(MAPA_ORIGINAL)
    print("\033[?25l")
    
    try:
        while not jogo.game_over:
            start = time.time()
            jogo.ler_input()
            jogo.update()
            jogo.desenhar()
            time.sleep(max(0, 0.1 - (time.time() - start)))
    except KeyboardInterrupt:
        pass
    finally:
        print("\033[?25h")
        os.system('cls')
        print(f"Fim de jogo! Score: {jogo.score}")

if __name__ == "__main__":
    main()
