import pygame

class Nonogram:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

    def draw(self, screen):
        cell_size = 20
        for row in range(self.rows):
            for col in range(self.cols):
                rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)
                if self.grid[row][col] == 1:
                    pygame.draw.rect(screen, (0, 0, 0), rect)