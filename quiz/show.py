import tkinter as tk            # Interface Gráfica
from tkinter import messagebox  # Caixas de aviso
import csv                      # Ler planilhas
import random                   # Sorteio
import threading                # Gerenciar processos paralelos (threads)
import imageio                  # Ler os frames do vídeo
from PIL import Image, ImageTk  # Manipular imagens para o Tkinter

# ==============================================================================
# 1. CONFIGURAÇÕES E CONSTANTES
# ==============================================================================

VIDEO_ENTRADA     = "intro_pythao.mp4"
VIDEO_FUNDO       = "bg_pythao.mp4"
ARQUIVO_PERGUNTAS = "perguntas.csv"

# Meta para vencer o jogo
META_ACERTOS = 10 

# Cores
COR_FUNDO = '#0d2727'
COR_TEXTO = '#ffffff'
COR_ERRO  = '#8b0000'

# ==============================================================================
# 2. VARIÁVEIS GLOBAIS
# ==============================================================================

# Widgets (Elementos visuais)
root = None
video_label = None
enunciado_label = None
botoes_alternativas_frame = None
widgets_vidas = []

# Controle do Vídeo
thread_video_atual = None       # Guarda a referência do processo do vídeo
evento_parar_video = None       # Um "interruptor" para desligar o vídeo antigo

# Estado do Jogo
perguntas_embaralhadas = []
indice_pergunta_atual = 0
vidas = 3
pontuacao_atual = 0
alternativas_atuais = []
gabarito_atual = ""

# ==============================================================================
# 3. FUNÇÕES DO SISTEMA DE VÍDEO (CORREÇÃO DO ERRO)
# ==============================================================================

def stream_video(caminho, label, evento_parar):
	"""
	Função que roda em paralelo (Thread).
	Lê o vídeo frame a frame e atualiza o Label.
	Obedece imediatamente ao sinal de 'evento_parar'.
	"""
	try:
		# Abre o vídeo para leitura
		video_reader = imageio.get_reader(caminho)
		
		# Loop infinito para repetir o vídeo (Loop)
		while not evento_parar.is_set():
			for frame in video_reader:
				# 1. Checa se mandaram parar IMEDIATAMENTE
				if evento_parar.is_set():
					return
				
				# 2. Checa se a janela ou o label ainda existem
				if not label.winfo_exists():
					return

				# 3. Converte o frame do vídeo para imagem compatível com Tkinter
				image = Image.fromarray(frame)
				
				# Redimensiona para caber na tela (ajuste fino de performance)
				image = image.resize((940, 520)) 
				frame_image = ImageTk.PhotoImage(image)
				
				# 4. Atualiza o Label
				label.config(image=frame_image)
				label.image = frame_image # Mantém referência para não sumir
				
				# Pequena pausa para controlar a velocidade (opcional)
				# time.sleep(0.001) 

	except Exception as e:
		print(f"Erro na thread de vídeo: {e}")

def exibe_video(caminho_video):
	"""
	Gerencia a troca segura de vídeos.
	Para o anterior antes de iniciar o próximo.
	"""
	global thread_video_atual, evento_parar_video, video_label

	# 1. Se já existe um vídeo rodando, manda parar!
	if evento_parar_video:
		evento_parar_video.set() # Aperta o botão de parada

	# 2. Cria o Label se ele não existir
	if video_label is None or not video_label.winfo_exists():
		video_label = tk.Label(root, bg='black')
		video_label.place(x=0, y=0, width=940, height=520)
		video_label.lower() # Manda para o fundo

	# 3. Prepara o novo sistema de controle
	evento_parar_video = threading.Event() # Cria um novo interruptor "ligado"
	
	# 4. Inicia a nova Thread
	thread_video_atual = threading.Thread(
		target=stream_video,
		args=(caminho_video, video_label, evento_parar_video)
	)
	thread_video_atual.daemon = True # Garante que fecha se o programa fechar
	thread_video_atual.start()

# ==============================================================================
# 4. LÓGICA DO JOGO
# ==============================================================================

def carrega_perguntas():
	"""Carrega perguntas do CSV."""
	global perguntas_embaralhadas
	todas = []
	try:
		with open(ARQUIVO_PERGUNTAS, 'r', newline='', encoding='utf-8') as f:
			leitor = csv.DictReader(f, delimiter='|')
			for linha in leitor:
				todas.append({
					"enunciado": linha['enunciado'],
					"alternativas": [
						linha['alternativa_1'],
						linha['alternativa_2'],
						linha['alternativa_3']
					]
				})
		random.shuffle(todas)
		perguntas_embaralhadas = todas
		return True
	except Exception as e:
		messagebox.showerror("Erro", f"Erro no arquivo CSV: {e}")
		return False

def verifica_resposta(escolha_jogador):
	"""Verifica se acertou ou errou."""
	global vidas, pontuacao_atual
	
	if escolha_jogador == gabarito_atual:
		pontuacao_atual += 1
		messagebox.showinfo("Correto", f"Certa resposta! ({pontuacao_atual}/{META_ACERTOS})")
		
		if pontuacao_atual >= META_ACERTOS:
			messagebox.showinfo("Vencedor", "PARABÉNS! Você venceu o Show do Pythão!")
			tela_inicial()
			return
	else:
		vidas -= 1
		atualiza_vidas()
		
		# Mostra a correta
		idx = alternativas_atuais.index(gabarito_atual)
		letra_correta = ['A', 'B', 'C'][idx]
		messagebox.showerror("Errou", f"Errado! A resposta era: {letra_correta}")
		
		if vidas <= 0:
			messagebox.showinfo("Game Over", "Suas vidas acabaram.")
			tela_inicial()
			return

	proxima_pergunta()

def proxima_pergunta():
	"""Avança para a próxima."""
	global indice_pergunta_atual
	indice_pergunta_atual += 1
	
	if indice_pergunta_atual >= len(perguntas_embaralhadas):
		messagebox.showinfo("Fim", "As perguntas acabaram!")
		tela_inicial()
		return
		
	monta_tela_jogo()

# ==============================================================================
# 5. INTERFACE GRÁFICA
# ==============================================================================

def atualiza_vidas():
	"""Desenha os corações."""
	for w in widgets_vidas: w.destroy()
	widgets_vidas.clear()

	vidas_frame = tk.Frame(root, bg=COR_FUNDO)
	vidas_frame.place(relx=0.5, y=440, anchor='n')

	for i in range(3):
		cor = 'green' if i < vidas else COR_ERRO
		l = tk.Label(vidas_frame, text="♥", font=('Segoe UI', 20), bg=COR_FUNDO, fg=cor)
		l.grid(row=0, column=i)
		widgets_vidas.append(l)

def monta_tela_jogo():
	"""Configura a pergunta na tela."""
	global alternativas_atuais, gabarito_atual, botoes_alternativas_frame
	
	pergunta = perguntas_embaralhadas[indice_pergunta_atual]
	gabarito_atual = pergunta['alternativas'][0]
	alternativas_atuais = list(pergunta['alternativas'])
	random.shuffle(alternativas_atuais)
	
	enunciado_label.config(text=pergunta['enunciado'])
	
	# Limpa botões anteriores
	for w in botoes_alternativas_frame.winfo_children():
		w.destroy()
		
	letras = ['A', 'B', 'C']
	for i, alt in enumerate(alternativas_atuais):
		btn = tk.Button(botoes_alternativas_frame, text=f"{letras[i]}) {alt}", command=lambda r=alt: verifica_resposta(r),
						font=('Segoe UI', 14, 'bold'), bg=COR_FUNDO, fg=COR_TEXTO, anchor='w', width=30)
		btn.grid(row=i, column=0, pady=5, sticky='w')

def limpar_tela():
	"""Remove tudo, mas cuida para não quebrar o vídeo."""
	global video_label
	for widget in root.winfo_children():
		if widget != video_label: # Protege o vídeo
			widget.destroy()

def comecar_jogo():
	"""Tela de Jogo."""
	global enunciado_label, botoes_alternativas_frame, vidas, pontuacao_atual, indice_pergunta_atual
	
	if not carrega_perguntas(): return
	
	vidas = 3
	pontuacao_atual = 0
	indice_pergunta_atual = 0
	
	limpar_tela()
	exibe_video(VIDEO_FUNDO) # Troca suave
	
	# Layout
	frame_l = 940 * 0.9
	x_pos = (940 - frame_l)/2
	
	conteudo = tk.Frame(root, bg=COR_FUNDO, width=int(frame_l), height=400)
	conteudo.place(x=x_pos, y=15)
	
	enunciado_label = tk.Label(conteudo, text="...", wraplength=int(frame_l*0.9), justify=tk.LEFT, font=('Segoe UI', 18, 'bold'), bg=COR_FUNDO, fg=COR_TEXTO)
	enunciado_label.place(relx=0.05, rely=0.05, anchor='nw')
	
	botoes_alternativas_frame = tk.Frame(conteudo, bg=COR_FUNDO)
	botoes_alternativas_frame.place(relx=0.05, rely=0.3, anchor='nw')
	
	atualiza_vidas()
	monta_tela_jogo()

def tela_inicial():
	"""Menu Principal."""
	global root, video_label
	
	if not root:
		root = tk.Tk()
		root.title("Show do Pythão")
		root.geometry("940x520")
	
	limpar_tela()
	exibe_video(VIDEO_ENTRADA)
	
	btn = tk.Button(root, text=" Começar Jogo ", command=comecar_jogo, font=('Segoe UI', 13, 'bold'), bg=COR_FUNDO, fg=COR_TEXTO)
	btn.place(relx=0.44, rely=0.95, anchor='s')
	
	btn_sair = tk.Button(root, text=" Sair ", command=root.destroy, font=('Segoe UI', 13, 'bold'), bg=COR_FUNDO, fg=COR_TEXTO)
	btn_sair.place(relx=0.55, rely=0.95, anchor='s')

if __name__ == "__main__":
	tela_inicial()
	if root:
		root.mainloop()
