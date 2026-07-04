"""
=============================================================
  FUTEBOL DE BOTÃO - Jogo Pedagógico em Python com Pygame
=============================================================
Criado para atividades de Matemática, Programação e Raciocínio Lógico.

Conceitos abordados durante o jogo:
  - Ângulo e direção (vetores)
  - Força e velocidade
  - Atrito (desaceleração)
  - Colisão entre objetos
  - Plano cartesiano (coordenadas x, y)

Como instalar o Pygame:
  pip install pygame

Como executar:
  python main.py

=============================================================
"""

import pygame
import math
import random
import sys
import array as _array

# ──────────────────────────────────────────────
# CONSTANTES E CONFIGURAÇÕES GERAIS
# ──────────────────────────────────────────────

# Dimensões da janela
LARGURA = 900
ALTURA  = 600

# Dimensões do campo (área interna, sem as bordas)
CAMPO_X      = 60    # margem lateral
CAMPO_Y      = 85    # margem superior (inclui espaço para o HUD)
CAMPO_LARG   = LARGURA - 2 * CAMPO_X
CAMPO_ALT    = ALTURA  - 2 * CAMPO_Y

# Gol: largura e posição
GOL_LARG = 10            # espessura da trave (visual)
GOL_ALT  = 120           # altura da abertura do gol
GOL_Y    = CAMPO_Y + (CAMPO_ALT - GOL_ALT) // 2  # centrado verticalmente

# Física
ATRITO         = 0.97    # fator de desaceleração a cada frame (0 a 1)
VELOCIDADE_MAX = 18.0    # velocidade máxima de lançamento
RAIO_BOTAO     = 18      # raio dos botões
RAIO_BOLA      = 10      # raio da bola
FRAMES_POR_SEG = 60

# Cores
VERDE_ESCURO = (34, 139, 34)
VERDE_CAMPO  = (50, 168, 82)
BRANCO       = (255, 255, 255)
PRETO        = (0,   0,   0)
AMARELO      = (255, 220,  0)
CINZA        = (160, 160, 160)
CINZA_ESCURO = (80,  80,  80)
AZUL         = (30,  80, 200)
VERMELHO     = (200,  30,  30)
LARANJA      = (255, 140,  0)
CIANO        = (0,   200, 200)
ROXO         = (140,  0,  200)
BEGE         = (240, 220, 180)

# Modos de jogo
MODO_2JOGADORES = "2jogadores"
MODO_COMPUTADOR = "computador"

TIMES_DISPONIVEIS = [
    {"nome": "Azul",         "cor": AZUL},
    {"nome": "Vermelho",     "cor": VERMELHO},
    {"nome": "Brasil",       "cor": (34, 139, 34)},
    {"nome": "Argentina",    "cor": (95, 180, 255)},
    {"nome": "Palmeiras",    "cor": (0, 120, 60)},
    {"nome": "Flamengo",     "cor": (190, 30, 30)},
    {"nome": "Corinthians",  "cor": (235, 235, 235)},
    {"nome": "Santos",       "cor": (250, 250, 250)},
    {"nome": "Sao Paulo",    "cor": (245, 245, 245)},
    {"nome": "Gremio",       "cor": (0, 140, 190)},
    {"nome": "Barcelona",    "cor": (0, 90, 170)},
    {"nome": "Real Madrid",  "cor": (248, 248, 248)},
]

CORES_PERSONALIZADAS = [
    AZUL, VERMELHO, VERDE_CAMPO, AMARELO, LARANJA, CIANO,
    ROXO, BRANCO, (255, 105, 180), (40, 40, 40), (0, 130, 160), (140, 90, 40),
]

# Botão de tela cheia — retângulo fixo no canto superior direito do HUD
BTN_FS_RECT = pygame.Rect(LARGURA - 40, 6, 32, 30)

# ──────────────────────────────────────────────
# MENSAGENS PEDAGÓGICAS
# (exibidas durante o jogo relacionando jogadas
#  a conceitos matemáticos e físicos)
# ──────────────────────────────────────────────

MSGS_PEDAGOGICAS = [
    "Ângulo: a direção do chute é medida em graus (°) em relação ao eixo X!",
    "Vetor: a jogada tem DIREÇÃO e INTENSIDADE — isso é um vetor!",
    "Velocidade: quanto maior a força, maior a velocidade inicial do botão.",
    "Atrito: a superfície desacelera o botão — energia se transforma em calor.",
    "Colisão: ao bater na bola, o botão transfere parte de seu movimento.",
    "Plano cartesiano: cada objeto tem coordenadas (x, y) no campo!",
    "Força: arrastar mais longe = mais força aplicada ao botão.",
    "Trajetória: o botão se move em linha reta — sem curvas nesta versão!",
    "Coordenadas: o canto superior esquerdo é o ponto (0, 0).",
    "Desaceleração: o botão para porque o atrito reduz a velocidade a cada instante.",
    "Ângulo de mira: tente apontar o vetor diretamente para a bola!",
    "Energia cinética: objeto em movimento possui energia — quanto mais rápido, mais energia!",
]

# ──────────────────────────────────────────────
# CONTROLE DE TELA CHEIA
# ──────────────────────────────────────────────

_tela_cheia = False   # estado atual: False = janela, True = tela cheia


def cor_texto_contraste(cor):
    """Escolhe preto ou branco para manter contraste legivel."""
    brilho = cor[0] * 0.299 + cor[1] * 0.587 + cor[2] * 0.114
    return PRETO if brilho >= 165 else BRANCO


def desenhar_texto_contornado(tela, fonte, texto, cor_texto, pos):
    """Desenha texto com contorno para manter legibilidade em qualquer fundo."""
    cor_contorno = cor_texto_contraste(cor_texto)
    txt_contorno = fonte.render(texto, True, cor_contorno)
    txt_principal = fonte.render(texto, True, cor_texto)
    x, y = pos
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        tela.blit(txt_contorno, (x + dx, y + dy))
    tela.blit(txt_principal, pos)
    return txt_principal


def alternar_tela_cheia():
    """
    Alterna entre modo janela (900×600) e tela cheia.
    Pressione F11 a qualquer momento durante o jogo.
    """
    global _tela_cheia
    _tela_cheia = not _tela_cheia
    if _tela_cheia:
        pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        pygame.display.set_mode((LARGURA, ALTURA))


def atualizar_tela(surface_logica):
    """
    Escala a surface lógica (900×600) para a janela real e exibe.
    Em tela cheia, mantém a proporção com barras pretas (letterbox).
    Conceito pedagógico: transformação de escala — ampliar sem distorcer.
    """
    tela_real = pygame.display.get_surface()
    tw, th = tela_real.get_size()
    # Calcula a escala preservando a proporção (aspect ratio)
    escala = min(tw / LARGURA, th / ALTURA)
    sw = int(LARGURA * escala)
    sh = int(ALTURA  * escala)
    # Centraliza com barras pretas se a proporção não bater exatamente
    off_x = (tw - sw) // 2
    off_y = (th - sh) // 2
    surf_esc = pygame.transform.smoothscale(surface_logica, (sw, sh))
    tela_real.fill(PRETO)
    tela_real.blit(surf_esc, (off_x, off_y))
    pygame.display.flip()


def escalar_mouse(pos):
    """
    Converte coordenadas do mouse da tela real para o espaço lógico (900×600).
    Necessário quando o jogo é escalado para tela cheia com letterbox.
    Conceito pedagógico: transformação inversa de escala.
    """
    tela_real = pygame.display.get_surface()
    tw, th = tela_real.get_size()
    escala = min(tw / LARGURA, th / ALTURA)
    sw = int(LARGURA * escala)
    sh = int(ALTURA  * escala)
    off_x = (tw - sw) // 2
    off_y = (th - sh) // 2
    mx, my = pos
    # Subtrai offset e divide pela escala para obter coordenadas lógicas
    gx = (mx - off_x) / escala
    gy = (my - off_y) / escala
    return (gx, gy)


def criar_sons():
    """
    Sintetiza sons em tempo real com ondas senoidais puras.
    Não usa arquivos externos — apenas matemática!
    Conceito pedagógico: som é uma onda; a frequência determina o tom.
    MELHORIA FUTURA: adicionar apito, aplausos, narrador de voz.
    """
    if not pygame.mixer.get_init():
        return {"gol": None, "chute": None, "bola": None, "botao": None}

    sr       = 44100   # amostras por segundo
    channels = 2       # estéreo: canal esquerdo + direito

    def gerar(notas, vol=0.55):
        """
        Gera buffer de áudio a partir de lista de (frequência_Hz, duração_s).
        Onda senoidal com fade-out suave nos últimos 25%.
        fórmula: y = A * sen(2π * f * t)
        """
        buf = _array.array('h')   # 'h' = inteiro 16 bits com sinal
        for freq, dur in notas:
            n = int(sr * dur)
            for i in range(n):
                env = (n - i) / (n * 0.25) if i >= int(n * 0.75) else 1.0
                v = int(32767 * vol * env * math.sin(2 * math.pi * freq * i / sr))
                for _ in range(channels):
                    buf.append(v)
        return pygame.mixer.Sound(buffer=buf)

    return {
        # Fanfarra ascendente: Dó→Mi→Sol→Dó (acorde maior)
        "gol":   gerar([(523, 0.10), (659, 0.10), (784, 0.10), (1047, 0.45)]),
        # Batida curta e grave para o chute
        "chute": gerar([(180, 0.07)], vol=0.28),
        # Clique médio-agudo: botão batendo na bola (plástico leve)
        # Conceito: frequência mais alta = som mais agudo
        "bola":  gerar([(600, 0.04), (400, 0.03)], vol=0.40),
        # Batida mais grave: botão batendo em botão (plástico pesado)
        "botao": gerar([(260, 0.05), (180, 0.03)], vol=0.35),
    }


# ──────────────────────────────────────────────
# CLASSES
# ──────────────────────────────────────────────

class Objeto:
    """
    Classe base para qualquer objeto circular no campo.
    Guarda posição (x, y), velocidade (vx, vy) e raio.
    """
    def __init__(self, x, y, raio, cor):
        self.x    = float(x)
        self.y    = float(y)
        self.raio = raio
        self.cor  = cor
        self.vx   = 0.0   # velocidade no eixo X
        self.vy   = 0.0   # velocidade no eixo Y

    @property
    def pos(self):
        """Retorna a posição como tupla de inteiros (para desenho)."""
        return (int(self.x), int(self.y))

    def esta_parado(self):
        """Retorna True se o objeto praticamente não se move mais."""
        return abs(self.vx) < 0.1 and abs(self.vy) < 0.1

    def aplicar_atrito(self):
        """
        Aplica atrito: multiplica a velocidade por um fator < 1.
        Conceito pedagógico: atrito desacelera o movimento.
        """
        self.vx *= ATRITO
        self.vy *= ATRITO
        # Zera velocidade muito pequena para evitar deslizamento infinito
        if abs(self.vx) < 0.05:
            self.vx = 0.0
        if abs(self.vy) < 0.05:
            self.vy = 0.0

    def mover(self):
        """Atualiza a posição com base na velocidade atual."""
        self.x += self.vx
        self.y += self.vy
        self.aplicar_atrito()

    def colidir_bordas(self):
        """
        Rebate o objeto ao atingir as bordas do campo.
        Conceito pedagógico: reflexão — o ângulo de saída = ângulo de entrada.
        """
        # Borda esquerda
        if self.x - self.raio < CAMPO_X:
            self.x  = CAMPO_X + self.raio
            self.vx = abs(self.vx)  # inverte sentido no eixo X
        # Borda direita
        if self.x + self.raio > CAMPO_X + CAMPO_LARG:
            self.x  = CAMPO_X + CAMPO_LARG - self.raio
            self.vx = -abs(self.vx)
        # Borda superior
        if self.y - self.raio < CAMPO_Y:
            self.y  = CAMPO_Y + self.raio
            self.vy = abs(self.vy)
        # Borda inferior
        if self.y + self.raio > CAMPO_Y + CAMPO_ALT:
            self.y  = CAMPO_Y + CAMPO_ALT - self.raio
            self.vy = -abs(self.vy)

    def distancia_para(self, outro):
        """
        Calcula a distância euclidiana até outro objeto.
        Conceito: distância = sqrt((x2-x1)² + (y2-y1)²)
        """
        dx = self.x - outro.x
        dy = self.y - outro.y
        return math.sqrt(dx * dx + dy * dy)

    def verificar_colisao(self, outro):
        """
        Verifica se este objeto colide com 'outro' (círculo a círculo).
        Retorna True se a distância entre centros < soma dos raios.
        """
        return self.distancia_para(outro) < (self.raio + outro.raio)

    def resolver_colisao(self, outro):
        """
        Resolve a colisão entre dois círculos de forma simplificada.
        O objeto 'outro' recebe parte da velocidade deste.
        Conceito: transferência de momento linear em colisão.
        """
        dx = outro.x - self.x
        dy = outro.y - self.y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist == 0:
            return  # evita divisão por zero

        # Vetor unitário na direção da colisão
        nx = dx / dist
        ny = dy / dist

        # Velocidade relativa projetada na direção normal
        vel_relativa = (self.vx - outro.vx) * nx + (self.vy - outro.vy) * ny

        # Só resolve se os objetos estão se aproximando
        if vel_relativa > 0:
            # Transfere velocidade para o outro objeto
            outro.vx += vel_relativa * nx
            outro.vy += vel_relativa * ny
            # Reduz velocidade deste objeto
            self.vx  -= vel_relativa * nx * 0.5
            self.vy  -= vel_relativa * ny * 0.5

        # Separa os objetos para não ficarem sobrepostos
        sobreposicao = (self.raio + outro.raio) - dist
        self.x  -= nx * sobreposicao * 0.5
        self.y  -= ny * sobreposicao * 0.5
        outro.x += nx * sobreposicao * 0.5
        outro.y += ny * sobreposicao * 0.5

    def desenhar(self, tela):
        """Desenha o círculo na tela."""
        pygame.draw.circle(tela, self.cor, self.pos, self.raio)


class Botao(Objeto):
    """
    Representa um botão (peça circular) de um time.
    Herda de Objeto e adiciona: número do time e identificador.
    """
    def __init__(self, x, y, cor, time, numero):
        super().__init__(x, y, RAIO_BOTAO, cor)
        self.time   = time    # 0 = lado esquerdo, 1 = lado direito
        self.numero = numero  # número do botão dentro do time
        self.selecionado = False

    def desenhar(self, tela, fonte_pequena, toque_count=0, maxed_out=False):
        """Desenha o botão com borda de destaque se selecionado.
        toque_count: número de toques usados (regra 12 toques).
        maxed_out: True se o botão atingiu o limite individual de 3 toques.
        """
        # Sombra sutil
        pygame.draw.circle(tela, CINZA_ESCURO, (self.pos[0]+2, self.pos[1]+2), self.raio)
        # Corpo do botão (escurecido se esgotado na regra de 12 toques)
        cor_corpo = CINZA_ESCURO if maxed_out else self.cor
        pygame.draw.circle(tela, cor_corpo, self.pos, self.raio)
        # Borda
        cor_padrao = cor_texto_contraste(cor_corpo)
        cor_borda = AMARELO if self.selecionado else (CINZA if maxed_out else cor_padrao)
        pygame.draw.circle(tela, cor_borda, self.pos, self.raio, 2)
        # Número do botão (para identificação)
        cor_numero = BRANCO if maxed_out else cor_padrao
        txt = fonte_pequena.render(str(self.numero + 1), True, cor_numero)
        tela.blit(txt, (self.pos[0] - txt.get_width()//2,
                        self.pos[1] - txt.get_height()//2))
        # Indicador de toques individuais (regra de 12 toques)
        if toque_count > 0 or maxed_out:
            fonte_tiny = pygame.font.SysFont("Arial", 12, bold=True)
            cor_ind = VERMELHO if maxed_out else LARANJA
            txt_tc = fonte_tiny.render(f"{toque_count}/3", True, cor_ind)
            tela.blit(txt_tc, (self.pos[0] - txt_tc.get_width()//2,
                               self.pos[1] + self.raio + 2))


class Bola(Objeto):
    """
    Representa a bola de futebol de botão.
    """
    def __init__(self, x, y):
        super().__init__(x, y, RAIO_BOLA, BRANCO)

    def desenhar(self, tela):
        # Sombra
        pygame.draw.circle(tela, CINZA_ESCURO, (self.pos[0]+2, self.pos[1]+2), self.raio)
        # Bola branca
        pygame.draw.circle(tela, BRANCO, self.pos, self.raio)
        # Miolo cinza para parecer bola
        pygame.draw.circle(tela, CINZA, self.pos, self.raio - 3)
        # Detalhe
        pygame.draw.circle(tela, BRANCO, self.pos, self.raio, 2)

    def colidir_bordas(self):
        """
        A bola rebate nas bordas, EXCETO nas aberturas dos gols.
        Conceito: condição lógica — 'se e somente se' não está na zona do gol.
        """
        # Borda esquerda (gol do time 1 está aqui)
        if self.x - self.raio < CAMPO_X:
            # Só rebate se NÃO estiver na abertura do gol
            if not (GOL_Y < self.y < GOL_Y + GOL_ALT):
                self.x  = CAMPO_X + self.raio
                self.vx = abs(self.vx)

        # Borda direita (gol do time 2 está aqui)
        if self.x + self.raio > CAMPO_X + CAMPO_LARG:
            if not (GOL_Y < self.y < GOL_Y + GOL_ALT):
                self.x  = CAMPO_X + CAMPO_LARG - self.raio
                self.vx = -abs(self.vx)

        # Borda superior
        if self.y - self.raio < CAMPO_Y:
            self.y  = CAMPO_Y + self.raio
            self.vy = abs(self.vy)

        # Borda inferior
        if self.y + self.raio > CAMPO_Y + CAMPO_ALT:
            self.y  = CAMPO_Y + CAMPO_ALT - self.raio
            self.vy = -abs(self.vy)


# ──────────────────────────────────────────────
# FUNÇÕES DE CRIAÇÃO DO TABULEIRO
# ──────────────────────────────────────────────

class Particula:
    """
    Partícula de confete para a celebração do gol.
    Conceito pedagógico: trajetória com gravidade e resistência do ar.
    Cada partícula tem posição (x, y), velocidade (vx, vy) e tempo de vida.
    """
    CORES = [AMARELO, BRANCO, LARANJA, CIANO, VERDE_CAMPO, VERMELHO, AZUL]

    def __init__(self, x, y):
        angulo       = random.uniform(0, 2 * math.pi)
        vel          = random.uniform(4, 10)
        self.x       = float(x)
        self.y       = float(y)
        self.vx      = math.cos(angulo) * vel
        self.vy      = math.sin(angulo) * vel - random.uniform(2, 6)  # tendência para cima
        self.cor     = random.choice(self.CORES)
        self.raio    = random.randint(3, 7)
        self.vida    = random.randint(80, 130)   # duração em frames
        self.vida_max = self.vida

    def atualizar(self):
        """Move a partícula aplicando gravidade (acéleração para baixo)."""
        self.x  += self.vx
        self.y  += self.vy
        self.vy += 0.20   # gravidade
        self.vx *= 0.99   # atrito horizontal
        self.vida -= 1

    def desenhar(self, tela):
        if self.vida > 0:
            pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), self.raio)

    def vivo(self):
        return self.vida > 0


def criar_botoes_time(time, cor_personalizada=None):
    """
    Cria 3 botões para o time indicado (0 ou 1) em posições iniciais.
    Time 0 → lado esquerdo
    Time 1 → lado direito

    MELHORIA FUTURA: adicionar mais botões (goleiro, meio, ataque).
    """
    cx = CAMPO_X + CAMPO_LARG // 2   # centro horizontal do campo
    cy = CAMPO_Y + CAMPO_ALT  // 2   # centro vertical do campo

    botoes = []
    if time == 0:
        cor       = cor_personalizada or AZUL
        posicoes  = [
            (cx - 200, cy - 100),   # atacante esquerdo
            (cx - 200, cy + 100),   # atacante direito
            (cx - 320, cy),         # meio
        ]
    else:
        cor       = cor_personalizada or VERMELHO
        posicoes  = [
            (cx + 200, cy - 100),
            (cx + 200, cy + 100),
            (cx + 320, cy),
        ]

    for i, (px, py) in enumerate(posicoes):
        botoes.append(Botao(px, py, cor, time, i))

    return botoes


def criar_bola():
    """Cria a bola no centro do campo."""
    cx = CAMPO_X + CAMPO_LARG // 2
    cy = CAMPO_Y + CAMPO_ALT  // 2
    return Bola(cx, cy)


# ──────────────────────────────────────────────
# FUNÇÕES DE DESENHO
# ──────────────────────────────────────────────

def desenhar_campo(tela):
    """
    Desenha o campo visto de cima, com linhas, círculo central e gols.
    MELHORIA FUTURA: adicionar textura de grama, áreas, cantos etc.
    """
    # Fundo geral (mesa)
    tela.fill(CINZA_ESCURO)

    # Superfície do campo
    pygame.draw.rect(tela, VERDE_CAMPO,
                     (CAMPO_X, CAMPO_Y, CAMPO_LARG, CAMPO_ALT))

    # Linhas internas ─────────────────────────────────────
    # Linha do meio-campo (vertical)
    cx = CAMPO_X + CAMPO_LARG // 2
    pygame.draw.line(tela, BRANCO,
                     (cx, CAMPO_Y), (cx, CAMPO_Y + CAMPO_ALT), 2)

    # Círculo central
    pygame.draw.circle(tela, BRANCO,
                       (cx, CAMPO_Y + CAMPO_ALT // 2), 60, 2)

    # Ponto central
    pygame.draw.circle(tela, BRANCO,
                       (cx, CAMPO_Y + CAMPO_ALT // 2), 4)

    # Áreas (retângulos frontais dos gols)
    area_larg = 80
    area_alt  = GOL_ALT + 60
    area_y    = CAMPO_Y + (CAMPO_ALT - area_alt) // 2

    pygame.draw.rect(tela, BRANCO,
                     (CAMPO_X, area_y, area_larg, area_alt), 2)
    pygame.draw.rect(tela, BRANCO,
                     (CAMPO_X + CAMPO_LARG - area_larg, area_y, area_larg, area_alt), 2)

    # Bordas do campo
    pygame.draw.rect(tela, BRANCO,
                     (CAMPO_X, CAMPO_Y, CAMPO_LARG, CAMPO_ALT), 3)

    # Gols ────────────────────────────────────────────────
    # Gol esquerdo (time 2 marca aqui)
    pygame.draw.rect(tela, CINZA,
                     (CAMPO_X - 20, GOL_Y, 20, GOL_ALT))
    pygame.draw.rect(tela, BRANCO,
                     (CAMPO_X - 20, GOL_Y, 20, GOL_ALT), 2)

    # Gol direito (time 1 marca aqui)
    pygame.draw.rect(tela, CINZA,
                     (CAMPO_X + CAMPO_LARG, GOL_Y, 20, GOL_ALT))
    pygame.draw.rect(tela, BRANCO,
                     (CAMPO_X + CAMPO_LARG, GOL_Y, 20, GOL_ALT), 2)


def desenhar_redes(tela, estado):
    """
    Desenha as redes dos dois gols.
    Quando a fase é 'gol', anima a rede do lado que sofreu o gol,
    usando funções seno/cosseno para simular o balanço.
    Conceito pedagógico: ondas senoidais modelam movimentos oscilatórios.
    """
    # Definição dos dois gols: (lado, x_esquerda_da_rede)
    # lado 0 = gol direito (time 1 ataca para cá), lado 1 = gol esquerdo
    gols = [
        (0, CAMPO_X + CAMPO_LARG),          # rede do gol direito
        (1, CAMPO_X - 20),                  # rede do gol esquerdo
    ]

    timer = estado["timer_gol"] if estado["fase"] == "gol" else 0
    lado_gol = estado.get("gol_time", -1) if estado["fase"] == "gol" else -1

    for lado, rx in gols:
        # Decide a amplitude de balanço para esta rede
        if lado == lado_gol and timer > 0:
            # Amplitude decresce com o tempo (amortecimento)
            amort   = max(0.0, 1.0 - timer / (FRAMES_POR_SEG * 3))
            amp     = 7 * amort
            fase_on = timer * 0.35    # velocidade da onda
        else:
            amp     = 0
            fase_on = 0

        # Fundo da rede (retângulo cinza)
        pygame.draw.rect(tela, CINZA, (rx, GOL_Y, 20, GOL_ALT))
        pygame.draw.rect(tela, BRANCO, (rx, GOL_Y, 20, GOL_ALT), 2)

        # Linhas verticais da rede (de cima para baixo)
        n_vert = 5
        for i in range(n_vert + 1):
            t_frac = i / n_vert                       # 0.0 → 1.0
            x_base = rx + int(t_frac * 20)            # posição X da linha
            # Deformação ondulatória: combina seno e cosseno
            dx_onda = int(amp * math.sin(fase_on + t_frac * math.pi * 2))
            pontos = []
            n_hor = 8
            for j in range(n_hor + 1):
                s_frac = j / n_hor
                y = GOL_Y + int(s_frac * GOL_ALT)
                dy_onda = int(amp * 0.6 * math.cos(fase_on * 1.3 + s_frac * math.pi * 2))
                pontos.append((x_base + dx_onda, y + dy_onda))
            if len(pontos) >= 2:
                pygame.draw.lines(tela, CINZA_ESCURO, False, pontos, 1)

        # Linhas horizontais da rede
        n_hor = 8
        for j in range(n_hor + 1):
            s_frac = j / n_hor
            y_base = GOL_Y + int(s_frac * GOL_ALT)
            dy_onda = int(amp * 0.6 * math.cos(fase_on * 1.3 + s_frac * math.pi * 2))
            pontos = []
            n_vert2 = 5
            for i in range(n_vert2 + 1):
                t_frac = i / n_vert2
                x = rx + int(t_frac * 20)
                dx_onda = int(amp * math.sin(fase_on + t_frac * math.pi * 2))
                pontos.append((x + dx_onda, y_base + dy_onda))
            if len(pontos) >= 2:
                pygame.draw.lines(tela, CINZA_ESCURO, False, pontos, 1)


def desenhar_hud(tela, fontes, estado):
    """
    Desenha o HUD (cabeçalho com placar, turno, mensagem pedagógica).
    MELHORIA FUTURA: adicionar temporizador, histórico de jogadas.
    """
    fonte_grande = fontes["grande"]
    fonte_media  = fontes["media"]
    fonte_pequena = fontes["pequena"]

    # Fundo do HUD superior
    pygame.draw.rect(tela, PRETO, (0, 0, LARGURA, CAMPO_Y - 5))

    # Nome do jogo (linha 1, centralizado)
    txt_nome = fonte_media.render("FUTEBOL DE BOTÃO", True, AMARELO)
    tela.blit(txt_nome, (LARGURA // 2 - txt_nome.get_width() // 2, 5))

    # Placar (linha 2, centralizado)
    placar_str = f"{estado['nome_j1']}  {estado['gols_j1']}  x  {estado['gols_j2']}  {estado['nome_j2']}"
    txt_placar = fonte_grande.render(placar_str, True, BRANCO)
    tela.blit(txt_placar, (LARGURA // 2 - txt_placar.get_width() // 2, 44))

    # Indicador de turno (canto esquerdo)
    nome_turno = estado["nome_j1"] if estado["turno"] == 0 else estado["nome_j2"]
    turno_str = f"Vez: {nome_turno}"
    cor_turno = estado["cor_j1"] if estado["turno"] == 0 else estado["cor_j2"]
    txt_turno = fonte_media.render(turno_str, True, cor_turno)
    tela.blit(txt_turno, (10, 5))

    # Indicador da regra dos 12 toques (canto esquerdo, abaixo do turno)
    if estado.get("regra") == "12toques":
        tc = estado.get("toques_coletivos", 0)
        cor_tc = VERMELHO if tc >= 10 else (LARANJA if tc >= 7 else AMARELO)
        txt_tc = fonte_pequena.render(f"Toques: {tc}/12", True, cor_tc)
        tela.blit(txt_tc, (10, 36))
        txt_reg = fonte_pequena.render("REGRA: 12 TOQUES", True, CIANO)
        tela.blit(txt_reg, (10, 56))
        # Cronômetro de 5 s por toque (só quando é vez de um humano)
        tt = estado.get("timer_toque", 5 * FRAMES_POR_SEG)
        seg_rest = max(0, math.ceil(tt / FRAMES_POR_SEG))
        fase_ativa = estado.get("fase", "") in ("selecionar", "mirar")
        turno_humano = (estado.get("turno") == 0 or
                        not estado.get("cpu_ativo", False))
        if fase_ativa and turno_humano:
            cor_tt = VERMELHO if seg_rest <= 2 else (LARANJA if seg_rest <= 3 else BRANCO)
            txt_tt = fonte_media.render(f"⏱ {seg_rest}s", True, cor_tt)
            tela.blit(txt_tt, (10, 72))

    # Botão de tela cheia (canto superior direito)
    desenhar_btn_fullscreen(tela)
    # Cronômetro e turnos (à esquerda do botão)
    seg_total  = estado.get("tempo_seg", 0)
    minutos    = seg_total // 60
    segundos   = seg_total % 60
    # Fica vermelho piscante nos últimos 30 segundos
    cor_timer  = VERMELHO if (seg_total <= 30 and seg_total % 2 == 0) else (
                 AMARELO  if seg_total <= 30 else BRANCO)
    txt_timer  = fonte_media.render(f"{minutos:02d}:{segundos:02d}", True, cor_timer)
    tela.blit(txt_timer, (BTN_FS_RECT.left - txt_timer.get_width() - 8,
                           BTN_FS_RECT.centery - txt_timer.get_height() // 2))
    # Turnos abaixo do cronômetro
    txt_turn = fonte_pequena.render(f"Turno: {estado['num_turno']}", True, CINZA)
    tela.blit(txt_turn, (BTN_FS_RECT.left - txt_turn.get_width() - 8, 52))

    # Fase do turno / mensagem de infração
    if estado["fase"] == "infracao":
        tipo_inf = estado.get("infracao_tipo", "falta")
        cor_fase = VERMELHO if tipo_inf == "falta" else AMARELO
        txt_fase = fonte_media.render(estado.get("infracao_msg", "FALTA!"), True, cor_fase)
    else:
        fase_str = {
            "selecionar":  "Clique em um botão para selecionar",
            "mirar":       "Arraste para mirar e definir a força",
            "animando":    "Aguardando...",
            "computador":  "Computador jogando...",
            "gol":         "⚽  G O L !  ⚽",
        }.get(estado['fase'], "")
        cor_fase = AMARELO if estado['fase'] == "gol" else BEGE
        txt_fase = fonte_pequena.render(fase_str, True, cor_fase)
    tela.blit(txt_fase, (LARGURA // 2 - txt_fase.get_width() // 2, CAMPO_Y + CAMPO_ALT + 8))

    # Mensagem pedagógica (rodapé)
    if estado.get("msg_pedagogica"):
        msg = estado["msg_pedagogica"]
        # Divide em duas linhas se muito longa
        partes = dividir_texto(msg, 80)
        for i, parte in enumerate(partes[:2]):
            txt_msg = fonte_pequena.render(parte, True, CIANO)
            tela.blit(txt_msg, (LARGURA // 2 - txt_msg.get_width() // 2,
                                CAMPO_Y + CAMPO_ALT + 32 + i * 23))


def desenhar_mira(tela, botao_sel, pos_mouse):
    """
    Desenha a linha de mira (vetor de força) enquanto o jogador arrasta.
    Conceito pedagógico: visualiza o vetor direção/força.
    """
    if botao_sel is None:
        return
    bx, by = botao_sel.pos
    mx, my = pos_mouse

    # Vetor do mouse → botão (direção do chute)
    dx = bx - mx
    dy = by - my
    comprimento = math.sqrt(dx * dx + dy * dy)

    if comprimento < 1:
        return

    # Normaliza e escala para visualização
    escala = min(comprimento, 80)  # limita o comprimento visual
    nx = dx / comprimento * escala
    ny = dy / comprimento * escala

    # Ponto final da seta (onde o botão vai)
    fx = int(bx + nx)
    fy = int(by + ny)

    # Linha principal (vermelho = vetor força)
    pygame.draw.line(tela, LARANJA, (bx, by), (fx, fy), 3)

    # Ponta da seta
    angulo = math.atan2(ny, nx)
    for delta in [0.5, -0.5]:
        ax = fx - 12 * math.cos(angulo + delta)
        ay = fy - 12 * math.sin(angulo + delta)
        pygame.draw.line(tela, LARANJA, (fx, fy), (int(ax), int(ay)), 2)

    # Exibe ângulo em graus e força (conceito pedagógico visual)
    angulo_graus = math.degrees(math.atan2(-dy, dx)) % 360
    forca_pct    = min(int(comprimento / 80 * 100), 100)
    fonte = pygame.font.SysFont("Arial", 17)
    txt = fonte.render(f"Ângulo: {angulo_graus:.0f}°  Força: {forca_pct}%", True, AMARELO)
    tela.blit(txt, (bx - txt.get_width() // 2, by - RAIO_BOTAO - 28))


def desenhar_btn_fullscreen(tela):
    """
    Desenha o botão de tela cheia no canto superior direito.
    Ícone: 4 cantos em 'L' (indica expandir/retrair a janela).
    """
    r   = BTN_FS_RECT
    cor = AMARELO if _tela_cheia else CINZA
    # Fundo
    pygame.draw.rect(tela, CINZA_ESCURO, r, border_radius=5)
    pygame.draw.rect(tela, cor, r, 2, border_radius=5)
    # Ícone: 4 cantos em L
    x, y, w, h = r.x, r.y, r.width, r.height
    m, s = 6, 5
    for (p1, p2, p3) in [
        ((x+m,     y+m+s),   (x+m,   y+m  ), (x+m+s,   y+m  )),
        ((x+w-m-s, y+m  ),   (x+w-m, y+m  ), (x+w-m,   y+m+s)),
        ((x+m,     y+h-m-s), (x+m,   y+h-m), (x+m+s,   y+h-m)),
        ((x+w-m-s, y+h-m),   (x+w-m, y+h-m), (x+w-m,   y+h-m-s)),
    ]:
        pygame.draw.line(tela, cor, p1, p2, 2)
        pygame.draw.line(tela, cor, p2, p3, 2)


def desenhar_celebracao_gol(tela, estado, fontes):
    """
    Animação de celebração ao marcar gol:
      - Flash colorido que desvanece
      - Texto 'GOOOOOOLLLL!' pulsante com sombra
      - Confête de partículas coloridas
    """
    timer    = estado["timer_gol"]
    gol_time = estado.get("gol_time", 0)
    nome     = estado["nome_j1"] if gol_time == 0 else estado["nome_j2"]
    cor_time = estado["cor_j1"] if gol_time == 0 else estado["cor_j2"]

    # ─ Flash colorido nos primeiros 18 frames ────────────────
    if timer < 18:
        alpha   = int(170 * (1 - timer / 18))
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((*cor_time, alpha))
        tela.blit(overlay, (0, 0))

    # ─ Texto GOOOOOOLLLL! pulsante ────────────────────────
    pulso   = 1.0 + 0.22 * math.sin(timer * 0.22)
    cx, cy  = LARGURA // 2, ALTURA // 2
    txt_raw = fontes["gol"].render("GOOOOOOLLLL!", True, AMARELO)
    tw = max(1, int(txt_raw.get_width()  * pulso))
    th = max(1, int(txt_raw.get_height() * pulso))
    # Sombra (deslocada 4px) desenhada primeiro
    sombra_esc = pygame.transform.smoothscale(
        fontes["gol"].render("GOOOOOOLLLL!", True, PRETO), (tw, th))
    tela.blit(sombra_esc, (cx - tw // 2 + 4, cy - th // 2 - 25 + 4))
    # Texto principal
    tela.blit(pygame.transform.smoothscale(txt_raw, (tw, th)),
              (cx - tw // 2, cy - th // 2 - 25))

    # Nome do time que marcou
    txt_time = fontes["grande"].render(f"Gol de {nome}!", True, cor_time)
    tela.blit(txt_time, (cx - txt_time.get_width() // 2, cy + th // 2 - 10))

    # ─ Partículas de confête ──────────────────────────────
    for p in estado["particulas"]:
        p.desenhar(tela)


# ──────────────────────────────────────────────
# FUNÇÕES AUXILIARES
# ──────────────────────────────────────────────

def dividir_texto(texto, limite_chars):
    """Divide um texto longo em linhas de no máximo 'limite_chars' caracteres."""
    palavras = texto.split()
    linhas, linha_atual = [], ""
    for palavra in palavras:
        if len(linha_atual) + len(palavra) + 1 <= limite_chars:
            linha_atual += (" " if linha_atual else "") + palavra
        else:
            if linha_atual:
                linhas.append(linha_atual)
            linha_atual = palavra
    if linha_atual:
        linhas.append(linha_atual)
    return linhas


def calcular_velocidade(botao_pos, mouse_pos, distancia_max=80):
    """
    Converte a posição do mouse em vetor de velocidade para o botão.
    Quanto mais longe o mouse do botão, maior a força.
    Retorna (vx, vy).
    Conceito: decomposição vetorial em componentes x e y.
    """
    bx, by = botao_pos
    mx, my = mouse_pos
    dx = bx - mx   # direção: do mouse para o botão
    dy = by - my
    comprimento = math.sqrt(dx * dx + dy * dy)
    if comprimento < 1:
        return 0.0, 0.0
    # Normaliza e aplica escala de força
    forca = min(comprimento, distancia_max) / distancia_max * VELOCIDADE_MAX
    vx = (dx / comprimento) * forca
    vy = (dy / comprimento) * forca
    return vx, vy


def verificar_gol(bola):
    """
    Verifica se a bola entrou em algum gol.
    Retorna 0 (gol para time 1 → no gol direito),
            1 (gol para time 2 → no gol esquerdo),
            ou None.
    """
    # Gol esquerdo (time 1 marca → bola passou para a esquerda)
    if bola.x < CAMPO_X - 5 and GOL_Y < bola.y < GOL_Y + GOL_ALT:
        return 1   # time 2 marcou (atacou para a esquerda)

    # Gol direito (time 2 marca → bola passou para a direita)
    if bola.x > CAMPO_X + CAMPO_LARG + 5 and GOL_Y < bola.y < GOL_Y + GOL_ALT:
        return 0   # time 1 marcou

    return None


def tudo_parado(botoes_t0, botoes_t1, bola):
    """Retorna True quando todos os objetos estão em repouso."""
    todos = botoes_t0 + botoes_t1 + [bola]
    return all(obj.esta_parado() for obj in todos)


def jogada_computador(botoes_cpu, bola, toques_individuais=None):
    """
    Realiza a jogada automática do computador com estratégia aprimorada.
    Considera alinhamento com o gol, situação defensiva e regra de 12 toques.
    O time da CPU (vermelho, time 1) ataca o gol esquerdo.
    """
    if not botoes_cpu:
        return None, (0.0, 0.0)

    # Gol que a CPU ataca (gol esquerdo: x < CAMPO_X)
    gol_atq_x = CAMPO_X - 10
    gol_atq_y = GOL_Y + GOL_ALT // 2
    # Gol que a CPU defende (gol direito: x > CAMPO_X + CAMPO_LARG)
    gol_def_x = CAMPO_X + CAMPO_LARG + 10
    gol_def_y = GOL_Y + GOL_ALT // 2

    # Filtra botões disponíveis: respeita limite individual de 3 toques
    if toques_individuais:
        botoes_disp = [b for b in botoes_cpu
                       if toques_individuais.get((b.time, b.numero), 0) < 3]
        if not botoes_disp:
            botoes_disp = botoes_cpu  # fallback: usa todos
    else:
        botoes_disp = botoes_cpu

    # Modo defensivo: bola próxima do próprio gol → prioridade é afastar
    dist_defesa = math.sqrt((bola.x - gol_def_x)**2 + (bola.y - gol_def_y)**2)
    modo_defesa = dist_defesa < 160

    if modo_defesa:
        # Usa o botão mais próximo da bola
        botao_escolhido = min(botoes_disp, key=lambda b: b.distancia_para(bola))
        # Aponta em direção ao gol adversário (com erro pequeno)
        dx = gol_atq_x - botao_escolhido.x
        dy = gol_atq_y - botao_escolhido.y
        angulo_base = math.atan2(dy, dx)
        erro  = random.uniform(-0.12, 0.12)
        forca = random.uniform(0.85, 1.0) * VELOCIDADE_MAX
    else:
        # Escolhe o botão mais bem posicionado: alinhado na linha botão→bola→gol
        def score_botao(b):
            dx_pb = bola.x - b.x
            dy_pb = bola.y - b.y
            dist_pb = max(1.0, math.sqrt(dx_pb**2 + dy_pb**2))
            dx_bg = gol_atq_x - bola.x
            dy_bg = gol_atq_y - bola.y
            dist_bg = max(1.0, math.sqrt(dx_bg**2 + dy_bg**2))
            # Cosseno do ângulo entre vetores (botão→bola) e (bola→gol)
            cos_alg = (dx_pb * dx_bg + dy_pb * dy_bg) / (dist_pb * dist_bg)
            return cos_alg - dist_pb / 350.0

        botao_escolhido = max(botoes_disp, key=score_botao)

        # Calcula ponto de mira para deflectir a bola em direção ao gol:
        # O botão deve vir do lado oposto ao gol, empurrando a bola "para lá".
        dx_bg = gol_atq_x - bola.x
        dy_bg = gol_atq_y - bola.y
        dist_bg = max(1.0, math.sqrt(dx_bg**2 + dy_bg**2))
        offset = RAIO_BOLA + RAIO_BOTAO + 2
        aim_x = bola.x - (dx_bg / dist_bg) * offset
        aim_y = bola.y - (dy_bg / dist_bg) * offset

        dx = aim_x - botao_escolhido.x
        dy = aim_y - botao_escolhido.y
        angulo_base = math.atan2(dy, dx)
        # Erro reduzido em relação à versão anterior (±0.15 rad em vez de ±0.3)
        erro = random.uniform(-0.15, 0.15)
        dist_bola = botao_escolhido.distancia_para(bola)
        # Tiro suave quando próximo; tiro forte quando longe
        if dist_bola < 100:
            forca = random.uniform(0.55, 0.80) * VELOCIDADE_MAX
        else:
            forca = random.uniform(0.70, 0.95) * VELOCIDADE_MAX

    angulo = angulo_base + erro
    vx = math.cos(angulo) * forca
    vy = math.sin(angulo) * forca
    return botao_escolhido, (vx, vy)


# ──────────────────────────────────────────────
# TELAS DE MENU
# ──────────────────────────────────────────────

def tela_sobre(tela, fontes):
    """
    Tela de créditos, objetivo e informações pedagógicas do jogo.
    Acessada pelo botão 'Sobre' no menu principal.
    """
    fonte_grande  = fontes["grande"]
    fonte_media   = fontes["media"]
    fonte_pequena = fontes["pequena"]
    clock         = pygame.time.Clock()

    # ─ Conteúdo em seções ────────────────────────────────
    secoes = [
        # (tipo, texto, cor)
        # tipo: 'titulo' | 'subtitulo' | 'texto' | 'destaque' | 'separador'
        ("titulo",    "FUTEBOL DE BOTÃO",                                AMARELO),
        ("subtitulo", "Jogo Pedagógico de Matemática, Física e Lógica",  BRANCO),
        ("separador", "",                                                 CINZA),

        ("subtitulo", "★  AUTOR",                                         CIANO),
        ("destaque",  "Júlio César Valera",                               AMARELO),
        ("texto",     "Professor de Matemática, Programação e Robótica",   BRANCO),
        ("texto",     "Rede Pública de Ensino — São Paulo / SP",           BRANCO),
        ("separador", "",                                                 CINZA),

        ("subtitulo", "★  PARA QUEM É",                                   CIANO),
        ("texto",     "Estudantes do Ensino Fundamental e Médio",          BRANCO),
        ("texto",     "Aulas de Matemática, Física, Computação e STEM",   BRANCO),
        ("texto",     "100% gratuito e de código aberto",                 VERDE_CAMPO),
        ("separador", "",                                                 CINZA),

        ("subtitulo", "★  OBJETIVO PEDAGÓGICO",                           CIANO),
        ("texto",     "Aprender conceitos de Física e Matemática",        BRANCO),
        ("texto",     "jogando e programando ao mesmo tempo.",             BRANCO),
        ("separador", "",                                                 CINZA),

        ("subtitulo", "★  CONCEITOS ABORDADOS",                           CIANO),
        ("texto",     "▶ Ângulo e direção — vetor de força",             BEGE),
        ("texto",     "▶ Velocidade e força aplicada",                    BEGE),
        ("texto",     "▶ Atrito e desaceleração",                         BEGE),
        ("texto",     "▶ Colisão e transferência de momento",             BEGE),
        ("texto",     "▶ Plano cartesiano (coordenadas x, y)",            BEGE),
        ("texto",     "▶ Ondas senoidais (som e animação da rede)",        BEGE),
        ("separador", "",                                                 CINZA),

        ("subtitulo", "★  TECNOLOGIA",                                    CIANO),
        ("texto",     "Desenvolvido em Python 3 + Pygame",                BRANCO),
        ("texto",     "Gráficos, sons e física feitos 100% em código",   BRANCO),
        ("texto",     "Sem imagens ou sons externos — tudo é programado!", BRANCO),
        ("separador", "",                                                 CINZA),

        ("texto",     "Versão 1.01 — Julho de 2026",                      CINZA),
    ]

    # Pré-renderiza todas as linhas
    linhas_render = []
    altura_total  = 20   # margem superior
    for tipo, texto, cor in secoes:
        if tipo == "separador":
            linhas_render.append(("sep", None, 0))
            altura_total += 18
        elif tipo == "titulo":
            surf = fonte_grande.render(texto, True, cor)
            linhas_render.append(("surf", surf, 0))
            altura_total += surf.get_height() + 4
        elif tipo == "subtitulo":
            surf = fonte_media.render(texto, True, cor)
            linhas_render.append(("surf", surf, 0))
            altura_total += surf.get_height() + 4
        elif tipo == "destaque":
            surf = fontes["grande"].render(texto, True, cor)
            linhas_render.append(("surf", surf, 0))
            altura_total += surf.get_height() + 4
        else:   # texto
            surf = fonte_pequena.render(texto, True, cor)
            linhas_render.append(("surf", surf, 0))
            altura_total += surf.get_height() + 2
    altura_total += 80   # espaço para o botão voltar

    scroll      = 0
    scroll_max  = max(0, altura_total - ALTURA + 20)
    btn_voltar  = pygame.Rect(LARGURA // 2 - 120, ALTURA - 52, 240, 42)
    animacao    = 0   # contador para efeitos visuais sutis

    while True:
        animacao += 1
        tela.fill((20, 20, 40))   # fundo escuro azulado

        # Estrelas de fundo (efeito decorativo)
        random.seed(42)
        for _ in range(40):
            sx = random.randint(0, LARGURA)
            sy = random.randint(0, ALTURA)
            brilho = 100 + int(55 * math.sin(animacao * 0.03 + sx))
            pygame.draw.circle(tela, (brilho, brilho, brilho), (sx, sy), 1)
        random.seed()   # restaura semente aleatória

        # Linha decorativa superior
        pygame.draw.line(tela, AMARELO, (40, 55), (LARGURA - 40, 55), 2)

        # Renderiza conteúdo com scroll
        cy = 20 - scroll
        for tipo_r, surf_r, _ in linhas_render:
            if tipo_r == "sep":
                if 0 < cy < ALTURA - 60:
                    pygame.draw.line(tela, (80, 80, 80),
                                     (60, cy + 8), (LARGURA - 60, cy + 8), 1)
                cy += 18
            else:
                if -surf_r.get_height() < cy < ALTURA - 60:
                    tela.blit(surf_r, (LARGURA // 2 - surf_r.get_width() // 2, cy))
                cy += surf_r.get_height() + (4 if surf_r.get_height() > 20 else 2)

        # Gradiente inferior para indicar scroll
        for i in range(40):
            alpha = int(200 * i / 40)
            s = pygame.Surface((LARGURA, 1))
            s.set_alpha(alpha)
            s.fill((20, 20, 40))
            tela.blit(s, (0, ALTURA - 60 - i))

        # Botão voltar
        mx, my = escalar_mouse(pygame.mouse.get_pos())
        hover  = btn_voltar.collidepoint(mx, my)
        pygame.draw.rect(tela, CINZA_ESCURO, btn_voltar, border_radius=10)
        pygame.draw.rect(tela, CIANO if hover else CINZA, btn_voltar, 2, border_radius=10)
        t_v = fonte_media.render("←  Voltar ao Menu", True, BRANCO)
        tela.blit(t_v, (btn_voltar.centerx - t_v.get_width() // 2,
                        btn_voltar.centery - t_v.get_height() // 2))

        # Indica scroll se houver mais conteúdo
        if scroll_max > 0:
            t_sc = fonte_pequena.render("▼  role para baixo", True, CINZA)
            tela.blit(t_sc, (LARGURA // 2 - t_sc.get_width() // 2, ALTURA - 55))

        desenhar_btn_fullscreen(tela)
        atualizar_tela(tela)
        clock.tick(FRAMES_POR_SEG)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
                    return
                if evento.key == pygame.K_F11:
                    alternar_tela_cheia()
                if evento.key == pygame.K_DOWN:
                    scroll = min(scroll + 30, scroll_max)
                if evento.key == pygame.K_UP:
                    scroll = max(scroll - 30, 0)
            if evento.type == pygame.MOUSEWHEEL:
                scroll = max(0, min(scroll - evento.y * 25, scroll_max))
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos_esc = escalar_mouse(evento.pos)
                if BTN_FS_RECT.collidepoint(pos_esc):
                    alternar_tela_cheia()
                elif btn_voltar.collidepoint(pos_esc):
                    return


def tela_cara_ou_coroa(tela, fontes, configuracao_times):
    """
    Anima uma moeda girando e sorteia quem começa jogando.
    Retorna 0 (jogador 1) ou 1 (jogador 2/computador).
    """
    clock  = pygame.time.Clock()
    nome_j1 = configuracao_times[0]["nome"]
    nome_j2 = configuracao_times[1]["nome"]
    cor_j1  = configuracao_times[0]["cor"]
    cor_j2  = configuracao_times[1]["cor"]

    resultado = random.randint(0, 1)   # sorteia imediatamente

    # ── Fases da animação ────────────────────────────────
    # fase 0: moeda girando (60 frames)
    # fase 1: moeda aterrissa na face correta (30 frames)
    # fase 2: exibe vencedor + aguarda clique/tecla
    GIRO_FRAMES    = 90   # duração do giro
    POUSO_FRAMES   = 30
    fase_anim      = 0
    frame_anim     = 0
    aguardando     = False

    cx = LARGURA  // 2
    cy = ALTURA   // 2
    R  = 68   # raio da moeda

    while True:
        tela.fill((20, 20, 40))

        # Estrelas decorativas
        random.seed(7)
        for _ in range(40):
            sx = random.randint(0, LARGURA)
            sy = random.randint(0, ALTURA)
            pygame.draw.circle(tela, (120, 120, 160), (sx, sy), 1)
        random.seed()

        # Título
        t1 = fontes["grande"].render("CARA OU COROA", True, AMARELO)
        tela.blit(t1, (cx - t1.get_width() // 2, 60))
        t2 = fontes["pequena"].render("Sorteando quem começa jogando...", True, BEGE)
        tela.blit(t2, (cx - t2.get_width() // 2, 108))

        cara_rect = pygame.Rect(cx - 320, 150, 250, 74)
        coroa_rect = pygame.Rect(cx + 70, 150, 250, 74)
        for face_rect, face_nome, nome_time, cor_time in (
            (cara_rect, "CARA", nome_j1, cor_j1),
            (coroa_rect, "COROA", nome_j2, cor_j2),
        ):
            pygame.draw.rect(tela, (28, 28, 52), face_rect, border_radius=14)
            pygame.draw.rect(tela, BRANCO, face_rect, 1, border_radius=14)
            pygame.draw.rect(tela, cor_time, face_rect, 3, border_radius=14)
            txt_face = fontes["pequena"].render(face_nome, True, BRANCO)
            tela.blit(txt_face, (face_rect.centerx - txt_face.get_width() // 2, face_rect.y + 10))
            txt_time = fontes["media"].render(nome_time, True, cor_time)
            desenhar_texto_contornado(
                tela, fontes["media"], nome_time, cor_time,
                (face_rect.centerx - txt_time.get_width() // 2, face_rect.y + 34)
            )

        # ── Desenho da moeda ────────────────────────────────
        if fase_anim == 0:
            # Giro: escala horizontal oscila com seno → ilusão de rotação 3D
            t_frac   = frame_anim / GIRO_FRAMES
            # acelera no início, desacelera no fim
            omega    = 2 * math.pi * (6 * t_frac - 3 * t_frac ** 2)
            escala_x = abs(math.cos(omega))
            w_moeda  = max(4, int(R * 2 * escala_x))
            # Alterna cor da face durante o giro
            face_visivel = int(omega / math.pi) % 2
            cor_moeda = AMARELO if face_visivel == 0 else CINZA
            cor_texto_moeda = PRETO
        elif fase_anim == 1:
            # Pouso: escala vai de 0 até 1
            t_pouso  = frame_anim / POUSO_FRAMES
            escala_x = t_pouso
            w_moeda  = max(4, int(R * 2 * escala_x))
            cor_moeda = AMARELO if resultado == 0 else CINZA
            cor_texto_moeda = PRETO
        else:
            # Resultado fixo
            w_moeda  = R * 2
            cor_moeda = AMARELO if resultado == 0 else CINZA
            cor_texto_moeda = PRETO

        moeda_rect = pygame.Rect(cx - w_moeda // 2, cy - R, w_moeda, R * 2)
        # Sombra
        pygame.draw.ellipse(tela, CINZA_ESCURO,
                            (moeda_rect.x + 6, moeda_rect.y + 6,
                             moeda_rect.width, moeda_rect.height))
        # Moeda
        pygame.draw.ellipse(tela, cor_moeda, moeda_rect)
        pygame.draw.ellipse(tela, BRANCO, moeda_rect, 3)
        # Letra C/K no centro
        if w_moeda > 20:
            letra = "C" if (fase_anim < 2 and (int(frame_anim * 0.3) % 2 == 0)) else \
                    ("C" if resultado == 0 else "K")
            tl = fontes["grande"].render(letra, True, cor_texto_moeda)
            tela.blit(tl, (moeda_rect.centerx - tl.get_width() // 2,
                           moeda_rect.centery - tl.get_height() // 2))

        # ── Resultado (fase 2) ──────────────────────────────
        if aguardando:
            nome_venc = nome_j1 if resultado == 0 else nome_j2
            cor_venc  = cor_j1  if resultado == 0 else cor_j2
            face_str  = "CARA" if resultado == 0 else "COROA"
            t_face = fontes["media"].render(f"Saiu: {face_str}!", True, cor_venc)
            desenhar_texto_contornado(
                tela, fontes["media"], f"Saiu: {face_str}!", cor_venc,
                (cx - t_face.get_width() // 2, cy + R + 20)
            )
            t_vez = fontes["grande"].render(f"{nome_venc} começa!", True, cor_venc)
            desenhar_texto_contornado(
                tela, fontes["grande"], f"{nome_venc} começa!", cor_venc,
                (cx - t_vez.get_width() // 2, cy + R + 55)
            )
            t_cont = fontes["pequena"].render(
                "Clique ou pressione qualquer tecla para jogar", True, CINZA)
            tela.blit(t_cont, (cx - t_cont.get_width() // 2, cy + R + 100))

        desenhar_btn_fullscreen(tela)
        atualizar_tela(tela)
        clock.tick(FRAMES_POR_SEG)

        # ── Avança animação ─────────────────────────────────
        if fase_anim == 0:
            frame_anim += 1
            if frame_anim >= GIRO_FRAMES:
                fase_anim  = 1
                frame_anim = 0
        elif fase_anim == 1:
            frame_anim += 1
            if frame_anim >= POUSO_FRAMES:
                fase_anim  = 2
                frame_anim = 0
                aguardando = True

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_F11:
                    alternar_tela_cheia()
                elif aguardando:
                    return resultado
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos_esc = escalar_mouse(evento.pos)
                if BTN_FS_RECT.collidepoint(pos_esc):
                    alternar_tela_cheia()
                elif aguardando:
                    return resultado


def tela_regras(tela, fontes):
    """
    Tela de escolha de regras do jogo.
    Retorna "normal", "12toques" ou "voltar" (para retornar ao menu de modo).
    """
    fonte_grande  = fontes["grande"]
    fonte_media   = fontes["media"]
    fonte_pequena = fontes["pequena"]
    clock = pygame.time.Clock()

    # Dois botões lado a lado + botão voltar
    btn_normal  = pygame.Rect(50,  185, 375, 215)
    btn_12toque = pygame.Rect(475, 185, 375, 215)
    btn_voltar  = pygame.Rect(LARGURA // 2 - 130, 435, 260, 44)

    descr_normal = [
        "Regra clássica do jogo.",
        "Times alternam jogadas sem",
        "limite de toques.",
        "Ideal para iniciantes.",
    ]
    descr_12 = [
        "Até 12 toques coletivos por posse.",
        "Cada botão: máx. 3 toques.",
        "FALTA: errar a bola ou tocar",
        "adversário antes da bola.",
    ]

    while True:
        tela.fill(VERDE_ESCURO)

        # Título
        t1 = fonte_grande.render("ESCOLHA AS REGRAS", True, AMARELO)
        tela.blit(t1, (LARGURA // 2 - t1.get_width() // 2, 90))
        t2 = fonte_pequena.render("Selecione o conjunto de regras para esta partida", True, BEGE)
        tela.blit(t2, (LARGURA // 2 - t2.get_width() // 2, 140))

        mx, my = escalar_mouse(pygame.mouse.get_pos())
        h_n = btn_normal.collidepoint(mx, my)
        h_12 = btn_12toque.collidepoint(mx, my)
        h_v = btn_voltar.collidepoint(mx, my)

        # ── Botão Regra Normal ───────────────────────────────
        pygame.draw.rect(tela, (20, 60, 160) if not h_n else AZUL,
                         btn_normal, border_radius=14)
        pygame.draw.rect(tela, BRANCO, btn_normal, 2, border_radius=14)
        tn = fonte_media.render("⚪  Regra Normal", True, BRANCO)
        tela.blit(tn, (btn_normal.centerx - tn.get_width() // 2, btn_normal.y + 16))
        pygame.draw.line(tela, (100, 130, 220),
                         (btn_normal.x + 20, btn_normal.y + 52),
                         (btn_normal.right - 20, btn_normal.y + 52), 1)
        for i, linha in enumerate(descr_normal):
            tl = fonte_pequena.render(linha, True, BEGE)
            tela.blit(tl, (btn_normal.centerx - tl.get_width() // 2,
                           btn_normal.y + 62 + i * 26))

        # ── Botão Regra 12 Toques ────────────────────────────
        pygame.draw.rect(tela, (140, 20, 20) if not h_12 else VERMELHO,
                         btn_12toque, border_radius=14)
        pygame.draw.rect(tela, BRANCO, btn_12toque, 2, border_radius=14)
        t12 = fonte_media.render("🔴  Regra dos 12 Toques", True, BRANCO)
        tela.blit(t12, (btn_12toque.centerx - t12.get_width() // 2, btn_12toque.y + 16))
        pygame.draw.line(tela, (220, 100, 100),
                         (btn_12toque.x + 20, btn_12toque.y + 52),
                         (btn_12toque.right - 20, btn_12toque.y + 52), 1)
        for i, linha in enumerate(descr_12):
            tl = fonte_pequena.render(linha, True, BEGE)
            tela.blit(tl, (btn_12toque.centerx - tl.get_width() // 2,
                           btn_12toque.y + 62 + i * 26))

        # ── Botão Voltar ─────────────────────────────────────
        pygame.draw.rect(tela, CINZA_ESCURO, btn_voltar, border_radius=10)
        pygame.draw.rect(tela, CIANO if h_v else CINZA, btn_voltar, 2, border_radius=10)
        tv = fonte_media.render("← Voltar", True, BRANCO)
        tela.blit(tv, (btn_voltar.centerx - tv.get_width() // 2,
                       btn_voltar.centery - tv.get_height() // 2))

        desenhar_btn_fullscreen(tela)
        atualizar_tela(tela)
        clock.tick(FRAMES_POR_SEG)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return "voltar"
                if evento.key == pygame.K_F11:
                    alternar_tela_cheia()
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos_esc = escalar_mouse(evento.pos)
                if BTN_FS_RECT.collidepoint(pos_esc):
                    alternar_tela_cheia()
                elif btn_normal.collidepoint(pos_esc):
                    return "normal"
                elif btn_12toque.collidepoint(pos_esc):
                    return "12toques"
                elif btn_voltar.collidepoint(pos_esc):
                    return "voltar"


def tela_times(tela, fontes, modo):
    """
    Tela para escolher os times e personalizar a cor principal de cada lado.
    Retorna uma lista com duas configuracoes de time ou "voltar".
    """
    fonte_grande  = fontes["grande"]
    fonte_media   = fontes["media"]
    fonte_pequena = fontes["pequena"]
    clock = pygame.time.Clock()

    selecoes = [
        {"preset": 0, "nome": TIMES_DISPONIVEIS[0]["nome"], "cor": TIMES_DISPONIVEIS[0]["cor"]},
        {"preset": 1, "nome": TIMES_DISPONIVEIS[1]["nome"], "cor": TIMES_DISPONIVEIS[1]["cor"]},
    ]

    cards = [
        pygame.Rect(40, 170, 380, 280),
        pygame.Rect(480, 170, 380, 280),
    ]
    btn_voltar = pygame.Rect(LARGURA // 2 - 130, 470, 260, 42)
    btn_confirmar = pygame.Rect(LARGURA // 2 - 170, 522, 340, 48)

    while True:
        tela.fill((26, 90, 48))

        t1 = fonte_grande.render("ESCOLHA OS TIMES", True, AMARELO)
        tela.blit(t1, (LARGURA // 2 - t1.get_width() // 2, 70))
        subtitulo = ("Defina nome e cor do Jogador 1 e do Computador"
                     if modo == MODO_COMPUTADOR
                     else "Defina nome e cor dos dois times antes da partida")
        t2 = fonte_pequena.render(subtitulo, True, BEGE)
        tela.blit(t2, (LARGURA // 2 - t2.get_width() // 2, 118))
        dica = fonte_pequena.render(
            "Use < e > para trocar o time e clique nas cores para personalizar.",
            True, BRANCO)
        tela.blit(dica, (LARGURA // 2 - dica.get_width() // 2, 140))

        mx, my = escalar_mouse(pygame.mouse.get_pos())
        controles = []

        for idx, card in enumerate(cards):
            selecao = selecoes[idx]
            cor_time = selecao["cor"]
            cor_texto = cor_texto_contraste(cor_time)
            titulo = "JOGADOR 1" if idx == 0 else ("COMPUTADOR" if modo == MODO_COMPUTADOR else "JOGADOR 2")

            prev_rect = pygame.Rect(card.x + 18, card.y + 54, 42, 42)
            next_rect = pygame.Rect(card.right - 60, card.y + 54, 42, 42)
            hover_prev = prev_rect.collidepoint(mx, my)
            hover_next = next_rect.collidepoint(mx, my)

            pygame.draw.rect(tela, (22, 38, 28), card, border_radius=16)
            pygame.draw.rect(tela, cor_time, card, 3, border_radius=16)

            txt_titulo = fonte_media.render(titulo, True, BRANCO)
            tela.blit(txt_titulo, (card.centerx - txt_titulo.get_width() // 2, card.y + 18))

            pygame.draw.rect(tela, CIANO if hover_prev else CINZA_ESCURO, prev_rect, border_radius=8)
            pygame.draw.rect(tela, BRANCO, prev_rect, 2, border_radius=8)
            pygame.draw.rect(tela, CIANO if hover_next else CINZA_ESCURO, next_rect, border_radius=8)
            pygame.draw.rect(tela, BRANCO, next_rect, 2, border_radius=8)
            txt_prev = fonte_media.render("<", True, BRANCO)
            txt_next = fonte_media.render(">", True, BRANCO)
            tela.blit(txt_prev, (prev_rect.centerx - txt_prev.get_width() // 2,
                                 prev_rect.centery - txt_prev.get_height() // 2))
            tela.blit(txt_next, (next_rect.centerx - txt_next.get_width() // 2,
                                 next_rect.centery - txt_next.get_height() // 2))

            txt_nome = fonte_grande.render(selecao["nome"], True, cor_time)
            tela.blit(txt_nome, (card.centerx - txt_nome.get_width() // 2, card.y + 58))

            centro = (card.centerx, card.y + 140)
            pygame.draw.circle(tela, CINZA_ESCURO, (centro[0] + 3, centro[1] + 3), 30)
            pygame.draw.circle(tela, cor_time, centro, 30)
            pygame.draw.circle(tela, cor_texto, centro, 30, 2)
            txt_num = fonte_media.render(str(idx + 1), True, cor_texto)
            tela.blit(txt_num, (centro[0] - txt_num.get_width() // 2,
                                centro[1] - txt_num.get_height() // 2))

            txt_cor = fonte_pequena.render("Cor personalizada", True, BEGE)
            tela.blit(txt_cor, (card.centerx - txt_cor.get_width() // 2, card.y + 182))

            paleta_rects = []
            base_x = card.x + 32
            base_y = card.y + 210
            for cor_idx, cor in enumerate(CORES_PERSONALIZADAS):
                col = cor_idx % 4
                row = cor_idx // 4
                rect = pygame.Rect(base_x + col * 82, base_y + row * 28, 52, 20)
                paleta_rects.append((rect, cor))
                pygame.draw.rect(tela, cor, rect, border_radius=6)
                borda = cor_texto_contraste(cor) if cor == cor_time else CINZA
                espessura = 3 if cor == cor_time else 1
                pygame.draw.rect(tela, borda, rect, espessura, border_radius=6)

            controles.append({
                "prev": prev_rect,
                "next": next_rect,
                "paleta": paleta_rects,
            })

        hover_voltar = btn_voltar.collidepoint(mx, my)
        hover_confirmar = btn_confirmar.collidepoint(mx, my)

        pygame.draw.rect(tela, CINZA_ESCURO, btn_voltar, border_radius=10)
        pygame.draw.rect(tela, CIANO if hover_voltar else CINZA, btn_voltar, 2, border_radius=10)
        txt_voltar = fonte_media.render("Voltar", True, BRANCO)
        tela.blit(txt_voltar, (btn_voltar.centerx - txt_voltar.get_width() // 2,
                               btn_voltar.centery - txt_voltar.get_height() // 2))

        pygame.draw.rect(tela, (20, 120, 70) if not hover_confirmar else VERDE_CAMPO,
                         btn_confirmar, border_radius=12)
        pygame.draw.rect(tela, BRANCO, btn_confirmar, 2, border_radius=12)
        txt_ok = fonte_media.render("Confirmar selecao", True, BRANCO)
        tela.blit(txt_ok, (btn_confirmar.centerx - txt_ok.get_width() // 2,
                           btn_confirmar.centery - txt_ok.get_height() // 2))

        desenhar_btn_fullscreen(tela)
        atualizar_tela(tela)
        clock.tick(FRAMES_POR_SEG)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return "voltar"
                if evento.key == pygame.K_F11:
                    alternar_tela_cheia()
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos_esc = escalar_mouse(evento.pos)
                if BTN_FS_RECT.collidepoint(pos_esc):
                    alternar_tela_cheia()
                    continue
                if btn_voltar.collidepoint(pos_esc):
                    return "voltar"
                if btn_confirmar.collidepoint(pos_esc):
                    return [
                        {"nome": selecoes[0]["nome"], "cor": selecoes[0]["cor"]},
                        {"nome": selecoes[1]["nome"], "cor": selecoes[1]["cor"]},
                    ]

                for idx, controle in enumerate(controles):
                    if controle["prev"].collidepoint(pos_esc):
                        novo_idx = (selecoes[idx]["preset"] - 1) % len(TIMES_DISPONIVEIS)
                        selecoes[idx]["preset"] = novo_idx
                        selecoes[idx]["nome"] = TIMES_DISPONIVEIS[novo_idx]["nome"]
                        selecoes[idx]["cor"] = TIMES_DISPONIVEIS[novo_idx]["cor"]
                        break
                    if controle["next"].collidepoint(pos_esc):
                        novo_idx = (selecoes[idx]["preset"] + 1) % len(TIMES_DISPONIVEIS)
                        selecoes[idx]["preset"] = novo_idx
                        selecoes[idx]["nome"] = TIMES_DISPONIVEIS[novo_idx]["nome"]
                        selecoes[idx]["cor"] = TIMES_DISPONIVEIS[novo_idx]["cor"]
                        break
                    clicou_cor = False
                    for rect, cor in controle["paleta"]:
                        if rect.collidepoint(pos_esc):
                            selecoes[idx]["cor"] = cor
                            clicou_cor = True
                            break
                    if clicou_cor:
                        break


def tela_menu(tela, fontes):
    """
    Exibe o menu inicial para escolher o modo de jogo.
    Retorna o modo escolhido: MODO_2JOGADORES ou MODO_COMPUTADOR.
    """
    fonte_grande = fontes["grande"]
    fonte_media  = fontes["media"]
    fonte_pequena = fontes["pequena"]

    clock = pygame.time.Clock()

    while True:
        tela.fill(VERDE_ESCURO)

        # Título
        t1 = fonte_grande.render("FUTEBOL DE BOTÃO", True, AMARELO)
        t2 = fonte_media.render("Jogo Pedagógico de Matemática e Física", True, BRANCO)
        tela.blit(t1, (LARGURA // 2 - t1.get_width() // 2, 70))
        tela.blit(t2, (LARGURA // 2 - t2.get_width() // 2, 118))

        # Opções — 3 botões empilhados
        opt1_rect   = pygame.Rect(LARGURA // 2 - 200, 185, 400, 52)
        opt2_rect   = pygame.Rect(LARGURA // 2 - 200, 252, 400, 52)
        sobre_rect  = pygame.Rect(LARGURA // 2 - 200, 319, 400, 52)

        mx, my = escalar_mouse(pygame.mouse.get_pos())
        hover1 = opt1_rect.collidepoint(mx, my)
        hover2 = opt2_rect.collidepoint(mx, my)
        hover3 = sobre_rect.collidepoint(mx, my)

        pygame.draw.rect(tela, AZUL           if not hover1 else CIANO,   opt1_rect,  border_radius=10)
        pygame.draw.rect(tela, VERMELHO       if not hover2 else LARANJA, opt2_rect,  border_radius=10)
        pygame.draw.rect(tela, (60, 40, 110)  if not hover3 else ROXO,    sobre_rect, border_radius=10)
        pygame.draw.rect(tela, BRANCO, opt1_rect,  2, border_radius=10)
        pygame.draw.rect(tela, BRANCO, opt2_rect,  2, border_radius=10)
        pygame.draw.rect(tela, BRANCO, sobre_rect, 2, border_radius=10)

        t_opt1  = fonte_media.render("🎮  2 Jogadores (mesmo PC)",      True, BRANCO)
        t_opt2  = fonte_media.render("🤖  1 Jogador vs Computador",     True, BRANCO)
        t_sobre = fonte_media.render("ℹ️   Sobre o Jogo",               True, BRANCO)
        tela.blit(t_opt1,  (opt1_rect.centerx  - t_opt1.get_width()  // 2,
                            opt1_rect.centery  - t_opt1.get_height()  // 2))
        tela.blit(t_opt2,  (opt2_rect.centerx  - t_opt2.get_width()  // 2,
                            opt2_rect.centery  - t_opt2.get_height()  // 2))
        tela.blit(t_sobre, (sobre_rect.centerx - t_sobre.get_width() // 2,
                            sobre_rect.centery - t_sobre.get_height() // 2))

        # Instruções rápidas
        instrucoes = [
            "Como jogar:",
            "1. Clique em um botão do seu time (círculo colorido)",
            "2. Arraste o mouse para mirar e definir a força",
            "3. Solte para chutar!",
            "4. Marque gol levando a bola até o gol adversário.",
            "F11 = tela cheia   |   ESC = voltar ao menu",
        ]
        for i, linha in enumerate(instrucoes):
            cor = AMARELO if i == 0 else (CINZA if i == 5 else BEGE)
            t = fonte_pequena.render(linha, True, cor)
            tela.blit(t, (LARGURA // 2 - t.get_width() // 2, 395 + i * 26))

        # Botão de tela cheia visível no menu
        desenhar_btn_fullscreen(tela)

        atualizar_tela(tela)
        clock.tick(FRAMES_POR_SEG)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_F11:
                alternar_tela_cheia()
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos_esc = escalar_mouse(evento.pos)
                if BTN_FS_RECT.collidepoint(pos_esc):
                    alternar_tela_cheia()
                elif opt1_rect.collidepoint(pos_esc):
                    return MODO_2JOGADORES
                elif opt2_rect.collidepoint(pos_esc):
                    return MODO_COMPUTADOR
                elif sobre_rect.collidepoint(pos_esc):
                    tela_sobre(tela, fontes)


def tela_fim_de_jogo(tela, fontes, estado):
    """
    Exibe a tela de fim de jogo com o vencedor e permite reiniciar.
    MELHORIA FUTURA: exibir estatísticas da partida.
    """
    fonte_grande = fontes["grande"]
    fonte_media  = fontes["media"]
    fonte_pequena = fontes["pequena"]

    clock = pygame.time.Clock()

    if estado["gols_j1"] > estado["gols_j2"]:
        vencedor = estado["nome_j1"]
        cor_v = estado["cor_j1"]
    elif estado["gols_j2"] > estado["gols_j1"]:
        vencedor = estado["nome_j2"]
        cor_v = estado["cor_j2"]
    else:
        vencedor = "EMPATE!"
        cor_v = AMARELO

    while True:
        tela.fill(VERDE_ESCURO)

        t1 = fonte_grande.render("FIM DE JOGO!", True, AMARELO)
        tela.blit(t1, (LARGURA // 2 - t1.get_width() // 2, 120))

        t2 = fonte_grande.render(vencedor, True, cor_v)
        tela.blit(t2, (LARGURA // 2 - t2.get_width() // 2, 190))

        placar_str = (f"{estado['nome_j1']}  {estado['gols_j1']}  x  "
                      f"{estado['gols_j2']}  {estado['nome_j2']}")
        t3 = fonte_media.render(placar_str, True, BRANCO)
        tela.blit(t3, (LARGURA // 2 - t3.get_width() // 2, 270))

        btn_rect = pygame.Rect(LARGURA // 2 - 150, 360, 300, 55)
        mx, my = escalar_mouse(pygame.mouse.get_pos())
        hover = btn_rect.collidepoint(mx, my)
        pygame.draw.rect(tela, CIANO if hover else CINZA, btn_rect, border_radius=10)
        pygame.draw.rect(tela, BRANCO, btn_rect, 2, border_radius=10)
        t_btn = fonte_media.render("▶  Jogar Novamente", True, PRETO)
        tela.blit(t_btn, (btn_rect.centerx - t_btn.get_width() // 2,
                          btn_rect.centery - t_btn.get_height() // 2))

        # Botão de tela cheia
        desenhar_btn_fullscreen(tela)

        atualizar_tela(tela)
        clock.tick(FRAMES_POR_SEG)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_F11:
                alternar_tela_cheia()
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos_esc = escalar_mouse(evento.pos)
                if BTN_FS_RECT.collidepoint(pos_esc):
                    alternar_tela_cheia()
                elif btn_rect.collidepoint(pos_esc):
                    return   # volta para o menu principal


# ──────────────────────────────────────────────
# LOOP PRINCIPAL DO JOGO
# ──────────────────────────────────────────────

def rodar_jogo(tela, fontes, modo, regra="normal", turno_inicial=0, sons=None,
               configuracao_times=None):
    """
    Loop principal de uma partida.
    Gerencia eventos, atualiza física e desenha tudo na tela.

    modo: MODO_2JOGADORES ou MODO_COMPUTADOR
    """
    clock = pygame.time.Clock()

    # ── Criação dos objetos ──────────────────────────────
    if configuracao_times is None:
        configuracao_times = [
            {"nome": "AZUL", "cor": AZUL},
            {"nome": "VERMELHO", "cor": VERMELHO},
        ]

    nome_j1 = configuracao_times[0]["nome"]
    nome_j2 = configuracao_times[1]["nome"]
    cor_j1 = configuracao_times[0]["cor"]
    cor_j2 = configuracao_times[1]["cor"]

    botoes_t0 = criar_botoes_time(0, cor_j1)
    botoes_t1 = criar_botoes_time(1, cor_j2)
    bola      = criar_bola()

    # ── Estado do jogo ───────────────────────────────────
    estado = {
        "gols_j1":           0,
        "gols_j2":           0,
        "nome_j1":           nome_j1,
        "nome_j2":           nome_j2,
        "cor_j1":            cor_j1,
        "cor_j2":            cor_j2,
        "cpu_ativo":         (modo == MODO_COMPUTADOR),
        "turno":             turno_inicial,  # definido pelo cara ou coroa
        "num_turno":         1,
        # Fases: selecionar | mirar | animando | computador | gol | infracao
        "fase":              ("computador" if modo == MODO_COMPUTADOR and turno_inicial == 1
                              else "selecionar"),
        "botao_sel":         None,  # botão selecionado para chutar
        "pos_mouse":         (0, 0),
        "msg_pedagogica":    random.choice(MSGS_PEDAGOGICAS),
        "timer_gol":         0,
        "gol_time":          0,
        "particulas":        [],
        "max_turnos":        40,    # (legado)
        "tempo_seg":         120,
        "frames_acum":       0,
        # ── Regra dos 12 toques ──────────────────────────────
        "regra":             regra,
        "toques_coletivos":  0,     # toques na posse atual
        "toques_individuais": {},   # {(time, numero): count}
        "botao_lancado":     None,  # referência ao botão lançado no turno atual
        "primeira_colisao":  None,  # "bola" | "oponente" | None
        "infracao_msg":      "",
        "infracao_timer":    0,
        "infracao_tipo":     "falta",  # "falta" | "fim_posse"
        # ── Timer de 5 segundos por toque ────────────────────
        "timer_toque":          5 * FRAMES_POR_SEG,  # 300 frames = 5 s
        # ── Bola tocou botão adversário ─────────────────
        "bola_tocou_oponente":  False,
        "ultimo_contato_bola":  None,
    }

    delay_computador = 0   # pequeno delay antes da jogada do PC
    # Cooldowns de som de colisão (em frames) para evitar repetição excessiva
    # Conceito: sem cooldown, o som tocaria dezenas de vezes enquanto os
    # objetos estiverem sobrepostos, causando distorção.
    cd_som_bola  = 0   # cooldown para som botão↔bola
    cd_som_botao = 0   # cooldown para som botão↔botão

    # ── Loop principal ───────────────────────────────────
    while True:

        # ── Eventos ─────────────────────────────────────
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return   # volta ao menu
                if evento.key == pygame.K_F11:
                    alternar_tela_cheia()

            # Botão de tela cheia (clicável a qualquer momento)
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if BTN_FS_RECT.collidepoint(escalar_mouse(evento.pos)):
                    alternar_tela_cheia()

            # Fase: selecionar botão
            if estado["fase"] == "selecionar" and estado["turno"] == 0:
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    pos_j = escalar_mouse(evento.pos)
                    for b in botoes_t0:
                        dist = math.sqrt((b.x - pos_j[0])**2 +
                                         (b.y - pos_j[1])**2)
                        if dist <= b.raio + 5:
                            # Na regra dos 12 toques, ignora botão esgotado
                            k = (b.time, b.numero)
                            if (estado["regra"] == "12toques" and
                                    estado["toques_individuais"].get(k, 0) >= 3):
                                break
                            # Deseleciona anterior
                            if estado["botao_sel"]:
                                estado["botao_sel"].selecionado = False
                            b.selecionado = True
                            estado["botao_sel"] = b
                            estado["fase"] = "mirar"
                            break

            elif estado["fase"] == "selecionar" and estado["turno"] == 1 and modo == MODO_2JOGADORES:
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    pos_j = escalar_mouse(evento.pos)
                    for b in botoes_t1:
                        dist = math.sqrt((b.x - pos_j[0])**2 +
                                         (b.y - pos_j[1])**2)
                        if dist <= b.raio + 5:
                            k = (b.time, b.numero)
                            if (estado["regra"] == "12toques" and
                                    estado["toques_individuais"].get(k, 0) >= 3):
                                break
                            if estado["botao_sel"]:
                                estado["botao_sel"].selecionado = False
                            b.selecionado = True
                            estado["botao_sel"] = b
                            estado["fase"] = "mirar"
                            break

            # Fase: mirar e soltar
            elif estado["fase"] == "mirar":
                if evento.type == pygame.MOUSEMOTION:
                    estado["pos_mouse"] = escalar_mouse(evento.pos)

                if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                    # Lança o botão
                    b = estado["botao_sel"]
                    if b:
                        vx, vy = calcular_velocidade(b.pos, estado["pos_mouse"])
                        b.vx = vx
                        b.vy = vy
                        b.selecionado = False
                        estado["botao_sel"] = None
                        estado["fase"] = "animando"
                        # Rastreamento para a regra dos 12 toques
                        estado["botao_lancado"]   = b
                        estado["primeira_colisao"] = None
                        estado["bola_tocou_oponente"] = False
                        estado["ultimo_contato_bola"] = None
                        estado["timer_toque"]     = 5 * FRAMES_POR_SEG
                        estado["msg_pedagogica"] = random.choice(MSGS_PEDAGOGICAS)
                        if sons and sons.get("chute"):
                            sons["chute"].play()

        # ── Lógica do computador ─────────────────────────
        if estado["fase"] == "computador":
            delay_computador += 1
            if delay_computador >= FRAMES_POR_SEG:  # espera 1 segundo
                delay_computador = 0
                ti_cpu = (estado["toques_individuais"]
                          if estado["regra"] == "12toques" else None)
                botao_cpu, (vx, vy) = jogada_computador(botoes_t1, bola, ti_cpu)
                if botao_cpu:
                    botao_cpu.vx = vx
                    botao_cpu.vy = vy
                    # Rastreamento para a regra dos 12 toques
                    estado["botao_lancado"]    = botao_cpu
                    estado["primeira_colisao"] = None
                    estado["bola_tocou_oponente"] = False
                    estado["ultimo_contato_bola"] = None
                estado["fase"] = "animando"
                estado["msg_pedagogica"] = random.choice(MSGS_PEDAGOGICAS)

        # ── Física ───────────────────────────────────────
        if estado["fase"] in ("animando", "computador"):
            todos_botoes = botoes_t0 + botoes_t1

            # Move todos os objetos
            for b in todos_botoes:
                b.mover()
                b.colidir_bordas()
            bola.mover()
            bola.colidir_bordas()

            # Colisões botão ↔ bola
            houve_contato_bola = False
            for b in todos_botoes:
                if b.verificar_colisao(bola):
                    houve_contato_bola = True
                    contato_bola = (b.time, b.numero)
                    novo_contato = estado.get("ultimo_contato_bola") != contato_bola
                    # Captura velocidade da bola ANTES da colisão
                    # (após a colisão frontal a bola pode parar — checar depois daria falso negativo)
                    vel_bola_antes = abs(bola.vx) + abs(bola.vy)
                    b.resolver_colisao(bola)
                    # Regra 12 toques: registra se o botão lançado tocou a bola
                    if (estado["regra"] == "12toques" and
                            estado.get("botao_lancado") is b and
                            estado.get("primeira_colisao") is None):
                        estado["primeira_colisao"] = "bola"
                    # A posse só passa se o último contato relevante da bola
                    # terminar no adversário.
                    if estado["regra"] == "12toques" and novo_contato and vel_bola_antes > 0.5:
                        if b.time != estado["turno"]:
                            estado["bola_tocou_oponente"] = True
                        elif estado["bola_tocou_oponente"]:
                            estado["bola_tocou_oponente"] = False
                    estado["ultimo_contato_bola"] = contato_bola
                    # Toca som apenas se o cooldown zerou e há velocidade real
                    if cd_som_bola == 0 and (abs(b.vx) + abs(b.vy)) > 1.0:
                        if sons and sons.get("bola"):
                            sons["bola"].play()
                        cd_som_bola = 8   # bloqueia por 8 frames (~0,13s)
            if not houve_contato_bola:
                estado["ultimo_contato_bola"] = None

            # Colisões botão ↔ botão
            for i in range(len(todos_botoes)):
                for j in range(i + 1, len(todos_botoes)):
                    bi = todos_botoes[i]
                    bj = todos_botoes[j]
                    if bi.verificar_colisao(bj):
                        bi.resolver_colisao(bj)
                        # Regra 12 toques: botão lançado acertou adversário antes da bola?
                        if (estado["regra"] == "12toques" and
                                estado.get("primeira_colisao") is None):
                            blnc = estado.get("botao_lancado")
                            if blnc is bi and bj.time != estado["turno"]:
                                estado["primeira_colisao"] = "oponente"
                            elif blnc is bj and bi.time != estado["turno"]:
                                estado["primeira_colisao"] = "oponente"
                        if cd_som_botao == 0 and (abs(bi.vx) + abs(bi.vy)) > 1.0:
                            if sons and sons.get("botao"):
                                sons["botao"].play()
                            cd_som_botao = 8

            # Decrementa cooldowns a cada frame
            if cd_som_bola  > 0: cd_som_bola  -= 1
            if cd_som_botao > 0: cd_som_botao -= 1

            # Verifica gol
            marcou = verificar_gol(bola)
            if marcou is not None:
                if marcou == 0:
                    estado["gols_j1"] += 1
                else:
                    estado["gols_j2"] += 1
                estado["fase"]       = "gol"
                estado["timer_gol"]  = 0
                estado["gol_time"]   = marcou
                # Confête explode no centro do campo
                cx_gol = CAMPO_X + CAMPO_LARG // 2
                cy_gol = CAMPO_Y + CAMPO_ALT  // 2
                estado["particulas"] = [Particula(cx_gol, cy_gol) for _ in range(80)]
                if sons and sons.get("gol"):
                    sons["gol"].play()

            # Verifica se tudo parou → fim da jogada
            elif estado["fase"] == "animando" and tudo_parado(botoes_t0, botoes_t1, bola):
                estado["num_turno"] += 1
                bola_oponente = estado["bola_tocou_oponente"]
                estado["bola_tocou_oponente"] = False  # reseta para próxima jogada

                if estado["regra"] == "12toques":
                    # ── Avalia a jogada dentro da regra dos 12 toques ──
                    prim_col   = estado.get("primeira_colisao")
                    botao_lanc = estado.get("botao_lancado")
                    infracao   = None
                    fim_posse  = False

                    if prim_col is None:
                        infracao = "FALTA! O botão não tocou na bola."
                    elif prim_col == "oponente":
                        infracao = "FALTA! Adversário tocado antes da bola."
                    elif botao_lanc:
                        k = (botao_lanc.time, botao_lanc.numero)
                        estado["toques_coletivos"] += 1
                        estado["toques_individuais"][k] = (
                            estado["toques_individuais"].get(k, 0) + 1)
                        # Checa limites
                        if estado["toques_individuais"][k] > 3:
                            infracao = (f"FALTA! Botão {k[1]+1} ultrapassou "
                                        "3 toques individuais.")
                        elif estado["toques_coletivos"] >= 12:
                            fim_posse = True
                        elif bola_oponente:
                            # Bola tocou botão adversário → transfere posse
                            fim_posse = True

                    # Limpa rastreamento do turno
                    estado["botao_lancado"]    = None
                    estado["primeira_colisao"] = None
                    estado["ultimo_contato_bola"] = None

                    if infracao:
                        estado["fase"]          = "infracao"
                        estado["infracao_msg"]  = infracao
                        estado["infracao_timer"] = 100
                        estado["infracao_tipo"] = "falta"
                    elif fim_posse:
                        msg_posse = ("A bola tocou o adversário! Posse transferida."
                                     if bola_oponente and estado["toques_coletivos"] < 12
                                     else "Fim da posse! (12 toques atingidos)")
                        estado["fase"]          = "infracao"
                        estado["infracao_msg"]  = msg_posse
                        estado["infracao_timer"] = 80
                        estado["infracao_tipo"] = "fim_posse"
                    else:
                        # Mesma equipe continua jogando
                        estado["timer_toque"] = 5 * FRAMES_POR_SEG
                        if modo == MODO_COMPUTADOR and estado["turno"] == 1:
                            estado["fase"] = "computador"
                        else:
                            estado["fase"] = "selecionar"
                else:
                    # Modo normal: alterna turno após cada jogada
                    # (bola_oponente já implica troca de turno no modo normal)
                    estado["turno"] = 1 - estado["turno"]
                    estado["timer_toque"] = 5 * FRAMES_POR_SEG
                    if modo == MODO_COMPUTADOR and estado["turno"] == 1:
                        estado["fase"] = "computador"
                    else:
                        estado["fase"] = "selecionar"

        # ── Timer após gol ────────────────────────────────
        if estado["fase"] == "gol":
            # Atualiza e remove partículas de confete mortas
            estado["particulas"] = [p for p in estado["particulas"] if p.vivo()]
            for p in estado["particulas"]:
                p.atualizar()
            estado["timer_gol"] += 1
            if estado["timer_gol"] > FRAMES_POR_SEG * 3:  # 3 segundos
                # Reinicia bola e botões
                botoes_t0 = criar_botoes_time(0, estado["cor_j1"])
                botoes_t1 = criar_botoes_time(1, estado["cor_j2"])
                bola      = criar_bola()
                # Zera contagens da regra dos 12 toques
                estado["toques_coletivos"]  = 0
                estado["toques_individuais"] = {}
                estado["botao_lancado"]     = None
                estado["primeira_colisao"]  = None
                estado["bola_tocou_oponente"] = False
                estado["ultimo_contato_bola"] = None
                # Alterna turno após gol
                estado["turno"] = 1 - estado["turno"]
                estado["timer_toque"] = 5 * FRAMES_POR_SEG
                if modo == MODO_COMPUTADOR and estado["turno"] == 1:
                    estado["fase"] = "computador"
                else:
                    estado["fase"] = "selecionar"

        # ── Fase de infração (regra dos 12 toques) ───────────
        if estado["fase"] == "infracao":
            estado["infracao_timer"] -= 1
            if estado["infracao_timer"] <= 0:
                # Transfere posse para o adversário e zera contagens
                estado["turno"]              = 1 - estado["turno"]
                estado["toques_coletivos"]   = 0
                estado["toques_individuais"] = {}
                estado["botao_lancado"]      = None
                estado["primeira_colisao"]   = None
                estado["bola_tocou_oponente"] = False
                estado["ultimo_contato_bola"] = None
                estado["timer_toque"]        = 5 * FRAMES_POR_SEG
                if modo == MODO_COMPUTADOR and estado["turno"] == 1:
                    estado["fase"] = "computador"
                else:
                    estado["fase"] = "selecionar"

        # ── Timer de 5 s por toque (regra dos 12 toques) ─────────
        if (estado["regra"] == "12toques" and
                estado["fase"] in ("selecionar", "mirar")):
            # O timer só corre para jogadores humanos
            # (computador age em 1 s dentro da fase "computador")
            if estado["turno"] == 0 or modo == MODO_2JOGADORES:
                estado["timer_toque"] -= 1
                if estado["timer_toque"] <= 0:
                    # Deseleciona botão se estava mirando
                    if estado.get("botao_sel"):
                        estado["botao_sel"].selecionado = False
                        estado["botao_sel"] = None
                    estado["fase"]          = "infracao"
                    estado["infracao_msg"]  = "TEMPO ESGOTADO! (máx. 5 segundos)"
                    estado["infracao_timer"] = 100
                    estado["infracao_tipo"] = "falta"

        # ── Verificação: todos os botões esgotados (regra 12 toques) ──
        if estado["fase"] == "selecionar" and estado["regra"] == "12toques":
            botoes_vez = botoes_t0 if estado["turno"] == 0 else botoes_t1
            ti = estado["toques_individuais"]
            if all(ti.get((b.time, b.numero), 0) >= 3 for b in botoes_vez):
                # Todos os botões do time atingiram o limite individual
                estado["fase"]          = "infracao"
                estado["infracao_msg"]  = "Todos os botões esgotados! Posse encerrada."
                estado["infracao_timer"] = 80
                estado["infracao_tipo"] = "fim_posse"

        # ── Cronômetro regressivo ────────────────────────────
        # Conta frames; a cada 60 frames (1 segundo) decrementa o tempo.
        # O tempo pausa durante a celebração de gol e infração.
        # Conceito pedagógico: 1 s = 60 frames → divisão e módulo.
        if estado["fase"] not in ("gol", "infracao") and estado["tempo_seg"] > 0:
            estado["frames_acum"] += 1
            if estado["frames_acum"] >= FRAMES_POR_SEG:
                estado["frames_acum"] = 0
                estado["tempo_seg"]  -= 1

        # ── Verifica fim de partida (tempo esgotado) ─────────
        if estado["tempo_seg"] <= 0:
            tela_fim_de_jogo(tela, fontes, estado)
            return

        # ── Desenho ──────────────────────────────────────
        desenhar_campo(tela)

        # Redes (com animação de balanço após gol)
        desenhar_redes(tela, estado)

        # Desenha botões
        for b in botoes_t0 + botoes_t1:
            if estado["regra"] == "12toques":
                ti = estado["toques_individuais"]
                tc = ti.get((b.time, b.numero), 0)
                b.desenhar(tela, fontes["pequena"], toque_count=tc, maxed_out=(tc >= 3))
            else:
                b.desenhar(tela, fontes["pequena"])

        # Desenha bola
        bola.desenhar(tela)

        # Desenha linha de mira
        if estado["fase"] == "mirar" and estado["botao_sel"]:
            desenhar_mira(tela, estado["botao_sel"], estado["pos_mouse"])

        # HUD
        desenhar_hud(tela, fontes, estado)

        # Animação de celebração (sobreposta a tudo)
        if estado["fase"] == "gol":
            desenhar_celebracao_gol(tela, estado, fontes)

        # Overlay de infração (regra dos 12 toques)
        if estado["fase"] == "infracao":
            overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
            overlay.fill((80, 0, 0, 110))
            tela.blit(overlay, (0, 0))
            msg = estado.get("infracao_msg", "FALTA!")
            tipo = estado.get("infracao_tipo", "falta")
            cor_inf = VERMELHO if tipo == "falta" else AMARELO
            # Sombra
            sombra = fontes["grande"].render(msg, True, PRETO)
            tela.blit(sombra,
                      (LARGURA // 2 - sombra.get_width() // 2 + 3,
                       ALTURA  // 2 - sombra.get_height() // 2 + 3))
            # Texto principal
            txt_inf = fontes["grande"].render(msg, True, cor_inf)
            tela.blit(txt_inf,
                      (LARGURA // 2 - txt_inf.get_width() // 2,
                       ALTURA  // 2 - txt_inf.get_height() // 2))

        atualizar_tela(tela)
        clock.tick(FRAMES_POR_SEG)


# ──────────────────────────────────────────────
# PONTO DE ENTRADA
# ──────────────────────────────────────────────

def main():
    """
    Função principal: inicializa o Pygame, cria a janela
    e entra no loop menu → jogo → menu.
    """
    # Configura o mixer ANTES do pygame.init() para garantir o formato correto
    # 44100 Hz, 16-bit com sinal, estéreo, buffer de 512 amostras
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()

    pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Futebol de Botão — Jogo Pedagógico")

    # Surface lógica: o jogo é sempre desenhado em 900×600 e depois escalado
    # para a tela real. Isso permite tela cheia (F11) sem alterar a lógica.
    tela = pygame.Surface((LARGURA, ALTURA))

    # Fontes maiores para melhor legibilidade e acessibilidade
    # MELHORIA FUTURA: carregar uma fonte TTF personalizada com pygame.font.Font()
    fontes = {
        "grande":  pygame.font.SysFont("Arial", 32, bold=True),
        "media":   pygame.font.SysFont("Arial", 24),
        "pequena": pygame.font.SysFont("Arial", 17),
        "gol":     pygame.font.SysFont("Arial", 80, bold=True),  # celebração de gol
    }

    # Sintetiza sons programaticamente (sem arquivos externos)
    sons = criar_sons()

    # Loop: menu → escolha de regra → partida → menu
    while True:
        modo = tela_menu(tela, fontes)
        while True:
            regra = tela_regras(tela, fontes)
            if regra == "voltar":
                break

            configuracao_times = tela_times(tela, fontes, modo)
            if configuracao_times == "voltar":
                continue

            turno_inicial = tela_cara_ou_coroa(tela, fontes, configuracao_times)
            rodar_jogo(tela, fontes, modo, regra, turno_inicial, sons, configuracao_times)
            break


if __name__ == "__main__":
    main()
