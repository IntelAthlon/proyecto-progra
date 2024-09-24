import pygame
import json
from pygame.draw import rect
from utils.file_handler import save_game
from utils.file_handler import load_games
from logic.generator import generate_nonogram
from logic.solver import solve_nonogram
from logic.hint_system import get_hint

class Nonogram:
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.player_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.row_clues = self.generate_row_clues()
        self.col_clues = self.generate_col_clues()
        self.history = []
        self.redo_stack = []

    def generate_row_clues(self):
        return [self.generate_clue(row) for row in self.grid]

    def generate_col_clues(self):
        return [self.generate_clue([self.grid[r][c] for r in range(self.rows)]) for c in range(self.cols)]

    def generate_clue(self, line):
        clue = []
        count = 0
        for cell in line:
            if cell == 1:
                count += 1
            elif count > 0:
                clue.append(count)
                count = 0
        if count > 0:
            clue.append(count)
        return clue if clue else [0]

    def toggle_cell(self, row, col):
        self.history.append((row, col, self.player_grid[row][col]))
        self.redo_stack.clear()
        self.player_grid[row][col] = 1 if self.player_grid[row][col] == 0 else 0

    def undo(self):
        if self.history:
            row, col, value = self.history.pop()
            self.redo_stack.append((row, col, self.player_grid[row][col]))
            self.player_grid[row][col] = value

    def redo(self):
        if self.redo_stack:
            row, col, value = self.redo_stack.pop()
            self.history.append((row, col, self.player_grid[row][col]))
            self.player_grid[row][col] = value

    def is_solved(self):
        return self.player_grid == self.grid

    def get_hint(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.player_grid[row][col] != self.grid[row][col]:
                    return row, col, self.grid[row][col]
        return None