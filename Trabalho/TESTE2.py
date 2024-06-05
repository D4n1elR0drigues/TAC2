import pygame
import sys
from PIL import Image
import mysql.connector

# Definições
LARGURA, ALTURA = 500, 500
MARGEM = 39  # Espaço entre o tabuleiro e a janela
LINHAS, COLUNAS = 8, 8
TAMANHO_QUADRADO = (ALTURA - 2 * MARGEM) // LINHAS

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (128, 128, 128)

# Conectar ao banco de dados MySQL
def conectar_banco():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="databasedama"
    )

class Display:
    def __init__(self):
        pygame.init()
        self.janela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Jogo de Damas")
        self.relogio = pygame.time.Clock()

class Evento:
    @staticmethod
    def obter_posicao_mouse():
        return pygame.mouse.get_pos()

class Images:
    @staticmethod
    def carregar_imagens():
        imagem_tabuleiro_original = Image.open("Imagens/imagemTabuleiro.PNG")
        imagem_tabuleiro = imagem_tabuleiro_original.resize((LARGURA, ALTURA))

        sprites_imagem = pygame.image.load('Sprites/pecas.png').convert_alpha()

        imagem_peca_branca_original = sprites_imagem.subsurface(pygame.Rect(130, 103, 190, 190))
        imagem_peca_branca = pygame.transform.scale(imagem_peca_branca_original, (TAMANHO_QUADRADO, TAMANHO_QUADRADO))

        imagem_peca_preto_original = sprites_imagem.subsurface(pygame.Rect(130, 378, 190, 190))
        imagem_peca_preto = pygame.transform.scale(imagem_peca_preto_original, (TAMANHO_QUADRADO, TAMANHO_QUADRADO))

        imagem_peca_branca_dama_original = sprites_imagem.subsurface(pygame.Rect(401, 103, 190, 190))
        imagem_peca_branca_dama = pygame.transform.scale(imagem_peca_branca_dama_original, (TAMANHO_QUADRADO, TAMANHO_QUADRADO))

        imagem_peca_preto_dama_original = sprites_imagem.subsurface(pygame.Rect(401, 222, 190, 190))
        imagem_peca_preto_dama = pygame.transform.scale(imagem_peca_preto_dama_original, (TAMANHO_QUADRADO, TAMANHO_QUADRADO))
        
        return imagem_tabuleiro, imagem_peca_branca, imagem_peca_preto, imagem_peca_branca_dama, imagem_peca_preto_dama

class Player:
    def __init__(self):
        self.turno = 'preto'

class Tabuleiro:
    def __init__(self):
        self.tabuleiro = [[None] * COLUNAS for _ in range(LINHAS)]
        self.display = Display()
        self.imagem_tabuleiro, self.imagem_peca_branca, self.imagem_peca_preto, self.imagem_peca_branca_dama, self.imagem_peca_preto_dama = Images.carregar_imagens()
        self.inicializar_pecas()
        self.peca_selecionada = None
        self.linha_peca_selecionada = None
        self.coluna_peca_selecionada = None
        self.player = Player()

    def inicializar_pecas(self):
        for linha in range(3):
            for coluna in range(COLUNAS):
                if (linha + coluna) % 2 == 1:
                    self.tabuleiro[linha][coluna] = "preto"

        for linha in range(LINHAS-1, LINHAS-4, -1):
            for coluna in range(COLUNAS):
                if (linha + coluna) % 2 == 1:
                    self.tabuleiro[linha][coluna] = "branco"

    def desenhar(self):
        self.display.janela.blit(pygame.image.fromstring(self.imagem_tabuleiro.tobytes(), self.imagem_tabuleiro.size, self.imagem_tabuleiro.mode), (0, 0))
        for linha in range(LINHAS):
            for coluna in range(COLUNAS):
                peca = self.tabuleiro[linha][coluna]
                if peca == "preto":
                    self.display.janela.blit(self.imagem_peca_preto, ((coluna * TAMANHO_QUADRADO) + MARGEM, (linha * TAMANHO_QUADRADO) + MARGEM))
                elif peca == "branco":
                    self.display.janela.blit(self.imagem_peca_branca, ((coluna * TAMANHO_QUADRADO) + MARGEM, (linha * TAMANHO_QUADRADO) + MARGEM))
                elif peca == "preto_dama":
                    self.display.janela.blit(self.imagem_peca_preto_dama, ((coluna * TAMANHO_QUADRADO) + MARGEM, (linha * TAMANHO_QUADRADO) + MARGEM))
                elif peca == "branco_dama":
                    self.display.janela.blit(self.imagem_peca_branca_dama, ((coluna * TAMANHO_QUADRADO) + MARGEM, (linha * TAMANHO_QUADRADO) + MARGEM))

    def obter_linha_coluna_do_mouse(self):
        pos = Evento.obter_posicao_mouse()
        x, y = pos
        linha = (y - MARGEM) // TAMANHO_QUADRADO
        coluna = (x - MARGEM) // TAMANHO_QUADRADO
        return linha, coluna

    def movimento_valido(self, linha_inicial, coluna_inicial, linha_final, coluna_final):
        if not (0 <= linha_final < LINHAS and 0 <= coluna_final < COLUNAS):
            return False
        if self.tabuleiro[linha_final][coluna_final] is not None:
            return False
        peca = self.tabuleiro[linha_inicial][coluna_inicial]
        if peca == "branco":
            return linha_final == linha_inicial - 1 and abs(coluna_final - coluna_inicial) == 1
        elif peca == "preto":
            return linha_final == linha_inicial + 1 and abs(coluna_final - coluna_inicial) == 1
        elif peca == "branco_dama" or peca == "preto_dama":
            return abs(linha_final - linha_inicial) == 1 and abs(coluna_final - coluna_inicial) == 1
        return False

    def mover_peca(self, linha_inicial, coluna_inicial, linha_final, coluna_final):
        self.tabuleiro[linha_final][coluna_final] = self.tabuleiro[linha_inicial][coluna_inicial]
        peca = self.tabuleiro[linha_final][coluna_final]
        if linha_final == 0 and peca == "preto":
            self.tabuleiro[linha_final][coluna_final] = "preto_dama"
        elif linha_final == LINHAS - 1 and peca == "branco":
            self.tabuleiro[linha_final][coluna_final] = "branco_dama"
        self.tabuleiro[linha_inicial][coluna_inicial] = None

class Menu:
    def __init__(self, display):
        self.display = display
        self.opcoes = ["Start Game", "Multiplayer", "Options", "Exit"]
        self.opcao_selecionada = None
        self.fonte = pygame.font.Font(None, 36)
        self.largura_opcao, self.altura_opcao = 200, 50  # Largura e altura de cada opção
        self.espacamento_opcoes = 10  # Espaçamento entre as opções

    def desenhar(self):
        self.display.janela.fill(PRETO)
        for i, opcao in enumerate(self.opcoes):
            x = (LARGURA - self.largura_opcao) // 2
            y = ((ALTURA - (len(self.opcoes) * self.altura_opcao + (len(self.opcoes) - 1) * self.espacamento_opcoes)) // 2 + i * (self.altura_opcao + self.espacamento_opcoes))
            rect = pygame.Rect(x, y, self.largura_opcao, self.altura_opcao)
            cor = BRANCO if rect.collidepoint(pygame.mouse.get_pos()) else CINZA
            pygame.draw.rect(self.display.janela, cor, rect)
            texto = self.fonte.render(opcao, True, PRETO)
            rect_texto = texto.get_rect(center=rect.center)
            self.display.janela.blit(texto, rect_texto)

    def selecionar_opcao(self):
        for i, opcao in enumerate(self.opcoes):
            x = (LARGURA - self.largura_opcao) // 2
            y = (ALTURA - (len(self.opcoes) * self.altura_opcao + (len(self.opcoes) - 1) * self.espacamento_opcoes)) // 2 + i * (self.altura_opcao + self.espacamento_opcoes)
            rect = pygame.Rect(x, y, self.largura_opcao, self.altura_opcao)
            if rect.collidepoint(pygame.mouse.get_pos()):
                if opcao == "Start Game":
                    return "start"
                elif opcao == "Multiplayer":
                    return "multiplayer"
                elif opcao == "Options":
                    return "options"
                elif opcao == "Exit":
                    return "exit"
        return None

class Login:
    def __init__(self, display):
        self.display = display
        self.fonte = pygame.font.Font(None, 36)
        self.fonte_pequena = pygame.font.Font(None, 24)
        self.username = ""
        self.password = ""
        self.erro = ""
        self.input_username = True
        self.registrando = False

    def desenhar(self):
        self.display.janela.fill(PRETO)

        titulo = self.fonte.render("Login" if not self.registrando else "Register", True, BRANCO)
        rect_titulo = titulo.get_rect(center=(LARGURA // 2, ALTURA // 4))
        self.display.janela.blit(titulo, rect_titulo)

        username_label = self.fonte_pequena.render("Username:", True, BRANCO)
        rect_username_label = username_label.get_rect(topleft=(LARGURA // 4, ALTURA // 2 - 50))
        self.display.janela.blit(username_label, rect_username_label)

        password_label = self.fonte_pequena.render("Password:", True, BRANCO)
        rect_password_label = password_label.get_rect(topleft=(LARGURA // 4, ALTURA // 2))
        self.display.janela.blit(password_label, rect_password_label)

        username_input = self.fonte_pequena.render(self.username, True, BRANCO)
        rect_username_input = pygame.Rect(LARGURA // 4 + 100, ALTURA // 2 - 50, 200, 30)
        pygame.draw.rect(self.display.janela, CINZA, rect_username_input)
        self.display.janela.blit(username_input, (LARGURA // 4 + 105, ALTURA // 2 - 45))

        password_input = self.fonte_pequena.render("*" * len(self.password), True, BRANCO)
        rect_password_input = pygame.Rect(LARGURA // 4 + 100, ALTURA // 2, 200, 30)
        pygame.draw.rect(self.display.janela, CINZA, rect_password_input)
        self.display.janela.blit(password_input, (LARGURA // 4 + 105, ALTURA // 2 + 5))

        erro_msg = self.fonte_pequena.render(self.erro, True, (255, 0, 0))
        rect_erro_msg = erro_msg.get_rect(center=(LARGURA // 2, ALTURA // 2 + 100))
        self.display.janela.blit(erro_msg, rect_erro_msg)

        login_btn = self.fonte_pequena.render("Login" if not self.registrando else "Register", True, PRETO)
        rect_login_btn = pygame.Rect(LARGURA // 2 - 50, ALTURA // 2 + 50, 100, 30)
        pygame.draw.rect(self.display.janela, BRANCO, rect_login_btn)
        rect_login_texto = login_btn.get_rect(center=rect_login_btn.center)
        self.display.janela.blit(login_btn, rect_login_texto)

        switch_btn_text = "Register" if not self.registrando else "Login"
        switch_btn = self.fonte_pequena.render(switch_btn_text, True, PRETO)
        rect_switch_btn = pygame.Rect(LARGURA // 2 - 50, ALTURA // 2 + 100, 100, 30)
        pygame.draw.rect(self.display.janela, BRANCO, rect_switch_btn)
        rect_switch_texto = switch_btn.get_rect(center=rect_switch_btn.center)
        self.display.janela.blit(switch_btn, rect_switch_texto)

    def handle_event(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            pos = pygame.mouse.get_pos()
            if (LARGURA // 4 + 100 < pos[0] < LARGURA // 4 + 300) and (ALTURA // 2 - 50 < pos[1] < ALTURA // 2 - 20):
                self.input_username = True
            elif (LARGURA // 4 + 100 < pos[0] < LARGURA // 4 + 300) and (ALTURA // 2 < pos[1] < ALTURA // 2 + 30):
                self.input_username = False
            elif (LARGURA // 2 - 50 < pos[0] < LARGURA // 2 + 50) and (ALTURA // 2 + 50 < pos[1] < ALTURA // 2 + 80):
                if self.registrando:
                    if self.registrar_usuario():
                        self.registrando = False
                    else:
                        self.erro = "Registration failed."
                else:
                    if self.verificar_login():
                        return "menu"
                    else:
                        self.erro = "Username or Password is incorrect."
            elif (LARGURA // 2 - 50 < pos[0] < LARGURA // 2 + 50) and (ALTURA // 2 + 100 < pos[1] < ALTURA // 2 + 130):
                self.registrando = not self.registrando
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_TAB:
                self.input_username = not self.input_username
            elif evento.key == pygame.K_BACKSPACE:
                if self.input_username:
                    self.username = self.username[:-1]
                else:
                    self.password = self.password[:-1]
            elif evento.key == pygame.K_RETURN:
                if self.registrando:
                    if self.registrar_usuario():
                        self.registrando = False
                    else:
                        self.erro = "Registration failed."
                else:
                    if self.verificar_login():
                        return "menu"
                    else:
                        self.erro = "Username or Password is incorrect."
            else:
                if self.input_username:
                    self.username += evento.unicode
                else:
                    self.password += evento.unicode
        return "login"

    def verificar_login(self):
        try:
            conexao = conectar_banco()
            cursor = conexao.cursor()
            query = "SELECT * FROM users WHERE username=%s AND password=%s"
            cursor.execute(query, (self.username, self.password))
            result = cursor.fetchone()
            cursor.close()
            conexao.close()
            return result is not None
        except mysql.connector.Error as err:
            self.erro = f"Database Error: {err}"
            return False

    def registrar_usuario(self):
        try:
            conexao = conectar_banco()
            cursor = conexao.cursor()
            query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(query, (self.username, self.password))
            conexao.commit()
            cursor.close()
            conexao.close()
            return True
        except mysql.connector.Error as err:
            self.erro = f"Database Error: {err}"
            return False

def main():
    display = Display()
    menu = Menu(display)
    login = Login(display)
    tabuleiro = Tabuleiro()

    estado = "login"
    executando = True

    while executando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False
            elif estado == "login":
                estado = login.handle_event(evento)
            elif estado == "menu":
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    opcao = menu.selecionar_opcao()
                    if opcao == "start":
                        estado = "jogo"
                    elif opcao == "exit":
                        executando = False
            elif estado == "jogo":
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    linha, coluna = tabuleiro.obter_linha_coluna_do_mouse()
                    if tabuleiro.peca_selecionada is None:
                        if tabuleiro.tabuleiro[linha][coluna] is not None and tabuleiro.tabuleiro[linha][coluna].startswith(tabuleiro.player.turno):
                            tabuleiro.peca_selecionada = tabuleiro.tabuleiro[linha][coluna]
                            tabuleiro.linha_peca_selecionada = linha
                            tabuleiro.coluna_peca_selecionada = coluna
                    else:
                        if tabuleiro.movimento_valido(tabuleiro.linha_peca_selecionada, tabuleiro.coluna_peca_selecionada, linha, coluna):
                            tabuleiro.mover_peca(tabuleiro.linha_peca_selecionada, tabuleiro.coluna_peca_selecionada, linha, coluna)
                            tabuleiro.player.turno = 'branco' if tabuleiro.player.turno == 'preto' else 'preto'
                        tabuleiro.peca_selecionada = None

        if estado == "login":
            login.desenhar()
        elif estado == "menu":
            menu.desenhar()
        elif estado == "jogo":
            display.desenhar_tabuleiro(tabuleiro)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
