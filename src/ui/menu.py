import pygame
from src.ui.components import Button
from src.config import *
from sys import exit

class Menu:
    def __init__(self, game):
        self.game = game
        screen_width, screen_height = pygame.display.get_surface().get_size()
        screen = pygame.display.set_mode((screen_width, screen_height))
        button_width, button_height = 225, 50
        spacing = 20
        total_height = 2 * button_height + spacing
        start_y = (screen_height - total_height) // 2

        self.buttons = [
            Button("Seleccionar nivel", (screen_width-button_width) // 2, start_y, button_width, button_height, self.select_level, self.game.sound_manager),
            Button("Salir", (screen_width-button_width) // 2, start_y + button_height + spacing, button_width, button_height, self.quit_game, self.game.sound_manager)
        ]

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)

    def draw(self, screen):
        font = pygame.font.Font(None, 48)
        title = font.render("AtomicGram", True, BLACK)
        title_rect = title.get_rect(center=(screen.get_width() //2, screen.get_height() // 2 - 100))
        screen.blit(title, title_rect)

        for button in self.buttons:
            button.draw(screen)

    def select_level(self):
        self.game.start_new_game()

    def quit_game(self):
        pygame.quit()
        exit()

    def update(self):
        pass