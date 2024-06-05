import pygame

class Evento:
    @staticmethod
    def obter_posicao_mouse():
        return pygame.mouse.get_pos()
