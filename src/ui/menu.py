import pygame
from src.ui.components import Button

class Menu:
    def __init__(self, game):
        self.game = game
        self.buttons = [
            Button("New Game", 300, 200, 200, 50, self.start_new_game),
            Button("Load Game", 300, 260, 200, 50, self.load_game),
            Button("Editor", 300, 320, 200, 50, self.start_editor),
            Button("Quit", 300, 380, 200, 50, self.quit_game)
        ]

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((255, 255, 255))
        font = pygame.font.Font(None, 48)
        title = font.render("AtomicGram", True, (0, 0, 0))
        screen.blit(title, (300, 100))

        for button in self.buttons:
            button.draw(screen)

    def start_new_game(self):
        self.game.start_new_game(10)  # Start with a 10x10 grid

    def load_game(self):
        self.game.load_game()

    def start_editor(self):
        self.game.start_editor()

    def quit_game(self):
        pygame.quit()
        quit()