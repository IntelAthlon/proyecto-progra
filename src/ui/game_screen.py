import os

import pygame
import json
from src.ui.components import Button
from src.config import *
from src.nonogram import Nonogram

class GameScreen:
    def __init__(self, game):
        self.game = game
        self.nonogram = None
        self.buttons = [
            Button("Hint", 650, 100, BUTTON_WIDTH, BUTTON_HEIGHT, self.get_hint),
            Button("Undo", 650, 160, BUTTON_WIDTH, BUTTON_HEIGHT, self.game.undo),
            Button("Redo", 650, 220, BUTTON_WIDTH, BUTTON_HEIGHT, self.game.redo),
            Button("Save", 650, 280, BUTTON_WIDTH, BUTTON_HEIGHT, self.game.save_game),
            Button("Menu", 650, 340, BUTTON_WIDTH, BUTTON_HEIGHT, self.return_to_menu)
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

    def load_level_data(self, level_key):
        file_path = os.path.join("data", "levels", f"{level_key}.json")
        abs_file_path = os.path.abspath(file_path)

        print(f"Attempting to load level file: {abs_file_path}")

        if not os.path.exists(abs_file_path):
            print(f"Error: Level file for {level_key} not found.")
            return None

        try:
            with open(abs_file_path, "r") as f:
                data = json.load(f)
            print(f"Successfully loaded data for {level_key}")
            return data
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in level file for {level_key}.")
            return None
        except Exception as e:
            print(f"Unexpected error loading {level_key}: {str(e)}")
            return None

    def start_level(self, level_key):
        level_data = self.load_level_data(level_key)
        if level_data and all(key in level_data for key in ["grid", "row_clues", "col_clues"]):
            print(f"Inicializando Nonograma del nivel {level_key}")
            print(f"Grilla: {level_data['grid']}")
            print(f"Pistas por fila: {level_data['row_clues']}")
            print(f"Pistas por columna: {level_data['col_clues']}")
            try:
                self.nonogram = Nonogram(
                    level_data["grid"],
                    level_data["row_clues"],
                    level_data["col_clues"]
                )
                self.game.nonogram = self.nonogram
                print(f"Nonograma de nivel {level_key} inicializado con éxito.")
            except Exception as e:
                print(f"Error inicializando Nonograma: {str(e)}")
        else:
            print(f"Error: Información del nivel {level_key} incompleta o inválida.")
            if level_data:
                print(f"Se encontraron las claves: {level_data.keys()}")
            else:
                print("No se cargó información.")

    def handle_event(self, event):
        if self.nonogram is None:
            print("Error: Nonograma no inicializado.")
            print(f"self.nonogram: {self.nonogram}")
            print(f"self.game.nonogram: {self.game.nonogram}")
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            grid_x = (x - self.nonogram.grid_offset[0]) // self.nonogram.cell_size
            grid_y = (y - self.nonogram.grid_offset[1]) // self.nonogram.cell_size
            if 0 <= grid_x < self.nonogram.cols and 0 <= grid_y < self.nonogram.rows:
                self.nonogram.toggle_cell(grid_y, grid_x)

        for button in self.buttons:
            button.handle_event(event)

    def update(self):
        if self.nonogram is not None and self.nonogram.is_solved():
            self.update_player_progress()

    def update_player_progress(self):
        level_key = f"level{self.game.current_level}"
        difficulty = self.get_level_difficulty()
        self.player_progress[difficulty][level_key] = True
        self.save_player_progress()

    def get_level_difficulty(self):
        if self.game.current_level <= 20:
            return "easy"
        elif self.game.current_level <= 40:
            return "medium"
        else:
            return "hard"

    def draw(self, screen):
        screen.fill(WHITE)
        if self.nonogram is not None:
            self.draw_grid(screen)
            self.draw_clues(screen)
            self.draw_timer(screen)
        else:
            font = pygame.font.Font(None, 36)
            message = font.render("No se cargó nivel.", True, (255, 0, 0))
            screen.blit(message, (300, 300))

        for button in self.buttons:
            button.draw(screen)

    def draw_grid(self, screen):
        self.nonogram.draw_grid(screen)

    def draw_clues(self, screen):
        font = pygame.font.Font(None, 24)
        for i, row_clue in enumerate(self.nonogram.row_clues):
            text = " ".join(map(str, row_clue))
            rendered = font.render(text, True, BLACK)
            screen.blit(rendered, (GRID_OFFSET[0] - 80, GRID_OFFSET[1] + i * CELL_SIZE + 5))

        for i, col_clue in enumerate(self.nonogram.col_clues):
            text = "\n".join(map(str, col_clue))
            rendered = font.render(text, True, BLACK)
            screen.blit(rendered, (GRID_OFFSET[0] + i * CELL_SIZE + 5, GRID_OFFSET[1] - 80))

    def draw_timer(self, screen):
        font = pygame.font.Font(None, 36)
        timer_text = f"Time: {self.game.timer.get_time():.1f}s"
        rendered = font.render(timer_text, True, BLACK)
        screen.blit(rendered, (650, 50))

