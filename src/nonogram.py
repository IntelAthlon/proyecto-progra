import pygame
import json
import copy

class Nonogram:
    def __init__(self, grid, row_clues, col_clues):
        self.row_clues = row_clues
        self.col_clues = col_clues
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.player_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.cell_size = 30
        self.grid_offset = (100, 100)
        self.font = pygame.font.Font(None, 24)
        self.history = []
        self.redo_stack = []

    @classmethod
    def from_level_data(cls, level_data):
        return cls(level_data['grid'], level_data['row_clues'], level_data['col_clues'])

    def draw(self, screen):
        self.draw_grid(screen)
        self.draw_clues(screen)
        self.draw_cells(screen)

    def draw_grid(self, screen):
        for i in range(self.rows + 1):
            start_pos = (self.grid_offset[0], self.grid_offset[1] + i * self.cell_size)
            end_pos = (self.grid_offset[0] + self.cols * self.cell_size, self.grid_offset[1] + i * self.cell_size)
            pygame.draw.line(screen, (0, 0, 0), start_pos, end_pos, 2)

        for j in range(self.cols + 1):
            start_pos = (self.grid_offset[0] + j * self.cell_size, self.grid_offset[1])
            end_pos = (self.grid_offset[0] + j * self.cell_size, self.grid_offset[1] + self.rows * self.cell_size)
            pygame.draw.line(screen, (0, 0, 0), start_pos, end_pos, 2)

    def draw_clues(self, screen):
        for i, row_clue in enumerate(self.row_clues):
            clue_text = " ".join(str(num) for num in row_clue)
            text_surface = self.font.render(clue_text, True, (0, 0, 0))
            screen.blit(text_surface, (
                self.grid_offset[0] - 10 - text_surface.get_width(),
                self.grid_offset[1] + i * self.cell_size + self.cell_size // 2 - text_surface.get_height() // 2
            ))

        for j, col_clue in enumerate(self.col_clues):
            clue_text = "\n".join(str(num) for num in col_clue)
            text_surfaces = [self.font.render(str(num), True, (0, 0, 0)) for num in col_clue]
            total_height = sum(surface.get_height() for surface in text_surfaces)
            current_y = self.grid_offset[1] - 10 - total_height
            for surface in text_surfaces:
                screen.blit(surface, (
                    self.grid_offset[0] + j * self.cell_size + self.cell_size // 2 - surface.get_width() // 2,
                    current_y
                ))
                current_y += surface.get_height()

    def draw_cells(self, screen):
        for i in range(self.rows):
            for j in range(self.cols):
                cell_rect = pygame.Rect(
                    self.grid_offset[0] + j * self.cell_size,
                    self.grid_offset[1] + i * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                if self.player_grid[i][j] == 1:
                    pygame.draw.rect(screen, (0, 0, 0), cell_rect)
                elif self.player_grid[i][j] == 2:
                    pygame.draw.line(screen, (255, 0, 0), cell_rect.topleft, cell_rect.bottomright, 2)
                    pygame.draw.line(screen, (255, 0, 0), cell_rect.topright, cell_rect.bottomleft, 2)

    def toggle_cell(self, row, col):
        self.history.append((row, col, self.player_grid[row][col]))
        self.player_grid[row][col] = (self.player_grid[row][col] + 1) % 3
        self.redo_stack.clear()

    def undo(self):
        if self.history:
            row, col, previous_state = self.history.pop()
            self.redo_stack.append((row, col, self.player_grid[row][col]))
            self.player_grid[row][col] = previous_state

    def redo(self):
        if self.redo_stack:
            row, col, next_state = self.redo_stack.pop()
            self.history.append((row, col, self.player_grid[row][col]))
            self.player_grid[row][col] = next_state

    def is_solved(self):
        playergrid_copy = copy.deepcopy(self.player_grid)

        for l in range(self.rows):
            for i in range(self.cols):
                if playergrid_copy[l][i] == 2:
                    playergrid_copy[l][i] = 0
        return playergrid_copy == self.grid

    @staticmethod
    def get_row_clue(row):
        clue = []
        count = 0
        for cell in row:
            if cell == 1:
                count += 1
            elif count > 0:
                clue.append(count)
                count = 0
        if count > 0:
            clue.append(count)
        return clue if clue else None
