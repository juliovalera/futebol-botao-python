# âš½ Futebol de BotÃ£o â€” Jogo PedagÃ³gico em Python

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Pygame](https://img.shields.io/badge/Pygame--CE-2.5%2B-green?style=for-the-badge)
![LicenÃ§a](https://img.shields.io/badge/Licen%C3%A7a-MIT-yellow?style=for-the-badge)
![EducaÃ§Ã£o](https://img.shields.io/badge/Educa%C3%A7%C3%A3o-P%C3%BAblica-orange?style=for-the-badge)
![VersÃ£o](https://img.shields.io/badge/Vers%C3%A3o-2.0-purple?style=for-the-badge)

**Jogo pedagÃ³gico de Futebol de BotÃ£o desenvolvido em Python + Pygame**  
*Para aulas de MatemÃ¡tica, FÃ­sica e ProgramaÃ§Ã£o na rede pÃºblica de ensino*

</div>

---

## ðŸŽ® Sobre o Jogo

**Futebol de BotÃ£o** Ã© um jogo digital que simula o clÃ¡ssico futebol de mesa/botÃ£o, desenvolvido como ferramenta pedagÃ³gica para **estudantes do Ensino Fundamental e MÃ©dio**. Enquanto jogam, os alunos visualizam e praticam conceitos de **MatemÃ¡tica, FÃ­sica e LÃ³gica de ProgramaÃ§Ã£o** de forma lÃºdica e interativa.

O jogo Ã© **100% programado em Python**, sem imagens ou sons externos â€” todos os grÃ¡ficos, animaÃ§Ãµes, fÃ­sica e sons sÃ£o gerados pelo prÃ³prio cÃ³digo, tornando-o tambÃ©m uma excelente referÃªncia de aprendizado de programaÃ§Ã£o.

---

## ðŸ“¸ Telas do Jogo

| Menu Principal | Partida em andamento |
|:-:|:-:|
| *Menu com modos de jogo + tela Sobre* | *Campo com placar, cronÃ´metro, mira e painel de toques* |

> **Dica:** Execute o jogo e pressione **F11** para jogar em tela cheia!

---

## ðŸ§  Conceitos PedagÃ³gicos Abordados

Durante cada jogada, o jogo exibe mensagens relacionando a partida com conceitos reais:

| Conceito | Como aparece no jogo |
|---|---|
| **Ã‚ngulo e DireÃ§Ã£o** | A mira mostra o Ã¢ngulo em graus (Â°) em relaÃ§Ã£o ao eixo X |
| **Vetor de ForÃ§a** | Seta laranja mostra direÃ§Ã£o + intensidade da jogada |
| **Velocidade** | Quanto mais se arrasta o mouse, maior a velocidade inicial |
| **Atrito** | O botÃ£o desacelera gradualmente atÃ© parar |
| **ColisÃ£o** | BotÃ£o transfere momento linear para a bola |
| **Plano Cartesiano** | Cada objeto tem coordenadas (x, y) no campo |
| **Ondas Senoidais** | A rede balanÃ§a usando funÃ§Ãµes seno/cosseno |
| **Escala e ProporÃ§Ã£o** | Tela cheia usa transformaÃ§Ã£o de escala sem distorÃ§Ã£o |
| **Probabilidade** | Cara ou coroa sorteado aleatoriamente antes de cada partida |

---

## ðŸ•¹ï¸ Como Jogar

```
1. Escolha o modo de jogo (2 jogadores ou vs Computador)
2. Escolha o conjunto de regras (Normal ou 12 Toques)
3. Aguarde o cara ou coroa para saber quem comeÃ§a
4. Clique em um botÃ£o do seu time (cÃ­rculo azul ou vermelho)
5. Arraste o mouse para definir a direÃ§Ã£o e a forÃ§a
6. Solte o mouse para chutar!
7. Leve a bola atÃ© o gol adversÃ¡rio
8. Vence quem marcar mais gols em 2 minutos
```

### Modos de Jogo
- **ðŸŽ® 2 Jogadores** â€” dois jogadores no mesmo computador, alternando turnos
- **ðŸ¤– vs Computador** â€” jogue contra uma IA com estratÃ©gia posicional

### Conjuntos de Regras
- **âšª Regra Normal** â€” times alternam jogadas sem limite de toques
- **ðŸ”´ Regra dos 12 Toques** â€” sistema de posse com regras completas (ver seÃ§Ã£o abaixo)

### Controles
| AÃ§Ã£o | Controle |
|---|---|
| Selecionar botÃ£o | Clique esquerdo no cÃ­rculo |
| Mirar | Arrastar o mouse |
| Chutar | Soltar o mouse |
| Tela cheia | F11 ou botÃ£o â›¶ no canto |
| Voltar ao menu | ESC |

---

## ðŸ”´ Regra dos 12 Toques

A **Regra dos 12 Toques** simula as regras oficiais do futebol de botÃ£o com sistema de posse:

### Como funciona a posse
- A equipe que estÃ¡ com a posse pode acumular **atÃ© 12 toques coletivos** consecutivos
- Cada botÃ£o individual pode tocar a bola no **mÃ¡ximo 3 vezes** por posse
- A posse se mantÃ©m enquanto as regras forem respeitadas
- Ao atingir 12 toques coletivos, a posse Ã© encerrada e transferida ao adversÃ¡rio

### Faltas (transferem a posse imediatamente)
| SituaÃ§Ã£o | Mensagem exibida |
|---|---|
| O botÃ£o lanÃ§ado nÃ£o toca a bola | *"FALTA! O botÃ£o nÃ£o tocou na bola."* |
| BotÃ£o adversÃ¡rio tocado antes da bola | *"FALTA! AdversÃ¡rio tocado antes da bola."* |
| BotÃ£o individual ultrapassou 3 toques | *"FALTA! BotÃ£o X ultrapassou 3 toques individuais."* |
| A bola toca um botÃ£o adversÃ¡rio | *"A bola tocou o adversÃ¡rio! Posse transferida."* |
| Tempo de 5 segundos esgotado sem jogar | *"TEMPO ESGOTADO! (mÃ¡x. 5 segundos)"* |

### Painel no HUD (canto esquerdo)
- **Toques: X/12** â€” contador da posse atual (muda de cor conforme se aproxima do limite)
- **REGRA: 12 TOQUES** â€” indicaÃ§Ã£o visual da regra ativa
- **â± Xs** â€” cronÃ´metro regressivo de 5 segundos para o jogador efetuar a jogada
- Cada botÃ£o exibe **X/3** embaixo indicando seus toques individuais; botÃµes esgotados ficam escuros e nÃ£o podem ser selecionados

---

## âœ¨ Funcionalidades

- ðŸª™ **Cara ou coroa** animado antes de cada partida para sortear quem comeÃ§a
- âš–ï¸ **Escolha de regras** com tela dedicada (Regra Normal ou 12 Toques)
- ðŸ¤– **IA aprimorada** com modo defensivo, mira calculada e seleÃ§Ã£o posicional de botÃ£o
- â±ï¸ **CronÃ´metro regressivo** de 2 minutos com alerta nos Ãºltimos 30s
- â³ **Timer de 5s por jogada** na Regra dos 12 Toques
- ðŸ”„ **TransferÃªncia de posse** ao tocar botÃ£o adversÃ¡rio (antes da bola) ou a bola tocar o adversÃ¡rio
- âš½ **DetecÃ§Ã£o de gol** com celebraÃ§Ã£o animada
- ðŸŽ‰ **Confete colorido** com fÃ­sica de partÃ­culas (gravidade + atrito)
- ðŸ”Š **Sons sintetizados** em cÃ³digo: chute, colisÃ£o de botÃµes, colisÃ£o com bola e fanfarra de gol
- ðŸ¥… **Rede balanÃ§ando** apÃ³s o gol (animaÃ§Ã£o com seno/cosseno amortecido)
- ðŸ’¡ **Mensagens pedagÃ³gicas** rotativas durante o jogo
- ðŸ“ **Mira com Ã¢ngulo e forÃ§a** exibidos em tempo real
- ðŸ–¥ï¸ **Tela cheia** com escala letterbox (mantÃ©m proporÃ§Ã£o)
- â„¹ï¸ **Tela "Sobre"** com crÃ©ditos e objetivos pedagÃ³gicos
- ðŸŽ¨ **100% sem arquivos externos** â€” grÃ¡ficos e sons gerados em cÃ³digo

---

## ðŸš€ InstalaÃ§Ã£o e ExecuÃ§Ã£o

### Passo 1 â€” Instale o Python

Acesse **https://www.python.org/downloads** e instale a versÃ£o mais recente.  
> Marque a opÃ§Ã£o **"Add Python to PATH"** durante a instalaÃ§Ã£o.

### Passo 2 â€” Baixe o jogo

**OpÃ§Ã£o A â€” Com Git instalado:**
```bash
git clone https://github.com/juliovalera/futebol-botao-python.git
cd futebol-botao-python
```

**OpÃ§Ã£o B â€” Sem Git (mais simples):**
1. Clique no botÃ£o verde **`<> Code`** nesta pÃ¡gina
2. Escolha **`Download ZIP`**
3. Extraia o arquivo ZIP em uma pasta de sua preferÃªncia

### Passo 3 â€” Instale o Pygame

Abra o terminal (Prompt de Comando ou PowerShell) dentro da pasta do jogo e execute:

```bash
pip install pygame-ce
```

> âš ï¸ **AtenÃ§Ã£o:** Use sempre `pygame-ce` (Community Edition) â€” compatÃ­vel com todas as versÃµes recentes do Python.

### Passo 4 â€” Execute o jogo

```bash
python main.py
```

Pronto! A janela do jogo vai abrir. Pressione **F11** para tela cheia. ðŸŽ®

---

## ðŸ—‚ï¸ Estrutura do Projeto

```
futebol-botao-python/
â”‚
â”œâ”€â”€ main.py          # CÃ³digo principal â€” todo o jogo em um Ãºnico arquivo
â”œâ”€â”€ .gitignore       # Arquivos ignorados pelo Git
â””â”€â”€ README.md        # Este arquivo
```

### OrganizaÃ§Ã£o do cÃ³digo (`main.py`)

| SeÃ§Ã£o | DescriÃ§Ã£o |
|---|---|
| `Constantes` | DimensÃµes, cores, fÃ­sica, modos de jogo |
| `Controle de tela cheia` | `alternar_tela_cheia()`, `atualizar_tela()`, `escalar_mouse()` |
| `criar_sons()` | SÃ­ntese de Ã¡udio via ondas senoidais puras |
| `class Objeto` | Classe base: posiÃ§Ã£o, velocidade, atrito, colisÃ£o |
| `class Botao` | PeÃ§a do jogador com seleÃ§Ã£o, desenho e indicador de toques |
| `class Bola` | Bola com detecÃ§Ã£o de gol |
| `class Particula` | Confete animado com gravidade |
| `desenhar_campo()` | Campo, linhas, cÃ­rculo central, Ã¡reas |
| `desenhar_redes()` | Redes com animaÃ§Ã£o senoidal de balanÃ§o |
| `desenhar_hud()` | Placar, cronÃ´metro, painel de 12 toques, mensagens pedagÃ³gicas |
| `desenhar_mira()` | Seta de forÃ§a com Ã¢ngulo e % de forÃ§a |
| `desenhar_celebracao_gol()` | Flash, GOOOOOL! pulsante, confete |
| `jogada_computador()` | IA com modo defensivo e mira posicional |
| `tela_cara_ou_coroa()` | AnimaÃ§Ã£o de moeda girando para sortear quem comeÃ§a |
| `tela_regras()` | Tela de seleÃ§Ã£o entre Regra Normal e 12 Toques |
| `tela_sobre()` | CrÃ©ditos com scroll e estrelas animadas |
| `tela_menu()` | Menu principal |
| `rodar_jogo()` | Loop principal: eventos, fÃ­sica, regras de posse, desenho |

---

## ðŸ“‹ HistÃ³rico de VersÃµes

### v2.0 â€” Julho de 2026
**Novas funcionalidades:**
- ðŸª™ Tela de **cara ou coroa** animada antes de cada partida (moeda com rotaÃ§Ã£o 3D simulada)
- âš–ï¸ **Tela de seleÃ§Ã£o de regras**: Regra Normal ou Regra dos 12 Toques
- ðŸ”´ **Regra dos 12 Toques** completa:
  - Limite de 12 toques coletivos por posse
  - Limite de 3 toques individuais por botÃ£o
  - Falta ao errar a bola, tocar adversÃ¡rio antes da bola ou ultrapassar limite individual
  - **Timer de 5 segundos** por jogada (falta ao estourar o tempo)
  - TransferÃªncia de posse quando a bola toca um botÃ£o adversÃ¡rio
  - Painel visual no HUD com contador de toques, timer e indicador por botÃ£o
  - BotÃµes esgotados ficam escuros e nÃ£o selecionÃ¡veis

**Melhorias na IA:**
- Modo **defensivo** ativado quando a bola estÃ¡ prÃ³xima do prÃ³prio gol
- **SeleÃ§Ã£o posicional** de botÃ£o baseada em alinhamento botÃ£oâ†’bolaâ†’gol (cosseno vetorial)
- **Mira calculada** para deflectir a bola em direÃ§Ã£o ao gol adversÃ¡rio
- Erro de pontaria reduzido (Â±0,15 rad â†’ mais precisa)
- ForÃ§a variÃ¡vel: suave em tiros curtos, potente em tiros longos
- Respeita o limite de 3 toques individuais na Regra dos 12 Toques

**CorreÃ§Ãµes:**
- Corrigido bug em que a bola tocando o botÃ£o adversÃ¡rio nÃ£o transferia a posse (velocidade da bola agora Ã© capturada *antes* da colisÃ£o para detecÃ§Ã£o correta)

### v1.0 â€” Julho de 2026
- VersÃ£o inicial com campo, fÃ­sica, colisÃµes, placar e cronÃ´metro
- Modos: 2 Jogadores e vs Computador
- Sons sintetizados, celebraÃ§Ã£o de gol com confete, tela cheia (F11)
- Mensagens pedagÃ³gicas rotativas
- Tela "Sobre" com crÃ©ditos

---

## ðŸ”­ Melhorias Futuras

- [ ] Mais botÃµes por time (goleiro, zagueiro, meia, atacante)
- [ ] Sons com arquivo `.wav` ou `.ogg` de maior qualidade
- [ ] Textura de grama no campo
- [ ] Perguntas de matemÃ¡tica integradas Ã s jogadas
- [ ] Modo torneio com placar acumulado
- [ ] EstatÃ­sticas da partida (chutes, distÃ¢ncia percorrida)
- [ ] SeleÃ§Ã£o de times e cores personalizadas
- [ ] IA com nÃ­vel de dificuldade ajustÃ¡vel

---

## ðŸ‘¨â€ðŸ« Autor

<div align="center">

**JÃºlio CÃ©sar Valera**  
Professor de MatemÃ¡tica, ProgramaÃ§Ã£o e RobÃ³tica  
Rede PÃºblica de Ensino â€” SÃ£o Paulo / SP  

*"Aprender programando, jogar aprendendo."*

</div>

---

## ðŸ« Para Educadores

Este projeto Ã© **livre para uso em sala de aula**. SugestÃµes de uso:

1. **Jogar primeiro** â€” deixe os alunos explorarem o jogo livremente
2. **Discutir a fÃ­sica** â€” pause e pergunte: *"Por que o botÃ£o para?"*, *"O que Ã© o vetor?"*
3. **Explorar o cÃ³digo** â€” mostre o `main.py` e identifique as funÃ§Ãµes juntos
4. **Propor desafios** â€” peÃ§a aos alunos que modifiquem cores, velocidade ou tamanho dos botÃµes
5. **Projetos** â€” use como base para criar variaÃ§Ãµes com novas regras

---

## ðŸ“„ LicenÃ§a

Este projeto Ã© distribuÃ­do sob a licenÃ§a **MIT** â€” livre para usar, copiar, modificar e distribuir, inclusive para fins comerciais e educacionais, desde que mantidos os crÃ©ditos ao autor.

---

<div align="center">

Feito com â¤ï¸ para a educaÃ§Ã£o pÃºblica paulista  
**Julho de 2026**

</div>


