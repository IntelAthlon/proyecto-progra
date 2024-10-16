import pygame
from src.ui.components import Button
from src.config import *

class LevelSelectScreen:
    def __init__(self, game):
        self.game = game
        self.buttons = []
        self.create_level_buttons()

    def create_level_buttons(self):
        for i, level_key in enumerate(self.game.levels.keys()):
            row = i // 10
            col = i % 10
            x = 100 + col * 60
            y = 100 + row * 60
            self.buttons.append(Button(level_key, x, y, 50, 50, lambda lk=level_key: self.select_level(lk), self.game.sound_manager))

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.set_screen('menu')

    def draw(self, screen):
        screen.fill(WHITE)
        font = pygame.font.Font(None, 48)
        title = font.render("Select Level", True, BLACK)
        screen.blit(title, (300, 30))

        for button in self.buttons:
            button.draw(screen)

    def select_level(self, level_key):
        print(f"Cargando el nivel {level_key}")
        self.game.start_level(level_key)

    def update(self):
        pass