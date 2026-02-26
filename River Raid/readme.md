# 🛩️ River Raid Terminal (Python + Curses)

Um clone simplificado e nostálgico do clássico jogo **River Raid** (do lendário Atari 2600), desenvolvido inteiramente em Python para ser jogado direto no terminal do seu computador. Desvie das margens, destrua inimigos e gerencie seu combustível para alcançar a maior pontuação possível!

## 📌 Sobre o Projeto

Este jogo utiliza a biblioteca `curses` para renderizar gráficos baseados em texto (ASCII/Unicode) diretamente no console. Ele apresenta mecânicas fiéis ao jogo original:
* Geração procedural do rio (retas e diagonais dinâmicas).
* Sistema de consumo e reabastecimento de combustível.
* Detecção de colisão (tiros e cenário).
* Tela de "Game Over" detalhando a causa da sua derrota.

## ⚙️ Pré-requisitos

Para rodar este jogo, você precisa ter o **Python 3.x** instalado em sua máquina. 

**Atenção usuários de Windows:** A biblioteca `curses` vem nativamente no Linux e no macOS. Se você estiver usando Windows, precisará instalar um pacote de compatibilidade antes de rodar o jogo. Basta executar o comando abaixo no seu terminal ou prompt de comando:

```bash
pip install windows-curses
```

## 🚀 Como Executar

1. Salve o código em um arquivo chamado `river_raid.py`.
2. Abra o seu terminal (ou Prompt de Comando/PowerShell).
3. Navegue até a pasta onde o arquivo foi salvo.
4. Execute o comando:

```bash
python river_raid.py
```
*(Dica: Jogue com o terminal maximizado para ter uma visão melhor e dar mais espaço para o rio se movimentar).*

## 🎮 Controles do Jogo

| Tecla | Ação |
| :--- | :--- |
| **Seta para a Esquerda** (`←`) | Move o avião para a esquerda |
| **Seta para a Direita** (`→`) | Move o avião para a direita |
| **Espaço** (`␣`) | Dispara tiros (limite de 3 simultâneos na tela) |
| **Q** ou **ESC** | Abandona a partida em andamento / Sai do jogo |

## 🕹️ Elementos e Mecânicas

### O Cenário
* **Água (`≈` azul):** Área segura por onde o avião deve voar.
* **Margens (`█` verde):** Terra firme. Tocar nelas resulta em explosão e Game Over imediato.

### Inimigos e Pontuação
Atirar em alvos não apenas limpa o seu caminho, mas também aumenta o seu *Score*:
* **Barco (`▅▄ ` branco):** Move-se horizontalmente pelo rio. Vale **50 pontos**.
* **Helicóptero (`━┳━` vermelho):** Mais agressivo visualmente, também se move pelos lados. Vale **50 pontos**.
* **Tanque de Combustível (`[F]` magenta):** Fica estático no rio. Atirar nele garante **80 pontos**, mas destrói sua chance de reabastecer!

### Gerenciamento de Combustível (Fuel)
No painel inferior, você verá a barra `FUEL: E[████████  ]F`. Seu combustível diminui constantemente durante o voo.
* **Para reabastecer:** Voe **por cima** (sem atirar!) de um tanque de combustível `[F]`. A barra encherá rapidamente.
* **Pane Seca:** Se a barra esvaziar completamente, seu avião cai e o jogo termina.
