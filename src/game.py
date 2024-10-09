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
        self.current_level = "level1"
        self.current_screen = 'menu'
        self.ui_manager = UIManager()
        self.progress_tracker = ProgressTracker()
        self.gamepad_handler = GamepadHandler()
        self.sound_manager = SoundManager()
        self.levels = self.load_levels()
        self.nonogram = None
        self.game_screen = None
        self.level_select_screen = None
        self.initialize_screens()
        self.current_level_key = None

    def load_levels(self):
        levels_path = os.path.join("levels/nonogram_levels.json")
        with open(levels_path, "r") as f:
            return json.load(f)

    def initialize_screens(self):
        self.game_screen = GameScreen(self)
        self.level_select_screen = LevelSelectScreen(self)

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
        level_data = self.game_screen.load_level_data(level_key)
        if level_data:
            self.nonogram = Nonogram.from_level_data(level_data)
            self.game_screen.nonogram = self.nonogram
            self.set_screen('game')
            print(f"Game: Current screen set to 'game'")
            print(f"Game: self.nonogram = {self.nonogram}")
        else:
            print(f"Error: Level data not found for {level_key}")

    def get_hint(self):
        return self.nonogram.get_hint() if self.nonogram else None

    def undo(self):
        if self.nonogram:
            self.nonogram.undo()

    def redo(self):
        if self.nonogram:
            self.nonogram.redo()
    n=0
    def save_game(grid, filename="data/saved_games/save" + str(n) + ".json"):
        with open(filename, 'w') as f:
            json.dump(grid, f)

    def update(self):
        if self.current_screen == 'game':
            self.game_screen.update()
            if self.nonogram and self.nonogram.is_solved():
                self.sound_manager.play_sound("complete")
                self.progress_tracker.mark_level_complete(self.current_level)
                self.set_screen('level_select')
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

    def load_game(filename="data/saved_games/save1.json"):
        with open(filename, 'r') as f:
            return json.load(f)