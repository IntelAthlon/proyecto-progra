import pygame

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.grid_size = 10
        self.cell_size = 40
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.selected_cell = None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            row = y // self.cell_size
            col = x // self.cell_size
            if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
                self.selected_cell = (row, col)
                self.grid[row][col] = 1 if self.grid[row][col] == 0 else 0

    def update(self):
        pass

    def draw(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                color = (0, 0, 0) if self.grid[row][col] == 1 else (255, 255, 255)
                pygame.draw.rect(self.screen, color,
                                 (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size))
                pygame.draw.rect(self.screen, (200, 200, 200),
                                 (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size), 1)
