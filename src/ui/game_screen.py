import os

import pygame
import json
from src.ui.components import Button
from src.config import *
from src.nonogram import Nonogram

class GameScreen:
    def __init__(self, game):
        self.game = game

        self.buttons = [
            Button("Hint", 750, 100, BUTTON_WIDTH, BUTTON_HEIGHT, self.get_hint),
            Button("Undo", 750, 160, BUTTON_WIDTH, BUTTON_HEIGHT, self.game.undo),
            Button("Redo", 750, 220, BUTTON_WIDTH, BUTTON_HEIGHT, self.game.redo),
            Button("Save", 750, 280, BUTTON_WIDTH, BUTTON_HEIGHT, self.game.save_game),
            Button("Load", 750, 340, BUTTON_WIDTH, BUTTON_HEIGHT, self.game.load_game),
            Button("Menu", 750, 400, BUTTON_WIDTH, BUTTON_HEIGHT, self.return_to_menu)
        ]
        self.load_player_progress()

    def load_player_progress(self):
        try:
            with open("data/player_progress.json", "r") as f:
                self.player_progress = json.load(f)
        except FileNotFoundError:
            self.player_progress = {
                "easy": {},
                "medium": {},
                "hard": {}
            }

    def save_player_progress(self):
        with open("data/player_progress.json", "w") as f:
            json.dump(self.player_progress, f, indent=2)

    def handle_event(self, event):

        if self.game.nonogram is None:
            print("Error: Nonograma no inicializado.")
            print(f"self.game.nonogram: {self.game.nonogram}")
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            grid_x = (x - self.game.nonogram.grid_offset[0]) // self.game.nonogram.cell_size
            grid_y = (y - self.game.nonogram.grid_offset[1]) // self.game.nonogram.cell_size
            if 0 <= grid_x < self.game.nonogram.cols and 0 <= grid_y < self.game.nonogram.rows:
                self.game.nonogram.toggle_cell(grid_y, grid_x)
            self.game.draw()
            self.game.update()

        for button in self.buttons:
            button.handle_event(event)

    def update(self):
        if self.game.nonogram is not None and self.game.nonogram.is_solved():
            self.update_player_progress()


    def update_player_progress(self):
        level_key = f"level{self.game.current_level}"
        difficulty = self.get_level_difficulty()
        self.player_progress[difficulty][level_key] = True
        self.save_player_progress()

    def get_level_difficulty(self):
        if 1 <= 20: #self.game.current_level
            return "easy"
        elif 1 <= 40: #self.game.current_level
            return "medium"
        else:
            return "hard"

    def draw(self, screen):
        screen.fill(WHITE)
        if self.game.nonogram is not None:
            self.game.nonogram.draw_grid(screen)
            self.game.nonogram.draw_cells(screen)
            self.draw_clues(screen)
            self.draw_timer(screen)
        else:
            font = pygame.font.Font(None, 36)
            message = font.render("No se cargó nivel.", True, (255, 0, 0))
            screen.blit(message, (300, 300))

        for button in self.buttons:
            button.draw(screen)

    def draw_clues(self, screen):
        font = pygame.font.Font(None, 24)
        for i, row_clue in enumerate(self.game.nonogram.row_clues):
            text = " ".join(map(str, row_clue))
            rendered = font.render(text, True, BLACK)
            screen.blit(rendered, (GRID_OFFSET[0] - 80, GRID_OFFSET[1] + i * CELL_SIZE + 5))

        for i, col_clue in enumerate(self.game.nonogram.col_clues):
            offset_col = 0
            for j in col_clue:
                text = str(j)
                rendered = font.render(text, True, BLACK)
                screen.blit(rendered, (GRID_OFFSET[0] + i * CELL_SIZE + 5, GRID_OFFSET[1] - 80 + offset_col))
                offset_col += CELL_SIZE / 2

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

