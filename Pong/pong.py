import sys
import time
import random

try:
    import msvcrt
except ImportError:
    print("Este código foi feito para Windows (msvcrt).")
    sys.exit(1)

# --- Caracteres do tabuleiro ---
CANTO_SUPERIOR_ESQUERDO = '╭'
CANTO_SUPERIOR_DIREITO = '╮'
CANTO_INFERIOR_ESQUERDO = '╰'
CANTO_INFERIOR_DIREITO = '╯'
HORIZONTAL = '─'
VERTICAL = '│'

# --- ANSI (cores/cursor) ---
CSI = "\x1b["
RESET = "\x1b[0m"

def cor_ansi(fg=None, bold=False):
    partes = []
    if bold:
        partes.append("1")
    if fg is not None:
        partes.append(str(fg))
    return CSI + ";".join(partes) + "m" if partes else ""

COR_BORDA = cor_ansi(96, True)
COR_BOLA  = cor_ansi(93, True)
COR_REB   = cor_ansi(92, True)

def ocultar_cursor():
    sys.stdout.write(CSI + "?25l")
    sys.stdout.flush()

def mostrar_cursor():
    sys.stdout.write(CSI + "?25h" + RESET)
    sys.stdout.flush()

def usar_buffer_alternativo(ativar=True):
    sys.stdout.write(CSI + ("?1049h" if ativar else "?1049l"))
    sys.stdout.flush()

def mover_cursor_home():
    sys.stdout.write(CSI + "H")

def clamp(v, mn, mx):
    return mn if v < mn else mx if v > mx else v

# --- Config ---
LARGURA = 78
ALTURA = 22

ALTURA_PADDLE = 6
VEL_PADDLE = 1

FPS = 30
DT_FRAME = 1.0 / FPS

VEL_BOLA = 12.0  # células por segundo (ajuste aqui se quiser mais lento/rápido)

X_MIN = 1
X_MAX = LARGURA - 2
Y_MIN = 1
Y_MAX = ALTURA - 2

# Posição do paddle
paddle_x = X_MIN + 1
paddle_y = (Y_MIN + Y_MAX) // 2 - ALTURA_PADDLE // 2

# Bola (float)
bola = {"x": 0.0, "y": 0.0, "vx": 0.0, "vy": 0.0}

def vy_inicial():
    return random.choice([-0.6, -0.3, 0.3, 0.6])

def sacar():
    # bola nasce encostada no paddle e vai para a direita
    global bola
    centro = paddle_y + ALTURA_PADDLE // 2
    bola["x"] = float(paddle_x + 1)
    bola["y"] = float(centro)
    bola["vx"] = +1.0
    bola["vy"] = vy_inicial()

def ler_tecla():
    if not msvcrt.kbhit():
        return None
    t = msvcrt.getch()
    if t in (b"\x00", b"\xe0"):
        return t + msvcrt.getch()  # teclas especiais (setas)
    return t

def pos_int_bola():
    return int(round(bola["x"])), int(round(bola["y"]))

def desenhar():
    bx, by = pos_int_bola()

    linhas = []
    linhas.append(COR_BORDA + CANTO_SUPERIOR_ESQUERDO + (HORIZONTAL * (LARGURA - 2)) + CANTO_SUPERIOR_DIREITO + RESET)

    for y in range(1, ALTURA - 1):
        linha = [" "] * (LARGURA - 2)

        # paddle esquerdo
        if paddle_y <= y <= paddle_y + ALTURA_PADDLE - 1:
            px = paddle_x - 1
            if 0 <= px < len(linha):
                linha[px] = "█"

        # bola
        if y == by:
            x = bx - 1
            if 0 <= x < len(linha):
                linha[x] = "●"

        conteudo = "".join(linha)
        conteudo = conteudo.replace("█", COR_REB + "█" + RESET)
        conteudo = conteudo.replace("●", COR_BOLA + "●" + RESET)

        linhas.append(COR_BORDA + VERTICAL + RESET + conteudo + COR_BORDA + VERTICAL + RESET)

    linhas.append(COR_BORDA + CANTO_INFERIOR_ESQUERDO + (HORIZONTAL * (LARGURA - 2)) + CANTO_INFERIOR_DIREITO + RESET)
    return "\n".join(linhas)

def atualizar_bola(dt):
    global paddle_y

    # próxima posição
    prox_x = bola["x"] + bola["vx"] * VEL_BOLA * dt
    prox_y = bola["y"] + bola["vy"] * VEL_BOLA * dt

    # quique no teto/chão
    if prox_y < Y_MIN:
        prox_y = float(Y_MIN)
        bola["vy"] *= -1.0
    elif prox_y > Y_MAX:
        prox_y = float(Y_MAX)
        bola["vy"] *= -1.0

    # quique na parede direita (não há paddle)
    if prox_x > X_MAX:
        prox_x = float(X_MAX)
        bola["vx"] *= -1.0

    # colisão com paddle esquerdo (se cruzou a coluna do paddle)
    x_ant, y_ant = pos_int_bola()
    x_nov = int(round(prox_x))
    y_nov = int(round(prox_y))

    if bola["vx"] < 0 and x_nov <= paddle_x and x_ant >= paddle_x:
        if paddle_y <= y_nov <= paddle_y + ALTURA_PADDLE - 1:
            bola["vx"] = +1.0

            # ângulo baseado no ponto de impacto
            centro = paddle_y + ALTURA_PADDLE // 2
            denom = max(1, ALTURA_PADDLE // 2)
            offset = (y_nov - centro) / denom
            bola["vy"] = clamp(offset, -1.0, 1.0) or vy_inicial()

            prox_x = float(paddle_x + 1)

    # errou o paddle: reinicia (sem pontos)
    if prox_x < X_MIN:
        sacar()
        return

    bola["x"] = prox_x
    bola["y"] = prox_y

def main():
    global paddle_y

    usar_buffer_alternativo(True)
    ocultar_cursor()
    sys.stdout.write(CSI + "2J" + CSI + "H")
    sys.stdout.flush()

    sacar()

    try:
        ultimo = time.perf_counter()

        while True:
            agora = time.perf_counter()
            delta = agora - ultimo
            ultimo = agora
            if delta > 0.05:
                delta = 0.05

            # entrada
            while True:
                t = ler_tecla()
                if t is None:
                    break
                if t == b"\x1b":
                    return
                if t == b"\xe0H":       # ↑
                    paddle_y -= VEL_PADDLE
                elif t == b"\xe0P":     # ↓
                    paddle_y += VEL_PADDLE

            paddle_y = clamp(paddle_y, Y_MIN, Y_MAX - ALTURA_PADDLE + 1)

            atualizar_bola(delta)

            mover_cursor_home()
            sys.stdout.write(desenhar())
            sys.stdout.flush()

            time.sleep(max(0.0, DT_FRAME - (time.perf_counter() - agora)))

    finally:
        mostrar_cursor()
        usar_buffer_alternativo(False)

if __name__ == "__main__":
    main()
