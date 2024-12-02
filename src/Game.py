import pygame
import json
import os

from src.logic.ProgressTracker import ProgressTracker
from src.config import *
from src.Nonogram import Nonogram
from src.utils.image_converter import image_to_nonogram
from src.utils.timer import Timer
from src.logic.GamepadHandler import GamepadHandler
from src.logic.SoundManager import SoundManager
from src.ui.GameScreen import GameScreen
from src.ui.LevelSelectScreen import LevelSelectScreen


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.timer = Timer()
        self.current_level = None
        self.current_screen = 'menu'
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
        self.victory_music_played = False

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

    def def_nono(self, level_key, custom):
        if custom is not None:
            a = image_to_nonogram(custom)
            self.nonogram = Nonogram(a[0], a[1], a[2])
            self.current_level = "custom"
        else:
            level_data = self.load_level_data(level_key)
            if level_data and all(key in level_data for key in ["grid", "row_clues", "col_clues"]):
                print(f"Inicializando Nonograma del nivel {level_key}")
                print(f"Pistas por fila: {level_data['row_clues']}")
                print(f"Pistas por columna: {level_data['col_clues']}")
                try:
                    self.nonogram = Nonogram(level_data['grid'],level_data['row_clues'],level_data['col_clues'])
                    print(f"Nonograma de nivel {level_key} inicializado con éxito.")
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
            self.sound_manager.stop_music()

    def start_new_game(self):
        self.set_screen("level_select")

    def start_level(self, level_key, custom=None):
        print(f"Game: Starting level {level_key}")
        self.def_nono(level_key, custom)
        self.set_screen('game')
        self.victory_music_played = False
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
        level_key = f"level{self.current_level}"
        filename=f"data/saved_games/{level_key}.json"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        save_data = {
            "player_grid": self.nonogram.player_grid,
            "timer": self.timer.get_time()
        }
        with open(filename, 'w') as f:
            json.dump(save_data, f, indent=2)

    def load_game(self):
        level_key = f"level{self.current_level}"
        filename = f"data/saved_games/{level_key}.json"
        try:
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    save_data = json.load(f)
                    self.nonogram.player_grid = save_data["player_grid"]
                    self.timer.set_time(save_data.get("timer", 0))
                    self.draw()
                    self.update()
            else:
                self.show_message("No hay juego guardado para este nivel.")
        except FileNotFoundError:
            self.show_message("No hay juego guardado para este nivel.")

    def show_message(self, message):
        font_path = os.path.join("assets", "fonts", "newsweekly", "newsweekly-Regular.ttf")
        font = pygame.font.Font(font_path, 36)
        dark_color = (63, 48, 43)
        light_color = (251, 226, 204)
        text_surface = font.render(message, True, dark_color)
        text_rect = text_surface.get_rect(center=self.screen.get_rect().center)
        border_width = 3

        background_surface = pygame.Surface((text_rect.width + 15, text_rect.height + 40))
        background_rect = background_surface.get_rect(center=self.screen.get_rect().center)

        pygame.draw.rect(self.screen, dark_color, background_rect.inflate(border_width * 2, border_width * 2), border_radius=10)
        pygame.draw.rect(self.screen, light_color, background_rect, border_radius=7)

        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()
        pygame.time.wait(1500)


    def update(self):
        if self.current_screen == 'game':
            self.game_screen.update()
            if self.nonogram and self.nonogram.is_solved():
                if not self.victory_music_played:
                    self.sound_manager.play_sound("complete")
                    self.victory_music_played = True
                self.timer.stop()
                self.progress_tracker.mark_level_complete(2, self.current_level)
        elif self.current_screen == 'level_select':
            self.level_select_screen.update()

    def handle_event(self, event):
        if self.current_screen == 'game':
            self.game_screen.handle_event(event)
        elif self.current_screen == 'level_select':
            self.level_select_screen.handle_event(event)

    def draw(self):
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