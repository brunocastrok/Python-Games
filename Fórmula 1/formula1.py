import os
import time
import msvcrt   # Biblioteca para controlar teclado no Windows
import random   # Biblioteca para gerar números aleatórios (sorteio)

# ==============================================================================
# 1. CONFIGURAÇÕES VISUAIS (CORES E DESENHOS)
# ==============================================================================
# O computador entende cores através de códigos especiais chamados "ANSI".
# É como dizer ao terminal: "Pinte tudo o que vier depois disso de azul".
COR_AZUL = '\033[94m'
COR_VERDE = '\033[92m'
COR_VERMELHO = '\033[91m'
COR_AMARELO = '\033[93m'
COR_CINZA = '\033[90m'
COR_RESET = '\033[0m'  # Este código desliga a cor e volta ao normal

# Estes são os "Atores" do nosso jogo
DESENHO_JOGADOR = '▲'
DESENHO_INIMIGO = '▼'

# ==============================================================================
# 2. O MAPA DO JOGO (A MOLDURA FIXA)
# ==============================================================================
# Os pontos (.) são lugares vazios onde os carros podem passar.
# O código vai substituir esses pontos pelos carros durante o jogo.

MAPA_BASE = r"""
╭───────────────────╮
│ PONTOS: 0000      │
├───────────────────┤
│ . │ . │ . │ . │ . │
│ . │ . │ . │ . │ . │
│ . │ . │ . │ . │ . │
│ . │ . │ . │ . │ . │
│ . │ . │ . │ . │ . │
│ . │ . │ . │ . │ . │
│ . │ . │ . │ . │ . │
│ . │ . │ . │ . │ . │
│ . │ . │ . │ . │ . │
│ . │ . │ . │ . │ . │
│ . │ . │ . │ . │ . │
│ . │ . │ . │ . │ . │
│ . │ . │ . │ . │ . │
│ . │ . │ . │ . │ . │
│ . │ . │ . │ . │ . │
╰───────────────────╯
"""

# ==============================================================================
# 3. CONFIGURAÇÃO DAS FAIXAS
# ==============================================================================
# O jogo tem 5 faixas (caminhos) onde os carros andam.
# Mas o computador precisa saber em qual "letra" da string acima cada faixa fica.
#
# Olhando o mapa acima: "│ . │ . │ . │ . │ . │"
# A faixa 0 (primeira) está na posição 2 da linha.
# A faixa 1 (segunda) está na posição 6 da linha, e assim por diante.
POSICOES_VISUAIS = [2, 6, 10, 14, 18]

def preparar_terminal():
    """
    Função para limpar a tela preta e esconder o cursor piscante,
    para o jogo ficar mais limpo visualmente.
    """
    os.system('') # Ativa o modo de cores no Windows
    print("\033[2J\033[?25l", end="") # Código mágico que limpa tudo

def obter_copia_do_mapa():
    """
    O MAPA_BASE é um texto fixo. Não podemos rabiscar nele.
    Esta função tira uma 'xerox' do mapa e transforma em uma lista
    de letras soltas, para que possamos desenhar os carros nessa cópia.
    """
    # Separa o texto em várias linhas
    linhas = MAPA_BASE.strip().split('\n')
    # Transforma cada linha em uma lista de letras editáveis
    return [list(linha) for linha in linhas]

# ==============================================================================
# 4. O JOGO PRINCIPAL (A LÓGICA)
# ==============================================================================
def iniciar_jogo():
    # Variáveis de Estado (Memória do Jogo)
    largura_pista = 5   # Temos 5 faixas
    altura_pista = 15   # A pista tem 15 andares de altura
    
    # Onde a pista começa visualmente no desenho (pula o cabeçalho de pontos)
    margem_topo = 3 
    
    posicao_jogador = 2  # Começa no meio (0, 1, [2], 3, 4)
    inimigos = []        # Lista vazia, vamos adicionar inimigos depois
    pontos = 0
    frame = 0            # Contador de quantos quadros já passaram
    velocidade = 0.15    # Tempo de espera (quanto menor, mais rápido)

    # LOOP INFINITO: O jogo roda aqui dentro sem parar até perder
    while True:
        # Marcamos a hora de agora para controlar a velocidade depois
        hora_inicio = time.time()

        # ---------------------------------------------------------
        # PASSO 1: ESCUTAR O JOGADOR (INPUT)
        # ---------------------------------------------------------
        # Verifica se alguma tecla foi apertada neste exato momento
        if msvcrt.kbhit():
            tecla = msvcrt.getch() # Lê a tecla
            
            # Se for ESC (\x1b), sai do jogo
            if tecla == b'\x1b': 
                break 
            
            # Se for uma tecla especial (como setas), ela manda dois códigos
            if tecla == b'\xe0': 
                seta = msvcrt.getch() # Lê o segundo código (a direção)
                
                # Se for ESQUERDA (K) e não estiver na borda, move pra esquerda
                if seta == b'K' and posicao_jogador > 0: 
                    posicao_jogador -= 1
                
                # Se for DIREITA (M) e não estiver na borda, move pra direita
                if seta == b'M' and posicao_jogador < largura_pista - 1: 
                    posicao_jogador += 1

        # ---------------------------------------------------------
        # PASSO 2: ATUALIZAR O MUNDO (LÓGICA)
        # ---------------------------------------------------------
        
        # A cada 3 frames (quadros), criamos um novo inimigo
        if frame % 3 == 0:
            coluna_sorteada = random.randint(0, largura_pista - 1)
            # Adiciona um inimigo na linha 0 (topo), na coluna sorteada
            inimigos.append([0, coluna_sorteada])
        
        # Faz todos os inimigos descerem um degrau (linha + 1)
        for inimigo in inimigos:
            inimigo[0] += 1
        
        # VERIFICA BATIDA (GAME OVER)
        # Se algum inimigo estiver na última linha (altura_pista - 1)
        # E estiver na mesma coluna do jogador... Bateu!
        bateu = False
        for inimigo in inimigos:
            if inimigo[0] == altura_pista - 1 and inimigo[1] == posicao_jogador:
                bateu = True
                break
        
        if bateu:
            break # Sai do loop infinito e termina o jogo

        # LIMPEZA E PONTOS
        # Criamos uma nova lista só com os inimigos que ainda estão na tela
        inimigos_na_tela = []
        for inimigo in inimigos:
            if inimigo[0] < altura_pista:
                # Se ainda está na tela, mantém
                inimigos_na_tela.append(inimigo)
            else:
                # Se saiu da tela (passou pelo jogador), ganha ponto!
                pontos += 1
                # Aumenta a velocidade (diminui o tempo de espera)
                velocidade = max(0.04, 0.15 - (pontos * 0.001))
        
        # Atualiza a lista oficial de inimigos
        inimigos = inimigos_na_tela

        # ---------------------------------------------------------
        # PASSO 3: DESENHAR A TELA (RENDERIZAÇÃO)
        # ---------------------------------------------------------
        
        # 1. Pega uma cópia limpa do mapa
        matriz_tela = obter_copia_do_mapa()

        # 2. Escreve a pontuação no cabeçalho
        texto_pontos = f"{pontos:04d}" # Formata numero 5 para "0005"
        # Escreve dígito por dígito na linha 1 do mapa
        for i, digito in enumerate(texto_pontos):
            matriz_tela[1][10 + i] = digito 

        # 3. Desenha os Inimigos
        for inimigo in inimigos:
            linha_real = inimigo[0]
            coluna_real = inimigo[1]
            
            # Calcula onde desenhar na matriz visual
            linha_visual = linha_real + margem_topo
            coluna_visual = POSICOES_VISUAIS[coluna_real]
            
            # Só desenha se estiver dentro do limite do desenho
            if linha_visual < len(matriz_tela) - 1:
                matriz_tela[linha_visual][coluna_visual] = DESENHO_INIMIGO

        # 4. Desenha o Jogador
        linha_jogador_visual = (altura_pista - 1) + margem_topo
        coluna_jogador_visual = POSICOES_VISUAIS[posicao_jogador]
        matriz_tela[linha_jogador_visual][coluna_jogador_visual] = DESENHO_JOGADOR

        # 5. TRANSFORMAÇÃO FINAL (Cores e Texto)
        # Agora vamos transformar nossa matriz de volta em texto para imprimir,
        # aplicando as cores no momento exato da impressão.
        
        texto_final = "\033[H" # Comando para voltar o cursor ao topo (não limpar tudo)
        
        for linha in matriz_tela:
            linha_colorida = ""
            for letra in linha:
                # Se for o jogador -> Verde
                if letra == DESENHO_JOGADOR:
                    linha_colorida += f"{COR_VERDE}{letra}{COR_RESET}"
                
                # Se for inimigo -> Vermelho
                elif letra == DESENHO_INIMIGO:
                    linha_colorida += f"{COR_VERMELHO}{letra}{COR_RESET}"
                
                # Se for parte da moldura (bordas) -> Azul
                elif letra in ['╭', '╮', '╯', '╰', '─', '│', '├', '┤']:
                    linha_colorida += f"{COR_AZUL}{letra}{COR_RESET}"
                
                # Se for ponto guia (.) -> Transforma em espaço vazio
                elif letra == '.':
                    linha_colorida += " "
                
                # Se for número ou texto -> Amarelo
                elif letra.isdigit() or letra in ['P', 'O', 'N', 'T', 'S', ':']:
                    linha_colorida += f"{COR_AMARELO}{letra}{COR_RESET}"
                
                # Qualquer outra coisa -> Normal
                else:
                    linha_colorida += letra
            
            # Adiciona a linha pronta ao texto final + quebra de linha
            texto_final += linha_colorida + "\n"
        
        # Adiciona instruções no rodapé
        texto_final += f"{COR_CINZA} ← → Mover | ESC Sair{COR_RESET}"

        # Imprime TUDO de uma única vez (evita piscar a tela)
        print(texto_final, flush=True)

        # ---------------------------------------------------------
        # PASSO 4: CONTROLE DE TEMPO (FPS)
        # ---------------------------------------------------------
        frame += 1
        
        # Calcula quanto tempo demorou para processar tudo
        tempo_gasto = time.time() - hora_inicio
        
        # Dorme apenas o tempo que sobrou para manter a velocidade constante
        tempo_dormir = max(0, velocidade - tempo_gasto)
        time.sleep(tempo_dormir)

    # ==========================================================================
    # FIM DE JOGO
    # ==========================================================================
    print(f"\n {COR_VERMELHO}GAME OVER! Pontuação Final: {pontos}{COR_RESET}")
    print("\033[?25h") # Mostra o cursor de volta

# Aqui é onde o programa realmente começa a rodar
if __name__ == "__main__":
    try:
        preparar_terminal()
        iniciar_jogo()
    except KeyboardInterrupt:
        # Se o usuário der Ctrl+C, restaura o terminal
        print("\033[?25h")
