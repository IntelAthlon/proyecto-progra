import pygame
from pygame import Rect
from src.ui.components import Button

class EditorScreen:
    def __init__(self, game):
        self.game = game
        self.grid_size = (10, 10)
        self.cell_size = 30
        self.grid_offset = (100, 100)
        self.grid = [[0 for _ in range(self.grid_size[1])] for _ in range(self.grid_size[0])]
        self.buttons = [
            Button("Guardar", 650, 100, 100, 50, self.save_nonogram),
            Button("Limpiar", 650, 160, 100, 50, self.clear_grid),
            Button("Menú", 650, 220, 100, 50, self.return_to_menu)
        ]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            grid_x = (x - self.grid_offset[0]) // self.cell_size
            grid_y = (y - self.grid_offset[1]) // self.cell_size
            if 0 <= grid_x < self.grid_size[1] and 0 <= grid_y < self.grid_size[0]:
                self.grid[grid_y][grid_x] = 1 if self.grid[grid_y][grid_x] == 0 else 0

        for button in self.buttons:
            button.handle_event(event)

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((255, 255, 255))
        self.draw_grid(screen)
        for button in self.buttons:
            button.draw(screen)

    def draw_grid(self, screen):
        for row in range(self.grid_size[0]):
            for col in range(self.grid_size[1]):
                x = self.grid_offset[0] + col * self.cell_size
                y = self.grid_offset[1] + row * self.cell_size
                rect = Rect(x, y, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)
                if self.grid[row][col] == 1:
                    pygame.draw.rect(screen, (0, 0, 0), rect)

    def save_nonogram(self):
        self.game.save_custom_nonogram(self.grid)

    def clear_grid(self):
        self.grid = [[0 for _ in range(self.grid_size[1])] for _ in range(self.grid_size[0])]

    def return_to_menu(self):
        self.game.set_screen('menu')