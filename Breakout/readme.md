# Jogo Breakout no Terminal

## Descrição

Este é um jogo simples de Breakout implementado em Python, projetado para rodar diretamente no terminal. O objetivo é quebrar todos os tijolos com uma bola quicando, controlando uma raquete (paddle) para rebater a bola. O jogo usa caracteres ASCII e cores ANSI para criar uma experiência visual divertida e nostálgica.

O jogo inclui:
- Movimentação fluida da bola com física básica (incluindo ângulos variados ao rebater na raquete).
- Tijolos distribuídos em fileiras.
- Pontuação baseada na destruição de tijolos.
- Condições de vitória (todos os tijolos destruídos) e derrota (bola cai abaixo da raquete).

## Requisitos

- **Python 3.x** (testado em Python 3.12, mas compatível com versões recentes).
- **Sistema Operacional**: Windows (devido ao uso da biblioteca `msvcrt` para detecção de teclas em tempo real). Para rodar em Linux ou macOS, seria necessário adaptar o código para usar bibliotecas cross-platform como `curses` ou `keyboard`.
- Nenhum pacote externo é necessário; o jogo usa apenas módulos padrão do Python (`os`, `time`, `msvcrt`, `random`).

## Instalação

1. Clone ou baixe este repositório.
2. Certifique-se de que o arquivo `breakout.py` está no diretório desejado.

## Como Executar

Abra o terminal (Prompt de Comando no Windows) e execute:

```
python breakout.py
```

O jogo iniciará imediatamente, limpando a tela e exibindo o quadro do jogo.

## Controles

- **Seta Esquerda (←)**: Move a raquete para a esquerda.
- **Seta Direita (→)**: Move a raquete para a direita.
- **Q**: Sai do jogo a qualquer momento.

Nota: Os controles usam detecção de teclas em tempo real, sem necessidade de pressionar Enter.

## Configurações Personalizáveis

No código-fonte (`breakout.py`), você pode ajustar as seguintes variáveis para modificar o jogo:
- `LARGURA` e `ALTURA`: Dimensões do campo de jogo.
- `PADDLE_TAMANHO`: Tamanho da raquete.
- `FPS`: Velocidade do jogo (menor valor = mais rápido).
- Velocidades iniciais da bola (`vel_x`, `vel_y`).
- Cores ANSI para bordas, raquete, bola e tijolos.

## Exemplos de Execução

- Ao iniciar, você verá uma borda, tijolos no topo, a raquete na base e a bola começando a se mover.
- Destrua tijolos para aumentar a pontuação (10 pontos por tijolo).
- Se a bola cair abaixo da raquete, o jogo termina com a mensagem "FIM DE JOGO!".
- Se todos os tijolos forem destruídos, aparece "VITORIA!".

## Limitações

- O jogo é otimizado para terminais com suporte a ANSI (a maioria dos terminais modernos).
- Em terminais muito pequenos, o layout pode se desconfigurar; recomenda-se uma janela de pelo menos 60 colunas de largura.
- Não há suporte a pausa ou níveis múltiplos nesta versão básica.

## Contribuições

Sinta-se à vontade para forkear o repositório e sugerir melhorias, como:
- Suporte cross-platform para input de teclado.
- Adição de power-ups ou níveis.
- Melhoria na física da bola.

## Licença

Este projeto é de código aberto sob a licença MIT. Sinta-se livre para usar, modificar e distribuir.
