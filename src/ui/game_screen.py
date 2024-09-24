import pygame
from src.ui.components import Button
from src.config import *

class GameScreen:
    def __init__(self, game):
        self.game = game
        self.buttons = [
            Button("Hint", 650, 100, BUTTON_WIDTH, BUTTON_HEIGHT, self.get_hint),
            Button("Undo", 650, 160, BUTTON_WIDTH, BUTTON_HEIGHT, self.game.undo),
            Button("Redo", 650, 220, BUTTON_WIDTH, BUTTON_HEIGHT, self.game.redo),
            Button("Save", 650, 280, BUTTON_WIDTH, BUTTON_HEIGHT, self.game.save_game),
            Button("Menu", 650, 340, BUTTON_WIDTH, BUTTON_HEIGHT, self.return_to_menu)
        ]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            grid_x = (x - GRID_OFFSET[0]) // CELL_SIZE
            grid_y = (y - GRID_OFFSET[1]) // CELL_SIZE
            if 0 <= grid_x < self.game.nonogram.cols and 0 <= grid_y < self.game.nonogram.rows:
                self.game.nonogram.toggle_cell(grid_y, grid_x)

        for button in self.buttons:
            button.handle_event(event)

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(WHITE)
        self.draw_grid(screen)
        self.draw_clues(screen)
        self.draw_timer(screen)
        for button in self.buttons:
            button.draw(screen)

    def draw_grid(self, screen):
        for row in range(self.game.nonogram.rows):
            for col in range(self.game.nonogram.cols):
                x = GRID_OFFSET[0] + col * CELL_SIZE
                y = GRID_OFFSET[1] + row * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, BLACK, rect, 1)
                if self.game.nonogram.player_grid[row][col] == 1:
                    pygame.draw.rect(screen, BLACK, rect)

    def draw_clues(self, screen):
        font = pygame.font.Font(None, 24)
        for i, row_clue in enumerate(self.game.nonogram.row_clues):
            text = " ".join(map(str, row_clue))
            rendered = font.render(text, True, BLACK)
            screen.blit(rendered, (GRID_OFFSET[0] - 80, GRID_OFFSET[1] + i * CELL_SIZE + 5))

        for i, col_clue in enumerate(self.game.nonogram.col_clues):
            text = "\n".join(map(str, col_clue))
            rendered = font.render(text, True, BLACK)
            screen.blit(rendered, (GRID_OFFSET[0] + i * CELL_SIZE + 5, GRID_OFFSET[1] - 80))

    def draw_timer(self, screen):
        font = pygame.font.Font(None, 36)
        timer_text = f"Time: {self.game.timer.get_time():.1f}s"
        rendered = font.render(timer_text, True, BLACK)
        screen.blit(rendered, (650, 50))

    def get_hint(self):
        hint = self.game.get_hint()
        if hint:
            row, col, value = hint
            self.game.nonogram.player_grid[row][col] = value

    def return_to_menu(self):
        self.game.set_screen('menu')