# 🏎️ Fórmula 1 - Python Console Game

Um jogo de corrida vertical simples e divertido, desenvolvido inteiramente em Python para rodar diretamente no terminal (prompt de comando). O projeto utiliza **ASCII Art** para os gráficos e **códigos ANSI** para colorização, sem necessidade de instalar bibliotecas pesadas de jogos.

---

## 📸 Preview

```text
╭───────────────────╮
│ PONTOS: 0015      │
├───────────────────┤
│ . │ . │ . │ . │ . │
│ . │ ▼ │ . │ . │ . │  <-- Inimigos (Vermelho)
│ . │ . │ . │ . │ . │
│ . │ . │ . │ . │ . │
│ . │ . │ ▲ │ . │ . │  <-- Você (Verde)
╰───────────────────╯
```

## 🎮 Como Jogar

O objetivo é simples: desvie dos carros inimigos e sobreviva o maior tempo possível para aumentar sua pontuação.

### Controles

| Tecla | Ação |
| :---: | :--- |
| **⬅️ Seta Esquerda** | Move o carro para a esquerda |
| **➡️ Seta Direita** | Move o carro para a direita |
| **ESC** | Sai do jogo imediatamente |

> **Nota:** A velocidade do jogo aumenta progressivamente conforme você ganha pontos!

---

## 🛠️ Requisitos

* **Sistema Operacional:** Windows (Este jogo usa a biblioteca `msvcrt`, que é nativa apenas no Windows).
* **Linguagem:** Python 3.x instalado.

## 🚀 Como Executar

1. Certifique-se de ter o Python instalado.
2. Baixe ou clone este repositório.
3. Abra o terminal (CMD ou PowerShell) na pasta do arquivo.
4. Execute o comando:

```bash
python formula1.py
```

---

## 🧩 Como Funciona (Por baixo do capô)

Este jogo é um excelente exemplo de como manipular o terminal sem interfaces gráficas complexas:

1. **Renderização:** O "mapa" é uma matriz de caracteres redesenhada a cada quadro.
2. **Cores:** Utilizamos códigos de escape ANSI (ex: `\033[94m`) para pintar o texto de Azul, Verde e Vermelho.
3. **Input:** A biblioteca `msvcrt` detecta o pressionamento de teclas em tempo real sem pausar o jogo (input não-bloqueante).
4. **Game Loop:** Um loop `while True` controla a lógica, atualização de posição e o tempo de espera (FPS) para manter a fluidez.

---

## 📝 Estrutura do Código

* `preparar_terminal()`: Limpa a tela e esconde o cursor piscante.
* `obter_copia_do_mapa()`: Cria uma versão editável do cenário base.
* `iniciar_jogo()`: Contém toda a lógica principal, detecção de colisão e controle de pontuação.

---

## ⚠️ Problemas Comuns

**O jogo não tem cores ou aparecem códigos estranhos (ex: `[94m`)?**
* Isso acontece se o seu terminal não suportar códigos ANSI. O CMD do Windows 10/11 e o PowerShell moderno suportam nativamente. Se estiver usando uma versão muito antiga do Windows, tente usar um emulador de terminal como o **Cmder** ou o novo **Windows Terminal**.

---

Desenvolvido para fins educacionais. Sinta-se à vontade para modificar e melhorar!
