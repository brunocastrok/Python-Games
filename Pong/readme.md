# 🏓 Pong para terminal Python (Windows)

Um jogo simples estilo Pong/Squash rodando inteiramente no terminal do Windows, escrito em Python puro. O jogo utiliza **ANSI escape sequences** para renderização colorida e **msvcrt** para controle de entrada sem bloqueio.

## 📋 Funcionalidades

* **Renderização Rápida:** Utiliza buffer alternativo e escape codes para evitar "flickering" (cintilação) no terminal.
* **Física Simples:** A bola rebate nas paredes e muda de ângulo dependendo de onde atinge a raquete (paddle).
* **Sem Dependências Externas:** Não requer `pygame` ou outras bibliotecas pesadas. Roda com a biblioteca padrão do Python.
* **Gráficos ASCII:** Interface limpa desenhada com caracteres Unicode.

## ⚠️ Pré-requisitos

Este código foi projetado especificamente para **Windows**.

* **Sistema Operacional:** Windows (devido ao uso da biblioteca `msvcrt`).
* **Linguagem:** Python 3.x.
* **Terminal:** Recomenda-se o uso do *Windows Terminal*, *PowerShell* ou *CMD* (Prompt de Comando).

> **Nota:** Se tentar rodar em Linux ou Mac, o script detectará a ausência do `msvcrt` e encerrará a execução automaticamente.

## 🚀 Como Executar

1.  Certifique-se de ter o Python instalado.
2.  Salve o código em um arquivo, por exemplo: `pong.py`.
3.  Abra seu terminal e navegue até a pasta do arquivo.
4.  Execute o comando:

```bash
python pong.py
