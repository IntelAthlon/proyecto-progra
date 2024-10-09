import pygame
from src.ui.components import Button
from src.config import *

class Menu:
    def __init__(self, game):
        self.game = game
        self.buttons = [
            Button("Seleccionar nivel", 300, 200, 200, 50, self.select_level, self.game.sound_manager),
            Button("Salir", 300, 260, 200, 50, self.quit_game, self.game.sound_manager)
        ]

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)

    def draw(self, screen):
        screen.fill(WHITE)
        font = pygame.font.Font(None, 48)
        title = font.render("AtomicGram", True, BLACK)
        screen.blit(title, (300, 100))

        for button in self.buttons:
            button.draw(screen)

    def select_level(self):
        self.game.start_new_game()

    def quit_game(self):
        pygame.quit()
        quit()

    def update(self):
        pass