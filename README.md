# ⚽ Futebol de Botão — Jogo Pedagógico em Python

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Pygame](https://img.shields.io/badge/Pygame--CE-2.5%2B-green?style=for-the-badge)
![Licença](https://img.shields.io/badge/Licen%C3%A7a-MIT-yellow?style=for-the-badge)
![Educação](https://img.shields.io/badge/Educa%C3%A7%C3%A3o-P%C3%BAblica-orange?style=for-the-badge)
![Versão](https://img.shields.io/badge/Vers%C3%A3o-1.0-purple?style=for-the-badge)

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
| *Menu com 3 modos + tela Sobre* | *Campo com placar, cronômetro e mira* |

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

---

## 🕹️ Como Jogar

```
1. Clique em um botão do seu time (círculo azul ou vermelho)
2. Arraste o mouse para definir a direção e a força
3. Solte o mouse para chutar!
4. Leve a bola até o gol adversário
5. Vence quem marcar mais gols em 2 minutos
```

### Modos de Jogo
- **🎮 2 Jogadores** — dois jogadores no mesmo computador, alternando turnos
- **🤖 vs Computador** — jogue contra uma IA simples

### Controles
| Ação | Controle |
|---|---|
| Selecionar botão | Clique esquerdo no círculo |
| Mirar | Arrastar o mouse |
| Chutar | Soltar o mouse |
| Tela cheia | F11 ou botão ⛶ no canto |
| Voltar ao menu | ESC |

---

## ✨ Funcionalidades

- ⏱️ **Cronômetro regressivo** de 2 minutos com alerta nos últimos 30s
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

### Pré-requisitos
- Python 3.10 ou superior

### Instalar dependências

```bash
pip install pygame-ce
```

> ⚠️ **Atenção:** Se você tiver Python 3.13+, use `pygame-ce` (Community Edition) em vez de `pygame`, pois o pygame clássico ainda não tem binário pré-compilado para versões mais recentes do Python.

### Executar o jogo

```bash
python main.py
```

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
| `class Botao` | Peça do jogador com seleção e desenho |
| `class Bola` | Bola com detecção de gol |
| `class Particula` | Confete animado com gravidade |
| `desenhar_campo()` | Campo, linhas, círculo central, áreas |
| `desenhar_redes()` | Redes com animação senoidal de balanço |
| `desenhar_hud()` | Placar, cronômetro, mensagens pedagógicas |
| `desenhar_mira()` | Seta de força com ângulo e % de força |
| `desenhar_celebracao_gol()` | Flash, GOOOOOL! pulsante, confete |
| `jogada_computador()` | IA simples com erro aleatório |
| `tela_sobre()` | Créditos com scroll e estrelas animadas |
| `tela_menu()` | Menu principal |
| `rodar_jogo()` | Loop principal: eventos, física, desenho |

---

## 🔭 Melhorias Futuras

Indicadas no código com o comentário `# MELHORIA FUTURA`:

- [ ] Mais botões por time (goleiro, zagueiro, meia, atacante)
- [ ] Sons com arquivo `.wav` ou `.ogg` de maior qualidade
- [ ] Textura de grama no campo
- [ ] Perguntas de matemática integradas às jogadas
- [ ] Modo torneio com placar acumulado
- [ ] Estatísticas da partida (chutes, distância percorrida)
- [ ] IA mais inteligente (defesa, passes, posicionamento)
- [ ] Seleção de times e cores personalizadas

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
