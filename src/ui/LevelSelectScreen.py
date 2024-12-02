import pygame
import os
from src.ui.Button import Button
from src.config import *

class LevelSelectScreen:
    def __init__(self, game):
        self.game = game
        self.buttons = []
        self.create_level_buttons()

    def create_level_buttons(self):
        screen_width, screen_height = pygame.display.get_surface().get_size()
        button_width, button_height = 50, 50
        padding = 10
        total_width = 10 * (button_width + padding) - padding
        total_height = ((len(self.game.levels) + 9) // 10) * (button_height + padding) - padding
        start_x = (screen_width - total_width) // 2
        start_y = (screen_height- total_height) // 2

        for i, level_key in enumerate(self.game.levels.keys()):
            row = i // 10
            col = i % 10
            x = start_x + col * (button_width + padding)
            y = start_y + row * (button_width + padding)
            self.buttons.append(Button(str(i+1), x, y, button_width, button_height, lambda lk=level_key: self.select_level(lk), self.game.sound_manager))

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.set_screen('menu')

    def draw(self, screen):
        font_path = os.path.join("assets", "fonts", "newsweekly", "newsweekly-Regular.ttf")
        font_size = 64

        border_font = pygame.font.Font(font_path, font_size)
        border_title = border_font.render("Select Level", True, WHITE)
        border_rect = border_title.get_rect(center=((screen.get_width() // 2) + 2, (screen.get_height() // 2) - 198))
        screen.blit(border_title, border_rect)

        font = pygame.font.Font(font_path, font_size)
        title = font.render("Select Level", True, BLACK)
        title_rect = title.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 200))
        screen.blit(title, title_rect)

        for button in self.buttons:
            button.draw(screen)

    def select_level(self, level_key):
        print(f"Cargando el nivel {level_key}")
        self.game.start_level(level_key)

    def update(self):
        pass