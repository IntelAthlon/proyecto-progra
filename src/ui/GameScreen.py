import pygame
import json
from src.ui.Button import Button
from src.config import *

class GameScreen:
    """
    Clase que representa la pantalla del juego donde se juega el Nonogram.

    Atributos:
        game (Game): Instancia del juego.
        mouse_button (int): Botón del ratón presionado.
        last_cell (tuple): Última celda interactuada.
        joystick_connected (bool): Indica si hay un joystick conectado.
        buttons (list): Lista de botones en la pantalla del juego.
        player_progress (dict): Progreso del jugador.
    """
    def __init__(self, game):
        """
        Inicializa una instancia de la clase GameScreen.

        Args:
            game (Game): Instancia del juego.
        """
        self.game = game
        self.mouse_button = None
        self.last_cell = None
        self.joystick_connected = False
        if pygame.joystick.get_count() > 0 and self.game.joystick is not None:
            self.joystick = self.game.joystick
            self.joystick_connected = True
        screen_width, screen_height = pygame.display.get_surface().get_size()
        button_width, button_height = 100, 50
        padding = 20
        start_x = screen_width - button_width - padding - 20
        start_y = (screen_height - (6 * button_height + 5 * padding)) // 2

        self.buttons = [
            Button("Hint", start_x, start_y, BUTTON_WIDTH, BUTTON_HEIGHT, self.get_hint, self.game.sound_manager,
                   self.game.joystick),
            Button("Undo", start_x, start_y + (button_height + padding), BUTTON_WIDTH, BUTTON_HEIGHT, self.game.undo,
                   self.game.sound_manager, self.game.joystick),
            Button("Redo", start_x, start_y + 2 * (button_height + padding), BUTTON_WIDTH, BUTTON_HEIGHT,
                   self.game.redo, self.game.sound_manager, self.game.joystick),
            Button("Save", start_x, start_y + 3 * (button_height + padding), BUTTON_WIDTH, BUTTON_HEIGHT,
                   self.game.save_game, self.game.sound_manager, self.game.joystick),
            Button("Load", start_x, start_y + 4 * (button_height + padding), BUTTON_WIDTH, BUTTON_HEIGHT,
                   self.game.load_game, self.game.sound_manager, self.game.joystick),
            Button("Menu", start_x, start_y + 5 * (button_height + padding), BUTTON_WIDTH, BUTTON_HEIGHT,
                   self.return_to_menu, self.game.sound_manager, self.game.joystick)
        ]
        self.load_player_progress()

    def load_player_progress(self):
        """
        Carga el progreso del jugador desde un archivo JSON.
        """
        try:
            with open("data/player_progress.json", "r") as f:
                self.player_progress = json.load(f)
        except FileNotFoundError:
            self.player_progress = {
                "easy": {},
                "medium": {},
                "hard": {}
            }

    def save_player_progress(self):
        """
        Guarda el progreso del jugador en un archivo JSON.
        """
        with open("data/player_progress.json", "w") as f:
            json.dump(self.player_progress, f, indent=2)

    def handle_event(self, event):
        """
        Maneja los eventos de la pantalla del juego.

        Args:
            event (pygame.event.Event): Evento a manejar.
        """
        if self.game.nonogram is None:
            print("Error: Nonograma no inicializado.")
            print(f"self.game.nonogram: {self.game.nonogram}")
            return
        if self.joystick_connected and event.type == pygame.JOYBUTTONDOWN:
            self.joystick = event.button
            mouse_pos = pygame.mouse.get_pos()
            self.update_cell(mouse_pos, event.button)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_button = event.button
            self.update_cell(event.pos, event.button)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_button = None
            self.last_cell = None
        elif event.type == pygame.MOUSEMOTION and self.mouse_button:
            self.update_cell(event.pos, self.mouse_button)

        for button in self.buttons:
            button.handle_event(event)

    def update_cell(self, pos, button):
        """
        Actualiza el estado de una celda en la cuadrícula del Nonogram.

        Args:
            pos (tuple): Posición del ratón.
            button (int): Botón del ratón presionado.
        """
        x, y = pos
        grid_x = (x - self.game.nonogram.grid_offset[0]) // self.game.nonogram.cell_size
        grid_y = (y - self.game.nonogram.grid_offset[1]) // self.game.nonogram.cell_size
        if 0 <= grid_x < self.game.nonogram.cols and 0 <= grid_y < self.game.nonogram.rows:
            current_cell = (grid_x, grid_y)
            if current_cell != self.last_cell:
                if button == 1: #Click Izquierdo
                    self.game.nonogram.set_cell(grid_y, grid_x, 1)
                elif button == 3: #Click Derecho
                    self.game.nonogram.set_cell(grid_y, grid_x, 2)
                self.last_cell = current_cell
        self.game.draw()
        self.game.update()

    def update(self):
        """
        Actualiza el estado de la pantalla del juego.
        """
        if self.game.nonogram is not None and self.game.nonogram.is_solved():
            self.update_player_progress()


    def update_player_progress(self):
        """
        Actualiza el progreso del jugador.
        """
        level_key = self.game.current_level
        if level_key == "custom":
            return
        difficulty = self.get_level_difficulty()
        self.player_progress[difficulty][level_key] = True
        self.save_player_progress()

    def get_level_difficulty(self):
        """
        Obtiene la dificultad del nivel actual.

        Returns:
            str: Dificultad del nivel ("easy", "medium" o "hard").
        """
        s = int(''.join(x for x in self.game.current_level if x.isdigit()))
        if s <= 20:
            return "easy"
        elif s <= 40:
            return "medium"
        else:
            return "hard"

    def draw(self, screen):
        """
        Dibuja la pantalla del juego.

        Args:
            screen (pygame.Surface): Superficie de la pantalla donde se dibuja el juego.
        """
        if self.game.nonogram is not None:
            self.game.nonogram.draw_grid(screen)
            self.game.nonogram.draw_cells(screen)
            self.draw_clues(screen)
            self.draw_timer(screen)
        else:
            font = pygame.font.Font(None, 36)
            message = font.render("No se cargó nivel.", True, (255, 0, 0))
            screen.blit(message, (300, 300))

        for button in self.buttons:
            button.draw(screen)

    def draw_clues(self, screen):
        """
        Dibuja las pistas del Nonogram en la pantalla.

        Args:
            screen (pygame.Surface): Superficie de la pantalla donde se dibujan las pistas.
        """
        font = pygame.font.Font(None, 24)
        for i, row_clue in enumerate(self.game.nonogram.row_clues):
            text = " ".join(map(str, row_clue))
            rendered = font.render(text, True, BLACK)
            screen.blit(rendered, (
                self.game.nonogram.grid_offset[0] - 10 - rendered.get_width(),
                self.game.nonogram.grid_offset[1] + i * self.game.nonogram.cell_size + self.game.nonogram.cell_size //2 - rendered.get_height() // 2
            ))

        for j, col_clue in enumerate(self.game.nonogram.col_clues):
            text_surfaces = [font.render(str(num), True, BLACK) for num in col_clue]
            total_height = sum(surface.get_height() for surface in text_surfaces)
            current_y = self.game.nonogram.grid_offset[1] - total_height - 10
            for surface in text_surfaces:
                screen.blit(surface, (
                    self.game.nonogram.grid_offset[0] + j * self.game.nonogram.cell_size + self.game.nonogram.cell_size //2 - surface.get_width() //2,
                    current_y
                ))
                current_y += surface.get_height()

    def draw_timer(self, screen):
        """
        Dibuja el temporizador en la pantalla del juego.

        Args:
            screen (pygame.Surface): Superficie de la pantalla donde se dibuja el temporizador.
        """
        font = pygame.font.Font(None, 36)
        timer_text = f"Time: {self.game.timer.get_time():.1f}s"
        rendered = font.render(timer_text, True, BLACK)
        timer_x = screen.get_width() - 150
        timer_y = self.buttons[0].rect.top - 50
        screen.blit(rendered, (timer_x, timer_y))

    def get_hint(self):
        """
        Proporciona una pista al jugador.
        """
        hint = self.game.get_hint()
        if hint:
            row, col, value = hint
            self.game.nonogram.player_grid[row][col] = value

    def return_to_menu(self):
        """
        Regresa al menú principal del juego.
        """
        self.game.set_screen('menu')