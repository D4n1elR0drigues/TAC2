import pygame
import sys

pygame.init()

imagemSOL = pygame.image.load('imagens/SOL.png')
imagemFundo = pygame.image.load('imagens/ART.PNG')

LARGURAJANELA = imagemFundo.get_width()
ALTURAJANELA = imagemFundo.get_height()
VEL = 6

janela = pygame.display.set_mode((LARGURAJANELA, ALTURAJANELA))
janela.blit(imagemFundo, (0, 0))  # Desenha o fundo na janela
pygame.display.set_caption('Imagem, Som e Objeto')

tamanho_sol = (50, 50)
imagemSOL = pygame.transform.scale(imagemSOL, tamanho_sol)

sol = {'objRect': pygame.Rect(475, 275, 50, 50), 'imagem': imagemSOL, 'vel': VEL}

pygame.mixer.music.load('som/som.mp3')
pygame.mixer.music.play(-1, 0.0)
somAtivado = True

deve_continuar = True

while deve_continuar:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            deve_continuar = False
    
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        sol['objRect'].x -= sol['vel']
    if teclas[pygame.K_RIGHT]:
        sol['objRect'].x += sol['vel']
    if teclas[pygame.K_UP]:
        sol['objRect'].y -= sol['vel']
    if teclas[pygame.K_DOWN]:
        sol['objRect'].y += sol['vel']

    janela.blit(imagemFundo, (0, 0))
    janela.blit(sol['imagem'], sol['objRect'])

    pygame.display.update()

    pygame.time.Clock().tick(40)

pygame.quit()
