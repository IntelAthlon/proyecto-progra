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
            screen.blit(rendered, (
                self.game.nonogram.grid_offset[0] - 10 - rendered.get_width(),
                self.game.nonogram.grid_offset[1] + i * self.game.nonogram.cell_size + self.game.nonogram.cell_size //2 - rendered.get_height() // 2
            ))

        for j, col_clue in enumerate(self.game.nonogram.col_clues):
            text_surfaces = [font.render(str(num), True, BLACK) for num in col_clue]
            total_height = sum(surface.get_height() for surface in text_surfaces)
            current_y = self.game.nonogram.grid_offset[1] - total_height - 10
            for surface in text_surfaces:
                screen.blit(surface, (
                    self.game.nonogram.grid_offset[0] + j * self.game.nonogram.cell_size + self.game.nonogram.cell_size //2 - surface.get_width() //2,
                    current_y
                ))
                current_y += surface.get_height()

    def draw_timer(self, screen):
        font = pygame.font.Font(None, 36)
        timer_text = f"Time: {self.game.timer.get_time():.1f}s"
        rendered = font.render(timer_text, True, BLACK)
        screen.blit(rendered, (750, 50))

    def get_hint(self):
        hint = self.game.get_hint()
        if hint:
            row, col, value = hint
            self.game.nonogram.player_grid[row][col] = value

    def return_to_menu(self):
        self.game.set_screen('menu')

