import itertools
import pygame
import json
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
        self.current_level = 0
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
        #with open("data/levels/nonogram_levels.json", "r") as f:
        with open("C:/Users/carlo/Desktop\proyecto progra\proyecto-progra\src\levels/nonogram_levels.json", "r") as f:
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
        self.game_screen.start_level(level_key)
        self.set_screen('game')
        print(f"Game: Current screen set to 'game'")
        print(f"Game: self.nonogram = {self.nonogram}")


    def get_hint(self):
        return self.nonogram.get_hint() if self.nonogram else None

    def undo(self):
        if self.nonogram:
            self.nonogram.undo()

    def redo(self):
        if self.nonogram:
            self.nonogram.redo()

    def save_game(self):
        # Implement save game logic here
        pass

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