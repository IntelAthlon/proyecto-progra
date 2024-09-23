import pygame
from ui import UI
from utils import save_game, load_game
from image_to_nonogram import image_to_nonogram
from levels import generate_levels

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.ui = UI(screen)
        self.running = True
        self.start_time = pygame.time.get_ticks()
        self.levels = generate_levels()
        self.current_level = 0

    def handle_event(self, event):
        self.ui.handle_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save_game(self.ui.grid)
            elif event.key == pygame.K_l:
                self.ui.grid = load_game()
            elif event.key == pygame.K_n:
                self.ui.grid = self.levels[self.current_level]
                self.current_level = (self.current_level + 1) % len(self.levels)
        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:  # ejemplo de botón.
                save_game(self.ui.grid)
            elif event.button == 1:
                self.ui.grid = load_game()

    def update(self):
        self.ui.update()

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.ui.draw()
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        font = pygame.font.Font(None, 36)
        time_text = font.render(f"Time: {elapsed_time}s", True, (0, 0, 0))
        self.screen.blit(time_text, (10, 10))
