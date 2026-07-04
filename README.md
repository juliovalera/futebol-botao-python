# ⚽ Futebol de Botão — Jogo Pedagógico em Python

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Pygame](https://img.shields.io/badge/Pygame--CE-2.5%2B-green?style=for-the-badge)
![Licença](https://img.shields.io/badge/Licen%C3%A7a-MIT-yellow?style=for-the-badge)
![Educação](https://img.shields.io/badge/Educa%C3%A7%C3%A3o-P%C3%BAblica-orange?style=for-the-badge)
![Versão](https://img.shields.io/badge/Vers%C3%A3o-2.0-purple?style=for-the-badge)

**Jogo pedagógico de Futebol de Botão desenvolvido em Python + Pygame**  
*Para aulas de Matemática, Física e Programação na rede pública de ensino*

</div>

---

## 🎮 Sobre o Jogo

**Futebol de Botão** é um jogo digital que simula o clássico futebol de mesa/botão, desenvolvido como ferramenta pedagógica para **estudantes do Ensino Fundamental e Médio**. Enquanto jogam, os alunos visualizam e praticam conceitos de **Matemática, Física e Lógica de Programação** de forma lúdica e interativa.

O jogo é **100% programado em Python**, sem imagens ou sons externos — todos os gráficos, animações, física e sons são gerados pelo próprio código, tornando-o também uma excelente referência de aprendizado de programação.

---

## 📸 Telas do Jogo

| Menu Principal | Partida em andamento |
|:-:|:-:|
| *Menu com modos de jogo + tela Sobre* | *Campo com placar, cronômetro, mira e painel de toques* |

> **Dica:** Execute o jogo e pressione **F11** para jogar em tela cheia!

---

## 🧠 Conceitos Pedagógicos Abordados

Durante cada jogada, o jogo exibe mensagens relacionando a partida com conceitos reais:

| Conceito | Como aparece no jogo |
|---|---|
| **Ângulo e Direção** | A mira mostra o ângulo em graus (°) em relação ao eixo X |
| **Vetor de Força** | Seta laranja mostra direção + intensidade da jogada |
| **Velocidade** | Quanto mais se arrasta o mouse, maior a velocidade inicial |
| **Atrito** | O botão desacelera gradualmente até parar |
| **Colisão** | Botão transfere momento linear para a bola |
| **Plano Cartesiano** | Cada objeto tem coordenadas (x, y) no campo |
| **Ondas Senoidais** | A rede balança usando funções seno/cosseno |
| **Escala e Proporção** | Tela cheia usa transformação de escala sem distorção |
| **Probabilidade** | Cara ou coroa sorteado aleatoriamente antes de cada partida |

---

## 🕹️ Como Jogar

```
1. Escolha o modo de jogo (2 jogadores ou vs Computador)
2. Escolha o conjunto de regras (Normal ou 12 Toques)
3. Aguarde o cara ou coroa para saber quem começa
4. Clique em um botão do seu time (círculo azul ou vermelho)
5. Arraste o mouse para definir a direção e a força
6. Solte o mouse para chutar!
7. Leve a bola até o gol adversário
8. Vence quem marcar mais gols em 2 minutos
```

### Modos de Jogo
- **🎮 2 Jogadores** — dois jogadores no mesmo computador, alternando turnos
- **🤖 vs Computador** — jogue contra uma IA com estratégia posicional

### Conjuntos de Regras
- **⚪ Regra Normal** — times alternam jogadas sem limite de toques
- **🔴 Regra dos 12 Toques** — sistema de posse com regras completas (ver seção abaixo)

### Controles
| Ação | Controle |
|---|---|
| Selecionar botão | Clique esquerdo no círculo |
| Mirar | Arrastar o mouse |
| Chutar | Soltar o mouse |
| Tela cheia | F11 ou botão ⛶ no canto |
| Voltar ao menu | ESC |

---

## 🔴 Regra dos 12 Toques

A **Regra dos 12 Toques** simula as regras oficiais do futebol de botão com sistema de posse:

### Como funciona a posse
- A equipe que está com a posse pode acumular **até 12 toques coletivos** consecutivos
- Cada botão individual pode tocar a bola no **máximo 3 vezes** por posse
- A posse se mantém enquanto as regras forem respeitadas
- Ao atingir 12 toques coletivos, a posse é encerrada e transferida ao adversário

### Faltas (transferem a posse imediatamente)
| Situação | Mensagem exibida |
|---|---|
| O botão lançado não toca a bola | *"FALTA! O botão não tocou na bola."* |
| Botão adversário tocado antes da bola | *"FALTA! Adversário tocado antes da bola."* |
| Botão individual ultrapassou 3 toques | *"FALTA! Botão X ultrapassou 3 toques individuais."* |
| A bola toca um botão adversário | *"A bola tocou o adversário! Posse transferida."* |
| Tempo de 5 segundos esgotado sem jogar | *"TEMPO ESGOTADO! (máx. 5 segundos)"* |

### Painel no HUD (canto esquerdo)
- **Toques: X/12** — contador da posse atual (muda de cor conforme se aproxima do limite)
- **REGRA: 12 TOQUES** — indicação visual da regra ativa
- **⏱ Xs** — cronômetro regressivo de 5 segundos para o jogador efetuar a jogada
- Cada botão exibe **X/3** embaixo indicando seus toques individuais; botões esgotados ficam escuros e não podem ser selecionados

---

## ✨ Funcionalidades

- 🪙 **Cara ou coroa** animado antes de cada partida para sortear quem começa
- ⚖️ **Escolha de regras** com tela dedicada (Regra Normal ou 12 Toques)
- 🤖 **IA aprimorada** com modo defensivo, mira calculada e seleção posicional de botão
- ⏱️ **Cronômetro regressivo** de 2 minutos com alerta nos últimos 30s
- ⏳ **Timer de 5s por jogada** na Regra dos 12 Toques
- 🔄 **Transferência de posse** ao tocar botão adversário (antes da bola) ou a bola tocar o adversário
- ⚽ **Detecção de gol** com celebração animada
- 🎉 **Confete colorido** com física de partículas (gravidade + atrito)
- 🔊 **Sons sintetizados** em código: chute, colisão de botões, colisão com bola e fanfarra de gol
- 🥅 **Rede balançando** após o gol (animação com seno/cosseno amortecido)
- 💡 **Mensagens pedagógicas** rotativas durante o jogo
- 📐 **Mira com ângulo e força** exibidos em tempo real
- 🖥️ **Tela cheia** com escala letterbox (mantém proporção)
- ℹ️ **Tela "Sobre"** com créditos e objetivos pedagógicos
- 🎨 **100% sem arquivos externos** — gráficos e sons gerados em código

---

## 🚀 Instalação e Execução

### Passo 1 — Instale o Python

Acesse **https://www.python.org/downloads** e instale a versão mais recente.  
> Marque a opção **"Add Python to PATH"** durante a instalação.

### Passo 2 — Baixe o jogo

**Opção A — Com Git instalado:**
```bash
git clone https://github.com/juliovalera/futebol-botao-python.git
cd futebol-botao-python
```

**Opção B — Sem Git (mais simples):**
1. Clique no botão verde **`<> Code`** nesta página
2. Escolha **`Download ZIP`**
3. Extraia o arquivo ZIP em uma pasta de sua preferência

### Passo 3 — Instale o Pygame

Abra o terminal (Prompt de Comando ou PowerShell) dentro da pasta do jogo e execute:

```bash
pip install pygame-ce
```

> ⚠️ **Atenção:** Use sempre `pygame-ce` (Community Edition) — compatível com todas as versões recentes do Python.

### Passo 4 — Execute o jogo

```bash
python main.py
```

Pronto! A janela do jogo vai abrir. Pressione **F11** para tela cheia. 🎮

---

## 🗂️ Estrutura do Projeto

```
futebol-botao-python/
│
├── main.py          # Código principal — todo o jogo em um único arquivo
├── .gitignore       # Arquivos ignorados pelo Git
└── README.md        # Este arquivo
```

### Organização do código (`main.py`)

| Seção | Descrição |
|---|---|
| `Constantes` | Dimensões, cores, física, modos de jogo |
| `Controle de tela cheia` | `alternar_tela_cheia()`, `atualizar_tela()`, `escalar_mouse()` |
| `criar_sons()` | Síntese de áudio via ondas senoidais puras |
| `class Objeto` | Classe base: posição, velocidade, atrito, colisão |
| `class Botao` | Peça do jogador com seleção, desenho e indicador de toques |
| `class Bola` | Bola com detecção de gol |
| `class Particula` | Confete animado com gravidade |
| `desenhar_campo()` | Campo, linhas, círculo central, áreas |
| `desenhar_redes()` | Redes com animação senoidal de balanço |
| `desenhar_hud()` | Placar, cronômetro, painel de 12 toques, mensagens pedagógicas |
| `desenhar_mira()` | Seta de força com ângulo e % de força |
| `desenhar_celebracao_gol()` | Flash, GOOOOOL! pulsante, confete |
| `jogada_computador()` | IA com modo defensivo e mira posicional |
| `tela_cara_ou_coroa()` | Animação de moeda girando para sortear quem começa |
| `tela_regras()` | Tela de seleção entre Regra Normal e 12 Toques |
| `tela_sobre()` | Créditos com scroll e estrelas animadas |
| `tela_menu()` | Menu principal |
| `rodar_jogo()` | Loop principal: eventos, física, regras de posse, desenho |

---

## 📋 Histórico de Versões

### v2.0 — Julho de 2026
**Novas funcionalidades:**
- 🪙 Tela de **cara ou coroa** animada antes de cada partida (moeda com rotação 3D simulada)
- ⚖️ **Tela de seleção de regras**: Regra Normal ou Regra dos 12 Toques
- 🔴 **Regra dos 12 Toques** completa:
  - Limite de 12 toques coletivos por posse
  - Limite de 3 toques individuais por botão
  - Falta ao errar a bola, tocar adversário antes da bola ou ultrapassar limite individual
  - **Timer de 5 segundos** por jogada (falta ao estourar o tempo)
  - Transferência de posse quando a bola toca um botão adversário
  - Painel visual no HUD com contador de toques, timer e indicador por botão
  - Botões esgotados ficam escuros e não selecionáveis

**Melhorias na IA:**
- Modo **defensivo** ativado quando a bola está próxima do próprio gol
- **Seleção posicional** de botão baseada em alinhamento botão→bola→gol (cosseno vetorial)
- **Mira calculada** para deflectir a bola em direção ao gol adversário
- Erro de pontaria reduzido (±0,15 rad → mais precisa)
- Força variável: suave em tiros curtos, potente em tiros longos
- Respeita o limite de 3 toques individuais na Regra dos 12 Toques

**Correções:**
- Corrigido bug em que a bola tocando o botão adversário não transferia a posse (velocidade da bola agora é capturada *antes* da colisão para detecção correta)

### v1.0 — Julho de 2026
- Versão inicial com campo, física, colisões, placar e cronômetro
- Modos: 2 Jogadores e vs Computador
- Sons sintetizados, celebração de gol com confete, tela cheia (F11)
- Mensagens pedagógicas rotativas
- Tela "Sobre" com créditos

---

## 🔭 Melhorias Futuras

- [ ] Mais botões por time (goleiro, zagueiro, meia, atacante)
- [ ] Sons com arquivo `.wav` ou `.ogg` de maior qualidade
- [ ] Textura de grama no campo
- [ ] Perguntas de matemática integradas às jogadas
- [ ] Modo torneio com placar acumulado
- [ ] Estatísticas da partida (chutes, distância percorrida)
- [ ] Seleção de times e cores personalizadas
- [ ] IA com nível de dificuldade ajustável

---

## 👨‍🏫 Autor

<div align="center">

**Júlio César Valera**  
Professor de Matemática, Programação e Robótica  
Rede Pública de Ensino — São Paulo / SP  

*"Aprender programando, jogar aprendendo."*

</div>

---

## 🏫 Para Educadores

Este projeto é **livre para uso em sala de aula**. Sugestões de uso:

1. **Jogar primeiro** — deixe os alunos explorarem o jogo livremente
2. **Discutir a física** — pause e pergunte: *"Por que o botão para?"*, *"O que é o vetor?"*
3. **Explorar o código** — mostre o `main.py` e identifique as funções juntos
4. **Propor desafios** — peça aos alunos que modifiquem cores, velocidade ou tamanho dos botões
5. **Projetos** — use como base para criar variações com novas regras

---

## 📄 Licença

Este projeto é distribuído sob a licença **MIT** — livre para usar, copiar, modificar e distribuir, inclusive para fins comerciais e educacionais, desde que mantidos os créditos ao autor.

---

<div align="center">

Feito com ❤️ para a educação pública paulista  
**Julho de 2026**

</div>


