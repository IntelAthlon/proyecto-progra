import json
import os
import random

import pygame

from src.config import *
from src.logic.generator import generate_nonogram
from src.nonogram import Nonogram
from src.ui_p import UI
from src.utils.timer import Timer


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.nonogram = None
        self.timer = Timer()
        self.current_level = 0
        self.levels = self.generate_levels(50)
        self.current_screen = 'menu'
        self.ui_p = UI(self)

    def set_screen(self, screen_name):
        self.current_screen = screen_name
        if screen_name == 'game':
            self.timer.start()
        else:
            self.timer.stop()

    def generate_levels(self, num_levels):
        levels = []
        for _ in range(num_levels):
            difficulty = random.randint(DIFFICULTY_EASY, DIFFICULTY_HARD)
            size = random.randint(5, 15)  # Adjust size range as needed
            grid = generate_nonogram(size, size, difficulty)
            levels.append(grid)
        return levels

    def start_new_game(self, level=None):
        if level is None:
            level = self.current_level
        if 0 <= level < len(self.levels):
            grid = self.levels[level]
            self.nonogram = Nonogram(grid)
            self.current_level = level
            self.timer.reset()
            self.timer.start()
            self.set_screen('game')

    def start_editor(self):
        self.editor_grid = [[0 for _ in range(DEFAULT_GRID_SIZE)] for _ in range(DEFAULT_GRID_SIZE)]
        self.set_screen('editor')

    def save_custom_nonogram(self, grid):
        if not os.path.exists(CUSTOM_NONOGRAMS_PATH):
            os.makedirs(CUSTOM_NONOGRAMS_PATH)
        filename = f"custom_nonogram_{len(os.listdir(CUSTOM_NONOGRAMS_PATH))}.json"
        with open(os.path.join(CUSTOM_NONOGRAMS_PATH, filename), 'w') as f:
            json.dump(grid, f)

    def load_custom_nonogram(self, filename):
        with open(os.path.join(CUSTOM_NONOGRAMS_PATH, filename), 'r') as f:
            grid = json.load(f)
        self.nonogram = Nonogram(grid)
        self.set_screen('game')

    def save_game(self):
        if not os.path.exists(SAVE_GAME_PATH):
            os.makedirs(SAVE_GAME_PATH)
        save_data = {
            'current_level': self.current_level,
            'player_grid': self.nonogram.player_grid,
            'time': self.timer.get_time()
        }
        with open(os.path.join(SAVE_GAME_PATH, 'saved_game.json'), 'w') as f:
            json.dump(save_data, f)

    def load_game(self):
        try:
            with open(os.path.join(SAVE_GAME_PATH, 'saved_game.json'), 'r') as f:
                save_data = json.load(f)
            self.current_level = save_data['current_level']
            self.start_new_game(self.current_level)
            self.nonogram.player_grid = save_data['player_grid']
            self.timer.total_time = save_data['time']
            self.set_screen('game')
        except FileNotFoundError:
            print("No saved game found.")

    def get_hint(self):
        return self.nonogram.get_hint() if self.nonogram else None

    def undo(self):
        if self.nonogram:
            self.nonogram.undo()

    def redo(self):
        if self.nonogram:
            self.nonogram.redo()

    def update(self):
        if self.current_screen == 'game' and self.nonogram.is_solved():
            self.timer.stop()
            print(f"Level {self.current_level} completed in {self.timer.get_time():.2f} seconds!")
            self.current_level += 1
            if self.current_level < len(self.levels):
                self.start_new_game()
            else:
                print("Congratulations! You've completed all levels!")
                self.set_screen('menu')

    def draw(self):
        self.screen.fill(WHITE)
        if self.current_screen == 'game':
            # Draw game screen
            pass
        elif self.current_screen == 'menu':
            # Draw menu screen
            pass
        elif self.current_screen == 'editor':
            # Draw editor screen
            pass
        pygame.display.flip()

    def run(self):
        while True:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                self.ui_p.handle_event(event)
            self.update()
            self.ui_p.update()
            self.ui_p.draw()
            pygame.display.flip()

    def handle_event(self, event):
        if self.current_screen == 'game':
            # Handle game screen events
            pass
        elif self.current_screen == 'menu':
            # Handle menu screen events
            pass
        elif self.current_screen == 'editor':
            # Handle editor screen events
            pass