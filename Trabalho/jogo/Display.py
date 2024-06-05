import pygame

class Display:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("Jogo de Damas")
        self.clock = pygame.time.Clock()
