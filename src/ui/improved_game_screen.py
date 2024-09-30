import pygame
import pygame.gfxdraw

class ImprovedGameScreen:
    def __init__(self, game, nonogram):
        self.game = game
        self.nonogram = nonogram
        self.cell_size = 30
        self.grid_offset = (100, 100)
        self.background = pygame.image.load("assets/images/background.png")
        self.cell_fill = pygame.image.load("assets/images/cell_fill.png")
        self.cell_x = pygame.image.load("assets/images/cell_x.png")
        self.font = pygame.font.Font(None, 24)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        self.draw_grid(screen)
        self.draw_clues(screen)
        self.draw_cells(screen)

    def draw_grid(self, screen):
        for i in range(self.nonogram.rows + 1):
            start_pos = (self.grid_offset[0], self.grid_offset[1] + i * self.cell_size)
            end_pos = (self.grid_offset[0] + self.nonogram.cols * self.cell_size, self.grid_offset[1] + i * self.cell_size)
            pygame.draw.line(screen, (0, 0, 0), start_pos, end_pos, 2)

        for j in range(self.nonogram.cols + 1):
            start_pos = (self.grid_offset[0] + j * self.cell_size, self.grid_offset[1])
            end_pos = (self.grid_offset[0] + j * self.cell_size, self.grid_offset[1] + self.nonogram.rows * self.cell_size)
            pygame.draw.line(screen, (0, 0, 0), start_pos, end_pos, 2)

    def draw_clues(self, screen):
        for i, row_clue in enumerate(self.nonogram.row_clues):
            clue_text = " ".join(str(num) for num in row_clue)
            text_surface = self.font.render(clue_text, True, (0, 0, 0))
            screen.blit(text_surface, (self.grid_offset[0] - 10 - text_surface.get_width(), self.grid_offset[1] + i * self.cell_size + self.cell_size // 2))

        for j, col_clue in enumerate(self.nonogram.col_clues):
            clue_text = "\n".join(str(num) for num in col_clue)
            text_surface = self.font.render(clue_text, True, (0, 0, 0))
            screen.blit(text_surface, (self.grid_offset[0] + j * self.cell_size + self.cell_size // 2, self.grid_offset[1] - 10 - text_surface.get_height()))

    def draw_cells(self, screen):
        for i in range(self.nonogram.rows):
            for j in range(self.nonogram.cols):
                cell_rect = pygame.Rect(
                    self.grid_offset[0] + j * self.cell_size,
                    self.grid_offset[1] + i * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                if self.nonogram.grid[i][j] == 1:
                    screen.blit(self.cell_fill, cell_rect)
                elif self.nonogram.grid[i][j] == 2:
                    screen.blit(self.cell_x, cell_rect)