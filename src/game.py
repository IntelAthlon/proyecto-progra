import itertools
import pygame
import json
import os
from src.ui_p import UIManager
from src.logic.progress import ProgressTracker
from src.config import *
from src.logic.generator import generate_nonogram
from src.logic.solver import solve_nonogram
from src.nonogram import Nonogram
from src.utils.timer import Timer
from src.logic.gamepad_handler import GamepadHandler
from src.logic.sound import SoundManager
from src.ui.game_screen import GameScreen
from src.ui.level_select_screen import LevelSelectScreen



class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.timer = Timer()
        self.current_level = None
        self.current_screen = 'menu'
        self.ui_manager = UIManager()
        self.progress_tracker = ProgressTracker()
        self.gamepad_handler = GamepadHandler()
        self.sound_manager = SoundManager()
        self.levels = self.load_levels()
        self.game_screen = None
        self.level_select_screen = None
        self.initialize_screens()
        try:
            _ = self.nonogram
        except AttributeError:
            self.nonogram = None

    def load_levels(self):
        levels_path = os.path.join("data/levels/nonogram_levels.json")
        with open(levels_path, "r") as f:
            return json.load(f)

    def initialize_screens(self):
        self.game_screen = GameScreen(self)
        self.level_select_screen = LevelSelectScreen(self)

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

    def def_nono(self, level_key):
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
                print(f"Nonograma de nivel {level_key} inicializado con éxito.")
                print(self.nonogram)
                self.current_level = level_key
            except Exception as e:
                print(f"Error inicializando Nonograma: {str(e)}")
        else:
            print(f"Error: Información del nivel {level_key} incompleta o inválida.")
            if level_data:
                print(f"Se encontraron las claves: {level_data.keys()}")
            else:
                print("No se cargó información.")


    def set_screen(self, screen_name):
        self.current_screen = screen_name
        if screen_name == 'game':
            self.timer.start()
        else:
            self.timer.stop()

    def start_new_game(self):
        self.set_screen("level_select")

    def start_level(self, level_key):
        print(f"Game: Starting level {level_key}")
        #level_data = self.levels.get(level_key)
        self.def_nono(level_key)
        self.set_screen('game')
        print(f"Game: Current screen set to 'game'")

    def get_hint(self):
        return self.nonogram.get_hint() if self.nonogram else None

    def undo(self):
        if self.nonogram:
            self.nonogram.undo()

    def redo(self):
        if self.nonogram:
            self.nonogram.redo()

    def save_game(self):
        filename="data/saved_games/" + str(self.current_level) + ".json"
        with open(filename, 'w') as f:
            json.dump(self.nonogram.player_grid, f)

    def load_game(self):
        filename = "data/saved_games/" + str(self.current_level) + ".json"
        with open(filename, 'r') as f:
            self.nonogram.player_grid = json.load(f)
            self.draw()
            self.update()

    def update(self):
        if self.current_screen == 'game':
            self.game_screen.update()
            if self.nonogram and self.nonogram.is_solved():
                self.sound_manager.play_sound("complete")
                self.timer.stop()
                self.progress_tracker.mark_level_complete(2,self.current_level)
        elif self.current_screen == 'level_select':
            self.level_select_screen.update()

    def handle_event(self, event):
        if self.current_screen == 'game':
            self.game_screen.handle_event(event)
        elif self.current_screen == 'level_select':
            self.level_select_screen.handle_event(event)

    def draw(self):
        self.screen.fill(WHITE)
        if self.current_screen == 'game':
            self.game_screen.draw(self.screen)
        elif self.current_screen == 'level_select':
            self.level_select_screen.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while True:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                self.handle_event(event)
            self.update()
            self.draw()

    def solve(self):
        if self.nonogram:
            solve_nonogram(self.nonogram)