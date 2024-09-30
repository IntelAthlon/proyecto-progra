from tkinter import filedialog

import pygame


from src.config import *



class UI:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.load_fonts()
        self.grid_size = DEFAULT_GRID_SIZE
        self.cell_size = CELL_SIZE
        self.grid_offset = GRID_OFFSET
        self.selected_cell = None
        self.buttons = self.create_buttons()
        self.grid = []
        self.row_clues = []
        self.col_clues = []



    def set_grid(self, grid, row_clues, col_clues):
        self.grid = grid
        self.row_clues = row_clues
        self.col_clues = col_clues
        self.grid_size = len(grid)

    def load_fonts(self):
        pygame.font.init()
        try:
            self.font = pygame.font.Font("assets/fonts/Roboto-Regular.ttf", 24)
            self.title_font = pygame.font.Font("assets/fonts/Roboto-Bold.ttf", 48)
        except FileNotFoundError:
            print("Custom font not found. Using default font.")
            self.font = pygame.font.Font(None, 24)
            self.title_font = pygame.font.Font(None, 48)

    def create_buttons(self):
        return [
            {"text": "Hint", "rect": pygame.Rect(650, 100, BUTTON_WIDTH, BUTTON_HEIGHT), "action": self.game.get_hint},
            {"text": "Undo", "rect": pygame.Rect(650, 160, BUTTON_WIDTH, BUTTON_HEIGHT), "action": self.game.undo},
            {"text": "Redo", "rect": pygame.Rect(650, 220, BUTTON_WIDTH, BUTTON_HEIGHT), "action": self.game.redo},
            {"text": "Save", "rect": pygame.Rect(650, 280, BUTTON_WIDTH, BUTTON_HEIGHT), "action": self.game.save_game},
            {"text": "Menu", "rect": pygame.Rect(650, 340, BUTTON_WIDTH, BUTTON_HEIGHT), "action": self.return_to_menu}
        ]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            grid_x = (x - self.grid_offset[0]) // self.cell_size
            grid_y = (y - self.grid_offset[1]) // self.cell_size
            if 0 <= grid_x < self.grid_size and 0 <= grid_y < self.grid_size:
                self.selected_cell = (grid_y, grid_x)
                self.game.nonogram.toggle_cell(grid_y, grid_x)

            for button in self.buttons:
                if button["rect"].collidepoint(event.pos):
                    button["action"]()

    def update(self):
        self.grid_size = self.game.nonogram.rows  # Assuming square grid

    def draw(self):
        self.screen.fill(WHITE)
        self.draw_grid()
        self.draw_clues()
        self.draw_buttons()
        self.draw_timer()
        self.draw_level()

    def draw_grid(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x = self.grid_offset[0] + col * self.cell_size
                y = self.grid_offset[1] + row * self.cell_size
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)

                if self.game.nonogram.player_grid[row][col] == 1:
                    pygame.draw.rect(self.screen, BLACK, rect)
                else:
                    pygame.draw.rect(self.screen, WHITE, rect)

                pygame.draw.rect(self.screen, GRAY, rect, 1)

                if (row, col) == self.selected_cell:
                    pygame.draw.rect(self.screen, BLUE, rect, 3)

    def draw_clues(self):
        for i, row_clue in enumerate(self.game.nonogram.row_clues):
            text = " ".join(map(str, row_clue))
            rendered = self.font.render(text, True, BLACK)
            self.screen.blit(rendered, (self.grid_offset[0] - 80, self.grid_offset[1] + i * self.cell_size + 5))

        for i, col_clue in enumerate(self.game.nonogram.col_clues):
            text = "\n".join(map(str, col_clue))
            rendered = self.font.render(text, True, BLACK)
            self.screen.blit(rendered, (self.grid_offset[0] + i * self.cell_size + 5, self.grid_offset[1] - 80))

    def draw_buttons(self):
        for button in self.buttons:
            pygame.draw.rect(self.screen, BLUE, button["rect"], border_radius=5)
            text = self.font.render(button["text"], True, WHITE)
            text_rect = text.get_rect(center=button["rect"].center)
            self.screen.blit(text, text_rect)

    def draw_timer(self):
        timer_text = f"Time: {self.game.timer.get_time():.1f}s"
        rendered = self.font.render(timer_text, True, BLACK)
        self.screen.blit(rendered, (650, 50))

    def draw_level(self):
        level_text = f"Level: {self.game.current_level + 1}"
        rendered = self.font.render(level_text, True, BLACK)
        self.screen.blit(rendered, (650, 10))

    def return_to_menu(self):
        self.game.set_screen('menu')

class UIManager:
    CLUE_SIZE = 20
    CELL_SIZE = 30
    def __init__(self):
        self.grid = None
        self.row_clues = None
        self.col_clues = None


    def set_grid(self, grid, row_clues, col_clues):
        self.grid = grid
        self.row_clues = row_clues
        self.col_clues = col_clues
        self.draw_nonogram()

    def draw_grid(self):
        pass

    #def set_grid(self, grid, row_clues, col_clues):
     #   self.grid = grid
      #  self.row_clues = row_clues
       # self.col_clues = col_clues
        #self.draw_grid()

    def draw_nonogram(self):

        if self.grid is None or self.row_clues is None or self.col_clues is None:
            return

        screen = self.game.screen
        screen.fill((255, 255, 255))


        rows = len(self.grid)
        cols = len(self.grid[0])


        for row_idx, clues in enumerate(self.row_clues):
            clues_str = " ".join(map(str, clues))
            text_surface = self.game.font.render(clues_str, True, (0, 0, 0))
            screen.blit(text_surface, (self.CLUE_SIZE - 10, self.CLUE_SIZE + row_idx * self.CELL_SIZE))


        for col_idx, clues in enumerate(self.col_clues):
            clues_str = " ".join(map(str, clues))
            text_surface = self.game.font.render(clues_str, True, (0, 0, 0))

            rotated_surface = pygame.transform.rotate(text_surface, 90)
            screen.blit(rotated_surface, (self.CLUE_SIZE + col_idx * self.CELL_SIZE, 0))


        for row in range(rows):
            for col in range(cols):

                if self.grid[row][col] == 1:
                    color = (0, 0, 0)
                else:
                    color = (255, 255, 255)


                cell_x = self.CLUE_SIZE + col * self.CELL_SIZE
                cell_y = self.CLUE_SIZE + row * self.CELL_SIZE


                pygame.draw.rect(screen, color, (cell_x, cell_y, self.CELL_SIZE, self.CELL_SIZE))


                pygame.draw.rect(screen, (0, 0, 0), (cell_x, cell_y, self.CELL_SIZE, self.CELL_SIZE), 1)

        pygame.display.flip()
