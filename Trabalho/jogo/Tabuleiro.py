import pygame
from Display import Display
from Images import Images

class Tabuleiro:
    def __init__(self, largura, altura, margem, linhas, colunas, tamanho_quadrado):
        self.tabuleiro = [[None] * colunas for _ in range(linhas)]
        self.mascaras_peca = {}
        self.display = Display(largura, altura)
        self.imagem_tabuleiro, self.imagem_peca_branca, self.imagem_peca_preto, self.imagem_peca_branca_dama, self.imagem_peca_preto_dama = Images.carregar_imagens(largura, altura, tamanho_quadrado)
        self.inicializar_pecas()
        self.peca_selecionada = None
        self.linha_peca_selecionada = None
        self.coluna_peca_selecionada = None

    def inicializar_pecas(self):
        for linha in range(3):
            for coluna in range(COLUNAS):
                if (linha + coluna) % 2 == 1:
                    self.tabuleiro[linha][coluna] = "preto"

        for linha in range(LINHAS-1, LINHAS-4, -1):
            for coluna in range(COLUNAS):
                if (linha + coluna) % 2 == 1:
                    self.tabuleiro[linha][coluna] = "branco"
    
    def criar_mascaras_peca(self):
        for linha in range(LINHAS):
            for coluna in range(COLUNAS):
                peca = self.tabuleiro[linha][coluna]
                if peca is not None:
                    if peca not in self.mascaras_peca:
                        imagem_peca = self.imagem_peca_branca if peca == 'branco' else self.imagem_peca_preto
                        self.mascaras_peca[peca] = pygame.mask.from_surface(imagem_peca)

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
            return linha_final == linha_inicial - 1 and abs(coluna_final - coluna_inicial) == 1 and not self.verificar_colisao_mascara(linha_final, coluna_final)
        elif peca == "preto":
            return linha_final == linha_inicial + 1 and abs(coluna_final - coluna_inicial) == 1 and not self.verificar_colisao_mascara(linha_final, coluna_final)
        elif peca == "branco_dama" or peca == "preto_dama":
            return abs(linha_final - linha_inicial) == 1 and abs(coluna_final - coluna_inicial) == 1 and not self.verificar_colisao_mascara(linha_final, coluna_final)
        return False

    def mover_peca(self, linha_inicial, coluna_inicial, linha_final, coluna_final):
        self.tabuleiro[linha_final][coluna_final] = self.tabuleiro[linha_inicial][coluna_inicial]
        peca = self.tabuleiro[linha_final][coluna_final]
        if linha_final == 0 and peca == "preto":
            self.tabuleiro[linha_final][coluna_final] = "preto_dama"
        elif linha_final == LINHAS - 1 and peca == "branco":
            self.tabuleiro[linha_final][coluna_final] = "branco_dama"
        self.tabuleiro[linha_inicial][coluna_inicial] = None

    def verificar_colisao_mascara(self, linha, coluna):
        for peca, mascara in self.mascaras_peca.items():
            if self.peca_selecionada is not None and self.tabuleiro[linha][coluna] is not None:
                if mascara.overlap_area(self.mascaras_peca[self.tabuleiro[linha][coluna]], (coluna*TAMANHO_QUADRADO - self.coluna_peca_selecionada*TAMANHO_QUADRADO, linha*TAMANHO_QUADRADO - self.linha_peca_selecionada*TAMANHO_QUADRADO)) is not None:
                    return True
        return False
