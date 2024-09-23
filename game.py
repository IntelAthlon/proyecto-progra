import pygame
from nonogram import Nonogram

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.nonogram = Nonogram(10, 10)  # Ejemplo de un nonograma de 10x10
        self.font = pygame.font.Font(None, 36)

    def handle_event(self, event):
        # Manejar eventos del juego
        pass

    def update(self):
        # Actualizar el estado del juego
        pass

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.nonogram.draw(self.screen)
        # Dibujar otros elementos del juego