import curses
import random
import time

def iniciar_river_raid(tela):
    # --- CONFIGURAÇÕES INICIAIS DA TELA ---
    curses.curs_set(0)  # Esconde o cursor
    
    # --- CONFIGURAÇÃO DE CORES (ESTILO ATARI 2600) ---
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Avião e Tiros
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Margens de Grama
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)    # Água do Rio
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)     # Helicópteros
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)   # Barcos
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # Tanques de Combustível
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_RED)     # Fundo Vermelho (Game Over)

    altura_tela, largura_tela = tela.getmaxyx()

    # O jogo inteiro roda dentro deste "while True" para permitir reiniciar
    while True:
        tela.nodelay(1) # O jogo não para esperando tecla durante a partida

        # --- VARIÁVEIS DA PARTIDA ---
        posicao_aviao_x = largura_tela // 2
        linha_do_aviao = altura_tela - 5
        largura_rio = 40
        centro_rio = largura_tela // 2
        
        pontuacao = 0
        velocidade = 0.05
        
        # Variáveis do Combustível
        combustivel_atual = 100.0
        taxa_consumo_combustivel = 0.2
        
        # Variáveis para criar o rio em blocos retos e diagonais (Estilo Atari)
        direcao_do_rio = 0
        linhas_para_mudar_direcao = 0

        # Preenche o rio inicialmente para ele cobrir a tela toda
        tracado_do_rio = [] 
        for _ in range(altura_tela):
            tracado_do_rio.append(centro_rio)

        entidades = [] # Guarda barcos, helicópteros e combustível
        tiros = []
        
        causa_da_morte = ""
        jogo_rodando = True

        # --- LOOP DA PARTIDA ATUAL ---
        while jogo_rodando:
            
            # 1. LER OS COMANDOS DO JOGADOR
            tecla = tela.getch()

            if tecla == curses.KEY_LEFT:
                posicao_aviao_x -= 3
            elif tecla == curses.KEY_RIGHT:
                posicao_aviao_x += 3
            elif tecla == ord(' '):  # Tecla de espaço para atirar
                # Limita a 3 tiros simultâneos na tela
                if len(tiros) < 3:
                    tiros.append({'x': posicao_aviao_x, 'y': linha_do_aviao - 1})
            elif tecla == ord('q') or tecla == ord('Q') or tecla == 27: # 27 é a tecla ESC
                jogo_rodando = False
                causa_da_morte = "SAIU DO JOGO"

            # 2. ATUALIZAR O FORMATO DO RIO (ESTILO ATARI - Retas e Diagonais)
            linhas_para_mudar_direcao -= 1
            if linhas_para_mudar_direcao <= 0:
                # Escolhe uma nova direção: -2 (esq rápida), -1 (esq), 0 (reto), 1 (dir), 2 (dir rápida)
                direcao_do_rio = random.choice([-2, -1, 0, 0, 0, 1, 2])
                # Mantém essa direção por várias linhas para criar retas e diagonais longas
                linhas_para_mudar_direcao = random.randint(5, 20)

            centro_rio += direcao_do_rio

            # Evita que o rio saia da tela
            margem_de_seguranca = largura_rio // 2 + 5
            if centro_rio < margem_de_seguranca:
                centro_rio = margem_de_seguranca
                direcao_do_rio = 0 # Força a ficar reto se bater na borda da tela
            elif centro_rio > largura_tela - margem_de_seguranca:
                centro_rio = largura_tela - margem_de_seguranca
                direcao_do_rio = 0

            # Move o rio para baixo
            tracado_do_rio.insert(0, centro_rio)
            tracado_do_rio.pop()

            pontuacao += 1

            # 3. CONSUMIR COMBUSTÍVEL
            combustivel_atual -= taxa_consumo_combustivel
            if combustivel_atual <= 0:
                jogo_rodando = False
                causa_da_morte = "PANE SECA (FALTA DE COMBUSTÍVEL)"

            # 4. GERAR ENTIDADES (INIMIGOS E COMBUSTÍVEL)
            if random.randint(1, 100) < 10:
                centro_atual_topo = tracado_do_rio[0]
                borda_esq = centro_atual_topo - (largura_rio // 2) + 4
                borda_dir = centro_atual_topo + (largura_rio // 2) - 4
                
                # Escolhe o que vai aparecer
                sorteio = random.randint(1, 100)
                if sorteio < 20:
                    tipo_ent = 'combustivel'
                    dir_ent = 0 # Combustível fica parado
                elif sorteio < 60:
                    tipo_ent = 'barco'
                    dir_ent = random.choice([-1, 1])
                else:
                    tipo_ent = 'helicoptero'
                    dir_ent = random.choice([-1, 1])
                
                pos_x_ent = random.randint(borda_esq, borda_dir)
                
                entidades.append({
                    'x': pos_x_ent, 
                    'y': 0, 
                    'tipo': tipo_ent,
                    'direcao': dir_ent
                })

            # 5. MOVIMENTAR TIROS
            tiros_ativos = []
            for tiro in tiros:
                tiro['y'] -= 1
                if tiro['y'] > 0:
                    tiros_ativos.append(tiro)
            tiros = tiros_ativos

            # 6. MOVIMENTAR ENTIDADES
            entidades_ativas = []
            for ent in entidades:
                ent['y'] += 1
                
                # Inimigos se movem para os lados. Combustível não.
                if ent['tipo'] != 'combustivel' and pontuacao % 2 == 0: 
                    ent['x'] += ent['direcao']

                # Bateu nas margens do rio, inverte a direção
                centro_rio_ent = tracado_do_rio[ent['y']] if ent['y'] < altura_tela else centro_rio
                if ent['x'] <= centro_rio_ent - (largura_rio // 2) + 2:
                    ent['direcao'] = 1
                elif ent['x'] >= centro_rio_ent + (largura_rio // 2) - 2:
                    ent['direcao'] = -1

                if ent['y'] < altura_tela:
                    entidades_ativas.append(ent)
            entidades = entidades_ativas

            # 7. VERIFICAR COLISÕES (TIROS X ENTIDADES)
            entidades_sobreviventes = []
            for ent in entidades:
                atingido = False
                for tiro in tiros:
                    if abs(tiro['x'] - ent['x']) <= 2 and abs(tiro['y'] - ent['y']) <= 1:
                        atingido = True
                        tiros.remove(tiro)
                        if ent['tipo'] == 'combustivel':
                            pontuacao += 80  # Destruir tanque dá mais pontos
                        else:
                            pontuacao += 50
                        break 
                
                if not atingido:
                    entidades_sobreviventes.append(ent)
            entidades = entidades_sobreviventes

            # 8. VERIFICAR COLISÃO DO AVIÃO
            centro_da_agua_do_aviao = tracado_do_rio[linha_do_aviao]
            limite_esquerdo = centro_da_agua_do_aviao - (largura_rio // 2)
            limite_direito = centro_da_agua_do_aviao + (largura_rio // 2)

            # Bateu na margem de terra verde
            if posicao_aviao_x <= limite_esquerdo + 2 or posicao_aviao_x >= limite_direito - 2:
                jogo_rodando = False 
                causa_da_morte = "BATEU NA MARGEM"

            # Interação do avião com as entidades
            for ent in entidades:
                if abs(posicao_aviao_x - ent['x']) <= 2 and abs(linha_do_aviao - ent['y']) <= 1:
                    if ent['tipo'] == 'combustivel':
                        # Se voar por cima, reabastece muito rápido, mas não explode
                        combustivel_atual += 3.0
                        if combustivel_atual > 100:
                            combustivel_atual = 100
                    else:
                        jogo_rodando = False
                        causa_da_morte = "BATEU EM UM INIMIGO"

            # 9. DESENHAR TUDO NA TELA
            tela.erase()

            # Desenha o rio e as margens
            for linha in range(altura_tela - 2): # Deixa 2 linhas livres na base para o painel
                centro_desta_linha = tracado_do_rio[linha]
                borda_esq = centro_desta_linha - (largura_rio // 2)
                borda_dir = centro_desta_linha + (largura_rio // 2)

                try:
                    # Margem Esquerda
                    tela.addstr(linha, 0, "█" * borda_esq, curses.color_pair(2))
                    # Água do Rio
                    largura_agua = borda_dir - borda_esq
                    tela.addstr(linha, borda_esq, "≈" * largura_agua, curses.color_pair(3))
                    # Margem Direita
                    espaco_direita = largura_tela - borda_dir
                    tela.addstr(linha, borda_dir, "█" * espaco_direita, curses.color_pair(2))
                except curses.error:
                    pass

            # Desenha os tiros
            for tiro in tiros:
                try:
                    tela.addstr(tiro['y'], tiro['x'], "│", curses.color_pair(1) | curses.A_BOLD)
                except curses.error:
                    pass

            # Desenha as Entidades
            for ent in entidades:
                try:
                    if ent['tipo'] == 'helicoptero':
                        tela.addstr(ent['y'], ent['x'] - 1, "━┳━", curses.color_pair(4) | curses.A_BOLD)
                    elif ent['tipo'] == 'barco':
                        tela.addstr(ent['y'], ent['x'] - 1, "▅▄ ", curses.color_pair(5))
                    elif ent['tipo'] == 'combustivel':
                        tela.addstr(ent['y'], ent['x'] - 1, "[F]", curses.color_pair(6) | curses.A_BOLD)
                except curses.error:
                    pass

            # Desenha o Avião do Jogador
            try:
                if jogo_rodando: # Se estiver vivo, desenha o avião normal
                    tela.addstr(linha_do_aviao - 1, posicao_aviao_x,     "▲", curses.color_pair(1) | curses.A_BOLD)
                    tela.addstr(linha_do_aviao,     posicao_aviao_x - 1, "▟█▙", curses.color_pair(1) | curses.A_BOLD)
                    tela.addstr(linha_do_aviao + 1, posicao_aviao_x,     "▀", curses.color_pair(1))
                else: # Se morreu, desenha uma explosão
                    tela.addstr(linha_do_aviao - 1, posicao_aviao_x - 1, "\\|/", curses.color_pair(4) | curses.A_BOLD)
                    tela.addstr(linha_do_aviao,     posicao_aviao_x - 1, "-*-", curses.color_pair(1) | curses.A_BOLD)
                    tela.addstr(linha_do_aviao + 1, posicao_aviao_x - 1, "/|\\", curses.color_pair(4) | curses.A_BOLD)
            except curses.error:
                pass

            # --- DESENHA O PAINEL INFERIOR ---
            # Barra de Combustível (Fuel)
            try:
                tamanho_barra = 20
                qtd_blocos = int((combustivel_atual / 100) * tamanho_barra)
                barra = "█" * qtd_blocos + " " * (tamanho_barra - qtd_blocos)
                texto_fuel = f" FUEL: E[{barra}]F "
                tela.addstr(altura_tela - 1, 2, texto_fuel, curses.color_pair(1) | curses.A_BOLD)
                
                # Placar
                texto_placar = f" SCORE: {pontuacao:05d} "
                tela.addstr(altura_tela - 1, largura_tela - len(texto_placar) - 2, texto_placar, curses.color_pair(1) | curses.A_BOLD)
            except curses.error:
                pass

            tela.refresh() 
            time.sleep(velocidade)

        # --- PAUSA DRAMÁTICA APÓS O GAME OVER ---
        # Exibe a explosão por 1.5 segundos antes de limpar a tela
        time.sleep(1.5)

        # --- TELA DE FIM DE JOGO (JANELA) ---
        tela.nodelay(0) # Volta a travar o terminal esperando o jogador apertar algo
        tela.erase()
        
        janela_altura = 7
        janela_largura = 70
        inicio_y = (altura_tela - janela_altura) // 2
        inicio_x = (largura_tela - janela_largura) // 2

        # Desenha a caixa vermelha de Game Over
        for y in range(janela_altura):
            try:
                tela.addstr(inicio_y + y, inicio_x, " " * janela_largura, curses.color_pair(7))
            except curses.error:
                pass

        msg_titulo = " G A M E   O V E R "
        msg_causa = f"Causa: {causa_da_morte}"
        msg_score = f"Seu Score Final: {pontuacao}"
        msg_instrucoes = "Pressione [ESPAÇO] para jogar novamente ou [ESC] para sair"

        try:
            tela.addstr(inicio_y + 1, inicio_x + (janela_largura - len(msg_titulo)) // 2, msg_titulo, curses.color_pair(7) | curses.A_BOLD)
            tela.addstr(inicio_y + 3, inicio_x + (janela_largura - len(msg_causa)) // 2, msg_causa, curses.color_pair(7))
            tela.addstr(inicio_y + 4, inicio_x + (janela_largura - len(msg_score)) // 2, msg_score, curses.color_pair(7))
            tela.addstr(inicio_y + 5, inicio_x + (janela_largura - len(msg_instrucoes)) // 2, msg_instrucoes, curses.color_pair(7) | curses.A_BOLD)
        except curses.error:
            pass
        
        tela.refresh()

        # Aguarda a tecla ESPAÇO (32) para reiniciar ou ESC (27) para sair
        tecla_fim = -1
        while tecla_fim not in [27, 32]:
            tecla_fim = tela.getch()

        if tecla_fim == 27: # Se apertou Esc, encerra o loop principal e sai do jogo
            break

if __name__ == "__main__":
    curses.wrapper(iniciar_river_raid)
