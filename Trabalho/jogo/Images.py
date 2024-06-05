import pygame
from PIL import Image

class Images:
    @staticmethod
    def carregar_imagens(largura, altura, tamanho_quadrado):
        imagem_tabuleiro_original = Image.open("Imagens/imagemTabuleiro.PNG")
        imagem_tabuleiro = imagem_tabuleiro_original.resize((largura, altura))

        sprites_imagem = pygame.image.load('Sprites/pecas.png').convert_alpha() 

        imagem_peca_branca_original = sprites_imagem.subsurface(pygame.Rect(130, 103, 190, 190))
        imagem_peca_branca = pygame.transform.scale(imagem_peca_branca_original, (tamanho_quadrado, tamanho_quadrado))

        imagem_peca_preto_original = sprites_imagem.subsurface(pygame.Rect(130, 378, 190, 190))
        imagem_peca_preto = pygame.transform.scale(imagem_peca_preto_original, (tamanho_quadrado, tamanho_quadrado))

        imagem_peca_branca_dama = sprites_imagem.subsurface(pygame.Rect(401, 103, 190, 190))
        imagem_peca_branca_dama = pygame.transform.scale(imagem_peca_branca_dama, (tamanho_quadrado, tamanho_quadrado))

        imagem_peca_preto_dama = sprites_imagem.subsurface(pygame.Rect(401, 222, 190, 190))
        imagem_peca_preto_dama = pygame.transform.scale(imagem_peca_preto_dama, (tamanho_quadrado, tamanho_quadrado))
        
        return imagem_tabuleiro, imagem_peca_branca, imagem_peca_preto, imagem_peca_branca_dama, imagem_peca_preto_dama
